"""Order service for handling checkout and promotions."""
from __future__ import annotations
from typing import List
from src.entities import Order, OrderItem


class OrderService:
    """Service for processing orders with promotions."""
    
    def __init__(self):
        self.threshold_discount_threshold = None
        self.threshold_discount_amount = None
        self.buy_one_get_one_cosmetics = False
        self.double11_group_size = None
        self.double11_discount_rate = None
    
    def set_threshold_discount(self, threshold: float, discount: float):
        """Configure threshold discount promotion."""
        self.threshold_discount_threshold = threshold
        self.threshold_discount_amount = discount
    
    def set_buy_one_get_one_cosmetics(self, enabled: bool):
        """Configure buy one get one promotion for cosmetics."""
        self.buy_one_get_one_cosmetics = enabled
    
    def set_double11_bulk_discount(self, group_size: int, discount_rate: float):
        """Configure Double 11 bulk discount promotion."""
        self.double11_group_size = group_size
        self.double11_discount_rate = discount_rate
    
    def checkout(self, items: List[OrderItem]) -> Order:
        """
        Build order and calculate order's total amount based on discount offers.
        
        Args:
            items: List of order items
            
        Returns:
            Order with calculated amounts
        """
        order = Order()
        order.items = items
        
        # Calculate original amount and track purchased items
        self._calculate_original_amount(order, items)
        
        # Apply promotions
        self._apply_buy_one_get_one_promotion(order, items)
        self._apply_double11_bulk_discount(order, items)
        self._apply_threshold_discount(order)
        
        return order
    
    def _calculate_original_amount(self, order: Order, items: List[OrderItem]) -> None:
        """Calculate original amount and initialize received items."""
        total = 0
        for item in items:
            total += item.product.unit_price * item.quantity
            order.received_items[item.product.name] = item.quantity
        order.original_amount = total
    
    def _apply_buy_one_get_one_promotion(self, order: Order, items: List[OrderItem]) -> None:
        """Apply buy one get one promotion for cosmetics."""
        if self.buy_one_get_one_cosmetics:
            for item in items:
                if item.product.category == 'cosmetics':
                    # Add 1 free item per cosmetic product (not per quantity)
                    order.received_items[item.product.name] += 1
    
    def _apply_threshold_discount(self, order: Order) -> None:
        """Apply threshold discount if applicable."""
        additional_discount = 0
        if (self.threshold_discount_threshold is not None and 
            self.threshold_discount_amount is not None and
            order.original_amount >= self.threshold_discount_threshold):
            additional_discount = self.threshold_discount_amount
        
        order.discount += additional_discount
        order.total_amount = order.original_amount - order.discount
    
    def _apply_double11_bulk_discount(self, order: Order, items: List[OrderItem]) -> None:
        """Apply Double 11 bulk discount for same product purchases."""
        if self.double11_group_size is None or self.double11_discount_rate is None:
            return
        
        # Calculate discount for each product
        total_discount = 0
        for item in items:
            quantity = item.quantity
            unit_price = item.product.unit_price
            
            # Calculate how many complete groups of group_size
            complete_groups = quantity // self.double11_group_size
            remaining_items = quantity % self.double11_group_size
            
            # Discount applies only to complete groups
            if complete_groups > 0:
                discount_per_group = self.double11_group_size * unit_price * (self.double11_discount_rate / 100)
                total_discount += complete_groups * discount_per_group
        
        order.discount = total_discount
        order.total_amount = order.original_amount - total_discount
