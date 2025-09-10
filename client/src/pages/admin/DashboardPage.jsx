// src/pages/admin/DashboardPage.js
import React, { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts";
import "./DashboardPage.css";
import { API_URL } from "../../utils/lib";

export default function DashboardPage() {
  const [stats, setStats] = useState({});
  const [revenueData, setRevenueData] = useState([]);
  const [orderStatus, setOrderStatus] = useState({});
  const [recentOrders, setRecentOrders] = useState([]);
  const [recentUsers, setRecentUsers] = useState([]);

  // 🎯 Gọi API khi load trang
  useEffect(() => {
    fetch( API_URL + "admin/dashboard/stats")
      .then((res) => res.json())
      .then(setStats);

    fetch(API_URL + "admin/dashboard/revenue-by-month?year=2025")
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.months.map((m, i) => ({
          month: m,
          revenue: data.revenues[i],
        }));
        setRevenueData(formatted);
      });

    fetch(API_URL + "admin/dashboard/order-status-ratio")
      .then((res) => res.json())
      .then(setOrderStatus);

    fetch(API_URL + "admin/dashboard/recent-orders?limit=5")
      .then((res) => res.json())
      .then(setRecentOrders);

    fetch(API_URL + "admin/dashboard/recent-users?limit=5")
      .then((res) => res.json())
      .then(setRecentUsers);
  }, []);

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#c45850"];

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">📊 Dashboard</h2>

      {/* Cards */}
      <div className="dashboard-cards">
        <div className="card">
          <h3>🛒 Sản phẩm</h3>
          <p>{stats.total_products || 0}</p>
        </div>
        <div className="card">
          <h3>📦 Đơn hàng</h3>
          <p>{stats.total_orders || 0}</p>
        </div>
        <div className="card">
          <h3>💰 Doanh thu</h3>
          <p>{(stats.total_revenue || 0).toLocaleString()} đ</p>
        </div>
        <div className="card">
          <h3>👥 Khách hàng</h3>
          <p>{stats.total_users || 0}</p>
        </div>
      </div>

      {/* Charts */}
      <div className="dashboard-charts">
        {/* Line Chart */}
        <div className="chart-box">
          <h3>📈 Doanh thu theo tháng</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Pie Chart */}
        <div className="chart-box">
          <h3>📊 Trạng thái đơn hàng</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={Object.entries(orderStatus).map(([name, value]) => ({
                  name,
                  value,
                }))}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {Object.entries(orderStatus).map((entry, index) => (
                  <Cell key={entry[0]} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Lists */}
      <div className="dashboard-lists">
        <div className="list-box">
          <h3>🆕 Đơn hàng gần nhất</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Khách hàng</th>
                <th>Tổng tiền</th>
                <th>Trạng thái</th>
                <th>Ngày tạo</th>
              </tr>
            </thead>
            <tbody>
              {recentOrders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.user?.full_name || order.user?.email}</td>
                  <td>{order.total_amount.toLocaleString()} đ</td>
                  <td>{order.status}</td>
                  <td>{new Date(order.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="list-box">
          <h3>👤 Khách hàng mới</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Tên</th>
                <th>Email</th>
                <th>Ngày đăng ký</th>
              </tr>
            </thead>
            <tbody>
              {recentUsers.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.full_name || "N/A"}</td>
                  <td>{user.email}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
