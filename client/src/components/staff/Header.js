import React, { useState } from "react";
import "./Header.css";
import { useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { API_URL } from "../../utils/lib";
import { clearUser } from "../../redux/userSlice";

const Header = () => {
  const [open, setOpen] = useState(false);
  const user = useSelector(state => state.user); 
  const access_token = localStorage.getItem("access_token") 
  const dispatch = useDispatch()  

  const toggleMenu = () => {
    setOpen(!open);
  };

    const logoutHandler = () => {
    fetch(API_URL + "auth/logout", {
      method: "GET",
      headers: {
        "Authorization": "Bearer " + access_token,
      }
    }).then(res => {
      
    })
    dispatch(clearUser());
    console.log("logout");
  };

  return (
    <header className="admin-header">
      <h1 className="admin-title">Staff Dashboard</h1>

      <div className="admin-profile">
        <img
          src={user.avatar_url}  // ảnh avatar mẫu
          alt={user.role}
          className="admin-avatar"
          onClick={toggleMenu}
        />

        {open && (
          <div className="admin-menu">
            <div className="admin-info">
              <img
                src={user.avatar_url}  // ảnh avatar mẫu
                alt="Admin"
                className="admin-avatar-large"
              />
              <div>
                <strong>{user.full_name}</strong>
                <p>Admin</p>
              </div>
            </div>
           <ul>
              <li>
                <Link to="/profile"> Tài khoản của tôi</Link>
              </li>
              <li>
                <Link to="/staff/settings"> Cài đặt</Link>
              </li>
              <li>
                <Link to="/"> Trang chủ</Link>
              </li>
              <li>
                <Link onClick={logoutHandler}> Đăng xuất</Link>
              </li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
