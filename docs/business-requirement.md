# Tour Guide Agent đa tác nhân

## Phạm vi và nguyên tắc sản phẩm

- Đối tượng chính là khách du lịch cá nhân tự túc tại Việt Nam; ưu tiên người Việt đi du lịch nội địa.
- Phạm vi dữ liệu bao phủ các điểm du lịch nổi tiếng trên toàn Việt Nam.
- Ngôn ngữ sản phẩm trong phạm vi hiện tại là tiếng Việt; chưa yêu cầu hỗ trợ tiếng Anh.
- Một tài khoản có thể lập kế hoạch cho nhiều người; sản phẩm không phục vụ cộng tác nhiều tài khoản, quản trị đoàn hoặc điều hành tour.
- Dữ liệu nền được tổng hợp từ nguồn bên thứ ba; danh mục điểm đến ưu tiên do hệ thống quản lý và kiểm duyệt.
- Thông tin ổn định được trình bày ngắn gọn. Thông tin biến động phải có nguồn, thời điểm kiểm tra và mức độ tin cậy.
- Agent không tự đặt dịch vụ, giữ tiền hoặc thanh toán thay người dùng.
- Hệ thống chỉ lưu lý do quyết định dạng tóm tắt có cấu trúc, không lưu hoặc hiển thị chuỗi suy luận thô của mô hình.
- Dữ liệu cá nhân và nhật ký chỉ được sử dụng để cung cấp, hỗ trợ và bảo vệ dịch vụ.
- Dữ liệu GPS, tệp media gốc, working/trip memory của Agent và log kỹ thuật chi tiết được lưu tối đa 7 ngày. Một cron job chạy hằng ngày để đánh dấu hết hạn và dọn dẹp dữ liệu quá hạn.
- Hồ sơ, kế hoạch, đánh giá, bản tổng kết và các dữ liệu có cấu trúc đã được người dùng xác nhận không được xem là memory tạm thời của Agent và tiếp tục được lưu trong lịch sử tài khoản.

## Tài khoản và cá nhân hóa

- Đăng ký, đăng nhập và quản lý tài khoản cá nhân.
- Cập nhật hồ sơ du lịch gồm sở thích, nhu cầu đặc biệt và ngân sách thường dùng.
- Xem lịch sử hội thoại, kế hoạch, chuyến đi và bản tổng kết.
- Cá nhân hóa đề xuất từ hồ sơ và dữ liệu chuyến đi đã được người dùng xác nhận.

## Tiếp nhận yêu cầu chuyến đi

- Bắt đầu yêu cầu lập chuyến đi bằng hội thoại tự nhiên.
- Phân tích yêu cầu ban đầu, hồ sơ cá nhân và thông tin người đi cùng để tạo bản tóm tắt yêu cầu.
- Tự động hỏi các thông tin còn thiếu; ngày đi, nơi xuất phát và ngân sách là dữ liệu bắt buộc.
- Tiếp nhận GPS, ảnh và tệp đa phương tiện trong hội thoại để bổ sung ngữ cảnh. **Ví dụ:** đề xuất địa điểm du lịch có cảnh quan tương tự ảnh hoặc tìm địa điểm trong bán kính người dùng yêu cầu.
- Cho phép người dùng xem, bổ sung và chỉnh sửa bản tóm tắt yêu cầu trước khi lập kế hoạch.

## Khám phá địa điểm du lịch

- Gợi ý địa điểm theo sở thích, vị trí, thời gian, ngân sách và thông tin người tham gia.
- Tìm địa điểm gần vị trí GPS hiện tại hoặc vị trí do người dùng cung cấp.
- Tìm địa điểm có cảnh quan hoặc đặc điểm tương đồng với ảnh đầu vào.
- Xếp hạng địa điểm theo mức độ phù hợp và các đánh giá công khai đã được xác minh.
- Hiển thị lý do đề xuất để người dùng so sánh và lựa chọn địa điểm.

## Lập lịch trình

