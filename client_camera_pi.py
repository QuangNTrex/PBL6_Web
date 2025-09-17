import cv2
import requests
import time

SERVER_URL = "http://localhost:8000/stream/upload"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')}
    
    try:
        requests.post(SERVER_URL, files=files, timeout=1)
    except Exception as e:
        print("Error:", e)
    
    time.sleep(1.0/30)  # gửi ~10 fps
