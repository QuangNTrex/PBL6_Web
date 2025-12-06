import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  removeFromCart,
  increaseQuantity,
  decreaseQuantity,
  clearCart,
  removeMoreFromCart,
} from "../../redux/cartSlice";
import "./CartPage.css";
import { useNavigate } from "react-router-dom";

export default function CartPage() {
  const navgate = useNavigate();
  const dispatch = useDispatch();
  const { items } = useSelector((state) => state.cart);

  // Local state cho việc chọn sản phẩm
  const [selectedItems, setSelectedItems] = useState([]);

  // Kiểm tra chọn toàn bộ
  const allSelected = items.length > 0 && selectedItems.length === items.length;

  // Toggle chọn 1 sản phẩm
  const toggleSelectItem = (id) => {
    if (selectedItems.includes(id)) {
      setSelectedItems(selectedItems.filter((itemId) => itemId !== id));
    } else {
      setSelectedItems([...selectedItems, id]);
    }
  };

  const handleRemoveSelected = () => {
    dispatch(removeMoreFromCart(selectedItems));
  }

  // Toggle chọn tất cả
  const toggleSelectAll = () => {
    if (allSelected) {
      setSelectedItems([]);
    } else {
      setSelectedItems(items.map((item) => item.id));
    }
  };

  // Tổng tiền chỉ tính sản phẩm đã chọn
  console.log(items)
  
  const totalAmount = items
    .filter((item) => selectedItems.includes(item.id))
    .reduce((sum, item) => sum + item.price * item.quantity, 0);

  const handleCheckout = () => {
    const selectedProducts = items.filter((item) =>
      selectedItems.includes(item.id)
    );
    navgate("/checkout", { state: { selectedItems: selectedProducts } });
  };

  return (
    <div className="cart-container">
      <h2 className="cart-title">Giỏ hàng của bạn</h2>

      {items.length === 0 ? (
        <p className="cart-empty">Giỏ hàng của bạn đang trống.</p>
      ) : (
        <>
          {/* Nút chọn toàn bộ */}
          <div className="select-all">
            <label>
              <input
                type="checkbox"
                checked={allSelected}
                onChange={toggleSelectAll}
              />
              Chọn tất cả
            </label>
          </div>

          {/* Danh sách sản phẩm */}
          <div className="cart-items">
            {items.map((item) => (
              <div key={item.id} className="cart-item">
                <input
                  type="checkbox"
                  checked={selectedItems.includes(item.id)}
                  onChange={() => toggleSelectItem(item.id)}
                />

                <img
                  src={item.image_path}
                  alt={item.name}
                  className="cart-item-img"
                />

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
            <h3>Tổng cộng: {totalAmount.toLocaleString()} đ</h3>
            <div className="cart-summary-actions">
               <button className="clear-btn" onClick={handleRemoveSelected}>
                Xóa
              </button>
              <button className="checkout-btn-1" onClick={handleCheckout}>
                Thanh toán
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
