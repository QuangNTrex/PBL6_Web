from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/order-details",
    tags=["OrderDetails"]
)

@router.post("/", response_model=schemas.OrderDetail)
def create_order_detail(order_detail: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    return crud.order_detail.create_order_detail(db=db, order_detail=order_detail)

@router.get("/", response_model=List[schemas.OrderDetail])
def read_order_details(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.order_detail.get_order_details(db=db, skip=skip, limit=limit)

@router.get("/{order_detail_id}", response_model=schemas.OrderDetail)
def read_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = crud.order_detail.get_order_detail(db, order_detail_id)
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return db_order_detail

@router.put("/{order_detail_id}", response_model=schemas.OrderDetail)
def update_order_detail(order_detail_id: int, order_detail: schemas.OrderDetailUpdate, db: Session = Depends(get_db)):
    db_order_detail = crud.order_detail.update_order_detail(db, order_detail_id, order_detail)
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return db_order_detail

@router.delete("/{order_detail_id}")
def delete_order_detail(order_detail_id: int, db: Session = Depends(get_db)):
    db_order_detail = crud.order_detail.delete_order_detail(db, order_detail_id)
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return {"detail": "OrderDetail deleted"}
