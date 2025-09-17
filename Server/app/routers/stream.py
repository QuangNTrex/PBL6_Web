from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import threading
import time
import cv2
import numpy as np

lock = threading.Lock()
latest_frame = None

router = APIRouter(prefix="/stream", tags=["Stream"])

@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    global latest_frame
    img_bytes = await file.read()
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    with lock:
        latest_frame = frame
    return {"status": "OK"}


def generate():
    global latest_frame
    while True:
        if latest_frame is not None:
            with lock:
                _, buffer = cv2.imencode('.jpg', latest_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(1.0/30)  # khoảng 20 fps


@router.get('/stream')
def stream():
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')
