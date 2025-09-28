import React, { useEffect, useRef, useState } from "react";
import "./ProductList.css";
import { API_URL } from "../../utils/lib";
import ProductCard from "./ProductCard";  // ✅ import component tái sử dụng

const ProductList = ({scroll}) => {
  const [products, setProducts] = useState([]);
  const [page, setPage] = useState(1);
  const [size] = useState(20);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const productsRef = useRef(null);

  const handleScroll = () => {
    setTimeout(() => {
      productsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 2000); 
    
  };

  const fetchProducts = async (pageNum) => {
    try {
      setLoading(true);
      const res = await fetch(`${API_URL}products/pagination?page=${pageNum}&size=${size}`);
      const data = await res.json();

      setProducts(data.products || []);
      setTotalPages(data.totalPages || 1);
      setLoading(false);
      
    } catch (err) {
      console.error("Lỗi khi load sản phẩm:", err);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts(page);
  }, [page]);

  const handlePrev = () => {
    page > 1 && setPage(page - 1)
    scroll();
  };
  const handleNext = () => {
    page < totalPages && setPage(page + 1)
    scroll();
  };
  console.log(products);

  return (
    <div className="product-list-container" ref={productsRef}>
      {loading ? (
        <p>Đang tải dữ liệu...</p>
      ) : (
        <div className="product-list">
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />  
          ))}
        </div>
      )}

      <div className="pagination">
        <button onClick={handlePrev} disabled={page === 1}>⬅ Trước</button>
        <span>Trang {page}/{totalPages}</span>
        <button onClick={handleNext} disabled={page === totalPages}>Tiếp ➡</button>
      </div>
    </div>
  );
};

export default ProductList;
