import asyncio
import os
import random
from urllib.parse import urljoin

import aiohttp

BASE_SERVER_URL = os.getenv("BASE_SERVER_URL", "http://localhost")
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "10"))
BREW_TIME_MIN = int(os.getenv("BREW_TIME_MIN", "30"))
BREW_TIME_MAX = int(os.getenv("BREW_TIME_MAX", "60"))


async def brew_coffee(worker_id: int) -> None:
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(urljoin(BASE_SERVER_URL, "/start/")) as response:
                if response.status == 200:
                    json_response = await response.json()
                    print(f"Worker {worker_id} started: {json_response}")
                else:
                    print(f"Worker {worker_id} received error: {response.status}")
                    if response.status == 404:
                        # very simple backoff - if no new orders to process, sleep for a while before next request
                        await asyncio.sleep(1)
                    continue

            # wait for coffe to brew
            order_id = json_response["order_id"]
            caffe_brew_time = random.randint(BREW_TIME_MIN, BREW_TIME_MAX)
            print(f"Worker {worker_id} brewing coffe for {caffe_brew_time}s ...")
            await asyncio.sleep(caffe_brew_time)

            async with session.post(urljoin(BASE_SERVER_URL, f"/finish/?order_id={order_id}")) as resp:
                if resp.status == 200:
                    print(f"Worker {worker_id} finished brewing coffee")
                else:
                    print(f"Error finishing order {order_id}: {resp.status}")


async def simulate_workers(num_workers: int) -> None:
    tasks = []
    for i in range(num_workers):
        print(f"Creating worker {i}")
        tasks.append(brew_coffee(i))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(simulate_workers(NUM_WORKERS))
