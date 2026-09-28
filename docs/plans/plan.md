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
Với cấu hình hợp lệ, backend phải khởi động và GET `/health` trả HTTP 200; khi thiếu biến bắt buộc, process thoát khác 0 và thông báo tên biến bị thiếu; smoke test kiểm tra cả hai trường hợp.

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
Backend kết nối PostgreSQL/PostGIS và Object Storage qua biến môi trường; compose khai báo named volume cho từng dịch vụ và dữ liệu vẫn tồn tại sau khi container được tạo lại.
Sau bước này, nhóm có thể kiểm tra truy vấn không gian và luồng upload/download bằng dữ liệu thử nghiệm.

**Acceptance Criteria**
- [ ] Một lệnh khởi động được PostgreSQL/PostGIS và Object Storage.
- [ ] Backend kết nối được cả hai dịch vụ bằng environment variables.
- [ ] PostgreSQL/PostGIS và Object Storage có health check; named volume giữ dữ liệu sau khi recreate container.

**Verification** Khởi động compose, chạy truy vấn PostGIS và upload/download một object thử nghiệm.

**Dependencies** Steps 1.1–1.2.
**Files Related** infra/compose.yaml, infra/env/, backend/app/infrastructure/.

### Step 1.5 - Define Configuration and Secret Boundaries

**Mô tả** Chuẩn hóa cách khai báo cấu hình và secret cho từng môi trường chạy.
Không cho phép credential, token hoặc dữ liệu nhạy cảm xuất hiện trong source control hay log ứng dụng.
Khi thiếu cấu hình bắt buộc, process phải thoát khác 0 và liệt kê tên biến bị thiếu; tệp environment mẫu chỉ chứa tên biến cùng giá trị giả không dùng được như credential thật.

**Acceptance Criteria**
- [ ] Có environment example không chứa credential thật.
- [ ] Startup thoát khác 0 và liệt kê tên secret bắt buộc bị thiếu mà không in giá trị secret.
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

**Màn hình:** SCR-01 (đăng ký/đăng nhập), SCR-02 (App Shell/lịch sử), SCR-03 (hồ sơ du lịch), SCR-28 (quản trị người dùng và phân quyền).

**Phạm vi:** Nền tảng dùng chung; US74.

### Step 2.1 - Create Migration and Persistence Foundation

**Mô tả** Chọn ORM và migration tool dùng thống nhất cho backend, sau đó tạo migration đầu tiên.
Application service mở, commit hoặc rollback transaction; API route chỉ gọi application service và không trực tiếp điều khiển transaction.
Cơ chế migration phải chạy được từ database trống, rollback được và được kiểm tra trên PostgreSQL thật.

**Acceptance Criteria**
- [ ] Migration có thể nâng từ database trống và rollback trong môi trường test.
- [ ] Application service quản lý transaction; API route không gọi trực tiếp commit hoặc rollback.
- [ ] Integration test chạy trên PostgreSQL thật, không thay bằng database khác.

**Verification** Chạy migrate up/down/up và integration test persistence.

**Dependencies** Phase 1.
**Files Related** backend/migrations/, backend/app/infrastructure/database/, backend/tests/integration/.

### Step 2.2 - Model Account, Profile and Session Data

**Mô tả** Chỉ tạo schema nền cho `users`, `user_profile` và `agent_session` để phục vụ authentication, profile, session ownership và quản trị tài khoản trong Phase 2.
Không tạo trước `trip_requests`, `trips`, các bảng dữ liệu địa điểm, itinerary hoặc các bảng nghiệp vụ của Phase sau; mỗi bảng domain được thêm bằng migration trong vertical slice đầu tiên sử dụng bảng đó.

**Acceptance Criteria**
- [ ] Quan hệ và constraint của tài khoản, hồ sơ và session ngăn dữ liệu mồ côi hoặc truy cập sai chủ sở hữu.
- [ ] `users.status` và `users.role` dùng đúng enum hiện có; repository chỉ ghi hoặc so sánh `agent_session.user_id` sau khi application service đã chuyển user ID sang chuỗi UUID canonical.
- [ ] Migration Phase 2 chỉ tạo `users`, `user_profile` và `agent_session`; không tạo các bảng còn lại trong `DATABASE.txt`.

**Verification** Chạy migration up/down/up từ database trống và integration test constraint cho account/profile/session.

**Dependencies** Step 2.1.
**Files Related** account/profile/session models, backend/migrations/, persistence tests.

### Step 2.3 - Define Shared Persistence Conventions

**Mô tả** Chuẩn hóa quy tắc dùng lại cho các migration ở Phase sau mà chưa tạo các bảng nghiệp vụ tương ứng trong `DATABASE.txt` ở Phase 2.
Các quy tắc bao gồm tiền tệ, thời gian, PostGIS SRID/index, retention và cách API biểu diễn datetime.

Thực hiện cập nhật toàn bộ database đã chốt vào bên trong models folder của Backend và tiến hành chạy migration. 

**Acceptance Criteria**
- [ ] Giá trị `TIMESTAMP` được hiểu theo múi giờ hệ thống đã cấu hình; API luôn trả datetime kèm offset rõ ràng.
- [ ] `DATETIME` trong tài liệu domain được ánh xạ sang kiểu PostgreSQL/ORM tương ứng; `planned_date` được hiểu theo ngày/giờ địa phương của chuyến đi khi bảng itinerary được tạo ở Phase 5.
- [ ] Dữ liệu không gian dùng SRID 4326 và spatial index 
- [ ] Toàn bộ database trong DATABASE.txt được cập nhật vào bên trong folder models/ của Backend và chạy migration thành công với `alembic`

**Verification** Unit/contract test cho type mapping, datetime serialization, SRID convention và retention-deadline calculation.

**Dependencies** Step 2.1.
**Files Related** shared database types, ORM conventions, retention utilities, contract tests.

### Step 2.4 - Implement Authentication and Role Authorization

**Mô tả** Triển khai đăng ký, đăng nhập, đăng xuất và quản lý phiên người dùng.
Áp dụng role-based authorization trực tiếp từ ba giá trị `USER`, `OPERATOR` và `ADMIN` hiện có; không tạo permission table, dynamic permission mapping hoặc abstraction quyền riêng.

Lỗi authentication và authorization dùng chung schema OpenAPI gồm `code`, `message`, `details` và `request_id`; authentication trả HTTP 401, authorization trả HTTP 403.

**Acceptance Criteria**
- [ ] User có thể tạo tài khoản, đăng nhập, đăng xuất và truy cập dữ liệu thuộc sở hữu.
- [ ] Endpoint/action áp dụng trực tiếp rule của `USER`, `OPERATOR` và `ADMIN`; Operator/Admin chỉ truy cập endpoint vận hành đúng role.
- [ ] Session ownership dùng chuỗi UUID canonical của người dùng đã xác thực; việc chuyển `agent_session.user_id` thành UUID foreign key không phải điều kiện tiên quyết.
- [ ] Authentication failure trả HTTP 401, authorization failure trả HTTP 403 và cả hai dùng schema lỗi chung gồm `code`, `message`, `details` và `request_id`.

**Verification** API integration test cho happy path, sai credential, sai role, cross-account access và chuyển UUID xác thực sang chuỗi canonical khi kiểm tra session ownership.

**Dependencies** Steps 2.1–2.2.
**Files Related** backend/app/modules/auth/, account schema, API routes, frontend session layer.

### Step 2.5 - Deliver Profile and History Slice

**Mô tả** Cho phép người dùng cập nhật hồ sơ du lịch và xem lịch sử `agent_session` thuộc tài khoản của mình trong Phase 2.
Phase 2 chỉ đưa `agent_session` vào lịch sử tài khoản; `itineraries`, `trips` và `trip_summaries` được bổ sung vào lịch sử khi phase sở hữu từng bảng được triển khai.
Frontend cần thể hiện đầy đủ trạng thái loading, empty và error cho cả hồ sơ lẫn lịch sử.

**Acceptance Criteria**
- [ ] User cập nhật sở thích, nhu cầu đặc biệt và ngân sách thường dùng.
- [ ] Lịch sử Phase 2 chỉ hiển thị các bản ghi `agent_session` của tài khoản hiện tại; khu vực `itineraries`, `trips` và `trip_summaries` hiển thị empty state cho đến khi các bảng tương ứng được triển khai.
- [ ] Frontend có trạng thái loading, empty và error.

