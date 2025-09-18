import { createSlice } from "@reduxjs/toolkit";

const loadFromLocalStorage = () => {
  try {
    const data = localStorage.getItem("cart");
    return data ? JSON.parse(data) : { items: [] };
  } catch (e) {
    console.error("❌ Lỗi load cart từ localStorage:", e);
    return { items: [] };
  }
};

const saveToLocalStorage = (state) => {
  try {
    localStorage.setItem("cart", JSON.stringify(state));
  } catch (e) {
    console.error("❌ Lỗi lưu cart vào localStorage:", e);
  }
};

const initialState = loadFromLocalStorage();

const cartSlice = createSlice({
  name: "cart",
  initialState,
  reducers: {
    // 🟢 Thêm sản phẩm (payload: { product, quantity })
    addToCart: (state, action) => {
      const { product, quantity } = action.payload;
      const existingItem = state.items.find((item) => item.id === product.id);

      if (existingItem) {
        existingItem.quantity += quantity;
      } else {
        state.items.push({ ...product, quantity });
      }
      saveToLocalStorage(state);
    },

    // 🟢 Xóa sản phẩm khỏi giỏ
    removeFromCart: (state, action) => {
      const productId = action.payload;
      state.items = state.items.filter((item) => item.id !== productId);
      saveToLocalStorage(state);
    },
    // 🟢 Xóa nhieu sản phẩm khỏi giỏ
    removeMoreFromCart: (state, action) => {
      const productIds = action.payload;
      state.items = state.items.filter((item) => !productIds.includes(item.id));
      saveToLocalStorage(state);
    },

    // 🟢 Tăng số lượng
    increaseQuantity: (state, action) => {
      const productId = action.payload;
      const item = state.items.find((item) => item.id === productId);
      if (item) {
        item.quantity += 1;
      }
      saveToLocalStorage(state);
    },

    // 🟢 Giảm số lượng
    decreaseQuantity: (state, action) => {
      const productId = action.payload;
      const item = state.items.find((item) => item.id === productId);
      if (item && item.quantity > 1) {
        item.quantity -= 1;
      }
      saveToLocalStorage(state);
    },

    // 🟢 Xóa toàn bộ giỏ
    clearCart: (state) => {
      state.items = [];
      saveToLocalStorage(state);
    },
    
  },
});

// 🟢 Selector: Tính tổng tiền
export const getTotalAmount = (state) =>
  state.cart.items.reduce((total, item) => total + item.price * item.quantity, 0);

// 🟢 Selector: Đếm tổng số lượng sản phẩm
export const getTotalQuantity = (state) =>
  state.cart.items.reduce((count, item) => count + item.quantity, 0);


export const {
  addToCart,
  removeFromCart,
  removeMoreFromCart,
  increaseQuantity,
  decreaseQuantity,
  clearCart,
} = cartSlice.actions;

export default cartSlice.reducer;
