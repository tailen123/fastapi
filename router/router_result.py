from enum import Enum
from typing import Literal

from fastapi import APIRouter, Depends, FastAPI, Query

from ManageOrder.crud.crud_order import get_orders_from_db, get_order_by_id, delete_order, update_order, create_order
from ManageOrder.crud.crud_message import get_message_by_order_id
from ManageOrder.crud.crud_result import get_result_by_ctx_id, update_score_by_result_id, get_sources, \
    get_todoresult_by_message_id

from sqlalchemy.orm import Session
from ManageOrder.database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request
from ManageOrder.schemas.schemas_order import Order, Order_list
from ManageOrder.schemas.schemas_message import Message, Message_list
from ManageOrder.schemas.schemas_result import Result, Result_list, Acc
from ManageOrder.middleware.middleware import auth_check

router = APIRouter(dependencies=[Depends(auth_check)])

source_list = Literal[
    "psychic-sft.13b.mscwsum.5_sum.5_airo.5_insight.5.e1",
    "psychic-7bv2-all.251k.20231003",
    "ct2.3b",
    "1.3b_pytorch",
    "psychic-13bv2-all.225k.20231012",
    "psychic-sft.7b.mscwsum.5_sum.5_airo.5_insight.5.e1"
]

@router.get("/{message_id}", response_model=Result_list)
def get_results_by_message_id(message_id: int,
                              source: source_list =
                              Query("psychic-sft.13b.mscwsum.5_sum.5_airo.5_insight.5.e1", enum=[
                                  "psychic-sft.13b.mscwsum.5_sum.5_airo.5_insight.5.e1",
                                  "psychic-7bv2-all.251k.20231003",
                                  "ct2.3b",
                                  "1.3b_pytorch",
                                  "psychic-13bv2-all.225k.20231012",
                                  "psychic-sft.7b.mscwsum.5_sum.5_airo.5_insight.5.e1"
                              ]), db: Session = Depends(get_db)):
    return get_result_by_ctx_id(db, message_id=message_id, source=source)


@router.patch("/{result_id}", response_model=Result)
def update_score_by_result_id1(result_id: int, score: int, db: Session = Depends(get_db)):
    return update_score_by_result_id(db, result_id=result_id, score=score)


@router.get("/")
def get_source(db: Session = Depends(get_db)):
    return get_sources(db)


@router.get("/todonums/")
def get_todo_nums(message_id: int,
                  source: source_list =
                  Query("psychic-sft.13b.mscwsum.5_sum.5_airo.5_insight.5.e1", enum=[
                      "psychic-sft.13b.mscwsum.5_sum.5_airo.5_insight.5.e1",
                      "psychic-7bv2-all.251k.20231003",
                      "ct2.3b",
                      "1.3b_pytorch",
                      "psychic-13bv2-all.225k.20231012",
                      "psychic-sft.7b.mscwsum.5_sum.5_airo.5_insight.5.e1"
                  ]), db: Session = Depends(get_db)):
    return get_todoresult_by_message_id(db, message_id=message_id, source=source)