**Verification** Backend integration test và frontend component/E2E test cho `user_profile`, lịch sử `agent_session`, ownership và empty state của `itineraries`, `trips`, `trip_summaries` chưa triển khai.

**Dependencies** Steps 2.2 và 2.4.
**Files Related** backend/app/modules/profile/, frontend/src/features/profile/, history queries.

### Step 2.6 - Establish OpenAPI Contract and Typed Client

**Mô tả** Chuẩn hóa cách API trả lỗi, validation error, phân trang và request ID trong toàn hệ thống.
Hoàn thiện tài liệu OpenAPI và sinh typed API client để frontend không phải khai báo lại contract bằng tay.

**Acceptance Criteria**
- [ ] OpenAPI mô tả authentication, validation error và response chính.
- [ ] Frontend dùng generated types/client thay vì khai báo trùng contract.
- [ ] CI phát hiện generated client bị lệch với API contract.

**Verification** Generate client từ clean state và chạy contract test cùng frontend type check.

**Dependencies** Steps 1.2–1.3 và 2.4.
**Files Related** backend OpenAPI config, frontend/src/shared/api/, generation script, CI.

### Step 2.7 - User and Role Administration

**Mô tả** Cung cấp giao diện quản trị để Admin tra cứu danh sách tài khoản, xem trạng thái và role hiện tại.
Admin có thể ban/unban tài khoản, gán role `OPERATOR` cho tài khoản `USER` hoặc thu hồi role này về `USER`.
Backend phải đọc trạng thái và role mới nhất từ `users` khi xác thực request để tài khoản bị ban hoặc bị thu hồi quyền không tiếp tục sử dụng quyền cũ.

**FE**

- [ ] Xây SCR-28 tại `/admin/users` với tìm kiếm, filter theo trạng thái/role, phân trang và trạng thái loading/empty/error.
- [ ] Cung cấp action ban/unban và gán/thu hồi Operator với confirm dialog, pending state và kết quả thành công/thất bại rõ ràng; cập nhật lại dòng tài khoản sau khi backend xác nhận.

**BE**

- [ ] Tạo Admin-only API để liệt kê tài khoản và cập nhật `users.status` hoặc `users.role`; backend phải đọc trạng thái và role mới nhất khi xác thực mỗi request.
- [ ] Ban chuyển `users.status` sang `BANNED`, unban chuyển về `ACTIVE`; tài khoản `BANNED` không thể đăng nhập và request từ session hiện có bị từ chối.
- [ ] Gán/thu hồi Operator chỉ chuyển `users.role` giữa `USER` và `OPERATOR`; không thay đổi role `ADMIN` qua luồng này và role mới có hiệu lực từ request tiếp theo.
- [ ] Chỉ `ADMIN` được gọi API quản trị tài khoản; `USER` và `OPERATOR` nhận HTTP 403 theo schema lỗi chung gồm `code`, `message`, `details` và `request_id`.

**Tích hợp và kiểm thử**

- [ ] Với US74, SCR-28 → list/filter → ban/unban → gán/thu hồi Operator chạy end-to-end; refresh trang giữ đúng trạng thái và role đã lưu.
- [ ] Test role matrix, session đang hoạt động của tài khoản bị ban và request tiếp theo của tài khoản vừa bị thu hồi Operator.

**Dependencies** Steps 2.4 và 2.6.
**Files Related** backend/app/modules/auth/, account administration API, frontend account administration feature, integration/E2E tests.

### Checkpoint - Core Platform Ready

- [ ] Migration account/profile/session chạy từ database trống.
- [ ] Auth, `user_profile` và lịch sử `agent_session` hoạt động end-to-end.
- [ ] Shared persistence conventions có contract test; migration Phase 2 chỉ chứa `users`, `user_profile` và `agent_session`.
- [ ] Frontend client đồng bộ OpenAPI.
- [ ] Không có cross-account data leak trong test.
- [ ] SCR-28 hoàn thành luồng quản trị tài khoản của US74 end-to-end; trạng thái và role mới được backend áp dụng từ request tiếp theo.

---

## Nguyên tắc triển khai từ Phase 3

Từ Phase 3, mọi phase là một **vertical increment** có thể kiểm thử và triển khai độc lập. FE và BE cùng bắt đầu từ một OpenAPI contract, interaction states và acceptance scenarios đã thống nhất.

- FE có thể dùng mock server và BE có thể dùng fake provider để làm song song, nhưng checkpoint bắt buộc chạy với FE + API + database thật.
- Agent Harness, Orchestrator, scheduler, audit và retention chỉ được thêm khi frontend route hoặc background job được nêu tên trong cùng phase sử dụng chúng; không tách thành phase backend riêng.
- Mỗi API mới phải có frontend route hoặc background job được nêu tên trong cùng phase. Mỗi màn hình mới phải có API/business logic thật trước khi đóng phase.
- Mỗi phase bao gồm migration, authorization/ownership, error handling, telemetry, automated tests, smoke test và rollback liên quan.
- Migration được sở hữu bởi vertical slice đầu tiên sử dụng dữ liệu: Phase 3 thêm `messages`, `trip_requests`, `media_files`, `agent_runs`, `tool_calls`, `information_sources` và `agent_memories`; Phase 4 thêm `place_categories`, `places`, `place_narrations`, `trip_request_selected_places` và `place_reviews`; Phase 5 thêm `itineraries`, `itinerary_days`, `itinerary_activities`, `itinerary_transits` và `evaluation_results`; Phase 6 thêm `itinerary_proposals` và `trips`; Phase 7 thêm `booking_offers`; Phase 8 thêm `gps_location_events`; Phase 9 thêm `trip_alerts`; Phase 10 thêm `review_reports`, `review_moderation_logs` và `operator_proposals`; Phase 11 thêm `trip_summaries`, `trip_summary_places`, `trip_expenses` và `next_trip_suggestions`; Phase 12 thêm `audit_access_logs` và `system_configs`.
- Chỉ có ba Agent: Planner, Critic/Evaluator, Booking & Logistics. Vision, search, weather và TTS là skill/tool.
- Không lưu chain-of-thought thô. Chỉ lưu kết quả có cấu trúc, lý do tóm tắt, nguồn, tool/result cần thiết và version.
- Giá vé, giờ mở cửa, thời tiết, thời gian di chuyển và booking offer phải có bản ghi `information_sources` với `source_name`, `source_url`, `checked_at` và `confidence`. `gps_location_events`, `agent_memories`, `agent_runs` và `tool_calls` dùng `expires_at`; trước Phase 12, hạn của `media_files` được tính từ `created_at` cộng giá trị retention trong application config, và từ Phase 12 dùng `temporary_data_retention_days` trong `system_configs`. API phải chặn truy cập ngay khi hết hạn, kể cả khi cleanup chưa chạy.
- Một phase chỉ “Done” khi đạt Project-wide Definition of Done trong [plan-requirement.md](plan-requirement.md).

---

## Phase 3 - Tiếp nhận và xác nhận yêu cầu chuyến đi

**Kết quả nghiệp vụ:** Người dùng gửi `messages` trong một `agent_session`, bổ sung ngữ cảnh và xác nhận bản ghi `trip_requests` đã có đủ dữ liệu bắt buộc.

- **Màn hình:** SCR-04, SCR-05.
- **Phạm vi:** US01–US08; nền transparency US65–US67.
- **Phụ thuộc:** Phase 2.

### Slice 3.1 - Hội thoại và trích xuất yêu cầu

**FE**

- [ ] Xây SCR-04 gồm danh sách `messages`, composer, lịch sử `agent_session`, processing/cancel/retry và SSE reconnect.
- [ ] Hiển thị câu hỏi làm rõ trong hội thoại.
**BE**

- [ ] Tạo API cho `agent_session` và `messages`; mỗi SSE event có ID để reconnect không tạo trùng bản ghi `messages`.
- [ ] Xây Agent Runtime, Model Gateway, registry cho prompt template/skill, validator và timeout/cancel đủ cho Slice 3.1; mỗi lần thực thi ghi `agent_runs`, mỗi tool call ghi `tool_calls`, còn nguồn dữ liệu biến động ghi `information_sources`.
- [ ] Nối Planner qua Orchestrator port để trích xuất ngày đi, nơi xuất phát, điểm đến, thời lượng, ngân sách, sở thích và người đi cùng; API route không gọi model provider một cách trực tiếp.

