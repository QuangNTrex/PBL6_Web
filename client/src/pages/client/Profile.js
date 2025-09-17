// src/pages/client/Profile.js
import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { setUser } from "../../redux/userSlice";
import "./Profile.css";
import { API_URL } from "../../utils/lib";
import { useNavigate } from "react-router-dom";

export default function Profile() {
    const access_token = localStorage.getItem("access_token");
  const user = useSelector((state) => state.user);
  console.log("User from Redux:", user);
  const dispatch = useDispatch();
  const navigator = useNavigate();
  const [activeTab, setActiveTab] = useState("account");

  // form local state
  const [formData, setFormData] = useState({
    full_name: user.full_name || "",
    email: user.email || "",
    phone: user.phone || "",
    address: user.address || "",
    avatar_url: user.avatar_url || "",
    birth_date: user.birth_date || "",
    gender: user.gender === 1 ? "male" : user.gender === 0 ? "female" : null || "",
  });

//   console.log(formData);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleUpdate = () => {
        const birthDate = new Date(formData.birth_date || "1970-01-01");
        const birthDateWithTime = new Date(
    birthDate.getFullYear(),
    birthDate.getMonth(),
    birthDate.getDate(),
    0, 0, 0  // giờ, phút, giây
    );
    const data = {...formData, gender: formData.gender === "male" ? 1 : 0, };
    
    console.log(data);
    fetch(API_URL + "users/update", {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json',
            "Authorization": `Bearer ${access_token}`
        },
        body: JSON.stringify(data)
    }).then(res => res.json()).then(data => {
        console.log(data);
        console.log("Cập nhật thành công");
        dispatch(setUser(data));

    }).catch(err => {
        console.error("Đăng nhập thất bại:", err);
    })
  };

  // State cho đổi mật khẩu
    const [passwordData, setPasswordData] = useState({
        old_password: "",
        new_password: "",
    });
    const [passwordMsg, setPasswordMsg] = useState("");



    const handlePasswordChange = (e) => {
        const { name, value } = e.target;
        setPasswordData((prev) => ({ ...prev, [name]: value }));
    };

    const handleChangePassword = () => {
        setPasswordMsg("");
        fetch(API_URL + "auth/change-password", {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${access_token}`
            },
            body: JSON.stringify({
                old_password: passwordData.old_password,
                new_password: passwordData.new_password,
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                setPasswordMsg("Đổi mật khẩu thành công!");
                console.log(data, "Đổi mật khẩu thành công!");
            } else {
                setPasswordMsg(data.message || "Đổi mật khẩu thất bại!");
            }
        })
        .catch(err => {
            setPasswordMsg("Có lỗi xảy ra!");
        });
    };

  return (
    <div className="profile-container">
      {/* Sidebar */}
      <aside className="profile-sidebar">
        <button
          className={activeTab === "account" ? "active" : ""}
          onClick={() => setActiveTab("account")}
        >
          Tài khoản của tôi
        </button>
        <button
          className={activeTab === "orders" ? "active" : ""}
          onClick={() => setActiveTab("orders")}
        >
          Đơn mua
        </button>
        <button
            className={activeTab === "changePassword" ? "active" : ""}
            onClick={() => setActiveTab("changePassword")}
        >
            Đổi mật khẩu
        </button>
        {user.role !== "customer" && <button
          className={activeTab === "admin" ? "active" : ""}
          onClick={() => navigator("/staff")}
        >
          Trang Nhân viên
        </button>}
        {user.role === "admin" && <button
          className={activeTab === "admin" ? "active" : ""}
          onClick={() => navigator("/admin")}
        >
          Trang Admin
        </button>}
      </aside>

      {/* Content */}
      <main className="profile-content">
        {activeTab === "account" && (
          <div className="account-form">
            <h2>Tài khoản của tôi</h2>
            <div className="form-group">
              <label>Họ và tên</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                readOnly
              />
            </div>

            <div className="form-group">
              <label>Số điện thoại</label>
              <input
                type="text"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Địa chỉ</label>
              <input
                type="text"
                name="address"
                value={formData.address}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Ảnh đại diện (URL)</label>
              <input
                type="text"
                name="avatar_url"
                value={formData.avatar_url}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Ngày sinh</label>
              <input
                type="date"
                name="birth_date"
                value={formData.birth_date}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Giới tính</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
              >
                <option value="">-- Chọn giới tính --</option>
                <option value="male">Nam</option>
                <option value="female">Nữ</option>
                <option value="other">Khác</option>
              </select>
            </div>

            <button className="update-btn" onClick={handleUpdate}>
              Cập nhật thông tin
            </button>
          </div>
        )}

        {activeTab === "orders" && (
          <div>
            <h2>Đơn mua</h2>
            <p>Chưa có đơn hàng nào.</p>
          </div>
        )}

        {activeTab === "changePassword" && (
                    <div className="change-password-form">
                        <h2>Đổi mật khẩu</h2>
                        <div className="form-group">
                            <label>Mật khẩu cũ</label>
                            <input
                                type="password"
                                name="old_password"
                                value={passwordData.old_password}
                                onChange={handlePasswordChange}
                            />
                        </div>
                        <div className="form-group">
                            <label>Mật khẩu mới</label>
                            <input
                                type="password"
                                name="new_password"
                                value={passwordData.new_password}
                                onChange={handlePasswordChange}
                            />
                        </div>
                        <button className="update-btn" onClick={handleChangePassword}>
                            Đổi mật khẩu
                        </button>
                        {passwordMsg && <p style={{ color: passwordMsg.includes("thành công") ? "green" : "red" }}>{passwordMsg}</p>}
                    </div>
                )}
      </main>
    </div>
  );
}
