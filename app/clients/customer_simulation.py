import asyncio
import os
import random
from urllib.parse import urljoin

import aiohttp

BASE_SERVER_URL = os.getenv("BASE_SERVER_URL", "http://localhost")
GROUP_MIN = int(os.getenv("GROUP_MIN", "100"))
GROUP_MAX = int(os.getenv("GROUP_MAX", "200"))

TIME_BETWEEN_CLIENTS_MIN_SEC = int(os.getenv("TIME_BETWEEN_CLIENTS_MIN", "10"))
TIME_BETWEEN_CLIENTS_MAX_SEC = int(os.getenv("TIME_BETWEEN_CLIENTS_MAX", "20"))

NUM_CLIENTS_KINDS_SERVED = int(os.getenv("NUM_CLIENTS_KINDS_SERVED", "100"))


async def place_single_order(client_id: str) -> None:
    print(f"Client {client_id} placing an order.")
    async with aiohttp.ClientSession() as session:
        async with session.post(urljoin(BASE_SERVER_URL, "order")) as response:
            if response.status == 200:
                print(f"Client {client_id} received: {await response.json()}")
            else:
                print(f"Client {client_id} received error: {response.status}")


async def main() -> None:
    all_order_tasks = []
    for c in range(NUM_CLIENTS_KINDS_SERVED):
        who_next_client = random.randint(0, 1)
        if who_next_client == 0:
            print("Single client comes for the caffe")
            task = asyncio.create_task(place_single_order(f"Normal_{c}"))
            all_order_tasks.append(task)
        elif who_next_client == 1:
            group_num = random.randint(GROUP_MIN, GROUP_MAX)
            print(f"Group size: {group_num} come for the caffe")
            for i in range(group_num):
                task = asyncio.create_task(place_single_order(f"Group_{c}_{i}"))
                all_order_tasks.append(task)
        elif who_next_client == 2:
            num_orders = random.randint(1000, 5000)
            print(f"Delusional client comes for the caffe and orders: {num_orders}")
            for i in range(num_orders):
                task = asyncio.create_task(place_single_order(f"Delusional_{c}_{i}"))
                all_order_tasks.append(task)
        time_till_next_client = random.randint(TIME_BETWEEN_CLIENTS_MIN_SEC, TIME_BETWEEN_CLIENTS_MAX_SEC)
        print(f"Waiting for the next client for {time_till_next_client}...")
        await asyncio.sleep(time_till_next_client)
    print("Awaiting all tasks...")
    for task in all_order_tasks:
        await task


# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
