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
- [ ] Backend khởi động được và GET /health trả trạng thái thành công.
- [ ] Cấu hình đọc từ environment với validation khi thiếu biến bắt buộc.
- [ ] Có smoke test cho application startup và health endpoint.

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
Áp dụng ba role tối thiểu là user, operator và engineer, đồng thời kiểm tra quyền sở hữu dữ liệu giữa các tài khoản.  
Các lỗi authentication và authorization phải có cấu trúc nhất quán để frontend xử lý rõ ràng.

**Acceptance Criteria**
- [ ] User có thể tạo tài khoản, đăng nhập, đăng xuất và truy cập dữ liệu thuộc sở hữu.
- [ ] Operator/engineer chỉ truy cập endpoint vận hành đúng quyền.
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

## Phase 3 - Agent Harness Foundation

Mục tiêu là xây runtime dùng chung cho đúng ba Agent. Phase này dùng fake model và fake tools để kiểm thử trước khi tích hợp nhà cung cấp thật.

### Step 3.1 - Define Agent Contracts and Runtime

**Mô tả** Định nghĩa contract chung cho request, result và trạng thái chạy của Agent.  
Runtime phải xử lý được lifecycle, cancellation và timeout trong cùng một process mà không để run bị treo.  
Contract chỉ lưu structured result cần thiết và không yêu cầu raw chain-of-thought.

**Acceptance Criteria**
- [ ] Runtime chạy được một fake Agent và trả structured result.
- [ ] Timeout/cancellation tạo lỗi có mã và không để run treo.
- [ ] Agent contract không chứa hoặc yêu cầu raw chain-of-thought.

**Verification** Unit test success, timeout, cancellation và invalid result.

**Dependencies** Phase 2.
**Files Related** backend/app/ai/harness/runtime/, contracts/, tests/unit/ai/.

### Step 3.2 - Implement Model Gateway

**Mô tả** Tạo một Model Gateway làm điểm gọi LLM tập trung cho toàn bộ Agent.  
Gateway quản lý structured output, token limit, timeout và retry có giới hạn thay vì để từng Agent gọi provider trực tiếp.  
Mọi kết quả từ model phải được validation trước khi trả về runtime.

**Acceptance Criteria**
- [ ] Agent không gọi SDK nhà cung cấp trực tiếp.
- [ ] Gateway validate structured output trước khi trả cho runtime.
- [ ] Retry chỉ áp dụng lỗi tạm thời và có giới hạn.

**Verification** Contract test bằng fake provider cho success, malformed output, rate limit và timeout.

**Dependencies** Step 3.1.
**Files Related** backend/app/ai/harness/model_gateway/, provider adapter, tests.

### Step 3.3 - Implement Prompt Registry

**Mô tả** Tạo Prompt Registry để quản lý system prompt, prompt template, output schema và version của từng Agent.  
Agent chỉ tham chiếu prompt bằng ID và version, tránh nhúng nội dung prompt rải rác trong code.  
Trace cần ghi nhận version đã dùng nhưng không được làm lộ secret hoặc nội dung nhạy cảm.

**Acceptance Criteria**
- [ ] Mỗi Agent tham chiếu prompt bằng ID/version, không nhúng prompt rải rác.
- [ ] Missing prompt/version gây lỗi rõ ràng.
- [ ] Version prompt xuất hiện trong trace nhưng không log secret.

**Verification** Unit test load/version/fallback failure và snapshot phần prompt không nhạy cảm.

**Dependencies** Steps 3.1–3.2.
**Files Related** backend/app/ai/harness/prompts/, prompt definitions, tests.

### Step 3.4 - Implement Skill Registry

**Mô tả** Tạo Skill Registry cho các skill có thể tái sử dụng giữa các Agent.  
Mỗi skill cần có ID, version, input/output contract và danh sách Agent được phép sử dụng.  
Skill chỉ đại diện cho một capability, không được triển khai như một sub-agent mới.

**Acceptance Criteria**
- [ ] Skill có ID, version, input/output contract và allow-list Agent.
- [ ] Runtime chỉ nạp skill Agent được phép dùng.
- [ ] Có skill mẫu cho requirement extraction và feasibility evaluation.

**Verification** Unit test registration, duplicate ID, permission và version selection.

**Dependencies** Steps 3.1 và 3.3.
**Files Related** backend/app/ai/harness/skills/, skill definitions, tests.

### Step 3.5 - Implement Tool Registry and Provider Ports

**Mô tả** Định nghĩa Tool Registry và các provider port cho travel, maps, weather, booking, vision và TTS.  
Registry chịu trách nhiệm validation arguments, result và quyền sử dụng tool của từng Agent.  
Các provider chưa được lựa chọn cần có fake adapter để việc phát triển và kiểm thử không bị chặn.

**Acceptance Criteria**
- [ ] Tool arguments và result được validate tại registry boundary.
- [ ] Mỗi Agent có allow-list tool riêng.
- [ ] Provider chưa chọn có fake adapter để phát triển không bị chặn.

**Verification** Unit/contract test permission denied, invalid argument, provider error và success.

**Dependencies** Steps 3.1–3.2.
**Files Related** backend/app/ai/harness/tools/, backend/app/infrastructure/providers/, tests.

### Step 3.6 - Implement Context Builder

**Mô tả** Xây dựng context tối thiểu từ yêu cầu đã xác nhận, profile cần thiết và dữ liệu đã kiểm chứng.  
Context phải giữ nguồn, confidence và plan version, đồng thời không được lấy dữ liệu từ tài khoản khác.  
Token budget được áp dụng theo quy tắc xác định để loại bỏ dữ liệu thừa trước khi gọi model.

**Acceptance Criteria**
- [ ] Context không tự lấy dữ liệu của account khác.
- [ ] Thông tin có nguồn và confidence được giữ cùng dữ liệu.
- [ ] Token budget loại dữ liệu thừa theo quy tắc xác định được.

**Verification** Unit test ownership, ordering, token budget và missing required context.

**Dependencies** Steps 2.2, 3.3 và 3.5.
**Files Related** backend/app/ai/harness/context/, query ports, tests.

### Step 3.7 - Implement Memory Manager

**Mô tả** Quản lý working memory và trip memory tạm thời theo user, trip và run.  
Memory tạm phải tách khỏi profile đã xác nhận, có expires_at không quá 7 ngày và không được đọc sau khi hết hạn.  
Chỉ preference được người dùng xác nhận mới được ghi vào profile thông qua use case riêng.

**Acceptance Criteria**
- [ ] Memory bị scope theo user/trip/run và có expires_at không quá 7 ngày.
- [ ] Confirmed preference được ghi vào profile qua use case riêng, không giữ như long-term Agent memory.
- [ ] Expired memory không được Context Builder đọc.

**Verification** Integration test isolation, expiry và confirmed-profile extraction.

**Dependencies** Steps 2.2 và 3.6.
**Files Related** backend/app/ai/harness/memory/, database models, repositories, tests.

### Step 3.8 - Add Guardrails, Output Validation and Trace

**Mô tả** Thêm guardrails trước và sau model call, validation nghiệp vụ và trace tóm tắt.  
Hệ thống phải chặn tool hoặc action ngoài quyền, đặc biệt là hành động tự động booking hay payment.  
Trace chỉ lưu metadata, tool call, lỗi và summary reason; không lưu raw chain-of-thought.

**Acceptance Criteria**
- [ ] Chặn tool/action ngoài quyền và chặn booking/payment tự động.
- [ ] Output biến động thiếu source, checked_at hoặc confidence bị từ chối.
- [ ] Trace lưu input/output metadata, tool call, lỗi và summary reason; không lưu raw chain-of-thought.

**Verification** Adversarial unit tests và integration test trace có expires_at tối đa 7 ngày.

**Dependencies** Steps 3.1–3.7.
**Files Related** guardrails/, validators/, tracing/, audit persistence, tests.

### Checkpoint - Harness Ready

- [ ] Fake Agent chạy end-to-end qua Runtime, Context, Model Gateway và Validator.
- [ ] Skill/tool permissions được kiểm tra.
- [ ] Memory và trace tuân thủ 7-day expiry.
- [ ] Không có direct provider call ngoài gateway/registry.
- [ ] Nhóm duyệt Agent contracts trước Phase 4.

---

## Phase 4 - AI Orchestration and Three Agents

### Step 4.1 - Implement Orchestrator State and Handoff

**Mô tả** Xây dựng state và cơ chế handoff để Orchestrator điều phối đúng ba Agent đã định nghĩa.  
Mỗi task phải giữ request summary, verified data, plan version và trạng thái lỗi trong suốt workflow.  
Các request bị gửi lại hoặc retry không được vô tình tạo thêm plan version.

