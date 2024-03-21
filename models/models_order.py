# models.py

from sqlalchemy import Column, Integer, String
from ManageOrder.database.databases_order import Base


class Order(Base):
    __tablename__ = "order_table"

    order_id = Column(Integer, primary_key=True)
    note = Column(String)
    flag_id = Column(Integer)
