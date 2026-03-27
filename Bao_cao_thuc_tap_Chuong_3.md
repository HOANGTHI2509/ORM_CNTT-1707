# CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

## 3.1. Phân tích nghiệp vụ "Quản lý Tài sản và Phòng họp"

### 3.1.1. Bối cảnh và Mô hình doanh nghiệp lựa chọn (Mô hình D)
Đề tài được xây dựng trên nền tảng bối cảnh thực tế của một doanh nghiệp giả định: **Công ty TNHH Giải pháp Công nghệ DNU (DNU Tech)**. Mô hình hoạt động cốt lõi của tổ chức này được định vị dưới dạng một Tập đoàn Công nghệ (Tech Hub) hoặc một hệ thống Không gian làm việc chung (Co-working Space). Đây là những mô hình đặc trưng sở hữu quy mô nhân sự lớn, chia thành nhiều phòng ban chuyên trách, nhưng lại thường xuyên phải tận dụng chung một hệ sinh thái tài nguyên đồ sộ bao gồm các không gian làm việc tập thể và trang thiết bị công nghệ đắt tiền.

**a. Đặc thù vận hành nghiệp vụ**
Điểm khác biệt lớn nhất của DNU Tech là giá trị cốt lõi nằm ở việc **"cung cấp Không gian và Tiện ích" (Space & Facility)** để phục vụ trọn vẹn nhu cầu nội bộ hoặc cho các cá nhân bên ngoài thuê. Việc sử dụng tài sản có sự gắn kết hữu cơ vô cùng chặt chẽ với từng không gian cụ thể. Ví dụ điển hình: Một thiết bị Máy chiếu 4K luôn được tích hợp cố định vào Hội trường A; do đó, khi hệ thống ghi nhận có lịch sử dụng hội trường, vòng đời hoạt động của máy chiếu đó cũng tự động kích hoạt.

**b. Thách thức trong quản trị và điều phối**
Với số lượng nhân sự đông đảo cùng tần suất hội họp liên tục, hệ thống ERP Odoo khi áp dụng vào doanh nghiệp này bắt buộc phải giải quyết hai bài toán cốt lõi:
- **Thứ nhất, ngăn chặn xung đột tài nguyên (Double-booking):** Triệt tiêu sự cố tranh chấp không gian khi có hai phòng ban cùng cố gắng đặt một phòng họp vào cùng một khung thời gian.
- **Thứ hai, tối ưu hóa quản trị vòng đời tài sản (Predictive Maintenance):** Tự động hóa việc theo dõi tần suất sử dụng thực tế và mức độ hao mòn của thiết bị phần cứng. Hệ thống có khả năng tự động sinh ra "Phiếu bảo trì" để nhắc nhở bộ phận Kỹ thuật kiểm tra khi máy móc đạt ngưỡng giới hạn an toàn.

**c. Sơ đồ tổ chức phòng ban**
Để vận hành trơn tru mô hình trên, DNU Tech được phân rã thành các khối phòng ban chính:
- **Khối Quản trị Nguồn nhân lực (HR):** Định danh nhân sự (Admin).
- **Khối Quản trị Không gian & Thiết bị (Facilities):** Điều phối phòng họp và cấp phát máy móc.
- **Khối Chuyên môn (Marketing, IT, Sales...):** Người dùng cuối (User) có nhu cầu đặt phòng làm việc.

### 3.1.2. Phân rã chức năng (The Matrix)
Để tuân thủ tuyệt đối nguyên tắc "Bất khả xâm phạm" (Hard Boundaries) của hệ thống ERP theo yêu cầu đồ án, tránh tình trạng viết code "lẩu thập cẩm" lấn sân nghiệp vụ, giới hạn quyền hạn của 3 Module chính được xây dựng qua bảng ma trận sau:

| Hạng mục | Module NHÂN SỰ (`hr.employee`) | Module PHÒNG HỌP (`quan_li_phong_hop_hoi_truong`) | Module TÀI SẢN (`quan_ly_tai_san`) |
| :--- | :--- | :--- | :--- |
| **Vai trò** | **"Người quản trị Con người"** | **"Người điều phối Không gian"** | **"Người giữ Thiết bị"** |
| **Chức năng chính** | - Quản lý Hồ sơ nhân viên, chức vụ, bộ phận.<br/>- Quyết định nhân sự nghỉ việc.<br/>- Cung cấp dữ liệu gốc để định danh "Ai đang thao tác". | - Booking lịch họp và kiểm tra Trống/Bận.<br/>- Điều phối sức chứa phòng và dịch vụ xuất Teabreak đi kèm. | - Quản lý Vòng đời tài sản.<br/>- Ghi nhận khấu hao ảo (giờ máy chạy).<br/>- Xuất Phiếu bảo trì tự động. |
| **Đầu ra (Output)** | Danh sách nhân viên và Cấp bậc quyền hạn rõ ràng. | Bảng Lịch trình khai thác phòng và Phiếu đặt duyệt thành công. | Lịch sử mượn trả thiết bị & Phiếu cảnh báo bảo trì định kỳ. |
| **🚨 CẤM KỴ** | CẤM không được tự tạo hay can thiệp vào máy móc. | **CẤM tự ý sửa đổi hồ sơ nhân viên.** CẤM tự sửa trạng thái hỏng hóc thiết bị. | CẤM duyệt lịch phòng họp thay thế cấp Quản lý. |