**Acceptance Criteria**
- [ ] Orchestrator chỉ dispatch Planner, Critic/Evaluator hoặc Booking & Logistics.
- [ ] Mỗi handoff giữ request summary và plan version.
- [ ] Duplicate/retried request không tạo plan version ngoài ý muốn.

**Verification** State-machine tests cho planning, rework, booking và failure recovery.

**Dependencies** Phase 3.
**Files Related** backend/app/ai/orchestrator/, workflow state, tests.

### Step 4.2 - Implement Planner Agent

**Mô tả** Triển khai Planner Agent để tạo mới hoặc điều chỉnh itinerary theo yêu cầu đã xác nhận.  
Kết quả cần bao gồm lịch theo ngày, di chuyển, nhóm chi phí, hành lý, điểm nổi bật và trade-offs.  
Khi chỉnh sửa, Planner chỉ được thay đổi đúng phạm vi người dùng yêu cầu và phải ghi rõ reason cùng plan version.

**Acceptance Criteria**
- [ ] Planner output đúng schema và tạo tối đa 4 phương án.
- [ ] Planner chỉ sửa phạm vi người dùng yêu cầu khi thực hiện adjustment.
- [ ] Mỗi đề xuất có summary reason, nguồn liên quan và plan version.

**Verification** Golden-fixture tests cho create, partial edit, missing data và impossible request.

**Dependencies** Step 4.1.
**Files Related** backend/app/ai/agents/planner/, skills, prompts, tests/evals/.

### Step 4.3 - Implement Mandatory Critic Agent

**Mô tả** Triển khai Critic Agent như bước kiểm tra bắt buộc trước khi một plan được hiển thị.  
Critic đánh giá ngân sách, giờ mở cửa, thời gian di chuyển và các rủi ro an toàn bằng dữ liệu có cấu trúc.  
Hard failure phải trả lại Planner để sửa, còn soft warning được giữ lại để người dùng cân nhắc.

**Acceptance Criteria**
- [ ] Mọi plan mới và thay đổi quan trọng đều đi qua Critic.
- [ ] Hard failure trả về Planner với issue có cấu trúc.
- [ ] Soft warning được giữ trong kết quả cho người dùng cân nhắc.

**Verification** Scenario tests cho over-budget, closed venue, impossible travel time, safety risk và pass.

**Dependencies** Steps 4.1–4.2.
**Files Related** backend/app/ai/agents/critic/, evaluation skills, prompts, tests/evals/.

### Step 4.4 - Implement Booking and Logistics Agent

**Mô tả** Triển khai Booking & Logistics Agent để tìm kiếm, so sánh và hướng dẫn dùng dịch vụ bên thứ ba.  
Kết quả cần nêu provider, final price, độ phù hợp và điều khoản hủy hoặc thay đổi.  
Agent chỉ cung cấp redirect hoặc hướng dẫn, không được tự đặt chỗ, giữ tiền hay thanh toán.

**Acceptance Criteria**
- [ ] Output gồm provider, final price, suitability và cancellation/change terms.
- [ ] Agent chỉ tạo redirect/instruction, không gọi action đặt chỗ hoặc thanh toán.
- [ ] Passenger data chỉ đi qua tool/provider được cho phép.

**Verification** Contract tests với fake providers và negative tests cho forbidden booking/payment action.

**Dependencies** Steps 3.5 và 4.1.
**Files Related** backend/app/ai/agents/booking/, provider tools, prompts, tests.

### Step 4.5 - Verify Full Agent Workflow

**Mô tả** Kiểm tra toàn bộ workflow giữa Orchestrator, Planner, Critic và Booking bằng dữ liệu đại diện.  
Luồng rework giữa Planner và Critic phải có giới hạn, lưu được handoff, tool call, result và version trong trace.  
Bộ kiểm thử phải chứng minh hệ thống chỉ có đúng ba Agent và không cần provider thật để chạy.

**Acceptance Criteria**
- [ ] Rework loop có giới hạn và trả lỗi có thể giải thích khi không hội tụ.
- [ ] Agent handoff, tool calls, result và version xuất hiện trong trace.
- [ ] Không có Agent hoặc sub-agent thứ tư.

**Verification** Integration suite với fake LLM/tools và snapshot execution graph.

**Dependencies** Steps 4.1–4.4.
**Files Related** backend/tests/integration/ai/, fixtures, trace assertions.

### Checkpoint - AI Core Ready

- [ ] Ba Agent chạy qua cùng Harness.
- [ ] Critic gate không thể bị bỏ qua.
- [ ] Booking/payment action bị chặn.
- [ ] Workflow integration tests pass không cần provider thật.

---

## Phase 5 - Trip Request and Destination Discovery

### Step 5.1 - Deliver Conversation Slice

**Mô tả** Xây dựng conversation, lưu trữ message và các REST/SSE endpoint cho trải nghiệm chat cơ bản.  
SSE cần phát rõ trạng thái start, progress, complete và error, đồng thời hỗ trợ reconnect an toàn.  
Giao diện chat phải hiển thị loading, retry và error mà không làm mất conversation hiện tại.

**Acceptance Criteria**
- [ ] User tạo conversation và gửi/nhận message thuộc đúng account.
- [ ] SSE stream có trạng thái start/progress/complete/error và hỗ trợ reconnect an toàn.
- [ ] Chat UI hiển thị loading, retry và error.

**Verification** API integration test và browser E2E cho một conversation hoàn chỉnh.

**Dependencies** Phases 2 và 4.
**Files Related** conversation module, API routes, frontend chat feature, tests.

### Step 5.2 - Extract and Complete Trip Requirements

**Mô tả** Dùng Planner skill để trích xuất yêu cầu chuyến đi từ natural language và kết hợp với profile.  
Hệ thống cần nhận biết ngày đi, nơi xuất phát, điểm đến, thời lượng, ngân sách và preferences còn thiếu hoặc chưa rõ.  
Planning chỉ bắt đầu sau khi các trường bắt buộc đã đủ và người dùng đã trả lời câu hỏi bổ sung.

**Acceptance Criteria**
- [ ] Extract được date/origin/destination/duration/budget/preferences theo schema.
- [ ] Không bắt đầu planning khi thiếu date, origin hoặc budget.
- [ ] Câu hỏi bổ sung chỉ hỏi dữ liệu chưa đủ hoặc chưa rõ.

**Verification** Eval fixtures tiếng Việt cho complete, missing và ambiguous requests.

**Dependencies** Steps 3.4, 4.2 và 5.1.
**Files Related** requirement skills, trip request module, prompts, evals.

### Step 5.3 - Confirm Trip Request Summary

**Mô tả** Hiển thị trip request summary để người dùng kiểm tra, chỉnh sửa và xác nhận trước khi planning.  
Mỗi thay đổi trên field phải tạo version mới và giữ đầy đủ preferences cùng thông tin người đi cùng.  
Chỉ summary đã được xác nhận mới được sử dụng làm input cho Planner.

**Acceptance Criteria**
- [ ] Frontend hiển thị đầy đủ required fields, preferences và companions.
- [ ] User có thể sửa từng field và xem version mới.
- [ ] Chỉ summary đã xác nhận được dùng làm planning input.

**Verification** E2E test create → clarify → edit → confirm.

**Dependencies** Step 5.2.
**Files Related** trip request API, summary UI, version persistence, tests.

### Step 5.4 - Build Curated Destination Catalog

**Mô tả** Xây dựng place catalog có quy trình import hoặc seed dữ liệu rõ ràng.  
Mỗi địa điểm cần lưu source, thời điểm kiểm tra gần nhất, confidence và moderation status.  
Quy trình nhập phải chạy lặp an toàn, không tạo duplicate và chỉ đưa place hợp lệ vào suggestion.

**Acceptance Criteria**
- [ ] Place có nguồn, last_checked_at, confidence và moderation status.
- [ ] Chỉ place hợp lệ xuất hiện trong suggestion.
- [ ] Import lặp lại không tạo duplicate.

**Verification** Import integration test và catalog query test.

**Dependencies** Steps 2.2–2.3.
**Files Related** destination module, import script, migrations, test fixtures.

### Step 5.5 - Deliver Destination Search and Ranking

**Mô tả** Xây dựng chức năng tìm kiếm và xếp hạng địa điểm theo trip request summary cùng profile.  
Điểm xếp hạng cần xét thời gian, ngân sách, người tham gia và review đã kiểm chứng, đồng thời giải thích reason cụ thể.  
Người dùng có thể chọn hoặc bỏ chọn địa điểm và thấy summary được cập nhật tương ứng.

