# NỘI DUNG CUỘC HỌP 
## Thảo luận và chốt các vấn đề trong Database
- Trường `version` bên trong bảng `trip_request` có tác dụng gì? 
- Có trường hợp nào cần query tất cả hình ảnh của tất cả `purpose` bên trong `media_file` không. Nếu có trường hợp đó thì thực hiện tách ra thành nhiều bảng khác nhau theo purpose. 
- 
Luồng: 
- Người dùng tạo trip_request

## Luồng nghiệp vụ

### Tạo tài khoản và hồ sơ du lịch

1. `USER` nhập `email`, `password` và `full_name`.
2. Người dùng đăng nhập khi `users.status` là `ACTIVE`.
3. Người dùng nhập `travel_preferences`, `special_needs` và `default_budget`.
4. Người dùng lưu thông tin vào `user_profile`.

### Tạo yêu cầu chuyến đi

1. Người dùng tạo một `agent_session` ở trạng thái `ACTIVE`.
2. Người dùng gửi nội dung qua `messages`.
3. Người dùng có thể gửi `media_files` với `purpose` là `REQUEST_IMAGE`.
4. Hệ thống tạo `trip_requests` ở trạng thái `DRAFT`.
5. Người dùng kiểm tra và chỉnh sửa thông tin chuyến đi.
6. Người dùng xác nhận để chuyển trạng thái sang `CONFIRMED`.

### Khám phá và chọn địa điểm

1. Người dùng tìm `places` theo `place_categories`, `province` hoặc `location`.
2. Người dùng xem giá, giờ mở cửa và `place_reviews` có trạng thái `PUBLIC`.
3. Người dùng kiểm tra `source_name`, `checked_at` và `confidence`.
4. Người dùng chọn hoặc bỏ chọn địa điểm trong `trip_request_selected_places`.

### Tạo và chọn lộ trình

1. Người dùng yêu cầu tạo lộ trình từ `trip_requests` đã `CONFIRMED`.
2. Người dùng theo dõi `agent_runs` của `PLANNER` và `CRITIC`.
3. Hệ thống lưu kết quả kiểm tra vào `evaluation_results`.
4. Người dùng so sánh 1–4 `itineraries` ở trạng thái `DRAFT`.
5. Người dùng xem chi phí, điểm nổi bật, cảnh báo và đánh đổi.
6. Người dùng chọn một `itineraries` sang trạng thái `SELECTED`.

### Chỉnh sửa và chốt lộ trình

1. Người dùng sửa `itinerary_days`, `itinerary_activities` hoặc `itinerary_transits`.
2. Người dùng có thể yêu cầu Agent tạo `itinerary_proposals`.
3. Người dùng xem `diff_payload`, `rationale` và `warnings`.
4. Người dùng chuyển `status` thành `accepted` hoặc `rejected`.
5. Người dùng chốt lộ trình để tạo `trips.finalized_itinerary_id`.

### So sánh dịch vụ đối tác

1. Người dùng mở `booking_offers` của lộ trình đã chọn.
2. Người dùng lọc theo `offer_type` và `status`.
3. Người dùng so sánh `provider_name`, `final_price` và `cancellation_policy`.
4. Người dùng mở `redirect_url` để tiếp tục với đơn vị cung cấp.

### Theo dõi chuyến đi

1. Người dùng bắt đầu chuyến đi từ `trips`.
2. Người dùng bật hoặc tắt `gps_consent`.
3. Hệ thống lưu vị trí vào `gps_location_events` khi có đồng ý.
4. Người dùng xem `itinerary_activities` và `itinerary_transits` trong ngày.
5. Người dùng có thể kết thúc chuyến đi sớm.

### Hỏi đáp và nghe thuyết minh

1. Người dùng gửi câu hỏi hoặc ảnh qua `messages` và `media_files`.
2. Người dùng xem thông tin nhận diện từ `places`.
3. Người dùng kiểm tra `information_sources.confidence`.
4. Người dùng chọn `place_narrations` đang hoạt động.
5. Người dùng nghe âm thanh hoặc đọc `transcript`.

### Xử lý cảnh báo chuyến đi

1. Người dùng nhận `trip_alerts` của chuyến đi.
2. Người dùng xem `severity`, `checked_at` và `confidence`.
3. Người dùng xem hoạt động bị ảnh hưởng và `alternative_proposal_id`.
4. Người dùng chấp nhận hoặc từ chối `itinerary_proposals`.
5. Người dùng đánh dấu cảnh báo đã xử lý.

### Viết và công khai đánh giá