### 3.1.3. Luồng nghiệp vụ hiện trạng (As-Is)
*   **Công tác quản lý Tài sản:** Các phòng ban mượn trang thiết bị đắt tiền của doanh nghiệp (máy ảnh, bộ máy chiếu, chìa khóa dự phòng) qua các loại giấy đi đường hoặc khai file excel lưu. Sự vắng bóng đồng bộ CSDL khiến việc rà soát luân chuyển tài sản, thu hồi để bảo trì, hay xác định trách nhiệm bảo quản người cầm gần như đứt đoạn.
*   **Vấn đề điều phối phòng họp chung:** Người điều hành thường đặt thời gian mượn phòng họp thông qua lịch chat rườm rà. Kết cục khi quy mô công ty gia tăng, tình huống 2 bộ phận cùng lao vào tổ chức họp chồng khung giờ tại cùng một không gian là bài toán nhức nhối cần giải bài.

### 3.1.4. Kịch bản nghiệp vụ (User Scenario) và Luồng đề xuất (To-Be)
Hệ thống ERP Odoo khi đưa vào lập trình sẽ tuân thủ cơ chế chuyển hóa dữ liệu tự động thay vì dùng giấy tờ thủ công, được mô phỏng qua luồng kịch bản toàn cảnh (All-in-one):
1. **(HRM nhận diện):** Hệ thống xác thực nhân viên `Trần Văn A` (Phòng Marketing) vừa đăng nhập hợp lệ vào hệ thống nội bộ.
2. **(Booking khởi tạo):** Sáng thứ Hai, `A` thao tác tạo yêu cầu mượn `Hội trường Tầng 3` từ 14h-16h để làm Seminar. Trong form đăng ký, `A` chọn tích kèm thêm dịch vụ mượn **Tài sản: Máy chiếu 4K**.
3. **(Booking chốt đơn):** Hệ thống quét thuật toán kiểm tra khung giờ 14h-16h, chốt phản hồi `Hội trường Tầng 3` đang rảnh rỗi. Ngay sau khi Quản lý nhấn duyệt phiếu, API Webhook liền bắn 1 thông báo tin nhắn qua **App Telegram** trên điện thoại gửi cho `A` để xác nhận lịch họp đã khởi tạo xong tức thì.
4. **(Asset tiếp nhận):** Module Tài sản được chia sẻ tham chiếu, tự động đổi tình trạng `Máy chiếu 4K` từ nằm trong kho thành "Đang mượn".
5. **(Bảo trì tự động):** 16h họp xong, tài nguyên phòng trống trở lại. Bộ máy tự động ghi nhận +2 giờ công suất hoạt động cho Máy chiếu 4K. Phát hiện tổng số giờ vận hành của máy chiếu này vừa vượt mốc 500 giờ, hàm điều phối ngay lập tức tự động sinh ra một tờ **Phiếu Bảo Trì** cảnh báo cho bộ phận Kỹ thuật đi kiểm tra thay bóng đèn cho thiết bị.
*   Định danh hoá: 100% tài sản cấp chung phải thiết lập thành thực thể số hóa (Digital Record). Dứt khoát liên kết chặt chẽ trách nhiệm bồi thường "Ownership" vào Profile của từng người thông qua bộ CSDL Nhân sự tập trung.
*   Hàng rào chốt chặn Logic (Validation Fence): Việc book không gian tổ chức bị cài cờ giới hạn vòng lặp theo Thời gian trôi (Overlapping Time Algorithm). 
*   Trải nghiệm Mức 3 phi truyền thống: Thay vì điền biểu mẫu rườm rà, `A` chỉ cần gõ hội thoại tự nhiên thông qua AI Chatbot nội bộ: *"Tìm nhanh phòng trống để họp Seminar 2 tiếng chiều nay cho 15 người"*, là đã xin lệnh tạo hóa hệ thống thành công. Ngay lập tức tín hiệu báo kết quả được Push Notification về điện thoại qua kênh Telegram.

## 3.2. Thiết kế Cơ sở dữ liệu và Tích hợp 3 Model Cốt lõi
Đáp ứng chính xác điểm chuẩn Mức 1 (Tích hợp Hệ thống), 3 Model custom sinh ra bằng Odoo Python được cấu hình thiết kế ERD liên thông chặt chẽ bằng khóa ngoại:

