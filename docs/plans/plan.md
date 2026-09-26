# Implementation Plan: Tour Guide Agent

> **Status:** Draft — cần được nhóm dự án xem xét và phê duyệt trước khi bắt đầu triển khai.

## Phase 1 - Project Foundation

Mục tiêu của Phase này là tạo repository có thể chạy, kiểm tra và phát triển cục bộ nhưng chưa thêm nghiệp vụ sản phẩm.

### Step 1.1 - Establish Repository Layout

**Mô tả** Tạo cấu trúc thư mục chung cho backend, frontend, hạ tầng, scripts và tài liệu.  
Phân chia rõ trách nhiệm của từng module trong kiến trúc modular monolith để người mới dễ xác định nơi đặt code.  
Bước này chỉ dựng bộ khung repository, chưa thêm code nghiệp vụ hoặc abstraction chưa cần thiết.

**Acceptance Criteria**
- [ ] Cấu trúc thư mục khớp kiến trúc đã thống nhất và không tạo microservice riêng.
- [ ] README mô tả cách cài đặt, chạy và vị trí các module chính.
- [ ] Không có placeholder code nghiệp vụ hoặc abstraction chưa cần thiết.

**Verification** Kiểm tra cây thư mục và toàn bộ đường dẫn trong README tồn tại.

**Dependencies** Không có (None).
**Files Related** README.md, backend/, frontend/, infra/, scripts/.

### Step 1.2 - Bootstrap FastAPI Backend

**Mô tả** Khởi tạo ứng dụng FastAPI tối thiểu cùng cấu hình và health endpoint.  
Thiết lập lifecycle hooks, cách đọc biến môi trường và cấu trúc test cơ bản để backend có thể chạy độc lập.  
Kết quả cần là một backend khởi động ổn định, báo lỗi cấu hình rõ ràng và có smoke test ban đầu.

**Acceptance Criteria**
- [x] Backend khởi động được và GET /health trả trạng thái thành công.
- [x] Cấu hình đọc từ environment với validation khi thiếu biến bắt buộc.
- [x] Có smoke test cho application startup và health endpoint.

**Verification** Chạy backend test và gọi /health trong môi trường local.

**Dependencies** Step 1.1.
**Files Related** backend/pyproject.toml, backend/app/main.py, backend/app/config.py, backend/tests/.

### Step 1.3 - Bootstrap React Frontend

**Mô tả** Khởi tạo React và TypeScript với application shell, router và test runner tối thiểu.  
Chuẩn bị route cho trang chủ và trang not-found, đồng thời thiết lập type check, unit test và production build.  
Bước này tạo nền frontend có thể chạy local và sẵn sàng để phát triển các màn hình nghiệp vụ sau đó.

**Acceptance Criteria**
- [ ] Frontend chạy local và hiển thị application shell.
- [ ] Có route cho home và trang not-found.
- [ ] Type check, unit test và production build chạy thành công.

**Verification** Chạy frontend test, type check và build; mở ứng dụng trong trình duyệt.

**Dependencies** Step 1.1.
**Files Related** frontend/package.json, frontend/src/app/, frontend/src/main.tsx, frontend/tests/.

### Step 1.4 - Provision Local Data Services

**Mô tả** Chuẩn bị PostgreSQL/PostGIS và Object Storage cho môi trường phát triển local.  
Backend phải kết nối được các dịch vụ qua biến môi trường và có health check cùng volume lưu dữ liệu rõ ràng.  
Sau bước này, nhóm có thể kiểm tra truy vấn không gian và luồng upload/download bằng dữ liệu thử nghiệm.

**Acceptance Criteria**
- [ ] Một lệnh khởi động được PostgreSQL/PostGIS và Object Storage.
- [ ] Backend kết nối được cả hai dịch vụ bằng environment variables.
- [ ] Có health check và volume local rõ ràng.

**Verification** Khởi động compose, chạy truy vấn PostGIS và upload/download một object thử nghiệm.

**Dependencies** Steps 1.1–1.2.
**Files Related** infra/compose.yaml, infra/env/, backend/app/infrastructure/.

### Step 1.5 - Define Configuration and Secret Boundaries

**Mô tả** Chuẩn hóa cách khai báo cấu hình và secret cho từng môi trường chạy.  
Không cho phép credential, token hoặc dữ liệu nhạy cảm xuất hiện trong source control hay log ứng dụng.  
Hệ thống phải dừng với thông báo rõ ràng khi thiếu cấu hình bắt buộc và cung cấp tệp environment mẫu an toàn.

**Acceptance Criteria**
- [ ] Có environment example không chứa credential thật.
- [ ] Startup thất bại rõ ràng khi thiếu secret bắt buộc.
- [ ] Logging filter che credential, token và dữ liệu nhạy cảm đã định nghĩa.

**Verification** Chạy test cấu hình thiếu/sai và quét repository tìm secret mẫu.

**Dependencies** Steps 1.2 và 1.4.
**Files Related** .env.example, backend/app/config.py, frontend env declarations, .gitignore.

### Checkpoint - Foundation Ready

- [ ] Local stack khởi động từ repository sạch.
- [ ] Backend health check và frontend shell hoạt động.
- [ ] PostgreSQL/PostGIS và Object Storage được kiểm tra.
- [ ] make check, make test và make build pass.
- [ ] Nhóm dự án duyệt cấu trúc trước Phase 2.

---

## Phase 2 - Core Platform and Persistence

