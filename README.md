# PBL6 - AI Product Detection & Smart Checkout System

## 1. Giới thiệu

PBL6 là hệ thống ứng dụng Trí tuệ nhân tạo (AI) và Computer Vision để nhận diện sản phẩm thông qua camera và hỗ trợ thanh toán tự động tại cửa hàng tạp hóa.

Hệ thống được xây dựng với mục tiêu:

- Tự động phát hiện sản phẩm qua camera
- Hiển thị sản phẩm lên giao diện web
- Hỗ trợ thanh toán nhanh
- Mô phỏng mô hình cửa hàng tự thanh toán (self-checkout)

---

## 2. Kiến trúc hệ thống

Hệ thống gồm 3 thành phần chính:

1. Frontend (ReactJS)
2. Backend (Python FastAPI)
3. Camera Client (Raspberry Pi 2W)

### Luồng hoạt động

1. Camera trên Raspberry Pi chụp ảnh sản phẩm.
2. Ảnh được gửi đến server FastAPI.
3. Server thực hiện AI inference để nhận diện sản phẩm.
4. Kết quả trả về frontend ReactJS.
5. Người dùng xác nhận và tiến hành thanh toán.

---

## 3. Công nghệ sử dụng

### Frontend
- ReactJS
- JavaScript
- HTML, CSS

### Backend
- Python
- FastAPI
- Uvicorn

### AI
- Object Detection (YOLO / PyTorch / TensorFlow)

### Phần cứng
- Raspberry Pi 2W
- Camera module

### Giao tiếp
- REST API

---

## 4. Cấu trúc thư mục
PBL6_Web/
│
├── client/ # Ứng dụng ReactJS
├── server/ # Backend FastAPI
├── client_camera_pi.py # Script gửi ảnh từ Raspberry Pi
├── client_rasp.py # Script xử lý camera
├── database.py # Xử lý cơ sở dữ liệu
├── google_sheet.py # Tích hợp Google Sheet (nếu có)
├── products.json # Dữ liệu sản phẩm
└── README.md

---

## 5. Hướng dẫn cài đặt và chạy

### 5.1 Clone repository

git clone https://github.com/QuangNTrex/PBL6_Web.git
cd PBL6_Web
### 5.2 Chạy Frontend
cd client
npm install
npm start

Truy cập:
http://localhost:3000

### 5.3 Chạy Backend
cd server
python -m venv venv

Kích hoạt môi trường ảo:

Windows:

venv\Scripts\activate

Linux / macOS:

source venv/bin/activate

Cài đặt thư viện:

pip install -r requirements.txt

Chạy server:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

API Docs:
http://localhost:8000/docs

### 5.4 Chạy Raspberry Pi Client

Trên Raspberry Pi:

Cài đặt Python và các thư viện cần thiết (opencv-python, requests, v.v.).

Cấu hình địa chỉ IP của server trong file client.

Chạy:

python client_camera_pi.py

Thiết bị sẽ:

Chụp ảnh từ camera

Gửi ảnh đến server

Nhận kết quả nhận diện

## 6. Chức năng chính

Nhận diện sản phẩm bằng AI

Hiển thị danh sách sản phẩm

Tính tổng tiền

Xác nhận thanh toán

Có thể mở rộng lưu lịch sử giao dịch

## 7. Hướng phát triển

Tối ưu mô hình AI để chạy trực tiếp trên Raspberry Pi

Tích hợp thanh toán điện tử

Triển khai bằng Docker

Phát triển thành hệ thống self-checkout hoàn chỉnh

## 8. Repository

https://github.com/QuangNTrex/PBL6_Web

## 9. Thông tin dự án

Dự án được thực hiện trong khuôn khổ học phần PBL6 với mục tiêu nghiên cứu và ứng dụng AI trong lĩnh vực bán lẻ thông minh.

Nguồn dữ liệu: https://universe.roboflow.com/lac-nguyen/vietnamese-productions-classification/dataset/21




