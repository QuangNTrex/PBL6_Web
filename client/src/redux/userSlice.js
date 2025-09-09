// src/redux/userSlice.js
import { createSlice } from "@reduxjs/toolkit";

// Lấy user từ localStorage nếu có
const storedUser = localStorage.getItem("user");
const initialState = storedUser
  ? JSON.parse(storedUser)
  : {
      username: "",
      email: "",
      full_name: "",
      phone: "",
      address: "",
      avatar_url: "",
      role: "",
      status: "",
      gender : "",
      birth_date : "",
    };

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUser(state, action) {
      const newUser = {
        ...state,
        ...action.payload,
      };
      // Lưu xuống localStorage
      localStorage.setItem("user", JSON.stringify(newUser));

      return newUser; // Redux Toolkit cho phép return object mới
    },
    clearUser() {
      // Xóa user trong localStorage
      localStorage.removeItem("user");

      return {
        username: "",
        email: "",
        full_name: "",
        phone: "",
        address: "",
        avatar_url: "",
        role: "",
        status: "",
        gender : "",
        birth_date : "",
      };
    },
  },
});

export const { setUser, clearUser } = userSlice.actions;
export default userSlice.reducer;
