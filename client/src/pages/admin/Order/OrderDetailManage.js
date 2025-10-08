import { useState, useEffect } from "react";
import "./OrderDetailManage.css";
import { useLocation, useParams } from "react-router-dom";
import { API_URL } from "../../../utils/lib";
import axios from "axios";

export default function OrderDetailManage() {
    const statusLabels = {
        pending: " Chờ xác nhận",
        confirmed: " Đã xác nhận",
        shipping: " Đang giao",
        completed: " Hoàn tất",
        cancelled: " Đã hủy",
    };

  const [order, setOrder] = useState(null);
  const [status, setStatus] = useState("");
    const orderId = useParams().id;

    const fetchOrder = async () => {
        try {
          const res = await axios.get(`${API_URL}orders/` + orderId);
          setOrder(res.data);
        } catch (error) {
          console.error("Lỗi lấy đơn hàng:", error);
        }
      };

    const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await axios.put(`${API_URL}orders/${orderId}`, { status: newStatus });
      fetchOrder(); // load lại danh sách
    } catch (error) {
      console.error("Lỗi cập nhật trạng thái:", error);
    }
  };
  useEffect(() => {
    // Giả sử gọi API lấy dữ liệu đơn hàng
    fetch(API_URL + `orders/${orderId}`)
      .then((res) => res.json())
      .then((data) => {
        setOrder(data);
        setStatus(data.order_status);
      });
  }, [orderId]);

  const handleStatusChange = (e) => {
    setStatus(e.target.value);
  };

  const handleUpdateStatus = async () => {
    await fetch(API_URL + `orders/${orderId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ order_status: status }),
    });

    alert("Cập nhật trạng thái thành công!");
  };

  if (!order) return <p>Loading...</p>;

  return (
    <div className="order-detail-container">
      <h1 className="order-title">Chi tiết đơn hàng #{order.id}</h1>

      <div className="order-card">
        <p><b>Khách hàng:</b> {order.user_id}</p>
        <p><b>Địa chỉ giao hàng:</b> {order.shipping_address}</p>
        <p><b>Phương thức thanh toán:</b> {order.payment_method}</p>
        <p><b>Tổng tiền:</b> {order.total_amount} VND</p>
        <p><b>Ngày tạo:</b> {new Date(order.created_at).toLocaleString()}</p>
        <p><b>Ghi chú:</b> {order.note || "Không có"}</p>

        <div className="status-section">
          <label>Trạng thái:</label>
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
        </div>
      </div>

      <div className="order-products">
        <h2>Sản phẩm</h2>
        <table>
          <thead>
            <tr>
              <th>Mã SP</th>
              <th>Tên sản phẩm</th>
              <th>Số lượng</th>
              <th>Đơn giá</th>
              <th>Thành tiền</th>
            </tr>
          </thead>
          <tbody>
            {order.order_details.map((item, idx) => (
              <tr key={idx}>
                <td>{item.product?.code || item.product_id}</td>
                <td>{item.product?.name || "N/A"}</td>
                <td>{item.quantity}</td>
                <td>{item.unit_price}</td>
                <td>{item.total_price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
