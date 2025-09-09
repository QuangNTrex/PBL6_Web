from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Unicode, UnicodeText, Date
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, date   # 👈 sửa import ở đây
import enum
from enum import Enum as PyEnum


# ====== Enum ======
class UserRole(enum.Enum):
    admin = "admin"
    staff = "staff"
    customer = "customer"

class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"

class OrderStatus(PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    shipping = "shipping"
    completed = "completed"
    cancelled = "cancelled"

class PaymentMethod(PyEnum):
    cash = "cash"
    credit_card = "credit_card"
    momo = "momo"
    zalopay = "zalopay"


# ====== User ======
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Unicode(50), unique=True, index=True, nullable=False)
    email = Column(Unicode(100), unique=True, nullable=False)
    password_hash = Column(Unicode(255), nullable=False)   # mật khẩu đã mã hóa

    role = Column(Enum(UserRole), default=UserRole.customer)
    full_name = Column(Unicode(150), nullable=True)
    phone = Column(Unicode(20), nullable=True)
    address = Column(Unicode(250), nullable=True)
    avatar_url = Column(Unicode(2000), nullable=True)       # ảnh đại diện
    status = Column(Enum(UserStatus), default=UserStatus.active)

    birth_date = Column(Date, nullable=True)          # ngày sinh
    gender = Column(Integer, nullable=True)               # 0 = nữ, 1 = nam

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ: 1 user có nhiều orders
    orders = relationship("Order", back_populates="user")


# ====== Category ======
class Category(Base):
    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode(100), unique=True, nullable=False)   # Tên danh mục
    description = Column(Unicode(250), nullable=True)          # Mô tả thêm
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ: 1 Category có nhiều Product
    products = relationship("Product", back_populates="category")


# ====== Product ======
class Product(Base):
    __tablename__ = "Products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Unicode(50), unique=True, index=True, nullable=True)    # Mã sản phẩm (barcode / SKU)
    name = Column(Unicode(150), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    description = Column(Unicode(500), nullable=True)                   # Mô tả sản phẩm
    unit = Column(Unicode(50), default="cái")
    image_path = Column(Unicode(250), nullable=True)                    # Ảnh upload nội bộ
    category_id = Column(Integer, ForeignKey("Categories.id"))  

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ với Category
    category = relationship("Category", back_populates="products")

    # Quan hệ với OrderDetail
    order_details = relationship("OrderDetail", back_populates="product")


# ====== Order ======
class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)

    status = Column(Enum(OrderStatus, name="order_status"), default=OrderStatus.pending)
    payment_method = Column(Enum(PaymentMethod, name="payment_method"), default=PaymentMethod.cash)

    total_amount = Column(Float, nullable=False, default=0)
    shipping_address = Column(Unicode(250), nullable=True)
    note = Column(Unicode(250), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ: 1 Order thuộc 1 User
    user = relationship("User", back_populates="orders")

    # Quan hệ: 1 Order có nhiều OrderDetail
    order_details = relationship("OrderDetail", back_populates="order")


# ====== OrderDetail ======
class OrderDetail(Base):
    __tablename__ = "OrderDetails"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("Products.id"), nullable=False)

    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)   # giá tại thời điểm đặt hàng
    total_price = Column(Float, nullable=False)  # quantity * unit_price - discount
    note = Column(Unicode(250), nullable=True)

    # Quan hệ: mỗi OrderDetail thuộc 1 Order
    order = relationship("Order", back_populates="order_details")

    # Quan hệ: mỗi OrderDetail thuộc 1 Product
    product = relationship("Product", back_populates="order_details")
