// src/components/client/Header.js
import React, { use, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Header.css";
import { useDispatch, useSelector } from "react-redux";
import { clearUser } from "../../redux/userSlice";
import { ShoppingCart } from "lucide-react"; // ✅ icon giỏ hàng
import { getTotalQuantity } from "../../redux/cartSlice";

const Header = () => {
  const user = useSelector((state) => state.user);
  const cart = useSelector((state) => state.cart); // ✅ lấy giỏ hàng từ Redux
  const cartTotalQuantity = cart.items.reduce((total, i) => total + i.quantity, 0);
  const isLoggedIn = !!user.username;

  const [isHovering, setIsHovering] = useState(false);
  const [keyword, setKeyword] = useState("");

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(clearUser());
    console.log("logout");
  };

  return (
    <header className="header">
      <div className="container header-content">
        {/* Logo */}
        <Link to="/" className="logo">
          <span>🛒 Tạp Hóa Xanh</span>
        </Link>

        {/* Ô tìm kiếm */}
        <div className="search-bar">
          <input
            type="text"
            placeholder="Tìm sản phẩm..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
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
                src={
                  "https://scontent.fdad3-6.fna.fbcdn.net/v/t39.30808-6/541324630_1425384951862072_1412098268221867522_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeEmtwcrtuA_cjjHeQZkRnBDd5vqFyFDi0d3m-oXIUOLR_JNVHVh907rmIKOezQDs8WdeuKv90qJmNONn-Bd4ypo&_nc_ohc=z9sqF6c2eS8Q7kNvwHWpF3W&_nc_oc=Adl2nq5ZXd8KDfDWDC0s8ITe4FGCdbxjrXGXgAkxS1Aw6CamhVwET0uZRznVhVSWxNjy7jvbbERcmQ1Ns8E2D2TF&_nc_zt=23&_nc_ht=scontent.fdad3-6.fna&_nc_gid=ohJVHsFs9wU0VhbTFb_qkA&oh=00_AfbgA0mZEPZ9lr5OGZTfJshpdObmHD33DZLLSTMFbSRSZA&oe=68C4DC13"
                }
                alt="Avatar"
                className="avatar-icon"
                style={{
                  width: "32px",
                  height: "32px",
                  borderRadius: "50%",
                  cursor: "pointer",
                }}
              />
              {isHovering && (
                <div
                  className="avatar-popup"
                  style={{
                    position: "absolute",
                    top: "20px",
                    right: 0,
                    background: "#fff",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
                    borderRadius: "8px",
                    padding: "12px",
                    minWidth: "200px",
                    zIndex: 100,
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                  onMouseEnter={() => setIsHovering(true)}
                  onMouseLeave={() => setIsHovering(false)}
                >
                  <Link
                    to="/profile"
                    className="popup-btn"
                    style={{
                      display: "block",
                      marginBottom: "8px",
                      color: "black",
                    }}
                  >
                    Tài khoản của tôi
                  </Link>
                  <Link
                    to="/orders"
                    className="popup-btn"
                    style={{
                      display: "block",
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