**Yêu cầu**

- [ ] Planner tạo hoặc cập nhật `trip_requests` ở trạng thái `DRAFT` từ `messages`; timeout, model output sai schema, validation failure và SSE reconnect failure có mã lỗi riêng và hỗ trợ retry mà không tạo bản ghi trùng.

### Slice 3.2 - Trip request, GPS và media

**FE**

- [ ] Xây SCR-05 để xem/sửa các trường của `trip_requests`, hiển thị missing-field/version-conflict và xác nhận đúng `version` hiện tại.
- [ ] SCR-04 hỗ trợ upload có progress/type-size error và GPS consent với mục đích “nơi xuất phát” hoặc “tâm tìm kiếm”.

**BE**

- [ ] Tạo hoặc cập nhật `trip_requests` từ `messages.content`, `user_profile` và các trường người dùng đã xác nhận; `start_date`, `origin_name`, `budget` và `currency` là bắt buộc trước khi xác nhận.
- [ ] Tăng `trip_requests.version` khi nội dung thay đổi; chỉ bản ghi có `status = CONFIRMED` được dùng cho phase sau.
- [ ] Tạo signed upload/download, safe file validation và location/media ownership.
- [ ] Thêm in-process scheduler với PostgreSQL coordination lock; Retention Cleanup idempotent cho GPS/memory/log dựa trên `expires_at` và cho media tạm thời dựa trên `media_files.created_at` cộng thời lượng retention trong cấu hình. Khi media hết hạn, API từ chối truy cập trước, sau đó cleanup xóa cả object và metadata.

**Tích hợp và kiểm thử**

- [ ] Login → tạo `agent_session` → gửi `messages` → clarification → sửa `trip_requests` → chuyển sang `CONFIRMED` chạy end-to-end sau refresh.
- [ ] GPS/media sai mục đích phải hỏi lại; time-travel test chứng minh dữ liệu hết hạn bị chặn trước khi xóa.

### Checkpoint Phase 3

- [ ] SCR-04 và SCR-05 dùng API thật trên staging, không còn phụ thuộc mock.
- [ ] `trip_requests` có `status = CONFIRMED` và `version` xác định là đầu vào duy nhất của Phase 4.
- [ ] `agent_runs.input_summary`, `agent_runs.output_summary`, `agent_runs.decision_summary` và `tool_calls` không chứa chain-of-thought; consent, ownership và retention tests pass.

---

## Phase 4 - Khám phá và lựa chọn địa điểm

**Kết quả nghiệp vụ:** Người dùng tìm, hiểu, so sánh và chọn địa điểm bằng danh sách, bản đồ, bán kính hoặc ảnh; Admin duy trì dữ liệu địa điểm, danh mục phân loại và nội dung thuyết minh.

- **Màn hình:** SCR-06, SCR-07, SCR-26.
- **Phạm vi:** US09–US15; US65–US67; US73.
- **Phụ thuộc:** Phase 3; shared persistence conventions ở Step 2.3; role foundation ở Step 2.4.

### Slice 4.1 - Dữ liệu địa điểm, ranking và lựa chọn

**FE**

- [ ] Xây SCR-06 với search/filter, list/map, loading/empty/error và selection state.
- [ ] Xây SCR-07 với lý do đề xuất, source, checked-at và confidence. Chỉ hiển thị review công khai đã được duyệt khi có dữ liệu; không có review phải hiển thị empty state hợp lệ và không chặn thao tác chọn địa điểm.
- [ ] Chọn, bỏ chọn hoặc đổi địa điểm phải cập nhật `trip_request_selected_places` và tăng `trip_requests.version` của bản ghi `DRAFT` hiện tại.

**BE**

- [ ] Tạo bộ dữ liệu địa điểm được kiểm duyệt, hỗ trợ seed/import và paginated search/detail API.
- [ ] Phase 4 chưa sử dụng `place_reviews` làm tín hiệu ranking; trước mắt chỉ dùng `places.category_id`, `province`, `min_price`, `max_price`, `trip_requests.destination_text`, `budget`, `preferences` và `user_profile.travel_preferences`, `special_needs`, `default_budget` để xếp hạng. Không dùng `places.average_rating` nếu giá trị này được tổng hợp từ review.
- [ ] Place detail chỉ đọc `place_reviews.status = PUBLIC` để hiển thị khi đã có bản ghi; chưa có dữ liệu phải trả danh sách rỗng. Phase 4 không tạo hoặc kiểm duyệt review và không dùng review để thay đổi ranking.
- [ ] Search/detail API trả `selection_reason` có cấu trúc cho `trip_request_selected_places` và yêu cầu `expected_version` khớp `trip_requests.version` khi thay đổi lựa chọn; không trả reasoning thô.

**Tích hợp và kiểm thử**

- [ ] Ranking dùng fixture cố định từ `places`, `place_categories`, `trip_requests` có `status = CONFIRMED` và `user_profile`; kết quả phải lặp lại cùng thứ tự, trả score trong API response mà không ghi vào cột database và nêu rõ các field đã dùng để tính score.
- [ ] SCR-07 hoạt động đúng khi API trả danh sách review rỗng; empty state không chặn compare/select hoặc làm Phase 4 thất bại.

### Slice 4.2 - Radius và image discovery

**FE**

- [ ] SCR-06 đồng bộ list/map, vị trí nhập tay hoặc GPS đã consent, radius control và fallback khi map/GPS lỗi.
- [ ] Hỗ trợ chọn/upload ảnh và processing state; vision adapter trả tối đa ba `places` ứng viên kèm similarity reason, đồng thời trả nhiều hơn một ứng viên khi `confidence` thấp hơn ngưỡng được khai báo trong contract của adapter.

**BE**

- [ ] Tạo PostGIS radius API với SRID/index thống nhất, distance/radius/page limits.
- [ ] Thêm vision tool adapter có schema, timeout và fake contract; đối chiếu đặc điểm ảnh với dữ liệu trong `places`.

**Tích hợp và kiểm thử**

- [ ] Search text/radius/image → compare → ghi `trip_request_selected_places` → cập nhật `trip_requests.version` chạy E2E.
- [ ] Spatial query dùng index; `media_files`, `agent_runs` và `tool_calls` phát sinh trong luồng này tiếp tục tuân thủ retention.

### Slice 4.3 - Quản trị địa điểm và nội dung thuyết minh

**FE**

- [ ] Xây SCR-26 tại `/admin/places` để tìm kiếm, tạo, chỉnh sửa và xóa danh mục; đồng thời tạo, chỉnh sửa, kích hoạt/ẩn và xóa địa điểm cùng nội dung thuyết minh. Giao diện có loading, empty, validation, confirm-delete và error states.
- [ ] Form địa điểm hỗ trợ danh mục, thông tin mô tả, địa chỉ, tọa độ, giờ mở cửa, khoảng giá, tiền tệ và ảnh; form thuyết minh hỗ trợ tiêu đề, transcript, audio và trạng thái hoạt động.

**BE**

- [ ] Tạo Admin-only CRUD API cho `place_categories`, `places` và `place_narrations`; validate slug, quan hệ danh mục–địa điểm, tọa độ, khoảng giá và metadata audio trước khi ghi.
- [ ] Kích hoạt/ẩn `places` và `place_narrations` bằng `is_active`. Chỉ xóa `place_categories` khi không còn `places.category_id` tham chiếu và chỉ xóa `places` khi không còn tham chiếu từ `place_narrations`, `trip_request_selected_places`, `itinerary_activities`, `place_reviews`, `trip_summary_places` hoặc `operator_proposals`; nếu còn tham chiếu thì trả conflict và không xóa.
- [ ] API tra cứu công khai chỉ trả địa điểm và nội dung thuyết minh đang hoạt động; thay đổi được áp dụng cho request mới ngay sau khi transaction commit.

**Tích hợp và kiểm thử**