### 3.2.1. Thiết kế Model Dữ liệu gốc: Phân hệ Nhân sự (`hr.employee`)
*   **Vị thế Master Model:** Kế thừa bản quyền từ Base Odoo Employees (`_inherit`). Mở rộng chèn thêm CCCD định danh nội địa. Đạt vai trò Bảng Gốc (Parent Table).
*   Đóng vai trò xuất cấp thông tin mã quy chiếu ID định danh nhân sự đi tham chiếu ngược vào 2 module custom còn lại trong toàn hệ thống.

### 3.2.2. Thiết kế Model Quản lý Tài sản (`quan_ly_tai_san`)
*   Hứng chịu khối model data vật phẩm thiết bị cấp phát nội bộ. Tận dụng cờ Checkbox Boolean `is_phong_hop` để làm Switch bật tắt các thuộc tính sức chứa số ghế ngồi (nếu thiết bị Tài sản đó mang tính không gian phòng họp tĩnh).
*   **Ràng buộc ERD:** Khởi tạo trường biến cột `nguoi_su_dung_id` (với kiểu ràng buộc liên kết `Many2one`) để móc nối móc khóa ngoại thẳng vào gốc rễ data bộ bảng `hr.employee`. Hệ thống cấm tiệt việc gắn quản lý tài sản cho nhân sự đã đăng xuất hoặc khai báo người không tồn tại.

### 3.2.3. Thiết kế Model Điều phối: Quản lý Phòng họp Hội trường (`quan_li_phong_hop_hoi_truong`)
*   Đóng vai trò làm Controller sinh mã bảng theo dõi chuỗi luân chuyển sự kiện, theo sát trục thời gian để tính rảnh rỗi.
*   **Tích hợp vào Model Tài sản:** Gõ biến `phong_hop_id` sử dụng hàm liên kết RDB Constraint (`Many2one`) nhằm dẫn nguồn Data phòng ốc vật tư về chung mục đích.
*   **Tích hợp vào Model Nhân sự:** Bọc Object trường `nguoi_dat_id` vào khóa `Many2one` kết nối trỏ đến `hr.employee` để tra cứu ai là người chịu trách nhiệm cá nhân khởi tạo cuộc họp.

## 3.3. Tự động hóa Dữ liệu và Thiết kế Trợ lý Agent
### 3.3.1. Thuật toán ngăn xung đột dữ liệu Lịch biểu phòng họp (Mức 2)
Xây dựng chốt chặn bằng Decorator `@api.constrains` trên mã nguồn back-end bảng Python của Event Đặt phòng. Khi logic ghi nhận hàm `create` yêu cầu Book Phòng A giờ X, Logic Backend chủ động:
*   Kích hoạt query lệnh `search_count()` rà soát toàn cõi bảng Lịch Trình nhằm lấy mẫu các Record có trúng trùng tham chiếu `phong_hop_id = A`.
*   Tiến hành xét tiếp đường bao biến Thời gian. Giải phương trình hai tập hợp thời gian có đè lên nhau hay không. Khi số lượng bản ghi phát sinh lỗi giao thoa Overlap $\geq$ 1, Odoo hất bỏ Object và thả Exception chặn lại tiến trình lặp lịch vô lý.

### 3.3.2. Cấu trúc liên kết Trợ lý Ảo AI (Gemini) và Push Notification Telegram (Mức 3)
*   **Giao tiếp Chatbot NLP:** Để tự động hóa hoàn toàn luồng nhập liệu tay truyền thống, API Chatbot mang não bộ LLM (Gemini API) đóng đô tại hệ thống Controller cục bộ. Nó nhận đoạn hội thoại thô do nhân viên nhập vào, bộ máy LLM gọi prompt thực thi bóc tách các Thực thể quan trọng: Object Tên phòng, Dải khung Range Time, Số lượng người ước tính, biên soạn trả về khối cấu trúc mảng JSON. 
*   Quá trình biến ảo diễn ra trong Model `quan_li_phong_hop_hoi_truong`, Odoo chọc parse cục JSON đó thành tham số thực, gọi hàm ORM `create()` điền bản ghi Event thẳng vào CSDL.
*   **Alert Webhook Telegram:** Cuối cùng, mã Token Bot API kết nối nền tảng Telegram đóng vai trò làm điểm gửi báo tin báo động tĩnh. Ngay sau khi lệnh phòng ban được xác thực lưu, Server bắt Trigger đẩy HTTP Webhook Request phóng một luồng Push Notification xác nhận số giờ lệnh room về màn hình App Telegram của điện thoại nhân viên khởi tạo lúc trước.
