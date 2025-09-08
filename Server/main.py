from fastapi import FastAPI
from app.database import Base, engine
import app.models as models
from app.routers import users, categories, order_details, products, orders, auth

app = FastAPI(title="PBL6 API",
    description="API cho hệ thống bán hàng (Users, Products, Orders...)",
    version="1.0.0",
)

# include tất cả routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(order_details.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)


# Tạo bảng trong DB (nếu chưa có)
Base.metadata.create_all(bind=engine)