- [ ] Với US73, SCR-26 chạy end-to-end cho luồng Admin create/edit/hide/activate/delete địa điểm, danh mục phân loại và nội dung thuyết minh; dữ liệu bị ẩn không xuất hiện trong search/detail public.
- [ ] `USER` và `OPERATOR` không gọi được API quản trị; test xóa dữ liệu có/không có tham chiếu và xác nhận nội dung trong `place_narrations` không bị temporary-media cleanup xóa.

### Checkpoint Phase 4

- [ ] SCR-06 và SCR-07 hiển thị `information_sources.source_name`, `source_url`, `checked_at` và `confidence` cho giá vé, giờ mở cửa hoặc dữ liệu biến động được trả về.
- [ ] Ranking Phase 4 chỉ phụ thuộc `places`, `place_categories`, `trip_requests` có `status = CONFIRMED` và `user_profile`; checkpoint không phụ thuộc dữ liệu hoặc moderation review của Phase 10.
- [ ] `trip_request_selected_places` của `trip_requests` đã xác nhận là đầu vào chọn địa điểm cho Phase 5.
- [ ] SCR-26 hoàn thành luồng quản trị `place_categories`, `places` và `place_narrations` của US73 end-to-end; test chứng minh chỉ `ADMIN` được ghi dữ liệu và các trường hợp xóa có tham chiếu trả conflict.

---

## Phase 5 - Tạo và so sánh lộ trình khả thi

**Kết quả nghiệp vụ:** Người dùng nhận 1–4 lộ trình đã qua Critic bắt buộc, so sánh và chọn một phương án.

- **Màn hình:** SCR-08, SCR-09.
- **Phạm vi:** US16–US22; US65–US67.
- **Phụ thuộc:** Phase 4.

### Slice 5.1 - Planner → Critic workflow

**FE**

- [ ] Xây SCR-08 bằng run-status component và SSE protocol đã có ở SCR-04; chỉ bổ sung các stage planning/evaluating/revising/completed/failed, không tạo state system hoặc reconnect flow thứ hai.

**BE**

- [ ] Hoàn thiện Orchestrator handoff Planner → Critic → Planner; tái sử dụng idempotency, cancel/retry, SSE event ID và reconnect protocol của Phase 3, không tạo Agent thứ tư hoặc transport riêng.
- [ ] Planner tạo 1–4 phương án gồm ngày, điểm, lưu trú, hoạt động, chặng, phương tiện, chi phí và hành lý.
- [ ] Lưu trú được ghi trong `itinerary_activities` với `activity_type = "lodging"`, sử dụng các trường `title`, `description`, `start_time`, `end_time`, `estimated_cost` và `order_index`; không tạo entity hoặc persistence model riêng cho lưu trú.
- [ ] Critic ghi một `evaluation_results` cho mỗi itinerary/proposal: `is_passed = false` nếu bất kỳ `budget_status`, `opening_hours_status`, `travel_time_status` hoặc `safety_status` là false và ghi nguyên nhân vào `hard_failures`; cảnh báo không làm thất bại được ghi vào `soft_warnings` và `itineraries.warnings`.
- [ ] Lưu trạng thái và version thực thi trong `agent_runs`, `tool_calls` và `evaluation_results`; retry trong cùng `agent_runs.workflow_id` không tạo trùng `itineraries` hoặc `evaluation_results`.

**Tích hợp và kiểm thử**

- [ ] Chỉ hiển thị `itineraries` có `evaluation_results.is_passed = true`; provider/model failure không để lại itinerary ở trạng thái có thể chọn.

### Slice 5.2 - So sánh và lựa chọn

**FE**

- [ ] Xây SCR-09 so sánh tối đa 4 phương án theo lịch ngày, chi phí, thời lượng, transport, luggage và highlights.
- [ ] Hiển thị lý do xếp hạng, warning/trade-off và component source/checked-at/confidence dùng chung; hỗ trợ mobile/keyboard.

**BE**

- [ ] Tạo comparison/selection API với ownership; client gửi `If-Match` hoặc `expected_version`, backend chỉ cập nhật khi khớp `itineraries.version`, sau đó tăng version và trả conflict khi stale.
- [ ] Chuẩn hóa `currency`, timezone và các bản ghi `information_sources`; không trình bày giá vé, giờ mở cửa, thời gian di chuyển hoặc booking offer đã hết hạn như dữ liệu hiện tại.

**Tích hợp và kiểm thử**

- [ ] Generate → Critic → compare → select chạy E2E bằng backend thật.

### Checkpoint Phase 5 - Planning MVP

- [ ] SCR-08 và SCR-09 deploy được và chỉ hiển thị phương án khả thi.
- [ ] `itineraries` có `status = SELECTED` cùng `version` hiện tại là đầu vào duy nhất của Phase 6.

---

## Phase 6 - Tùy chỉnh, phê duyệt và lưu kế hoạch cuối

**Kết quả nghiệp vụ:** Người dùng chỉnh tay hoặc yêu cầu Agent sửa đúng phạm vi, xem diff và chủ động chấp nhận/từ chối trước khi finalize.

- **Màn hình:** SCR-10, SCR-11.
- **Phạm vi:** US23–US28; US65–US67.
- **Phụ thuộc:** Phase 5.

### Slice 6.1 - Manual edit và tính lại

**FE**

- [ ] Xây editor SCR-10 cho add/update/delete/reorder điểm, chặng, hoạt động, vật dụng và hoạt động có `activity_type = "lodging"`; có validation. Khi nhận stale-version conflict, FE tải bản mới nhất và cho phép người dùng nhập lại thay đổi; không xây draft undo hoặc merge-conflict UI.

**BE**

- [ ] Mọi edit command nhận `If-Match` hoặc `expected_version`, cập nhật có điều kiện trên một trường `itineraries.version` và tăng version khi thành công; không tạo lock table, lock token hoặc cơ chế concurrency thứ hai.
- [ ] Sau thay đổi `itinerary_days.planned_date`, địa điểm/thời gian/thứ tự/chi phí trong `itinerary_activities`, hoặc bất kỳ `itinerary_transits` nào, tạo `evaluation_results` mới và chỉ cho chọn phiên bản khi `is_passed = true`; thay đổi chỉ ở `itineraries.title`, `itineraries.summary`, `itineraries.highlights`, `itineraries.trade_offs`, `itineraries.luggage_checklist`, `itinerary_days.title`/`description`, `itinerary_activities.title`/`description` hoặc `itinerary_transits.route_notes` không bắt buộc chạy lại Critic.

**Tích hợp và kiểm thử**

- [ ] Edit itinerary với `expected_version` hiện tại thành công và tăng `itineraries.version`; edit dùng version cũ trả conflict, không ghi đè dữ liệu và cho phép reload/reapply.

### Slice 6.2 - Agent proposal và user approval

**FE**

- [ ] SCR-10 nhận yêu cầu sửa bằng chat và hiển thị `itinerary_proposals.diff_payload`, `rationale`, `warnings`, `status` cùng action accept/reject.

**BE**

- [ ] Planner chỉ tạo `itinerary_proposals` ở trạng thái `pending`; `diff_payload` chỉ chứa field thuộc `itineraries`, `itinerary_days`, `itinerary_activities` hoặc `itinerary_transits` mà yêu cầu người dùng đã nêu. Proposal chạm các field phải kiểm tra lại ở Slice 6.1 phải có `evaluation_results.is_passed = true` trước khi accept.
- [ ] Application service chỉ cho phép chuyển `pending` → `accepted` hoặc `pending` → `rejected`; không yêu cầu migration enum mới cho ba giá trị đã được tài liệu hóa.
- [ ] Accept/reject idempotent: accept chỉ thực hiện khi `base_itinerary_id` trỏ đến itinerary hiện tại và `expected_version` khớp `itineraries.version`, sau đó tạo version mới và cập nhật `status`/`user_decision_at` trong cùng transaction; stale accept trả conflict. Lặp lại cùng quyết định không tạo thêm version, quyết định ngược lại sau trạng thái cuối trả conflict, còn reject giữ current version.

**Tích hợp và kiểm thử**

- [ ] `itinerary_proposals` không đổi itinerary khi còn `pending` hoặc sau khi `rejected`; test hai transition hợp lệ, retry cùng quyết định, conflict khi đổi quyết định và từ chối `diff_payload` chứa field ngoài yêu cầu người dùng hoặc ngoài bốn nhóm bảng được phép.

