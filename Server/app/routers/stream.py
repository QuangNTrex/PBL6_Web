from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import threading
import time
import cv2
import numpy as np

router = APIRouter(prefix="/stream", tags=["Stream"])

lock = threading.Lock()
latest_frame: np.ndarray | None = None

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    Nhận frame từ client (upload qua HTTP).
    """
    global latest_frame
    img_bytes = await file.read()
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is not None:
        with lock:
            latest_frame = frame
    return {"status": "OK"}


def generate_fps(fps: int = 25, quality: int = 80):
    """
    Generator để stream frame MJPEG.
    - fps: số khung hình/giây.
    - quality: chất lượng JPEG (0-100).
    """
    global latest_frame
    delay = 1.0 / fps

    while True:
        frame_copy = None
        with lock:
            if latest_frame is not None:
                frame_copy = latest_frame.copy()

        if frame_copy is not None:
            # Encode với chất lượng nén để giảm dung lượng
            success, buffer = cv2.imencode(
                ".jpg", frame_copy, [cv2.IMWRITE_JPEG_QUALITY, quality]
            )
            if success:
                frame_bytes = buffer.tobytes()
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
                )

        time.sleep(delay)


@router.get("/stream")
def stream():
    """
    Stream MJPEG từ latest_frame.
    """
    return StreamingResponse(
        generate_fps(fps=25, quality=80),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )
