import asyncio
from collections import deque


class OrdersQueue:
    def __init__(self):
        self.queue = deque()
        self.lock = asyncio.Lock()

    def put(self, order):
        self.queue.append(order)

    async def pop(self):
        async with self.lock:
            return self.queue.popleft()

    def empty(self) -> bool:
        return len(self.queue) == 0
