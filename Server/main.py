from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models
from app.routers import users, categories, order_details, products, orders, auth, statistics, cart, stream

app = FastAPI()

# CORS
origins = [
    "http://localhost:3000",  # React/Next.js dev server
    # Có thể thêm domain deploy thật sau này (VD: https://myshop.com)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Cho phép tất cả method: GET, POST, PUT, DELETE...
    allow_headers=["*"],   # Cho phép tất cả headers
)

# Tạo bảng
Base.metadata.create_all(bind=engine)

# Router
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(order_details.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(statistics.router)
app.include_router(cart.router)
app.include_router(stream.router)
