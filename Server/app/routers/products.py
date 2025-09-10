from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])


# 🟢 API: Thêm sản phẩm
@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.code == product.code).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product with this code already exists")

    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# 🟢 API: Lấy toàn bộ sản phẩm
@router.get("/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


# 🟢 API: Sửa sản phẩm
@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


# 🟢 API: Xóa sản phẩm
@router.delete("/{product_id}", response_model=schemas.ProductOut)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return db_product



# 🟢 API: Tìm kiếm sản phẩm theo tên
@router.get("/search", response_model=List[schemas.ProductOut])
def search_products(q: str = Query(..., min_length=1, description="Tên sản phẩm cần tìm"),
                    db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.name.ilike(f"%{q}%")).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

# 🟢 API phân trang
@router.get("/pagination", response_model=List[schemas.ProductOut])
def get_products_pagination(
    page: int = Query(1, ge=1, description="Trang hiện tại (bắt đầu từ 1)"),
    size: int = Query(10, ge=1, le=100, description="Số sản phẩm mỗi trang"),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách sản phẩm theo phân trang.
    - page: số trang (mặc định = 1)
    - size: số sản phẩm mỗi trang (mặc định = 10)
    """
    offset = (page - 1) * size
    products = (
        db.query(models.Product)
        .order_by(models.Product.created_at.desc())
        .offset(offset)
        .limit(size)
        .all()
    )
    return products

# 🟢 API: Lấy sản phẩm theo ID
@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 🟢 API: lấy sản phẩm theo category_id
@router.get("/category/{category_id}", response_model=List[schemas.ProductOut])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    products = (
        db.query(models.Product)
        .filter(models.Product.category_id == category_id)
        .all()
    )
    return products