### Slice 6.3 - Finalize và mobile itinerary

**FE**

- [ ] Xây SCR-11 dạng mobile-first; reopen itinerary đã chốt phải tạo một `itineraries` mới ở trạng thái `DRAFT`.

**BE**

- [ ] Itinerary chỉ chuyển `DRAFT` → `REVIEWING` → `SELECTED`. Khi người dùng chốt, tạo/cập nhật `trips` với `status = "DRAFT"` và `finalized_itinerary_id` trỏ đến itinerary `SELECTED`; khi kích hoạt hoặc kết thúc chuyến đi, chỉ cập nhật `trips.status`, không tạo trạng thái `finalized` hoặc `active` cho itinerary.

**Tích hợp và kiểm thử**

- [ ] Edit/propose → Critic → accept/reject → itinerary `SELECTED` → gán `trips.finalized_itinerary_id` → mobile view chạy E2E; test kích hoạt chuyến đi chứng minh chỉ `trips.status` thay đổi.

### Checkpoint Phase 6

- [ ] SCR-10, SCR-11 deploy được; mọi manual edit, selection và proposal approval dùng cùng `expected_version` rule, stale write không ghi đè trạng thái mới hơn.
- [ ] Phase sau không ghi đè `itineraries` được `trips.finalized_itinerary_id` tham chiếu.

---

## Phase 7 - Tìm dịch vụ và hướng dẫn đặt chỗ

**Kết quả nghiệp vụ:** Người dùng so sánh dịch vụ và tự chuyển sang đối tác; hệ thống không thực hiện giao dịch.

- **Màn hình:** SCR-12, SCR-13.
- **Phạm vi:** US29–US34.
- **Phụ thuộc:** Phase 6.

### Slice 7.1 - Search và comparison

**FE**

- [ ] Xây SCR-12 để filter/compare `booking_offers` theo `final_price`, `match_score`, `provider_name` và `cancellation_policy`; hiển thị đúng trạng thái `STALE` hoặc `UNAVAILABLE`.

**BE**

- [ ] Mở rộng Harness/Orchestrator cho Booking & Logistics Agent; provider ports có allow-list, timeout, rate limit và bounded retry.
- [ ] API trả các field `booking_offers.status`, `final_price`, `currency`, `cancellation_policy`, `checked_at`, `expires_at` và nguồn tương ứng trong `information_sources`; offer không phải booking confirmation.

**Tích hợp và kiểm thử**

- [ ] Finalized itinerary → search → compare chạy với sandbox/fake contract; offer hết hạn buộc refresh.

### Slice 7.2 - Passenger data và safe redirect

**FE**

- [ ] Xây SCR-13 chỉ yêu cầu các trường hành khách mà provider contract đánh dấu bắt buộc cho `booking_offers.id` đã chọn; review screen phải liệt kê từng trường, `final_price`, `cancellation_policy` và thông báo giao dịch diễn ra bên ngoài hệ thống.

**BE**

- [ ] Validate passenger data trong request tạm thời, không ghi dữ liệu hành khách vào bảng hoặc log; redirect/deep link chỉ đến allow-listed domain và trace chỉ lưu `booking_offers.id` cùng kết quả redirect đã redact.
- [ ] Guardrail cấm Agent/API tự đặt chỗ, giữ tiền, lưu payment credential hoặc xác nhận thanh toán.

**Tích hợp và kiểm thử**

- [ ] Redirect chỉ sau explicit user action; test fake domain, parameter injection và cross-account access.

### Checkpoint Phase 7

- [ ] SCR-12 → SCR-13 → safe redirect chạy E2E.
- [ ] UI hiển thị thông báo chuyển sang đối tác; API chỉ trả `redirect_url` và không trả trạng thái thanh toán; trace không ghi booking confirmation vì hệ thống không có bảng booking/payment.

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

- [ ] Application service chỉ chấp nhận `trips.status` thuộc `DRAFT`, `ACTIVE`, `COMPLETED`, `CANCELLED`; activate chuyển `DRAFT` → `ACTIVE`, end chuyển `ACTIVE` → `COMPLETED`. Mỗi request ghi/đọc `gps_location_events` phải dùng `trip_id` để kiểm tra `trips.gps_consent`, không lưu consent trên event; GPS hết hạn tối đa 7 ngày.

**Tích hợp và kiểm thử**

- [ ] Toggle off dừng FE upload và BE từ chối event mới; ownership tests bao phủ nhiều account/trip.

### Slice 8.2 - Q&A và place identification

**FE**

- [ ] Xây SCR-15 cho text/image question, activity suggestions, source panel và low-confidence choices.

**BE**

- [ ] Thêm skills/tools để trả lời lịch sử và văn hóa của địa điểm theo `places.id`, tra cứu `places.min_price`, `max_price`, `currency`, `opening_hours`, điều kiện tham quan và nhận diện ảnh bằng `places.visual_attributes`.
- [ ] Output validator yêu cầu bản ghi `information_sources` cho giá vé, giờ mở cửa, thời tiết và thời gian di chuyển; nếu thiếu `source_name` hoặc `checked_at`, response phải đánh dấu field chưa được kiểm chứng và không trình bày như dữ liệu hiện tại.

**Tích hợp và kiểm thử**

- [ ] Q&A trong/ngoài itinerary và identification có success/low-confidence/failure E2E.

### Slice 8.3 - Proximity và user-controlled audio

**FE**

- [ ] Xây SCR-16 với thông báo khi ở gần địa điểm, play/pause và transcript; audio chỉ phát sau thao tác của người dùng.

**BE**

- [ ] PostGIS proximity + dedup; narration/TTS adapter và signed audio URL. Audio trong `place_narrations` là dữ liệu bền vững, được hiển thị theo `is_active`; retention tối đa 7 ngày chỉ áp dụng cho media tạm thời do người dùng tải lên và artifact TTS sinh tạm thời.

**Tích hợp và kiểm thử**

- [ ] Tắt GPS dừng proximity; radius/dedup tests ngăn spam; không consent vẫn dùng được chức năng không phụ thuộc vị trí.

### Checkpoint Phase 8

- [ ] SCR-14 → SCR-15/SCR-16 chạy E2E trên staging.
- [ ] GPS và media/audio tạm thời đúng consent, ownership và retention; nội dung trong `place_narrations` bật/tắt đúng `is_active` và không bị cleanup theo retention tạm thời.

---

## Phase 9 - Theo dõi thời gian thực và replanning có phê duyệt

**Kết quả nghiệp vụ:** Bản ghi `trips` có `status = "ACTIVE"` được kiểm tra định kỳ; sự cố tạo `trip_alerts` và phương án thay thế nhưng không tự sửa itinerary được `finalized_itinerary_id` tham chiếu.

- **Màn hình:** SCR-17.
- **Phạm vi:** US42–US45; tái sử dụng US25–US27.
- **Phụ thuộc:** Phases 6 và 8.

### Slice 9.1 - Monitoring và alert

**FE**

- [ ] Xây SCR-17 với alert inbox/timeline, severity, unavailable place và source/checked-at/confidence.

**BE**

- [ ] Mở rộng scheduler bằng idempotent Weather Monitor và PostgreSQL lock cho multi-worker.
- [ ] Chỉ quét `trips` có `status = "ACTIVE"`. Weather Monitor contract phải định nghĩa ngưỡng và đơn vị cho thời tiết, số phút thay đổi travel time và thay đổi opening hours; chỉ khi giá trị vượt ngưỡng mới tạo `trip_alerts`, đồng thời dedup theo `trip_id`, `affected_activity_id`, `alert_type` và time bucket tính từ chu kỳ kiểm tra của Weather Monitor.

**Tích hợp và kiểm thử**

- [ ] Fixture phải có giá trị dưới, bằng và vượt từng ngưỡng của Weather Monitor; chỉ trường hợp vượt ngưỡng tạo đúng một `trip_alerts`, và dashboard phải phát hiện lần chạy trễ và tăng metric `weather_monitor_failures_total` khi job lỗi.

### Slice 9.2 - Alternative proposal và approval

**FE**

- [ ] SCR-17 hiển thị proposal diff cho điểm, phương tiện, thời gian, chi phí/warning và accept/reject.

**BE**

- [ ] Job chỉ yêu cầu Planner tạo proposal, Critic kiểm tra và tái sử dụng atomic approval/version flow Phase 6.

