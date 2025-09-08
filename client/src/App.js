import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Layouts
import AdminLayout from "./layouts/AdminLayout";
import ClientLayout from "./layouts/ClientLayout";

// Auth Pages
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

// Admin Pages
import Dashboard from "./pages/admin/Dashboard";
import ProductList from "./pages/admin/Product/ProductList";
import ProductForm from "./pages/admin/Product/ProductForm";
import CategoryList from "./pages/admin/Category/CategoryList";
import CategoryForm from "./pages/admin/Category/CategoryForm";
import UserList from "./pages/admin/User/UserList";
import UserForm from "./pages/admin/User/UserForm";
import OrderList from "./pages/admin/Order/OrderList";

// Client Pages
import Home from "./pages/client/Home";
import ProductDetail from "./pages/client/ProductDetail";
import CategoryPage from "./pages/client/CategoryPage";
import Cart from "./pages/client/Cart";
import Checkout from "./pages/client/Checkout";
import { useSelector } from "react-redux";


function App() {
  const user = useSelector(state => state.user);
  return (
      <Routes>
        {/* Auth */}

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        
        <Route element={<ClientLayout />}>
          
          <Route path="/" element={<Home />} />
        </Route>
      
        {/* <Route element={<ClientLayout />}>
          
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/category/:id" element={<CategoryPage />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />
        </Route>

        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<Dashboard />} />
          <Route path="products" element={<ProductList />} />
          <Route path="products/new" element={<ProductForm />} />
          <Route path="products/:id/edit" element={<ProductForm />} />

          <Route path="categories" element={<CategoryList />} />
          <Route path="categories/new" element={<CategoryForm />} />
          <Route path="categories/:id/edit" element={<CategoryForm />} />

          <Route path="users" element={<UserList />} />
          <Route path="users/new" element={<UserForm />} />
          <Route path="users/:id/edit" element={<UserForm />} />

          <Route path="orders" element={<OrderList />} />
        </Route> */}
      </Routes>

  );
}

export default App;
