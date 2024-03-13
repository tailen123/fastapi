# models.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .database import Base


class Order(Base):
    __tablename__ = "order_table"
    order_id = Column(Integer, primary_key=True, index=True)
    note = Column(String, unique=True)
