from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)

# ====== Helper ======
def recalc_cart_total(cart: models.Cart, db: Session):
    total = sum(item.total_price for item in cart.items)
    cart.total_amount = total
    cart.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(cart)
    return cart


# ====== Lấy giỏ hàng theo user ======
@router.get("/{user_id}", response_model=schemas.CartOut)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        # Nếu chưa có giỏ, tạo mới
        cart = models.Cart(user_id=user_id, total_amount=0)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


# ====== Thêm sản phẩm vào giỏ ======
@router.post("/{user_id}/items", response_model=schemas.CartOut)
def add_to_cart(user_id: int, item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        cart = models.Cart(user_id=user_id, total_amount=0)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Kiểm tra sản phẩm đã có trong giỏ chưa
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
        cart_item.total_price = cart_item.quantity * cart_item.unit_price
    else:
        cart_item = models.CartItem(
            cart_id=cart.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
            total_price=item.quantity * product.price
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart)
    return recalc_cart_total(cart, db)


# ====== Cập nhật số lượng sản phẩm ======
@router.put("/{user_id}/items/{item_id}", response_model=schemas.CartOut)
def update_cart_item(user_id: int, item_id: int, data: schemas.CartItemUpdate, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.cart_id == cart.id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if data.quantity is not None:
        if data.quantity <= 0:
            db.delete(cart_item)
        else:
            cart_item.quantity = data.quantity
            cart_item.total_price = cart_item.quantity * cart_item.unit_price

    db.commit()
    return recalc_cart_total(cart, db)


# ====== Xóa sản phẩm khỏi giỏ ======
@router.delete("/{user_id}/items/{item_id}", response_model=schemas.CartOut)
def delete_cart_item(user_id: int, item_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == item_id,
        models.CartItem.cart_id == cart.id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(cart_item)
    db.commit()
    return recalc_cart_total(cart, db)


# ====== Xóa toàn bộ giỏ hàng ======
@router.delete("/{user_id}", response_model=schemas.CartOut)
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    for item in cart.items:
        db.delete(item)

    cart.total_amount = 0
    db.commit()
    db.refresh(cart)
    return cart
