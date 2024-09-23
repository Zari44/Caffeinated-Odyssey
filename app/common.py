import asyncio
import enum


# this is not 100% needed for the scope presented in the task
# however in my solution I wanted to imitate the solution
# that would work very similar to when some persistent
# storage was used for storing orders - in such a case I
# guess we would like to have an information on the orders
class OrderStatus(str, enum.Enum):
    IN_PREPARATION = "IN_PREPARATION"
    FINISHED = "FINISHED"


# Currently we only have one type of coffe to brew, but hey,
# when we grow we probably can serve more types
class OrderType(str, enum.Enum):
    AMERICANO = "AMERICANO"


class Order:
    def __init__(self, order_type: OrderType, order_id: str) -> None:
        self.event = asyncio.Event()
        self.type = order_type
        self.order_id = order_id
        self.status = OrderStatus.IN_PREPARATION

    async def wait(self) -> None:
        await self.event.wait()

    def set_ready(self) -> None:
        self.status = OrderStatus.FINISHED
        self.event.set()
