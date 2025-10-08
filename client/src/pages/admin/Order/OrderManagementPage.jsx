import React, { useEffect, useState } from "react";
import axios from "axios";
import "./OrderManagementPage.css";
import { useNavigate } from "react-router-dom";

const API_URL = "http://localhost:8000"; // đổi theo backend của bạn

const statusLabels = {
  pending: " Chờ xác nhận",
  confirmed: " Đã xác nhận",
  shipping: " Đang giao",
  completed: " Hoàn tất",
  cancelled: " Đã hủy",
};

export default function OrderManagementPage() {
  const navigate = useNavigate()
  const [orders, setOrders] = useState([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  // Lấy danh sách đơn
  const fetchOrders = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/orders`);
      setOrders(res.data);
    } catch (error) {
      console.error("Lỗi lấy đơn hàng:", error);
    }
    setLoading(false);
  };

  // Cập nhật trạng thái đơn
  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await axios.put(`${API_URL}/orders/${orderId}`, { status: newStatus });
      fetchOrders(); // load lại danh sách
    } catch (error) {
      console.error("Lỗi cập nhật trạng thái:", error);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // Lọc đơn theo trạng thái
  const filteredOrders =
    filter === "all" ? orders : orders.filter((o) => o.status === filter);

  return (
    <div className="order-management-container">
      <h2>📦 Quản lý đơn hàng</h2>

      {/* Bộ lọc trạng thái */}
      <div className="order-filter">
        <label>Lọc theo trạng thái: </label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="all">Tất cả</option>
          <option value="pending">Chờ xác nhận</option>
          <option value="confirmed">Đã xác nhận</option>
          <option value="shipping">Đang giao</option>
          <option value="completed">Hoàn tất</option>
          <option value="cancelled">Đã hủy</option>
        </select>
      </div>

      {loading ? (
        <p>Đang tải đơn hàng...</p>
      ) : (
        <table className="order-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Khách hàng</th>
              <th>Tổng tiền</th>
              <th>Trạng thái</th>
              <th>Ngày đặt</th>
              <th>Chi tiết</th>
              <th>Hành động</th>
            </tr>
          </thead>
          <tbody>
            {filteredOrders.length === 0 ? (
              <tr>
                <td colSpan="6">Không có đơn hàng nào.</td>
              </tr>
            ) : (
              filteredOrders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.user?.full_name || "Ẩn danh"}</td>
                  <td>{order.total_amount.toLocaleString()} đ</td>
                  <td>
                    <span className={`status ${order.status}`}>
                      {statusLabels[order.status]}
                    </span>
                  </td>
                  <td>{new Date(order.created_at).toLocaleString()}</td>
                  <td>
                    <button className="btn-order-detail" onClick={() => {navigate("/admin/order/" + order.id)}}>Chi tiết đơn hàng</button>
                  </td>
                  <td>
                    <select
                      value={order.status}
                      onChange={(e) =>
                        updateOrderStatus(order.id, e.target.value)
                      }
                    >
                      {Object.keys(statusLabels).map((status) => (
                        <option key={status} value={status}>
                          {statusLabels[status]}
                        </option>
                      ))}
                    </select>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
