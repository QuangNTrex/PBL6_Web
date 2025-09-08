from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

import enum

# ====== Enum ======
class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    customer = "customer"

class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"

class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipping = "shipping"
    completed = "completed"
    cancelled = "cancelled"

class PaymentMethod(str, enum.Enum):
    cash = "cash"
    credit_card = "credit_card"
    momo = "momo"
    zalopay = "zalopay"

# ====== User ======
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    role: Optional[UserRole] = UserRole.customer
    status: Optional[UserStatus] = UserStatus.active

class UserCreate(UserBase):
    password: str   # nhận mật khẩu thô để đăng ký

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[UserStatus] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ======= Auth ======

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    role: UserRole
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # thay thế cho orm_mode trong Pydantic v2

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ====== Category ======
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ====== Product ======
class ProductBase(BaseModel):
    code: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    unit: Optional[str] = "cái"
    image_path: Optional[str] = None
    category_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None
    image_path: Optional[str] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ====== OrderDetail ======
class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    note: Optional[str] = None

class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(BaseModel):
    quantity: Optional[int] = None
    note: Optional[str] = None

class OrderDetail(OrderDetailBase):
    id: int

    class Config:
        from_attributes = True

# ====== Order ======
class OrderBase(BaseModel):
    user_id: int
    status: Optional[OrderStatus] = OrderStatus.pending
    payment_method: Optional[PaymentMethod] = PaymentMethod.cash
    total_amount: float
    shipping_address: Optional[str] = None
    note: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    payment_method: Optional[PaymentMethod] = None
    shipping_address: Optional[str] = None
    note: Optional[str] = None

class Order(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    order_details: List[OrderDetail] = []

    class Config:
        from_attributes = True
