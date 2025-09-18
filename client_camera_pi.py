import cv2
import requests
import time

SERVER_URL = "http://localhost:8000/stream/upload"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Giảm kích thước ảnh xuống 640x480 (tuỳ bạn điều chỉnh)
    frame_resized = cv2.resize(frame, (640, 480))

    # Encode ảnh sau khi resize
    _, img_encoded = cv2.imencode('.jpg', frame_resized, [cv2.IMWRITE_JPEG_QUALITY, 80])  
    # JPEG quality = 80 để giảm dung lượng mà vẫn rõ

    files = {'file': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')}
    
    try:
        requests.post(SERVER_URL, files=files, timeout=1)
    except Exception as e:
        print("Error:", e)
    
    time.sleep(1.0/25)  # ~25 fps
