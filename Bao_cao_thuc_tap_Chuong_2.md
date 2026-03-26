# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÔNG NGHỆ SỬ DỤNG

## 2.1. Nền tảng Hoạch định Nguồn lực Doanh nghiệp (Odoo 15)
### 2.1.1. Giới thiệu tổng quát về Odoo 15
Odoo (trước đây là TinyERP và OpenERP) là một bộ giải pháp phần mềm quản trị doanh nghiệp mã nguồn mở (Open Source ERP) mạnh mẽ và linh hoạt nhất hiện nay, được phát triển bởi Fabien Pinckaers. Khởi đầu từ một dự án nhỏ, Odoo đã vươn tầm trở thành một hệ sinh thái phần mềm đồ sộ với hàng chục nghìn ứng dụng, phục vụ hàng triệu người dùng trên toàn cầu từ các doanh nghiệp siêu nhỏ đến các tập đoàn đa quốc gia.

Điểm cốt lõi tạo nên sự khác biệt của Odoo là **kiến trúc mô-đun (Modular Architecture)**. Thay vì một khối phần mềm cồng kềnh, Odoo cho phép doanh nghiệp bắt đầu với những tính năng thiết yếu nhất và mở rộng dần theo quy mô phát triển. Các mô-đun trong Odoo, dù được phát triển độc lập, vẫn sở hữu khả năng liên kết hữu cơ và chia sẻ cơ sở dữ liệu chung tuyệt vời.

Một số phân hệ nòng cốt tạo nên sức mạnh của hệ thống bao gồm:
- **Human Resource Management (HRM):** Quản lý hồ sơ nhân viên, cơ cấu tổ chức và quy trình tuyển dụng.
- **Calendar & Planning:** Điều phối lịch trình làm việc và các sự kiện nội bộ theo thời gian thực.
- **Inventory & Warehouse:** Kiểm soát dòng chảy hàng hóa và tối ưu hóa không gian lưu trữ.
- **Accounting & Finance:** Tự động hóa bút toán và báo cáo tài chính theo tiêu chuẩn quốc tế.

Về mặt kỹ thuật, Odoo 15 được xây dựng trên bộ khung công nghệ hiện đại:
- **Ngôn ngữ Python:** Đảm bảo khả năng xử lý logic mạnh mẽ, dễ đọc và dễ bảo trì.
- **Hệ quản trị PostgreSQL:** Cung cấp sự ổn định, an toàn và hiệu năng cao cho cơ sở dữ liệu quy mô lớn.
- **XML & JavaScript:** Cho phép tùy biến giao diện linh hoạt và xây dựng các ứng dụng Web (SPA) mượt mà.

Trong phạm vi đề tài này, Odoo 15 không chỉ đóng vai trò là một phần mềm nghiệp vụ, mà còn được khai thác tối đa với tư cách là một **Framework phát triển (Development Framework)**. Đội ngũ thực hiện đã tận dụng khả năng mở rộng (Extensibility) của Odoo để:
1. **Xây dựng module tùy chỉnh `quan_ly_tai_san`:** Số hóa toàn bộ danh mục thiết bị vật lý và vòng đời tài sản.
2. **Phát triển module `quan_li_phong_hop_hoi_truong`:** Thiết lập quy trình điều phối không gian làm việc thông minh.
3. **Tích hợp API Đa phương thức:** Kết nối đồng bộ với Trí tuệ nhân tạo (Gemini AI) và luồng tin nhắn di động (Telegram Webhook) để hiện thực hóa văn phòng thông minh (Smart Office).

Chính sự linh hoạt này đã giúp Odoo 15 trở thành lựa chọn hàng đầu cho các dự án chuyển đổi số đòi hỏi tính đặc thù cao và khả năng tích hợp không giới hạn.

### 2.1.2. Cơ chế kế thừa và quản trị ORM
Odoo được xây dựng dựa trên mô hình kiến trúc MVC (Model – View – Controller), trong đó:
- **Model:** Đại diện cho Cấu trúc cơ sở dữ liệu và logic nghiệp vụ cốt lõi.
- **View:** Giao diện người dùng cuối hiển thị tương tác (Viết bằng XML).
- **Controller:** Xử lý yêu cầu HTTP Routing và điều hướng hệ thống tới ngoại vi.

Hệ thống sử dụng ORM (Object-Relational Mapping) để làm cầu nối giữa các đối tượng trong Python và dữ liệu nằm dưới PostgreSQL. Nhờ đó, lập trình viên có thể thao tác với dữ liệu dưới dạng object thân thiện mà không cần viết trực tiếp các câu lệnh truy vấn SQL khô khan, phức tạp.

