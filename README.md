<h1 align="center">HỆ THỐNG ERP: ĐIỀU PHỐI TÀI SẢN VÀ PHÒNG HỌP</h1>
<p align="center"><i>BÁO CÁO BÀI TẬP LỚN: HỘI NHẬP VÀ QUẢN TRỊ PHẦN MỀM DOANH NGHIỆP</i></p>
<div align="center">

[![Odoo](https://img.shields.io/badge/Odoo-15.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

## 📌 THÔNG TIN ĐỀ TÀI
- **Tên đề tài:** Đề 6 - Quản lý Tài sản + Phòng họp (Nâng cao)
- **Mục tiêu cốt lõi:** Quản lý tài sản và điều phối lịch sử dụng phòng họp như những tài sản dùng chung.
- **Nền tảng:** Phân tích, Tái cấu trúc và Mở rộng dựa trên Odoo 15.

---

## 🌟 ĐÁP ỨNG TIÊU CHÍ ĐÁNH GIÁ (MỨC 1 - MỨC 2 - MỨC 3)

### 🟢 MỨC 1: TÍCH HỢP HỆ THỐNG (Cơ bản - Đáp ứng 100%)
Đảm bảo tính nhất quán dữ liệu xuyên suốt 3 Module, lấy hồ sơ Nhân sự làm Trái tim:
1. **Dữ liệu Gốc Nhân Sự (`nhan_su`):** Kế thừa `hr.employee` gốc của Odoo, mở rộng quản lý thông tin nhân viên (CCCD, Quê quán, ...).
2. **Module Tài Sản (`quan_ly_tai_san`):** Tất cả tài sản đều được gắn với `nguoi_su_dung_id` trỏ về `hr.employee`.
3. **Module Phòng Họp (`quan_li_phong_hop_hoi_truong`):** Mọi giao dịch Đặt phòng, Duyệt phòng, và Lập Biên bản đền bù đều trỏ Khóa ngoại tham chiếu về tập dữ liệu chuẩn `hr.employee`. Cấm tuyệt đối nhập liệu người dùng ảo.

### 🟡 MỨC 2: TỰ ĐỘNG HÓA QUY TRÌNH (Nâng cao - Vượt ngưỡng)
Giảm thiểu tối đa thao tác thủ công bằng các Trigger tự động ngầm (Event-driven):
- **Tự động Trích xuất Bảo trì (Cross-module):** Ngay khi một cuộc họp kết thúc (bấm `Trả phòng`), hệ thống tự động quét toàn bộ `tai_san_ids` (Loa, Máy chiếu) đi kèm trong phòng đó, trích xuất thời lượng cuộc họp (ví dụ: 2 giờ) và tự động cộng dồn vào `so_gio_su_dung` của Tài sản. Nếu máy chiếu vượt hạn mức (VD: 5000 giờ), **tự động phân rã Biên Bản Bảo Trì** ở Phân hệ Tài sản mà không cần con người nhúng tay thao tác.
- **Auto-Cancel (Thuật toán Hủy Lịch Di Dây):** Khi 1 phiếu đặt phòng được duyệt, toàn bộ các phiếu khác trùng phòng xếp hàng chờ duyệt sẽ bị hệ thống **Tự động chuyển trạng thái Hủy** và gửi báo cáo về Email của người bị hủy.
- **Scheduled Actions (Cron Jobs):** Hệ thống tự động đẩy Email nhắc nhở trước giờ họp 15 phút và cảnh báo tự động khi quá hạn trả phòng.

### 🔴 MỨC 3: ỨNG DỤNG CÔNG NGHỆ MỚI (Xuất sắc)
- **Tích hợp External API (Telegram Bot API):** Toàn bộ luồng nghiệp vụ quan trọng đều được bắn thông báo thời gian thực về kênh chat qua hệ mã hóa Bot Telegram Token:
  - Báo động có đơn Đặt phòng mới (Chờ duyệt).
  - Lãnh đạo duyệt phòng thành công.
  - Thông báo Force-Override "Cướp lịch" / Tự động hủy để nhường slot theo Hệ Chức vụ HR.
  - Cảnh báo sinh Phiếu bảo trì tự động / Lập biên bản đền bù tài sản hỏng ngay lập tức vào Smart Phone.

---

## 🚀 CÁC TÍNH NĂNG VƯỢT TRỘI CẤP CAO ĐỀ 6
Nhóm đã phát triển 3 Cơ chế Điều phối Lịch độc quyền theo Sơ đồ ERD, xoáy mạnh vào Mục tiêu cốt lõi *Tránh Xung Đột Lịch (Booking Conflict)* của Đề 6:

1. **Chống Trùng Lịch Kép (Tài sản dùng chung chéo):** Lọc `@api.constrains` không chỉ check Xung đột Phòng, mà ghim chặt cả Cấu trúc Tài Sản Đính kèm. Khóa cứng quyền mượn nếu Thiết bị đó (VD: Máy tính VIP) đang bị 1 phòng khác ở cách đó 10 mét mượn trong cùng khung giờ.
2. **Nhượng Quyền Điều Phối HR (Force Override):** Tích hợp Sơ đồ tổ chức HR. Trưởng phòng / Giám đốc có quyền Đặt phòng/Thiết bị đè lên khung giờ của Nhân viên thực tập sinh. Hệ thống tự động tước quyền (Auto-Cancel) của Nhân viên để ưu tiên Cấp Lãnh đạo bằng một tin nhắn Thông báo đĩnh đạc.
3. **Smart Suggestion (Tự động Điều Phối Thiết bị):** Nếu người dùng chọn mượn "Máy chiếu Sony" nhưng trúng lịch kẹt, hàm `@api.onchange` tự động quét kho và swap sang "Máy chiếu Panasonic" (Thiết bị rảnh rỗi tương đương) để cứu vãn đơn Đặt phòng thay vì báo lỗi cục súc. Kèm chức năng Đặt Dịch vụ (Tea-break, MC) hoàn thiện qua widget Checkbox.

---

## 🔀 LUỒNG NGHIỆP VỤ TỔNG QUAN (BUSINESS FLOW)

![Sơ đồ Nghiệp vụ](docs/business_flow/Nhom06_BusinessFlow_TaiSanPhongHop.png)

> **Mô tả điểm Tích hợp (Integration Points):** 
> 1. Trụ cốt Yêu cầu: Cán bộ thuộc HR làm Tọa độ gốc.
> 2. Các điểm chạm Xuyên Module: Hành vi Trả phòng thành công sẽ ghi Log hao mòn thiết bị và kích hoạt sự kiện Tự Động tạo Phiếu Bảo Trì (Bên Tài Sản). 
> 3. Điểm External API: Mọi Action Event (Ký nhận, Duyệt, Trừ hao mòn) đều Auto-Request API ra Telegram.

---

## ⚙️ HƯỚNG DẪN CÀI ĐẶT
1. Clone Mã Nguồn vào máy.
2. Khởi tạo Database Postgres.
3. Liên kết Server qua file `odoo.conf`.
4. Run & Cài 3 cục Module Nhóm tạo. Hưởng thụ sản phẩm.
