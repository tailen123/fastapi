import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from test import crud, models, schemas
from test.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 增加
@app.post("/orders/", response_model=schemas.Order)
def create_order_api(order_id: int, note: str, db: Session = Depends(get_db)):
    db_order = crud.get_order_by_id(db, order_id=order_id)
    if db_order:
        raise HTTPException(status_code=400, detail="已经注册")
    db_order=crud.create_order(db, order_id=order_id,note=note)
    return db_order


@app.patch("/orders/{order_id}/", response_model=schemas.Order)
def update_note(order_id: int, new_note: str, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id=order_id, new_note=new_note)
    return db_order


@app.get("/", response_model=list[schemas.Order])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders


@app.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id)
    return db_order


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
