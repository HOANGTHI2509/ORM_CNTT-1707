# CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI

## 1.1. Cơ sở hình thành và lý do chọn đề tài
### 1.1.1. Bối cảnh số hóa trong quản trị nội bộ doanh nghiệp
Trong tiến trình chuyển đổi số, ứng dụng công nghệ thông tin là yếu tố then chốt để nâng cao năng lực cạnh tranh. Tuy nhiên, tại nhiều tổ chức, mảng quản trị tài sản và điều phối tài nguyên vẫn tồn tại những rào cản nghiêm trọng:
- **Quản trị phân tán và công cụ lạc hậu:** Việc duy trì quản lý bằng sổ sách hoặc Excel tạo ra các "ốc đảo dữ liệu", khiến thông tin đứt gãy, khó theo dõi vòng đời tài sản và dẫn đến công tác bảo trì thụ động.
- **Thiếu minh bạch và rủi ro thất thoát:** Cấp phát thiếu định danh số khiến việc luân chuyển thiết bị mất kiểm soát, khó quy trách nhiệm cá nhân khi xảy ra hư hỏng, gây lãng phí nguồn lực tài chính.
- **Xung đột tài nguyên:** Thiếu hệ thống theo dõi thời gian thực dẫn đến tình trạng trùng lịch họp thường xuyên, gây gián đoạn công việc và suy giảm tính chuyên nghiệp trong vận hành.
- **Suy giảm hiệu suất vận hành:** Các quy trình thủ công tạo "điểm nghẽn" tiêu tốn thời gian của đội ngũ quản lý, cản trở sự phát triển chuyên nghiệp và tính minh bạch cần có của doanh nghiệp hiện đại.

### 1.1.2. Sự cần thiết của hệ thống quản lý có tính tích hợp
Để giải quyết tận gốc các vấn đề nêu trên, việc thiết lập một hệ thống quản trị tổng thể theo mô hình "All-in-one" thay vì sử dụng các phần mềm rời rạc là một nhu cầu cấp thiết. Hệ thống này đóng vai trò là "trung tâm dữ liệu" giúp xóa bỏ tình trạng cát cứ thông tin thông qua các giải pháp cốt lõi:
- **Quản lý tập trung toàn trình dữ liệu:** Hệ thống hóa toàn bộ vòng đời tài sản từ khâu mua sắm, nhập kho, cấp phát cho đến khi thanh lý. Điều này cho phép doanh nghiệp truy vết chính xác lịch sử mượn/trả, đánh giá tình trạng nguyên vẹn và giá trị còn lại của tài sản tại mọi thời điểm.
- **Điều phối thông minh và tối ưu hóa không gian:** Thay thế quy trình đặt phòng họp thủ công bằng thuật toán điều phối tự động, có khả năng phát hiện và chặn lặp lịch ngay từ bước khởi tạo, đảm bảo tài nguyên được khai thác tối đa và công bằng.

**Tích hợp HRM - "Chìa khóa vàng" trong quản trị trách nhiệm:** 
Điểm mấu chốt của hệ thống là việc liên kết chặt chẽ vòng đời tài sản vào bản ghi dữ liệu cốt lõi của con người. Việc tích hợp mạnh mẽ với phân hệ Quản lý Nhân sự giúp:
- **Định danh chính xác:** Xác định rõ ràng nhân sự và phòng ban đang chiếm hữu hoặc sử dụng tài sản/không gian.
- **Gắn liền trách nhiệm:** Thiết lập ràng buộc pháp lý và cơ chế bồi thường cụ thể cho từng cá nhân, giảm thiểu rủi ro sử dụng sai mục đích.
- **Chuẩn hóa dữ liệu toàn hệ thống:** Tự động hóa quy trình thu hồi tài sản đối với nhân viên nghỉ việc, đảm bảo không có sự sai lệch giữa dữ liệu nhân sự và thực tế lưu kho.

## 1.2. Mục tiêu nghiên cứu
### 1.2.1. Mục tiêu tổng quát
Mục tiêu bao trùm của đề tài là phân tích, thiết kế và triển khai hệ thống Quản lý Tài sản và Điều phối Phòng họp đạt chuẩn quản trị doanh nghiệp hiện đại. Hệ thống được xây dựng trên nền tảng lõi ERP Odoo 15, có khả năng chia sẻ cơ sở dữ liệu đồng nhất với phân hệ Nhân sự, đồng thời tích hợp Trợ lý Ảo AI (Gemini) làm cầu nối giao tiếp thông minh và đẩy thông báo qua ứng dụng Telegram.

### 1.2.2. Mục tiêu cụ thể
Để đạt được mục tiêu tổng quát, đề tài tập trung giải quyết các mục tiêu cụ thể theo ba cấp độ kỹ thuật tăng dần:

