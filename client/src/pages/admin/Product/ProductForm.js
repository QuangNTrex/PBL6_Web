import React, { useState, useEffect } from "react";
import "./ProductForm.css";

const ProductForm = ({ categories, initialData = {}, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    code: "",
    name: "",
    price: "",
    quantity: 0,
    description: "",
    unit: "cái",
    image_path: "",
    category_id: "",
  });

  // Nếu có initialData (khi sửa), load vào form
  useEffect(() => {
    if (initialData && Object.keys(initialData).length > 0) {
      setFormData({
        code: initialData.code || "",
        name: initialData.name || "",
        price: initialData.price || "",
        quantity: initialData.quantity || 0,
        description: initialData.description || "",
        unit: initialData.unit || "cái",
        image_path: initialData.image_path || "",
        category_id: initialData.category.id || "",
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  console.log(formData);

  return (
    <div className="product-form-modal">
      <form className="product-form" onSubmit={handleSubmit}>
        <h3>{initialData?.id ? "✏ Sửa sản phẩm" : "➕ Thêm sản phẩm"}</h3>

        <input
          type="text"
          name="code"
          placeholder="Mã sản phẩm (SKU)"
          value={formData.code}
          onChange={handleChange}
        />
        <input
          type="text"
          name="name"
          placeholder="Tên sản phẩm"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="price"
          placeholder="Giá"
          value={formData.price}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="quantity"
          placeholder="Số lượng"
          value={formData.quantity}
          onChange={handleChange}
        />
        <input
          type="text"
          name="unit"
          placeholder="Đơn vị (vd: cái, hộp, kg)"
          value={formData.unit}
          onChange={handleChange}
        />
        <input
          type="text"
          name="image_path"
          placeholder="Đường dẫn ảnh"
          value={formData.image_path}
          onChange={handleChange}
        />
        <textarea
          name="description"
          placeholder="Mô tả sản phẩm"
          value={formData.description}
          onChange={handleChange}
        />
        <select
          name="category_id"
          value={formData.category_id}
          onChange={handleChange}
          required
        >
          <option value="">Chọn danh mục</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id} selected={c.id === formData.category_id}>
              {c.name}
            </option>
          ))}
        </select>

        <div className="form-actions">
          <button type="submit">💾 Lưu</button>
          <button type="button" onClick={onCancel}>
            ❌ Hủy
          </button>
        </div>
      </form>
    </div>
  );
};

export default ProductForm;
