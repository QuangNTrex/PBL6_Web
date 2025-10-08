import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <aside className="admin-sidebar">
      <ul>
        <li>
          <NavLink to="/staff/orders">
            Orders
          </NavLink>
        </li>
        <li>
          <NavLink to="/staff/scan-product">
            Scan product
          </NavLink>
        </li>
        
        <li>
          <NavLink to="/staff/products">
            Products
          </NavLink>
        </li>
      </ul>
    </aside>
  );
};

export default Sidebar;
