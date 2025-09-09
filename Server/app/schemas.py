from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
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

#----- Token -----
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


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
    birth_date: Optional[date] = None
    gender: Optional[int] = None   # 0 = nữ, 1 = nam

class UserCreate(UserBase):
    password: str   # mật khẩu thô để đăng ký

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[UserStatus] = None
    birth_date: Optional[date] = None
    gender: Optional[int] = None

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ======= Auth ======
class UserLogin(BaseModel):
    username: str
    password: str

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
    birth_date: Optional[date] = None
    gender: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# ====== Category ======
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None   # 👈 thêm field

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None   # 👈 thêm field

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryOut(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
    user_id: Optional[int] = None      # 👈 thêm field

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
    user_id: Optional[int] = None      # 👈 thêm field

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductOut(BaseModel):
    id: int
    code: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    unit: Optional[str] = "cái"
    image_path: Optional[str] = None
    category_id: Optional[int] = None
    user_id: Optional[int] = None       # 👈 thêm field
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
