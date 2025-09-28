// src/components/client/Header.js
import React, { use, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Header.css";
import { useDispatch, useSelector } from "react-redux";
import { clearUser } from "../../redux/userSlice";
import { ShoppingCart } from "lucide-react"; // ✅ icon giỏ hàng
import { getTotalQuantity } from "../../redux/cartSlice";
import { API_URL } from "../../utils/lib";

const Header = () => {
  const user = useSelector((state) => state.user);
  const cart = useSelector((state) => state.cart); // ✅ lấy giỏ hàng từ Redux
  const cartTotalQuantity = cart.items.reduce((total, i) => total + i.quantity, 0);
  const isLoggedIn = !!user.username;
  const access_token = localStorage.getItem("access_token")

  const [isHovering, setIsHovering] = useState(false);
  const [isHovering1, setIsHovering1] = useState(false);
  const [keyword, setKeyword] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
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
    <header className="header">
      <div className="container header-content">
        {/* Logo */}
        <Link to="/" className="logo">
          <span>Tạp Hóa Xanh</span>
        </Link>

        {/* Ô tìm kiếm */}
        <div className="search-bar">
          <input
            type="text"
            placeholder="Tìm sản phẩm..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                // gọi hàm rỗng hoặc xử lý gì đó
                console.log("Enter pressed");
                navigate(`/search?q=${encodeURIComponent(keyword)}`);
              }
            }}
          />
          <button
            onClick={() => {
              navigate(`/search?q=${encodeURIComponent(keyword)}`);
            }}
          >
            Tìm
          </button>
        </div>

        {/* Menu */}
        <nav className="nav-links">
          {/* ✅ Nút giỏ hàng với icon + badge */}
          <Link to="/cart" className="cart-icon-container">
            <ShoppingCart size={24} />
            {cartTotalQuantity > 0 && (
              <span className="cart-badge">{cartTotalQuantity}</span>
            )}
          </Link>

          {!isLoggedIn ? (
            <>
              <Link to="/login">Đăng nhập</Link>
              <Link to="/register">Đăng ký</Link>
            </>
          ) : (
            <div
              className="avatar-container"
              style={{ position: "relative", display: "inline-block" }}
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
            >
              <img
                src={user.avatar_url}
                alt="Avatar"
                className="avatar-icon"
                style={{
                  width: "2rem",
                  height: "2rem",
                  borderRadius: "50%",
                  cursor: "pointer",
                  marginLeft: "0.5rem"
                }}
              />
              {(isHovering || isHovering1) && (
                <div
                  className="avatar-popup"
                  style={{
                    position: "absolute",
                    top: "20px",
                    right: 0,
                    background: "#fff",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
                    borderRadius: "8px",
                    padding: "1rem",
                    paddingTop: "2rem",
                    paddingBottom: "2rem",
                    minWidth: "200px",
                    zIndex: 100,
                    display: "flex",
                    gap: "1rem",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                  onMouseEnter={() => setIsHovering1(true)}
                  onMouseLeave={() => setIsHovering1(false)}
                >
                  <Link
                    to="/profile"
                    className="popup-btn"
                    style={{

                      color: "black",
                    }}
                  >
                    Tài khoản của tôi
                  </Link>
                  <Link
                    to="/orders"
                    className="popup-btn"
                    style={{

                      marginBottom: "8px",
                      color: "black",
                    }}
                  >
                    Đơn mua
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="popup-btn"
                    style={{
                      display: "block",
                      width: "100%",
                      background: "none",
                      border: "none",
                      color: "#e74c3c",
                      cursor: "pointer",
                    }}
                  >
                    Đăng xuất
                  </button>
                </div>
              )}
            </div>
          )}
        </nav>
      </div>
    </header>
  );
};

export default Header;