**Tích hợp và kiểm thử**

- [ ] Provider change → job → alert → proposal → accept/reject chạy E2E; retry không nhân đôi alert/version.

### Checkpoint Phase 9

- [ ] SCR-17 deploy được; test chạy đồng thời nhiều worker chỉ tạo một `trip_alerts` cho cùng khóa dedup, còn telemetry ghi lần chạy, độ trễ và lỗi.
- [ ] Không có code path tự đổi `itineraries` được `trips.finalized_itinerary_id` tham chiếu khi chưa có user approval.

---

## Phase 10 - Review, kiểm duyệt và tín hiệu xếp hạng

**Kết quả nghiệp vụ:** `place_reviews` mặc định `PRIVATE`, chuyển sang `PENDING` khi yêu cầu công khai và chỉ thành `PUBLIC` sau kiểm duyệt; ranking chỉ dùng review có `status = PUBLIC` và `visit_status = VERIFIED`. Operator gửi kiến nghị vận hành và Admin quyết định áp dụng hoặc từ chối.

- **Màn hình:** SCR-18, SCR-19, SCR-20, SCR-27.
- **Phạm vi:** US46–US51; US71–US72; nền dùng lại cho US59–US60.
- **Phụ thuộc:** Role foundation ở Phase 2; dữ liệu địa điểm và nội dung thuyết minh ở Phase 4; Phase 8.

### Slice 10.1 - Review private và publication request

**FE**

- [ ] Xây SCR-18 với rating/comment, private default và privacy/moderation status.
- [ ] SCR-19 chỉ hiển thị approved public reviews và report dialog/status.

**BE**

- [ ] Tạo state machine cho `place_reviews.status`, kiểm tra `user_id` ownership và `trip_id` để đặt `visit_status`; mỗi transition kiểm duyệt phải thêm một `review_moderation_logs` và không sửa/xóa log đã tạo.
- [ ] Ngăn private/pending review xuất hiện trong public query, ranking, logs không được phép hoặc account khác.

**Tích hợp và kiểm thử**

- [ ] Create → private → request public chạy E2E; privacy toggle không bypass moderation.

### Slice 10.2 - Moderation, reporting và ranking

**FE**

- [ ] Xây SCR-20 cho Operator/Admin với filters, report/review detail và action theo trạng thái hiện tại: approve/reject khi review là `PENDING`, hide khi là `PUBLIC`, restore khi là `HIDDEN`; mọi action bắt buộc nhập reason trước khi xác nhận.
- [ ] Sau mỗi quyết định, SCR-20 hiển thị trạng thái mới và thông tin người kiểm duyệt; loading, empty, forbidden, stale-state conflict và action error phải có trạng thái riêng.

**BE**

- [ ] Spam/policy/relevance/verified-trip checks trước publish; cả `OPERATOR` và `ADMIN` được thực hiện các transition hợp lệ `PENDING` → `PUBLIC` (`APPROVE`), `PENDING` → `REJECTED` (`REJECT`), `PUBLIC` → `HIDDEN` (`HIDE`) và `HIDDEN` → `PUBLIC` (`RESTORE`).
- [ ] Mỗi quyết định cập nhật `place_reviews.status` và thêm đúng một `review_moderation_logs` trong cùng transaction, gồm `review_id`, `moderator_id`, `moderator_type`, `action`, `previous_status`, `new_status`, `reason`, `details` và `created_at`; log đã tạo không được update hoặc delete.
- [ ] Với quyết định thủ công, backend lấy `moderator_id` và `moderator_type` từ actor đã xác thực, không nhận hai giá trị này từ request payload; `moderator_id` chỉ được null khi `moderator_type = SYSTEM`.
- [ ] Tạo workflow `review_reports` và rate limit; ranking chỉ đọc `place_reviews` có `status = PUBLIC`, `visit_status = VERIFIED` và lần `APPROVE` tương ứng trong `review_moderation_logs.details` xác nhận relevance.

**Tích hợp và kiểm thử**

- [ ] Fixture gồm hai `places` có dữ liệu giống nhau phải chứng minh review `PRIVATE`, `PENDING`, `REJECTED` và `HIDDEN` không đổi thứ tự ranking; review `PUBLIC` + `VERIFIED` đã duyệt làm tăng điểm của đúng địa điểm theo công thức được version hóa trong ranking service contract.
- [ ] Authorization matrix chứng minh `USER` không truy cập được SCR-20 hoặc moderation API; `OPERATOR` và `ADMIN` đều thực hiện được approve/reject/hide/restore khi review ở đúng trạng thái.
- [ ] Mỗi approve/reject/hide/restore tạo đúng một immutable moderation log với ID và type của actor thực tế; invalid transition, stale request hoặc retry không ghi đè log cũ và không tạo quyết định trùng.
- [ ] Sau approve/reject/hide/restore, ranking query đọc trạng thái mới từ `place_reviews`; review không còn `PUBLIC` bị loại ngay khỏi lần tính ranking tiếp theo.

### Slice 10.3 - Operator Proposal and Admin Approval

**FE**

- [ ] Xây SCR-27 tại `/operations/proposals` với form cho `operator_proposals`: `PLACE_UPDATE` bắt buộc `target_place_id`; `WEATHER_REPORT` và `AI_ISSUE` để `target_place_id` null; `related_trip_id` là tùy chọn nhưng phải tham chiếu `trips.id` hợp lệ nếu được gửi; cả ba loại bắt buộc `title`, `description` và `proposed_payload`.
- [ ] SCR-27 cung cấp danh sách/detail cho Admin xem kiến nghị `PENDING`, nội dung hiện tại, thay đổi đề xuất và căn cứ; approve/reject đều bắt buộc nhập ghi chú trước khi xác nhận.
- [ ] Operator xem được trạng thái và ghi chú phản hồi của kiến nghị do mình tạo; không được tự duyệt hoặc sửa kiến nghị đã có quyết định.

**BE**

- [ ] Tạo role-protected API để `OPERATOR` tạo và chỉ xem `operator_proposals` của mình. Validation yêu cầu `PLACE_UPDATE` có `target_place_id` và payload chỉ chứa field của `places`; `WEATHER_REPORT`/`AI_ISSUE` không có `target_place_id`; `related_trip_id` là tùy chọn nhưng phải tồn tại trong `trips` nếu có, và hai loại này không cập nhật bảng nghiệp vụ khi Admin duyệt.
- [ ] Chỉ `ADMIN` được chuyển `PENDING` sang `APPROVED` hoặc `REJECTED`; lưu `admin_id`, `admin_note` và `reviewed_at`, đồng thời từ chối thay đổi quyết định đã hoàn tất.
- [ ] Khi duyệt `PLACE_UPDATE`, validate lại payload và cập nhật `places` cùng quyết định proposal trong một transaction; reject hoặc duyệt hai loại còn lại không được thay đổi dữ liệu địa điểm.

**Tích hợp và kiểm thử**

- [ ] Với US71–US72, SCR-27 chạy end-to-end cho luồng Operator submit → Admin review → approve/reject → Operator xem kết quả ở cả ba loại kiến nghị.
- [ ] Approved `PLACE_UPDATE` cập nhật `places` đúng một lần; rejected proposal không đổi dữ liệu trong `places` và retry/double-submit không tạo quyết định hoặc cập nhật trùng.
- [ ] Test role matrix chứng minh `USER` không tạo/xem proposal vận hành, `OPERATOR` không duyệt và chỉ `ADMIN` được quyết định.

### Checkpoint Phase 10

- [ ] SCR-18/SCR-19 và SCR-20 cho Operator/Admin chạy end-to-end.
- [ ] Privacy default, authorization moderation, immutable moderation log và ranking signal của US51 có security/integration tests; review `PRIVATE`, `PENDING`, `REJECTED` và `HIDDEN` không ảnh hưởng kết quả Phase 4.
- [ ] SCR-27 hoàn thành luồng Maker–Checker của US71–US72 end-to-end; approved `PLACE_UPDATE` cập nhật `places` trong cùng transaction với `operator_proposals.status`; mọi quyết định phải ghi `admin_id`, `admin_note` và `reviewed_at`.

---

## Phase 11 - Tổng kết chuyến đi và vòng cá nhân hóa

