// src/pages/client/Home.js
import React from "react";
import Banner from "../../components/client/Banner";
import CategoryList from "../../components/client/CategoryList";
import ProductList from "../../components/client/ProductList";

const Home = () => {
  return (
    <div>
      {/* Banner */}
      <Banner />

      <div className="container" style={{ padding: "20px" }}>
        {/* Danh mục */}
        <h2 style={{ marginBottom: "10px" }}>Danh mục sản phẩm</h2>
        <CategoryList/>

        {/* Sản phẩm nổi bật */}
        <h2 style={{ margin: "30px 0 10px" }}>Sản phẩm nổi bật</h2>
        {/* <h2 style={{ margin: "30px 0 10px" }}>🛒 Danh sách sản phẩm</h2> */}
        <ProductList />
      </div>
    </div>
  );
};

export default Home;
