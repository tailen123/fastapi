from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import models_message, models_result
from schemas import schemas_order, schemas_result, schemas_message



def get_message_by_order_id(db: Session, order_id: int):
    messages = db.query(models_message.Message).filter(models_message.Message.dialog_id == order_id,
                                                       models_message.Message.reason_type != 0).all()
    if messages is None:
        raise HTTPException(status_code=404,detail={"消息不存在"})
    else:
        return schemas_message.Message_list(messages=messages)

