import React from "react";
import "./ProductItem.css";

const ProductItem = ({ product }) => {
  return (
    <div className="product-card">
      <img
        src={product.image_path || "/default-product.png"}
        alt={product.name}
        className="product-img"
      />
      <div className="product-info">
        <h3>{product.name}</h3>
        <p className="product-price">
          {product.price.toLocaleString()} đ
        </p>
        <p className="product-desc">
          {product.description || "Không có mô tả"}
        </p>
      </div>
    </div>
  );
};

export default ProductItem;
