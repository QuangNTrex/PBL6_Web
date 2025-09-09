import React from "react";
import Header from "../components/admin/Header";
import Sidebar from "../components/admin/Sidebar";

const AdminLayout = ({ children }) => {
  return (
    <div className="admin-container">
      <Header />
      <div className="admin-body">
        <Sidebar />
        <main className="admin-content">{children}</main>
      </div>
    </div>
  );
};

export default AdminLayout;
