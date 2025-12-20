import time
from multiprocessing import Manager, Lock
from ctypes import c_char_p
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.crud import products as crud_products
from app import models
from app.database import get_db


# Import các modules của ứng dụng
from collections import Counter
import asyncio
import json


class ScanState:
    IDLE = 0
    SCANNING = 1

EMPTY_TIMEOUT = 2  # Thời gian chờ để xác nhận kết thúc đợt quét

router = APIRouter(prefix="/stream", tags=["Stream"])
def detect_segments(frames_labels, min_detect=60, min_silence=15):
    """
    frames_labels: list of frame label lists, ví dụ [[{label:..}], [], [], ...]
    min_detect: số frame tối thiểu để xem là 1 khoảng detect
    min_silence: số frame tối thiểu để xem là 1 khoảng lặng
    """
    if not frames_labels:
        return []

    segments = []
    current_type = "detect" if len(frames_labels[0]) > 0 else "silence"
    start_idx = 0

    # --- 1️⃣ Tạo danh sách các khoảng thô ---
    for i in range(1, len(frames_labels)):
        this_type = "detect" if len(frames_labels[i]) > 0 else "silence"
        if this_type != current_type:
            segments.append({
                "type": current_type,
                "start": start_idx,
                "end": i - 1,
                "frames": frames_labels[start_idx:i]
            })
            start_idx = i
            current_type = this_type

    # Thêm khoảng cuối cùng
    segments.append({
        "type": current_type,
        "start": start_idx,
        "end": len(frames_labels) - 1,
        "frames": frames_labels[start_idx:]
    })

    # --- 2️⃣ Gộp các khoảng nhỏ hơn ngưỡng ---
    merged = []
    for seg in segments:
        seg_len = seg["end"] - seg["start"] + 1
        too_short = (
            (seg["type"] == "detect" and seg_len < min_detect) or
            (seg["type"] == "silence" and seg_len < min_silence)
        )

        if too_short and merged:
            # Gộp vào khoảng trước
            merged[-1]["end"] = seg["end"]
            merged[-1]["frames"].extend(seg["frames"])
        else:
            merged.append(seg)

    # --- 3️⃣ Gộp các khoảng cùng loại liền nhau ---
    final_segments = []
    for seg in merged:
        if final_segments and seg["type"] == final_segments[-1]["type"]:
            final_segments[-1]["end"] = seg["end"]
            final_segments[-1]["frames"].extend(seg["frames"])
        else:
            final_segments.append(seg)

    return final_segments

from collections import Counter



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

