# models.py
from sqlalchemy import Column, Integer, String, CheckConstraint
from ManageOrder.database.databases_order import Base


class Result(Base):
    __tablename__ = "result_table"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    text_zh = Column(String)
    score = Column(Integer)
    source = Column(String)
    is_del = Column(Integer)
    result_id = Column(Integer)
    message_id = Column(Integer)
    __table_args__ = (
        CheckConstraint('score IN (0, 1, 2)', name='score_check'),
    )


class Acc(Base):
    __tablename__ = "acc_view"
    message_id = Column(Integer,primary_key=True)
    source = Column(String)
    todonums = Column(Integer)
    onenums = Column(Integer)
    twonums = Column(Integer)
    total = Column(Integer)