**Acceptance Criteria**
- [ ] Kết quả có suitability score và reason gắn với tiêu chí cụ thể.
- [ ] Thông tin biến động có source, checked_at và confidence.
- [ ] User chọn/bỏ chọn place và summary được cập nhật.

**Verification** Ranking tests và E2E selection flow.

**Dependencies** Steps 5.3–5.4.
**Files Related** recommendation skill, destination API, frontend discovery list, tests.

### Step 5.6 - Deliver Geospatial Discovery

**Mô tả** Cho phép tìm địa điểm trong một bán kính quanh GPS hoặc vị trí do người dùng nhập.  
Người dùng phải chọn rõ vị trí đó là origin hay search center, còn truy vấn khoảng cách được thực hiện bằng PostGIS.  
GPS chỉ được sử dụng khi consent của chuyến đi đang bật.

**Acceptance Criteria**
- [ ] User chọn rõ GPS là origin hay search center.
- [ ] Radius query dùng PostGIS và trả distance.
- [ ] GPS không được dùng khi trip consent đang tắt.

**Verification** PostGIS integration tests và browser permission-denied/allowed tests.

**Dependencies** Steps 2.3 và 5.4.
**Files Related** location API, geospatial repository, map UI, tests.

### Step 5.7 - Deliver Image-supported Discovery

**Mô tả** Cho phép upload ảnh và dùng vision tool để tìm địa điểm hoặc cảnh quan tương đồng.  
File phải được validation về loại và kích thước, còn object gốc có expires_at không quá 7 ngày.  
Kết quả cần mô tả điểm tương đồng, kèm confidence và tránh khẳng định tuyệt đối khi độ tin cậy thấp.

**Acceptance Criteria**
- [ ] File type/size được validate và object có expires_at tối đa 7 ngày.
- [ ] Kết quả nêu đặc điểm tương đồng và confidence.
- [ ] Confidence thấp được hiển thị như nhiều khả năng, không khẳng định tuyệt đối.

**Verification** Provider contract test, unsafe-file test và E2E upload/search.

**Dependencies** Steps 2.3, 3.5 và 5.4.
**Files Related** media module, vision tool adapter, discovery UI, tests.

### Checkpoint - Discovery Ready

- [ ] US01–US15 có trace tới implementation và test.
- [ ] Conversation → summary confirmation → destination selection hoạt động end-to-end.
- [ ] Radius và image discovery có nguồn/confidence.
- [ ] GPS/media có expires_at 7 ngày.

---

## Phase 6 - Itinerary Planning and Customization

### Step 6.1 - Generate One to Four Itineraries

**Mô tả** Tạo từ một đến bốn itinerary dựa trên summary đã được người dùng xác nhận.  
Mỗi phương án phải có lịch theo ngày, chi phí, di chuyển, hành lý, điểm nổi bật, cảnh báo và trade-offs.  
Tất cả itinerary đều phải qua Critic gate; phương án hard-fail không được hiển thị.

**Acceptance Criteria**
- [ ] Số itinerary nằm trong 1–4 và mỗi itinerary có daily schedule đầy đủ.
- [ ] Cost, transport, packing, highlights, warnings và trade-offs được trả theo schema.
- [ ] Không hiển thị itinerary hard-fail Critic.

**Verification** Integration/E2E test planning với 1 và nhiều phương án.

**Dependencies** Phases 4–5.
**Files Related** itinerary module, planning endpoint, planner/critic integration, tests.

### Step 6.2 - Build Itinerary Comparison Workspace

**Mô tả** Xây dựng không gian so sánh tối đa bốn itinerary trên desktop và mobile.  
Người dùng cần thấy rõ thời lượng, chi phí, điểm nổi bật, warning, reason và nguồn của dữ liệu biến động.  
Trạng thái empty, error hoặc partial không được làm mất trip request đang thao tác.

**Acceptance Criteria**
- [ ] UI so sánh được tối đa 4 itinerary trên desktop và mobile.
- [ ] Source/confidence có thể mở xem tại dữ liệu biến động.
- [ ] Empty/error/partial-state không làm mất request hiện tại.

**Verification** Component tests, responsive browser test và E2E comparison.

**Dependencies** Step 6.1.
**Files Related** frontend itinerary feature, API query, shared components, tests.

### Step 6.3 - Add Manual Editing and Plan Versioning

**Mô tả** Cho phép chỉnh sửa thủ công place, lodging, activity, movement và các item trong itinerary.  
Mỗi thay đổi phải tạo version có kiểm soát, đồng thời tính lại dữ liệu liên quan về chi phí, thời gian và hành lý.  
Thay đổi quan trọng phải chạy lại Critic trước khi được dùng tiếp.

**Acceptance Criteria**
- [ ] Manual edit không overwrite version ngoài ý muốn.
- [ ] Related cost/time/packing data được tính lại.
- [ ] Important change bắt buộc chạy Critic lại.

**Verification** API concurrency/version tests và E2E manual edit.

**Dependencies** Steps 2.2 và 6.1.
**Files Related** itinerary commands, version repository, editor UI, tests.

### Step 6.4 - Create Agent Change Proposal

**Mô tả** Cho phép Agent tạo change proposal nhưng chưa áp dụng trực tiếp vào plan.  
Proposal cần ghi base plan version, diff, các phần bị ảnh hưởng, reason và warning, đồng thời giữ nguyên phần ngoài phạm vi yêu cầu.  
Proposal phải hết hiệu lực nếu base version đã thay đổi.

**Acceptance Criteria**
- [ ] Proposal tham chiếu base plan version.
- [ ] Phần ngoài phạm vi yêu cầu không bị thay đổi.
- [ ] Proposal hết hiệu lực nếu base version đã thay đổi.

**Verification** Unit/integration tests cho scoped diff và stale proposal.

**Dependencies** Steps 4.2 và 6.3.
**Files Related** proposal model, Planner adjustment flow, diff builder, tests.

### Step 6.5 - Accept or Reject Agent Proposal

**Mô tả** Hiển thị proposal để người dùng chủ động chấp nhận hoặc từ chối trước khi cập nhật plan.  
Accept tạo version mới sau các bước validation và Critic cần thiết, còn reject giữ nguyên plan và ghi decision event.  
Không endpoint nội bộ nào được bỏ qua bước xác nhận đối với finalized plan.

**Acceptance Criteria**
- [ ] Accept tạo version mới sau validation/Critic cần thiết.
- [ ] Reject giữ nguyên plan và ghi decision event.
- [ ] Không có endpoint nội bộ nào bypass confirmation cho finalized plan.

**Verification** E2E accept/reject và authorization test cho bypass attempt.

**Dependencies** Step 6.4.
**Files Related** proposal API, confirmation UI, audit event, tests.

### Step 6.6 - Finalize and Reopen Plan

**Mô tả** Cho phép người dùng finalize plan để sử dụng trong chuyến đi và mở lại khi cần thay đổi.  
Finalized plan phải tham chiếu một version bất biến, còn replan tạo proposal mới thay vì sửa lịch sử.  
Ứng dụng mobile phải tải được plan đã lưu mà không cần generate lại.

**Acceptance Criteria**
- [ ] Finalized plan có immutable version reference.
- [ ] Replan tạo proposal mới, không sửa lịch sử.
- [ ] Mobile view tải plan đã lưu mà không cần generate lại.

**Verification** E2E finalize → reload → propose change.

**Dependencies** Steps 6.1–6.5.
**Files Related** plan lifecycle, mobile itinerary view, tests.

### Checkpoint - Planning Ready

- [ ] US16–US28 có trace tới implementation và test.
- [ ] Planner/Critic loop chạy bắt buộc.
- [ ] Manual edit và Agent proposal có versioning.
- [ ] Accept/reject hoạt động và reject không đổi plan.

---

## Phase 7 - Booking and Logistics

### Step 7.1 - Define Booking Provider Contract

**Mô tả** Định nghĩa contract chung cho kết quả tìm kiếm từ các booking provider.  
Contract phải hỗ trợ tối thiểu hotel, flight và ground transport, bao gồm giá, điều khoản hủy hoặc đổi và redirect.  
Không đưa command thanh toán hay giữ chỗ tự động vào contract; provider chưa sẵn sàng dùng fake hoặc sandbox adapter.

**Acceptance Criteria**
- [ ] Contract hỗ trợ hotel, flight và ground transport tối thiểu.
- [ ] Có fake/sandbox adapter cho test.
- [ ] Contract không có command thanh toán hoặc giữ chỗ tự động.

