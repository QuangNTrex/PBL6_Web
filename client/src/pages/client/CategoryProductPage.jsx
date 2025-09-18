// src/pages/client/CategoryProductsPage.js
import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import "./CategoryProductsPage.css";
import { API_URL } from "../../utils/lib";

export default function CategoryProductsPage() {
  const { categoryId } = useParams(); // lấy id từ URL
  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate(); 

  useEffect(() => {
    async function fetchData() {
      try {
        // Lấy thông tin danh mục
        const resCategory = await fetch(API_URL + `categories/${categoryId}`);
        const categoryData = await resCategory.json();
        setCategory(categoryData);
        console.log("✅ Thông tin danh mục đã tải:", categoryData);

        // Lấy sản phẩm trong danh mục
        const resProducts = await fetch(API_URL + `products/category/${categoryId}`);
        const productsData = await resProducts.json();
        setProducts(productsData);
        console.log("✅ Sản phẩm trong danh mục đã tải:", productsData);
      } catch (err) {
        console.error("Lỗi khi tải dữ liệu:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [categoryId]);

  if (loading) return <p className="loading">Đang tải dữ liệu...</p>;
  
  return (
    <div className="category-products-container">
      <h2 className="category-title">
        Danh mục: {category?.name || "Không xác định"}
      </h2>

      {products.length === 0 ? (
        <p>Không có sản phẩm nào trong danh mục này.</p>
      ) : (
        <div className="product-grid">
          {products.map((p) => (
            <div onClick={() => navigate("/products/" + p.id)} key={p.id} className="product-card">
              <img src={p.image_path} alt={p.name} />
              <h3>{p.name}</h3>
              <p className="price">{p.price.toLocaleString()} đ</p>
              <button className="btn-add">Thêm vào giỏ</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
