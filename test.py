import os
import uvicorn
import multiprocessing
import time
from multiprocessing import Manager, Lock
from ctypes import c_char_p

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Import các modules của ứng dụng
from app.database import Base, engine
from app import models
from app.routers import users, categories, order_details, products, orders, auth, statistics, cart
from collections import Counter


# ============================================================
# 🧩 1. MJPEG STREAM GENERATOR
# ============================================================
def generate_mjpeg_stream(shared_frame_buffer, frame_lock):
    mjpeg_header = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
    while True:
        with frame_lock:
            jpg_buffer = shared_frame_buffer.value
        if jpg_buffer:
            yield mjpeg_header
            yield jpg_buffer
            yield b'\r\n'
        time.sleep(0.033)  # ~30 FPS


# ============================================================
# 🧩 2. IMAGEZMQ RECEIVER PROCESS
# ============================================================
def image_loop(stop_event, raw_frame_buffer, frame_lock):
    """Nhận ảnh JPEG từ client và lưu vào buffer chia sẻ."""
    import imagezmq
    import cv2

    image_hub = imagezmq.ImageHub(open_port='tcp://*:5555')
    print("📡 Server đang chờ kết nối từ client ImageZMQ tại cổng 5555...")

    while not stop_event.is_set():
        try:
            rpi_name, jpg_buffer = image_hub.recv_jpg()
            jpg_buffer = bytes(jpg_buffer)  # 🔧 chuyển thành bytes thuần
            with frame_lock:
                raw_frame_buffer.value = jpg_buffer
            image_hub.send_reply(b'OK')
        except Exception as e:
            print(f"⚠️ Lỗi trong ImageZMQ worker: {e}")
            break

    print("✨ ImageZMQ worker kết thúc.")


# ============================================================
# 🧩 3. YOLO DETECTION PROCESS
# ============================================================
def yolo_detect_loop(stop_event, raw_frame_buffer, detected_frame_buffer, detected_labels_history, frame_lock_raw, frame_lock_detect, detected_labels_lock):
    """Process phát hiện sản phẩm từ ảnh nhận được (YOLOv8)."""
    import cv2
    import numpy as np
    import time
    from ultralytics import YOLO

    # Load model YOLO
    print("🧠 Đang tải mô hình YOLO...")
    model = YOLO("model/epoch5.pt")
    model.to("cuda")
    print("✅ Mô hình YOLO đã sẵn sàng.")

    prev_time = time.time()


    while not stop_event.is_set():
        with frame_lock_raw:
            jpg_buffer = raw_frame_buffer.value

        if not jpg_buffer:
            time.sleep(0.02)
            continue

        # Giải mã JPEG thành ảnh OpenCV
        nparr = np.frombuffer(jpg_buffer, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            continue

        # Detect sản phẩm
        results = model(frame, conf=0.75, verbose=False)
        annotated_frame = results[0].plot()

        frame_labels = []

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            frame_labels.append(label)

        # --- 🧮 Gộp nhãn trùng lặp ---
        label_counts = Counter(frame_labels)
        merged_labels = [{"label": lbl, "quantity": cnt, "time": time.time()} for lbl, cnt in label_counts.items()]

        # --- 📝 Lưu vào danh sách lịch sử ---
        with detected_labels_lock:
            detected_labels_history.append(merged_labels)
       
        # Tính FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
        prev_time = current_time
        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Mã hóa lại thành JPEG để stream
        ret, encoded_jpg = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if not ret:
            continue

        jpg_bytes = bytes(encoded_jpg)

        # Lưu kết quả vào buffer chia sẻ
        with frame_lock_detect:
            detected_frame_buffer.value = jpg_bytes

    print("🧠 YOLO detection process kết thúc.")


# ============================================================
# 🧩 4. MAIN PROCESS (FastAPI + Workers)
# ============================================================
try:
    multiprocessing.set_start_method("spawn", force=True)
except RuntimeError:
    pass

if __name__ == "__main__":
    # 4.1. Tạo shared memory và Lock
    manager = Manager()
    raw_frame_buffer = manager.Value(c_char_p, b"")         # ảnh gốc từ client
    detected_frame_buffer = manager.Value(c_char_p, b"")    # ảnh đã detect
    detected_labels_history = manager.list()
    frame_lock_raw = Lock()
    frame_lock_detect = Lock()
    detected_labels_lock = Lock()
    stop_event = multiprocessing.Event()

    # 4.2. Khởi tạo process con
    receiver_process = multiprocessing.Process(
        target=image_loop,
        args=(stop_event, raw_frame_buffer, frame_lock_raw)
    )
    detector_process = multiprocessing.Process(
        target=yolo_detect_loop,
        args=(stop_event, raw_frame_buffer, detected_frame_buffer, detected_labels_history, frame_lock_raw, frame_lock_detect, detected_labels_lock)
    )

    receiver_process.start()
    detector_process.start()

    # 4.3. FastAPI App
    app = FastAPI()
    app.state.detected_frame_buffer = detected_frame_buffer
    app.state.frame_lock_detect = frame_lock_detect

    # CORS
    origins = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # DB & routers
    Base.metadata.create_all(bind=engine)
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(categories.router)
    app.include_router(order_details.router)
    app.include_router(products.router)
    app.include_router(orders.router)
    app.include_router(statistics.router)
    app.include_router(cart.router)

    # 4.4. MJPEG endpoint cho ảnh đã detect
    @app.get("/video_feed")
    async def video_feed_endpoint(request: Request):
        buffer = request.app.state.detected_frame_buffer
        lock = request.app.state.frame_lock_detect
        return StreamingResponse(
            generate_mjpeg_stream(buffer, lock),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )

    # 4.5. Run server
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)

    except KeyboardInterrupt:
        print("\n🛑 Ngắt chương trình.")

    finally:
        print("⚙️ Đang dừng các tiến trình con...")
        stop_event.set()
        receiver_process.join(timeout=5)
        detector_process.join(timeout=5)

        for proc in [receiver_process, detector_process]:
            if proc.is_alive():
                print(f"⚠️ {proc.name} chưa dừng, buộc terminate.")
                proc.terminate()
                proc.join()

        print("✅ Tất cả tiến trình đã kết thúc.")