**Mức 1 – Xây dựng kiến trúc hệ thống và tích hợp dữ liệu cốt lõi:**
- Thiết kế và phát triển hai phân hệ Quản lý Tài sản và Điều phối Phòng họp trên framework Odoo.
- Thiết lập cơ chế liên kết dữ liệu vật lý với phân hệ HRM, lấy hồ sơ nhân viên làm dữ liệu gốc để định danh và truy vết mọi giao dịch mượn/trả tài sản.

**Mức 2 – Tự động hóa kiểm soát logic nghiệp vụ:**
- Phát triển thuật toán kiểm tra xung đột thời gian (Overlapping Time Algorithm) cho phân hệ phòng họp.
- Thiết lập cơ chế kiểm soát tự động (Validation Rules) để ngăn chặn và cảnh báo mọi nỗ lực khởi tạo lịch họp trùng lặp, thay thế hoàn toàn việc kiểm duyệt thủ công.

**Mức 3 – Thông minh hóa quy trình với AI Chatbot và Telegram Webhook:**
Ứng dụng công nghệ cốt lõi LLM (Gemini API) kết hợp cùng Webhook Telegram để xử lý hai quy trình phối hợp nhịp nhàng:
- **Trợ lý Ảo AI (Xử lý NLP):** Cung cấp giao diện Chatbot nội bộ để tiếp nhận câu lệnh ngôn ngữ tự nhiên từ người dùng. AI giữ vai trò bóc tách thực thể (Thời gian, Số lượng, Tên phòng) và gọi thẳng API vào Odoo để tự động tạo lịch mà không cần điền form tay.
- **Webhook Telegram (Thông báo đẩy):** Thay vì dùng để nhắn tin đặt phòng, Telegram hoạt động như một hệ thống Push Notification. Ngay khi Odoo cấp lịch thành công, hệ thống tự động bắn một Alert xác nhận về App Telegram trên thiết bị cá nhân của nhân sự.

## 1.3. Đối tượng và phạm vi nghiên cứu
### 1.3.1. Đối tượng nghiên cứu
Những đối tượng chính được đưa vào phân tích và áp dụng thực nghiệm trong đồ án bao gồm:
- **Framework Odoo 15:** Nghiên cứu sâu về kiến trúc đa tầng, mô hình MVC, cấu trúc dữ liệu trên PostgreSQL và sức mạnh của bộ công cụ ORM trong việc xử lý các truy vấn dữ liệu phức tạp.
- **Quy trình nghiệp vụ quản trị nội bộ:** Chuẩn hóa quy trình quản lý vòng đời tài sản từ nhập kho, khấu hao đến thanh lý; và nghiệp vụ điều phối phòng họp dựa trên sơ đồ trạng thái để quản lý lịch biểu thực tế.
- **Kiến trúc tích hợp hệ thống:** Nghiên cứu cơ chế giao tiếp qua RESTful API, phương thức xác thực bảo mật và kỹ thuật Webhook để thiết lập luồng gửi báo động (Alerts) tức thời giữa Odoo và Telegram.
- **Trí tuệ nhân tạo (NLP):** Kỹ thuật Prompt Engineering để LLM (Gemini) phân tích ngôn ngữ tự nhiên, bóc tách thực thể để chuyển đổi thành dữ liệu có cấu trúc.

### 1.3.2. Phạm vi nghiên cứu
Để đảm bảo đề tài đạt được tính khả thi và tập trung giải quyết triệt để các bài toán cốt lõi trong quỹ thời gian cho phép, dự án giới hạn phạm vi nghiên cứu ở ba khía cạnh sau:

**a) Phạm vi dữ liệu**
Hệ thống tập trung cấu trúc và quản lý ba nhóm thực thể dữ liệu trọng tâm:
- **Dữ liệu Vòng đời Tài sản:** Lưu trữ thông số cấu hình kỹ thuật, trạng thái vận hành, tọa độ vị trí vật lý và nhật ký điều chuyển thiết bị.
- **Dữ liệu Gốc Nhân sự:** Kế thừa cấu trúc từ phân hệ HR Base của Odoo. Giới hạn ở việc lấy định danh (Họ tên, Mã NV, Phòng ban) làm "mỏ neo" gắn trách nhiệm pháp lý. Hệ thống tuyệt đối không can thiệp vào dữ liệu chấm công hay tiền lương.
- **Dữ liệu Lịch biểu và Điều phối:** Quản lý sức chứa, trang thiết bị đi kèm của từng phòng chức năng và tọa độ thời gian các sự kiện. Băng thông dữ liệu này phục vụ trực tiếp thuật toán kiểm soát xung đột (Hard Boundaries).

