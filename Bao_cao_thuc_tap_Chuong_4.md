# CHƯƠNG 4: TRIỂN KHAI VÀ ĐÁNH GIÁ KẾT QUẢ THỰC NGHIỆM

## 4.1. Chuẩn bị môi trường triển khai
### 4.1.1. Cấu hình máy chủ phần mềm
Hệ thống Odoo được khởi tạo đồng bộ toàn diện dựa trên nền tảng kỹ thuật mã nguồn chia sẻ của Hệ sinh thái Odoo, qua sự tinh chỉnh chuyên sâu theo cấu trúc cá nhân của sinh viên:
- **Môi trường Sandbox:** Hệ điều hành WSL (Linux Ubuntu 22.04 LTS) trực thuộc lõi điều phối Windows.
- **Hệ quản trị CSDL:** PostgreSQL 14 đóng vai trò lưu trữ và thao tác cơ sở dữ liệu.
- **Application Layer:** Odoo 15 Community/Enterprise đi kèm môi trường Python (Virtual Environment) tích hợp các thư viện mở rộng (`requests`, `json`) để phục vụ nhận/gửi API ra ngoại vi.

### 4.1.2. Thiết lập thông số bảo mật API
Để giao tiếp với thế giới bên ngoài, hệ thống tiến hành khai báo hai chốt chặn API mang tính chất quyết định:
- **Gemini (LLM API Key):** Đăng ký Token cấp quyền từ Google AI Studio, nạp thẳng vào System Parameters của Odoo để gọi lệnh bóc tách dữ liệu NLP nội bộ.
- **Telegram (Bot Token API):** Khởi tạo `BotFather`, lấy chuỗi Token API và cấu hình mã ChatID để Odoo sử dụng dưới dạng Webhook Push Notifications (Điểm báo tin một chiều đẩy ra).

## 4.2. Kết quả xây dựng ứng dụng cốt lõi (Mức 1)
### 4.2.1. Giao diện chức năng Model Tài sản (`quan_ly_tai_san`)
Việc minh bạch hóa dữ liệu CSDL diễn ra hoàn hảo tại Model Quản lý Tài sản. Giao diện Form View cho phép nhân sự chức năng thao tác:
- Cấp phát Máy chiếu, Loa, Micro... cho từng cá nhân/phòng ban.
- Tra cứu tức thì: Gắn biến `nguoi_su_dung_id` (trỏ Foreign Key đến `hr.employee`) để xác nhận danh tính người mượn. Bằng giao diện Odoo, quản trị viên dễ dàng nhấp ngay một Smart Button (nút thông minh) hiển thị trong thẻ thông tin Nhân sự, tự động liệt kê tất cả các khối thiết bị mà cá nhân đó đang quản lý mà không cần tìm kiếm thủ công mỏi mắt.
- Thay đổi thông tin người thụ hưởng ở file `quan_ly_tai_san`, danh mục `hr.employee` cập nhật ngay lập tức. Đây là đặc quyền của việc chuẩn hóa kiến trúc Master Data.

### 4.2.2. Giao diện Model Phòng họp Hội trường (`quan_li_phong_hop_hoi_truong`)
Model làm nhiệm vụ lên lịch khai thác sở hữu giao diện vô cùng linh hoạt cho tổ chức:
- **Lưới Calendar / Kanban:** Hiển thị trực quan bức tranh trạng thái không gian làm việc rảnh/bận trong tuần lễ.
- **Ràng buộc thiết bị:** Trong quá trình lập phiếu đăng ký sự kiện, người dùng được quyền bấm chọn tick list danh mục tài sản đi kèm phòng (Ví dụ: Yêu cầu thêm Máy chiếu 4K) thông qua hàm liên kết hiển thị dữ liệu gốc lấy từ module `quan_ly_tai_san`.

