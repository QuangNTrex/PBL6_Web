import cv2
import time
import imagezmq
import numpy as np
import zmq

# --- CẤU HÌNH ---
SERVER_IP = '127.0.0.1' 
SERVER_PORT = 5555
SERVER_URL = f"tcp://{SERVER_IP}:{SERVER_PORT}"
SENDER_NAME = 'Client_PC'

# --- HÀM TẠO KẾT NỐI ---
def create_sender():
    """Tạo kết nối mới tới server, thử liên tục cho tới khi thành công."""
    while True:
        try:
            sender = imagezmq.ImageSender(connect_to=SERVER_URL)
            print(f"✅ Kết nối thành công tới server: {SERVER_URL}")
            return sender
        except zmq.error.ZMQError as e:
            print(f"⚠️ Lỗi khi kết nối tới server: {e}. Thử lại sau 5 giây...")
            time.sleep(5)

# --- HÀM STREAM ẢNH ---
def stream_images():
    """Vòng lặp đọc và gửi ảnh, tự động kết nối lại khi mất liên lạc."""
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("❌ Lỗi: Không thể truy cập camera.")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(2.0)

    sender = create_sender()
    print("🚀 Bắt đầu gửi luồng ảnh...")

    while True:
        ret, frame = camera.read()
        if not ret:
            print("⚠️ Lỗi: Không thể đọc frame từ camera.")
            time.sleep(1)
            continue

        # Nén ảnh JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        ret, jpg_buffer = cv2.imencode('.jpg', frame, encode_param)
        jpg_bytes = jpg_buffer.tobytes()

        try:
            # Gửi ảnh đến server
            reply = sender.send_jpg(SENDER_NAME, jpg_bytes)
            # print(f"Server phản hồi: {reply.decode('utf-8')}")

        except (zmq.error.ZMQError, zmq.error.Again, BrokenPipeError, TimeoutError) as e:
            print(f"⚠️ Mất kết nối tới server ({e}). Đang thử kết nối lại...")
            try:
                sender.close()
            except Exception:
                pass
            sender = create_sender()  # Kết nối lại và tiếp tục stream
            continue

        # Hiển thị ảnh để debug
        cv2.imshow('Image Client', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Dừng client theo yêu cầu người dùng.")
            break

    # --- DỌN DẸP ---
    camera.release()
    cv2.destroyAllWindows()
    try:
        sender.close()
    except Exception:
        pass
    print("✅ Client đã đóng kết nối.")

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    while True:
        try:
            stream_images()
            break  # Chạy xong thì thoát
        except Exception as e:
            print(f"⚠️ Lỗi bất ngờ trong quá trình stream: {e}")
            print("🔁 Tự động khởi động lại sau 5 giây...")
            time.sleep(5)