**b) Phạm vi chức năng**
Dự án tập trung phát triển các luồng chức năng tự động hóa:
- **Phân hệ Quản lý Tài sản:** Thực thi các nghiệp vụ khởi tạo, bàn giao, thu hồi và chuyển nhượng tài sản. Ghi nhận thời gian hoạt động để tính khấu hao.
- **Phân hệ Điều phối Phòng họp:** Cung cấp giao diện Kanban hiển thị trạng thái rảnh/bận. Đặt lịch và xác thực ưu tiên cấp bậc nhân sự.
- **Phân hệ Trợ lý Ảo AI & Thông báo Telegram:** Cung cấp Chatbot Gemini nội bộ để xử lý chức năng "Text-to-Booking", kèm theo luồng Webhook bắn cảnh báo lịch biểu về App Telegram.

**c) Phạm vi ranh giới công nghệ**
Hệ thống được xây dựng và triển khai dựa trên các công cụ chỉ định:
- **Nền tảng lõi:** Hệ sinh thái Odoo 15.
- **Ngôn ngữ thực thi:** Lập trình Logic Backend bằng Python 3; thiết kế giao diện Frontend qua XML và mã nguồn Odoo Web Client.
- **Cơ sở dữ liệu:** PostgreSQL tương tác thông qua tầng ORM.
- **Giao tiếp ngoại vi:** Telegram API kết hợp với các mô hình ngôn ngữ lớn (Gemini LLM API) thông qua định dạng JSON POST Requests (Webhook).

## 1.4. Ý nghĩa khoa học và thực tiễn
### 1.4.1. Ý nghĩa thực tiễn
Sản phẩm phần mềm của đồ án có khả năng triển khai thực tế tại các doanh nghiệp quy mô vừa và lớn, đem lại bộ tứ giá trị cốt lõi:
- **Minh bạch hóa quản trị tài sản vật lý:** Khắc phục triệt để lỗ hổng gây thất thoát tài chính thông qua cơ chế định danh người dùng cuối, dễ dàng quy cứu trách nhiệm.
- **Tối ưu hóa hiệu suất thời gian:** Hệ thuật toán chặn lặp lịch giúp xóa sổ văn hóa "chat hỏi phòng trống" thủ công, giảm thiểu xung đột tài nguyên.
- **Nâng tầm trải nghiệm người dùng (UX):** Chuyển đổi các quy trình "điền form hành chính" khô khan thành thao tác trò chuyện với Trợ lý Ảo và nhận thông báo điện thoại, phù hợp với xu thế làm việc hối hả.
- **Thúc đẩy chuyển đổi số phi giấy tờ (Paperless):** Lệnh điều động thiết bị, phê duyệt phòng họp đều được chuyển hóa thành các bản ghi số hóa.

### 1.4.2. Ý nghĩa học thuật
Bên cạnh giá trị ứng dụng, đồ án còn đóng góp vào khía cạnh nghiên cứu khoa học:
- **Làm chủ quy trình tích hợp hệ thống:** Chứng minh tính hiệu quả của mô hình thiết kế CSDL phân mảnh có giao thoa chặt chẽ bằng khóa ngoại (Foreign Key) trong OOP MVC Odoo.
- **Giải bài toán chuẩn hóa dữ liệu phi cấu trúc:** Ứng dụng LLM như một màng lọc Parser biểu diễn việc chuyển hóa ngôn ngữ tự nhiên con người sang cấu trúc JSON máy tính.
- **Tạo nền tảng cho bảo trì dự phòng:** Dữ liệu vòng đời là cơ sở quan trọng cho các nghiên cứu tiếp theo về AI Predictive Maintenance.

## 1.5. Cấu trúc của báo cáo 
**Nội dung các chương chi tiết**
- **Chương 1: Tổng quan về đề tài:** Trình bày rõ bức tranh lý do hình thành dự án, chốt hạ mục tiêu phấn đấu, các biến số giới hạn phạm vi nghiên cứu và ý nghĩa đem lại.
- **Chương 2: Cơ sở lý thuyết và công nghệ sử dụng:** Trang bị kiến thức logic nền tảng về hệ kiến trúc Odoo, sơ đồ thiết kế cơ sở dữ liệu phân tán (ERD) và lý thuyết cốt lõi của Trợ lý AI / Webhooks.
- **Chương 3: Phân tích và thiết kế hệ thống:** Đóng vai trò hạt nhân của báo cáo, tiến hành giải phẫu nghiệp vụ (bản vẽ As-Is/To-Be), cấu trúc Bảng Ranh giới chức năng (Matrix) và lên ERD tích hợp 3 Model.
- **Chương 4: Triển khai và đánh giá kết quả thực nghiệm:** Phô diễn thành quả phần mềm. Cung cấp hình ảnh giao diện thực tế và các kịch bản test (Double-booking, Text-to-Booking AI).
- **Chương 5: Kết luận và hướng phát triển:** Đóng gói lại chuỗi đánh giá ưu, nhược điểm toàn hệ thống, mở ra định hướng roadmap mở rộng tính năng bảo trì AI tương lai dài hạn.
