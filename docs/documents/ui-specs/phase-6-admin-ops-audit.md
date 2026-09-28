# Ý Tưởng Giao Diện: Phase 6 — Quản Trị Vận Hành & Giám Sát An Ninh

Nhóm màn hình này dành riêng cho **Nhân viên vận hành (Operator)** và **Quản trị viên (Admin)** để duy trì dữ liệu địa điểm & toàn bộ dịch vụ du lịch (lưu trú, ăn uống, di chuyển), phê duyệt kiến nghị cập nhật (Maker–Checker), hỗ trợ người dùng khi gặp sự cố và điều chỉnh các tham số hệ thống (`SCR-24` đến `SCR-29`).

---

## 1. Màn Hình SCR-24 & SCR-25: Tra Cứu Sự Cố & Cổng Kiểm Soát Hỗ Trợ (Audit & Ticket Gate)

### 1.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Khi người dùng phản ánh chuyến đi gặp trục trặc, nhân viên kỹ thuật cần xem lại lịch sử AI đã tư vấn những gì. Tuy nhiên, để đảm bảo quyền riêng tư, nhân viên bắt buộc phải nhập mã Ticket hỗ trợ trước khi mở xem.
- **Mục tiêu:** Minh bạch hóa quy trình hỗ trợ khách hàng, ngăn chặn việc nhân viên xem lén dữ liệu riêng tư mà không có lý do chính đáng.

