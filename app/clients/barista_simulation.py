import asyncio
import os
from urllib.parse import urljoin

import aiohttp
from aiohttp import TCPConnector

BASE_SERVER_URL = os.getenv("BASE_SERVER_URL", "http://localhost")
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "10"))


async def brew_coffee(worker_id: int):
    connector = TCPConnector(limit_per_host=NUM_WORKERS)
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            print(f"Worker {worker_id} getting a new task to work on")
            async with session.get(urljoin(BASE_SERVER_URL, "/start/")) as response:
                if response.status == 200:
                    json_response = await response.json()
                    print(f"Worker {worker_id} started: {json_response}")
                else:
                    print(f"Worker{worker_id} received error: {response.status}")
                    continue
            # wait for cofee to brew
            order_id = json_response["order_id"]
            await asyncio.sleep(1)
            # Automatically call finish endpoint
            async with session.post(urljoin(BASE_SERVER_URL, f"/finish/?order_id={order_id}")) as resp:
                if resp.status == 200:
                    print(f"Worker {worker_id} finished brewing coffee")
                else:
                    print(f"Error finishing order {order_id}: {resp.status}")


async def simulate_workers(num_workers):
    tasks = []
    for i in range(num_workers):
        print(f"Creating task {i}")
        tasks.append(brew_coffee(i))
        # await asyncio.sleep(1)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(simulate_workers(NUM_WORKERS))
