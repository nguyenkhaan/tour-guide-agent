# Yêu cầu triển khai kế hoạch Tour Guide Agent

## 1. Mục đích

Tài liệu này xác định phạm vi, các màn hình phải xây dựng, dependency và tiêu chuẩn hoàn thành cho kế hoạch triển khai tại [plan.md](plan.md).

Sản phẩm phục vụ khách du lịch tự túc tại Việt Nam, dùng React + TypeScript cho frontend (FE) và Python + FastAPI cho backend (BE) dạng modular monolith. Backend gồm API Service, AI Orchestrator với đúng ba Agent, Agent Harness, PostgreSQL/PostGIS, Object Storage và các background job chạy trong cùng ứng dụng.

Từ Phase 3, công việc phải được triển khai theo **Feature-Driven Development / Vertical Slicing**: mỗi increment bao gồm UI, API, business logic, persistence, integration và test cần thiết cho cùng một hành vi người dùng. Không coi một UI chỉ chạy bằng mock hoặc một API chưa có màn hình sử dụng là feature đã hoàn thành.

## 2. Nguồn yêu cầu

Thứ tự đối chiếu khi triển khai:

1. [Business requirement](../business-requirement.md)
2. [User story](../documents/user-story.md)
3. [Use case](../documents/usecase.md)
4. [Architecture](../documents/architecture.md)
5. Tài liệu này và [plan.md](plan.md)

Nếu bốn tài liệu nguồn mâu thuẫn, dừng phần việc bị ảnh hưởng và thống nhất lại yêu cầu trước khi tiếp tục.

## 3. Quyết định phạm vi cố định

- Ngôn ngữ sản phẩm hiện tại là tiếng Việt.
- Một tài khoản có thể lập kế hoạch cho nhiều người; không có cộng tác nhiều tài khoản, quản trị đoàn hoặc điều hành tour.
- Tài khoản hỗ trợ đăng ký, đăng nhập, đăng xuất, hồ sơ du lịch và lịch sử; phân quyền 3 vai trò: User, Operator, Admin.
- Mỗi yêu cầu lập kế hoạch tạo từ 1 đến 4 lộ trình.
- Chỉ có ba Agent: Planner, Critic/Evaluator và Booking & Logistics.
- Critic/Evaluator bắt buộc kiểm tra lộ trình mới và thay đổi quan trọng.
- Agent/background job chỉ tạo đề xuất; finalized plan chỉ đổi sau khi người dùng chấp nhận.
- Áp dụng cơ chế Maker – Checker: Operator tạo kiến nghị thay đổi, Admin xem xét và phê duyệt.
- Hệ thống không tự đặt chỗ, giữ tiền hoặc thanh toán.
- Không lưu/hiển thị chain-of-thought thô; chỉ lưu lý do tóm tắt có cấu trúc và dữ liệu truy vết cần thiết.
- Thông tin biến động phải có nguồn, thời điểm kiểm tra và độ tin cậy.
- Mở log kỹ thuật của người dùng bắt buộc có quyền phù hợp, mục đích truy cập và Ticket ID.
- GPS, media gốc, working/trip memory và log kỹ thuật chi tiết hết hạn tối đa 7 ngày.
- Weather Monitor, Trip Completion và Retention Cleanup chạy trong modular monolith; chưa cần message broker.
- Không thêm microservice, distributed cache hoặc vector database nếu chưa có nhu cầu đã đo lường.

## 4. Luồng sản phẩm và cây phụ thuộc

Đây là rationale triển khai có thể kiểm chứng, không phải chuỗi suy luận nội bộ:

    Tài khoản + hồ sơ + typed API
        └── Hội thoại yêu cầu chuyến đi
              └── Summary đã xác nhận
                    ├── Khám phá/chọn địa điểm
                    │     └── Tạo + Critic kiểm tra lộ trình
                    │           └── Chọn/chỉnh sửa/phê duyệt/finalize plan
                    │                 ├── Tìm dịch vụ + chuyển sang đối tác
                    │                 └── Kích hoạt Trip Companion
                    │                       ├── Q&A/nhận diện/thuyết minh
                    │                       ├── Monitoring/cảnh báo/replanning
                    │                       └── Kết thúc + tổng kết chuyến đi
                    └── Hồ sơ/lịch sử dùng cho cá nhân hóa

    Review private → kiểm duyệt public → tín hiệu ranking
    Event/trace theo từng feature → Operations search/trace viewer
    Temporary data theo từng feature → Retention Cleanup tối đa 7 ngày

