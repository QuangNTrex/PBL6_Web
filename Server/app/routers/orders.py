# routers/order.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# 🟢 Tạo đơn hàng kèm OrderDetail
@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        user_id=order.user_id,
        status=order.status,
        payment_method=order.payment_method,
        total_amount=order.total_amount,
        shipping_address=order.shipping_address,
        note=order.note,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # 🟢 Thêm order_details
    for detail in order.order_details:
        db_detail = models.OrderDetail(
            order_id=db_order.id,
            product_id=detail.product_id,
            quantity=detail.quantity,
            unit_price=detail.unit_price,
            total_price=detail.total_price,
            note=detail.note
        )
        db.add(db_detail)

    db.commit()
    db.refresh(db_order)
    return db_order


# 🟢 Lấy toàn bộ đơn hàng
@router.get("/", response_model=List[schemas.Order])
def get_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


# 🟢 Lấy đơn hàng theo ID
@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


# 🟢 Cập nhật đơn hàng (không động đến order_details ở đây)
@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = order_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order


# 🟢 Xóa đơn hàng + chi tiết
@router.delete("/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Xóa chi tiết trước
    db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).delete()
    db.delete(db_order)
    db.commit()
    return {"message": "Order and details deleted successfully"}
