from typing import Optional

from common import Order


# abstraction on any persistent storage that could be used in production system
class OrdersStorage:
    def __init__(self):
        self.orders: dict[str, Order] = {}

    def get(self, order_id: str) -> Optional[Order]:
        return self.orders.get(order_id, None)

    def insert(self, order: Order) -> None:
        self.orders[order.order_id] = order