### 1.2. Phác Thảo Cửa Sổ Nhập Lý Do (SCR-25: Ticket Gate Modal)
```text
+-----------------------------------------------------------------------------------+
| [!] XÁC THỰC MỤC ĐÍCH TRUY CẬP DỮ LIỆU HỖ TRỢ                         [ Đóng (X) ]|
+-----------------------------------------------------------------------------------+
| Bạn đang yêu cầu mở xem chi tiết lịch sử tư vấn AI của chuyến đi #TRIP-5510.      |
| Để bảo vệ quyền riêng tư của du khách, vui lòng xác nhận mục đích của bạn:        |
|                                                                                   |
| * Mã Phiếu Hỗ Trợ Sự Cố (Ticket ID - Bắt buộc):                                  |
|   [ TICKET-2026-0928-8812                                                       ] |
|                                                                                   |
| * Lý do tra cứu cụ thể:                                                           |
|   [ Khách phản ánh AI gợi ý quán ăn đã đóng cửa, cần kiểm tra nguồn dữ liệu     ] |
|                                                                                   |
| (i) Hoạt động mở xem này sẽ được lưu lại vĩnh viễn trong Nhật ký An ninh hệ thống.|
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| |                    [ XÁC NHẬN MỞ XEM ĐỂ HỖ TRỢ DU KHÁCH ]                     | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 1.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `audit_access_logs`**:
  - Người truy cập $\rightarrow$ `audit_access_logs.actor_id`
  - Người dùng mục tiêu $\rightarrow$ `audit_access_logs.target_user_id`
  - Mã Ticket hỗ trợ $\rightarrow$ `audit_access_logs.ticket_id`
  - Mục đích tra cứu $\rightarrow$ `audit_access_logs.purpose`
  - Địa chỉ IP & Thiết bị $\rightarrow$ `audit_access_logs.client_ip`, `audit_access_logs.user_agent`, `accessed_at`
- **Bảng `agent_runs` & `tool_calls`**:
  - Vết thực thi của AI $\rightarrow$ `agent_runs.input_summary`, `agent_runs.output_summary`, `agent_runs.decision_summary`
  - Danh sách tool đã gọi $\rightarrow$ `tool_calls.tool_name`, `tool_calls.arguments`, `tool_calls.result`, `tool_calls.status` (`SUCCEEDED`, `FAILED`)

---

## 2. Màn Hình SCR-26: Quản Trị Kho Địa Điểm & Dịch Vụ Du Lịch Toàn Diện (Places & Travel Services Admin)

### 2.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Một trung tâm điều hành dữ liệu du lịch đa năng cho Quản trị viên (Admin), bao quát trọn vẹn cả **Điểm tham quan / Danh lam thắng cảnh** lẫn **Hệ sinh thái dịch vụ du lịch (Khách sạn/Lưu trú, Nhà hàng/Ẩm thực, Nhà xe/Di chuyển)** và các bài thuyết minh âm thanh (Audio Guide).
- **Mục tiêu:** Quản trị viên dễ dàng chuyển đổi qua lại giữa các loại hình dịch vụ, cập nhật bảng giá, giờ mở cửa, liên kết đặt chỗ đối tác và ẩn/hiện các địa điểm tạm dừng hoạt động.

### 2.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| QUẢN TRỊ KHO ĐỊA ĐIỂM & DỊCH VỤ DU LỊCH                       [ + THÊM DỮ LIỆU MỚI]|
+-----------------------------------------------------------------------------------+
| [ TAB: ĐIỂM THAM QUAN (120) ]  [ TAB: KHÁCH SẠN / LƯU TRÚ (45) ]                  |
| [ TAB: NHÀ HÀNG / QUÁN CAFE (80) ]  [ TAB: VÉ XE / DI CHUYỂN (25) ]  [ DANH MỤC ] |
+-----------------------------------------------------------------------------------+
| [Tìm kiếm theo tên...             ] [Tỉnh/TP: Lâm Đồng v] [Trạng thái: Đang mở v] |
+-----------------------------------------------------------------------------------+
| (HIỂN THỊ THEO TAB ĐANG CHỌN):                                                    |
|                                                                                   |
| 1. NẾU Ở TAB "ĐIỂM THAM QUAN / DANH LAM THẮNG CẢNH":                              |
| TÊN ĐIỂM ĐẾN & VỊ TRÍ  | GIỜ MỞ CỬA     | GIÁ VÉ THAM KHẢO | AUDIO GUIDE | THAO TÁC|
| Puppy Farm Đà Lạt      | 07:30 - 17:30  | 100.000 VNĐ      | [ Có audio ]| [Sửa][Ẩn]|
| Tiệm cà phê Hoàng Hôn  | 07:00 - 22:00  | Miễn phí (Nước)  | [ Chưa có ] | [Sửa][Ẩn]|
|                                                                                   |
| --------------------------------------------------------------------------------- |
| 2. NẾU Ở TAB "DỊCH VỤ KHÁCH SẠN / LƯU TRÚ":                                       |
| TÊN KHÁCH SẠN / RESORT | HẠNG SAO / LOẠI| KHOẢNG GIÁ PHÒNG | ĐỐI TÁC LIÊN KẾT     |
| Khách sạn Colline ĐL   | 4★ - Trung tâm | 1.2tr - 2.5tr/đêm| Agoda, Booking.com   |
| Terracotta Resort      | 4★ - Hồ Tuyền L| 1.8tr - 4.5tr/đêm| Booking.com Partner  |
|                                                                                   |
| --------------------------------------------------------------------------------- |
| 3. NẾU Ở TAB "DỊCH VỤ VÉ XE / DI CHUYỂN":                                         |
| NHÀ XE / HÃNG VẬN TẢI  | TUYẾN ĐƯỜNG    | LOẠI XE          | GIÁ VÉ NIÊM YẾT      |
| Limousine Thành Bưởi   | Sài Gòn - ĐL   | Giường nằm VIP   | 320.000 VNĐ / vé     |
| Xe VIP An Anh          | Sài Gòn - ĐL   | Phòng đôi Cung Đ | 450.000 VNĐ / vé     |
+-----------------------------------------------------------------------------------+
```

### 2.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `place_categories`**: Quản lý các nhóm phân loại dịch vụ (`slug = 'sightseeing'`, `'lodging'`, `'restaurant'`, `'cafe'`, `'transport'`).
- **Bảng `places`**: Quản lý dữ liệu chung của địa điểm/cơ sở dịch vụ:
  - Tên cơ sở $\rightarrow$ `places.name`
  - Địa chỉ & Tỉnh thành $\rightarrow$ `places.address`, `places.province`
  - Tọa độ bản đồ $\rightarrow$ `places.location` (PostGIS Point 4326)
  - Giờ mở cửa/nhận phòng $\rightarrow$ `places.opening_hours` (JSONB)
  - Khoảng giá $\rightarrow$ `places.min_price`, `places.max_price`, `places.currency`
  - Trạng thái hoạt động $\rightarrow$ `places.is_active` (Bật/Ẩn)
