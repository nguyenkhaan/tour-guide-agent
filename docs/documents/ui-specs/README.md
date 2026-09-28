# Đặc Tả Ý Tưởng Giao Diện & Luồng Người Dùng — Tour Guide Agent

Tài liệu này tập trung hoàn toàn vào **ý tưởng thiết kế giao diện (UI)**, **trải nghiệm người dùng (UX)** và **luồng hoạt động (User Flow)** của từng màn hình trong hệ thống **Tour Guide Agent**.

Mọi màn hình đều được **đối chiếu và đồng bộ 100% với mô hình cơ sở dữ liệu** được định nghĩa trong [`DATABASE.txt`](../DATABASE.txt).

---

## 1. Triết Lý Thiết Kế Giao Diện AI Đồng Hành (Agentic UX Philosophy)

Ứng dụng Tour Guide Agent được thiết kế xoay quanh 4 trải nghiệm cốt lõi:

```text
+---------------------------------------------------------------------------------+
|                        TRIẾT LÝ TRẢI NGHIỆM NGƯỜI DÙNG                          |
|                                                                                 |
|   +-----------------------+     +-----------------------+     +---------------+ |
|   | 1. Tương tác Tự nhiên | --> | 2. Quyền Kiểm soát    | --> | 3. Minh bạch  | |
|   |    & Trực quan        |     |    Của Người dùng     |     |    & Tin cậy  | |
|   +-----------------------+     +-----------------------+     +---------------+ |
|               |                             |                         |         |
|               v                             v                         v         |
|   - Nói/chat như người thật     - AI chỉ đưa đề xuất          - Thấy rõ nguồn   |
|   - Nhận diện qua ảnh & GPS     - Xem trước thay đổi (Diff)   - Hiển thị độ tin |
|   - Thuyết minh tự động         - Chủ động bấm Đồng ý/Từ chối   cậy của thông tin|
+---------------------------------------------------------------------------------+
```

1. **Tương tác Tự nhiên & Đa phương tiện**: Người dùng có thể trò chuyện bằng ngôn ngữ tự nhiên, gửi hình ảnh phong cảnh yêu thích, hoặc bật định vị để AI tự hiểu ngữ cảnh mà không cần điền form phức tạp.
2. **Quyền Kiểm soát thuộc về Con người (Human-in-the-loop)**: AI đóng vai trò người tư vấn. Mọi điều chỉnh kế hoạch, đổi lịch trình hay đổi điểm đến đều phải hiển thị dạng bảng so sánh trước/sau (*Visual Diff*) và chỉ áp dụng khi người dùng bấm xác nhận.
3. **Minh bạch & Dễ hiểu**: Dữ liệu có thể biến động (thời tiết, giờ mở cửa, giá vé) luôn đi kèm nhãn chú thích nguồn gốc và độ tin cậy để người dùng an tâm.
4. **Tôn trọng Quyền riêng tư**: Giao diện luôn hỏi ý kiến trước khi bật định vị GPS, và có thông báo nhắc nhở rõ ràng về việc tự động xóa các dữ liệu nhạy cảm sau chuyến đi.

---

## 2. Bản Đồ Các Màn Hình & Đối Chiếu Cơ Sở Dữ Liệu

| Giai đoạn | Tên nhóm màn hình | Mã màn hình | Bảng dữ liệu tương ứng trong DB | Tài liệu đặc tả chi tiết |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Khởi Đầu & Cá Nhân Hóa** | `SCR-01` $\rightarrow$ `SCR-03` | `users`, `user_profile`, `agent_session` | [Xem chi tiết](./phase-1-foundation-auth-profile.md) |
| **Phase 2** | **Lên Ý Tưởng & Khám Phá** | `SCR-04` $\rightarrow$ `SCR-07` | `messages`, `trip_requests`, `places`, `place_categories`, `media_files` | [Xem chi tiết](./phase-2-discovery-and-request.md) |
| **Phase 3** | **Lập Lịch Trình & Tùy Chỉnh** | `SCR-08`, `SCR-09`, `SCR-09B`, `SCR-10`, `SCR-11` | `itineraries`, `itinerary_days`, `itinerary_activities`, `itinerary_proposals`, `evaluation_results` | [Xem chi tiết](./phase-3-multi-agent-itinerary.md) |
| **Phase 4** | **Đặt Chỗ & Đồng Hành Thực Tế** | `SCR-12` $\rightarrow$ `SCR-16` | `booking_offers`, `trips`, `gps_location_events`, `place_narrations` | [Xem chi tiết](./phase-4-booking-and-companion.md) |
| **Phase 5** | **Cảnh Báo Realtime & Hậu Chuyến Đi** | `SCR-17` $\rightarrow$ `SCR-23` | `trip_alerts`, `place_reviews`, `review_reports`, `trip_summaries`, `trip_expenses`, `next_trip_suggestions` | [Xem chi tiết](./phase-5-alerts-review-summary.md) |
| **Phase 6** | **Quản Trị Vận Hành & Hỗ Trợ** | `SCR-24` $\rightarrow$ `SCR-29` | `operator_proposals`, `agent_runs`, `tool_calls`, `audit_access_logs`, `system_configs` | [Xem chi tiết](./phase-6-admin-ops-audit.md) |

👉 **Tra cứu chi tiết toàn bộ ánh xạ:** Xem [**Bảng Đối Chiếu Dữ Liệu UI & Database Matrix**](./database-ui-mapping.md).

---

## 3. Định Hướng Phong Cách Thị Giác (Design Guidelines)
- **Tông màu chủ đạo**: Xanh biển (du lịch/tự do) kết hợp Xanh ngọc (thiên nhiên/khám phá). Điểm nhấn màu Tím nhẹ cho các hành động trí tuệ nhân tạo (AI Assistant).
- **Phân cấp thị giác**:
  - `Thẻ thông tin (Cards)`: Bo góc mềm mại, phân tách rõ ràng giữa nội dung gợi ý và nội dung người dùng nhập.
  - `Trạng thái AI đang xử lý`: Hiệu ứng nhịp đập (pulse) hoặc các bước tiến trình từng chặng rõ ràng, tránh để màn hình tĩnh gây cảm giác ứng dụng bị treo.
  - `Bảng so sánh (Diff View)`: Sử dụng màu Xanh lá cho phần thêm mới/thay đổi tốt hơn, màu Đỏ/Cam gạch cho phần bị hủy bỏ hoặc cảnh báo rủi ro.