Agent Harness, Orchestrator, scheduler, audit và retention chỉ được mở rộng bên trong phase có feature đầu tiên sử dụng chúng. Chúng không tạo thành phase BE độc lập.

## 5. Danh sách màn hình cần triển khai

Route chỉ là định hướng; nhóm có thể đổi tên nhưng phải giữ nguyên trách nhiệm và quyền truy cập.

| ID | Màn hình / route gợi ý | Người dùng | Mục tiêu và trạng thái UI bắt buộc | Capability BE đi kèm | Phase |
| --- | --- | --- | --- | --- | --- |
| SCR-01 | Đăng ký / đăng nhập — `/register`, `/login` | Guest | Form validation, submitting, lỗi credential, session expired | Auth/session API, password policy, structured auth errors | 2 |
| SCR-02 | App Shell & lịch sử — `/`, `/history` | User | Navigation, loading/empty/error, danh sách conversation/plan/trip/summary | Ownership-aware history query, pagination | 2 |
| SCR-03 | Hồ sơ du lịch — `/profile` | User | Sở thích, nhu cầu đặc biệt, ngân sách thường dùng, save/error state | Profile read/update, validation, audit metadata | 2 |
| SCR-04 | Hội thoại yêu cầu — `/trips/new/chat` | User | Message list, composer, upload, GPS purpose, streaming, cancel/retry/reconnect | Conversation/message API, SSE, Planner requirement extraction, media/location API | 3 |
| SCR-05 | Xác nhận yêu cầu — `/trip-requests/:id/summary` | User | Xem/sửa trường, missing-field errors, version conflict, confirm | Versioned trip-request summary, mandatory-field validation, confirm command | 3 |
| SCR-06 | Khám phá địa điểm — `/trip-requests/:id/discovery` | User | Search/filter, list-map sync, radius, image search, selection, loading/empty/error | Catalog/search/ranking API, PostGIS radius query, vision tool, selection persistence | 4 |
| SCR-07 | Chi tiết địa điểm — `/places/:id` | User | Lý do đề xuất, review hợp lệ, source, checked-at, confidence | Place detail/provenance API, public-approved review query | 4 |
| SCR-08 | Tiến trình tạo lộ trình — `/trip-requests/:id/planning` | User | Planning/evaluating/revising/completed/failed, cancel/retry | Orchestrator run API/SSE, Planner→Critic workflow, idempotency | 5 |
| SCR-09 | So sánh lộ trình — `/trip-requests/:id/itineraries` | User | So sánh 1–4 phương án, chi phí, cảnh báo, trade-off, chọn plan | Itinerary query/selection, provenance, version control | 5 |
| SCR-10 | Chỉnh sửa và proposal — `/itineraries/:id/edit` | User | Manual editor, chat change request, diff, accept/reject, conflict | Edit commands, recalculation, Agent proposal, Critic recheck, atomic approval | 6 |
| SCR-11 | Kế hoạch cuối trên mobile — `/trips/:id/plan` | User | Timeline theo ngày, transport, luggage, offline/error-friendly view, reopen draft | Finalize/reopen lifecycle, immutable finalized version | 6 |
| SCR-12 | Tìm và so sánh dịch vụ — `/trips/:id/booking` | User | Filter/compare offer, stale/unavailable, giá cuối, provider, điều kiện | Booking Agent, provider normalization, offer expiry | 7 |
| SCR-13 | Kiểm tra thông tin và chuyển hướng — `/trips/:id/booking/review` | User | Passenger form, review data, external-transaction notice, explicit continue | Passenger validation/redaction, allow-listed safe redirect, redirect audit | 7 |
| SCR-14 | Trip Companion — `/trips/:id/companion` | User | Activate/end trip, GPS toggle/status, today plan, activity suggestions | Trip lifecycle, per-trip consent, GPS ingestion/retention | 8 |
| SCR-15 | Q&A và nhận diện địa điểm — `/trips/:id/guide` | User | Text/image question, low-confidence choices, sources, failure fallback | Place Q&A/vision skills and tools, output validation/provenance | 8 |
| SCR-16 | Thuyết minh — modal/panel trong Companion | User | Proximity prompt, play/pause, transcript; tuyệt đối không autoplay | Proximity/dedup logic, narration/TTS adapter, signed audio URL | 8 |
| SCR-17 | Cảnh báo và replanning — `/trips/:id/alerts` | User | Alert severity/timeline, unavailable place, proposal diff, accept/reject | Weather Monitor, impact rules, Planner/Critic proposal, approval/version API | 9 |
| SCR-18 | Viết và quản lý review — `/places/:id/reviews/new`, `/reviews/:id` | User | Rating/comment, private default, request-public/status, edit privacy | Review state machine, ownership, moderation submission | 10 |
| SCR-19 | Review công khai và báo cáo — trong place detail | User | Approved reviews, report dialog/status | Public review query, report/rate-limit workflow | 10 |
| SCR-20 | Hàng đợi kiểm duyệt — `/operations/moderation` | Operator / Admin | Filters, review/report detail, approve/reject/hide, reason required | Role-protected moderation commands, immutable moderation audit | 10 |
| SCR-21 | Bản nháp tổng kết — `/trips/:id/summary` | User | Đã đi/bỏ qua/phát sinh, evidence/confidence, sửa trước confirm | Idempotent completion job, activity classification/correction API | 11 |
| SCR-22 | Chi phí, nhật ký và media — panel trong summary | User | Optional expenses, variance, diary, photos, ratings/reviews | Expense calculation, media retention, reuse review module | 11 |
| SCR-23 | Gợi ý chuyến tiếp theo — `/trips/:id/next-trip` | User | 1–3 cards, explanation, start planning | Confirmed-summary profile update, suggestion API, prefilled conversation | 11 |
| SCR-24 | Tìm kiếm audit — `/operations/audit` | Operator / Admin | Filter theo trip/Agent/error/time, pagination, role-aware states | Protected audit search, redaction, retention-aware results | 12 |
| SCR-25 | Chi tiết trace — `/operations/audit/:id` | Admin / Operator | Purpose + Ticket ID gate, execution flow, tool/handoff/error/version | Access audit, trace projection, role/field-level authorization | 12 |
| SCR-26 | Quản lý địa điểm du lịch — `/admin/places` | Admin | CRUD danh mục địa điểm, giờ mở cửa, giá vé, kích hoạt/tạm ẩn | Curated place catalog admin API, spatial updates | 4 |
| SCR-27 | Kiến nghị & Phê duyệt Maker-Checker — `/operations/proposals` | Operator / Admin | Form tạo kiến nghị (Operator), duyệt/từ chối kèm ghi chú (Admin) | Operator proposal API, approval auto-update catalog | 10 |
| SCR-28 | Quản trị người dùng & phân quyền — `/admin/users` | Admin | Danh sách người dùng, khóa/mở khóa tài khoản (ban), gán quyền Operator | User administration API, ban policy enforcement | 2 |
| SCR-29 | Cấu hình hệ thống — `/admin/configs` | Admin | Tinh chỉnh tham số toàn cục (retention days, chu kỳ quét) | System configuration API | 12 |