- **Bảng `booking_offers`**: Quản lý thông tin liên kết đặt chỗ cho khách sạn và vé xe (`provider_name`, `redirect_url`, `final_price`, `cancellation_policy`).
- **Bảng `place_narrations`**: Quản lý tệp thuyết minh âm thanh (`place_narrations.audio_object_key`, `place_narrations.transcript`, `place_narrations.duration_seconds`).

---

## 3. Màn Hình SCR-27: Bảng Kiến Nghị Vận Hành Maker–Checker (Operator Proposals)

### 3.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Cơ chế "2 người kiểm tra" (Maker - Checker): Nhân viên ngoài thực địa (*Operator*) khi phát hiện thông tin mới về địa điểm hoặc dịch vụ (ví dụ: khách sạn đổi giá, đường đèo sạt lở) sẽ gửi đề xuất; Quản trị viên (*Admin*) kiểm tra giấy tờ/nguồn tin rồi mới bấm duyệt để đưa lên hệ thống chính.
- **Mục tiêu:** Đảm bảo kho dữ liệu luôn chính xác 100%, tránh sai sót do một cá nhân tự ý thay đổi.

### 3.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| DUYỆT KIẾN NGHỊ CẬP NHẬT THÔNG TIN ĐỊA ĐIỂM & DỊCH VỤ (Maker - Checker)          |
+-----------------------------------------------------------------------------------+
| Kiến nghị #PROP-102 | Người gửi: Nhân viên @linh_ops | Ngày gửi: 28/09/2026       |
| Địa điểm/Dịch vụ mục tiêu: Thác Cam Ly - TP. Đà Lạt                               |
| Loại kiến nghị: [ CẬP NHẬT ĐỊA ĐIỂM (PLACE_UPDATE) ]                              |
|                                                                                   |
| [NỘI DUNG ĐỐI CHIẾU THAY ĐỔI]:                                                    |
| - Hiện tại trên hệ thống: Đang mở cửa bình thường (07:00 - 17:00)                 |
| - Đề xuất cập nhật mới:   TẠM ĐÓNG CỬA BẢO TRÌ SỬA CHỮA ĐẾN HẾT 30/10/2026       |
| - Căn cứ chứng minh:      Thông báo chính thức số 12 của Ban Quản Lý Khu Du Lịch  |
|                                                                                   |
| Ghi chú của Quản trị viên khi duyệt (Bắt buộc):                                   |
| [ Đã kiểm tra văn bản của BQL, thông tin chuẩn xác. Đồng ý cập nhật ngay.       ] |
|                                                                                   |
| +------------------------------------+     +------------------------------------+ |
| |   [V] PHÊ DUYỆT & CẬP NHẬT NGAY    |     |      [X] TỪ CHỐI KIẾN NGHỊ         | |
| +------------------------------------+     +------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 3.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `operator_proposals`**:
  - Người đề xuất $\rightarrow$ `operator_proposals.operator_id`
  - Loại kiến nghị $\rightarrow$ `operator_proposals.proposal_type` (`PLACE_UPDATE`, `WEATHER_REPORT`, `AI_ISSUE`)
  - Địa điểm mục tiêu $\rightarrow$ `operator_proposals.target_place_id`
  - Tiêu đề & Mô tả $\rightarrow$ `operator_proposals.title`, `operator_proposals.description`
  - Nội dung đề xuất $\rightarrow$ `operator_proposals.proposed_payload` (JSONB)
  - Trạng thái duyệt $\rightarrow$ `operator_proposals.status` (`PENDING`, `APPROVED`, `REJECTED`)
  - Quản trị viên duyệt & Ghi chú $\rightarrow$ `operator_proposals.admin_id`, `operator_proposals.admin_note`, `reviewed_at`

