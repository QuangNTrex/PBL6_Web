from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

# Create category
@router.post("/", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# Get all categories
@router.get("/", response_model=List[schemas.CategoryOut])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = db.query(models.Category).order_by(models.Category.name).all()
    return categories


# Get category by id
@router.get("/{category_id}", response_model=schemas.CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# Update category
@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in category_update.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


# Delete category
@router.delete("/{category_id}", response_model=schemas.CategoryOut)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(db_category)
    db.commit()
    return db_category