## 4.3. Đánh giá tính năng Tự động hóa và Ràng buộc (Mức 2)
### 4.3.1. Kịch bản chặn lỗi trùng lịch phòng họp (Double-booking)
Giả định khung thực nghiệm thao tác thực tế:
- **Bối cảnh:** Nhân viên A đã tiến hành Submit (chốt rành) phiếu giữ vị trí Phòng Họp A trong hệ thống Lịch từ thời điểm 13:00 - 15:00. 
- **Bước thử nghiệm:** Ngay lập tức, nhân viên B tạo một Calendar Event Đặt Phòng mới, cố ý thiết lập lịch trùng lại Phòng Họp A lúc 14:30 - 15:30.
- **Kết quả:** Quá trình Đăng ký của cá nhân B bị hệ thống chém đứng lại bởi một cờ báo lỗi Popup ngáng đường: **"Failure Notification: Không gian này đang được mượn vào giờ quy định, xin mời hủy thao tác dời chọn lịch trình thay thế!"**. 
Kết luận, hàm kiểm duyệt nội dung `@api.constrains` chặn Overlapping Time hoạt động vững chãi, đạt tỷ lệ 100% tự động hóa xử lý lồng lấp thời gian chết.

## 4.4. Đánh giá luồng Tích hợp AI và Thông báo (Mức 3)
Chức năng cao cấp nhất phô diễn bản lĩnh điều hướng ứng dụng Trí tuệ ảo (AI NLP) và tích hợp kênh viễn thông Push Notification (Telegram Webhook). Đưa hệ thống ERP thoát khỏi kén thụ động nhập liệu.

### 4.4.1. Phô diễn tính năng Nội bộ: Trợ lý AI Chatbot (Gemini)
Thực nghiệm quá trình Text-to-Booking tại Odoo:
- Tình trạng khởi điểm: Người dùng mở box Chat Terminal Trợ lý Ảo trên phần mềm công ty.
- Nhập liệu: Gõ một đoạn Text mộc mạc bằng chính ngôn ngữ tự nhiên: *"Hãy tìm nhanh và chốt cho tôi Phòng Họp Lớn vào lúc 15h chiều mai phục vụ báo cáo cổ đông với sức chứa 20 người"*.
- **Kết quả xử lý:** Khi người dùng ấn nút, mô hình LLM API xử lý lọc nhiễu ngôn từ, bóc tách tóm gọn các Thực thể lõi (Entities: `Phòng_Họp_Lớn`, `15:00`, `20_người`). Trả về cấu trúc khối file JSON thuần chủng. Nhận đối số mảng, Controller Odoo tự kích hàm thiết lập ra bản ghi sự kiện mới (Event Calendar Record) ngay tức khắc mà không dùng tay điền chằng chịt các box Form Web.

### 4.4.2. Phô diễn tính năng Ngoại tuyến: Webhook Thông báo (Telegram)
Thực nghiệm luồng Push Notification bám đuôi người dùng:
- Quay trở lại kết quả cấp duyệt thành công lệnh Booking được gọi tại tiến trình 4.4.1. Hệ thống cập nhật Status chốt đơn.
- Một cước bấm cò lệnh Webhook (HTTP POST) âm thầm khởi động kích bắn một bức thư ra Internet nhắm trúng cái đích Gateway API do Telegram Server cung cấp. 
- **Kết quả hiển thị:** Trong cùng tích tắc (chưa đầy 3s thực thi), màn hình điện thoại di động của người đăng kí rung lên hiển thị một Push Alert tĩnh tại App Telegram: *"🎉 Lệnh mượn Phòng Họp Lớn của bạn vào lúc 15:00 chiều mai đã được duyệt và cập nhật thành công lên Hệ thống"*.
- **Đánh giá tổng quan:** Gỡ bỏ rào cản hành chính. Đẳng cấp hệ thống tự lưu, tự chốt và tự nhảy Alert qua SmartPhone biến mô hình ERP từ trạng thái lưu trữ cứng nhắc (Passive) thành tương tác chủ động (Proactive Real-time Notifications). Cỗ máy thay đổi hoàn toàn thói quen báo cáo số cực kỳ tiện lợi!
