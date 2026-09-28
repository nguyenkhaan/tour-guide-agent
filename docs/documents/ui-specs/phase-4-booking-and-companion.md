# Ý Tưởng Giao Diện: Phase 4 — Gợi Ý Dịch Vụ & Đồng Hành Trong Chuyến Đi

Nhóm màn hình này hỗ trợ người dùng tìm kiếm các dịch vụ lưu trú & di chuyển phù hợp với lịch trình đã chốt, chuyển hướng trực tiếp sang trang đặt chỗ chính thức của nhà cung cấp, và đóng vai trò là "người bạn đồng hành thông minh" trong suốt chuyến đi (`SCR-12`, `SCR-14` đến `SCR-16`).

---

## 1. Màn Hình SCR-12: Gợi Ý Dịch Vụ Lưu Trú & Di Chuyển (Booking Services & Direct Redirect)

### 1.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Trình bày danh sách các gợi ý khách sạn, vé xe, chuyến bay phù hợp nhất với lịch trình đã chọn. Khi người dùng ưng ý dịch vụ nào, chỉ cần bấm nút là hệ thống **mở trực tiếp trang web chính thức của nhà cung cấp dịch vụ đó (trong tab mới)** để người dùng tự do đặt phòng/vé và thanh toán.
- **Mục tiêu:** Trải nghiệm chuyển tiếp nhanh gọn, trực diện, không có màn hình trung gian hay biểu mẫu sao chép dữ liệu rườm rà.