- Tạo từ 1 đến 4 lộ trình để người dùng so sánh và lựa chọn.
- Lập lịch theo từng ngày với điểm tham quan, nơi lưu trú, hoạt động, chặng di chuyển và thời gian dự kiến.
- Đề xuất phương tiện phù hợp cho từng chặng di chuyển.
- Dự trù tổng chi phí và các nhóm chi phí chính của chuyến đi.
- Tạo danh sách hành lý và vật dụng theo thời tiết, hoạt động, thời lượng và người tham gia.
- Hiển thị chi tiết thời lượng, tổng chi phí, điểm nổi bật, cảnh báo và đánh đổi của từng lộ trình để người dùng dễ lựa chọn. Giải thích lý do xếp hạng bằng ngôn ngữ dễ hiểu.

**Yêu cầu**: Kiểm tra ngân sách, giờ mở cửa, thời gian di chuyển và rủi ro an toàn trước khi hiển thị lộ trình.
  - Chặn lộ trình không khả thi và trả lại cho Planner Agent để điều chỉnh.
  - Hiển thị cảnh báo mềm để người dùng cân nhắc trước khi chọn.

## Tùy chỉnh lại kế hoạch

Có thể thực hiện chỉnh tay hoặc thông qua Agent.
- Chỉnh tay các thông tin đơn giản bằng thao tác thêm, sửa hoặc xóa từng điểm tham quan, nơi lưu trú, chặng di chuyển, hoạt động và vật dụng.
- Yêu cầu Agent thêm, xóa, thay thế hoặc sắp xếp lại từng phần của kế hoạch bằng hội thoại.
- Sau mỗi đề xuất chỉnh sửa của Agent, hiển thị phần bị ảnh hưởng, lý do thay đổi và cảnh báo phát sinh để người dùng xác nhận chấp nhận hoặc từ chối. Chỉ áp dụng thay đổi khi người dùng chấp nhận.
- Kiểm tra lại tính khả thi sau các thay đổi quan trọng.
- Tính lại lịch trình, chi phí, phương tiện, nơi lưu trú, hành lý và hoạt động.
- Cho phép người dùng xác nhận và lưu kế hoạch cuối để sử dụng trong chuyến đi.

## Đặt dịch vụ và logistics

- Tìm kiếm khách sạn, chuyến bay, phương tiện và dịch vụ liên quan qua API đối tác.
- So sánh lựa chọn theo giá, mức độ phù hợp, nhà cung cấp và điều kiện hủy hoặc đổi.
- Chuẩn bị thông tin hành khách và thông tin đăng ký cần thiết cho dịch vụ được chọn.
- Hiển thị giá cuối, nhà cung cấp và điều kiện hủy hoặc đổi để người dùng xác nhận rõ trước khi tiếp tục.
- Chuyển người dùng đến trang của bên thứ ba và hướng dẫn hoàn tất đăng ký hoặc thanh toán.

## Theo dõi thời gian thực trong chuyến đi

### Khám phá địa điểm du lịch

- Đề xuất các hoạt động nên thực hiện tại từng địa điểm du lịch, như tham quan điểm nổi bật hoặc mua quà lưu niệm.
- Trả lời câu hỏi và cung cấp thông tin về lịch sử, văn hóa, giá vé, giờ mở cửa và điều kiện tham quan của địa điểm trong hoặc ngoài lịch trình.
- Nhận câu hỏi bằng văn bản hoặc ảnh để nhận diện và giới thiệu địa điểm. Khi độ tin cậy thấp, Agent đưa ra nhiều khả năng và hỏi lại người dùng thay vì khẳng định một địa điểm duy nhất.
- Gợi ý nội dung thuyết minh khi người dùng đến gần một điểm trong lịch trình.
- Phát thuyết minh bằng âm thanh khi người dùng xác nhận thông báo hoặc chủ động yêu cầu.
- Cho phép bật hoặc tắt theo dõi GPS chủ động cho từng chuyến đi.

**Yêu cầu**: Hiển thị nguồn, thời điểm kiểm tra và mức độ tin cậy cho các thông tin có thể thay đổi.

