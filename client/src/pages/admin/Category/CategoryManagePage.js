import React, { useEffect, useState } from "react";
import "./CategoryManagePage.css";
import { API_URL } from "../../../utils/lib";

const CategoryManagePage = () => {
  const [categories, setCategories] = useState([]);
  const access_token = localStorage.getItem("access_token");

  const [newCategory, setNewCategory] = useState("");
  const [newImage, setNewImage] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editedName, setEditedName] = useState("");
  const [editedImage, setEditedImage] = useState("");

  // ----------------- Thêm mới -----------------
  const handleAdd = () => {
    if (!newCategory.trim()) return;

    fetch(API_URL + "categories/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify({ name: newCategory, image_url: newImage }),
    })
      .then((res) => res.json())
      .then((data) => {
        setCategories([...categories, data]);
        setNewCategory("");
        setNewImage("");
      })
      .catch((err) => {
        console.error("Thêm thất bại:", err);
      });
  };

  // ----------------- Xóa -----------------
  const handleDelete = (id) => {
    fetch(API_URL + "categories/" + id, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then(() => {
        setCategories(categories.filter((cat) => cat.id !== id));
      })
      .catch((err) => {
        console.error("Xóa thất bại:", err);
      });
  };

  // ----------------- Sửa -----------------
  const handleEdit = (id, name, image_url) => {
    setEditingId(id);
    setEditedName(name);
    setEditedImage(image_url || "");
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditedName("");
    setEditedImage("");
  };

  const handleConfirmEdit = (id) => {
    if (!editedName.trim()) return;

    fetch(API_URL + "categories/" + id, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify({ name: editedName, image_url: editedImage }),
    })
      .then((res) => res.json())
      .then((data) => {
        setCategories(
          categories.map((cat) =>
            cat.id === id
              ? { ...cat, name: data.name, image_url: data.image_url }
              : cat
          )
        );
        setEditingId(null);
        setEditedName("");
        setEditedImage("");
      })
      .catch((err) => {
        console.error("Sửa thất bại:", err);
      });
  };

  // ----------------- Lấy dữ liệu -----------------
  useEffect(() => {
    fetch(API_URL + "categories/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setCategories(data);
      })
      .catch((err) => {
        console.error("Lấy danh mục thất bại:", err);
      });
  }, []);

  return (
    <div className="category-container">
      <h2>📂 Quản lý Category</h2>

      <div className="category-form">
        <input
          type="text"
          placeholder="Tên category..."
          value={newCategory}
          onChange={(e) => setNewCategory(e.target.value)}
        />
        <input
          type="text"
          placeholder="URL ảnh..."
          value={newImage}
          onChange={(e) => setNewImage(e.target.value)}
        />
        <button onClick={handleAdd}>Thêm</button>
      </div>

      <table className="category-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Tên Category</th>
            <th>Ảnh</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {categories.map((cat) => (
            <tr key={cat.id}>
              <td>{cat.id}</td>
              <td>
                {editingId === cat.id ? (
                  <input
                    type="text"
                    value={editedName}
                    onChange={(e) => setEditedName(e.target.value)}
                  />
                ) : (
                  cat.name
                )}
              </td>
              <td>
                {editingId === cat.id ? (
                  <input
                    type="text"
                    value={editedImage}
                    onChange={(e) => setEditedImage(e.target.value)}
                  />
                ) : cat.image_url ? (
                  <img
                    src={cat.image_url}
                    alt={cat.name}
                    style={{ width: "60px", height: "60px", objectFit: "cover" }}
                  />
                ) : (
                  "—"
                )}
              </td>
              <td>
                {editingId === cat.id ? (
                  <>
                    <button
                      className="confirm-btn"
                      onClick={() => handleConfirmEdit(cat.id)}
                    >
                      Xác nhận
                    </button>
                    <button className="cancel-btn" onClick={handleCancelEdit}>
                      Hủy
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      className="edit-btn"
                      onClick={() =>
                        handleEdit(cat.id, cat.name, cat.image_url)
                      }
                    >
                      ✏ Sửa
                    </button>
                    <button
                      className="delete-btn"
                      onClick={() => handleDelete(cat.id)}
                    >
                      🗑 Xóa
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CategoryManagePage;