### 1.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| GỢI Ý DỊCH VỤ LƯU TRÚ & DI CHUYỂN CHO CHUYẾN ĐI                   [Bỏ qua bước này]|
| Lịch trình: Đà Lạt Thư Giãn (15/10 - 17/10/2026)                                  |
+-----------------------------------------------------------------------------------+
| [ TAB: DỊCH VỤ KHÁCH SẠN (3) ]         [ TAB: DỊCH VỤ XE LIMOUSINE (2) ]          |
+-----------------------------------------------------------------------------------+
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [Ảnh phòng] KHÁCH SẠN COLLINE ĐÀ LẠT (4★)              [PHÙ HỢP NHẤT - 96%]    | |
| | * Vị trí: Đường Phan Bội Châu, Phường 1 (Gần Chợ Đà Lạt, đi bộ ra Hồ Xuân Hương)|
| | * Loại phòng: Deluxe King (Kèm bữa sáng buffet cho 2 người lớn + 1 bé)          | |
| | * Chính sách: [V] Miễn phí hủy phòng trước ngày 13/10                           | |
| | * Giá trọn gói: 1.850.000 VNĐ / 2 đêm (Đã bao gồm thuế phí)                    | |
| |                                                                               | |
| | [ ĐẶT PHÒNG TRÊN AGODA (Mở tab mới) >> ]   [ So sánh giá với các bên khác v ]  | |
| +-----------------------------------------------+-------------------------------+ |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [Ảnh phòng] TERRACOTTA RESORT & SPA (4★)               [KHÔNG GIAN YÊN TĨNH]   | |
| | * Vị trí: Khu du lịch Hồ Tuyền Lâm (Có sân chơi cỏ rộng và hồ bơi nước ấm)      | |
| | * Tiện ích: Phòng hướng vườn, xe đưa đón trung tâm miễn phí                     | |
| | * Chính sách: [!] Không hoàn tiền nếu hủy phòng                                 | |
| | * Giá trọn gói: 2.100.000 VNĐ / 2 đêm                                          | |
| |                                                                               | |
| | [ ĐẶT PHÒNG TRÊN BOOKING.COM (Mở tab mới) >> ] [ So sánh giá với các bên khác v]|
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
| (i) Bạn sẽ được chuyển hướng trực tiếp sang trang chính thức của nhà cung cấp     |
|     để hoàn tất đặt chỗ và thanh toán. Ứng dụng không thu tiền hay giữ tiền.     |
+-----------------------------------------------------------------------------------+
```

### 1.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `booking_offers`**:
  - Loại dịch vụ $\rightarrow$ `booking_offers.offer_type` (`HOTEL`, `FLIGHT`, `TRANSPORT`, `ACTIVITY`)
  - Trạng thái chỗ trống $\rightarrow$ `booking_offers.status` (`AVAILABLE`, `STALE`, `UNAVAILABLE`)
  - Tên dịch vụ & Tiện ích $\rightarrow$ `booking_offers.title`, `booking_offers.description`
  - Đơn vị cung cấp $\rightarrow$ `booking_offers.provider_name` (Ví dụ: "Agoda", "Booking.com", "Vexere")
  - Mức độ phù hợp với lịch trình $\rightarrow$ `booking_offers.match_score`
  - Giá cuối cùng & Tiền tệ $\rightarrow$ `booking_offers.final_price`, `booking_offers.currency`
  - Chính sách hủy phòng/vé $\rightarrow$ `booking_offers.cancellation_policy` (TEXT)
  - **Đường dẫn chuyển tiếp trực tiếp** $\rightarrow$ `booking_offers.redirect_url` (Mở trực tiếp liên kết này khi click)
  - Thời hạn ưu đãi $\rightarrow$ `booking_offers.expires_at`

---

## 2. Màn Hình SCR-14: Bảng Điều Khiển Chuyến Đi Đang Diễn Ra (Active Trip Dashboard)

### 2.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Màn hình chính trong suốt những ngày đi du lịch; đóng vai trò như một "người quản gia hành trình", nhắc nhở giờ giấc, cập nhật thời tiết và sẵn sàng hỗ trợ tại chỗ.
- **Mục tiêu:** Giúp người dùng theo dõi tiến độ chuyến đi và dễ dàng bật/tắt định vị GPS theo ý muốn.

### 2.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| CHUYẾN ĐI ĐANG DIỄN RA: ĐÀ LẠT (NGÀY 1 / 3)              [ KẾT THÚC CHUYẾN SỚM ]  |
+-----------------------------------------------------------------------------------+
| [TRẠNG THÁI ĐỊNH VỊ GPS & QUYỀN RIÊNG TƯ]                                         |
| * Tự động nhận diện điểm đến gần bạn: [ BẬT (Công tắc) ]                          |
| * Dữ liệu vị trí chỉ dùng để phát thuyết minh và sẽ tự động xóa sau 7 ngày.       |
+-----------------------------------------------------------------------------------+
| (LỊCH TRÌNH HÔM NAY - 15/10/2026 | Thời tiết: 22°C Nắng nhẹ, rất mát mẻ)          |
|                                                                                   |
| [12:00] [V] ĐÃ ĐẾN: Khách sạn Colline Đà Lạt (Đã nhận phòng)                      |
|                                                                                   |
| [14:30] [*] ĐANG Ở ĐÂY: Nông trại Cún Puppy Farm                                  |
|         -> Bạn đang cách điểm tham quan này khoảng 50m                            |
|         -> [ Xem mẹo vui chơi tại đây ]  [ (Audio) Nghe giới thiệu điểm này ]     |
|                                                                                   |
| [17:30] [ ] SẮP TỚI: Ngắm hoàng hôn tại Tiệm cà phê Hoàng Hôn                     |
|         -> Nhắc nhở: Trời chiều Đà Lạt se lạnh, bạn nhớ mang áo khoác ấm cho bé   |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [ HỎI ĐÁP TẠI CHỖ ]: Bạn cần tìm quán ăn ngon gần đây hoặc hỏi thêm thông tin?  | |
| | [ Nhập câu hỏi...                                     ] [Gửi ảnh] [HỎI AI]     | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 2.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `trips`**:
  - Trạng thái chuyến đi $\rightarrow$ `trips.status` (Đang diễn ra)
  - Đồng ý chia sẻ định vị $\rightarrow$ `trips.gps_consent` (BOOLEAN)
  - Ngày bắt đầu thực tế $\rightarrow$ `trips.actual_start_date`
  - Lộ trình đã chốt $\rightarrow$ `trips.finalized_itinerary_id`
- **Bảng `gps_location_events`**:
  - Điểm GPS gửi lên $\rightarrow$ `gps_location_events.location`, `accuracy_meters`, `recorded_at`
  - Hạn tự động xóa $\rightarrow$ `gps_location_events.expires_at` (Tối đa 7 ngày)

---

## 3. Màn Hình SCR-15: Hỏi Đáp Tại Chỗ & Nhận Diện Ảnh Phong Cảnh (On-site Place Q&A)

### 3.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Khi đứng trước một bức tượng, cổng đền hay món ăn lạ, người dùng chỉ cần chụp ảnh và hỏi: *"Đây là gì?"*, AI sẽ giải thích ngay lập tức.
- **Mục tiêu:** Mang lại trải nghiệm khám phá sống động và nhiều kiến thức bổ ích.

### 3.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| < Quay lại chuyến đi | TRỢ LÝ HỎI ĐÁP TẠI CHỖ                                     |
+-----------------------------------------------------------------------------------+
| [Bạn]: (Gửi ảnh chụp một bức tượng gỗ trong khuôn viên)                           |
|        "Tượng này tên là gì và có ý nghĩa gì vậy trợ lý?"           [14:45 PM]    |
|                                                                                   |
| [Trợ lý AI - Đã nhận diện hình ảnh (Độ tin cậy 92%)]:                             |
| * Đây là Tượng Thần Nông Tây Nguyên tại nông trại Puppy Farm.                     |
| * Câu chuyện thú vị:                                                              |
|   Bức tượng được các nghệ nhân địa phương tạc từ thân cây thông cổ thụ nhằm tôn   |
|   vinh tinh thần lao động cần cù của người dân vùng đất cao nguyên trồng dâu tây. |
|                                                                                   |
| (?) Hoạt động gợi ý gần vị trí này:                                               |
|   - Gian hàng cho bé trải nghiệm hái dâu tây hữu cơ (cách 30m)                    |
|   - Quầy thưởng thức sữa chua dâu tươi                                            |
|                                                                     [14:46 PM]    |
|                                                                                   |
| [ Nghe đọc thuyết minh giọng Nam Bộ ]     [ Hữu ích: (Thích) (Chưa đúng) ]        |
|                                                                                   |
| [ Chụp ảnh khác... ] [ Nhập câu hỏi thắc mắc...                           ] [GỬI] |
+-----------------------------------------------------------------------------------+
```

