from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# 🟢 API: Lấy toàn bộ user
@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


# 🟢 API: Lấy chi tiết user theo id
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#lấy user theo số điên thoại
@router.get("/phone/{phone}", response_model=schemas.UserOut)
def get_user_by_phone(phone: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🟢 API: Cập nhật thông tin user
@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# 🟢 API: Xóa user
@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user

# 🟢 API: Cập nhật role và status của user
@router.patch("/admin/{user_id}", response_model=schemas.UserOut)
def update_user_role_status(
    user_id: int,
    update_data: schemas.UserRoleStatusUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.role is not None:
        user.role = update_data.role
    if update_data.status is not None:
        user.status = update_data.status

    db.commit()
    db.refresh(user)
    return user
