# Ý Tưởng Giao Diện: Phase 2 — Tiếp Nhận Nhu Cầu & Khám Phá Địa Điểm

Nhóm màn hình này là nơi người dùng trò chuyện tự nhiên với AI để định hình chuyến đi, xem lại bản tóm tắt yêu cầu và tự do khám phá các điểm đến tại Việt Nam (`SCR-04` đến `SCR-07`).

---

## 1. Màn Hình SCR-04: Hội Thoại Lập Kế Hoạch Với AI (Conversational Planning)

### 1.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Trải nghiệm như đang nói chuyện với một hướng dẫn viên du lịch người bản địa thân thiện, am hiểu và chu đáo.
- **Mục tiêu:** Người dùng thoải mái gõ mô tả chuyến đi, gửi hình ảnh cảnh đẹp mình thích hoặc gửi vị trí hiện tại; AI sẽ tự động phân tích và hỏi lại nhẹ nhàng những thông tin còn thiếu.

### 1.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| < Quay lại | Lập kế hoạch chuyến đi mới                     [Bản Tóm Tắt (3 mục)] |
+-----------------------------------------------------------------------------------+
| (Khu vực dòng chảy tin nhắn - Tin nhắn xuất hiện mượt mà từng chữ)                 |
|                                                                                   |
| [Trợ lý AI]: Chào bạn! Bạn đang dự định có một chuyến đi như thế nào? Cứ chia sẻ  |
|              tự nhiên nhé!                                          [10:00 AM]    |
|                                                                                   |
| [Bạn]: Mình muốn đi Đà Lạt 3 ngày 2 đêm vào cuối tuần sau cùng 2 người lớn và 1 bé |
|        4 tuổi, ngân sách tầm 8 triệu từ Sài Gòn.                                  |
|                                                                     [10:01 AM]    |
|                                                                                   |
| [Trợ lý AI - Đang lắng nghe & ghi chú...]:                                        |
| * Tuyệt vời! Tôi đã ghi nhận sơ bộ:                                               |
|   - Điểm đến: Đà Lạt | Xuất phát: TP.HCM | Thời gian: 3N2Đ                        |
|   - Thành viên: 2 người lớn + 1 bé 4 tuổi | Ngân sách: ~8.000.000đ                |
|                                                                                   |
| (?) Để chuyến đi hoàn hảo nhất cho bé, bạn cho tôi hỏi thêm xíu nhé:              |
|   1. Bạn thích đi xe giường nằm cao cấp hay bay thẳng lên Liên Khương?            |
|   2. Gia đình có thích ghé các nông trại cún/cừu cho bé chơi không?               |
|                                                                     [10:01 AM]    |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | (Gợi ý trả lời nhanh): [ Đi Xe giường nằm ] [ Đi Máy bay ] [ Thích nông trại ]| |
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
| [ [+] Gửi ảnh phong cảnh ] [ (GPS) Gửi vị trí ] [ Nhập tin nhắn...        ] [GỬI] |
| (i) Ảnh và vị trí của bạn chỉ dùng để hỗ trợ chuyến đi và tự động xóa sau 7 ngày  |
+-----------------------------------------------------------------------------------+
```

### 1.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `messages`**:
  - Nội dung tin nhắn chat $\rightarrow$ `messages.content`
  - Vai trò tin nhắn $\rightarrow$ `messages.role` (`user`, `assistant`)
  - Lần chạy Agent tạo tin nhắn $\rightarrow$ `messages.agent_run_id`
- **Bảng `media_files`**:
  - Ảnh phong cảnh tải lên $\rightarrow$ `media_files.object_key`, `media_files.file_name`, mục đích `purpose = MediaImage.REQUEST_IMAGE`
- **Bảng `agent_session`**:
  - Phiên làm việc $\rightarrow `agent_session.id`, `agent_session.status` (`ACTIVE`)

---

## 2. Màn Hình SCR-05: Bản Tóm Tắt Yêu Cầu Chuyến Đi (Trip Request Summary)

### 2.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Một "tờ phiếu thông tin chuyến đi" gọn gàng, rõ ràng, giúp người dùng rà soát lại toàn bộ những gì mình và AI đã thống nhất trước khi bấm tạo lịch trình.
- **Mục tiêu:** Cho phép xem nhanh, chỉnh sửa trực tiếp các ô thông tin và cảnh báo nếu còn thiếu yếu tố bắt buộc (như ngày đi, ngân sách).

### 2.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| BẢN TÓM TẮT YÊU CẦU CHUYẾN ĐI (Bản nháp v2)                    [Trò chuyện tiếp]  |
| Vui lòng kiểm tra lại thông tin trước khi AI tiến hành thiết kế lịch trình        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
| [THÔNG TIN CỐT LÕI]                                                               |
| * Nơi xuất phát:  [ TP. Hồ Chí Minh                             (Chỉnh sửa) ]     |
| * Ngày khởi hành: [ 15/10/2026               ] Đến ngày: [ 17/10/2026       ]     |
| * Tổng ngân sách: [ 8.000.000 VNĐ                               (Chỉnh sửa) ]     |
|                                                                                   |
| [THÀNH VIÊN ĐI CÙNG]                                                              |
| * Số lượng: 3 người ([2] Người lớn, [1] Trẻ em 4 tuổi)                            |
| * Ghi chú: Bé dễ mệt khi đi đường đèo dốc, cần thời gian nghỉ ngơi giữa chặng     |
|                                                                                   |
| [ĐIỂM ĐẾN & SỞ THÍCH ƯU TIÊN]                                                     |
| * Phong cách: Quán cà phê view đẹp, Nông trại trải nghiệm, Ẩm thực ấm nóng        |
| * Địa điểm bạn đã chọn trước (2 điểm):                                            |
|   1. Tiệm cà phê Hoàng Hôn - Đà Lạt [Xóa]                                         |
|   2. Puppy Farm Đà Lạt [Xóa]                                                      |
|   [+ Thêm địa điểm khác từ bản đồ khám phá]                                       |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | (i) Đánh giá sơ bộ: Ngân sách 8 triệu cho gia đình 3 người tại Đà Lạt là        | |
| |     [Rất hợp lý và thoải mái] cho lịch trình 3 ngày 2 đêm.                      | |
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
| +------------------------------------+     +------------------------------------+ |
| |   XÁC NHẬN & TẠO LỊCH TRÌNH NGAY   |     | QUAY LẠI ĐỂ SỬA THÊM               | |
| +------------------------------------+     +------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 2.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `trip_requests`**:
  - Điểm xuất phát & Tọa độ $\rightarrow$ `trip_requests.origin_name`, `trip_requests.origin_location`
  - Điểm đến mong muốn $\rightarrow$ `trip_requests.destination_text`
  - Ngày khởi hành & Số ngày $\rightarrow$ `trip_requests.start_date`, `trip_requests.duration_days`
  - Tổng ngân sách & Tiền tệ $\rightarrow$ `trip_requests.budget`, `trip_requests.currency`
  - Thành viên đi cùng $\rightarrow$ `trip_requests.companions_count`, `trip_requests.companions_info` (JSONB)
  - Sở thích riêng $\rightarrow$ `trip_requests.preferences` (JSONB)
  - Số phiên bản & Trạng thái $\rightarrow$ `trip_requests.version`, `trip_requests.status` (`DRAFT` khi tạo nháp $\rightarrow$ `CONFIRMED` khi người dùng bấm xác nhận tóm tắt $\rightarrow$ `PLANNING` khi AI thực thi $\rightarrow$ `PLANNED` khi hoàn tất đề xuất $\rightarrow$ `CANCELLED` nếu hủy)
  - Thời điểm xác nhận $\rightarrow$ `trip_requests.confirmed_at`
- **Bảng `trip_request_selected_places`**:
  - Danh sách địa điểm đã chọn trước $\rightarrow$ `trip_request_selected_places.place_id`, `selection_status`, `selection_reason`

---

## 3. Màn Hình SCR-06: Khám Phá Địa Điểm Du Lịch (Destination Discovery)

### 3.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Kết hợp linh hoạt giữa chế độ xem **Danh sách dạng thẻ ảnh** và **Bản đồ tương tác**, giúp người dùng hình dung địa điểm một cách trực quan nhất.
- **Mục tiêu:** Hỗ trợ tìm kiếm theo từ khóa, lọc theo bán kính quanh vị trí đang đứng, hoặc tìm điểm đến có cảnh quan tương tự như bức ảnh người dùng tải lên.

### 3.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| [Tìm: Quán cà phê, đồi chè...   ] [Tỉnh/TP: Lâm Đồng v] [Bán kính: 10km v] [Lọc v]|
+---------------------------------------------------+-------------------------------+
| (DANH SÁCH GỢI Ý ĐỊA ĐIỂM)                        | (BẢN ĐỒ DU LỊCH TRỰC QUAN)   |
|                                                   |                               |
| +-----------------------------------------------+ |       [ (1) ]                 |
| | [Ảnh đẹp] TIỆM CÀ PHÊ HOÀNG HÔN               | |                 [ (2) ]       |
| | * Lý do hợp bạn: Có view ngắm cảnh, gần KS    | |    [ (3) ]                    |
| | * Đánh giá: 4.8★ (128 nhận xét đã kiểm duyệt) | |                               |
| | * Giá tham khảo: 50.000đ - 90.000đ            | |  * Vị trí của bạn:            |
| |                                               | |    (Tâm tìm kiếm: 10km)       |
| | [x] ĐÃ CHỌN VÀO CHUYẾN ĐI   [Xem chi tiết >>] | |                               |
| +-----------------------------------------------+ | [ + Phóng to ] [ - Thu nhỏ ]  |
|                                                   | [ (O) Quay lại vị trí của tôi]|
| +-----------------------------------------------+ |                               |
| | [Ảnh đẹp] NÔNG TRẠI CÚN PUPPY FARM            | |                               |
| | * Lý do hợp bạn: Rất thích hợp cho bé 4 tuổi  | |                               |
| | * Đánh giá: 4.6★ (95 nhận xét)                | |                               |
| | * Vé vào cổng: 100.000đ / người               | |                               |
| |                                               | |                               |
| | [ + CHỌN ĐỊA ĐIỂM NÀY ]     [Xem chi tiết >>] | |                               |
| +-----------------------------------------------+ |                               |
+---------------------------------------------------+-------------------------------+
```

