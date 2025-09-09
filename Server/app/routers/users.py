from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserUpdate, UserOut
from app.routers.auth import get_current_user
from ..routers.auth import create_access_token  # nếu muốn refresh token

from app import schemas, crud

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
# routers/user.py

# @router.post("/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.user.create_user(db=db, user=user)

# @router.get("/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return crud.user.get_users(db=db, skip=skip, limit=limit)

# @router.get("/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.user.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.put("/{user_id}", response_model=schemas.User)
# def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     db_user = crud.user.update_user(db, user_id, user)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.delete("/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.user.delete_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"detail": "User deleted"}

@router.put("/update", response_model=UserOut)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
     current_user: User = Depends(get_current_user)
):
    """
    API: Cập nhật thông tin cá nhân của user đang đăng nhập
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Cập nhật các trường cho phép
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
