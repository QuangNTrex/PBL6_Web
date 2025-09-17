from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from typing import List, Dict, Any

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/statistics", tags=["Statistics"])

# 🟢 1. Thống kê tổng quan
@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    total_products = db.query(func.count(models.Product.id)).scalar()
    total_orders = db.query(func.count(models.Order.id)).scalar()
    total_revenue = db.query(func.coalesce(func.sum(models.Order.total_amount), 0)).scalar()
    total_customers = db.query(func.count(models.User.id)).filter(models.User.role == "customer").scalar()

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_customers": total_customers
    }


# 🟢 2. Doanh thu theo tháng trong năm (tham số: year)
@router.get("/revenue-by-month")
def revenue_by_month(year: int, db: Session = Depends(get_db)):
    month_expr = extract("month", models.Order.created_at)

    revenues = (
        db.query(
            month_expr.label("month"),
            func.coalesce(func.sum(models.Order.total_amount), 0).label("revenue")
        )
        .filter(extract("year", models.Order.created_at) == year)
        .group_by(month_expr)          # ✅ dùng lại biểu thức
        .order_by(month_expr)          # ✅ dùng lại biểu thức
        .all()
    )

    return [{"month": int(month), "revenue": float(revenue)} for month, revenue in revenues]


# 🟢 3. Tỉ lệ đơn hàng theo trạng thái (Pie chart) trong tháng hiện tại
@router.get("/order-status-ratio")
def order_status_ratio(db: Session = Depends(get_db)):
    now = datetime.now()
    results = (
        db.query(models.Order.status, func.count(models.Order.id).label("count"))
        .filter(
            extract("year", models.Order.created_at) == now.year,
            extract("month", models.Order.created_at) == now.month
        )
        .group_by(models.Order.status)
        .all()
    )

    total = sum(count for _, count in results) or 1  # tránh chia cho 0
    return [
        {"status": status, "count": count, "ratio": round(count / total * 100, 2)}
        for status, count in results
    ]


# 🟢 4. 5 đơn hàng gần nhất
@router.get("/latest-orders", response_model=List[schemas.Order])
def get_latest_orders(db: Session = Depends(get_db)):
    orders = (
        db.query(models.Order)
        .order_by(models.Order.created_at.desc())
        .limit(5)
        .all()
    )
    return orders


# 🟢 5. 5 khách hàng mới đăng ký
@router.get("/latest-customers", response_model=List[schemas.UserOut])
def get_latest_customers(db: Session = Depends(get_db)):
    users = (
        db.query(models.User)
        .filter(models.User.role == "customer")
        .order_by(models.User.created_at.desc())
        .limit(5)
        .all()
    )
    return users