@router.get("/video_feed")
async def video_feed_endpoint(request: Request):
    buffer = request.app.state.detected_frame_buffer
    lock = request.app.state.frame_lock_detect
    return StreamingResponse(
        generate_mjpeg_stream(buffer, lock),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
# --- Endpoint stream dữ liệu ---
@router.get("/label_feed")
async def label_feed(request: Request):
    buffer = request.app.state.detected_labels_history
    lock = request.app.state.detected_labels_lock
    return StreamingResponse(event_generator(buffer, lock), media_type="text/event-stream")

@router.get("/product_feed")
async def label_feed(request: Request, db: Session = Depends(get_db)):
    buffer = request.app.state.detected_labels_history
    lock = request.app.state.detected_labels_lock
    mqtt_client = request.app.state.mqtt_client

    # Gửi lệnh SCAN khi client kết nối
    try:
        mqtt_client.publish("cmd/raspi_cam", "SCAN")
        print("[MQTT] Sent SCAN to cmd/raspi_cam")
    except Exception as e:
        print(f"[ERROR] MQTT Publish failed: {e}")

    async def merge_label_generate(buffer, lock):
        # --- FSM State Initialization ---
        state = ScanState.IDLE
        last_seen_time = 0
        batch_frame_counters = []
        session_total = Counter()   # Tổng các đợt đã quét xong
        current_scanning = {}       # Đợt đang quét hiện tại

        try:
            while True:
                await asyncio.sleep(0.04)
                
                # 1. Lấy dữ liệu từ shared memory và chuyển về dạng Counter
                frame_counter = Counter()
                now = time.time()
                
                with lock:
                    data_list = list(buffer)
                
                if data_list:
                    # Lấy timestamp từ frame đầu tiên nếu có
                    now = data_list[0].get("time", now)
                    for item in data_list:
                        lbl = item.get("label")
                        qty = item.get("quantity", 0)
                        if lbl:
                            frame_counter[lbl] += qty

                # 2. FSM Logic (Thuật toán quét)
                if state == ScanState.IDLE:
                    if frame_counter:
                        state = ScanState.SCANNING
                        batch_frame_counters = [frame_counter]
                        last_seen_time = now
                        # print("\n[SCAN] START")

                elif state == ScanState.SCANNING:
                    if frame_counter:
                        batch_frame_counters.append(frame_counter)
                        last_seen_time = now
                    
                    # Cập nhật mục "đang quét" (current_scanning) bằng cách vote
                    if batch_frame_counters:
                        votes = Counter(tuple(sorted(c.items())) for c in batch_frame_counters)
                        if votes:
                            best, _ = votes.most_common(1)[0]
                            current_scanning = dict(best)

                    # Kiểm tra điều kiện kết thúc đợt quét (timeout)
                    if not frame_counter:
                        if now - last_seen_time > EMPTY_TIMEOUT:
                            if current_scanning:
                                # Chỉ chấp nhận nếu có đủ số lượng frame (tránh nhiễu)
                                if len(batch_frame_counters) >= 5:
                                    # print("[SCAN] END ->", current_scanning)
                                    session_total.update(current_scanning)

                                    # Gửi MQTT thông tin sản phẩm vừa quét xong để hiển thị LCD
                                    for label, quantity in current_scanning.items():
                                        try:
                                            product_db = crud_products.get_product_by_code(db=db, code=label)
                                            if product_db:
                                                payload = {
                                                    "label": product_db.code,
                                                    "price": product_db.price,
                                                    "quantity": quantity
                                                }
                                                mqtt_client.publish("pbl6/products", json.dumps(payload))
                                                print(f"[MQTT] Published Product to pbl6/products: {payload}")
                                        except Exception as e:
                                            print(f"[ERROR] MQTT Publish failed: {e}")
                                # else: print(f"[SCAN] IGNORED (Too few frames: {len(batch_frame_counters)})")
                                
                                current_scanning.clear()

                            state = ScanState.IDLE
                            batch_frame_counters.clear()

                # 3. Chuẩn bị dữ liệu trả về client
                # Tổng hợp = Đã quét xong (session_total) + Đang quét (current_scanning)
                display_counter = session_total + Counter(current_scanning)
                
                total_labels_array = [
                    {"label": lbl, "quantity": qty} 
                    for lbl, qty in display_counter.items()
                ]

                yield f"data: {json.dumps(total_labels_array)}\n\n"
        finally:
            # Gửi lệnh STOP khi client ngắt kết nối
            try:
                mqtt_client.publish("cmd/raspi_cam", "STOP")
                print("[MQTT] Sent STOP to cmd/raspi_cam")
            except Exception as e:
                print(f"[ERROR] MQTT Publish failed: {e}")

    return StreamingResponse(merge_label_generate(buffer, lock), media_type="text/event-stream")

@router.post("/scan_complete")
async def scan_complete(request: Request, products: list, db: Session = Depends(get_db)):
    """
    Gửi MQTT thông báo hoàn thành quét sản phẩm về client (Raspberry Pi)
    """
    try:
        request.app.state.mqtt_client.publish("cmd/raspi_cam", "STOP")
        print(f"[MQTT] Sent STOP to cmd/raspi_cam")
        return {"status": "success", "message": "Scan complete notification sent"}
    except Exception as e:
        print(f"[ERROR] Failed to send scan complete MQTT: {e}")
        raise HTTPException(status_code=500, detail="Failed to send notification")