---

## 4. Màn Hình SCR-28: Quản Trị Người Dùng & Phân Quyền (User Management)

### 4.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Mục tiêu:** Dành cho Quản trị viên theo dõi danh sách thành viên, khóa các tài khoản spam quảng cáo hoặc cấp quyền Nhân viên vận hành cho tài khoản mới.

### 4.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| QUẢN TRỊ TÀI KHOẢN NGƯỜI DÙNG                                                     |
+-----------------------------------------------------------------------------------+
| [Tìm email, tên người dùng...     ] [Vai trò: Tất cả v] [Trạng thái: Hoạt động v] |
+-----------------------------------------------------------------------------------+
| EMAIL / HỌ TÊN         | VAI TRÒ HIỆN TẠI | TRẠNG THÁI   | THAO TÁC XỬ LÝ         |
+------------------------+------------------+--------------+------------------------+
| linh.ops@tourguide.vn  | NHÂN VIÊN        | [ Hoạt động] | [Thu hồi quyền]        |
| (Nguyễn Thị Linh)      | (Operator)       |              | [Tạm khóa tài khoản]   |
+------------------------+------------------+--------------+------------------------+
| spammer99@badmail.com  | NGƯỜI DÙNG       | [ ĐÃ KHÓA ]  | [Mở khóa lại]          |
| (Tài khoản spam)       | (User)           |              |                        |
+-----------------------------------------------------------------------------------+
```

### 4.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `users`**:
  - Quản trị danh sách người dùng $\rightarrow$ `users.email`, `users.full_name`
  - Cập nhật trạng thái $\rightarrow$ `users.status` (`ACTIVE`, `BANNED`, `DISABLED`)
  - Gán/thu hồi quyền $\rightarrow$ `users.role` (`USER`, `OPERATOR`, `ADMIN`)

---

## 5. Màn Hình SCR-29: Cấu Hình Tham Số Hoạt Động Của Hệ Thống (System Settings)

### 5.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Một bảng điều khiển cho phép Quản trị viên tùy chỉnh các cài đặt quan trọng của hệ thống một cách trực quan mà không làm gián đoạn người dùng đang sử dụng.
- **Mục tiêu:** Dễ dàng điều chỉnh tần suất quét thời tiết, số ngày lưu dữ liệu tạm và số lượng phương án lịch trình AI tạo ra.

### 5.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| CẤU HÌNH THAM SỐ HOẠT ĐỘNG CỦA TRỢ LÝ AI                                          |
| Các thay đổi tại đây sẽ có hiệu lực ngay lập tức cho các chuyến đi tiếp theo      |
+-----------------------------------------------------------------------------------+
|                                                                                   |
| [1. Tần suất kiểm tra thời tiết & sự cố ngầm]                                     |
| Quét thông tin thời tiết tự động mỗi: [ 30 ] Phút một lần (Gợi ý: 15 - 60 phút)   |
|                                                                                   |
| [2. Thời gian tự động dọn dẹp dữ liệu tạm thời (Quyền riêng tư)]                  |
| Tự động xóa dữ liệu định vị GPS và ảnh chụp sau: [ 7 ] Ngày                       |
|                                                                                   |
| [3. Số lượng phương án lịch trình tối đa]                                         |
| Số phương án lộ trình AI tạo ra để người dùng so sánh: [ 2 ] Phương án (Tối đa 4) |
|                                                                                   |
| Cập nhật lần cuối: 28/09/2026 bởi Quản trị viên @hoangthai                        |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| |                         [ LƯU THAY ĐỔI CẤU HÌNH ]                             | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 5.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `system_configs`**:
  - Mã cấu hình $\rightarrow$ `system_configs.config_key` (Ví dụ: `weather_monitor_interval_minutes`, `temporary_data_retention_days`, `max_itinerary_alternatives`)
  - Giá trị cấu hình $\rightarrow$ `system_configs.config_value` (JSONB)
  - Mô tả & Người cập nhật $\rightarrow$ `system_configs.description`, `system_configs.updated_by`, `system_configs.updated_at`
