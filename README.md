<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    PLATFORM ERP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Platform ERP được áp dụng vào học phần Thực tập doanh nghiệp dựa trên mã nguồn mở Odoo. 

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🚀 3. Các project đã thực hiện dựa trên Platform

Một số project sinh viên đã thực hiện:
- #### [Khoá 15](./docs/projects/K15/README.md)
- #### [Khoá 16](./docs/projects/K16/README.md)
- #### [Khoá 17](./docs/projects/K17/README.md)

## ⚙️ 4. Cài đặt và Khởi chạy

### 4.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 4.1.1. Tải project
Mã nguồn dự án nằm trên môi trường Linux (WSL). Truy cập vào Terminal hoặc PowerShell trên Windows và gõ lệnh:
```bash
wsl
```
Sau đó, clone project và di chuyển vào thư mục dự án:
```bash
git clone https://github.com/FIT-DNU/Business-Internship.git
cd /home/dmin/Business-Internship
```

#### 4.1.2. Cài đặt các thư viện hệ thống cần thiết
Người sử dụng thực thi lệnh sau đề cài đặt các thư viện cần thiết:
```bash
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```

#### 4.1.3. Khởi tạo môi trường ảo Python
Odoo yêu cầu các thư viện đặc tả phải nằm trong một môi trường chia cách (virtual environment) để không bị xung đột.
- Khởi tạo môi trường ảo:
```bash
python3.10 -m venv ./venv
```
- Thay đổi trình thông dịch sang môi trường ảo (Tại mỗi phiên làm việc mới bạn **phải** chạy lệnh này):
```bash
source venv/bin/activate
```
*(Thành công khi ở đầu dòng code trong terminal xuất hiện chữ `(venv)`).*
- Chạy requirements.txt để cài đặt các thư viện được yêu cầu:
```bash
pip3 install -r requirements.txt
```

### 4.2. Setup database (PostgreSQL)
Cơ sở dữ liệu của dự án chạy trong Docker. Nếu không bật Docker Desktop, Odoo sẽ báo lỗi `Connection refused`.
- Mở **Docker Desktop** trên Windows và chờ cho tới khi trạng thái hiển thị *Engine Running*.
- Khởi tạo database trên docker bằng việc thực thi file `docker-compose.yml` (đứng ở thư mục gốc của project):
```bash
sudo docker-compose up -d
```

### 4.3. Setup tham số chạy cho hệ thống
Tạo tệp **odoo.conf** (có thể sao chép từ file **odoo.conf.template**) có nội dung như sau:
```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```

### 4.4. Chạy hệ thống Odoo và Cập nhật code

#### 4.4.1. Lệnh khởi chạy Odoo
Đảm bảo bạn vẫn đang ở trong môi trường ảo `(venv)`. Chạy Odoo và tự động gán luôn database `Business-Internship` của dự án:
```bash
python3 odoo-bin -c odoo.conf -d Business-Internship
```

> **🔴 LƯU Ý RẤT QUAN TRỌNG VỀ TÊN DATABASE:**
> Hành động `-d Business-Internship` sẽ gặp vấn đề nếu database thực sự của bạn đang mang tên khác (ví dụ: odoo, db_nhansu...). Hãy đổi chữ `Business-Internship` thành đúng tên Database cũ bạn hay làm.
> *Cách xem tất cả Database bạn đang sở hữu: Chạy lệnh `python3 odoo-bin -c odoo.conf` (không có `-d`), mở trình duyệt tới `http://localhost:8069/web/database/selector` để kiểm tra.*

#### 4.4.2. Lệnh cập nhật module (Update Code)
Khi bạn sửa code XML giao diện hoặc Model Python, cần thêm cờ `-u` để Odoo áp dụng:
- Cập nhật toàn bộ các module (Dùng khi sửa nhiều nơi hoặc khởi tạo lại):
```bash
python3 odoo-bin -c odoo.conf -d Business-Internship -u all
```
- Cập nhật một module cụ thể (Nhanh hơn, ví dụ module tên `nhan_su` hoặc `my_custom_module`):
```bash
python3 odoo-bin -c odoo.conf -d Business-Internship -u nhan_su
```

*(Lưu ý: Nếu bạn sử dụng Docker ngầm hoàn toàn hoặc SystemC, bạn có thể truy cập bằng lệnh: `docker exec -it <tên_container> /bin/bash` và gõ lệnh odoo tương ứng `-c /etc/odoo/odoo.conf -d Business-Internship`)*

Truy cập theo đường dẫn **[http://localhost:8069/](http://localhost:8069/)** để đăng nhập vào hệ thống.

## 📚 5. Nguồn phát triển dữ liệu
Tài liệu hướng dẫn cài đặt và khởi chạy dự án Odoo được tham khảo, tổng hợp và phát triển dựa trên đóng góp từ 2 nhóm thực tập:
- **Nhóm TTDN-15-05-N8**
- **Nhóm TTDN-15-05-N1**

## 📝 6. License

© 2024 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.
