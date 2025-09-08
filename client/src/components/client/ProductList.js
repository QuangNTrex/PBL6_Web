// src/components/client/ProductList.js
import React from "react";
import "./ProductList.css";

const products = [
  { id: 1, name: "Táo Mỹ", price: "50.000đ/kg", img: "https://via.placeholder.com/150" },
  { id: 2, name: "Cam Sành", price: "40.000đ/kg", img: "https://via.placeholder.com/150" },
  { id: 3, name: "Coca-Cola", price: "12.000đ/lon", img: "https://via.placeholder.com/150" },
  { id: 4, name: "Mì Gói", price: "4.000đ/gói", img: "https://via.placeholder.com/150" },
];

const ProductList = () => {
  return (
    <div className="product-list">
      {products.map((p) => (
        <div key={p.id} className="product-card">
          <img src={p.img} alt={p.name} />
          <h3>{p.name}</h3>
          <p className="price">{p.price}</p>
          <button>Thêm vào giỏ</button>
        </div>
      ))}
    </div>
  );
};

export default ProductList;