**Verification** Provider contract tests và forbidden-operation review.

**Dependencies** Steps 3.5 và 4.4.
**Files Related** provider ports, booking models, fake adapter, tests.

### Step 7.2 - Deliver Search and Comparison Slice

**Mô tả** Tìm các dịch vụ phù hợp với itinerary và so sánh kết quả từ nhiều provider.  
Kết quả phải gắn với plan version và passenger constraints hiện tại, đồng thời hiển thị provider cùng checked_at.  
Lỗi từ một provider không được làm mất các kết quả hợp lệ từ provider khác.

**Acceptance Criteria**
- [ ] Search gắn với plan version và passenger constraints hiện tại.
- [ ] Result hiển thị checked_at và provider.
- [ ] Provider failure không làm mất các result hợp lệ khác.

**Verification** Integration test nhiều fake provider và partial failure.

**Dependencies** Step 7.1.
**Files Related** booking module, Booking Agent flow, comparison API, tests.

### Step 7.3 - Prepare Passenger Information Safely

**Mô tả** Thu thập tối thiểu thông tin hành khách cần thiết cho dịch vụ mà người dùng đã chọn.  
Dữ liệu nhạy cảm không được xuất hiện trong log hoặc trace và chỉ được gửi tới provider sau khi người dùng xác nhận.  
Không chia sẻ dữ liệu với bất kỳ provider nào chưa được lựa chọn.

**Acceptance Criteria**
- [ ] Field nhạy cảm không xuất hiện trong log/trace.
- [ ] User xem và xác nhận dữ liệu trước redirect.
- [ ] Data không được gửi cho provider chưa chọn.

**Verification** Security tests, log inspection và E2E confirmation.

**Dependencies** Steps 2.4 và 7.2.
**Files Related** passenger form/API, redaction rules, booking UI, tests.

### Step 7.4 - Implement Partner Redirect

**Mô tả** Hiển thị final price và terms trước khi chuyển người dùng sang trang của partner.  
Redirect chỉ được trỏ tới HTTPS destination trong allow-list và giao diện phải nói rõ giao dịch diễn ra ngoài hệ thống.  
Sự kiện redirect được audit nhưng không được chứa payment data.

**Acceptance Criteria**
- [ ] Redirect chỉ dùng allow-listed HTTPS destination.
- [ ] UI nói rõ giao dịch nằm ngoài Tour Guide Agent.
- [ ] Redirect event được audit nhưng không chứa payment data.

**Verification** E2E redirect và open-redirect security test.

**Dependencies** Steps 7.2–7.3.
**Files Related** redirect endpoint, booking UI, allow-list config, tests.

### Step 7.5 - Verify Booking Guardrails

**Mô tả** Kiểm tra xuyên suốt các guardrail để Agent và API không thể tự thực hiện giao dịch.  
Adversarial prompt không được tạo forbidden tool call và provider adapter không được expose action bị cấm.  
Khi chặn hành động, audit reason phải đủ rõ để nhóm vận hành hiểu nguyên nhân.

**Acceptance Criteria**
- [ ] Adversarial prompts không tạo forbidden tool call.
- [ ] Provider adapter không expose forbidden action.
- [ ] Audit reason giải thích rõ hành động bị chặn.

**Verification** Red-team tests trên Agent, Tool Registry và API.

**Dependencies** Steps 7.1–7.4.
**Files Related** guardrail tests, booking integration tests, eval fixtures.

### Checkpoint - Booking Ready

- [ ] US29–US34 có trace tới implementation và test.
- [ ] Search/compare/redirect hoạt động với sandbox provider.
- [ ] Passenger data được redacted.
- [ ] Không có đường tự động giao dịch.

---

## Phase 8 - In-trip Experience and Realtime Monitoring

### Step 8.1 - Implement Trip Activation and GPS Consent

**Mô tả** Quản lý vòng đời chuyến đi qua các trạng thái upcoming, active và ended.  
GPS mặc định tắt, chỉ bắt đầu thu thập sau explicit consent và phải dừng ngay khi người dùng thu hồi quyền.  
Mọi GPS event cần có expires_at không quá 7 ngày và chỉ được dùng trong đúng chuyến đi.

**Acceptance Criteria**
- [ ] GPS mặc định tắt và chỉ thu thập sau explicit consent.
- [ ] User tắt GPS thì ingestion dừng và downstream không dùng dữ liệu mới.
- [ ] GPS event hết hạn tối đa sau 7 ngày.

**Verification** E2E consent on/off và retention metadata test.

**Dependencies** Steps 2.3, 2.4 và 6.6.
**Files Related** trip lifecycle, location ingestion, companion UI, tests.

### Step 8.2 - Deliver Destination Q&A

**Mô tả** Cung cấp chức năng hỏi đáp về lịch sử, văn hóa, giá vé, giờ mở cửa và điều kiện tham quan.  
Hệ thống phải phân biệt stable fact với volatile fact; dữ liệu biến động luôn đi kèm source, checked_at và confidence.  
Nếu bằng chứng chưa đủ, câu trả lời cần nói rõ giới hạn thay vì tự suy đoán.

**Acceptance Criteria**
- [ ] Stable facts và volatile facts được phân biệt.
- [ ] Volatile facts luôn có source, checked_at và confidence.
- [ ] Câu trả lời không đủ bằng chứng nói rõ giới hạn thay vì suy đoán.

**Verification** Grounded-answer eval và missing-source negative test.

**Dependencies** Steps 3.5, 5.4 và 8.1.
**Files Related** guide skills, travel data tools, companion API/UI, evals.

### Step 8.3 - Add Place Identification

**Mô tả** Nhận diện địa điểm từ ảnh hoặc text trong trải nghiệm đồng hành cùng chuyến đi.  
Khi confidence thấp, hệ thống cần đưa ra nhiều khả năng và hỏi thêm thay vì khẳng định một kết quả duy nhất.  
Media gốc được bảo vệ bằng thời hạn lưu trữ tối đa 7 ngày.

**Acceptance Criteria**
- [ ] Confidence thấp trả nhiều khả năng và clarification prompt.
- [ ] Không khẳng định duy nhất khi chưa qua threshold.
- [ ] Media gốc có expires_at tối đa 7 ngày.

**Verification** Vision contract tests và E2E high/low-confidence cases.

**Dependencies** Steps 3.5, 5.7 và 8.2.
**Files Related** vision tool, identification skill, companion UI, tests.

### Step 8.4 - Add Proximity Narration and TTS

**Mô tả** Gợi ý nội dung thuyết minh khi người dùng đến gần một điểm trong itinerary.  
Logic proximity chỉ hoạt động khi GPS consent đang bật và notification không được tự phát audio.  
TTS chỉ nhận nội dung đã qua output validation và chỉ phát sau thao tác xác nhận của người dùng.

**Acceptance Criteria**
- [ ] Proximity logic chỉ chạy khi GPS consent bật.
- [ ] Notification không tự phát audio.
- [ ] TTS chỉ nhận nội dung đã qua output validation.

**Verification** Unit test geofence và browser E2E notification/confirm/play.

**Dependencies** Steps 8.1–8.3.
**Files Related** proximity service, TTS tool, notification/audio UI, tests.

### Step 8.5 - Implement Background Scheduler

**Mô tả** Xây dựng scheduler cho các recurring job ngay trong modular monolith.  
PostgreSQL coordination lock và idempotency giúp nhiều worker không chạy trùng cùng một lượt job.  
Mỗi job cần run ID, timeout, retry có giới hạn và trạng thái đủ rõ để theo dõi khi restart.

**Acceptance Criteria**
- [ ] Nhiều worker chỉ có một scheduler thực thi mỗi lượt job.
- [ ] Job có run ID, timeout, retry giới hạn và observable status.
- [ ] Restart không tạo duplicate side effect.

**Verification** Multi-worker integration test và crash/restart test.

**Dependencies** Steps 1.4 và 2.1.
**Files Related** backend/app/jobs/runtime/, job tables/locks, tests.

### Step 8.6 - Implement Weather Monitor Job

**Mô tả** Tạo Weather Monitor job để định kỳ kiểm tra active trip theo cadence cấu hình.  
Job theo dõi weather, travel time và opening hours, đồng thời tránh tạo alert trùng khi dữ liệu không đổi.  
Thay đổi đáng kể phải tạo cảnh báo có source, confidence và có thể yêu cầu Planner đề xuất phương án khác.

