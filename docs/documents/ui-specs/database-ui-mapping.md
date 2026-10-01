# Bảng Đối Chiếu Dữ Liệu: Giao Diện Người Dùng (UI) & Cơ Sở Dữ Liệu (Database)

Tài liệu này đối chiếu **100% các thành phần thị giác trên các màn hình** (`SCR-01` đến `SCR-29`, bao gồm `SCR-09B`) với **23 bảng cơ sở dữ liệu và các kiểu dữ liệu liệt kê (Enums)** được định nghĩa trong [`DATABASE.txt`](file:///home/phamhoangthai/Documents/project/tour-guide-agent/docs/DATABASE.txt).

---

## 1. Bảng Tổng Hợp Ánh Xạ Giữa Màn Hình (UI Screens) & Bảng Dữ Liệu (Tables)

| Mã Màn Hình | Tên Màn Hình / Chức Năng | Bảng Dữ Liệu Chính (Primary Tables) | Bảng Liên Quan & Enums |
| :--- | :--- | :--- | :--- |
| **SCR-01** | Đăng nhập & Đăng ký | `users` | `AccountStatus` (`ACTIVE`, `BANNED`, `DISABLED`), `UserRole` (`USER`, `OPERATOR`, `ADMIN`) |
| **SCR-02** | Khung App Shell & Lịch sử | `agent_session`, `trips`, `trip_requests` | `AgentSessionStatus` (`ACTIVE`, `ARCHIVED`), `UserRole` |
| **SCR-03** | Hồ sơ du lịch cá nhân | `user_profile`, `agent_memories` | `travel_preferences`, `special_needs`, `default_budget`, `AgentMemoryScope` (`WORKING`, `TRIP`) |
| **SCR-04** | Hội thoại lập kế hoạch AI | `messages`, `agent_session`, `media_files` | `agent_runs`, `MediaImage.REQUEST_IMAGE`, `AgentSessionStatus.ACTIVE` |
| **SCR-05** | Bản tóm tắt yêu cầu chuyến đi | `trip_requests`, `trip_request_selected_places` | `TripRequestStatus` (`DRAFT`, `CONFIRMED`, `PLANNING`, `PLANNED`, `CANCELLED`), `version` |
| **SCR-06** | Khám phá địa điểm (Danh sách & Map) | `places`, `place_categories`, `media_files` | `location` (PostGIS Point 4326), `visual_attributes`, `is_active` |
| **SCR-07** | Chi tiết địa điểm & Căn cứ đề xuất | `places`, `information_sources`, `place_reviews` | `source_name`, `confidence`, `checked_at`, `SourceEntityType.PLACE`, `ReviewStatus.PUBLIC` |
| **SCR-08** | Tiến trình thực thi Đa tác nhân | `agent_runs`, `evaluation_results` | `AgentType` (`PLANNER`, `CRITIC`), `AgentRunStatus` (`RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`), `TripRequestStatus.PLANNING` |
| **SCR-09** | So sánh các phương án AI đề xuất | `itineraries`, `evaluation_results`, `information_sources` | `ItineraryStatus` (`DRAFT`, `REVIEWING`), `trade_offs`, `cost_breakdown`, `highlights`, `warnings` |
| **SCR-09B**| **Danh sách & Thư viện lịch trình đã lưu** | `itineraries`, `trips`, `trip_requests` | `ItineraryStatus` (`DRAFT`, `SELECTED`), `trips.finalized_itinerary_id`, `TripRequestStatus.PLANNED` |
| **SCR-10** | Chi tiết lịch trình & Bàn làm việc Timeline | `itineraries`, `itinerary_days`, `itinerary_activities`, `itinerary_transits` | `luggage_checklist` (JSONB), `activity_type`, `transport_mode`, `planned_date` |
| **SCR-11** | Bảng xem trước đề xuất thay đổi (Diff) | `itinerary_proposals`, `evaluation_results` | `ItineraryProposalStatus` (`pending`, `accepted`, `rejected`), `diff_payload`, `rationale` |
| **SCR-12** | Gợi ý dịch vụ & Chuyển hướng trực tiếp | `booking_offers`, `information_sources` | `BookingOfferType` (`HOTEL`, `FLIGHT`, `TRANSPORT`, `ACTIVITY`), `BookingOfferStatus` (`AVAILABLE`, `STALE`, `UNAVAILABLE`), `redirect_url` |
| **SCR-14** | Bảng điều khiển chuyến đi đang chạy | `trips`, `gps_location_events`, `itineraries` | `gps_consent`, `actual_start_date`, `is_expired` (7 ngày), `expires_at` |
| **SCR-15** | Hỏi đáp tại chỗ & Nhận diện ảnh | `messages`, `places`, `information_sources` | `visual_attributes`, `confidence`, `MediaImage.REQUEST_IMAGE`, `SourceEntityType.MESSAGE` |
| **SCR-16** | Trình phát thuyết minh Audio Guide | `place_narrations`, `gps_location_events` | `audio_object_key`, `transcript`, `duration_seconds`, `is_active` |
| **SCR-17** | Cảnh báo thời tiết & Đề xuất đổi lịch | `trip_alerts`, `itinerary_proposals`, `information_sources` | `severity`, `confidence`, `affected_activity_id`, `alternative_proposal_id`, `SourceEntityType.TRIP_ALERT` |
| **SCR-18** | Soạn thảo đánh giá cá nhân | `place_reviews`, `media_files` | `ReviewStatus` (`PRIVATE`, `PENDING`), `VisitVerificationStatus` (`UNVERIFIED`, `VERIFIED`), `MediaImage.REVIEW_PHOTO` |
| **SCR-19** | Xem đánh giá cộng đồng & Báo cáo | `place_reviews`, `review_reports` | `ReviewStatus.PUBLIC`, `ReviewReportReason` (`SPAM`, `ABUSE`, `IRRELEVANT`, `FALSE_INFORMATION`, `OTHER`), `ReviewReportStatus` (`OPEN`, `REVIEWING`) |
| **SCR-20** | Bảng kiểm duyệt đánh giá (Operator/Admin) | `place_reviews`, `review_reports`, `review_moderation_logs` | `ModerationAction` (`APPROVE`, `REJECT`, `HIDE`, `RESTORE`), `ModeratorType` (`SYSTEM`, `OPERATOR`, `ADMIN`) |
| **SCR-21** | Tổng kết điểm đến thực tế | `trip_summaries`, `trip_summary_places` | `SummaryPlaceStatus` (`VISITED`, `SKIPPED`, `UNPLANNED`), `is_user_corrected`, `evidence` (GPS/tương tác) |
| **SCR-22** | Báo cáo chi phí thực tế & Nhật ký | `trip_summaries`, `trip_expenses`, `media_files` | `ExpenseCategory` (`LODGING`, `TRANSPORT`, `FOOD`, `TICKET`, `SHOPPING`, `OTHER`), `MediaImage.SUMMARY_PHOTO` |
| **SCR-23** | Chốt tổng kết & Gợi ý chuyến tiếp theo | `trip_summaries`, `next_trip_suggestions`, `user_profile` | `TripSummaryStatus.CONFIRMED`, `rank` (1..3), `estimated_budget`, `started_agent_session_id` |
| **SCR-24** | Tra cứu nhật ký kỹ thuật & sự cố | `agent_runs`, `trips` | `AgentRunStatus` (`RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`, `EXPIRED`), `error_code`, `expires_at` (7 ngày) |
| **SCR-25** | Cửa sổ Ticket ID & Chi tiết Trace | `audit_access_logs`, `agent_runs`, `tool_calls` | `ticket_id`, `purpose`, `ToolCallStatus` (`RUNNING`, `SUCCEEDED`, `FAILED`), `decision_summary` |
| **SCR-26** | Quản trị kho địa điểm & Toàn diện Dịch vụ | `places`, `place_categories`, `place_narrations`, `booking_offers` | `is_active`, `opening_hours`, `location` (Point 4326), `visual_attributes`, `BookingOfferType` |
| **SCR-27** | Bảng kiến nghị Maker–Checker | `operator_proposals`, `places` | `OperatorProposalType` (`PLACE_UPDATE`, `WEATHER_REPORT`, `AI_ISSUE`), `OperatorProposalStatus` (`PENDING`, `APPROVED`, `REJECTED`) |
| **SCR-28** | Quản trị người dùng & Phân quyền | `users` | `AccountStatus` (`ACTIVE`, `BANNED`, `DISABLED`), `UserRole` (`USER`, `OPERATOR`, `ADMIN`) |
| **SCR-29** | Cấu hình tham số hệ thống động | `system_configs` | `config_key`, `config_value` (JSONB) |

---

## 2. Chi Tiết Khớp Nối Dữ Liệu Từng Thành Phần UI

### 2.1. Nhóm Dữ Liệu Đảm Bảo Tính Minh Bạch (Information Provenance)
Mọi nhãn thông tin có huy hiệu *Nguồn dữ liệu / Độ tin cậy* trên các màn hình `SCR-07`, `SCR-09`, `SCR-12`, `SCR-15`, `SCR-17` đều tương ứng trực tiếp với bảng **`information_sources`**:
- **Nhãn Tên Nguồn (Source Name)** $\rightarrow$ `information_sources.source_name` (Ví dụ: "Google Maps", "OpenWeather", "Agoda").
- **Nhãn Thời Điểm Kiểm Tra (Checked At)** $\rightarrow$ `information_sources.checked_at` (Ví dụ: "10 phút trước").
- **Nhãn Mức Độ Tin Cậy (Confidence Badge)** $\rightarrow$ `information_sources.confidence` (Ví dụ: `0.95` hiển thị thành `95%`).

---

### 2.2. Nhóm Dữ Liệu Về Quyền Riêng Tư & Hạn Lưu Trữ 7 Ngày (Data Retention)
Các thông báo nhắc nhở về quyền riêng tư và tự hủy dữ liệu trên `SCR-01`, `SCR-04`, `SCR-14`, `SCR-24`, `SCR-25` tương ứng với các trường thời hạn trong cơ sở dữ liệu:
- **Tọa độ di chuyển GPS** $\rightarrow$ `gps_location_events.expires_at` & `gps_location_events.is_expired`.
- **File ảnh tải lên** $\rightarrow$ `media_files.created_at` (Tính hạn theo `system_configs.temporary_data_retention_days`).
- **Bộ nhớ hội thoại & Log kỹ thuật** $\rightarrow$ `agent_memories.expires_at` & `agent_runs.expires_at`.

---

### 2.3. Nhóm Dữ Liệu Phê Duyệt & Khóa Phiên Bản (Optimistic Locking & Approval)
- **Bản tóm tắt yêu cầu (`SCR-05`)** $\rightarrow$ `trip_requests.version` (Tăng số hiệu mỗi khi có thay đổi; chỉ chuyển sang `status = 'CONFIRMED'` khi đủ 4 thông tin bắt buộc: `origin_name`, `start_date`, `budget`, `currency`).
- **Lộ trình và đề xuất thay đổi (`SCR-10`, `SCR-11`)** $\rightarrow$ `itineraries.version` và `itinerary_proposals.status` (`pending` $\rightarrow$ `accepted`/`rejected`).
- **Kiểm soát 4 mắt Maker–Checker (`SCR-27`)** $\rightarrow$ `operator_proposals.status` (`PENDING` $\rightarrow$ `APPROVED`/`REJECTED`) đi kèm `admin_note` và `admin_id`.
