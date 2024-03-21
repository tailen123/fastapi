# routes.py

from fastapi import APIRouter, Depends, FastAPI

from ManageOrder.crud.crud_order import get_orders_from_db, get_order_by_id, delete_order, update_order, create_order
from sqlalchemy.orm import Session
from ManageOrder.database.databases_order import get_db
from fastapi import FastAPI, Depends, HTTPException, status, Request

from ManageOrder.middleware.middleware import auth_check
from ManageOrder.schemas import schemas_order

router = APIRouter(dependencies=[Depends(auth_check)])


@router.get("/", response_model=schemas_order.Order_list)
async def get_orders(db: Session = Depends(get_db)):
    orders = get_orders_from_db(db)
    return orders


@router.get("/orders/{order_id}", response_model=schemas_order.Order)
async def get_one_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db, order_id=order_id)
    return order


@router.post("/orders/", response_model=schemas_order.Order)
async def create_new_item(order_id: int, note: str, db: Session = Depends(get_db)):
    return create_order(db, order_id=order_id, note=note)


@router.patch("/orders/{order_id}", response_model=schemas_order.Order)
async def update_note(order_id: int, new_note: str, db: Session = Depends(get_db)):
    return update_order(db, order_id=order_id, new_note=new_note)


@router.delete("/orders/{order_id}", response_model=schemas_order.Order)
async def delete_order_by_order_id(order_id: int, db: Session = Depends(get_db)):
    return delete_order(db, order_id=order_id)
