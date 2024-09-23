import asyncio
from collections import deque
from typing import Deque


# abstraction on any queue that might be used on production system -
class OrdersQueue:
    def __init__(self) -> None:
        self.queue: Deque[str] = deque()
        self.lock = asyncio.Lock()

    def put(self, order: str) -> None:
        self.queue.append(order)

    async def pop(self) -> str:
        async with self.lock:
            return self.queue.popleft()

    def empty(self) -> bool:
        return len(self.queue) == 0