**Kết quả nghiệp vụ:** Người dùng nhận `trip_summaries` ở trạng thái `DRAFT`, chỉnh địa điểm thực tế, chi phí và nhật ký, chuyển tổng kết sang `CONFIRMED` rồi bắt đầu chuyến tiếp theo.

- **Màn hình:** SCR-21, SCR-22, SCR-23.
- **Phạm vi:** US52–US64.
- **Phụ thuộc:** Phases 8–10.

### Slice 11.1 - Completion và actual route

**FE**

- [ ] Xây SCR-21 với early-end, notification và các `trip_summary_places.status` gồm `VISITED`, `SKIPPED`, `UNPLANNED`; hiển thị `evidence`, `confidence` và cho phép correction đặt `is_user_corrected = true`.

**BE**

- [ ] Thêm idempotent Trip Completion job cho scheduled end hoặc early-end command; mỗi `trips.id` chỉ tạo một `trip_summaries` có `status = DRAFT`.
- [ ] Đối chiếu itinerary từ `trips.finalized_itinerary_id` với tương tác người dùng và `gps_location_events` chỉ khi `trips.gps_consent = true`; ghi kết quả vào `trip_summary_places.evidence`, và vẫn tạo draft từ tương tác/xác nhận khi không có GPS.

**Tích hợp và kiểm thử**

- [ ] Job retry/multi-worker không tạo trùng `trip_summaries` cho cùng `trip_id`; correction cập nhật `trip_summary_places` trước khi `trip_summaries.status` chuyển sang `CONFIRMED`.

### Slice 11.2 - Expenses, diary, media và place reviews

**FE**

- [ ] Xây SCR-22 với `trip_expenses.category`, chênh lệch chi phí, `trip_summaries.diary_notes`, media có `purpose = SUMMARY_PHOTO`, `overall_rating` và `place_reviews`.

**BE**

- [ ] Lưu `trip_expenses.amount`, `currency`, `category`; tính chênh lệch tuyệt đối giữa tổng chi phí thực tế đã quy đổi và `itineraries.estimated_total_cost`, còn chênh lệch phần trăm trả null khi chi phí dự kiến null hoặc bằng 0. Chưa có `trip_expenses` nghĩa là “không nhập”, khác với tổng bằng 0.
- [ ] Media `SUMMARY_PHOTO` dùng `media_files` và retention hiện có; đánh giá địa điểm dùng `place_reviews`, `review_reports`, `review_moderation_logs`, không tạo bảng song song.

**Tích hợp và kiểm thử**

- [ ] Có thể chuyển `trip_summaries` sang `CONFIRMED` khi không có `trip_expenses`; test công thức chênh lệch và xác nhận `place_reviews.status` mặc định là `PRIVATE`.

### Slice 11.3 - Xác nhận `trip_summaries` và tạo chuyến tiếp theo

**FE**

- [ ] Review-before-confirm liệt kê field từ `trip_summaries`, `trip_summary_places` và `trip_expenses` sẽ cập nhật hồ sơ; SCR-23 hiển thị 1–3 `next_trip_suggestions` theo `rank` cùng action start planning.

**BE**

- [ ] Trong một transaction, chuyển `trip_summaries.status` từ `DRAFT` sang `CONFIRMED`, ghi `confirmed_at`, từ chối sửa/xóa tổng kết đã xác nhận và chỉ cập nhật `user_profile.travel_preferences` hoặc `default_budget` từ dữ liệu đã xác nhận.
- [ ] Sinh 1–3 `next_trip_suggestions`; start endpoint tạo `agent_session` và `trip_requests` mới, ghi `started_agent_session_id`, đồng thời prefill từ `user_profile` và suggestion đã chọn.

**Tích hợp và kiểm thử**

- [ ] Double confirm không cập nhật trùng; `trip_summaries.status = CONFIRMED` → `user_profile`/lịch sử chuyến đi → `next_trip_suggestions` → `agent_session` mới chạy E2E.

### Checkpoint Phase 11

- [ ] SCR-21 → SCR-22 → SCR-23 chạy E2E.
- [ ] `trip_summaries` có `status = CONFIRMED` là dữ liệu bền vững và không được lưu thay thế trong `agent_memories`.

---

## Phase 12 - Audit, privacy và hỗ trợ vận hành

**Kết quả nghiệp vụ:** `OPERATOR`/`ADMIN` tra cứu trace qua SCR-24/SCR-25 và mỗi lần mở detail tạo `audit_access_logs`; retention được kiểm chứng trên các bảng có hạn lưu, còn `ADMIN` cập nhật `system_configs` mà không cần khởi động lại ứng dụng.

- **Màn hình:** SCR-24, SCR-25, SCR-29.
- **Phạm vi:** US68–US70; US75; hoàn thiện US65–US67 và shared retention.
- **Phụ thuộc:** Role foundation Phase 2; retention Phase 3; Planner Phase 5; Weather Monitor Phase 9; audit events Phases 3–11.

### Slice 12.1 - Audit search và protected detail

**FE**

- [ ] Xây SCR-24 với filters trip/Agent/error/time, pagination và role-aware states.
- [ ] SCR-25 bắt buộc form purpose + Ticket ID trước khi tải detail; không prefetch nội dung bảo vệ.

**BE**

- [ ] Chuẩn hóa trace từ `agent_runs`, `tool_calls` và `information_sources`; chỉ lưu các field đã định nghĩa trong ba bảng này và redact secret, passenger data cùng PII không cần thiết trước khi ghi.
- [ ] Tạo role-based search/detail API; khi actor đã được cấp quyền mở protected detail, ghi một `audit_access_logs` gồm `actor_id`, `target_user_id`, `agent_run_id`, `purpose`, `ticket_id`, `client_ip`, `user_agent` và `accessed_at`.

**Tích hợp và kiểm thử**

- [ ] Thiếu role/purpose/ticket thì không tải detail; lần mở detail thành công có `audit_access_logs`, còn authorization denial chỉ được ghi trong application/security log đã redact.

### Slice 12.2 - Trace viewer và retention verification

**FE**

- [ ] SCR-25 hiển thị redacted input, tool/result, source, handoff, validation, error và versions cho Admin.
- [ ] Deep link dữ liệu đã dọn hiển thị “đã hết hạn”, không tạo broken UI.

**BE**

- [ ] Xây trace trực tiếp từ `agent_runs.id`, `workflow_id` và `parent_run_id`; hỗ trợ lọc theo `agent_session_id`, `trip_request_id` và `trip_id`, đánh dấu run/tool call thiếu hoặc hết hạn, giới hạn tối đa 100 bản ghi mỗi trang và khoảng thời gian truy vấn không quá 30 ngày.
- [ ] Retention service chặn đọc rồi xóa `gps_location_events` theo `expires_at`/`is_expired`, xóa `agent_memories`, `agent_runs` và `tool_calls` theo `expires_at`; với `media_files`, deadline bằng `created_at` cộng `temporary_data_retention_days`, sau đó xóa cả object và bản ghi metadata. Retry cùng batch phải idempotent.
- [ ] Không xóa `user_profile`, `itineraries` được `trips.finalized_itinerary_id` tham chiếu, `place_reviews` có `status = PUBLIC` hoặc `trip_summaries` có `status = CONFIRMED`; metrics ghi số bản ghi/object đã chặn, xóa, bỏ qua và lỗi theo từng bảng.

**Tích hợp và kiểm thử**

- [ ] Từ `agent_runs.parent_run_id` và `tool_calls.sequence_number`, Admin xem được timeline Planner → Critic/Booking gồm status, version, tool result đã redact và error; màn hình không chạy lại Agent và không hiển thị secret/chain-of-thought.
- [ ] Time-travel E2E chứng minh API chặn dữ liệu hết hạn, sau cleanup không còn bản ghi PostgreSQL hoặc object tương ứng; retry không xóa dữ liệu còn hạn và không thất bại khi mục tiêu đã được xóa.

### Slice 12.3 - Global System Configuration

**FE**

- [ ] Xây SCR-29 cho Admin xem và cập nhật chu kỳ kiểm tra thời tiết, thời hạn lưu dữ liệu tạm thời và giới hạn số phương án lộ trình; hiển thị đơn vị, khoảng giá trị hợp lệ, giá trị hiện tại và thời điểm cập nhật gần nhất.
- [ ] Form có loading, validation, saving, success và error states; yêu cầu xác nhận trước khi lưu và không hiển thị thành công khi backend từ chối toàn bộ thay đổi.