**Acceptance Criteria**
- [ ] Chỉ active trip được quét theo cadence cấu hình.
- [ ] Unchanged data không tạo duplicate alert.
- [ ] Significant change tạo alert có source/confidence và có thể yêu cầu Planner đề xuất thay thế.

**Verification** Time-controlled integration tests cho unchanged, warning và critical cases.

**Dependencies** Steps 3.5, 4.2 và 8.5.
**Files Related** backend/app/jobs/weather_monitor.py, provider tools, alerts, tests.

### Step 8.7 - Deliver Alert and Approved Replanning

**Mô tả** Hiển thị cảnh báo cùng phương án thay thế khi một địa điểm đóng cửa hoặc không còn an toàn.  
Phương án mới luôn xuất hiện dưới dạng proposal và không tự động sửa finalized plan.  
Việc accept hoặc reject phải dùng lại quy tắc version và confirmation đã thiết lập ở Phase 6.

**Acceptance Criteria**
- [ ] Closed/unsafe destination được đánh dấu rõ.
- [ ] Alternative xuất hiện dưới dạng proposal, không auto-apply.
- [ ] Accept/reject dùng cùng version/confirmation rules Phase 6.

**Verification** E2E weather event → proposal → accept/reject.

**Dependencies** Steps 6.4–6.5 và 8.6.
**Files Related** alert API/UI, planning proposal integration, tests.

### Checkpoint - In-trip Ready

- [ ] US35–US45 có trace tới implementation và test.
- [ ] GPS opt-in/off được kiểm chứng.
- [ ] Weather job không chạy trùng.
- [ ] Alert/replan không bypass user confirmation.
- [ ] Audio không tự phát.

---

## Phase 9 - Reviews and Moderation

### Step 9.1 - Deliver Private Review Slice

**Mô tả** Cho phép người dùng rating và comment cho place hoặc experience sau chuyến đi.  
Mọi review mới đều ở trạng thái private và chỉ owner có quyền xem hoặc chỉnh sửa.  
Người dùng khác tuyệt đối không được truy cập private review.

**Acceptance Criteria**
- [ ] Review mới luôn private.
- [ ] Owner có thể edit và xem review của mình.
- [ ] Người khác không đọc private review.

**Verification** API authorization tests và E2E create/edit private review.

**Dependencies** Steps 2.4–2.5 và 5.4.
**Files Related** review module, API, frontend review form, tests.

### Step 9.2 - Add Publication and Moderation

**Mô tả** Cho phép người dùng yêu cầu công khai review và đưa nội dung qua quy trình moderation.  
Quy trình kiểm tra content, spam, relevance và tính hợp lệ của chuyến đi trước khi hiển thị công khai.  
Review bị từ chối vẫn private, có reason phù hợp và người dùng có thể chuyển review công khai về private.

**Acceptance Criteria**
- [ ] Public request đi qua moderation state machine.
- [ ] Rejected content không public và có reason phù hợp.
- [ ] User có thể chuyển public review về private.

**Verification** Moderation scenario tests và E2E publish/unpublish.

**Dependencies** Step 9.1.
**Files Related** moderation service, review states, UI, tests.

### Step 9.3 - Implement Review Reporting

**Mô tả** Cho phép người dùng report một public review và để operator xử lý theo đúng role.  
Hệ thống không tạo duplicate report đang mở và mọi state transition đều phải được audit.  
API cần hỗ trợ đầy đủ luồng tạo, giải quyết hoặc từ chối report với authorization rõ ràng.

**Acceptance Criteria**
- [ ] User report với reason và không tạo duplicate report mở.
- [ ] Operator xử lý theo authorization.
- [ ] Tất cả state transition được audit.

**Verification** API integration tests cho create/resolve/reject report và role checks.

**Dependencies** Steps 2.4 và 9.2.
**Files Related** report model/API, operator UI, audit hooks, tests.

### Step 9.4 - Feed Valid Reviews into Ranking

**Mô tả** Chỉ sử dụng public review hợp lệ làm tín hiệu cho hệ thống ranking.  
Review private, pending, rejected hoặc bị ẩn do report không được ảnh hưởng tới kết quả xếp hạng.  
Mỗi ranking signal phải truy ngược được về review nguồn và cập nhật nhất quán khi moderation thay đổi.

**Acceptance Criteria**
- [ ] Private, pending, rejected hoặc reported-hidden review không ảnh hưởng ranking.
- [ ] Ranking signal có thể truy về nguồn review.
- [ ] Thay đổi moderation cập nhật signal nhất quán.

**Verification** Ranking integration tests cho từng review state.

**Dependencies** Steps 5.5 và 9.2–9.3.
**Files Related** ranking query, review projections, tests.

### Checkpoint - Reviews Ready

- [ ] US46–US51 có trace tới implementation và test.
- [ ] Private-by-default được kiểm chứng.
- [ ] Moderation/report/ranking state nhất quán.

---

## Phase 10 - Trip Summary and Personalization

### Step 10.1 - Implement Trip Completion Job

**Mô tả** Tạo Trip Completion job để phát hiện chuyến đi đã kết thúc hoặc được kết thúc sớm.  
Mỗi trip chỉ có một summary draft đang hoạt động và job phải idempotent khi retry hoặc chạy trên nhiều worker.  
Khi draft sẵn sàng, hệ thống gửi notification để người dùng tiếp tục hoàn thiện.

**Acceptance Criteria**
- [ ] Mỗi trip completion chỉ có một draft active.
- [ ] Job idempotent khi retry hoặc nhiều worker.
- [ ] User nhận notification khi draft sẵn sàng.

**Verification** Time-controlled, duplicate-run và early-end integration tests.

**Dependencies** Steps 8.1 và 8.5.
**Files Related** backend/app/jobs/trip_completion.py, summary model, notification, tests.

### Step 10.2 - Classify Actual Trip Activity

**Mô tả** Đối chiếu finalized plan với confirmation, interaction và GPS nếu người dùng đã bật consent.  
Summary draft phân loại hoạt động thành visited, skipped hoặc unplanned và lưu evidence tương ứng.  
Người dùng có thể sửa classification trước khi xác nhận, còn GPS không được dùng nếu consent đang tắt.

**Acceptance Criteria**
- [ ] Draft phân loại visited/skipped/unplanned với evidence.
- [ ] Không dùng GPS khi consent tắt.
- [ ] User chỉnh lại classification trước confirm.

**Verification** Scenario tests với GPS on/off và E2E correction.

**Dependencies** Steps 8.1 và 10.1.
**Files Related** summary classifier, trip evidence query, correction UI, tests.

### Step 10.3 - Add Actual Expense Comparison

**Mô tả** Cho phép nhập actual expense theo category và so sánh với estimate của itinerary.  
Việc nhập chi phí là tùy chọn; giá trị còn thiếu không được tự động coi là zero.  
Hệ thống cần tính đúng total, chênh lệch tuyệt đối và tỷ lệ phần trăm theo currency.

**Acceptance Criteria**
- [ ] Không nhập chi phí vẫn hoàn thành summary.
- [ ] Hệ thống không suy diễn missing amount bằng zero.
- [ ] Tính total, absolute difference và percentage đúng với currency.

**Verification** Unit/property tests cho money calculation và E2E skip/input flows.

**Dependencies** Steps 6.1 và 10.1.
**Files Related** expense model/service, summary API/UI, tests.

### Step 10.4 - Add Diary, Ratings and Media

**Mô tả** Cho phép bổ sung overall rating, diary, place review và ảnh vào trip summary.  
Place review vẫn private theo mặc định, còn media gốc phải hiển thị rõ ngày hết hạn và bị xóa sau tối đa 7 ngày.  
Structured summary vẫn phải tồn tại bình thường sau khi media gốc hết hạn.

**Acceptance Criteria**
- [ ] Place review vẫn private mặc định.
- [ ] Media gốc hiển thị rõ ngày hết hạn và bị xóa sau tối đa 7 ngày.
- [ ] Summary có thể tồn tại sau khi media gốc hết hạn.

**Verification** E2E summary media flow và expiry behavior test.

**Dependencies** Steps 2.3, 9.1 và 10.1.
**Files Related** summary UI, media metadata, review integration, tests.

### Step 10.5 - Confirm Summary and Update Profile

**Mô tả** Khóa summary sau khi người dùng xác nhận và cập nhật preference vào profile.  
Chỉ confirmed summary mới được dùng để trích xuất sở thích, financial pace và travel pace, kèm provenance về summary nguồn.  
Temporary Agent memory không được thay thế cho dữ liệu profile đã xác nhận.

