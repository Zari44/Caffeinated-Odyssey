from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from common import OrderStatus
from data import orders_queue, orders_storage
from logs import logger

barista_app = FastAPI()


@barista_app.get("/start/")
async def start() -> JSONResponse:
    if orders_queue.empty():
        raise HTTPException(status_code=404, detail="No pending orders to prepare")
    order_id = await orders_queue.pop()
    return JSONResponse(status_code=200, content={"order_id": order_id})


@barista_app.post("/finish/")
async def finish(order_id: str) -> JSONResponse:
    # when solving this problem I tried to achieve the level of abstraction that would allow just for attaching
    # some persistent storage without the change of the application logic - however not removing orders
    # from memory storage might result in memory overflow in this case
    order = orders_storage.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    if order.status == OrderStatus.FINISHED:
        # should never happen, but when it does - let's log this information as something really strange is going on
        logger.error("Trying to finish already finished order")
        raise HTTPException(status_code=400, detail="This order is already finished!")
    order.set_ready()
    return JSONResponse(status_code=200, content={"message": f"Order {order_id} is completed!"})