Một trong những đặc điểm tạo nên sức mạnh của Odoo là cơ chế kế thừa thông qua từ khóa:
- `_inherit`: Mở rộng trực tiếp hoặc ghi đè một model đang có sẵn mà không làm vỡ code gốc.
- `_name`: Khai sinh cấu trúc tạo một model hoàn toàn mới.

**Ví dụ:** 
- Kế thừa và mở rộng bảng `hr.employee` gốc của Odoo để gắn trực tiếp khóa liên kết đến bảng dữ liệu tài sản sở hữu.
- Kế thừa `calendar.event` để xây dựng chức năng module điều phối phòng họp.

**Ưu điểm của cơ chế này:**
- Đảm bảo an toàn không làm thay đổi hay phá hỏng cấu trúc mã nguồn gốc.
- Dễ bảo trì và nâng cấp lên phiên bản cao hơn một cách độc lập.
- Đảm bảo tính ổn định tuyệt đối khi đưa hệ thống ra chạy thực tế (Production).

*→ Đây là nền tảng quan trọng giúp hệ thống phân hệ trong đề tài có thể mở rộng theo cấp số nhân mà vẫn giữ được tính toàn vẹn của một kho dữ liệu ERP.*

## 2.2. Cơ sở lý thuyết Tích hợp Hệ thống
### 2.2.1. Sơ đồ thực thể ERD
Trong một hệ thống ERP chuẩn mực, các trường dữ liệu giữa các phân hệ không bao giờ được phép nằm tồn tại cô lập rời rạc, mà phải có mối quan hệ tham chiếu chặt chẽ với nhau. Việc thiết kế sơ đồ ERD (Entity-Relationship Diagram) đóng vai trò xương sống kiến trúc.

Sơ đồ ERD trong Odoo giải quyết bài toán:
- Xác định điểm chạm của các thực thể như: Nhân viên cầm Tài sản, hay Nhân sự Mượn Phòng họp.
- Thiết lập quy tắc truyền tải giữa các thực thể tham chiếu chéo.
- Đảm bảo tính toàn vẹn và sạch sẽ của CSDL.

Trong Odoo, các mối quan hệ được ràng buộc chặt thông qua các trường liên kết (Relational Fields):
- **`Many2one`**: Khóa ngoại liên kết Nhiều → Một (Ví dụ: Nhiều thiết bị máy chiếu tài sản đều thuộc quyền sở hữu quản lý của chung Một phòng ban IT).
- **`One2many`**: Liên kết Một → Nhiều.
- **`Many2many`**: Liên kết Nhiều ↔ Nhiều (ví dụ: Nhiều người cùng tham gia vào Một sự kiện phòng họp, và một khối tài sản có thể luân chuyển qua nhiều người).

Việc thiết kế ERD đúng chuẩn mang lại các lợi ích to lớn:
- Tránh trùng lặp sinh rác dữ liệu trên server.
- Tối ưu hóa tốc độ truy xuất.
- Dễ dàng truy ngược lịch sử log.

*→ Đây là bước nền tảng để đồ án có thể thiết kế kiến trúc khóa ngoại giao thoa giữa 3 model `quan_ly_tai_san`, `quan_li_phong_hop_hoi_truong` và `hr.employee` một cách khoa học.*

### 2.2.2. Tính rành mạch của dữ liệu cốt lõi
Trong hệ thống ERP, khái niệm Master Data (Dữ liệu Gốc) đóng vai trò làm điểm trung tâm quy chiếu, từ đó phân phát thông tin đảm bảo tính nhất quán đồng bộ trên toàn cõi hệ thống.

Trong kiến trúc của đồ án:
- **Module Nhân sự (`hr.employee`)** được tôn trọng và định vị là nguồn dữ liệu gốc (Master Data).
- Mọi con người thật ngoài đời đều chỉ được quy chiếu bằng một bản ghi định danh duy nhất trong CSDL `hr.employee`.

Tất cả các module nghiệp vụ tự code xung quanh đều bắt buộc phải gọi tham chiếu Foreign Keys đến dữ liệu gốc này, bao gồm:
- Giao định danh ai là người quản lý tài sản trên model `quan_ly_tai_san`.
- Xác định chính xác tài khoản nhân viên nào vừa thao tác mượn không gian trên `quan_li_phong_hop_hoi_truong`.

Nguyên lý này được gọi là **“Hard Boundaries” (Ranh giới cứng)**, điều đó ấn định rằng:
- Tuyệt đối không được phép thiết kế Data cài cắm rời rạc hay cho phép nhập text tay tên người thao tác. Mọi ID định danh đều phải trỏ đúng về HR Master Data.
- Chỉ thông qua Master Data, hệ thống mới gắn được trách nhiệm cá nhân trực diện cho từng phòng ban.