**BE**

- [ ] Tạo API đọc/cập nhật `system_configs` chỉ dành cho `ADMIN`; chỉ chấp nhận `weather_check_interval_minutes`, `temporary_data_retention_days` và `itinerary_option_limit`, không cho client tạo key tùy ý.
- [ ] Validation yêu cầu số nguyên với `weather_check_interval_minutes` từ 1–1440, `temporary_data_retention_days` từ 1–7 và `itinerary_option_limit` từ 1–4; request có key lạ hoặc bất kỳ giá trị không hợp lệ phải bị từ chối nguyên tử.
- [ ] Mỗi update hợp lệ ghi `config_value`, `updated_by` và `updated_at`, đồng thời ghi structured application/security log gồm actor, key, giá trị cũ/mới và thời điểm; log phải được redact vì `DATABASE.txt` chưa định nghĩa bảng audit riêng cho thay đổi cấu hình.
- [ ] Weather Monitor đọc chu kỳ mới trước khi lập lần chạy tiếp theo; Retention service đọc thời hạn mới khi tính deadline cho media và dữ liệu tạm mới; Planner đọc giới hạn phương án khi bắt đầu mỗi planning run. Thay đổi áp dụng cho lần chạy tiếp theo mà không restart và không sửa input của lần chạy đang thực hiện.

**Tích hợp và kiểm thử**

- [ ] Với US75, Admin cập nhật từng key và test chứng minh Weather Monitor dùng chu kỳ mới, Retention áp dụng thời hạn mới và Planner không tạo quá giới hạn phương án ở các lần chạy tiếp theo.
- [ ] `USER` và `OPERATOR` không đọc hoặc cập nhật được cấu hình; request có key lạ, sai kiểu hoặc ngoài khoảng không thay thế giá trị hiện tại và không tạo audit event cập nhật thành công.
- [ ] SCR-29 → update API → Weather Monitor/Retention service/Planner đọc cấu hình mới chạy end-to-end mà không restart ứng dụng; refresh trang trả đúng giá trị, `updated_by` và `updated_at` mới nhất.

### Checkpoint Phase 12

- [ ] `OPERATOR` và `ADMIN` đi qua purpose/ticket gate từ SCR-24 đến SCR-25; truy cập thành công tạo đúng một `audit_access_logs`, còn `USER` nhận HTTP 403.
- [ ] Discovery, planning, proposal và alert dùng `information_sources` cho source/checked-at/confidence, `evaluation_results.hard_failures`/`soft_warnings` cho kết quả Critic, `itinerary_proposals.rationale`/`warnings` cho proposal và `trip_alerts.message`/`severity` cho alert.
- [ ] Retention/consent matrix phải liệt kê `media_files`, `gps_location_events`, `agent_memories`, `agent_runs` và `tool_calls` cùng deadline, điều kiện chặn đọc, hành động xóa và metric giám sát; test xác nhận GPS chỉ được đọc/ghi khi `trips.gps_consent = true`.
- [ ] Luồng cấu hình US75 chạy end-to-end trên SCR-29; giá trị hợp lệ có hiệu lực ở lần chạy tiếp theo mà không restart, còn role hoặc giá trị không hợp lệ bị từ chối.

---

## Phase 13 - Production readiness và phát hành

**Kết quả nghiệp vụ:** Toàn bộ vertical slices dùng cùng artifact đã qua test để deploy production; dashboard/alert, backup-restore, rollback và kết quả UAT phải có bằng chứng được liên kết trong release record.

Phase này không thêm nghiệp vụ mới; quality/telemetry cơ bản đã đi cùng từng phase.

### Slice 13.1 - Packaging và observability

**FE**

- [ ] Tạo production bundle/image và runtime config; error report phải redact dữ liệu nhạy cảm, web-vitals phải đạt performance budget đã phê duyệt, accessibility test đạt WCAG 2.1 AA và responsive regression pass trên viewport đã khai báo.

**BE**

- [ ] Tạo production image và migration job; health/readiness kiểm tra database cùng Object Storage, telemetry ghi latency/error cho API, SSE, `agent_runs`, provider và scheduler.
- [ ] Trước production phải phê duyệt SLO có ngưỡng số cho p95 latency, error rate, provider/token usage, job lag, cleanup failure và storage; dashboard hiển thị từng metric và alert kích hoạt khi vượt ngưỡng.

**Tích hợp**

- [ ] Immutable FE/BE artifacts từ cùng commit; deploy staging và smoke auth, `agent_session`/`messages`, discovery, itinerary planning, `trips.finalized_itinerary_id` và scheduler.

### Slice 13.2 - Security, performance và recovery

**FE**

- [ ] Security test phải chặn XSS, file upload sai type/size, redirect ngoài allow-list và request từ session hết hạn; cache không lưu response nhạy cảm, còn chat/map/comparison/Companion phải đạt performance budget đã phê duyệt.

**BE**

- [ ] Threat model phải liệt kê threat, trust boundary, biện pháp và test cho auth/ownership, upload/signed URL, SSRF/provider, redirect và model-prompt/tool-call boundaries; OpenAPI ghi rate limit cho từng endpoint công khai hoặc endpoint gọi provider.
- [ ] Load test API/SSE/PostGIS/scheduler/provider phải đạt SLO đã phê duyệt; failure test chứng minh retry không tạo dữ liệu trùng, còn backup/restore drill khôi phục được PostgreSQL và Object Storage trong RTO/RPO đã phê duyệt.

### Slice 13.3 - Traceability, UAT và rollout

**FE + BE + Product/Ops**

- [ ] Map US01–US75 và SCR-01–SCR-29 đến automated/UAT tests.
- [ ] UAT chín journey: planning; customization/finalize; booking guidance; active-trip response; xác nhận `trip_summaries`; quản trị địa điểm; Operator proposal → Admin approval; quản trị người dùng; cấu hình hệ thống.
- [ ] Runbooks cho provider outage, stuck Agent run, missed job, retention failure và rollback-compatible migration.
- [ ] Deploy staging → smoke/UAT → production, theo dõi SLO và diễn tập application/migration rollback trước general availability.
- Canary deployment và feature flags không phải release gate; chỉ bổ sung khi rủi ro rollout hoặc quy mô triển khai thực tế yêu cầu.

### Final Checkpoint - Production Ready

- [ ] Tất cả checkpoint Phase 1–12 đạt; issue mức Critical/High trong release risk register phải được đóng hoặc có quyết định chấp nhận rủi ro được phê duyệt.
- [ ] Deploy/rollback, migration, backup/restore và scheduler failover đã diễn tập.
- [ ] Product Owner phê duyệt kết quả UAT; Security phê duyệt threat model/test; accessibility không còn lỗi Critical; load test đạt SLO; bảng traceability không thiếu US hoặc SCR.

---

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
| US71–US72 | 10 | SCR-27 |
| US73 | 4 | SCR-26 |
| US74 | 2 | SCR-28 |
| US75 | 12 | SCR-29 |

## Rủi ro chính và kiểm soát

| Rủi ro | Kiểm soát bắt buộc |
| --- | --- |
| FE dùng mock quá lâu | Contract-first, generated client, drift CI, E2E API thật ở checkpoint |
| AI/provider không ổn định | Structured output, validator, bounded retry, golden eval |
| Dữ liệu biến động lỗi thời | `information_sources.source_name`, `source_url`, `checked_at`, `confidence` và quy tắc expiry/refresh theo từng field |
| Planner bỏ qua feasibility | Mandatory Critic và test không cho bypass |
| Agent/job tự sửa itinerary | Chỉ ghi `itinerary_proposals`, atomic approval và kiểm tra `expected_version` |
| Rò GPS/media/log | Consent, ownership, redaction, signed URL, 7-day cleanup |
| Scheduler chạy trùng | PostgreSQL lock, idempotency, unique constraints |
| Booking vượt phạm vi | No-payment guardrail, allow-list, redirect security tests |
| Scope tăng do hạ tầng/Agent | Modular monolith, đúng ba Agent, chỉ thêm khi có số liệu |