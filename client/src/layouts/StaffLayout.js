import React from "react";
import Header from "../components/staff/Header";
import Sidebar from "../components/staff/Sidebar";
import { Outlet } from "react-router-dom";
import "./StaffLayout.css";




const StaffLayout = () => {
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

export default StaffLayout;
