import React, { useEffect, useState } from "react";
import "./ScanProductPage.css";
import { useNavigate } from "react-router-dom";

function ScanProductPage() {
  const [labels, setLabels] = useState([]);
  const [segmentLabels, setSegmentLabels] = useState([])
  const [products, setProducts] = useState([])
  const [merge, setMerge] = useState([])
  var productMap = new Map(products.map(p => [p.code, p]));
    const navigate = useNavigate()

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/stream/label_feed");

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLabels(data);
      var ss = ""
      data.map(e => ss += e.label + ", ")
      console.log(ss)
    };

    eventSource.onerror = (err) => {
      console.warn("Mất kết nối /label_feed, đang thử lại...", err);
    };

    return () => eventSource.close();
  }, []);

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/stream/product_feed");

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      const merged = data.total_labels_array.map(item => {
      const product = productMap.get(item.label);
        return {
          ...product,
          ...item,
        };
      });
      setSegmentLabels(merged);
      console.log("-------------")
      console.log(data)
      setMerge(merged)
    };

    eventSource.onerror = (err) => {
      console.warn("Mất kết nối /label_feed, đang thử lại...", err);
    };

    return () => eventSource.close();
  }, []);

  useEffect(() => {
    fetch("http://localhost:8000/products").then(res => res.json()).then(data => {
      productMap = new Map(data.map(p => [p.code, p]));
      setProducts(data)
      console.log("product", data)
    })
  }, [])

  return (
    <div className="scan-page">
      <h2 className="title">Đang quét sản phẩm...</h2>
      <div className="wrap-all">

      <div className="video-card">
              <div className="video-wrapper">
                <img
                  src="http://localhost:8000/stream/video_feed"
                  alt="Video Stream"
                  className="video-stream"
                />
              </div>
            
              
      </div>
       <div>
          <table className="product-table">
            <thead>
              <tr>
                <th>Ảnh</th>
                <th>Mã SP</th>
                <th>Tên SP</th>
                <th>Danh mục</th>
                <th>Giá</th>
                <th>Số lượng</th>
              </tr>
            </thead>
            <tbody>
              {merge.map((p) => (
                <tr key={p.id}>
                  <td>
                    {p.image_path ? (
                      <img src={p.image_path} className="product-image" />
                    ) : (
                      <span className="no-image">Không có ảnh</span>
                    )}
                  </td>
                  <td>{p.code}</td>
                  
                  <td>{p.name}</td>
                  <td>{p.category ? p.category.name : null}</td>
                  <td>{p.price}</td>
                  <td>{p.quantity}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      <div className="button-group" onClick={() => {
        navigate("/staff/checkout", {state: {selectedItems: merge}})
      }}>
                <button className="btn btn-primary">Tiếp theo</button>
              </div>
    </div>
    
  );
}

export default ScanProductPage;
