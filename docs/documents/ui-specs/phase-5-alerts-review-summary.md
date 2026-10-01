# Ý Tưởng Giao Diện: Phase 5 — Cảnh Báo Realtime, Đánh Giá & Hậu Chuyến Đi

Nhóm màn hình này xử lý các tình huống bất ngờ phát sinh trong chuyến đi (thời tiết xấu, điểm đến đóng cửa), cho phép viết đánh giá trải nghiệm và tổng kết toàn bộ hành trình sau khi trở về (`SCR-17` đến `SCR-23`).

---

## 1. Màn Hình SCR-17: Cảnh Báo Thời Gian Thực & Đề Xuất Đổi Lịch Trình (Real-time Alerts & Replanning)

### 1.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Khi trời bỗng đổ mưa to hoặc điểm tham quan có sự cố đột xuất, AI sẽ chủ động gửi thông báo cảnh báo và lập tức đưa ra phương án thay thế tối ưu nhất để người dùng lựa chọn.
- **Mục tiêu:** Giúp chuyến đi không bị gián đoạn hay mất vui khi có yếu tố khách quan ngoài ý muốn.

### 1.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| [!] CẢNH BÁO THỜI TIẾT ĐỘT XUẤT — CHUYẾN ĐI ĐÀ LẠT                               |
+-----------------------------------------------------------------------------------+
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [MỨC ĐỘ ẢNH HƯỞNG: CẦN THAY ĐỔI] — CƠN MƯA LỚN VÀO CHIỀU NAY (15:00 - 18:00)    | |
| | Điểm bị ảnh hưởng: Tiệm cà phê Hoàng Hôn (Không gian ngoài trời, dốc trơn)      | |
| | Cập nhật từ: Trạm quan trắc thời tiết | Cách đây 10 phút (Độ tin cậy: 92%)      | |
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
| [PHƯƠNG ÁN THAY THẾ DO AI ĐỀ XUẤT ĐỂ AN TOÀN CHO BÉ]:                             |
|                                                                                   |
|  CHIỀU HÔM NAY (15:30 - 17:30)                                                    |
|  [-] TẠM DỪNG: Tiệm cà phê Hoàng Hôn (Nguy cơ ướt mưa và lạnh cho bé)             |
|  [+] THAY THẾ: Tham quan Dinh 1 Bảo Đại (Khuôn viên có mái che, lịch sử thú vị)   |
|                                                                                   |
|  ĐÁNH GIÁ TỔNG QUAN:                                                              |
|  - Chi phí: Vé vào cổng +80.000đ (Vẫn nằm gọn trong ngân sách dự trù)             |
|  - Di chuyển: Gần hơn 2 km so với quán cà phê ngoài trời                          |
|                                                                                   |
| +------------------------------------+     +------------------------------------+ |
| |    [V] ĐỒNG Ý ĐỔI SANG DINH 1      |     |     [X] TÔI TỰ TÌM CHỖ TRÚ MƯA     | |
| +------------------------------------+     +------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 1.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `trip_alerts`**:
  - Tiêu đề & Nội dung cảnh báo $\rightarrow$ `trip_alerts.title`, `trip_alerts.message`
  - Mức độ nghiêm trọng $\rightarrow$ `trip_alerts.severity`
  - Hoạt động bị ảnh hưởng $\rightarrow$ `trip_alerts.affected_activity_id`
  - Phương án thay thế liên kết $\rightarrow$ `trip_alerts.alternative_proposal_id`
  - Nguồn & Độ tin cậy $\rightarrow$ `trip_alerts.source`, `trip_alerts.confidence`, `trip_alerts.checked_at`

---

## 2. Màn Hình SCR-18: Soạn Thảo Đánh Giá Cá Nhân (Review Editor)

### 2.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Giúp du khách lưu lại cảm nhận chân thực về từng địa điểm mình đã đi qua (chấm sao, viết nhật ký, đính kèm ảnh chụp).
- **Mục tiêu:** Mặc định bài đánh giá được lưu ở chế độ **Riêng tư (Chỉ mình tôi xem)**; người dùng có thể chủ động chọn chia sẻ ra cộng đồng nếu muốn.

