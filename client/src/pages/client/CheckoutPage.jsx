import React, { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import { clearCart } from "../../redux/cartSlice";
import { useNavigate, useLocation } from "react-router-dom";
import "./CheckoutPage.css";
import { API_URL } from "../../utils/lib";

export default function CheckoutPage() {
    const access_token = localStorage.getItem("access_token");
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  // ✅ Lấy danh sách sản phẩm từ CartPage
  const { selectedItems } = location.state || { selectedItems: [] };

  // ✅ Địa chỉ mặc định từ thông tin user (ví dụ lấy từ localStorage)
  const user = JSON.parse(localStorage.getItem("user")) || {};
  const [address, setAddress] = useState(user.address || "");
  const [note, setNote] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");

  // 🟢 Tính tổng tiền
  const totalAmount = selectedItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  // 🟢 Submit đơn hàng
  const handleSubmit = async () => {
    if (!address) {
      alert("Vui lòng nhập địa chỉ giao hàng!");
      return;
    }

    const orderData = {
      user_id: user.id, // TODO: thay bằng user_id từ Redux/Auth
      shipping_address: address,
      note,
      payment_method: paymentMethod,
      total_amount: totalAmount,
      order_details: selectedItems.map((item) => ({
        product_id: item.id,
        quantity: item.quantity,
        unit_price: item.price,
        total_price: item.price * item.quantity,
      })),
    };
    console.log("📝 Dữ liệu đơn hàng:", orderData);
    try {
      const res = await fetch(API_URL + "orders", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${access_token}` },
        body: JSON.stringify(orderData),
      });

      if (!res.ok) throw new Error("Đặt hàng thất bại");

      const data = await res.json();
      console.log("✅ Đặt hàng thành công:", data);

      
      navigate("/orders");
    } catch (err) {
      console.error("❌ Lỗi khi đặt hàng:", err);
    }
  };

  return (
    <div className="checkout-container">
      <h2 className="checkout-title">Thanh toán</h2>

      {/* Bảng sản phẩm */}
      <table className="checkout-table">
        <thead>
          <tr>
            <th>Hình ảnh</th>
            <th>Sản phẩm</th>
            <th>Giá</th>
            <th>Số lượng</th>
            <th>Thành tiền</th>
          </tr>
        </thead>
        <tbody>
          {selectedItems.map((item) => (
            <tr key={item.id}>
              <td>
                <img
                  src={item.image_path}
                  alt={item.name}
                  className="checkout-img"
                />
              </td>
              <td>{item.name}</td>
              <td>{item.price.toLocaleString()} đ</td>
              <td>{item.quantity}</td>
              <td>{(item.price * item.quantity).toLocaleString()} đ</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Tổng tiền */}
      <div className="checkout-total">
        <h3>Tổng cộng: {totalAmount.toLocaleString()} đ</h3>
      </div>

      {/* Form thông tin giao hàng */}
      <div className="checkout-form">
        <label>
          Địa chỉ giao hàng:
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            placeholder="Nhập địa chỉ..."
          />
        </label>

        <label>
          Ghi chú:
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Ví dụ: Giao ngoài giờ hành chính"
          />
        </label>

        <label>
          Phương thức thanh toán:
          <select
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
          >
            <option value="cash">Tiền mặt</option>
            <option value="credit_card">Thẻ tín dụng</option>
            <option value="momo">Momo</option>
            <option value="zalopay">ZaloPay</option>
          </select>
        </label>
      </div>

      {/* Nút xác nhận */}
      <button className="checkout-btn" onClick={handleSubmit}>
        Xác nhận đặt hàng
      </button>
    </div>
  );
}
