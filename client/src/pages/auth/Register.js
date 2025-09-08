// src/pages/auth/Register.js
import React from "react";
import { useDispatch } from "react-redux";
import { setUser } from "../../redux/userSlice";
import AuthForm from "./AuthForm";
import authApi from "../../api/authApi";
import { API_URL } from "../../utils/lib";
import { useNavigate } from "react-router-dom";

function Register() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleRegister = async (formData) => {
    // fetch(API_URL + "auth/test").then(res => res.json()).then(data => {
    //        console.log(data)
    //     }).catch(err => {
    //         console.error("Đăng ký thất bại:", err);
    //     })

    console.log(formData);
    const abc = { username: formData.username, email: formData.email, password: formData.password, full_name: formData.full_name };

    
    fetch(API_URL + "auth/register", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(abc)
        }).then(res => res.json()).then(data => {
          console.log(data);
            console.log(data)
            navigate("/login");
        }).catch(err => {
            console.error("Đăng ký thất bại:", err);
        })
  };

  return <AuthForm type="register" onSubmit={handleRegister} />;
}

export default Register;
