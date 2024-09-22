import asyncio

from uvicorn import Config, Server

from barista_app import barista_app
from customer_app import customer_app


async def start_servers():
    config_client = Config(app=customer_app, host="0.0.0.0", port=8000)
    config_worker = Config(app=barista_app, host="0.0.0.0", port=8001)

    server_client = Server(config_client)
    server_worker = Server(config_worker)

    await asyncio.gather(
        server_client.serve(),
        server_worker.serve(),
    )


if __name__ == "__main__":
    asyncio.run(start_servers())
