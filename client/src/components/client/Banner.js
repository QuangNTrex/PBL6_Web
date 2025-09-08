// src/components/client/Banner.js
import React, { useState, useEffect } from "react";
import "./Banner.css";

const images = [
  "/assets/banner1.png",
  "/assets/banner2.png",
  "/assets/banner3.png",
];

export default function Banner() {
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % images.length);
    }, 3000); // đổi ảnh sau 3 giây
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="banner-container">
      {images.map((img, index) => (
        <div
          key={index}
          className={`banner-slide ${index === current ? "active" : ""}`}
          style={{ backgroundImage: `url(${img})` }}
        />
      ))}
      <div className="banner-dots">
        {images.map((_, index) => (
          <span
            key={index}
            className={index === current ? "dot active" : "dot"}
            onClick={() => setCurrent(index)}
          />
        ))}
      </div>
    </div>
  );
}
