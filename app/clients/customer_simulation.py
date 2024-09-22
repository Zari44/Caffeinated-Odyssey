import asyncio
import os
import random
from urllib.parse import urljoin

import aiohttp

BASE_SERVER_URL = os.getenv("BASE_SERVER_URL", "http://localhost")


async def place_single_order(client_id):
    print(f"Client {client_id} placing an order.")
    async with aiohttp.ClientSession() as session:
        async with session.post(urljoin(BASE_SERVER_URL, "order")) as response:
            if response.status == 200:
                print(f"Client {client_id} received: {await response.json()}")
            else:
                print(f"Client {client_id} received error: {response.status}")


async def main():
    all_order_tasks = []
    for c in range(100):
        who_next_client = random.randint(0, 1)
        if who_next_client == 0:
            # Normal client
            task = asyncio.create_task(place_single_order(f"Normal_{c}"))
            all_order_tasks.append(task)
        elif who_next_client == 1:
            # Groupie clients
            group_num = random.randint(10, 20)
            print(f"Group size: {group_num}")
            for i in range(group_num):
                task = asyncio.create_task(place_single_order(f"Group_{c}_{i}"))
                all_order_tasks.append(task)
        wait_for_next_client_seconds = random.randint(1, 2)
        await asyncio.sleep(wait_for_next_client_seconds)  # Pause between client arrivals
    print("Awaiting all tasks...")
    for task in all_order_tasks:
        await task


# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