### 3.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `places`**:
  - Tên, Địa chỉ, Tỉnh thành $\rightarrow$ `places.name`, `places.address`, `places.province`
  - Vị trí trên bản đồ $\rightarrow$ `places.location` (PostGIS `GEOMETRY(Point, 4326)`)
  - Khoảng giá $\rightarrow$ `places.min_price`, `places.max_price`, `places.currency`
  - Điểm đánh giá trung bình $\rightarrow$ `places.average_rating`
  - Bộ sưu tập ảnh $\rightarrow$ `places.images` (JSONB)
  - Đặc điểm ảnh trích xuất $\rightarrow$ `places.visual_attributes` (JSONB - phục vụ tìm kiếm theo ảnh)
- **Bảng `place_categories`**:
  - Phân loại bộ lọc $\rightarrow$ `place_categories.name`, `place_categories.slug`

---

## 4. Màn Hình SCR-07: Chi Tiết Địa Điểm & Minh Bạch Lý Do Gợi Ý (Place Detail)

### 4.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Trình bày đầy đủ thông tin về một điểm đến, nhưng đặc biệt nhấn mạnh vào câu hỏi: *"Tại sao AI lại gợi ý nơi này cho bạn?"*.
- **Mục tiêu:** Cung cấp thông tin giờ mở cửa, giá vé, hình ảnh chân thực, các nhận xét đã kiểm duyệt và hiển thị rõ nguồn dữ liệu để người dùng hoàn toàn tin cậy.

