from fastapi import APIRouter, Depends, HTTPException

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@order_router.get("/")
async def hello():
    return {"message": "Hello, World!"}