import React from "react";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <aside className="admin-sidebar">
      <ul>
        <li><a href="#">🏠 Dashboard</a></li>
        <li><a href="#">👤 Users</a></li>
        <li><a href="#">📦 Products</a></li>
        <li><a href="#">⚙ Settings</a></li>
      </ul>
    </aside>
  );
};

export default Sidebar;
