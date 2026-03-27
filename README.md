<h2 align="center">
    OFFICE RESOURCE MANAGER
</h2>
<div align="center">

[![Odoo](https://img.shields.io/badge/Odoo-16.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

> **Học Phần:** Hội nhập và quản trị phần mềm doanh nghiệp - Đề Tài 6

## 📖 1. Giới thiệu
**Office Resource Manager** là hệ thống quản lý tài nguyên doanh nghiệp được xây dựng trên nền tảng Odoo. Hệ thống tập trung vào việc số hóa quy trình quản lý hành chính nội bộ.

### ✨ Những điểm mới & Cải tiến so với dự án gốc (Khóa trước - K15)
Trong quá trình thực tập và phát triển "Đề 6: Quản lý tài sản và phòng họp", dự án đã được bổ sung và phát triển hướng tới tự động hóa quy trình với các điểm nổi bật sau:

**1. Phân hệ Quản lý Phòng họp (Room Booking):**
- **Trải nghiệm UI/UX Kanban:** Bổ sung giao diện Kanban dạng thẻ trực quan phân loại tự động trạng thái phòng mượn (Chờ duyệt, Đã duyệt, Đang sử dụng, Đã trả, Đã hủy).
- **Tính năng Dịch vụ đi kèm (`dich_vu_di_kem`):** Bổ sung mô hình hoàn toàn mới liên kết với đơn đặt phòng cho phép thêm các dịch vụ phát sinh (trà, nước, máy chiếu, v.v...).
- **Tích hợp Bot Telegram Webhooks:** Hệ thống tự động đẩy thông báo toàn diện qua Telegram khi có đơn đặt, bao gồm thời gian đặt, tên người dùng đăng kí và chi tiết dịch vụ đi kèm.
- **Tối ưu lịch đặt phòng:** Đặt chế độ xem bằng Lịch (Calendar View) làm cấu hình mặc định, đổi thuật ngữ từ `Đăng ký mượn phòng` thành `Đơn đặt phòng` cho chuyên nghiệp.

**2. Phân hệ Quản lý Tài sản (Asset Management):**
- **Ràng buộc Toàn vẹn Dữ liệu (Unique SQL Constraints):** Bổ sung các cấu hình ràng buộc cơ sở dữ liệu để chống trùng lặp dữ liệu đối với 'Loại tài sản' và 'Nhà cung cấp', hỗ trợ xử lý và quản lý tối ưu kho.
- **Liên kết Hệ thống Nhân sự:** Kế thừa thông tin Nhân viên (`hr.employee` và `nhan_vien_inherit`) bổ sung thuộc tính người thụ hưởng tạo dây chuyền luân chuyển dữ liệu mạch lạc từ yêu cầu đến nhận tài sản.

**3. Công nghệ mới:** 
- **Tích hợp AI:** Xây dựng mô hình tương tác tích hợp Gemini AI và Telegram Webhooks, tự động hóa quy trình phản hồi thông minh (được phát triển theo báo cáo).

### Các module chính:
1.  **Quản lý Nhân sự (`nhan_su`)**: Hồ sơ nhân viên, quản lý thông tin cá nhân.
2.  **Quản lý Tài sản (`quan_ly_tai_san`)**: Theo dõi tài sản, khấu hao, bảo trì, cấp phát tài sản cho nhân viên.
3.  **Quản lý Phòng họp (`quan_li_phong_hop_hoi_truong`)**: Đặt phòng họp, duyệt yêu cầu, tránh trùng lịch.

## 🚀 2. Hướng dẫn Cài đặt & Sử dụng

### 2.1. Clone dự án
Tải mã nguồn về máy:
```bash
git clone https://github.com/HOANGTHI2509/office-resource-manager.git
cd office-resource-manager
```

### 2.2. Cài đặt môi trường
Yêu cầu: `Python 3.10`, `PostgreSQL`, `Docker` (tùy chọn).

1.  **Cài đặt thư viện hệ thống (Ubuntu/WSL):**
    ```bash
    sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-dev build-essential libpq-dev
    ```

2.  **Tạo môi trường ảo & cài dependencies:**
    ```bash
    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### 2.3. Cấu hình Database
Sử dụng Docker để chạy PostgreSQL nhanh chóng:
```bash
sudo docker-compose up -d
```

### 2.4. Cấu hình Odoo
Tạo file `odoo.conf` (hoặc copy từ template):
```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```

### 2.5. Chạy hệ thống
```bash
python3 odoo-bin.py -c odoo.conf -u nhan_su,quan_ly_tai_san,quan_li_phong_hop_hoi_truong
```
Truy cập: `http://localhost:8069`
Tài khoản mặc định (nếu dùng demo data): `admin` / `admin`

## 🤝 Nguồn phát triển dữ liệu & Đóng góp
Dự án được phát triển dựa trên nền tảng Business Internship của Khoa CNTT - Đại học Đại Nam.

Tài liệu hướng dẫn cài đặt và khởi chạy dự án Odoo được tham khảo, tổng hợp và phát triển dựa trên đóng góp từ 2 nhóm thực tập:
- **Nhóm TTDN-15-05-N8**
- **Nhóm TTDN-15-05-N1**
