from fastapi import APIRouter, Depends, FastAPI


from crud.crud_message import get_message_by_order_id

from sqlalchemy.orm import Session
from database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request
from schemas.schemas_order import Order, Order_list
from schemas.schemas_message import Message, Message_list
from middleware.middleware import auth_check


router = APIRouter(dependencies=[Depends(auth_check)])


@router.get("/messages", response_model=Message_list)
def get_messages_by_order_id(order_id: int, db: Session = Depends(get_db)):
    return get_message_by_order_id(db, order_id=order_id)
