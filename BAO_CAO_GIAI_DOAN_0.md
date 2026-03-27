# BÁO CÁO PHÂN TÍCH NGHIỆP VỤ (GIAI ĐOẠN 0)
**Đề tài 6: Quản lý Nhân sự + Quản lý Tài sản + Quản lý Phòng họp**

---

## BƯỚC 1: CHỌN MÔ HÌNH DOANH NGHIỆP (DOMAIN)

Nhóm căn cứ vào bối cảnh Đề tài 6 để xây dựng **Mô hình D** chuyên biệt, tích hợp chặt chẽ việc quản trị con người và tài sản dùng chung:

**Mô hình D: Tập đoàn Công nghệ / Không gian làm việc chung (Tech Hub / Co-working Space)**
- **Tên doanh nghiệp giả định:** Công ty TNHH Giải pháp Công nghệ DNU (DNU Tech)
- **Phù hợp với:** Nhóm xử lý logic Vận hành tài nguyên chia sẻ (Shared Resources) & Tự động hoá tiện ích văn phòng (Facility Management).
- **Bối cảnh:** Trụ sở Tập đoàn Công nghệ nhiều phòng ban, Toà nhà Văn phòng chia sẻ (Co-working Space), Trung tâm Đào tạo.
- **Đặc thù:**
  - Không bán sản phẩm vật lý, mà "cung cấp Không gian và Tiện ích" (Space & Facility) phục vụ nội bộ hoặc khách thuê.
  - Tài sản (Máy chiếu, Màn hình tương tác, Loa...) gắn liền chặt chẽ với Trạng thái Không gian (Hội trường, Phòng họp).
- **Thách thức cốt lõi:** Quản lý chống xung đột lịch trống (Double-booking) giữa các phòng ban và theo dõi công suất/hao mòn tài sản để kích hoạt bảo trì tự động (Predictive Maintenance).

---

## BƯỚC 2: PHÂN RÃ CHỨC NĂNG (THE MATRIX)

Bảng phân chia ranh giới quyền hạn độc lập (Hard Boundaries) giữa 3 Module để tránh tình trạng "lẩu thập cẩm":

| Hạng mục | Module NHÂN SỰ (HRM) | Module PHÒNG HỌP (Booking) | Module TÀI SẢN (Asset) |
| :--- | :--- | :--- | :--- |
| **Vai trò** | **"Người quản trị Con người"** | **"Người điều phối Không gian"** | **"Người giữ Thiết bị"** |
| **Chức năng chính** | - Quản lý Hồ sơ nhân viên, chức vụ, bộ phận.<br/>- Quyết định nhân sự nào đang làm việc hay đã nghỉ.<br/>- Cung cấp dữ liệu gốc (Master Data) để định danh "Ai đang thao tác". | - Quản lý danh mục phòng họp, sức chứa.<br/>- Booking lịch họp và kiểm tra Trống/Bận.<br/>- Điều phối các Dịch vụ đi kèm (Teabreak). | - Quản lý Vòng đời tài sản (Cấp phát, Thu hồi, Thanh lý).<br/>- Ghi nhận khấu hao ảo (giờ máy chạy).<br/>- Xuất "Phiếu bảo trì" tự động. |
| **Đầu ra (Output)** | Danh sách nhân viên và Cấp bậc quyền hạn rõ ràng. | Phiếu đặt phòng được Duyệt/Huỷ & Lịch họp. | Lịch sử mượn trả thiết bị & Phiếu bảo trì định kỳ. |
| **🚨 CẤM KỴ (Ranh giới đỏ)** | Không được tự tạo Trạng thái phòng họp hay can thiệp vào máy móc. | **Không được tự ý sửa đổi hồ sơ nhân viên.** Không được tự quyền thay đổi trạng thái hỏng hóc hay "Lưu trữ" của tài sản trong phòng. | Không được tự ý duyệt lịch phòng họp thay cho Quản lý. |

---

## BƯỚC 3: THIẾT KẾ LUỒNG DỮ LIỆU (DATA FLOW) VÀ KỊCH BẢN

**Kịch bản nghiệp vụ (User Scenario): Chu trình đặt phòng họp "All-in-one"**

1. **(HRM):** Hệ thống nhận diện nhân viên `Trần Văn A` (thuộc phòng Marketing) đăng nhập hợp lệ.
2. **(Booking):** Sáng thứ Hai, `Nhân viên A` tiến hành tạo yêu cầu mượn `Hội trường Tầng 3` từ 14h-16h để tổ chức Seminar. Trong Phiếu, A tích chọn thêm **Dịch vụ Teabreak** và mượn kèm thêm **Tài sản: Máy chiếu 4K**.
3. **(Booking):** Hệ thống kiểm tra khung giờ 14h-16h và xác nhận `Hội trường Tầng 3` đang rảnh. Quản lý hệ thống duyệt Phiếu. Lập tức API gọi Notification bắn tin nhắn qua **[Telegram]** thông báo cho A lịch họp đã chốt.
4. **(Asset):** Hệ thống Tài sản tự động trích xuất trạng thái `Máy chiếu 4K` từ "Lưu trữ" sang "Đang mượn".
5. **(Booking/Asset):** 16h họp xong, `A` bấm nút "Trả phòng". Phòng họp trở về trạng thái trống. Đồng thời, hệ thống `(Asset)` tự động tính toán +2 giờ công suất hoạt động cho `Máy chiếu 4K`. Do Máy chiếu đã vượt mốc 500 giờ hoạt động, hệ thống lập tức tự động sinh ra một **Phiếu Bảo Trì** cảnh báo cho bộ phận Kỹ thuật đi kiểm tra thiết bị.
