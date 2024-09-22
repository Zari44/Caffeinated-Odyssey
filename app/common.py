import asyncio
import enum


class OrderStatus(str, enum.Enum):
    IN_PREPARATION = "IN_PREPARATION"
    FINISHED = "FINISHED"


# Currently we only have one type of coffe to brew, but hey,
# when we grow we probably can serve more types
class OrderType(str, enum.Enum):
    AMERICANO = "AMERICANO"


class Order:
    def __init__(self, order_type: OrderType, order_id: str):
        self.event = asyncio.Event()
        self.type = order_type
        self.order_id = order_id
        self.status = OrderStatus.IN_PREPARATION

    async def wait(self):
        await self.event.wait()

    def set_ready(self):
        self.status = OrderStatus.FINISHED
        self.event.set()