**Acceptance Criteria**
- [ ] Chỉ confirmed summary cập nhật profile.
- [ ] Dữ liệu profile có provenance về summary.
- [ ] Agent memory tạm không được giữ thay cho profile.

**Verification** Integration test draft/no-update và confirm/update.

**Dependencies** Steps 2.5 và 10.2–10.4.
**Files Related** summary confirmation, profile updater, audit, tests.

### Step 10.6 - Suggest and Start Next Trip

**Mô tả** Tạo từ một đến ba gợi ý cho chuyến đi tiếp theo dựa trên profile và confirmed history.  
Mỗi suggestion cần có reason; khi được chọn, hệ thống mở conversation mới thay vì sửa trip cũ.  
Dữ liệu prefill vẫn phải được người dùng kiểm tra và xác nhận như một trip request mới.

**Acceptance Criteria**
- [ ] Suggestion dựa trên profile/confirmed history và có reason.
- [ ] Chọn suggestion tạo conversation mới, không sửa trip cũ.
- [ ] Prefill vẫn yêu cầu user xác nhận summary trip request mới.

**Verification** E2E confirm summary → suggestions → new trip request.

**Dependencies** Steps 5.1–5.3 và 10.5.
**Files Related** personalization skill, suggestion API/cards, new conversation flow, tests.

### Checkpoint - Summary Ready

- [ ] US52–US64 có trace tới implementation và test.
- [ ] Completion job idempotent.
- [ ] Expense optionality đúng.
- [ ] Confirmed profile update tách khỏi temporary memory.
- [ ] Media expiry không xóa structured summary.

---

## Phase 11 - Audit, Retention and Privacy Operations

### Step 11.1 - Complete Audit Event Model

**Mô tả** Hoàn thiện audit event cho metadata đầu vào, đầu ra, source, tool, result, error và Agent handoff.  
Event phải có correlation, run, trip và Agent identifier nhưng không chứa PII, secret hoặc raw chain-of-thought.  
Detailed event cần có expires_at không quá 7 ngày.

**Acceptance Criteria**
- [ ] Event có correlation/run/trip/Agent identifiers.
- [ ] PII/secret/raw chain-of-thought không xuất hiện.
- [ ] Detailed event có expires_at tối đa 7 ngày.

**Verification** Schema tests, redaction tests và representative trace snapshot.

**Dependencies** Steps 3.8 và 4.5.
**Files Related** audit model, trace serializer, migrations, tests.

### Step 11.2 - Enforce Purpose and Ticket ID

**Mô tả** Bảo vệ endpoint xem log chi tiết bằng role, mục đích truy cập và Ticket ID bắt buộc.  
Mỗi access event phải ghi identity, thời gian, IP, purpose và Ticket ID của người truy cập.  
Search metadata không được làm lộ nội dung chi tiết trước khi access guard cho phép.

**Acceptance Criteria**
- [ ] Thiếu một trong hai field thì không mở log.
- [ ] Access event ghi identity, time, IP, purpose và Ticket ID.
- [ ] Search metadata không làm lộ detail trước khi access guard pass.

**Verification** Authorization/audit tests cho đủ/thiếu/sai role.

**Dependencies** Steps 2.4 và 11.1.
**Files Related** audit API, access guard, operator form, tests.

### Step 11.3 - Build Execution Trace Viewer

**Mô tả** Xây dựng viewer cho operator và engineer theo dõi execution trace của Agent.  
Viewer hiển thị input/output summary, tool, result, error và handoff, đồng thời hỗ trợ filter theo trip, Agent, mã lỗi và thời gian.  
Mọi lần mở detail phải qua access guard và không được hiển thị chain-of-thought hay field đã redacted.

**Acceptance Criteria**
- [ ] Filter theo trip ID, Agent, error code và time range.
- [ ] Viewer không hiển thị chain-of-thought hoặc redacted fields.
- [ ] Mở detail luôn đi qua Step 11.2.

**Verification** E2E operator/engineer viewer và negative role test.

**Dependencies** Steps 11.1–11.2.
**Files Related** audit query API, operations UI, trace visualization, tests.

### Step 11.4 - Apply Seven-day Expiry Consistently

**Mô tả** Áp dụng chính sách hết hạn 7 ngày cho GPS, media gốc, working memory, trip memory và detailed audit log.  
Repository phải chặn đọc expired data ngay cả khi dữ liệu chưa được physical deletion.  
Confirmed structured record không thuộc nhóm dữ liệu tạm và không được loại bởi filter này.

**Acceptance Criteria**
- [ ] Tất cả record/object thuộc scope có expires_at không quá 7 ngày.
- [ ] Expired data bị chặn đọc ngay cả trước physical deletion.
- [ ] Confirmed structured records không bị query filter này loại.

**Verification** Time-travel integration tests cho trước/đúng/sau expiry.

**Dependencies** Steps 2.2–2.3, 3.7 và 11.1.
**Files Related** shared retention policy, repositories, object metadata, tests.

### Step 11.5 - Implement Daily Retention Cleanup Cron

**Mô tả** Tạo cron job hằng ngày để đánh dấu hết hạn, xóa hoặc ẩn danh database data và xóa object.  
Job phải idempotent, dùng scheduler lock và retry được sau partial failure mà không xóa nhầm confirmed data.  
Kết quả cleanup được ghi bằng metric và audit summary nhưng không chứa payload đã xóa.

**Acceptance Criteria**
- [ ] Job idempotent và dùng scheduler lock.
- [ ] Partial failure có thể retry mà không xóa confirmed structured data.
- [ ] Kết quả cleanup có metric/audit summary không chứa payload đã xóa.

**Verification** Integration test mixed-age data, partial object-store failure và rerun.

**Dependencies** Steps 8.5 và 11.4.
**Files Related** backend/app/jobs/retention_cleanup.py, repositories, object store adapter, tests.

### Step 11.6 - Verify Consent and Data Boundaries

**Mô tả** Kiểm tra xuyên hệ thống các boundary về GPS consent, media access, account ownership và quyền xem technical log.  
Việc thu hồi consent phải chặn ingestion và sử dụng GPS mới; signed media URL cần hết hạn và kiểm tra ownership.  
Mọi truy cập sai account hoặc sai role phải bị chặn và được audit.

**Acceptance Criteria**
- [ ] Revoked GPS consent ngăn ingestion/use mới.
- [ ] Signed media access hết hạn và kiểm tra ownership.
- [ ] Cross-account/cross-role access bị chặn và audit.

**Verification** Security integration suite và manual privacy review.

**Dependencies** Steps 8.1, 10.4 và 11.2–11.5.
**Files Related** authorization policies, signed URL service, privacy tests.

### Checkpoint - Audit and Retention Ready

- [ ] US65–US70 có trace tới implementation và test.
- [ ] Purpose + Ticket ID được enforce.
- [ ] Dữ liệu tạm hết hạn sau 7 ngày.
- [ ] Cleanup cron chạy idempotent.
- [ ] Confirmed business records không bị xóa nhầm.

---

## Phase 12 - Quality, Security and Evaluation

### Step 12.1 - Complete Automated Test Pyramid

**Mô tả** Hoàn thiện test pyramid gồm unit, contract, integration và E2E cho các luồng quan trọng.  
Mỗi module cần được kiểm tra tại boundary có rủi ro cao, còn integration test dùng PostgreSQL/PostGIS và Object Storage thật trong CI.  
Các E2E journey quan trọng phải chạy ổn định mà không phụ thuộc vào production provider.

**Acceptance Criteria**
- [ ] Mỗi module có test tại boundary rủi ro chính.
- [ ] Integration test dùng PostgreSQL/PostGIS và Object Storage thật trong CI.
- [ ] Critical E2E journeys chạy ổn định không phụ thuộc provider production.

**Verification** make test, make integration-test và make e2e pass nhiều lần liên tiếp.

**Dependencies** Phases 2–11.
**Files Related** backend/tests/, frontend/tests/, e2e/, CI.

### Step 12.2 - Build LLM Evaluation Suite

**Mô tả** Xây dựng bộ LLM evaluation bằng dữ liệu tiếng Việt cho các khả năng AI chính.  
Dataset cần bao phủ requirement extraction, recommendation, planning, Critic và grounded answer với cả trường hợp bình thường, mơ hồ, không an toàn và bất khả thi.  
Mỗi lần đổi prompt hoặc model phải có regression eval và so sánh với baseline đã duyệt.

**Acceptance Criteria**
- [ ] Eval dataset có normal, ambiguous, unsafe và impossible cases.
- [ ] Có threshold cho schema validity, grounding, tool correctness và Critic recall.
- [ ] Prompt/model change chạy regression eval trong CI phù hợp.

