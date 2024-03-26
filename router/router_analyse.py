from fastapi import APIRouter, Depends, FastAPI, Query

from crud.crud_analyse import get_ctxdata_analyse, get_reason_type_analyse, get_all_analyse, \
    get_model_analyse


from sqlalchemy.orm import Session
from database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request

from middleware.middleware import auth_check

router = APIRouter(dependencies=[Depends(auth_check)])


@router.get("/analyse_by_ctx")
def get_hard_level_by_ctx(message_id: int, hard_level: float , db: Session = Depends(get_db)):
    return get_ctxdata_analyse(db, message_id=message_id, diff_level=hard_level)


@router.get("/analyse_by_reason_type")
def get_hardset_by_one_reason_type(reason_type: int, hard_level: float,
                                   db: Session = Depends(get_db)):
    return get_reason_type_analyse(db, reason_type=reason_type, diff_level=hard_level)


@router.get("/analyse_all")
def get_all_ctx_analyse(hard_level: float, db: Session = Depends(get_db)):
    return get_all_analyse(db, diff_level=hard_level)


@router.get("/model_analyse")
def get_analyse_by_model(modelA: str, modelB: str, reason_type: list[int] = Query(...), db: Session = Depends(get_db)):
    return get_model_analyse(db, modelA=modelA, modelB=modelB, reason_type=reason_type)
