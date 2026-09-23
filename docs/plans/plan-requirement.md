# YÊU CẦU TRONG VIỆC TRIỂN KHAI KẾ HOẠCH
## 1. Overview

Kế hoạch này triển khai toàn bộ Tour Guide Agent từ một repository chưa có mã nguồn. Sản phẩm phục vụ khách du lịch tự túc tại Việt Nam, sử dụng React + TypeScript cho frontend và Python + FastAPI cho backend modular monolith. Backend gồm API Service, AI Orchestrator với đúng ba Agent, Agent Harness, PostgreSQL có PostGIS extension và Object Storage.

Kế hoạch ưu tiên các vertical slice có thể kiểm thử end-to-end. Mỗi Step phải hoàn thành cả dữ liệu, backend, frontend và kiểm thử liên quan trong phạm vi của Step; không xây toàn bộ một tầng rồi chờ đến cuối mới tích hợp.

## 2. Sources of Truth

Thứ tự đối chiếu khi triển khai:

1. docs/business-requirement.md
2. docs/documents/user-story.md
3. docs/documents/usecase.md
4. docs/documents/architecture.md
5. Kế hoạch này

Nếu phát hiện mâu thuẫn, dừng Step liên quan và đồng bộ lại bốn tài liệu nguồn trước khi tiếp tục.

## 3. Scope and Fixed Decisions

- Phạm vi ngôn ngữ hiện tại là tiếng Việt.
- Không triển khai cộng tác nhiều tài khoản, quản trị đoàn hoặc điều hành tour.
- Không bổ sung user story riêng cho đăng ký và đăng nhập, nhưng vẫn triển khai chức năng tài khoản theo business requirement.
- Mỗi yêu cầu lập kế hoạch tạo từ 1 đến 4 lộ trình.
- Hệ thống chỉ có Planner Agent, Critic/Evaluator Agent và Booking & Logistics Agent.
- Critic/Evaluator bắt buộc kiểm tra lộ trình mới và thay đổi quan trọng.
- Đề xuất chỉnh sửa của Agent chỉ được áp dụng sau khi người dùng chấp nhận.
- Agent không tự đặt chỗ, giữ tiền hoặc thanh toán.
- Không lưu hoặc hiển thị chuỗi suy luận thô; chỉ lưu lý do tóm tắt có cấu trúc.
- Truy cập log kỹ thuật bắt buộc có cả mục đích truy cập và Ticket ID.
- GPS, media gốc, working/trip memory và log kỹ thuật chi tiết hết hạn sau tối đa 7 ngày.
- Weather Monitor và Trip Completion chạy bằng background job trong modular monolith.
- Retention Cleanup chạy bằng một cron job hằng ngày.

## 4. Proposed Repository Structure

    tour-guide-agent/
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── modules/
    │   │   ├── ai/
    │   │   │   ├── orchestrator/
    │   │   │   ├── agents/
    │   │   │   └── harness/
    │   │   ├── infrastructure/
    │   │   ├── jobs/
    │   │   └── main.py
    │   ├── migrations/
    │   ├── tests/
    │   └── pyproject.toml
    ├── frontend/
    │   ├── src/
    │   │   ├── app/
    │   │   ├── features/
    │   │   ├── shared/
    │   │   └── main.tsx
    │   ├── tests/
    │   └── package.json
    ├── infra/
    │   ├── compose.yaml
    │   └── env/
    ├── docs/
    ├── scripts/
    ├── Makefile
    └── README.md

Tên thư mục có thể điều chỉnh trong Phase 1, nhưng ranh giới API Service, AI Orchestrator, Agent Harness và background jobs phải được giữ rõ ràng.

## 5. Dependency Order

    Repository and local infrastructure
        ├── Database, PostGIS and Object Storage
        ├── Backend and frontend foundations
        └── CI and quality gates
             │
             ├── Core platform and API contracts
             │     └── Vertical product slices
             │
             └── Agent Harness
                   └── AI Orchestrator and three Agents
                         └── Planning, booking and in-trip AI flows

    Background scheduler
        ├── Weather Monitor
        ├── Trip Completion
        └── Retention Cleanup

    All product slices
        └── Security, evaluation, observability, deployment and release

## 6. Requirement Coverage by Phase

| Requirement group | Planned phase |
| --- | --- |
| Account, profile and history | Phase 2 |
| Trip request and destination discovery — US01–US15 | Phase 5 |
| Itinerary and customization — US16–US28 | Phase 6 |
| Booking and logistics — US29–US34 | Phase 7 |
| In-trip guide and realtime updates — US35–US45 | Phase 8 |
| Reviews and moderation — US46–US51 | Phase 9 |
| Trip summary and personalization — US52–US64 | Phase 10 |
| Transparency and audit — US65–US70 | Phase 11 |
| Cross-cutting quality and production readiness | Phases 12–14 |

## 7. Project-wide Definition of Done

Mỗi Step chỉ được đánh dấu hoàn thành khi:

- [ ] Acceptance criteria của Step đã được đáp ứng và có bằng chứng kiểm thử.
- [ ] Backend lint, type check và test liên quan đều pass.
- [ ] Frontend lint, type check, test và production build liên quan đều pass.
- [ ] API contract/OpenAPI và tài liệu bị ảnh hưởng đã được cập nhật.
- [ ] Validation, authorization, error handling và audit áp dụng tại trust boundary.
- [ ] Không log secret, dữ liệu nhạy cảm không cần thiết hoặc chain-of-thought thô.
- [ ] Migration có đường nâng cấp rõ ràng và không làm mất dữ liệu ngoài chính sách retention.
- [ ] UI thay đổi được kiểm tra responsive, accessibility cơ bản và trạng thái loading/error/empty.

Các lệnh chuẩn sẽ được tạo trong Phase 1:

    make check
    make test
    make integration-test
    make e2e
    make build

---