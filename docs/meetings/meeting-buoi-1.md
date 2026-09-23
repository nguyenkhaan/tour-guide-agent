# Biên Bản Cuộc Họp: Tour Guide Agent - Buổi 1

> **Trạng thái:** Bản nháp. Thông tin ngày, người tham gia và phân công chưa được cập nhật; tài liệu này không thay thế yêu cầu nghiệp vụ và user story.

**Ngày họp:** [DD/MM/YYYY]  
**Thời gian:** [Giờ bắt đầu] - [Giờ kết thúc]  
**Địa điểm/Link họp:** [Phòng họp / Link Google Meet/Zoom...]  
**Người ghi biên bản (Thư ký):** [Tên người ghi chép]  

---

## Mục tiêu cuộc họp

1. Thống nhất các user story cho người dùng.
2. Thống nhất công nghệ sử dụng.
3. Thống nhất sơ đồ use case.

---

## Nội dung thảo luận

### 1. User Story

#### Phía người dùng

- Danh sách hiện tại gồm US01–US70 trong `docs/documents/user-story.md`.
- Không bổ sung user story riêng cho đăng ký và đăng nhập trong phạm vi hiện tại.
- Thống nhất hệ thống tạo từ 1 đến 4 lộ trình.
- Với đề xuất chỉnh sửa của Agent, người dùng xác nhận chấp nhận hoặc từ chối trước khi hệ thống áp dụng.

#### Phía hệ thống

- Critic/Evaluator là bước kiểm tra bắt buộc với lộ trình mới và thay đổi quan trọng.
- Truy cập log kỹ thuật yêu cầu đồng thời mục đích truy cập và Ticket ID.
- Weather Monitor và Trip Completion được thực hiện bằng background job trong backend monolith.
- GPS, media gốc, working/trip memory và log kỹ thuật chi tiết có thời hạn lưu tối đa 7 ngày; cron cleanup chạy hằng ngày.

### 2. Công nghệ

**Nội dung chính**:

- Frontend: React + TypeScript.
- Backend: Python + FastAPI theo kiến trúc modular monolith.
- AI: một Orchestrator với ba Agent — Planner, Critic/Evaluator và Booking & Logistics — chạy trên Agent Harness dùng chung.
- Data Storage: một PostgreSQL có PostGIS extension và một Object Storage.
- Background processing: scheduler/job runner nội bộ; dùng khóa điều phối trong PostgreSQL và job idempotent, chưa cần message broker.

**Phân công**:

- Chưa cập nhật.
