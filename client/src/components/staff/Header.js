import React, { useState } from "react";
import "./Header.css";
import { useSelector } from "react-redux";
import { Link } from "react-router-dom";

const Header = () => {
  const [open, setOpen] = useState(false);
  const user = useSelector(state => state.user);    

  const toggleMenu = () => {
    setOpen(!open);
  };

    const logoutHandler = () => () => {
    }

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
                <Link to="/staff/profile">👤 Tài khoản của tôi</Link>
              </li>
              <li>
                <Link to="/staff/settings">⚙ Cài đặt</Link>
              </li>
              <li>
                <Link onClick={logoutHandler()}>🚪 Đăng xuất</Link>
              </li>
            </ul>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
