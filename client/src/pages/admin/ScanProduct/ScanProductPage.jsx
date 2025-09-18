import React from "react";
import "./ScanProductPage.css";

function ScanProductPage() {
  return (
    <div className="scan-page">
      <h2 className="title">Đang quét sản phẩm...</h2>

      <div className="video-card">
        <div className="video-wrapper">
          <img
            src="http://localhost:8000/stream/stream"
            alt="Video Stream"
            className="video-stream"
          />
        </div>

        <div className="button-group">
          <button className="btn btn-primary">Chụp</button>
        </div>
      </div>
    </div>
  );
}

export default ScanProductPage;
