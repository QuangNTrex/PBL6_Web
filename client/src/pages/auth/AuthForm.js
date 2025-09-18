// src/pages/auth/AuthForm.js
import React, { useState } from "react";
import "./AuthForm.css";

function AuthForm({ type, onSubmit }) {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
    phone: "",
    address: "",
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form);
  };

  return (
    <div className="auth-container">
      <h2 className="auth-title">
        {type === "login" ? "Đăng nhập" : "Đăng ký"}
      </h2>
      <form className="auth-form" onSubmit={handleSubmit}>
        <input
              type="text"
              name="username"
              placeholder="Tên đăng nhập"
              value={form.username}
              onChange={handleChange}
              className="auth-input"
              required
            />
        {type === "register" && (
          <>
            
            <input
              type="text"
              name="full_name"
              placeholder="Họ và tên"
              value={form.full_name}
              onChange={handleChange}
              className="auth-input"
            />
            {/* <input
              type="text"
              name="phone"
              placeholder="Số điện thoại"
              value={form.phone}
              onChange={handleChange}
              className="auth-input"
            />
            <input
              type="text"
              name="address"
              placeholder="Địa chỉ"
              value={form.address}
              onChange={handleChange}
              className="auth-input"
            /> */}
            <input
              name="email"
              placeholder="Email"
              value={form.email}
              onChange={handleChange}
              className="auth-input"
        
            />
          </>
          
        )}

        

        <input
          type="password"
          name="password"
          placeholder="Mật khẩu"
          value={form.password}
          onChange={handleChange}
          className="auth-input"
          required
        />

        <button type="submit" className="auth-button">
          {type === "login" ? "Đăng nhập" : "Đăng ký"}
        </button>
      </form>
    </div>
  );
}

export default AuthForm;
