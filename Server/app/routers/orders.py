# routers/order.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from ..core.auth_middleware import get_current_user
import paho.mqtt.client as mqtt
import json

# ========== MQTT Setup ==========
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "pbl6/products"

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT Orders] Connected successfully to broker.")
    else:
        print(f"[MQTT Orders] Failed to connect, return code {rc}")

try:
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
except Exception as e:
    print(f"[ERROR] Could not start MQTT client in orders.py: {e}")
# ==============================

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

    # --- Send Total Price via MQTT ---
    try:
        payload = {
            "label": "Thanh Tien",
            "price": order.total_amount,
            "quantity": 0
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"[MQTT] Published Total Price to {MQTT_TOPIC}: {payload}")
    except Exception as e:
        print(f"[ERROR] Failed to publish total price via MQTT: {e}")
    # ---------------------------------

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

# 🟢 Lấy đơn hàng theo user_id
@router.get("/user/{user_id}", response_model=List[schemas.Order])
def get_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.user_id == user_id).all()
    if not orders:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng nào cho user này")
    return orders


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

#huy don hang tu nguoi dung
@router.put("/{order_id}/cancel", response_model=schemas.Order)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    API: Người dùng hủy đơn hàng của chính mình
    """
    # Lấy đơn hàng thuộc về user
    print(current_user.id)
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found or not owned by user")

    if order.status in [schemas.OrderStatus.shipping, schemas.OrderStatus.completed]:
        raise HTTPException(status_code=400, detail="Order cannot be canceled at this stage")

    # Cập nhật trạng thái
    order.status = schemas.OrderStatus.cancelled
    db.commit()
    db.refresh(order)

    return order