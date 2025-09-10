import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./OrderPage.css";

export default function OrderPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const user = JSON.parse(localStorage.getItem("user")) || { id: 1 };

  // 🟢 Gọi API lấy danh sách đơn hàng của user
  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await fetch(`http://localhost:8000/orders?user_id=${user.id}`);
        if (!res.ok) throw new Error("Không thể tải đơn hàng");
        const data = await res.json();
        setOrders(data);
      } catch (err) {
        console.error("❌ Lỗi khi tải đơn hàng:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, [user.id]);

  if (loading) return <p className="orders-loading">Đang tải đơn hàng...</p>;

  return (
    <div className="orders-container">
      <h2 className="orders-title">📦 Đơn hàng của bạn</h2>

      {orders.length === 0 ? (
        <p className="orders-empty">Bạn chưa có đơn hàng nào.</p>
      ) : (
        <table className="orders-table">
          <thead>
            <tr>
              <th>Mã đơn</th>
              <th>Ngày đặt</th>
              <th>Tổng tiền</th>
              <th>Trạng thái</th>
              <th>Chi tiết</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td>{new Date(order.created_at).toLocaleString()}</td>
                <td>{order.total_amount.toLocaleString()} đ</td>
                <td>
                  <span className={`status ${order.status}`}>
                    {order.status}
                  </span>
                </td>
                <td>
                  <button
                    className="order-detail-btn"
                    onClick={() => navigate(`/orders/${order.id}`)}
                  >
                    Xem chi tiết
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