**Lợi ích của việc tuân thủ triết lý này:**
- Dễ dàng bóc tách để quy cứu trách nhiệm hoặc truy xuất log lỗi.
- Đóng gói và thu hồi quyền lợi tự động ngay lập tức đối với nhân viên nghỉ việc.
- Hệ thống luôn hoạt động Single Source of Truth (Nguồn chân lý duy nhất).

## 2.3. Công nghệ kết nối API ngoại tuyến và Trí tuệ Nhân tạo
### 2.3.1. External API và Webhook (Telegram Push Notification)
Để mở rộng khả năng tiếp cận và thông báo, hệ thống sử dụng cơ chế API và điểm nối Webhook nhằm tương tác với các ứng dụng nền tảng bên ngoài. Phá bỏ ranh giới phần mềm trong môi trường cục bộ.

- **API RESTful:** Cầu nối cho phép Controller của Odoo giao tiếp trực tuyến với máy chủ Server Telegram ngoài Internet.
- **Webhook Endpoint:** Hoạt động như một cơ chế báo động kích hoạt dữ liệu tự động ngay khi có một sự kiện chốt tín hiệu hoàn tất ở hệ thống (ví dụ: Quản lý vừa bấm nút "Duyệt" cấp phòng họp).

Trong cấu trúc luồng của đồ án này:
- Nền tảng Telegram được tận dụng để hoạt động tựa như một dịch vụ điện tín Push Notification (Thông báo đẩy) dành riêng cho ID của từng người dùng đầu cuối.
- **Quy trình hoạt động:** Ngay khi ghi nhận thiết lập phiên mượn phòng được hệ thống Odoo chốt duyệt lưu CSDL thành công, thuật toán Webhook Python sẽ ngay lập tức tự động biên dịch dữ liệu, lấy thông tin thời gian/địa điểm cuộc họp và bắn một cảnh báo (Alert) bay thẳng về ứng dụng nhắn tin Telegram cài sẵn trên điện thoại của nhân sự.

Ưu điểm của giải pháp gửi thông báo qua nền tảng viễn thông này:
- Giúp người dùng cập nhật trạng thái kết quả lịch làm việc tức khoảnh khắc mọi lúc, mọi nơi mà không bắt buộc phải mở màn hình web ERP theo dõi liên tục.
- Thông báo mang tính cá biệt hóa cá nhân đối với từng user tài khoản.

*→ Việc cấu hình Webhook Telegram đóng vai trò như một "Đường dây liên lạc tự động" trung thành giữa kho cơ sở dữ liệu Odoo và cuộc sống di động của nhân viên.*

### 2.3.2. Trợ lý Trí tuệ Nhân tạo xử lý ngôn ngữ (Gemini AI Chatbot)
Nhằm bứt phá vượt lên sự kỳ vọng của một hệ thống nhập liệu thủ công khô khan, đồ án tiên phong nâng cấp bằng việc nhúng thêm các bộ API mô hình ngôn ngữ lớn (Ví dụ công nghệ Gemini tiên tiến của nhà phát triển Google). Việc thấu hiểu Xử lý ngôn ngữ tự nhiên (NLP) đem lại cho cấu trúc Odoo một bộ não ngoại vi.

Sự hiện diện của nền tảng LLM có mô phỏng luồng hoạt động như một **Trợ lý Ảo (Smart Chatbot)**:
- **Tiếp nhận hội thoại:** Nhận tin nhắn do nhân viên cung cấp bằng lời nói văn bản quen thuộc đời thường (Ví dụ dòng văn bản: *"Tìm nhanh cho chị phòng nào trống lúc 9h sáng thứ Hai tuần sau cỡ 50 người để họp ban giám đốc"*).
- **Trích xuất thông tin (Entity Extraction):** Thay vì sử dụng những câu lệnh Regex tìm kiếm từ khóa cứng nhắc, bộ não AI đọc dữ liệu, thấu hiểu ngữ cảnh và tự động bóc tách các Thực thể quan trọng (Entities): Tên không gian phòng, Chuỗi dải Range Time quy chuẩn, Số lượng sức chứa bắt buộc.
- **Cấu trúc hóa tham số lập trình:** Mô hình biên dịch cụm hội thoại hỗn loạn thành một khối mảng cấu trúc JSON đạt chuẩn giao thức. Thông qua API nội bộ, khối dữ liệu này lập tức tải vào Database Odoo và tự động hoàn thành sinh bản ghi Event Lịch biểu mới không cần user thao tác tay nhọc nhằn.

*→ Việc chuyển đổi từ thao tác điền Form rườm rà truyền thống thông qua hành vi "Trò chuyện tạo Data trực tiếp" với Trợ lý ảo đánh dấu bước tiến công nghệ to lớn, khẳng định giá trị ứng dụng mạnh mẽ nhất cho bài toán ERP tương lai.*