**Verification** Chạy eval bằng fixed fixtures và lưu báo cáo baseline.

**Dependencies** Phases 3–8.
**Files Related** backend/tests/evals/, datasets, evaluator scripts, CI.

### Step 12.3 - Perform Threat Modeling and Hardening

**Mô tả** Thực hiện threat modeling cho authentication, prompt injection, tool abuse, SSRF, upload và open redirect.  
Phạm vi cũng bao gồm PII leakage, provider compromise, egress policy và URL allow-list.  
Mọi phát hiện high-risk cần mitigation rõ ràng và automated regression test tương ứng.

**Acceptance Criteria**
- [ ] Threat model có asset, boundary, attack và mitigation.
- [ ] High-risk findings có automated regression test.
- [ ] Tool/provider egress và URL allow-list được enforce.

**Verification** Security test suite và review checklist được ký duyệt.

**Dependencies** Phases 2–11.
**Files Related** docs/security/, guardrails, upload/redirect/provider policies, tests.

### Step 12.4 - Validate Accessibility and Responsive UX

**Mô tả** Kiểm tra accessibility và responsive UX trên các journey cốt lõi của frontend.  
Người dùng phải thao tác được bằng keyboard, nhận focus, label, error và streaming status rõ ràng, kể cả với screen reader cơ bản.  
Chat, itinerary comparison và trip companion cần hoạt động trên các viewport mobile mục tiêu.

**Acceptance Criteria**
- [ ] Core journeys dùng được bằng keyboard.
- [ ] Form/error/streaming update có accessible labels/status.
- [ ] Chat, comparison và trip companion hoạt động trên viewport mục tiêu.

**Verification** Automated accessibility scan và manual keyboard/mobile review.

**Dependencies** Phases 5–11.
**Files Related** frontend shared UI/features, E2E accessibility tests.

### Step 12.5 - Test Performance and Capacity

**Mô tả** Đo performance của API, SSE, spatial query, Agent run và background job.  
Thiết lập baseline cùng target cho latency, concurrency và throughput, đồng thời rà query plan để tránh full scan ngoài dự kiến.  
Rate limit và backpressure phải bảo vệ được model/provider budget khi tải tăng.

**Acceptance Criteria**
- [ ] Có baseline và target cho các operation chính.
- [ ] Spatial query và history query không full-scan ngoài dự kiến.
- [ ] Rate limit/backpressure bảo vệ model/provider budget.

**Verification** Load tests và database query-plan review.

**Dependencies** Phases 5–11.
**Files Related** load-tests/, indexes, rate limiting, performance report.

### Step 12.6 - Test Failure and Recovery

**Mô tả** Mô phỏng lỗi timeout hoặc partial failure từ LLM, provider, database và Object Storage.  
Kiểm tra scheduler restart, retry và recovery để bảo đảm không mất confirmed data hoặc tạo duplicate plan, summary hay alert.  
Các cơ chế circuit breaker và bounded retry không được gây retry storm.

**Acceptance Criteria**
- [ ] User nhận error/retry state rõ ràng và không mất confirmed data.
- [ ] Job retry không tạo duplicate plan/summary/alert.
- [ ] Circuit/bounded retry không gây retry storm.

**Verification** Fault-injection integration tests và recovery checklist.

**Dependencies** Phases 3–11.
**Files Related** resilience policies, integration tests, job tests.

### Checkpoint - Quality Gate

- [ ] Full automated suite pass.
- [ ] LLM eval đạt threshold được duyệt.
- [ ] Không còn high-risk security finding mở.
- [ ] Accessibility và performance đạt target.
- [ ] Failure recovery được kiểm chứng.

---

## Phase 13 - Observability and Deployment

### Step 13.1 - Add Production Observability

**Mô tả** Bổ sung structured log, metric, distributed trace và dashboard cho môi trường production.  
Correlation ID phải nối được API request với Agent run và job run để hỗ trợ điều tra lỗi end-to-end.  
Dashboard và alert chỉ dùng metadata cần thiết, không chứa payload nhạy cảm.

**Acceptance Criteria**
- [ ] Có metrics cho latency/error/model/tool/job/cleanup.
- [ ] Correlation ID nối API request với Agent run và job run.
- [ ] Dashboard/alert không chứa payload nhạy cảm.

**Verification** Gây lỗi thử và theo dấu end-to-end trên local/staging observability.

**Dependencies** Phases 3, 8 và 11.
**Files Related** observability config, instrumentation, dashboards, alerts.

### Step 13.2 - Build Production Images

**Mô tả** Tạo production image tối thiểu cho backend và frontend với dependency được khóa phiên bản.  
Container phải chạy non-root, có health check và không chứa secret hoặc dev dependency không cần thiết.  
Quy trình build cần reproducible và đáp ứng vulnerability scan policy.

**Acceptance Criteria**
- [ ] Build reproducible và pin dependency lock files.
- [ ] Image không chứa source secret/dev dependency không cần thiết.
- [ ] Container chạy non-root và pass vulnerability scan policy.

**Verification** Build/run images và container security scan.

**Dependencies** Phase 12.
**Files Related** backend/frontend container files, build scripts, CI.

### Step 13.3 - Provision Staging Environment

**Mô tả** Chuẩn bị staging có PostgreSQL/PostGIS, Object Storage, secret, provider sandbox và ingress TLS.  
Cấu hình staging phải tách khỏi production và migration được chạy như một deployment step có kiểm soát.  
Sau mỗi lần deploy, nhóm phải chạy được smoke test và integration test cần thiết.

**Acceptance Criteria**
- [ ] Environment config tách biệt production.
- [ ] Migration được chạy như deployment step có kiểm soát.
- [ ] Smoke test có thể chạy sau deploy.

**Verification** Deploy staging từ clean environment và chạy smoke/integration tests.

**Dependencies** Steps 13.1–13.2.
**Files Related** infra deployment manifests, secret config, CI/CD.

### Step 13.4 - Establish Backup and Restore

**Mô tả** Thiết lập backup cho PostgreSQL và quy định rõ retention behavior của Object Storage.  
Backup không được kéo dài thời gian tồn tại của sensitive data đã hết hạn ngoài policy được duyệt.  
Quy trình restore, recovery objective và hướng dẫn vận hành cần được kiểm chứng bằng restore drill.

**Acceptance Criteria**
- [ ] Backup không kéo dài lifetime của expired sensitive data ngoài policy đã duyệt.
- [ ] Restore database vào isolated environment thành công.
- [ ] Recovery objectives và procedure được ghi trong runbook.

**Verification** Thực hiện restore drill và kiểm tra dữ liệu/retention metadata.

**Dependencies** Step 13.3.
**Files Related** backup config, scripts, runbook, drill report.

### Step 13.5 - Implement Deployment and Rollback

**Mô tả** Tự động hóa việc deploy versioned artifact, chạy migration, smoke test và rollback.  
Pipeline phải dừng rollout khi migration hoặc smoke test thất bại và luôn sử dụng immutable version hoặc tag.  
Rollback application không được làm hỏng database schema hoặc dữ liệu đã xác nhận.

**Acceptance Criteria**
- [ ] Deploy dùng immutable version/tag.
- [ ] Failure ở migration/smoke test dừng rollout.
- [ ] Rollback application không làm database schema hỏng.

**Verification** Staging deploy thành công và rollback drill.

**Dependencies** Steps 13.2–13.4.
**Files Related** CI/CD workflows, deployment manifests, migration/runbook.

### Step 13.6 - Validate Scheduler Operations

**Mô tả** Xác nhận Weather Monitor, Trip Completion và Retention Cleanup chạy đúng trên staging và production.  
Trong mô hình nhiều instance, mỗi lượt chỉ có một scheduler leader và mọi delay, failure hoặc duplicate attempt đều tạo metric cùng alert.  
Retention Cleanup phải chạy hằng ngày và báo cáo được số record đã hết hạn hoặc bị xóa.

**Acceptance Criteria**
- [ ] Chỉ một scheduler leader chạy mỗi lượt.
- [ ] Job delay/failure/duplicate-attempt tạo metric và alert.
- [ ] Retention Cleanup chạy hằng ngày và có báo cáo số lượng expired/deleted.

**Verification** Multi-instance staging soak test qua ít nhất một chu kỳ job/cron thử nghiệm.

**Dependencies** Steps 8.5–8.7, 10.1, 11.5 và 13.3.
**Files Related** scheduler config, dashboards, operational tests.

### Checkpoint - Staging Ready

