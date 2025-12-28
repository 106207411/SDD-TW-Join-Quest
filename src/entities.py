"""Domain entities for the order system."""
from __future__ import annotations
from typing import Dict, List


class Product:
    """Product entity."""
    
    def __init__(self, name: str, unit_price: float, category: str = ""):
        self.name = name
        self.unit_price = unit_price
        self.category = category


class OrderItem:
    """Order item entity."""
    
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        self.product = product
        self.quantity = quantity


class Order:
    """Order entity."""
    
    def __init__(self):
        self.total_amount: float = 0
        self.original_amount: float = 0
        self.discount: float = 0
        self.items: List[OrderItem] = []
        self.received_items: Dict[str, int] = {}
