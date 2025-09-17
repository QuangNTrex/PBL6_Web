// src/pages/admin/DashboardPage.js
import React, { useEffect, useState } from "react";
import {
  LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip,
  PieChart, Pie, Cell, Legend
} from "recharts";
import "./DashboardPage.css";
import { API_URL } from "../../utils/lib";

export default function DashboardPage() {
  const [overview, setOverview] = useState({});
  const [revenueData, setRevenueData] = useState([]);
  const [statusData, setStatusData] = useState([]);
  const [latestOrders, setLatestOrders] = useState([]);
  const [latestCustomers, setLatestCustomers] = useState([]);

  console.log("Overview data:", overview);
  console.log("Revenue data:", revenueData);
  console.log("Status data:", statusData);
  console.log("Latest orders:", latestOrders);
  console.log("Latest customers:", latestCustomers);
  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. Tổng quan
        const resOverview = await fetch(API_URL + "statistics/overview");
        setOverview(await resOverview.json());

        // 2. Doanh thu theo tháng (năm hiện tại)
        const year = new Date().getFullYear();
        const resRevenue = await fetch(API_URL + `statistics/revenue-by-month?year=${year}`);
        setRevenueData(await resRevenue.json());

        // 3. Tỉ lệ đơn hàng theo trạng thái
        const resStatus = await fetch(API_URL + "statistics/order-status-ratio");
        setStatusData(await resStatus.json());

        // 4. Đơn hàng gần nhất
        const resOrders = await fetch(API_URL + "statistics/latest-orders");
        setLatestOrders(await resOrders.json());

        // 5. Khách hàng mới
        const resCustomers = await fetch(API_URL + "statistics/latest-customers");
        setLatestCustomers(await resCustomers.json());
      } catch (err) {
        console.error("Lỗi khi tải dashboard:", err);
      }
    };
    fetchData();
  }, []);

  const COLORS = ["#3498db", "#2ecc71", "#e67e22", "#e74c3c", "#9b59b6"];

  return (
    <div className="dashboard-container">
      <h1>📊 Dashboard</h1>

      {/* --- Tổng quan --- */}
      <div className="overview-cards">
        <div className="card">📦 Sản phẩm: <span>{overview.total_products}</span></div>
        <div className="card">🧾 Đơn hàng: <span>{overview.total_orders}</span></div>
        <div className="card">💰 Doanh thu: <span>{overview.total_revenue?.toLocaleString()} đ</span></div>
        <div className="card">👥 Khách hàng: <span>{overview.total_customers}</span></div>
      </div>

      {/* --- Biểu đồ --- */}
      <div className="charts">
        <div className="chart-box">
          <h3>📈 Doanh thu theo tháng</h3>
          <LineChart width={500} height={300} data={revenueData}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="revenue" stroke="#3498db" />
          </LineChart>
        </div>

        <div className="chart-box">
          <h3>🥧 Tỉ lệ đơn hàng theo trạng thái</h3>
          <PieChart width={400} height={300}>
            <Pie
              data={statusData}
              dataKey="count"
              nameKey="status"
              cx="50%"
              cy="50%"
              outerRadius={100}
              fill="#8884d8"
              label
            >
              {statusData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>
      </div>

      {/* --- Danh sách gần nhất --- */}
      <div className="recent-lists">
        <div className="list-box">
          <h3>🧾 5 Đơn hàng gần nhất</h3>
          <ul>
            {latestOrders.map((o) => (
              <li key={o.id}>
                #{o.id} - {o.status} - {o.total_amount.toLocaleString()} đ
              </li>
            ))}
          </ul>
        </div>

        <div className="list-box">
          <h3>👥 5 Khách hàng mới</h3>
          <ul>
            {latestCustomers.map((c) => (
              <li key={c.id}>
                {c.full_name || c.username} - {c.email}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
