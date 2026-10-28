# Thực hành IoT buổi 3 – Lập trình Python với CoAP

## 1. Giới thiệu
Bộ bài thực hành mô phỏng 3 bài theo đề CoAP:
- **Bài 1:** CoAP Server/Client dùng GET và POST.
- **Bài 2:** Server cảm biến nhiệt độ/độ ẩm và Client giám sát định kỳ.
- **Bài 3:** Đèn thông minh dùng GET/PUT và CoAP Observe.

## 2. Môi trường
- Python 3.10+ khuyến nghị.
- Thư viện `aiocoap`.
- Chạy server và client trên cùng máy bằng `localhost`/`127.0.0.1`, UDP cổng 5683.
- Không cần MQTT Broker.

Cài thư viện:
```bash
python -m pip install -r requirements.txt
```
Nếu lệnh trên không chạy được:
```bash
python -m pip install aiocoap
```

## 3. Cấu trúc thư mục
```text
CoAP_Lab/
├── bai1/
│   ├── coap_server_bai1.py
│   └── coap_client_bai1.py
├── bai2/
│   ├── sensor_server_bai2.py
│   └── monitor_client_bai2.py
├── bai3/
│   ├── light_server_bai3.py
│   ├── light_controller_bai3.py
│   └── light_monitor_bai3.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 4. Cách chạy

Mở các terminal riêng trong thư mục gốc `CoAP_Lab`. Luôn chạy server trước client.

### Bài 1 – GET/POST
Terminal 1:
```bash
python bai1/coap_server_bai1.py
```
Terminal 2:
```bash
python bai1/coap_client_bai1.py
```
Sửa họ tên và mã sinh viên trong file `bai1/coap_client_bai1.py` trước khi chạy.

### Bài 2 – Giám sát cảm biến
Terminal 1:
```bash
python bai2/sensor_server_bai2.py
```
Terminal 2:
```bash
python bai2/monitor_client_bai2.py
```
Client gửi GET mỗi 3 giây và hiển thị dữ liệu/cảnh báo. Nhấn `Ctrl+C` để dừng.

### Bài 3 – Điều khiển đèn và Observe
Terminal 1:
```bash
python bai3/light_server_bai3.py
```
Terminal 2 – bật/tắt hoặc xem trạng thái:
```bash
python bai3/light_controller_bai3.py
```
Terminal 3 – theo dõi tự động:
```bash
python bai3/light_monitor_bai3.py
```
Nhập `ON`, `OFF`, `STATUS` hoặc `EXIT` ở Terminal 2. Terminal 3 nhận thông báo tự động qua **CoAP Observe**, không polling GET. Nhấn `Ctrl+C` để dừng Monitoring Client.

## 5. URI và giao thức
| Bài | URI | Phương thức |
|---|---|---|
| 1 | `coap://localhost/iot/lab/message` | GET, POST |
| 2 | `coap://localhost/iot/lab/sensor01/data` | GET |
| 3 | `coap://localhost/iot/lab/light01/status` | GET, PUT, Observe |

Các server mặc định dùng UDP cổng 5683. Nếu chạy trên máy khác, thay `localhost` trong client bằng địa chỉ IP của máy chạy server và cho phép UDP/5683 qua tường lửa.

## 6. Kết quả mong đợi
- Bài 1: Client GET nhận lời chào, POST gửi thông tin sinh viên; Server in payload và thời điểm nhận.
- Bài 2: Server cập nhật cảm biến mỗi 3 giây; Client hiển thị nhiệt độ, độ ẩm và cảnh báo khi nhiệt độ > 35°C hoặc độ ẩm < 40%.
- Bài 3: Controller thay đổi trạng thái đèn qua PUT, truy vấn qua GET; Monitoring Client nhận trạng thái ban đầu và các thay đổi qua Observe.

## 7. Lưu ý trước khi nộp
- Điền họ tên và mã sinh viên thật trong file client bài 1.
- Chạy thử đủ các chương trình, chụp ảnh màn hình kết quả thực tế và bổ sung vào bài nộp nếu giảng viên yêu cầu.
- README mô tả kết quả mong đợi; chỉ ghi là đã chạy thành công sau khi bạn tự chạy và kiểm tra trên máy.