### 2.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| VIẾT CẢM NHẬN VỀ ĐIỂM ĐẾN                                             [ HỦY BỎ ]  |
| Địa điểm: Nông trại Cún Puppy Farm - Đà Lạt                                       |
+-----------------------------------------------------------------------------------+
| Bạn đánh giá nơi này thế nào?: [ ★ ] [ ★ ] [ ★ ] [ ★ ] [ ★ ] (5/5 sao - Rất thích)|
|                                                                                   |
| Chia sẻ trải nghiệm của gia đình bạn:                                             |
| [ Nông trại rất sạch sẽ, các bé cún được chăm sóc kỹ và rất thân thiện với trẻ em.|
|   Gia đình mình đi cùng bé 4 tuổi, bé mê tít hoạt động hái dâu tây tại vườn.      |
|                                                                                 ] |
|                                                                                   |
| Thêm hình ảnh kỷ niệm: [ (Ảnh 1) (Ảnh 2) ] [ + Thêm ảnh ] (Tối đa 5 ảnh)          |
|                                                                                   |
| [CHẾ ĐỘ HIỂN THỊ ĐÁNH GIÁ]                                                        |
| (•) Chỉ lưu trong nhật ký cá nhân của tôi (MẶC ĐỊNH RIÊNG TƯ)                     |
| ( ) Chia sẻ công khai cho cộng đồng (Sẽ được ban quản trị kiểm duyệt trước)       |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| |                                 [ LƯU ĐÁNH GIÁ ]                              | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 2.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `place_reviews`**:
  - Số sao $\rightarrow$ `place_reviews.rating` (1..5)
  - Lời bình $\rightarrow$ `place_reviews.comment`
  - Trạng thái riêng tư/công khai $\rightarrow$ `place_reviews.status` (`PRIVATE` mặc định, hoặc `PENDING` khi xin duyệt)
  - Xác minh đã đến điểm $\rightarrow$ `place_reviews.visit_status` (`VERIFIED`, `UNVERIFIED`)
- **Bảng `media_files`**:
  - Ảnh đính kèm $\rightarrow$ `media_files.purpose = MediaImage.REVIEW_PHOTO`

---

## 3. Màn Hình SCR-19 & SCR-20: Đánh Giá Cộng Đồng & Bảng Duyệt Đánh Giá

### 3.1. Màn Hình SCR-19: Xem Đánh Giá Cộng Đồng (Public Community Reviews)
- **Bảng `place_reviews`**: Danh sách nhận xét công khai đã được xác minh (`status = ReviewStatus.PUBLIC`).
- **Bảng `review_reports`**: Khi bấm nút *Báo cáo vi phạm*, lưu lý do `reason_code` (`SPAM`, `ABUSE`, `IRRELEVANT`, `FALSE_INFORMATION`, `OTHER`), chi tiết `details`, trạng thái `status = ReviewReportStatus.OPEN`.

### 3.2. Màn Hình SCR-20: Bảng Duyệt Đánh Giá Dành Cho Ban Quản Trị (Moderation Dashboard)
- **Bảng `review_moderation_logs`**:
  - Hành động duyệt $\rightarrow$ `ModerationAction` (`APPROVE`, `REJECT`, `HIDE`, `RESTORE`)
  - Người duyệt $\rightarrow$ `moderator_id`, `moderator_type` (`OPERATOR`, `ADMIN`)
  - Lý do xử lý $\rightarrow$ `review_moderation_logs.reason`

```text
+-----------------------------------------------------------------------------------+
| BẢNG KIỂM DUYỆT ĐÁNH GIÁ TỪ DU KHÁCH                    [ Lọc: Đang chờ duyệt (5)]|
+-----------------------------------------------------------------------------------+
| NGÀY GỬI       | ĐỊA ĐIỂM / TÀI KHOẢN | CẢM NHẬN ĐƯỢC GỬI         | HÀNH ĐỘNG      |
+----------------+----------------------+---------------------------+----------------+
| 15/10 16:30    | Puppy Farm Đà Lạt    | "Trang trại sạch sẽ, phù  | [V Duyệt bài]  |
|                | Du khách: @hoangnam  | hợp cho bé nhỏ..." (5★)   | [X Từ chối]    |
+----------------+----------------------+---------------------------+----------------+
| 14/10 21:00    | Chợ Đêm Đà Lạt       | "Bán đắt, mua tại link:   | [Ẩn bài viết]  |
|                | (Có 2 lượt báo cáo)  | http://shoponline..."     | [Xem vi phạm]  |
+----------------+----------------------+---------------------------+----------------+
```

---

## 4. Màn Hình SCR-21, SCR-22 & SCR-23: Tổng Kết Chuyến Đi & Vòng Cá Nhân Hóa

### 4.1. Màn Hình SCR-21: Tổng Kết Điểm Đến Thực Tế (Places Visited Summary)
- **Bảng `trip_summary_places`**:
  - Địa điểm trong tổng kết $\rightarrow$ `trip_summary_places.place_id` (nếu có trong kho địa điểm) hoặc `trip_summary_places.place_name` (lưu tên trực tiếp nếu là điểm dừng chân phát sinh tự do ngoài danh mục).
  - Trạng thái phân loại điểm $\rightarrow$ `trip_summary_places.status` (`VISITED` - đã đi, `SKIPPED` - đã bỏ qua, `UNPLANNED` - phát sinh ngoài kế hoạch ban đầu)
  - Bằng chứng phân loại tự động $\rightarrow$ `trip_summary_places.evidence` (Dữ liệu tọa độ GPS, thời gian dừng, tương tác chat)
  - Độ tin cậy nhận diện $\rightarrow$ `trip_summary_places.confidence`
  - Cờ đánh dấu người dùng đã tự tay đính chính $\rightarrow$ `trip_summary_places.is_user_corrected` (BOOLEAN)
  - Ghi chú riêng cho điểm đến $\rightarrow$ `trip_summary_places.notes`

