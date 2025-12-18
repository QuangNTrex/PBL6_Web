from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import EmailVerificationCode, User, UserRole, UserStatus
from ..schemas import UserCreate, UserLogin, LoginResponse, UserOut, ChangePasswordRequest
from ..core.auth_utils import verify_password, get_password_hash, create_access_token, pwd_context
from ..core.auth_middleware import get_current_user
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# Tài khoản email dùng để gửi (bạn chỉnh lại)
SMTP_USER = "test.quangnt@gmail.com"
SMTP_PASS = "ybnzsajognsatswy"   # KHÔNG dùng mật khẩu Gmail, dùng App Password!


def send_email(to: str, subject: str, body: str):
    try:
        # Tạo email
        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Kết nối SMTP
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)

        # Gửi email
        server.send_message(msg)
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print("Failed to send email:", str(e))
        raise e

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
    print(user_in.password)
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

def generate_verification_code():
    return f"{random.randint(0, 999999):06d}"

# gửi mã
@router.post("/send-code")
def send_verification_code(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email không tồn tại")

    code = generate_verification_code()

    record = EmailVerificationCode(
        user_id=user.id,
        email=email,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        is_used=False,
    )

    db.add(record)
    db.commit()

    # gửi OTP qua email
    send_email(
        to=email,
        subject="Mã xác minh tài khoản",
        body=f"Mã xác minh của bạn là: {code}"
    )

    return {"message": "Đã gửi mã xác minh đến email"}

@router.post("/verify-code")
def verify_code(email: str, code: str, db: Session = Depends(get_db)):
    # lấy mã mới nhất
    record = (
        db.query(EmailVerificationCode)
        .filter(EmailVerificationCode.email == email)
        .order_by(EmailVerificationCode.id.desc())
        .first()
    )

    if not record:
        raise HTTPException(status_code=404, detail="Không tìm thấy mã xác minh")
    
    # kiểm tra hết hạn
    if record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Mã đã hết hạn")

    # kiểm tra đã dùng
    if record.is_used:
        raise HTTPException(status_code=400, detail="Mã đã được sử dụng")

    # kiểm tra khớp mã
    if code != record.code:
        db.commit()
        raise HTTPException(status_code=400, detail="Mã không đúng")

    # nếu đúng → xác thực thành công
    record.is_used = True

    user = db.query(User).filter(User.id == record.user_id).first()
    user.is_verified = True

    db.commit()

    return {"message": "Xác thực email thành công!"}
