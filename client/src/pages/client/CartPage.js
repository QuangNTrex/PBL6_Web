import React from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  removeFromCart,
  increaseQuantity,
  decreaseQuantity,
  clearCart,
} from "../../redux/cartSlice";
import "./CartPage.css";

export default function CartPage() {
  const dispatch = useDispatch();
  const { items, totalAmount } = useSelector((state) => state.cart);

  return (
    <div className="cart-container">
      <h2 className="cart-title">🛒 Giỏ hàng của bạn</h2>

      {items.length === 0 ? (
        <p className="cart-empty">Giỏ hàng của bạn đang trống.</p>
      ) : (
        <>
          {/* Danh sách sản phẩm */}
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.id} className="cart-item">
                <img src={item.image_path} alt={item.name} className="cart-item-img" />

                <div className="cart-item-info">
                  <h3>{item.name}</h3>
                  <p className="price">{item.price.toLocaleString()} đ</p>

                  <div className="cart-item-controls">
                    <button onClick={() => dispatch(decreaseQuantity(item.id))}>
                      −
                    </button>
                    <span>{item.quantity}</span>
                    <button onClick={() => dispatch(increaseQuantity(item.id))}>
                      +
                    </button>
                  </div>
                </div>

                <div className="cart-item-total">
                  {(item.price * item.quantity).toLocaleString()} đ
                </div>

                <button
                  className="remove-btn"
                  onClick={() => dispatch(removeFromCart(item.id))}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>

          {/* Tổng cộng & Thanh toán */}
          <div className="cart-summary">
            <h3>Tổng cộng: {1111} đ</h3>
            <div className="cart-summary-actions">
              <button
                className="clear-btn"
                onClick={() => dispatch(clearCart())}
              >
                Xóa giỏ hàng
              </button>
              <button className="checkout-btn">Thanh toán</button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