### 4.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| < Quay lại danh sách                                     [ + Chọn điểm này (+1) ] |
+-----------------------------------------------------------------------------------+
| TIỆM CÀ PHÊ HOÀNG HÔN                                                             |
| Địa chỉ: Dốc số 7, Phường 11, TP. Đà Lạt, Lâm Đồng                                |
|                                                                                   |
| [Bộ sưu tập ảnh phong cảnh: (Ảnh 1) (Ảnh 2) (Ảnh 3)...]                           |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [VÌ SAO NƠI NÀY PHÙ HỢP VỚI GIA ĐÌNH BẠN?]                                    | |
| | - Đúng gu: Bạn đã chọn sở thích "ngắm hoàng hôn và thích không gian mở".       | |
| | - An toàn cho bé: Quán có sân phẳng, nhiều cây xanh, lối đi có rào chắn.       | |
| | - Khoảng cách hợp lý: Chỉ cách khách sạn dự kiến 15 phút đi taxi.              | |
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
| [THÔNG TIN KIỂM CHỨNG & THỜI ĐIỂM KIỂM TRA]                                       |
| - Giờ mở cửa: 07:00 - 22:00 hàng ngày      [Nguồn: Google Maps - 15p trước (98%)] |
| - Giá nước uống: 50.000đ - 90.000đ         [Nguồn: Bảng giá niêm yết tại quán]    |
| - Tình trạng thời tiết: Nắng ráo, se lạnh  [Nguồn: OpenWeather - 30p trước (92%)]  |
|                                                                                   |
| [ĐÁNH GIÁ TỪ DU KHÁCH THỰC TẾ (128 nhận xét)]:                                    |
| > Hoàng Nam (Tháng 08/2026): "Hoàng hôn ở đây rất đẹp, gia đình có bé nhỏ đi taxi |
|   vào tận nơi rất tiện." (5 sao ★★★★★)                                            |
+-----------------------------------------------------------------------------------+
```

### 4.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `information_sources`**:
  - Nguồn dữ liệu kiểm chứng $\rightarrow$ `information_sources.source_name`, `information_sources.source_url`
  - Thời điểm kiểm tra $\rightarrow$ `information_sources.checked_at`
  - Mức độ tin cậy $\rightarrow$ `information_sources.confidence` (Ví dụ: `0.98` hiển thị thành `98%`)
  - Trường thông tin $\rightarrow$ `information_sources.field_name` (`opening_hours`, `price`, `weather`)
- **Bảng `place_reviews`**:
  - Nhận xét hiển thị công khai $\rightarrow$ `place_reviews.comment`, `place_reviews.rating`, `place_reviews.published_at` (với điều kiện `status = ReviewStatus.PUBLIC`)