### Cập nhật thời gian thực
- Theo dõi thời tiết, thời gian di chuyển, giờ mở cửa và các yếu tố ảnh hưởng đến kế hoạch.
- Background Weather Monitor định kỳ quét các chuyến đi đang hoạt động và kiểm tra dữ liệu biến động. Khi phát hiện ảnh hưởng đáng kể, job tạo cảnh báo và yêu cầu Agent lập phương án thay thế.
- Gửi cảnh báo quan trọng và đề xuất địa điểm, phương tiện hoặc lộ trình thay thế theo thời gian thực.
- Yêu cầu người dùng chấp thuận trước khi cập nhật kế hoạch đã chốt.
- Đánh dấu điểm đến không thể thực hiện khi đã đóng cửa hoặc có rủi ro an toàn rõ ràng.

## Đánh giá và nhận xét

- Chấm điểm và viết nhận xét cho địa điểm hoặc trải nghiệm.
- Lưu bài đánh giá ở chế độ riêng tư mặc định.
- Cho phép người dùng công khai từng bài đánh giá.
- Tiếp nhận báo cáo bài đánh giá vi phạm.
- Kiểm duyệt, chống spam và xác minh mức độ liên quan của bài đánh giá công khai.
- Sử dụng bài đánh giá công khai hợp lệ làm tín hiệu xếp hạng địa điểm.

## Tổng kết chuyến đi

- Tự động tạo bản nháp tổng kết sau khi chuyến đi kết thúc.
  - Background Trip Completion job định kỳ quét các chuyến đi đã đến thời điểm kết thúc hoặc nhận tín hiệu kết thúc sớm để tạo bản nháp đúng một lần.
  - Tổng hợp địa điểm đã đi, địa điểm đã bỏ qua và các thay đổi thực tế.
  - So sánh chi phí dự kiến với chi phí do người dùng nhập.
  - Ghi nhận đánh giá và trải nghiệm cá nhân của người dùng.
  - Cho phép người dùng xác nhận hoặc chỉnh sửa bản tổng kết.
  - Cập nhật lịch sử cá nhân hóa từ dữ liệu tổng kết đã được xác nhận.
- Gợi ý chuyến đi tiếp theo dựa trên hồ sơ và lịch sử đã xác nhận.

## Nhật ký kiểm toán

- Lưu nhật ký kiểm toán gồm đầu vào, phản hồi, nguồn dữ liệu, công cụ đã gọi, kết quả, lý do tóm tắt, lỗi và phiên bản Agent.
- Cho phép người dùng xem nguồn, cảnh báo, thay đổi và lý do quyết định của chuyến đi.
- Cho phép đội vận hành tra cứu log kỹ thuật theo phân quyền.
- Trước khi mở chi tiết log kỹ thuật, yêu cầu khai báo cả mục đích truy cập và Ticket ID.
- Ghi nhận người thực hiện, thời gian, địa chỉ IP, mục đích truy cập và Ticket ID cho mỗi lần truy cập log kỹ thuật.
- Hỗ trợ truy vết lỗi và kiểm tra lại quyết định của Agent từ nhật ký kiểm toán.

---

## Hệ thống đa tác nhân

- **Planner Agent**: phân tích yêu cầu để tạo và điều chỉnh lộ trình.
- **Critic/Evaluator Agent**: kiểm tra bắt buộc đối với lộ trình mới và các thay đổi quan trọng.
- **Booking & Logistics Agent**: tìm, so sánh và hướng dẫn sử dụng dịch vụ bên thứ ba.

### Nhiệm vụ của các Agent

- Chia sẻ cùng một bản tóm tắt yêu cầu, dữ liệu đã kiểm chứng và phiên bản kế hoạch hiện tại giữa các Agent.
- Điều phối việc chuyển giao nhiệm vụ, kết quả và lỗi giữa các Agent.
- Yêu cầu Agent liên quan xử lý lại khi kết quả không đạt điều kiện kiểm chứng.
