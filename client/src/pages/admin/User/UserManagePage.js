import React, { useEffect, useState } from "react";
import "./UserManagePage.css";
import { API_URL } from "../../../utils/lib";

const UserManagePage = () => {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const access_token = localStorage.getItem("access_token");

  useEffect(() => {
    fetch(API_URL + "users/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
      })
      .catch((err) => {
        console.error("Lỗi tải danh sách người dùng:", err);
      });
  }, []);

  const filteredUsers = users.filter((user) => {
    const matchName = user.full_name
      ?.toLowerCase()
      .includes(search.toLowerCase());
    const matchStatus =
      statusFilter === "all" ? true : user.status === statusFilter;
    return matchName && matchStatus;
  });

  const renderGender = (gender) => {
    if (gender === 1) return "Nam";
    if (gender === 2) return "Nữ";
    return "Khác";
  };

  const handleToggleBan = (id, currentStatus) => {
    const newStatus = currentStatus === "active" ? "banned" : "active";
    fetch(API_URL + `users/${id}/status`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify({ status: newStatus }),
    })
      .then((res) => res.json())
      .then((data) => {
        setUsers(users.map((u) => (u.id === id ? { ...u, status: newStatus } : u)));
      })
      .catch((err) => console.error("Lỗi cập nhật status:", err));
  };

  const handleDelete = (id) => {
    if (!window.confirm("Bạn có chắc muốn xóa người dùng này?")) return;

    fetch(API_URL + `users/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((res) => {
        if (res.ok) {
          setUsers(users.filter((u) => u.id !== id));
        }
      })
      .catch((err) => console.error("Lỗi xóa người dùng:", err));
  };

  return (
    <div className="user-container">
      <h2>👤 Quản lý Người dùng</h2>

      <div className="user-toolbar">
        <input
          type="text"
          placeholder="🔍 Tìm kiếm theo tên..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="all">Tất cả trạng thái</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="banned">Banned</option>
        </select>
      </div>

      <table className="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Avatar</th>
            <th>Họ tên</th>
            <th>Username</th>
            <th>Email</th>
            <th>SĐT</th>
            <th>Địa chỉ</th>
            <th>Ngày sinh</th>
            <th>Giới tính</th>
            <th>Role</th>
            <th>Trạng thái</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {filteredUsers.map((u) => (
            <tr key={u.id}>
              <td>{u.id}</td>
              <td>
                {u.avatar_url ? (
                  <img src={u.avatar_url} alt="avatar" className="user-avatar" />
                ) : (
                  "—"
                )}
              </td>
              <td>{u.full_name || "—"}</td>
              <td>{u.username}</td>
              <td>{u.email}</td>
              <td>{u.phone || "—"}</td>
              <td>{u.address || "—"}</td>
              <td>
                {u.birth_date
                  ? new Date(u.birth_date).toLocaleDateString("vi-VN")
                  : "—"}
              </td>
              <td>{renderGender(u.gender)}</td>
              <td>
                <span className={`role ${u.role}`}>{u.role}</span>
              </td>
              <td>
                <span className={`status ${u.status}`}>{u.status}</span>
              </td>
              <td>
                <button
                  className="ban-btn"
                  onClick={() => handleToggleBan(u.id, u.status)}
                >
                  {u.status === "active" ? "🚫 Ban" : "✅ Unban"}
                </button>
                <button className="delete-btn" onClick={() => handleDelete(u.id)}>
                  🗑 Xóa
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserManagePage;