1. Người dùng chọn một `places` đã ghé thăm.
2. Người dùng nhập `rating`, `comment` và ảnh `REVIEW_PHOTO`.
3. Người dùng lưu `place_reviews` ở trạng thái `PRIVATE`.
4. Người dùng yêu cầu công khai để chuyển trạng thái sang `PENDING`.
5. Người dùng xem bài đánh giá khi trạng thái là `PUBLIC`.

### Báo cáo và kiểm duyệt đánh giá

1. Người dùng chọn lý do trong `ReviewReportReason`.
2. Hệ thống tạo `review_reports` ở trạng thái `OPEN`.
3. `OPERATOR` hoặc `ADMIN` kiểm tra bài đánh giá.
4. Người kiểm duyệt chọn `APPROVE`, `REJECT`, `HIDE` hoặc `RESTORE`.
5. Hệ thống lưu kết quả vào `review_moderation_logs`.

### Tổng kết chuyến đi

1. Người dùng mở `trip_summaries` ở trạng thái `DRAFT`.
2. Người dùng kiểm tra các địa điểm `VISITED`, `SKIPPED` và `UNPLANNED`.
3. Người dùng chỉnh sửa `trip_summary_places` khi cần.
4. Người dùng nhập `trip_expenses`, `diary_notes` và `overall_rating`.
5. Người dùng có thể thêm ảnh `SUMMARY_PHOTO`.
6. Người dùng xác nhận để chuyển `trip_summaries` sang `CONFIRMED`.

### Bắt đầu chuyến đi tiếp theo

1. Người dùng xem 1–3 `next_trip_suggestions`.
2. Người dùng so sánh `suggested_places` và `estimated_budget`.
3. Người dùng chọn một gợi ý để tạo `agent_session` mới.
4. Hệ thống lưu phiên mới vào `started_agent_session_id`.

### Tra cứu nhật ký kỹ thuật

1. `OPERATOR` hoặc `ADMIN` tìm `agent_runs` theo chuyến đi, Agent, lỗi hoặc thời gian.
2. Người truy cập nhập `ticket_id` và `purpose`.
3. Hệ thống lưu lần truy cập vào `audit_access_logs`.
4. Người truy cập xem `decision_summary` và các `tool_calls`.
5. `ADMIN` xem quan hệ giữa `workflow_id` và `parent_run_id`.

### Quản trị địa điểm và kiến nghị

1. `ADMIN` quản lý `place_categories`, `places` và `place_narrations`.
2. `OPERATOR` tạo `operator_proposals` ở trạng thái `PENDING`.
3. `ADMIN` xem `proposed_payload` và nhập `admin_note`.
4. `ADMIN` chuyển trạng thái sang `APPROVED` hoặc `REJECTED`.
5. Hệ thống cập nhật `places` khi kiến nghị được duyệt.

### Quản trị tài khoản

1. `ADMIN` tìm người dùng theo `email`, `full_name`, `role` hoặc `status`.
2. `ADMIN` chuyển trạng thái giữa `ACTIVE`, `BANNED` và `DISABLED`.
3. `ADMIN` gán hoặc thu hồi vai trò `USER`, `OPERATOR` và `ADMIN`.

### Cấu hình hệ thống

1. `ADMIN` xem các tham số trong `system_configs`.
2. `ADMIN` sửa `config_value` theo `config_key`.
3. `ADMIN` lưu thay đổi.
4. Hệ thống cập nhật `updated_by` và `updated_at`.

## Câu hỏi cần chốt

1. Khi người dùng sửa một `trip_requests` đã ở trạng thái `CONFIRMED`, hệ thống tạo bản ghi mới với `version` và `parent_trip_request_id`, hay cập nhật bản ghi hiện có?

2. Với mỗi yêu cầu trong `trip_requests`, chỉ một lộ trình trong `itineraries` được ở trạng thái `SELECTED` và `trips.finalized_itinerary_id` phải trỏ đến lộ trình đó, đúng không?


3. Khi `itinerary_proposals.status` chuyển thành `accepted`, hệ thống tạo một `itineraries` mới theo `target_version` hay cập nhật lộ trình hiện tại?


4. Có cần giới hạn mỗi `trips.id` chỉ có một bản ghi `trip_summaries`, kể cả khi việc tạo bản tổng kết được chạy lại không?


5. Ảnh có `media_files.purpose` là `SUMMARY_PHOTO` được giữ cùng `trip_summaries` đã `CONFIRMED`, hay bị xóa sau 7 ngày như tệp media gốc?
