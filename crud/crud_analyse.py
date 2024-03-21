from fastapi import HTTPException
from sqlalchemy.orm import Session
from ManageOrder.models import models_order
from ManageOrder.models import models_message, models_result
from ManageOrder.schemas import schemas_order, schemas_result, schemas_message


def get_data_analyse(db:Session,message_id:int):
    db_ctx=db.query(models_message.Message).filter(models_message.Message.message_id==message_id
                                                   ,models_message.Message.reason_type!=0).first()
    