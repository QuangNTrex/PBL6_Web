// src/pages/auth/Login.js
import React from "react";
import { useDispatch } from "react-redux";
import { setUser } from "../../redux/userSlice";
import AuthForm from "./AuthForm";
import authApi from "../../api/authApi";    

function Login() {
  const dispatch = useDispatch();

  const handleLogin = async (formData) => {
    const response = await authApi.login(formData);
    if (!response || response.status !== 200) {
      console.error("Đăng nhập thất bại:", response ? response.data : "No response");
      return;
    }
    localStorage.setItem("access_token", response.data.access_token);
    const userData = response.data.user;

    dispatch(setUser(userData));
    console.log("Đăng nhập thành công:", userData);
  };

  return <AuthForm type="login" onSubmit={handleLogin} />;
}

export default Login;
