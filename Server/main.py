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
from app.routers import users, categories, order_details, products, orders, auth, statistics, cart, stream
from collections import Counter
import asyncio
import json

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

async def event_generator(detected_labels_history, frame_lock_labels):
    last_data = None
    while True:
        await asyncio.sleep(0.04)  # 25 lần/giây ≈ 40ms
        with frame_lock_labels:
            data = list(detected_labels_history)

        if data != last_data or True:  # chỉ gửi khi có thay đổi
            last_data = data
            yield f"data: {json.dumps(data)}\n\n"


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
def yolo_detect_loop(stop_event, raw_frame_buffer, detected_frame_buffer, detected_labels_history,
                     frame_lock_raw, frame_lock_detect, detected_labels_lock):
    """Process phát hiện sản phẩm từ ảnh nhận được (YOLOv8)."""
    import cv2
    import numpy as np
    import time
    from ultralytics import YOLO
    from collections import Counter
    import torch

    print("🧠 Đang tải mô hình YOLO...")
    model = YOLO("model/no_mosaic_sgd_0284.pt")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    print(f"✅ Mô hình YOLO đã sẵn sàng trên {device.upper()}.")

    prev_time = time.time()
    last_detect_time = 0

    # Cấu hình: resize để tăng tốc
    TARGET_SIZE = (640, 640)
    MIN_INTERVAL = 1 / 30  # tối đa 30fps inference

    while not stop_event.is_set():
        loop_start = time.time()

        # --- Đọc frame an toàn ---
        with frame_lock_raw:
            jpg_buffer = raw_frame_buffer.value

        if not jpg_buffer:
            time.sleep(0.01)
            continue

        # --- Giải mã JPEG thành ảnh ---
        nparr = np.frombuffer(jpg_buffer, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            time.sleep(0.01)
            continue

        # --- Resize để tối ưu tốc độ ---
        frame_resized = cv2.resize(frame, TARGET_SIZE)

        # --- Detect sản phẩm ---
        results = model.predict(frame_resized, conf=0.4,iou=0.45, verbose=False, stream=False)
        result = results[0]

        annotated_frame = result.plot()

        # --- Lấy nhãn & đếm số lượng ---
        boxes = result.boxes
        if boxes is not None and len(boxes) > 0:
            cls_ids = boxes.cls.cpu().numpy().astype(int)
            labels = [model.names[i] for i in cls_ids]
        else:
            labels = []

        with detected_labels_lock:
            label_counts = Counter(labels)
            detected_labels_history[:] = [
                {"label": lbl, "quantity": cnt, "time": time.time()}
                for lbl, cnt in label_counts.items()
            ]

        # --- Tính FPS ---
        now = time.time()
        fps = 1.0 / (now - prev_time) if (now - prev_time) > 0 else 0
        prev_time = now

        cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # --- Mã hóa lại để stream ---
        success, encoded = cv2.imencode('.jpg', annotated_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        if success:
            with frame_lock_detect:
                detected_frame_buffer.value = encoded.tobytes()

        # --- Giữ nhịp ổn định ---
        elapsed = time.time() - loop_start
        if elapsed < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - elapsed)

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
    app.state.detected_labels_history = detected_labels_history
    app.state.detected_labels_lock = detected_labels_lock

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
    app.include_router(stream.router)

    # 4.4. MJPEG endpoint cho ảnh đã detect
    @app.get("/video_feed")
    async def video_feed_endpoint(request: Request):
        buffer = request.app.state.detected_frame_buffer
        lock = request.app.state.frame_lock_detect
        return StreamingResponse(
            generate_mjpeg_stream(buffer, lock),
            media_type="multipart/x-mixed-replace; boundary=frame",
        )
    # --- Endpoint stream dữ liệu ---
    @app.get("/label_feed")
    async def label_feed(request: Request):
        buffer = request.app.state.detected_labels_history
        lock = request.app.state.detected_labels_lock
        return StreamingResponse(event_generator(buffer, lock), media_type="text/event-stream")
    
    @app.get("/product_feed")
    async def label_feed(request: Request):

        buffer = request.app.state.detected_labels_history
        lock = request.app.state.detected_labels_lock
        return StreamingResponse(event_generator(buffer, lock), media_type="text/event-stream")
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
