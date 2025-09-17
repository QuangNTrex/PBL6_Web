import React from "react";

function ScanProductPage() {
  return (
    <div className="p-6 flex flex-col items-center">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Quét sản phẩm thanh toán tự động
      </h2>

      <div className="bg-white shadow-xl rounded-2xl p-4 w-full max-w-4xl">
        <div className="flex justify-center">
          <img
            src="http://localhost:8000/stream/stream"
            alt="Video Stream"
            className="rounded-xl border-4 border-gray-300 max-h-[70vh] shadow-md"
          />
        </div>
      </div>
    </div>
  );
}

export default ScanProductPage;
