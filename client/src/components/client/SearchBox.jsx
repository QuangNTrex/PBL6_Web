import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const SearchBox = () => {
  const [keyword, setKeyword] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (keyword.trim()) {
      navigate(`/search?query=${encodeURIComponent(keyword)}`);
    }
  };

  return (
    <form onSubmit={handleSearch} style={{ display: "flex", gap: "10px" }}>
      <input
        type="text"
        placeholder="Tìm sản phẩm..."
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        style={{ flex: 1, padding: "8px" }}
      />
      <button type="submit">Tìm</button>
    </form>
  );
};

export default SearchBox;
