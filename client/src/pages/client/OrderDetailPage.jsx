import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./OrderDetailPage.css";

export default function OrderDetailPage() {
  const { id } = useParams(); // lấy orderId từ URL
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrderDetail = async () => {
      try {
        const res = await fetch(`http://localhost:8000/orders/${id}`);
        if (!res.ok) throw new Error("Không thể tải chi tiết đơn hàng");
        const data = await res.json();
        console.log("✅ Chi tiết đơn hàng đã tải:", data);
        setOrder(data);
      } catch (err) {
        console.error("❌ Lỗi khi tải chi tiết đơn hàng:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrderDetail();
  }, [id]);

  if (loading) return <p className="order-detail-loading">Đang tải chi tiết đơn hàng...</p>;
  if (!order) return <p className="order-detail-error">Không tìm thấy đơn hàng.</p>;

  return (
    <div className="order-detail-container">
      <h2 className="order-detail-title">📑 Chi tiết đơn hàng #{order.id}</h2>

      {/* Thông tin đơn hàng */}
      <div className="order-info">
        <p><strong>Ngày đặt:</strong> {new Date(order.created_at).toLocaleString()}</p>
        <p><strong>Địa chỉ giao hàng:</strong> {order.shipping_address}</p>
        <p><strong>Phương thức thanh toán:</strong> {order.payment_method}</p>
        <p>
          <strong>Trạng thái:</strong>{" "}
          <span className={`status ${order.status}`}>{order.status}</span>
        </p>
        {order.note && <p><strong>Ghi chú:</strong> {order.note}</p>}
      </div>

      {/* Danh sách sản phẩm */}
      <h3 className="order-products-title">🛒 Sản phẩm</h3>
      <table className="order-products-table">
        <thead>
          <tr>
            <th>Ảnh</th>
            <th>Tên sản phẩm</th>
            <th>Giá</th>
            <th>Số lượng</th>
            <th>Thành tiền</th>
          </tr>
        </thead>
        <tbody>
          {order.order_details.map((detail) => (
            <tr key={detail.id}>
              <td>
                <img
                  src={detail.product.image_path}
                  alt={detail.product.name}
                  className="order-product-img"
                />
              </td>
              <td>{detail.product.name}</td>
              <td>{detail.unit_price.toLocaleString()} đ</td>
              <td>{detail.quantity}</td>
              <td>{detail.total_price.toLocaleString()} đ</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Tổng tiền */}
      <div className="order-total">
        <h3>Tổng cộng: {order.total_amount.toLocaleString()} đ</h3>
      </div>

      <button className="back-btn" onClick={() => navigate("/orders")}>
        ← Quay lại danh sách đơn hàng
      </button>
    </div>
  );
}
