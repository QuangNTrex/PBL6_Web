import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <aside className="admin-sidebar">
      <ul>
        <li>
          <NavLink to="/admin" end>
            Dashboard
          </NavLink>
        </li>
        <li>
          <NavLink to="/admin/orders">
            Orders
          </NavLink>
        </li>
        <li>
          <NavLink to="/admin/users">
            Users
          </NavLink>
        </li>
        <li>
          <NavLink to="/admin/categories">
            Categories
          </NavLink>
        </li>
        <li>
          <NavLink to="/admin/products">
            Products
          </NavLink>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
