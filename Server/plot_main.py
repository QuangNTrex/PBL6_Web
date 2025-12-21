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
import paho.mqtt.client as mqtt

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
def image_loop(stop_event, detected_frame_buffer, detected_labels_history, frame_lock, labels_lock):
    """Nhận ảnh JPEG và dữ liệu detect từ Raspberry Pi qua ImageZMQ."""
    import imagezmq
    import json
    import time
    import threading
    import queue
    import cv2
    import numpy as np

    # Queue trung gian để tách biệt luồng nhận (IO) và luồng xử lý (CPU/Shared Memory)
    # Maxsize nhỏ để drop frame cũ nếu xử lý không kịp, đảm bảo realtime
    process_queue = queue.Queue(maxsize=3)

    def process_worker():
        while not stop_event.is_set():
            try:
                # Lấy dữ liệu từ queue với timeout để kiểm tra stop_event
                json_msg, frame = process_queue.get(timeout=0.1)

                if frame is None:
                    continue

                # Parse JSON message to get detections and counter
                detections = []
                counter = {}
                timestamp = time.time()
                try:
                    msg = json.loads(json_msg)
                    detections = msg.get("detections", [])
                    counter = msg.get("counter", {})
                    timestamp = msg.get("time", time.time())
                except json.JSONDecodeError:
                    pass

                # Draw detections on frame
                for det in detections:
                    box = det.get("box")
                    label = det.get("label")
                    conf = det.get("conf")
                    if box:
                        x1, y1, x2, y2 = map(int, box)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label_text = f"{label} {conf:.2f}" if conf else label
                        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

                # Resize ảnh về 640x640
                frame = cv2.resize(frame, (640, 640))
                _, encoded_img = cv2.imencode('.jpg', frame)
                jpg_buffer = encoded_img.tobytes()

                # 1. Cập nhật ảnh vào buffer
                with frame_lock:
                    detected_frame_buffer.value = jpg_buffer
                
                # 2. Cập nhật thông tin nhãn (labels)
                try:
                    # Chuyển đổi format dict {label: qty} -> list [{label, quantity, time}]
                    current_labels = []
                    for label, qty in counter.items():
                        current_labels.append({
                            "label": label,
                            "quantity": qty,
                            "time": timestamp
                        })
                    
                    with labels_lock:
                        detected_labels_history[:] = current_labels
                        
                except Exception as e:
                    print(f"⚠️ Lỗi xử lý dữ liệu JSON từ Pi: {e}")
            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ Lỗi trong process_worker: {e}")

    # Khởi chạy thread xử lý nền
    worker_thread = threading.Thread(target=process_worker, daemon=True)
    worker_thread.start()

    image_hub = imagezmq.ImageHub(open_port='tcp://*:5555')
    print("📡 Server đang chờ kết nối từ client ImageZMQ tại cổng 5555...")

    while not stop_event.is_set():
        try:
            # rpi_name chứa JSON string: {"camera_name": "...", "counter": {...}}
            json_msg, frame = image_hub.recv_image()
            image_hub.send_reply(b'OK')

            # Đẩy vào queue để xử lý bất đồng bộ, tránh block client
            if not process_queue.full():
                process_queue.put((json_msg, frame))

        except Exception as e:
            print(f"⚠️ Lỗi trong ImageZMQ worker: {e}")
            break

    print("✨ ImageZMQ worker kết thúc.")


# ============================================================
# 🧩 4. MAIN PROCESS (FastAPI + Workers)
# ============================================================
try:
    multiprocessing.set_start_method("spawn", force=True)
except RuntimeError:
    pass

# ============================================================
# 🧩 5. MQTT CLIENT SETUP
# ============================================================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected successfully to broker.")
    else:
        print(f"[MQTT] Failed to connect, return code {rc}")

mqtt_client.on_connect = on_connect

if __name__ == "__main__":
    # 4.1. Tạo shared memory và Lock
    manager = Manager()
    detected_frame_buffer = manager.Value(c_char_p, b"")    # ảnh đã detect
    detected_labels_history = manager.list()
    frame_lock_detect = Lock()
    detected_labels_lock = Lock()
    stop_event = multiprocessing.Event()

    # 4.2. Khởi tạo process con
    receiver_process = multiprocessing.Process(
        target=image_loop,
        args=(stop_event, detected_frame_buffer, detected_labels_history, frame_lock_detect, detected_labels_lock)
    )

    receiver_process.start()

    # 4.2.5 Start MQTT
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        mqtt_client.loop_start()
    except Exception as e:
        print(f"[ERROR] Could not start MQTT client: {e}")

    # 4.3. FastAPI App
    app = FastAPI()
    app.state.detected_frame_buffer = detected_frame_buffer
    app.state.frame_lock_detect = frame_lock_detect
    app.state.detected_labels_history = detected_labels_history
    app.state.detected_labels_lock = detected_labels_lock
    app.state.mqtt_client = mqtt_client

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
        receiver_process.join(timeout=3)

        for proc in [receiver_process]:
            if proc.is_alive():
                print(f"⚠️ {proc.name} chưa dừng, buộc terminate.")
                proc.terminate()
                proc.join()

        print("✅ Tất cả tiến trình đã kết thúc.")
