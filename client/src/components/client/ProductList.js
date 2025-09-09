// src/components/client/ProductList.js
import React, { useEffect, useState } from "react";
import "./ProductList.css";
import { API_URL } from "../../utils/lib"; // chỉnh lại path nếu khác

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(1);        // trang hiện tại
  const [size] = useState(10);                // số sản phẩm mỗi trang
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);

  const fetchProducts = async (pageNum) => {
    try {
      setLoading(true);
      const res = await fetch(`${API_URL}products/pagination?page=${pageNum}&size=${size}`);
      const data = await res.json();

      // Giả định backend trả về { items: [], totalPages: N }
      setProducts(data || []);
      setTotalPages(data.totalPages || 1);
      setLoading(false);
      console.log("Sản phẩm:", data);
    } catch (err) {
      console.error("Lỗi khi load sản phẩm:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts(page);
  }, [page]);

  const handlePrev = () => {
    if (page > 1) setPage(page - 1);
  };

  const handleNext = () => {
    if (page < totalPages) setPage(page + 1);
  };

  return (
    <div className="product-list-container">
      

      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : (
        <div className="product-list">
          {products.map((p) => (
            <div key={p.id} className="product-card">
              <img src={p.image_url} alt={p.name} />
              <h3>{p.name}</h3>
              <p className="price">{p.price}đ</p>
              <button>Thêm vào giỏ</button>
            </div>
          ))}
        </div>
      )}

      {/* Điều khiển phân trang */}
      <div className="pagination">
        <button onClick={handlePrev} disabled={page === 1}>
          ⬅ Trước
        </button>
        <span>
          Trang {page}/{totalPages}
        </span>
        <button onClick={handleNext} disabled={page === totalPages}>
          Tiếp ➡
        </button>
      </div>
    </div>
  );
};

export default ProductList;