### 3.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `places`**:
  - Đặc điểm ảnh đối chiếu $\rightarrow$ `places.visual_attributes` (JSONB)
  - Thông tin mô tả địa điểm $\rightarrow$ `places.description`
- **Bảng `information_sources`**:
  - Độ tin cậy nhận diện $\rightarrow$ `information_sources.confidence`

---

## 4. Màn Hình SCR-16: Trình Phát Thuyết Minh Tự Động (Audio Guide & Transcript)

### 4.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Tự động như có một người thuyết minh viên đi cạnh: Khi người dùng bước đến gần di tích, ứng dụng nhẹ nhàng gợi ý phát giọng đọc kể về lịch sử điểm đến đó.
- **Mục tiêu:** Cung cấp trình phát âm thanh dễ dùng (Play/Pause/Tua lại) kèm phụ đề chạy chữ đồng bộ.

### 4.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| [Thuyết minh tự động] BẠN ĐANG ĐỨNG TẠI: GA XE LỬA ĐÀ LẠT          [ Thu nhỏ v ]  |
| (Khoảng cách: 20 mét | Thời lượng câu chuyện: 02 phút 30 giây)                    |
+-----------------------------------------------------------------------------------+
| [========================>                                ] 01:10 / 02:30         |
|                                                                                   |
|                   [ << 10s ]   [ (TẠM DỪNG) ]   [ 10s >> ]   [ Tốc độ: 1.0x v ]   |
|                                                                                   |
| [LỜI THUYẾT MINH CHẠY CHỮ ĐỒNG BỘ]:                                               |
| "...Nhà ga xe lửa Đà Lạt được xây dựng từ những năm 1932, mang phong cách kiến    |
| trúc Art Deco độc đáo kết hợp cùng hình tượng ba mái chóp nhọn mô phỏng đỉnh núi  |
| Langbiang huyền thoại..."                                                         |
|                                                                                   |
| [x] Tự động cuộn theo giọng đọc      [ Nghe lại từ đầu ]      [ Tắt âm thanh ]    |
+-----------------------------------------------------------------------------------+
```

### 4.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `place_narrations`**:
  - Tiêu đề bài thuyết minh $\rightarrow$ `place_narrations.title`
  - File âm thanh giọng đọc $\rightarrow$ `place_narrations.audio_object_key`
  - Lời bình chạy chữ $\rightarrow$ `place_narrations.transcript` (TEXT)
  - Thời lượng âm thanh $\rightarrow$ `place_narrations.duration_seconds`
  - Trạng thái hoạt động $\rightarrow$ `place_narrations.is_active`
