from fastapi import APIRouter, Depends, FastAPI, Query

from ManageOrder.crud.crud_order import get_orders_from_db, get_order_by_id, delete_order, update_order, create_order
from ManageOrder.crud.crud_message import get_message_by_order_id
from ManageOrder.crud.crud_result import get_result_by_ctx_id, update_score_by_result_id, get_sources, \
    get_todoresult_by_message_id
from ManageOrder.crud.crud_analyse import get_ctxdata_analyse, get_reason_type_analyse, get_all_analyse

from sqlalchemy.orm import Session
from ManageOrder.database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request
from ManageOrder.schemas.schemas_order import Order, Order_list
from ManageOrder.schemas.schemas_message import Message, Message_list
from ManageOrder.schemas.schemas_result import Result, Result_list, Acc, Hard
from ManageOrder.middleware.middleware import auth_check

router = APIRouter(dependencies=[Depends(auth_check)])


@router.get("/analyse_by_ctx")
def get_hard_level_by_ctx(message_id: int, hard_level: float, db: Session = Depends(get_db)):
    return get_ctxdata_analyse(db, message_id=message_id, diff_level=hard_level)


@router.get("/analyse_by_reason_type")
def get_hardset_by_one_reason_type(reason_type: int, hard_level: float, db: Session = Depends(get_db)):
    return get_reason_type_analyse(db, reason_type=reason_type, diff_level=hard_level)


@router.get("analyse_all")
def get_all_analyse(hard_level: float, db: Session = Depends(get_db)):
    return get_all_analyse(db, diff_level=hard_level)
