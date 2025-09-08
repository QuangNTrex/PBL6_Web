// src/pages/auth/Login.js
import React from "react";
import { useDispatch } from "react-redux";
import { setUser } from "../../redux/userSlice";
import AuthForm from "./AuthForm";
import authApi from "../../api/authApi";    
import { useNavigate } from "react-router-dom";
import { API_URL, SERVERURL } from "../../utils/lib";

function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const access_token = localStorage.getItem("access_token");
  const handleLogin = async (formData) => {
    console.log(formData);
    fetch(API_URL + "auth/login", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            }).then(res => res.json()).then(data => {
                console.log(data);
                dispatch(setUser(data.user));
                localStorage.setItem("access_token", data.access_token);
                dispatch(setUser(data.user));
                navigate("/");

            }).catch(err => {
                console.error("Đăng nhập thất bại:", err);
            })
  };

  return <AuthForm type="login" onSubmit={handleLogin} />;
}

export default Login;
