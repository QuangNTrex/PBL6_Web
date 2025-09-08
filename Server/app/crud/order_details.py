from sqlalchemy.orm import Session
from app import models, schemas

def create_order_detail(db: Session, order_detail: schemas.OrderDetailCreate):
    db_order_detail = models.OrderDetail(
        order_id=order_detail.order_id,
        product_id=order_detail.product_id,
        quantity=order_detail.quantity,
        unit_price=order_detail.unit_price,
        total_price=order_detail.total_price,
        note=order_detail.note,
    )
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail

def get_order_details(db: Session, order_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()

def get_order_detail(db: Session, detail_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id).first()

def update_order_detail(db: Session, detail_id: int, order_detail: schemas.OrderDetailUpdate):
    db_detail = get_order_detail(db, detail_id)
    if not db_detail:
        return None
    for key, value in order_detail.dict(exclude_unset=True).items():
        setattr(db_detail, key, value)
    db.commit()
    db.refresh(db_detail)
    return db_detail

def delete_order_detail(db: Session, detail_id: int):
    db_detail = get_order_detail(db, detail_id)
    if not db_detail:
        return None
    db.delete(db_detail)
    db.commit()
    return db_detail
