# Ý Tưởng Giao Diện: Phase 1 — Khởi Đầu & Cá Nhân Hóa

Nhóm màn hình này tập trung vào trải nghiệm chào đón người dùng, giúp đăng nhập nhanh chóng, làm quen với giao diện chính và thiết lập phong cách du lịch cá nhân (`SCR-01` đến `SCR-03`).

---

## 1. Màn Hình SCR-01: Đăng Nhập & Đăng Ký (Authentication)

### 1.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Thiết kế tối giản, thân thiện, tạo cảm giác an tâm và hứng khởi bắt đầu chuyến hành trình.
- **Mục tiêu:** Giúp người dùng đăng nhập hoặc tạo tài khoản mới nhanh chóng, có thông báo nhắc nhở nhẹ nhàng về việc bảo mật thông tin cá nhân.

### 1.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
|  [Logo Tour Guide Agent]                                       [Tiếng Việt v]     |
|                                                                                   |
|                      +-------------------------------------+                      |
|                      |             ĐĂNG NHẬP               |                      |
|                      |  Chào mừng bạn trở lại với trợ lý   |                      |
|                      |  du lịch thông minh                 |                      |
|                      |                                     |                      |
|                      |  Email / Tên đăng nhập:             |                      |
|                      |  [ Nhập email của bạn...          ] |                      |
|                      |                                     |                      |
|                      |  Mật khẩu:                          |                      |
|                      |  [ Nhập mật khẩu...          (eye)] |                      |
|                      |                                     |                      |
|                      |  [x] Ghi nhớ đăng nhập   Quên MK?   |                      |
|                      |                                     |                      |
|                      |  +-------------------------------+  |                      |
|                      |  |       ĐĂNG NHẬP NGAY          |  |                      |
|                      |  +-------------------------------+  |                      |
|                      |                                     |                      |
|                      |  Chưa có tài khoản? [Đăng ký ngay]  |                      |
|                      +-------------------------------------+                      |
|                                                                                   |
|  (i) Dữ liệu cá nhân của bạn luôn được bảo mật và tự động dọn dẹp định kỳ         |
+-----------------------------------------------------------------------------------+
```

### 1.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `users`**:
  - Ô nhập Email $\rightarrow$ `users.email`
  - Ô nhập Mật khẩu $\rightarrow$ `users.password` (được băm bảo mật)
  - Họ và tên khi đăng ký $\rightarrow$ `users.full_name`
  - Trạng thái tài khoản $\rightarrow$ `users.status` (`ACTIVE`, `BANNED`, `DISABLED`)
  - Vai trò người dùng $\rightarrow$ `users.role` (`USER`, `OPERATOR`, `ADMIN`)

### 1.4. Luồng Hoạt Động & Trạng Thái Giao Diện
- **Chuyển đổi Đăng nhập / Đăng ký**: Người dùng bấm *[Đăng ký ngay]* thì form trượt mượt mà sang giao diện tạo tài khoản (thêm ô nhập lại mật khẩu và họ tên).
- **Trạng thái đang xử lý**: Khi bấm nút, nút hiển thị vòng xoay chờ nhẹ và tạm khóa ô nhập để tránh bấm liên tục.
- **Báo lỗi thân thiện**: Nếu tài khoản ở trạng thái `BANNED`, hiện thông báo: *"Tài khoản bị tạm khóa, vui lòng liên hệ Admin"*.

---

## 2. Màn Hình SCR-02: Khung Giao Diện Chính & Lịch Sử Chuyến Đi (App Shell & History)

### 2.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Đóng vai trò là "ngôi nhà chung" của ứng dụng, nơi người dùng dễ dàng chuyển qua lại giữa việc khám phá địa điểm, lập kế hoạch mới và theo dõi các chuyến đi đang diễn ra.
- **Mục tiêu:** Bố cục thanh điều hướng rõ ràng, đồng thời hiển thị danh sách các chuyến đi gần đây ở thanh bên (Sidebar) để người dùng quay lại bất cứ lúc nào.

### 2.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| [Logo Agent] | [Khám phá] [Lập kế hoạch] [Chuyến đi] [Lịch sử]  | [Chuông (2)] [Avatar]|
+--------------+---------------------------------------------------+----------------+
| (Thanh bên: Lịch sử chuyến đi) | (Khu vực nội dung chính của màn hình)             |
|                                |                                                  |
| [+ BẮT ĐẦU CHUYẾN ĐI MỚI]      |                                                  |
|                                |                                                  |
| Chuyến đi của bạn:             |                                                  |
| > Đà Lạt 3N2Đ                  |                                                  |
|   [Đang diễn ra - Live GPS]    |                                                  |
| > Đà Nẵng - Hội An             |                                                  |
|   [Kế hoạch đã chốt]           |                                                  |
| > Hà Giang mùa lúa chín        |                                                  |
|   [Bản nháp yêu cầu]           |                                                  |
|                                |                                                  |
| [Xem tất cả lịch sử >>]        |                                                  |
|                                |                                                  |
| ------------------------------ |                                                  |
| Trạng thái: Người dùng         |                                                  |
+--------------------------------+--------------------------------------------------+
```

