import React from "react";
import Header from "../components/admin/Header";
import Sidebar from "../components/admin/Sidebar";
import { Outlet } from "react-router-dom";
import "./AdminLayout.css";




const AdminLayout = () => {
  return (
    <div className="admin-container">
      <Header />
      <div className="admin-body">
        <Sidebar />
        <main className="admin-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
