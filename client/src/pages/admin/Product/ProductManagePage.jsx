import React, { useEffect, useState } from "react";
import "./ProductManagePage.css";
import { API_URL } from "../../../utils/lib";
import ProductForm from "./ProductForm";
import { useSelector } from "react-redux";

const ProductManagePage = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");

  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const access_token = localStorage.getItem("access_token");
  const user = useSelector(state => state.user)

  // =============== Load data ===============
  useEffect(() => {
    fetch(API_URL + "categories/", {
      headers: { Authorization: `Bearer ${access_token}` },
    })
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch((err) => console.error("Lỗi tải category:", err));

    fetchProducts();
  }, []);

  const fetchProducts = () => {
    fetch(API_URL + "products/", {
      headers: { Authorization: `Bearer ${access_token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        if(data.detail) throw new Error(data.detail);
        console.log("Sản phẩm:", data);
        setProducts(data);
      })
      .catch((err) => console.error("Lỗi tải sản phẩm:", err));
  };

  // =============== Thêm & Sửa sản phẩm ===============
  const handleSubmitProduct = (formData) => {
    if (editingProduct) {
      // --- Sửa sản phẩm ---
      fetch(API_URL + "products/" + editingProduct.id, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
        body: JSON.stringify({
          ...formData,
          price: parseFloat(formData.price),
          quantity: parseInt(formData.quantity),
          category_id: parseInt(formData.category_id),
          user_id: user.id
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          setProducts(products.map((p) => (p.id === data.id ? data : p)));
          setShowForm(false);
          setEditingProduct(null);
        })
        .catch((err) => console.error("Lỗi sửa sản phẩm:", err));
    } else {
      // --- Thêm sản phẩm ---
      const product = {
          ...formData,
          price: parseFloat(formData.price),
          quantity: parseInt(formData.quantity),
          category_id: parseInt(formData.category_id),
          user_id: user.id
        }
        console.log("Thêm sản phẩm:", product);
      fetch(API_URL + "products/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
        body: JSON.stringify(product),
      })
        .then((res) => res.json())
        .then((data) => {
          setProducts([...products, data]);
          setShowForm(false);
        })
        .catch((err) => console.error("Lỗi thêm sản phẩm:", err));
    }
  };

  const handleEdit = (product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  // =============== Xóa sản phẩm ===============
  const handleDelete = (id) => {
    fetch(API_URL + "products/" + id, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${access_token}` },
    })
      .then(() => {
        setProducts(products.filter((p) => p.id !== id));
      })
      .catch((err) => console.error("Lỗi xóa sản phẩm:", err));
  };

  // =============== Lọc + tìm kiếm ===============
  const filteredProducts = products.filter((p) => {
    const matchCategory =
      selectedCategory === "all" || p.category.id === parseInt(selectedCategory);
    const matchSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase());
    return matchCategory && matchSearch;
  });

  return (
    <div className="product-container">
      <h2>🛒 Quản lý Sản phẩm</h2>

      {/* Bộ lọc */}
      <div className="filters">
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="all">Tất cả danh mục</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Tìm kiếm sản phẩm..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />

        <button onClick={() => { setShowForm(true); setEditingProduct(null); }}>
          ➕ Thêm sản phẩm
        </button>
      </div>

      {/* Bảng sản phẩm */}
      <table className="product-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Mã SP</th>
            <th>Tên SP</th>
            <th>Giá</th>
            <th>Số lượng</th>
            <th>Danh mục</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {filteredProducts.map((p) => (
            <tr key={p.id}>
              <td>{p.id}</td>
              <td>{p.code}</td>
              <td>{p.name}</td>
              <td>{p.price}</td>
              <td>{p.quantity}</td>
              <td>{p.category.name}</td>
              <td>
                <button onClick={() => handleEdit(p)}>✏ Sửa</button>
                <button onClick={() => handleDelete(p.id)}>🗑 Xóa</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Form thêm/sửa */}
      {showForm && (
        <ProductForm
          categories={categories}
          initialData={editingProduct}
          onSubmit={handleSubmitProduct}
          onCancel={() => {
            setShowForm(false);
            setEditingProduct(null);
          }}
        />
      )}
    </div>
  );
};

export default ProductManagePage;