### 2.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `agent_session`**:
  - Danh sách phiên chat $\rightarrow$ `agent_session.title`, `agent_session.summary`
  - Trạng thái phiên $\rightarrow$ `agent_session.status` (`ACTIVE`, `ARCHIVED`)
- **Bảng `trips` & `trip_requests`**:
  - Nhãn trạng thái chuyến đi $\rightarrow$ `trips.status` (Đang diễn ra) hoặc `trip_requests.status` (`DRAFT`, `CONFIRMED`)
- **Phân quyền Menu** $\rightarrow$ Dựa trên `users.role` (`USER`, `OPERATOR`, `ADMIN`)

---

## 3. Màn Hình SCR-03: Hồ Sơ Du Lịch Cá Nhân (Travel Profile & Preferences)

### 3.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Giúp AI hiểu rõ “gu” du lịch của từng người (thích nghỉ dưỡng hay khám phá, đi cùng ai, ăn uống thế nào, ngân sách bao nhiêu).
- **Mục tiêu:** Cung cấp giao diện trắc nghiệm trực quan, dễ chọn lựa với các thẻ hình ảnh/icon sinh động thay vì các biểu mẫu khô khan.

### 3.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| HỒ SƠ DU LỊCH CÁ NHÂN                                                             |
| Tùy chỉnh phong cách để AI đề xuất các chuyến đi phù hợp nhất với bạn              |
|                                                                                   |
| [1. Phong cách du lịch yêu thích]                                                 |
| [X] Nghỉ dưỡng & Thư giãn      [X] Khám phá thiên nhiên      [ ] Check-in sống ảo |
| [X] Trải nghiệm ẩm thực địa phương                         [ ] Khám phá di tích   |
|                                                                                   |
| [2. Nhu cầu & Lưu ý đặc biệt]                                                     |
| [x] Thường đi cùng trẻ nhỏ (< 6 tuổi)        [ ] Hạn chế đi bộ dốc cao            |
| [ ] Ăn chay / Dị ứng thực phẩm               [x] Ưu tiên nơi yên tĩnh             |
| Ghi chú riêng: [ Thích các quán cà phê có không gian ngắm hoàng hôn             ] |
|                                                                                   |
| [3. Mức ngân sách & Nhịp độ chuyến đi ưa thích]                                   |
| Mức chi tiêu trung bình / ngày: [ 1.500.000 VNĐ       v]                          |
| Nhịp độ chuyến đi:              ( ) Thong thả   (x) Vừa phải   ( ) Dày đặc        |
|                                                                                   |
| [4. Sở thích được AI tích lũy tự động qua các chuyến đi trước]                    |
| * Sau chuyến Đà Lạt: Ghi nhận sở thích đi cà phê chiều hoàng hôn   [Xóa]          |
| * Sau chuyến Nha Trang: Ghi nhận thói quen chọn khách sạn ven biển [Xóa]          |
|                                                                                   |
| +-------------------------------+    +----------------------------------+         |
| |       LƯU HỒ SƠ CỦA TÔI       |    | HỦY BỎ THAY ĐỔI                  |         |
| +-------------------------------+    +----------------------------------+         |
+-----------------------------------------------------------------------------------+
```

### 3.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `user_profile`**:
  - Thẻ phong cách du lịch $\rightarrow$ `user_profile.travel_preferences` (JSONB)
  - Nhu cầu đặc biệt & Ghi chú $\rightarrow$ `user_profile.special_needs` (TEXT)
  - Mức chi tiêu trung bình $\rightarrow$ `user_profile.default_budget` (NUMERIC)
  - Đơn vị tiền tệ $\rightarrow$ `user_profile.preferred_currency` (VARCHAR(3), mặc định `VND`)
- **Bảng `agent_memories`**:
  - Sở thích tích lũy $\rightarrow$ Trích xuất từ working memory sau khi người dùng xác nhận tổng kết chuyến đi.
