// src/components/client/CategoryList.js
import React, { useEffect, useState } from "react";
import "./CategoryList.css";
import { API_URL } from "../../utils/lib";



const CategoryList = () => {
  const access_token = localStorage.getItem("access_token");
  const [categories, setCategories] = useState([])
  useEffect(() => {
    fetch(`${API_URL}categories/`, {
      headers: { Authorization: `Bearer ${access_token}` },
    })
      .then((res) => res.json())
      .then((data) =>{
         setCategories(data)
         console.log(data)
      })
      .catch((err) => console.error("Lỗi lấy categories:", err));
  }, []);
  return (
    <div className="category-list">
      {categories.map((cat) => (
        <div key={cat.id} className="category-card">
          <img src={cat.image_url} alt={cat.name} />
          <p>{cat.name}</p>
        </div>
      ))}
    </div>
  );
};

export default CategoryList;