### 5.1. Thành phần dùng chung bắt buộc

- App shell, session guard, role guard và not-found/forbidden/error boundary.
- Typed API client sinh từ OpenAPI; FE không khai báo lại DTO bằng tay.
- Source/checked-at/confidence panel dùng chung cho SCR-07, SCR-09, SCR-15 và SCR-17.
- Decision summary/warning/trade-off component dùng chung cho SCR-09, SCR-10 và SCR-17.
- Upload component với type/size/progress/cancel và error state.
- Consent component không đánh đồng browser permission với consent của sản phẩm.
- Responsive/mobile baseline; keyboard navigation, focus management và screen-reader labels.

### 5.2. Quy tắc navigation và authorization

- Guest chỉ truy cập SCR-01.
- User chỉ xem/sửa dữ liệu thuộc tài khoản của mình; không truy cập SCR-20, SCR-24 đến SCR-29.
- Operator truy cập kiểm duyệt (SCR-20), tạo kiến nghị Maker-Checker (SCR-27), và tra cứu audit theo Ticket ID (SCR-24, SCR-25).
- Admin toàn quyền truy cập khu vực vận hành và quản trị (SCR-20 đến SCR-29), bao gồm quản lý kho địa điểm, phê duyệt kiến nghị Maker-Checker, quản trị người dùng, cấu hình hệ thống và xem biểu đồ dòng thực thi AI.
- UI guard chỉ cải thiện trải nghiệm; BE luôn kiểm tra role và ownership độc lập.
- Deep link vào dữ liệu đã hết hạn phải hiển thị trạng thái rõ ràng, không trả signed URL đã vô hiệu.

