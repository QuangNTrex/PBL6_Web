// src/redux/userSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  username: "",
  email: 'abc@gmail.com',
  full_name: "",
  phone: "",
  address: "",
  avatar_url: "",
  role: "",
  status: "",
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser(state, action) {
      state.full_name = action.payload.full_name;
      state.username = action.payload.username;
      state.email = action.payload.email;
      state.avatar_url = action.payload.avatar_url;
      state.address = action.payload.address;
      state.phone = action.payload.phone;
      state.email = action.payload.email;
      state.role = action.payload.role;

    },
    clearUser(state) {
      state.username = '';
      state.email = '';
      state.avatarUrl = '';
      state.role = ''
    }
  }
});

export const { setUser, pushUser, clearUser } = userSlice.actions;
export default userSlice.reducer;