- [ ] Staging deploy/rollback được kiểm chứng.
- [ ] Backup restore drill thành công.
- [ ] Observability nối API–Agent–job.
- [ ] Scheduler multi-instance không chạy trùng.
- [ ] Production runbook được duyệt.

---

## Phase 14 - Release Readiness and Launch

### Step 14.1 - Prepare Production Seed and Provider Configuration

**Mô tả** Chuẩn bị destination data đã kiểm duyệt và cấu hình production provider trước khi phát hành.  
Quy trình seed hoặc import phải có provenance, validation và idempotency; provider key cùng scope không được ghi vào log.  
Production chỉ được dùng data và provider nằm trong danh sách cho phép.

**Acceptance Criteria**
- [ ] Seed/import có provenance, idempotency và validation.
- [ ] Provider keys/scopes được kiểm tra mà không ghi vào log.
- [ ] Production không dùng test data/provider ngoài danh sách cho phép.

**Verification** Dry-run import và provider connectivity smoke test.

**Dependencies** Steps 5.4, 7.1 và 13.3.
**Files Related** seed/import data, provider config, release scripts.

### Step 14.2 - Complete Requirement Traceability

**Mô tả** Lập traceability matrix nối business requirement và US01–US70 với implementation, endpoint, UI, test và tài liệu.  
Ba Agent cùng các global policy cần có trace riêng và mọi deferment phải được ghi rõ.  
Bước này cũng rà soát để loại bỏ mâu thuẫn còn lại giữa các tài liệu nguồn.

**Acceptance Criteria**
- [ ] Mỗi US/SYS có implementation/test reference hoặc documented deferment.
- [ ] Ba Agent và các global policies có trace riêng.
- [ ] Không còn yêu cầu mâu thuẫn giữa bốn tài liệu nguồn.

**Verification** Manual review ma trận với product và engineering.

**Dependencies** Phases 2–13.
**Files Related** docs/traceability/, test references, requirement docs.

### Step 14.3 - Execute User Acceptance Testing

**Mô tả** Thực hiện UAT bằng tiếng Việt với dữ liệu đại diện tại Việt Nam.  
Phạm vi bao gồm planning, customization, booking redirect, in-trip experience, review và trip summary.  
Blocking defect phải được sửa, có regression test và nhận stakeholder sign-off trước khi phát hành.

**Acceptance Criteria**
- [ ] Planning, customization, booking redirect, in-trip, review và summary journeys pass.
- [ ] User hiểu warning, source/confidence và accept/reject Agent proposal.
- [ ] Blocking defects được sửa và regression test trước sign-off.

**Verification** UAT report có evidence và stakeholder sign-off.

**Dependencies** Steps 14.1–14.2.
**Files Related** UAT scripts, issue tracker, regression tests.

### Step 14.4 - Finalize Documentation and Runbooks

**Mô tả** Hoàn thiện README, architecture, API docs và các runbook vận hành.  
Tài liệu cần bao phủ provider operation, incident, backup, scheduler và retention, đồng thời phản ánh đúng code cùng deployment cuối.  
Một người không tham gia triển khai phải có thể làm theo runbook để thực hiện dry-run thành công.

**Acceptance Criteria**
- [ ] Tài liệu phản ánh đúng code/deployment cuối.
- [ ] On-call có hướng dẫn xử lý provider outage, stuck job và cleanup failure.
- [ ] Không còn placeholder trong tài liệu release.

**Verification** Một người không tham gia triển khai thực hiện dry-run theo runbook.

**Dependencies** Phases 12–13.
**Files Related** README.md, docs/, OpenAPI, operational runbooks.

### Step 14.5 - Run Production Launch Checklist

**Mô tả** Thực hiện checklist cuối cho security, migration, monitoring, rollback, provider và data policy trước go-live.  
Mọi checkpoint trước đó phải pass hoặc có waiver được phê duyệt, đồng thời dashboard, alert, backup và incident ownership phải hoạt động.  
Sau deploy, nhóm chạy smoke test, core synthetic journey và theo dõi production trong khoảng thời gian đã thống nhất.

**Acceptance Criteria**
- [ ] Tất cả checkpoint trước đã pass hoặc có waiver được phê duyệt.
- [ ] Dashboard/alerts, backup, rollback và incident ownership hoạt động.
- [ ] Sau deploy, smoke test và core synthetic journey pass.

**Verification** Signed launch checklist, production smoke test và post-deploy monitoring window.

**Dependencies** Steps 14.1–14.4.
**Files Related** release checklist, deployment pipeline, monitoring.

### Final Checkpoint - Project Complete

- [ ] Business requirements và US01–US70 có traceability đầy đủ.
- [ ] Frontend, API Service, AI Orchestrator, ba Agent và Agent Harness hoạt động production.
- [ ] PostgreSQL/PostGIS và Object Storage được backup/monitor đúng policy.
- [ ] Weather Monitor, Trip Completion và Retention Cleanup ổn định.
- [ ] Security, privacy, 7-day retention và audit access được kiểm chứng.
- [ ] UAT và production launch checklist được phê duyệt.

---

## 8. Parallelization Strategy

Chỉ parallel sau khi contract liên quan đã được chốt:

- Sau Phase 1, frontend shell, database foundation và Agent Harness có thể tiến hành song song với coordination.
- Sau OpenAPI contract, frontend feature và backend vertical slice tương ứng có thể chia cho hai luồng.
- Provider adapter có thể làm song song nếu cùng tuân Tool/Provider contract.
- Reviews (Phase 9) có thể song song với phần cuối In-trip (Phase 8) sau khi auth/audit/media contracts ổn định.
- LLM eval, security tests và accessibility có thể bắt đầu sớm theo từng feature thay vì chờ Phase 12.
- Migration, shared schema, Agent contracts, scheduler lock và generated client phải có một owner tại một thời điểm.

## 9. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Chưa chọn travel/maps/weather/booking/vision/TTS providers | High | Xây provider ports và fake adapters trước; spike từng provider trước vertical slice liên quan |
| Dữ liệu giá/giờ mở cửa lỗi thời | High | Bắt buộc source, checked_at, confidence và freshness rule |
| LLM tạo plan không khả thi | High | Mandatory Critic gate, deterministic validators và eval fixtures |
| Agent tự vượt quyền hoặc gọi tool nguy hiểm | High | Tool allow-list, guardrails, no payment/booking action và adversarial tests |
| Scheduler chạy trùng trên nhiều worker | High | PostgreSQL coordination lock, idempotency key và unique constraints |
| Dữ liệu nhạy cảm tồn tại quá 7 ngày | High | expires_at từ lúc ghi, read filtering và daily cleanup with metrics |
| Cleanup xóa nhầm confirmed records | High | Phân loại temporary/confirmed rõ ràng, transaction, dry-run test và invariant |
| GPS bị dùng khi chưa đồng ý | High | Consent check tại ingestion, query và tool boundary |
| Provider outage làm hỏng toàn flow | Medium | Timeout, bounded retry, partial result và user-facing degradation |
| Token/cost tăng không kiểm soát | Medium | Context budget, model gateway metrics, rate limit và eval |
| Scope 70 user stories quá lớn | High | Thực hiện theo vertical slice, checkpoint từng Phase và release theo milestone nội bộ |
| Tài liệu lệch code | Medium | Traceability matrix và cập nhật docs trong Definition of Done |

## 10. Open Decisions Before Relevant Phases

Các quyết định này không chặn Phase 1 nhưng phải được chốt trước Step tương ứng:

- Nhà cung cấp LLM và model policy — trước Step 3.2.
- Travel catalog source và quy trình kiểm duyệt — trước Step 5.4.
- Maps/routing/weather providers và freshness thresholds — trước Steps 5.6 và 8.6.
- Vision và TTS providers — trước Steps 5.7, 8.3 và 8.4.
- Booking partners/sandbox và passenger fields tối thiểu — trước Phase 7.
- Notification channel đầu tiên — trước Step 10.1.
- Cadence của Weather Monitor và Trip Completion — trước Steps 8.6 và 10.1.
- Production hosting, observability stack và backup service — trước Phase 13.
- Currency/timezone normalization policy — trước Step 2.2.

## 11. Plan Approval

Trước khi bắt đầu triển khai:

- [ ] Product owner xác nhận scope và thứ tự Phase.
- [ ] Technical owner xác nhận repository structure và architecture boundaries.
- [ ] Security/privacy owner xác nhận retention 7 ngày và log access policy.
- [ ] Nhóm xác nhận provider decisions cần cho ba Phase đầu.
- [ ] Phase 1 được tạo thành các issue nhỏ theo từng Step trong tài liệu này.
