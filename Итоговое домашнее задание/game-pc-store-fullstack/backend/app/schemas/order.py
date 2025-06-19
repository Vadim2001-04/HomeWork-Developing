from pydantic import BaseModel
from typing import List

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemBase]

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    items: list[OrderItem] = []

    class Config:
        orm_mode = True