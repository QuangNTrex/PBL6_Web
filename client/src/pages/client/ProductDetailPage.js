// src/pages/client/ProductDetailPage.js
import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./ProductDetailPage.css";
import { useDispatch } from "react-redux";
import { addToCart } from "../../redux/cartSlice";

const ProductDetailPage = () => {
  const { id } = useParams();
  const dispatch = useDispatch();

  const [product, setProduct] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await fetch(`http://localhost:8000/products/${id}`);
        if (!res.ok) {
          throw new Error("Failed to fetch product");
        }
        const data = await res.json();
        setProduct(data);
      } catch (err) {
        console.error("❌ Lỗi khi gọi API:", err);
      }
    };

    fetchProduct();
  }, [id]);

  const [quantity, setQuantity] = useState(1);

  const increaseQty = () => setQuantity((prev) => prev + 1);
  const decreaseQty = () => setQuantity((prev) => (prev > 1 ? prev - 1 : 1));

  const handleAddToCart = () => {
    dispatch(addToCart({product, quantity }));
  };
  
   if (!product) return <p>Đang tải...</p>;

  return (
    <div className="product-detail-container">
      <div className="product-detail-card">
        {/* Hình ảnh */}
        <div className="product-image">
          <img src={product.image_path} alt={product.name} />
        </div>

        {/* Thông tin */}
        <div className="product-info">
          <h1 className="product-name">{product.name}</h1>
          <p className="product-code">Mã sản phẩm: {product.code}</p>
          <p className="product-category">
            Danh mục: <strong>{product.category.name}</strong>
          </p>
          <p className="product-price">{product.price}đ</p>
          

          {/* Nhập số lượng */}
          <div className="quantity-control">
            <button onClick={decreaseQty}>-</button>
            <input
              type="number"
              min="1"
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
            />
            <button onClick={increaseQty}>+</button>
          </div>

          {/* Nút thêm giỏ hàng */}
          <button className="add-cart-btn" onClick={handleAddToCart}>
            Thêm vào giỏ hàng
          </button>
        </div>
      </div>
      {/* Mô tả sản phẩm */}
      <div className="product-description">
        <h2>Mô tả sản phẩm</h2>
        <p>{product.description}</p>
      </div>
    </div>
  );
};

export default ProductDetailPage;