// src/layouts/ClientLayout.js
import React from "react";
import Header from "../components/client/Header";
import Footer from "../components/client/Footer";
import { Outlet } from "react-router-dom";

const ClientLayout = () => {
  return (
    <div className="client-layout">
      {/* Header */}
      <Header />

      {/* Nội dung trang con */}
      <main style={{ minHeight: "70vh", padding: "6rem", paddingTop: "2rem"}}>
        <Outlet />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default ClientLayout;