Mục tiêu là xây nền dữ liệu, tài khoản, quyền truy cập và API contract đủ để các vertical slice sau không phải tự tạo lại hạ tầng.

**Màn hình:** SCR-01 (đăng ký/đăng nhập), SCR-02 (App Shell/lịch sử), SCR-03 (hồ sơ du lịch).

### Step 2.1 - Create Migration and Persistence Foundation

**Mô tả** Chọn ORM và migration tool dùng thống nhất cho backend, sau đó tạo migration đầu tiên.  
Thiết lập cách quản lý transaction tại application boundary để route không phải tự xử lý chi tiết persistence.  
Cơ chế migration phải chạy được từ database trống, rollback được và được kiểm tra trên PostgreSQL thật.

**Acceptance Criteria**
- [ ] Migration có thể nâng từ database trống và rollback trong môi trường test.
- [ ] Transaction được quản lý tại application boundary, không rò rỉ vào route.
- [ ] Integration test chạy trên PostgreSQL thật, không thay bằng database khác.

**Verification** Chạy migrate up/down/up và integration test persistence.

**Dependencies** Phase 1.
**Files Related** backend/migrations/, backend/app/infrastructure/database/, backend/tests/integration/.

### Step 2.2 - Model Core Travel Data

**Mô tả** Xây dựng schema tối thiểu cho user, profile, conversation, trip request, trip, place và itinerary.  
Bổ sung itinerary version cùng audit metadata, đồng thời định nghĩa rõ quan hệ, constraint, tiền tệ và múi giờ.  
Mục tiêu là có nền dữ liệu đủ chặt chẽ để các module sau dùng chung mà không tạo lại cấu trúc riêng.

**Acceptance Criteria**
- [ ] Quan hệ và constraint ngăn dữ liệu mồ côi hoặc version kế hoạch không hợp lệ.
- [ ] Trường tiền tệ, múi giờ và thời điểm dùng kiểu dữ liệu rõ ràng.
- [ ] Các bảng dữ liệu tạm thời có created_at và expires_at.

**Verification** Migration test và test constraint với dữ liệu hợp lệ/không hợp lệ.

