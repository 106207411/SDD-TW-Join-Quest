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
    
    def set_threshold_discount(self, threshold: float, discount: float):
        """Configure threshold discount promotion."""
        self.threshold_discount_threshold = threshold
        self.threshold_discount_amount = discount
    
    def set_buy_one_get_one_cosmetics(self, enabled: bool):
        """Configure buy one get one promotion for cosmetics."""
        self.buy_one_get_one_cosmetics = enabled
    
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
        discount = 0
        if (self.threshold_discount_threshold is not None and 
            self.threshold_discount_amount is not None and
            order.original_amount >= self.threshold_discount_threshold):
            discount = self.threshold_discount_amount
        
        order.discount = discount
        order.total_amount = order.original_amount - discount
