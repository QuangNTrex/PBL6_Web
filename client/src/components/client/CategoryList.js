// src/components/client/CategoryList.js
import React from "react";
import "./CategoryList.css";

const categories = [
  { id: 1, name: "Rau củ", img: "https://cdnv2.tgdd.vn/bhx-static/bhx/Category/Images/8820/rau-la_202509081007292616.png" },
  { id: 2, name: "Trái cây", img: "https://via.placeholder.com/100" },
  { id: 3, name: "Đồ uống", img: "https://via.placeholder.com/100" },
  { id: 4, name: "Gia vị", img: "https://via.placeholder.com/100" },
];

const CategoryList = () => {
  return (
    <div className="category-list">
      {categories.map((cat) => (
        <div key={cat.id} className="category-card">
          <img src={cat.img} alt={cat.name} />
          <p>{cat.name}</p>
        </div>
      ))}
    </div>
  );
};

export default CategoryList;
