

from pydantic import BaseModel,Field


class OrderBase(BaseModel):
    order_id: int
    note: str


class OrderCreate(OrderBase):
    flag_id: int = Field(..., ge=0, le=1)


class Order(OrderBase):
    order_id: int

    class Config:
        from_attributes = True


class Order_list(BaseModel):
    orders: list[Order]
