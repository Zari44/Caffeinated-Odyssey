import uuid

from fastapi import FastAPI
from starlette.responses import JSONResponse

from common import Order, OrderType
from data import orders_queue, orders_storage
from logs import logger

customer_app = FastAPI()


@customer_app.post("/order/")
async def order() -> JSONResponse:
    new_order = Order(order_type=OrderType.AMERICANO, order_id=str(uuid.uuid4()))
    logger.info(f"New order placed. Order id = {new_order.order_id}")
    orders_queue.put(new_order.order_id)
    orders_storage.insert(new_order)
    await new_order.wait()  # as stated in the task: server is waiting with the response until the order is finished
    return JSONResponse(status_code=200, content={"message": f"Order {new_order.order_id} is ready!"})
