from sqlalchemy.orm import Session
from . import models, schemas


# 获取多个订单
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()


# 创建订单
def create_order(db: Session, order_id:int,note:str):
    db_order = models.Order(note=note, order_id=order_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# 查询订单
def get_order_by_id(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    return db_order


# 删除订单

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    db.delete(db_order)
    db.commit()
    return db_order


# 修改订单

def update_order(db: Session, order_id: int, new_note: str):
    db_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    db_order.note = new_note
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
