# 🎬 Kịch Bản Video Quay Dự Án: Hệ Sinh Thái Odoo (HR - Tài Sản - Đặt Phòng) & Trợ Lý AI

**Cấu trúc Video:** 
1. Giới thiệu tổng quan 3 module.
2. Phân tích ERD và Luồng dữ liệu (Data Flow).
3. Demo tích hợp trên giao diện truyền thống.
4. **Cú Twist ở cuối:** Dùng AI để làm tất cả các bước trên bằng 1 câu lệnh.

---

### 1️⃣ Phần 1: Giới thiệu Bối Cảnh (30 giây)

**[Cảnh quay]**
- Màn hình hiển thị trang chủ Dashboard Odoo chứa icon 3 module: Tuyển dụng/Nhân sự, Quản lý tài sản, Đặt phòng họp.

**[Lời thoại]**
> "Chào thầy cô và các bạn! Hôm nay mình xin phép demo một hệ sinh thái chuyển đổi số thu nhỏ doanh nghiệp trên nền tảng Odoo. Dự án của mình tập trung vào 3 phân hệ cốt lõi: Quản trị Nhân sự, Quản lý Tài sản và Đặt phòng họp/Hội trường. Điểm đáng giá nhất của hệ thống này không phải nằm ở từng module, mà nằm ở tính toàn vẹn dữ liệu và khả năng liên kết sâu sắc giữa chúng."

---

### 2️⃣ Phần 2: Giải thích Mô Hình ERD và Luồng Dữ Liệu (45 giây)

**[Cảnh quay]**
- Đưa hình ảnh/Slide chụp sơ đồ ERD (Entity Relationship Diagram) lên màn hình. Đánh dấu đỏ (highlight) vào các đường nối (Foreign Keys) giữa 3 bảng chính: `hr.employee` (Nhân sự), `tai_san` (Tài sản) và `dat_phong` (Đặt phòng).

**[Lời thoại]**
> "Hãy nhìn vào kiến trúc ERD của hệ thống! Bảng **Nhân sự (hr.employee)** đóng vai trò là Master Data trung tâm.
> - Khi một cá nhân cần công cụ làm việc, hệ thống Tài Sản sẽ nối khóa ngoại (`Many2one`) trực tiếp với bảng Nhân sự để tạo ra **Phiếu Bàn Giao**.
> - Tương tự, tại phân hệ **Đặt Phòng Hội Trường**, bảng Phiếu Đặt Phòng (dat_phong) vừa liên kết với Nhân sự để biết *Ai là người đặt*, lại vừa liên kết với bảng **Tài Sản (tai_san)** qua cấu trúc `Many2many` để biết cuộc họp này *Cần mượn thêm những máy móc nào*.
> Luồng dữ liệu đi một đường thẳng rõ ràng: Khởi tạo con người -> Cấp phát thiết bị -> Tổ chức sự kiện kèm theo thiết bị đó. Lát cắt dữ liệu hoàn toàn không bị trùng lặp."

---

### 3️⃣ Phần 3: Demo Tính Liên Kết Trên Giao Diện (1 phút)

**[Cảnh quay]**
- Mở danh sách Nhân sự, cho thấy một nhân viên tên Nguyễn Thanh Tùng.
- Chuyển sang module *Quản lý Tài Sản*. Bấm tạo "Phiếu bàn giao". Tại ô Người nhận, sổ dropdown xuống và chọn đúng "Nguyễn Thanh Tùng" (đã đồng bộ ngay lập tức). Chọn máy chiếu. Lưu lại.
- Chuyển sang module *Đặt phòng*. Tạo mới phếu đặt phòng. Chọn người đặt là "Nguyễn Thanh Tùng", duyệt xuống dưới mục "Tài sản mượn kèm", click chọn thêm các loại dây cáp/Micro từ module Tài sản.

**[Lời thoại]**
> "Trên giao diện truyền thống, tính tích hợp này thể hiện rất mượt mà. Ngay khi nhân sự được tạo bên module HR, tên của họ lập tức xuất hiện ở các dropdown chọn người mượn bên Tài Sản và Đặt Phòng. Và khi Tùng set up một sự kiện phòng họp Lớn, bạn ấy không cần chạy sang kho mượn đồ riêng, mà tick chọn mượn thẳng Máy Chiếu từ danh mục của kho Tài sản ngay bên trong báo cáo Đặt Phòng. Trạng thái của Máy chiếu bên phân hệ kia cũng rẽ nhánh sang *Đang sử dụng* ngay lập tức!"

---

### 4️⃣ Phần 4: "Cú Twist" Cuối Cùng - Trợ Lý AI Khép Kín Chu Trình (1 phút 15 giây) ⭐

**[Cảnh quay]**
- Xóa các phiếu mượn làm thủ công ban nãy đi, quay lại màn hình trắng.
- Bật pop-up chat của **Trợ lý AI Gemini** (ở phân hệ Đặt phòng).
- Gõ vào khung chat hoặc đọc voice: *"Đặt phòng họp lớn cho Tùng vào sáng mai, thêm 1 máy chiếu và 2 cái micro nhé."*
- Nhấn Enter. Dành 2-3 giây cho AI processing (có xoay viền loading). Màn hình TỰ ĐỘNG BẬT RA một Phiếu Đặt Phòng hoàn chỉnh từ A-Z với đầy đủ liên kết. 

**[Lời thoại]**
> "Nhưng khoan đã! Việc điền từng bảng biểu, chọn từng dropdown như vừa rồi vẫn còn quá rườm rà. Nắm giữ trái tim của dự án chính là sự xuất hiện của **AI tích hợp**.
> Thay vì lặp lại 10 cú click chuột qua các phân hệ, mình chỉ tích hợp mô hình phân tích ngôn ngữ tự nhiên Gemini của Google vào làm một Trợ lý Ảo.
> Mình gõ thử: *'Đặt phòng họp lớn cho Tùng sáng mai, thêm 1 máy chiếu và micro'*.
> Lúc này, sức mạnh của ERD phát huy tác dụng: Lệnh của mình được AI phân tách, đâm xuyên qua cả 3 bảng Database. AI định danh 'Tùng' trong Object Nhân sự, convert 'sáng mai' thành khung giờ lưu trữ dưới DB, đồng thời gọi API sang module Tài sản để nhặt đúng mã Máy chiếu đang rảnh rỗi nhét vào sự kiện Đặt phòng.
> Cuối cùng thì... bùm! Một Phiếu đặt phòng hoàn hảo sinh ra chỉ sau 1 câu lệnh. Công nghệ AI khi kết hợp với một Data Model chuẩn xác sẽ mang lại quyền năng chuyển đổi số tuyệt vời. Xin cảm ơn các bạn đã lắng nghe!"

---
**Ghi chú quay dựng:** Đoạn chiếu file hình ảnh ERD (Sơ đồ thực thể liên kết) bạn có thể chèn hình vào khi dựng video nhé. Và lúc làm bước 3 "Click tạo tay thủ công", bạn hãy bấm chọn nhanh/tua nhanh để tạo độ tương phản với tốc độ xử lý 1 chạm của AI ở Phần 4.