### 4.2. Màn Hình SCR-22: Báo Cáo Chi Phí & Nhật Ký Kỷ Niệm (Trip Expenses & Diary)
- **Bảng `trip_expenses`**:
  - Hạng mục chi phí $\rightarrow$ `trip_expenses.category` (`LODGING`, `TRANSPORT`, `FOOD`, `TICKET`, `SHOPPING`, `OTHER`)
  - Số tiền & Tiền tệ $\rightarrow$ `trip_expenses.amount`, `trip_expenses.currency`
- **Bảng `trip_summaries`**:
  - Cảm nhận chung $\rightarrow$ `trip_summaries.diary_notes`
  - Đánh giá tổng thể $\rightarrow$ `trip_summaries.overall_rating` (1..5)
- **Bảng `media_files`**:
  - Ảnh kỷ niệm tổng kết $\rightarrow$ `media_files.purpose = MediaImage.SUMMARY_PHOTO`

```text
+-----------------------------------------------------------------------------------+
| TỔNG KẾT CHI PHÍ & NHẬT KÝ CHUYẾN ĐI ĐÀ LẠT 3N2Đ                                  |
+-----------------------------------------------------------------------------------+
| [ĐỐI CHIẾU NGÂN SÁCH DỰ TRÙ VÀ THỰC TẾ]:                                          |
|                                                                                   |
| * Ngân sách dự trù ban đầu: 7.250.000 VNĐ                                         |
| * Tổng chi tiêu thực tế:    6.950.000 VNĐ  [BẠN ĐÃ TIẾT KIỆM ĐƯỢC: 300.000 VNĐ]   |
|                                                                                   |
| CHI TIẾT TỪNG KHOẢN CHI THỰC TẾ:                                                  |
| - Khách sạn Colline (LODGING):   1.850.000đ  | Xe Limousine (TRANSPORT): 2.100.000đ|
| - Ăn uống (FOOD):                1.900.000đ  | Vé tham quan (TICKET):   1.100.000đ |
| [+ Thêm khoản chi tiêu khác...]                                                   |
|                                                                                   |
| [NHẬT KÝ CẢM XÚC CHUNG VỀ CHUYẾN ĐI]:                                             |
| [ Chuyến đi rất vui và ý nghĩa cho bé, khí hậu mát mẻ, đồ ăn ngon và hợp khẩu vị. ]|
| Đánh giá chuyến đi tổng thể: [ ★ ] [ ★ ] [ ★ ] [ ★ ] [ ★ ] (5/5 sao)              |
+-----------------------------------------------------------------------------------+
```

### 4.3. Màn Hình SCR-23: Chốt Kỷ Niệm & Gợi Ý Chuyến Đi Kế Tiếp (Next Trip Recommendations)
- **Bảng `trip_summaries`**: Chốt trạng thái $\rightarrow$ `trip_summaries.status = TripSummaryStatus.CONFIRMED`, `confirmed_at`
- **Bảng `next_trip_suggestions`**:
  - Thứ tự gợi ý $\rightarrow$ `next_trip_suggestions.rank` (1..3)
  - Tiêu đề & Mô tả $\rightarrow$ `next_trip_suggestions.title`, `next_trip_suggestions.description`
  - Địa điểm đề xuất $\rightarrow$ `next_trip_suggestions.suggested_places` (JSONB)
  - Ngân sách ước tính $\rightarrow$ `next_trip_suggestions.estimated_budget`, `currency`
  - Phiên chat khởi tạo $\rightarrow$ `next_trip_suggestions.started_agent_session_id`

```text
+-----------------------------------------------------------------------------------+
| [V] CHÚC MỪNG BẠN ĐÃ HOÀN THÀNH CHUYẾN ĐI ĐÀ LẠT 3N2Đ!                            |
| Kỷ niệm và chi phí đã được lưu trữ an toàn trong sổ tay du lịch cá nhân.          |
+-----------------------------------------------------------------------------------+
| [AI GỢI Ý 2 Ý TƯỞNG CHO KỲ NGHỈ TIẾP THEO DỰA TRÊN SỞ THÍCH CỦA BẠN]:            |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | (GỢI Ý 1): NGHỈ DƯỠNG BIỂN QUY NHƠN 3N2Đ (Thích hợp cho gia đình có bé nhỏ)   | |
| | * Vì sao hợp bạn: Dựa trên thói quen chi tiêu ~2tr/ngày & thích khách sạn sân | |
| |   vườn thoáng đãng mà bạn vừa trải nghiệm ở Đà Lạt.                           | |
| | * Ngân sách dự trù: ~7.500.000 VNĐ                                            | |
| |                                                                               | |
| | [ BẮT ĐẦU LẬP KẾ HOẠCH TỪ GỢI Ý NÀY (Tự động điền sẵn sở thích) >> ]          | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```
