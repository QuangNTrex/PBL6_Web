import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import "./SearchPage.css";
import { API_URL } from "../../utils/lib";
import ProductCard from "../../components/client/ProductCard";

const SearchPage = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  const [sort, setSort] = useState(""); // sort: asc, desc
  const [category, setCategory] = useState("");

  const access_token = localStorage.getItem("access_token");

  // Lấy query param q
  const { search } = useLocation();
  const params = new URLSearchParams(search);
  const q = params.get("q") || "";

  useEffect(() => {
    // Gọi API lấy categories
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

  useEffect(() => {
    if (!q) return;

    setLoading(true);
    let url = `${API_URL}products/search?q=${encodeURIComponent(q)}`;
    if (category) url += `&category=${category}`;
    if (sort) url += `&sort=${sort}`;

    fetch(url, {
      headers: { Authorization: `Bearer ${access_token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Lỗi phản hồi từ server");
        return res.json();
      })
      .then((data) => {
        console.log(data);
        setProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Lỗi tìm sản phẩm:", err);
        setLoading(false);
      });
  }, [q]);

  const newProducts = products.filter(p => category ? p.category.id == category : true);
  newProducts.sort((p1, p2) => (sort === "asc" ? p1.price - p2.price : sort==="desc" ? p2.price - p1.price: true));
  return (
    <div className="search-container">
      <h2 className="search-title">
        Kết quả tìm kiếm cho: <span>"{q}"</span>
      </h2>

      {/* Bộ lọc */}
      <div className="filters">
        <select value={sort} onChange={(e) => setSort(e.target.value)}>
          <option value="">Sắp xếp</option>
          <option value="asc">Giá: Thấp → Cao</option>
          <option value="desc">Giá: Cao → Thấp</option>
        </select>

        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="">Tất cả danh mục</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Đang tải...</p>
      ) : products.length > 0 ? (
        <div className="product-grid">
          {newProducts.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      ) : (
        <p>Không tìm thấy sản phẩm nào.</p>
      )}
    </div>
  );
};

export default SearchPage;
