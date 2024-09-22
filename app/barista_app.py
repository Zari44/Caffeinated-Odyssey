from fastapi import FastAPI, HTTPException

from common import OrderStatus
from data import orders_queue, orders_storage

barista_app = FastAPI()


@barista_app.get("/start/")
async def start():
    if orders_queue.empty():
        raise HTTPException(status_code=404, detail="No pending orders to prepare")
    order_id = await orders_queue.pop()
    return {"order_id": order_id}


@barista_app.post("/finish/")
async def finish(order_id: str):
    order = orders_storage.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    if order.status == OrderStatus.FINISHED:
        raise HTTPException(status_code=400, detail="This order is already finished!")
    order.set_ready()
    return {"message": f"Order {order_id} is completed!"}