## 6. Cấu trúc repository định hướng

    tour-guide-agent/
    ├── backend/
    │   ├── app/
    │   │   ├── api/
    │   │   ├── modules/
    │   │   ├── ai/{orchestrator,agents,harness}/
    │   │   ├── infrastructure/
    │   │   ├── jobs/
    │   │   └── main.py
    │   ├── migrations/
    │   └── tests/
    ├── frontend/
    │   ├── src/{app,features,shared}/
    │   └── tests/
    ├── infra/
    ├── docs/
    ├── scripts/
    ├── Makefile
    └── README.md

Tên thư mục có thể đổi trong Phase 1, nhưng ranh giới API Service, AI Orchestrator, Agent Harness và background jobs phải rõ; đây là module, không phải microservice riêng.

## 7. Requirement Coverage by Phase

| Requirement group | Planned phase |
| --- | --- |
| Account, profile, history | Phase 2 |
| US01–US08 — Trip request | Phase 3 |
| US09–US15 — Destination discovery | Phase 4 |
| US16–US22 — Itinerary generation/comparison | Phase 5 |
| US23–US28 — Customization/finalization | Phase 6 |
| US29–US34 — Booking/logistics guidance | Phase 7 |
| US35–US41 — In-trip guide | Phase 8 |
| US42–US45 — Realtime monitoring | Phase 9 |
| US46–US51 — Reviews/moderation/ranking | Phase 10 |
| US52–US64 — Summary/personalization | Phase 11 |
| US65–US67 — User transparency | Phases 3–11; cross-check Phase 12 |
| US68–US70 — Operations audit/trace | Phase 12 |
| Production hardening/release | Phase 13 |

## 8. Project-wide Definition of Done

Mỗi vertical slice chỉ hoàn thành khi:

- [ ] Acceptance criteria có bằng chứng test và Product Owner đã nghiệm thu trên increment tích hợp.
- [ ] FE dùng API thật ở checkpoint; lint, type check, component test, accessibility check và production build pass.
- [ ] BE lint, type check, unit/integration/contract tests pass trên PostgreSQL/PostGIS thật khi liên quan.
- [ ] OpenAPI, generated client và UI/API error states đồng bộ; CI phát hiện contract drift.
- [ ] Authorization, ownership, validation, idempotency và audit được kiểm tra tại trust boundary.
- [ ] Dữ liệu biến động có source/checked-at/confidence; dữ liệu tạm có `expires_at` và cleanup test.
- [ ] Không log secret, dữ liệu nhạy cảm không cần thiết hoặc chain-of-thought thô.
- [ ] Migration tương thích triển khai, có rollback; FE/BE artifacts deploy được và smoke test pass.
- [ ] UI có loading/empty/error/retry, responsive và accessibility cơ bản.

Các lệnh chuẩn dự kiến:

    make check
    make test
    make integration-test
    make e2e
    make build

## 9. Quy tắc đồng bộ kế hoạch

- Mọi mã SCR trong tài liệu này phải xuất hiện ở đúng phase của [plan.md](plan.md).
- Khi thêm/bỏ màn hình, cập nhật đồng thời screen inventory, requirement coverage, API contract và E2E journey.
- Không tách “làm toàn bộ BE trước” hoặc “làm toàn bộ UI sau”. Technical spike ngắn được phép, nhưng checkpoint vẫn phải là vertical increment.
- Có thể phát triển FE bằng mock và BE bằng fake provider song song sau khi chốt contract; cả hai phải hội tụ vào API thật trước khi đóng phase.
