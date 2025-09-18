from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, UserRole, UserStatus
from ..schemas import UserCreate, UserLogin, LoginResponse, UserOut, ChangePasswordRequest
from ..core.auth_utils import verify_password, get_password_hash, create_access_token, pwd_context
from ..core.auth_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# 🟢 Đăng ký
@router.post("/register", response_model=LoginResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed_password,
        full_name=user_in.full_name,
        role=UserRole.customer,
        status=UserStatus.active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserOut.model_validate(new_user)
    )

# 🟢 Đăng nhập
@router.post("/login", response_model=LoginResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if user.status != UserStatus.active:
        raise HTTPException(status_code=403, detail="User is inactive")

    access_token = create_access_token(data={"sub": str(user.id)})
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserOut.model_validate(user)
    )

# 🟢 Đăng xuất
@router.get("/logout")
def logout():
    return {"message": "Logout successful. Please remove token on client."}

# 🟢 Đổi mật khẩu
@router.put("/change-password")
def change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(req.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.password_hash = pwd_context.hash(req.new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}

# 🟢 Lấy thông tin user hiện tại
@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
