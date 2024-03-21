from sqlalchemy.orm import Session
from fastapi import HTTPException
from ManageOrder.models import models_order
from ManageOrder.models import models_message, models_result
from ManageOrder.schemas import schemas_order, schemas_result, schemas_message

# def get_orders_from_db(db: Session, skip: int = 0, limit: int = 100):
#     orders = db.query(models_order.Order).filter(models_order.Order.flag_id == 1).offset(skip).limit(limit).all()
#     return orders


def get_message_by_order_id(db: Session, order_id: int):
    messages = db.query(models_message.Message).filter(models_message.Message.dialog_id == order_id,
                                                       models_message.Message.reason_type != "0").all()
    if messages is None:
        raise HTTPException(status_code=404,detail={"消息不存在"})
    else:
        return schemas_message.Message_list(messages=messages)

