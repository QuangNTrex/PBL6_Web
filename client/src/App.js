import React, { Suspense, lazy } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { useSelector } from "react-redux";
import StaffLayout from "./layouts/StaffLayout";
import ProductStaffManagePage from "./pages/staff/Product/ProductStaffManagePage";

// Layouts
const AdminLayout = lazy(() => import("./layouts/AdminLayout"));
const ClientLayout = lazy(() => import("./layouts/ClientLayout"));

// Auth Pages
const Login = lazy(() => import("./pages/auth/Login"));
const Register = lazy(() => import("./pages/auth/Register"));

// Admin Pages
const CategoryManagePage = lazy(() => import("./pages/admin/Category/CategoryManagePage"));
const ProductManagePage = lazy(() => import("./pages/admin/Product/ProductManagePage"));
const UserManagePage = lazy(() => import("./pages/admin/User/UserManagePage"));
const OrderManagementPage = lazy(() => import("./pages/admin/Order/OrderManagementPage"));
const DashboardPage = lazy(() => import("./pages/admin/DashboardPage"));
const ScanProductPage = lazy(() => import("./pages/admin/ScanProduct/ScanProductPage"));

// Client Pages
const Home = lazy(() => import("./pages/client/Home"));
const Profile = lazy(() => import("./pages/client/Profile"));
const SearchPage = lazy(() => import("./pages/client/SearchPage"));
const CartPage = lazy(() => import("./pages/client/CartPage"));
const ProductDetailPage = lazy(() => import("./pages/client/ProductDetailPage"));
const CheckoutPage = lazy(() => import("./pages/client/CheckoutPage"));
const OrderPage = lazy(() => import("./pages/client/OrderPage"));
const OrderDetailPage = lazy(() => import("./pages/client/OrderDetailPage"));
const CategoryProductsPage = lazy(() => import("./pages/client/CategoryProductPage"));



// --------- Protected Routes ----------
const PrivateRoute = ({ children, user }) => {
  return user?.username ? children : <Navigate to="/login" replace />;
};

const AdminRoute = ({ children, user }) => {
  return user?.role === "admin" ? children : <Navigate to="/" replace />;
};

const StaffRoute = ({ children, user }) => {
  return user?.role === "staff" ? children : user?.role === "admin" ? children : <Navigate to="/" replace />;
};

function App() {
  const user = useSelector((state) => state.user);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Routes>
        {/* Auth */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Client */}
        <Route element={<ClientLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/categories/:categoryId" element={<CategoryProductsPage />} />

          <Route path="/profile" element={<PrivateRoute user={user}><Profile /></PrivateRoute>} />
          <Route path="/checkout" element={<PrivateRoute user={user}><CheckoutPage /></PrivateRoute>} />
          <Route path="/orders" element={<PrivateRoute user={user}><OrderPage /></PrivateRoute>} />
          <Route path="/orders/:id" element={<PrivateRoute user={user}><OrderDetailPage /></PrivateRoute>} />
        </Route>

        {/* Admin */}
        <Route
          path="/admin"
          element={
            <AdminRoute user={user}>
              <AdminLayout />
            </AdminRoute>
          }
        >
          <Route index element={<DashboardPage />} />
          <Route path="categories" element={<CategoryManagePage />} />
          <Route path="products" element={<ProductManagePage />} />
          <Route path="users" element={<UserManagePage />} />
          <Route path="orders" element={<OrderManagementPage />} />
          <Route path="scan-product" element={<ScanProductPage />} />
        </Route>
        {/* staff */}
        <Route
          path="/staff"
          element={
            <StaffRoute user={user}>
              <StaffLayout />
            </StaffRoute>
          }
        >
          <Route path="scan-product" element={<ScanProductPage />} />
          <Route path="products" element={<ProductStaffManagePage />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}

export default App;