**Dependencies** Step 2.1.
**Files Related** backend/app/modules/*/models.py, backend/migrations/, persistence tests.

### Step 2.3 - Add PostGIS Location Support

**Mô tả** Bổ sung kiểu dữ liệu không gian cho địa điểm, sự kiện GPS và vị trí chuyến đi bằng PostGIS.  
Cung cấp các truy vấn cơ bản về bán kính và khoảng cách, dùng cùng SRID và spatial index để bảo đảm hiệu năng.  
Dữ liệu GPS phải gắn với trạng thái consent và thời điểm hết hạn không quá 7 ngày.

**Acceptance Criteria**
- [ ] Place và GPS event dùng kiểu không gian có SRID thống nhất.
- [ ] Query bán kính trả đúng kết quả và dùng spatial index.
- [ ] GPS event có consent state và expires_at tối đa 7 ngày.

**Verification** Integration test với các tọa độ trong/ngoài bán kính và kiểm tra query plan.

**Dependencies** Step 2.2.
**Files Related** place/location models, migrations, geospatial repositories, integration tests.

### Step 2.4 - Implement Authentication and Role Authorization

**Mô tả** Triển khai đăng ký, đăng nhập, đăng xuất và quản lý phiên người dùng.  
Áp dụng ba role là user, operator và admin (theo cơ chế Permission-based authorization), đồng thời kiểm tra quyền sở hữu dữ liệu giữa các tài khoản.  
Các lỗi authentication và authorization phải có cấu trúc nhất quán để frontend xử lý rõ ràng.

**Acceptance Criteria**
- [ ] User có thể tạo tài khoản, đăng nhập, đăng xuất và truy cập dữ liệu thuộc sở hữu.
- [ ] Operator/admin chỉ truy cập endpoint vận hành đúng quyền.
- [ ] Authentication failure và authorization failure trả lỗi nhất quán.

**Verification** API integration test cho happy path, sai credential, sai role và cross-account access.

**Dependencies** Steps 2.1–2.2.
**Files Related** backend/app/modules/auth/, account schema, API routes, frontend session layer.

### Step 2.5 - Deliver Profile and History Slice

**Mô tả** Cho phép người dùng cập nhật hồ sơ du lịch và xem lại dữ liệu lịch sử của mình.  
Lịch sử bao gồm conversation, plan, trip và summary nhưng tuyệt đối không được lộ dữ liệu của tài khoản khác.  
Frontend cần thể hiện đầy đủ trạng thái loading, empty và error cho cả hồ sơ lẫn lịch sử.

**Acceptance Criteria**
- [ ] User cập nhật sở thích, nhu cầu đặc biệt và ngân sách thường dùng.
- [ ] History chỉ hiển thị dữ liệu của tài khoản hiện tại.
- [ ] Frontend có trạng thái loading, empty và error.

**Verification** Backend integration test và frontend component/E2E test cho profile/history.

**Dependencies** Steps 2.2 và 2.4.
**Files Related** backend/app/modules/profile/, frontend/src/features/profile/, history queries.

### Step 2.6 - Establish OpenAPI Contract and Typed Client

**Mô tả** Chuẩn hóa cách API trả lỗi, validation error, phân trang và request ID trong toàn hệ thống.  
Hoàn thiện tài liệu OpenAPI và sinh typed API client để frontend không phải khai báo lại contract bằng tay.  
CI cần phát hiện khi generated client không còn đồng bộ với API contract hiện tại.

**Acceptance Criteria**
- [ ] OpenAPI mô tả authentication, validation error và response chính.
- [ ] Frontend dùng generated types/client thay vì khai báo trùng contract.
- [ ] CI phát hiện generated client bị lệch với API contract.

**Verification** Generate client từ clean state và chạy contract test cùng frontend type check.

**Dependencies** Steps 1.2–1.3 và 2.4.
**Files Related** backend OpenAPI config, frontend/src/shared/api/, generation script, CI.

### Checkpoint - Core Platform Ready

- [ ] Migration chạy từ database trống.
- [ ] Auth, profile và history hoạt động end-to-end.
- [ ] PostGIS query bán kính có integration test.
- [ ] Frontend client đồng bộ OpenAPI.
- [ ] Không có cross-account data leak trong test.

---

## Nguyên tắc triển khai từ Phase 3

Từ Phase 3, mọi phase là một **vertical increment** có thể kiểm thử và triển khai độc lập. FE và BE cùng bắt đầu từ một OpenAPI contract, interaction states và acceptance scenarios đã thống nhất.

- FE có thể dùng mock server và BE có thể dùng fake provider để làm song song, nhưng checkpoint bắt buộc chạy với FE + API + database thật.
- Agent Harness, Orchestrator, scheduler, audit và retention chỉ được xây vừa đủ trong feature đầu tiên cần dùng; không tách thành phase backend riêng.
- Mỗi API mới phải có màn hình hoặc consumer cụ thể trong cùng phase. Mỗi màn hình mới phải có API/business logic thật trước khi đóng phase.
- Mỗi phase bao gồm migration, authorization/ownership, error handling, telemetry, automated tests, smoke test và rollback liên quan.
- Chỉ có ba Agent: Planner, Critic/Evaluator, Booking & Logistics. Vision, search, weather và TTS là skill/tool.
- Không lưu chain-of-thought thô. Chỉ lưu kết quả có cấu trúc, lý do tóm tắt, nguồn, tool/result cần thiết và version.
- Dữ liệu biến động có source, checked-at và confidence. GPS/media/memory/log chi tiết có `expires_at` tối đa 7 ngày.
- Một phase chỉ “Done” khi đạt Project-wide Definition of Done trong [plan-requirement.md](plan-requirement.md).

---

## Phase 3 - Tiếp nhận và xác nhận yêu cầu chuyến đi

**Kết quả nghiệp vụ:** Người dùng tạo yêu cầu bằng hội thoại tiếng Việt, bổ sung ngữ cảnh và xác nhận summary đủ dữ liệu bắt buộc.

- **Màn hình:** SCR-04, SCR-05.
- **Phạm vi:** US01–US08; nền transparency US65–US67.
- **Phụ thuộc:** Phase 2.

### Slice 3.1 - Hội thoại và trích xuất yêu cầu

**FE**

- [ ] Xây SCR-04 gồm message list, composer, lịch sử phiên, processing/cancel/retry và SSE reconnect.
- [ ] Hiển thị câu hỏi làm rõ trong hội thoại và cho biết profile nào đang được dùng để cá nhân hóa.

**BE**

- [ ] Tạo conversation/message API, ownership policy và SSE event ID để reconnect không nhân đôi message.
- [ ] Xây phần tối thiểu của Agent Runtime, Model Gateway, Prompt/Skill Registry, validator, timeout/cancel và structured trace cho use case này.
- [ ] Nối Planner qua Orchestrator port để trích xuất ngày đi, nơi xuất phát, điểm đến, thời lượng, ngân sách, sở thích và người đi cùng; route không gọi model provider trực tiếp.

**Tích hợp và kiểm thử**

- [ ] Prompt tiếng Việt tạo structured draft; timeout, malformed output và reconnect đều có trạng thái lỗi có thể retry.

### Slice 3.2 - Summary, GPS và media

**FE**

- [ ] Xây SCR-05 để xem/sửa từng trường, hiển thị missing-field/version-conflict và confirm version cuối.
- [ ] SCR-04 hỗ trợ upload có progress/type-size error và GPS consent với mục đích “nơi xuất phát” hoặc “tâm tìm kiếm”.

**BE**

- [ ] Kết hợp prompt, profile và dữ liệu đã xác nhận; ngày đi, nơi xuất phát, ngân sách là bắt buộc.
- [ ] Version hóa summary; chỉ status `confirmed` được dùng cho phase sau.
- [ ] Tạo signed upload/download, safe file validation và location/media ownership.
- [ ] Thêm in-process scheduler với PostgreSQL coordination lock; Retention Cleanup idempotent cho GPS/media/memory/log phát sinh, tối đa 7 ngày.

**Tích hợp và kiểm thử**

- [ ] Login → chat → clarification → edit → confirm chạy end-to-end sau refresh.
- [ ] GPS/media sai mục đích phải hỏi lại; time-travel test chứng minh dữ liệu hết hạn bị chặn trước khi xóa.

### Checkpoint Phase 3

- [ ] SCR-04 và SCR-05 dùng API thật trên staging, không còn phụ thuộc mock.
- [ ] Confirmed summary là contract đầu vào ổn định cho Phase 4.
- [ ] Trace không chứa chain-of-thought; consent, ownership và retention tests pass.

---

## Phase 4 - Khám phá và lựa chọn địa điểm

**Kết quả nghiệp vụ:** Người dùng tìm, hiểu, so sánh và chọn địa điểm bằng danh sách, bản đồ, bán kính hoặc ảnh.

- **Màn hình:** SCR-06, SCR-07.
- **Phạm vi:** US09–US15; US51 khi có review hợp lệ; US65–US67.
- **Phụ thuộc:** Phase 3 và PostGIS ở Step 2.3.

### Slice 4.1 - Catalog, ranking và lựa chọn

**FE**

- [ ] Xây SCR-06 với search/filter, list/map, loading/empty/error và selection state.
- [ ] Xây SCR-07 với lý do đề xuất, review hợp lệ, source, checked-at và confidence.
- [ ] Chọn/bỏ chọn/đổi địa điểm phải cập nhật draft summary hiện tại.

**BE**

- [ ] Tạo curated destination catalog, seed/import có kiểm duyệt và paginated search/detail API.
- [ ] Mở rộng Tool Registry/provider ports; ranking dùng confirmed request, profile và chỉ public-approved review.
- [ ] Trả explanation có cấu trúc và version hóa selection; không trả reasoning thô.

**Tích hợp và kiểm thử**

- [ ] Ranking ổn định bằng fixture, không dùng review private/pending và giải thích được các tín hiệu chính.

### Slice 4.2 - Radius và image discovery

**FE**

- [ ] SCR-06 đồng bộ list/map, vị trí nhập tay hoặc GPS đã consent, radius control và fallback khi map/GPS lỗi.
- [ ] Hỗ trợ chọn/upload ảnh, processing state, similarity reason và nhiều khả năng khi confidence thấp.

**BE**

- [ ] Tạo PostGIS radius API với SRID/index thống nhất, distance/radius/page limits.
- [ ] Thêm vision tool adapter có schema, timeout và fake contract; đối chiếu đặc điểm ảnh với catalog.

**Tích hợp và kiểm thử**

- [ ] Search text/radius/image → compare → select → updated summary chạy E2E.
- [ ] Spatial query dùng index; media/trace mới tiếp tục tuân thủ retention.

### Checkpoint Phase 4

- [ ] SCR-06 và SCR-07 hoạt động trên staging với provenance/confidence nhất quán.
- [ ] Danh sách địa điểm đã chọn sẵn sàng cho Phase 5.

---

## Phase 5 - Tạo và so sánh lộ trình khả thi

**Kết quả nghiệp vụ:** Người dùng nhận 1–4 lộ trình đã qua Critic bắt buộc, so sánh và chọn một phương án.

- **Màn hình:** SCR-08, SCR-09.
- **Phạm vi:** US16–US22; US65–US67.
- **Phụ thuộc:** Phase 4.

### Slice 5.1 - Planner → Critic workflow

**FE**

- [ ] Xây SCR-08 với planning/evaluating/revising/completed/failed, cancel/retry và SSE reconnect.

**BE**

- [ ] Hoàn thiện Orchestrator handoff Planner → Critic → Planner; không tạo Agent thứ tư.
- [ ] Planner tạo 1–4 phương án gồm ngày, điểm, lưu trú, hoạt động, chặng, phương tiện, chi phí và hành lý.
- [ ] Critic bắt buộc kiểm tra ngân sách, giờ mở cửa, travel time và an toàn; hard failure quay lại Planner, soft warning được giữ.
- [ ] Lưu run/idempotency state và agent/prompt/tool versions; retry không tạo plan trùng.

**Tích hợp và kiểm thử**

- [ ] Không itinerary nào hiển thị nếu chưa có Critic pass; provider/model failure không để plan nửa vời.

### Slice 5.2 - So sánh và lựa chọn

**FE**

- [ ] Xây SCR-09 so sánh tối đa 4 phương án theo lịch ngày, chi phí, thời lượng, transport, luggage và highlights.
- [ ] Hiển thị lý do xếp hạng, warning/trade-off và component source/checked-at/confidence dùng chung; hỗ trợ mobile/keyboard.

**BE**

- [ ] Tạo comparison/selection API với ownership, immutable version và optimistic concurrency.
- [ ] Chuẩn hóa money/timezone/provenance; không trình bày dữ liệu đã hết hạn như dữ liệu hiện tại.

**Tích hợp và kiểm thử**

- [ ] Generate → Critic → compare → select chạy E2E bằng backend thật.

### Checkpoint Phase 5 - Planning MVP

- [ ] SCR-08 và SCR-09 deploy được và chỉ hiển thị phương án khả thi.
- [ ] Selected itinerary là đầu vào ổn định của Phase 6.

---

## Phase 6 - Tùy chỉnh, phê duyệt và lưu kế hoạch cuối

**Kết quả nghiệp vụ:** Người dùng chỉnh tay hoặc yêu cầu Agent sửa đúng phạm vi, xem diff và chủ động chấp nhận/từ chối trước khi finalize.

- **Màn hình:** SCR-10, SCR-11.
- **Phạm vi:** US23–US28; US65–US67.
- **Phụ thuộc:** Phase 5.

### Slice 6.1 - Manual edit và tính lại

**FE**

- [ ] Xây editor SCR-10 cho add/update/delete/reorder điểm, lưu trú, chặng, hoạt động, vật dụng; có validation, draft undo và conflict UI.

**BE**

- [ ] Tạo edit commands, immutable versions và optimistic lock.
- [ ] Tính lại lịch, chi phí, transport, lodging, luggage/activity; thay đổi quan trọng bắt buộc qua Critic.

**Tích hợp và kiểm thử**

- [ ] Concurrent edits không ghi đè im lặng; dữ liệu phụ thuộc luôn nhất quán.

### Slice 6.2 - Agent proposal và user approval

**FE**

- [ ] SCR-10 nhận yêu cầu sửa bằng chat, hiển thị scope/diff/reason/warning và accept/reject.

**BE**

- [ ] Planner chỉ tạo proposal chưa áp dụng và đúng phạm vi; thay đổi quan trọng qua Critic.
- [ ] Accept/reject idempotent: accept tạo version mới nguyên tử, reject giữ current version và ghi audit.

**Tích hợp và kiểm thử**

- [ ] Proposal không đổi plan trước accept; double submit không tạo hai version; Agent không sửa ngoài scope.

### Slice 6.3 - Finalize và mobile plan

**FE**

- [ ] Xây SCR-11 dạng mobile-first; reopen plan đã chốt phải tạo draft mới.

**BE**

- [ ] Tạo lifecycle draft/selected/finalized/active; finalized version là baseline cho booking, active trip và summary.

**Tích hợp và kiểm thử**

- [ ] Edit/propose → Critic → accept/reject → finalize → mobile view chạy E2E.

### Checkpoint Phase 6

- [ ] SCR-10, SCR-11 deploy được; version history đủ khôi phục trạng thái.
- [ ] Phase sau không ghi đè finalized version.

---

## Phase 7 - Tìm dịch vụ và hướng dẫn đặt chỗ

**Kết quả nghiệp vụ:** Người dùng so sánh dịch vụ và tự chuyển sang đối tác; hệ thống không thực hiện giao dịch.

- **Màn hình:** SCR-12, SCR-13.
- **Phạm vi:** US29–US34.
- **Phụ thuộc:** Phase 6.

### Slice 7.1 - Search và comparison

**FE**

- [ ] Xây SCR-12 với filter/compare theo giá cuối, độ phù hợp, provider, điều kiện hủy/đổi; có stale/unavailable states.

**BE**

- [ ] Mở rộng Harness/Orchestrator cho Booking & Logistics Agent; provider ports có allow-list, timeout, rate limit và bounded retry.
- [ ] Chuẩn hóa offer/currency/source/checked-at/expiry/conditions; offer không phải booking confirmation.

**Tích hợp và kiểm thử**

- [ ] Finalized itinerary → search → compare chạy với sandbox/fake contract; offer hết hạn buộc refresh.

### Slice 7.2 - Passenger data và safe redirect

**FE**

- [ ] Xây SCR-13 với minimum passenger data, review screen, final price/conditions và external-transaction notice.

**BE**

- [ ] Validate/redact passenger data; redirect/deep link chỉ đến allow-listed domain và luôn ghi audit.
- [ ] Guardrail cấm Agent/API tự đặt chỗ, giữ tiền, lưu payment credential hoặc xác nhận thanh toán.

**Tích hợp và kiểm thử**

- [ ] Redirect chỉ sau explicit user action; test fake domain, parameter injection và cross-account access.

### Checkpoint Phase 7

- [ ] SCR-12 → SCR-13 → safe redirect chạy E2E.
- [ ] UI, API và trace đều thể hiện rõ ranh giới với đối tác.

---

## Phase 8 - Trip Companion và thuyết minh tại điểm đến

**Kết quả nghiệp vụ:** Người dùng kích hoạt chuyến đi, kiểm soát GPS, hỏi/nhận diện địa điểm và nghe audio khi chủ động yêu cầu.

- **Màn hình:** SCR-14, SCR-15, SCR-16.
- **Phạm vi:** US35–US41.
- **Phụ thuộc:** Phase 6; retention scheduler từ Phase 3.

### Slice 8.1 - Trip lifecycle và GPS consent

**FE**

- [ ] Xây SCR-14 với activate/end trip, GPS toggle/status/last-send và thông tin sử dụng/xóa dữ liệu.

**BE**

- [ ] Tạo trip lifecycle và location ingestion; kiểm tra consent trên mọi request, GPS hết hạn tối đa 7 ngày.

**Tích hợp và kiểm thử**

- [ ] Toggle off dừng FE upload và BE từ chối event mới; ownership tests bao phủ nhiều account/trip.

### Slice 8.2 - Q&A và place identification

**FE**

- [ ] Xây SCR-15 cho text/image question, activity suggestions, source panel và low-confidence choices.

**BE**

- [ ] Thêm skills/tools cho lịch sử, văn hóa, giá vé, opening hours, điều kiện tham quan và vision identification.
- [ ] Output validator bắt buộc provenance cho dữ liệu biến động; thiếu nguồn phải nêu giới hạn.

**Tích hợp và kiểm thử**

- [ ] Q&A trong/ngoài itinerary và identification có success/low-confidence/failure E2E.

### Slice 8.3 - Proximity và user-controlled audio

**FE**

- [ ] Xây SCR-16 với proximity prompt, play/pause và transcript; tuyệt đối không autoplay.

**BE**

- [ ] PostGIS proximity + dedup; narration/TTS adapter, signed audio URL và retention.

**Tích hợp và kiểm thử**

- [ ] Tắt GPS dừng proximity; radius/dedup tests ngăn spam; không consent vẫn dùng được chức năng không phụ thuộc vị trí.

### Checkpoint Phase 8

- [ ] SCR-14 → SCR-15/SCR-16 chạy E2E trên staging.
- [ ] GPS/media/audio đúng consent, ownership và retention.

---

## Phase 9 - Theo dõi thời gian thực và replanning có phê duyệt

**Kết quả nghiệp vụ:** Active trip được kiểm tra định kỳ; sự cố tạo cảnh báo/phương án thay thế nhưng không tự sửa finalized plan.

- **Màn hình:** SCR-17.
- **Phạm vi:** US42–US45; tái sử dụng US25–US27.
- **Phụ thuộc:** Phases 6 và 8.

### Slice 9.1 - Monitoring và alert

**FE**

- [ ] Xây SCR-17 với alert inbox/timeline, severity, unavailable place và source/checked-at/confidence.

**BE**

- [ ] Mở rộng scheduler bằng idempotent Weather Monitor và PostgreSQL lock cho multi-worker.
- [ ] Chỉ quét active trip; kiểm tra weather/travel time/opening hours, material-change threshold, dedup và job metrics.

**Tích hợp và kiểm thử**

- [ ] Significant fixture tạo đúng một alert; thay đổi nhỏ không cảnh báo; dashboard phát hiện job trễ/lỗi.

### Slice 9.2 - Alternative proposal và approval

**FE**

- [ ] SCR-17 hiển thị proposal diff cho điểm, phương tiện, thời gian, chi phí/warning và accept/reject.

**BE**

- [ ] Job chỉ yêu cầu Planner tạo proposal, Critic kiểm tra và tái sử dụng atomic approval/version flow Phase 6.

**Tích hợp và kiểm thử**

- [ ] Provider change → job → alert → proposal → accept/reject chạy E2E; retry không nhân đôi alert/version.

### Checkpoint Phase 9

- [ ] SCR-17 deploy được; scheduler an toàn trên multi-worker và có telemetry.
- [ ] Không có code path tự đổi finalized plan khi chưa có user approval.

---

## Phase 10 - Review, kiểm duyệt và tín hiệu xếp hạng

**Kết quả nghiệp vụ:** Review mặc định private, chỉ public sau yêu cầu và kiểm duyệt; chỉ review hợp lệ ảnh hưởng ranking.

- **Màn hình:** SCR-18, SCR-19, SCR-20.
- **Phạm vi:** US46–US51; nền dùng lại cho US59–US60.
- **Phụ thuộc:** Phases 4 và 8.

### Slice 10.1 - Review private và publication request

**FE**

- [ ] Xây SCR-18 với rating/comment, private default và privacy/moderation status.
- [ ] SCR-19 chỉ hiển thị approved public reviews và report dialog/status.

**BE**

- [ ] Tạo review state machine với ownership, visit context và immutable moderation history.
- [ ] Ngăn private/pending review xuất hiện trong public query, ranking, logs không được phép hoặc account khác.

**Tích hợp và kiểm thử**

- [ ] Create → private → request public chạy E2E; privacy toggle không bypass moderation.

### Slice 10.2 - Moderation, reporting và ranking

**FE**

- [ ] Xây SCR-20 cho operator với filters, report/review detail, approve/reject/hide và reason bắt buộc.

**BE**

- [ ] Spam/policy/relevance/verified-trip checks trước publish; operator override có role và audit.
- [ ] Tạo report workflow/rate limit; ranking projection chỉ dùng public + approved + relevant reviews.

**Tích hợp và kiểm thử**

- [ ] Private/pending/rejected/removed review không ảnh hưởng SCR-06; user role không gọi được moderation API.

### Checkpoint Phase 10

- [ ] SCR-18/SCR-19/SCR-20 chạy end-to-end.
- [ ] Privacy default, moderation và ranking signal có security/integration tests.

---

## Phase 11 - Tổng kết chuyến đi và vòng cá nhân hóa

**Kết quả nghiệp vụ:** Người dùng nhận draft tổng kết, chỉnh hành trình/chi phí/kỷ niệm, xác nhận vào lịch sử và bắt đầu chuyến tiếp theo.

- **Màn hình:** SCR-21, SCR-22, SCR-23.
- **Phạm vi:** US52–US64.
- **Phụ thuộc:** Phases 8–10.

### Slice 11.1 - Completion và actual route

**FE**

- [ ] Xây SCR-21 với early-end, notification và nhóm đã đi/bỏ qua/phát sinh có evidence/confidence và correction.

**BE**

- [ ] Thêm idempotent Trip Completion job cho scheduled end/early end; tạo đúng một draft.
- [ ] Đối chiếu finalized plan với interaction, confirmation và consented GPS; không có GPS vẫn tạo draft từ evidence còn lại.

**Tích hợp và kiểm thử**

- [ ] Job retry/multi-worker không tạo draft trùng; user correction được lưu trước confirm.

### Slice 11.2 - Expenses, diary, media và place reviews

**FE**

- [ ] Xây SCR-22 với optional expense categories, variance, diary, photos, trip rating và place reviews.

**BE**

- [ ] Lưu amount/currency/category, tính absolute/percentage variance và phân biệt “không nhập” với 0.
- [ ] Tái sử dụng media retention và review privacy/moderation, không tạo model song song.

**Tích hợp và kiểm thử**

- [ ] Có thể hoàn tất summary không nhập chi phí; calculations và private-default reviews đúng.

### Slice 11.3 - Confirm summary và next trip

**FE**

- [ ] Review-before-confirm giải thích dữ liệu dùng cá nhân hóa; SCR-23 hiển thị 1–3 cards và start planning.

**BE**

- [ ] Confirm summary nguyên tử, khóa history và cập nhật preference/spending/travel pace chỉ từ confirmed data.
- [ ] Sinh 1–3 suggestions; start endpoint tạo conversation/request mới với preference prefill.

**Tích hợp và kiểm thử**

- [ ] Double confirm không tạo/cập nhật trùng; confirm → profile/history → suggestion → new conversation chạy E2E.

### Checkpoint Phase 11

- [ ] SCR-21 → SCR-22 → SCR-23 chạy E2E.
- [ ] Confirmed summary là dữ liệu bền vững, không phải Agent memory tạm thời.

---

## Phase 12 - Audit, privacy và hỗ trợ vận hành

**Kết quả nghiệp vụ:** Operator/Admin được cấp quyền có thể truy vết an toàn; user transparency và retention được kiểm chứng xuyên hệ thống.

- **Màn hình:** SCR-24, SCR-25, SCR-29.
- **Phạm vi:** US68–US70; US75; hoàn thiện US65–US67 và shared retention.
- **Phụ thuộc:** Audit events Phases 3–11 và role foundation Phase 2.

### Slice 12.1 - Audit search và protected detail

**FE**

- [ ] Xây SCR-24 với filters trip/Agent/error/time, pagination và role-aware states.
- [ ] SCR-25 bắt buộc form purpose + Ticket ID trước khi tải detail; không prefetch nội dung bảo vệ.

**BE**

- [ ] Chuẩn hóa events từ API, Orchestrator, Agents, tools/providers/jobs; redact secrets, passenger data và PII không cần thiết.
- [ ] Tạo role-based search/detail API; mọi detail attempt ghi actor, timestamp, IP, purpose và Ticket ID.

**Tích hợp và kiểm thử**

- [ ] Thiếu role/purpose/ticket thì không tải detail; mỗi access/denial có audit.

### Slice 12.2 - Trace viewer và retention verification

**FE**

- [ ] SCR-25 hiển thị redacted input, tool/result, source, handoff, validation, error và versions cho Admin.
- [ ] Deep link dữ liệu đã dọn hiển thị “đã hết hạn”, không tạo broken UI.

**BE**

- [ ] Xây trace projection theo correlation/request/run ID, đánh dấu span thiếu/hết hạn và giới hạn query.
- [ ] Cleanup đầy đủ GPS, media gốc, working/trip memory, detailed logs; mark-expired trước delete/anonymize.
- [ ] Không xóa profile, finalized plan, approved review hoặc confirmed summary; thêm cleanup metrics/safe retry.

**Tích hợp và kiểm thử**

- [ ] Admin tái dựng được Planner→Critic/Booking fixture lỗi mà không thấy secret/chain-of-thought.
- [ ] Time-travel E2E và cleanup/restore drill bao phủ PostgreSQL + Object Storage.

### Checkpoint Phase 12

- [ ] SCR-24 → purpose/ticket gate → SCR-25 chạy đúng role.
- [ ] Source/reason/warning nhất quán ở discovery, planning, proposal và alert.
- [ ] Retention/consent matrix đầy đủ và cleanup được giám sát.

---

## Phase 13 - Production readiness và phát hành

**Kết quả nghiệp vụ:** Toàn bộ vertical slices vận hành an toàn trong production, có observability, recovery, rollback và UAT truy vết được.

Phase này không thêm nghiệp vụ mới; quality/telemetry cơ bản đã đi cùng từng phase.

### Slice 13.1 - Packaging và observability

**FE**

- [ ] Production bundle/image, runtime config, redacted error reporting, web vitals và accessibility/responsive regression.

**BE**

- [ ] Production image, migration job, health/readiness và telemetry cho API/SSE/Agents/providers/scheduler.
- [ ] SLO/dashboard/alerts cho latency, error, provider/token usage, job lag, cleanup và storage.

**Tích hợp**

- [ ] Immutable FE/BE artifacts từ cùng commit; deploy staging và smoke auth, chat, discovery, planning, finalized plan, scheduler.

### Slice 13.2 - Security, performance và recovery

**FE**

- [ ] Kiểm tra XSS/upload/redirect, session expiry, sensitive caching và performance chat/map/comparison/Companion.

**BE**

- [ ] Threat model auth/ownership, upload/signed URL, SSRF/provider, redirect, prompt/tool boundaries và rate limits.
- [ ] Load/failure tests cho API/SSE/PostGIS/scheduler/providers; backup/restore drill PostgreSQL/Object Storage.

### Slice 13.3 - Traceability, UAT và rollout

**FE + BE + Product/Ops**

- [ ] Map US01–US70 và SCR-01–SCR-25 đến automated/UAT tests.
- [ ] UAT năm journey: planning; customization/finalize; booking guidance; active-trip response; post-trip summary.
- [ ] Runbooks cho provider outage, stuck Agent run, missed job, retention failure và rollback-compatible migration.
- [ ] Canary/feature-flag rollout, theo dõi SLO và diễn tập rollback trước general availability.

### Final Checkpoint - Production Ready

- [ ] Tất cả checkpoint Phase 1–12 đạt; không còn blocker severity cao.
- [ ] Deploy/rollback, migration, backup/restore và scheduler failover đã diễn tập.
- [ ] UAT, security, accessibility, performance và traceability được phê duyệt.

---

## Milestones và dependency sequence

| Milestone | Phases | Increment triển khai được | Điều kiện đầu ra |
| --- | --- | --- | --- |
| M0 - Platform Ready | 1–2 | Stack, identity, profile, persistence, typed API | Platform dùng chung |
| M1 - Planning MVP | 3–5 | Confirm request, discovery, itinerary khả thi | Selected itinerary |
| M2 - Finalized Trip | 6–7 | Customize/finalize và booking guidance | Immutable finalized plan, safe redirect |
| M3 - Active Trip | 8–9 | Companion, consented GPS, narration, alert/replanning | Active lifecycle, scheduler |
| M4 - Learning Loop | 10–11 | Trusted reviews, summary, personalization | Confirmed summary cập nhật profile |
| M5 - Operable Release | 12–13 | Audit/privacy operations và production rollout | UAT/SLO/security/recovery approved |

### Dependency không được bỏ qua

- Phase 4 chỉ dùng summary đã confirmed.
- Phase 5 chỉ hiển thị itinerary sau mandatory Critic check.
- Phases 6–9 không ghi đè finalized plan; Agent/job chỉ tạo proposal.
- Phase 7 chỉ hướng dẫn/chuyển hướng, không giao dịch.
- Phases 8–11 chỉ dùng GPS khi consent của trip đang bật.
- Phase 10 chỉ đưa public-approved review vào ranking.
- Phase 11 chỉ cập nhật profile từ confirmed summary.
- Phase 12 chỉ mở technical detail sau authorization + purpose + Ticket ID.

## Chiến lược phát triển song song FE–BE

- Đầu phase: FE lead, BE lead và Product chốt screen states, OpenAPI schema, error codes và E2E scenarios.
- Trong phase: FE dùng generated client + mock theo contract; BE dùng fake provider + contract tests. Contract drift làm CI fail.
- Giữa phase: tích hợp thin thread sớm từ UI → API → DB/provider trước khi mở rộng edge cases.
- Cuối phase: bỏ mock khỏi acceptance path, chạy migration, integration/E2E, accessibility, security smoke và deploy staging.
- Breaking API/migration phải có version hoặc backward-compatible rollout để FE và BE deploy an toàn.

## Requirement coverage

| Nhóm yêu cầu | Phase chính | Màn hình |
| --- | --- | --- |
| Account/profile/history | 2 | SCR-01–SCR-03 |
| US01–US08 | 3 | SCR-04–SCR-05 |
| US09–US15 | 4 | SCR-06–SCR-07 |
| US16–US22 | 5 | SCR-08–SCR-09 |
| US23–US28 | 6 | SCR-10–SCR-11 |
| US29–US34 | 7 | SCR-12–SCR-13 |
| US35–US41 | 8 | SCR-14–SCR-16 |
| US42–US45 | 9 | SCR-17 |
| US46–US51 | 10 | SCR-18–SCR-20 |
| US52–US64 | 11 | SCR-21–SCR-23 |
| US65–US67 | 3–11; verify 12 | Shared transparency components |
| US68–US70 | 12 | SCR-24–SCR-25 |

## Rủi ro chính và kiểm soát

| Rủi ro | Kiểm soát bắt buộc |
| --- | --- |
| FE dùng mock quá lâu | Contract-first, generated client, drift CI, E2E API thật ở checkpoint |
| AI/provider không ổn định | Structured output, validator, bounded retry, golden eval |
| Dữ liệu biến động lỗi thời | Source + checked-at + confidence + expiry/refresh |
| Planner bỏ qua feasibility | Mandatory Critic và test không cho bypass |
| Agent/job tự sửa plan | Proposal-only, atomic approval, immutable versions |
| Rò GPS/media/log | Consent, ownership, redaction, signed URL, 7-day cleanup |
| Scheduler chạy trùng | PostgreSQL lock, idempotency, unique constraints |
| Booking vượt phạm vi | No-payment guardrail, allow-list, redirect security tests |
| Scope tăng do hạ tầng/Agent | Modular monolith, đúng ba Agent, chỉ thêm khi có số liệu |

## Quyết định cần chốt trước phase

- Phase 3: LLM provider/model, SSE reconnect policy, media types/limits.
- Phase 4: curated sources, provenance/confidence rules, map provider/quota.
- Phase 5: hard feasibility rules, warning taxonomy, eval thresholds.
- Phase 7: booking sandbox, deep-link contract, minimum passenger data.
- Phase 8: proximity threshold, notification policy, TTS/audio UX.
- Phase 9: monitor interval, material-change thresholds, notification channels.
- Phase 10: community policy, moderation SLA và report outcomes.
- Phase 11: expense categories, confirmation semantics, personalization consent.
- Phase 13: hosting, SLO/RTO/RPO, rollout và production data licensing.

Mỗi quyết định phải có owner/deadline. Fake adapter hoặc feature flag giúp giữ tiến độ nhưng không đủ để tuyên bố production-ready.

## Phê duyệt kế hoạch

- [ ] Product Owner xác nhận scope/thứ tự US01–US70 và SCR-01–SCR-25.
- [ ] FE lead xác nhận routes, interaction states, accessibility và typed-client workflow.
- [ ] BE/AI lead xác nhận modular-monolith boundaries, three-Agent design và provider contracts.
- [ ] Security/Operations xác nhận consent, retention, audit, deployment và rollback.
- [ ] Nhóm cam kết không đóng phase khi UI và BE chưa tích hợp end-to-end.
