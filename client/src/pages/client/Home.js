// src/pages/client/Home.js
import React, { useRef } from "react";
import Banner from "../../components/client/Banner";
import CategoryList from "../../components/client/CategoryList";
import ProductList from "../../components/client/ProductList";

const Home = () => {
  const productsRef = useRef(null);
  const handleScroll = () => {
    setTimeout(() => {
      productsRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 150); 
  };
  return (
    <div>
      {/* Banner */}
      <Banner />

      <div className="container" style={{ padding: "20px" }}>
        {/* Danh mục */}
        <h2 style={{ marginBottom: "3rem" }}>Danh mục sản phẩm</h2>
        <CategoryList/>

        {/* Sản phẩm nổi bật */}
        <h2 style={{ margin: "30px 0 10px" ,marginBottom: "15rem"}} ref={productsRef}></h2>
        <h2 style={{ margin: "30px 0 10px", marginBottom: "4rem"}} >Sản phẩm nổi bật</h2>
        {/* <h2 style={{ margin: "30px 0 10px" }}>🛒 Danh sách sản phẩm</h2> */}
        <ProductList scroll={handleScroll} />
      </div>
    </div>
  );
};

export default Home;
