import React from "react";
import "./ProductCard.css";
import { useDispatch } from "react-redux";
import { addToCart } from "../../redux/cartSlice";
import { useNavigate } from "react-router-dom";
import "./ProductCard.css";

export default function ProductCard({ product }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleAddToCart = (e) => {
    e.preventDefault(); // Ngăn chặn sự kiện mặc định của thẻ <a> hoặc <button>
    e.stopPropagation(); // Ngăn chặn sự kiện nổi bọt lên các phần tử cha
    dispatch(addToCart({ product, quantity: 1 }));
  };

  return (
    <div className="product-card" onClick={() => {
        navigate(`/products/${product.id}`);
    }}>
      <img src={product.image_path} alt={product.name} className="product-image-1" />
      <h3 className="product-name">{product.name}</h3>
      <p className="product-price">{product.price.toLocaleString()} đ</p>
      <button className="add-cart-btn" onClick={handleAddToCart}>
        🛒 Thêm vào giỏ
      </button>
    </div>
  );
}
