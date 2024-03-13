from pydantic import BaseModel


class OrderBase(BaseModel):
    order_id: int
    note: str


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    order_id: int

    class Config:
        from_attributes = True
