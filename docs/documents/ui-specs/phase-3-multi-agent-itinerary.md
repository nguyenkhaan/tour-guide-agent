# Ý Tưởng Giao Diện: Phase 3 — Lập Lịch Trình Đa Tác Nhân & Quản Lý Kế Hoạch

Nhóm màn hình này là "trái tim" của trải nghiệm sản phẩm, nơi hệ thống AI đa tác nhân phối hợp để tạo ra 1–4 phương án lộ trình tối ưu; người dùng chọn lưu các phương án mình thích vào Danh Sách Lịch Trình, xem chi tiết, quản lý đánh dấu đặt chỗ, tích chọn hành lý cần mang, chỉnh sửa thủ công hoặc yêu cầu AI tinh chỉnh lại theo ý muốn (`SCR-08`, `SCR-09`, `SCR-09B`, `SCR-10`, `SCR-11`).

---

## 🧭 Luồng Hoạt Động Cốt Lõi Của Phase 3 (Core User Journey)

```text
+---------------------+     +--------------------------------+     +-------------------------------+
|  SCR-08: TIẾN TRÌNH | --> |  SCR-09: SO SÁNH CÁC PHƯƠNG ÁN | --> |  SCR-09B: DANH SÁCH LỊCH TRÌNH|
|  AI lập & thẩm định |     |  - Hiển thị 1-4 phương án      |     |  - Tự động chuyển hướng đến   |
|  kế hoạch an toàn   |     |  - Tick chọn các phương án ưng |     |  - Hiển thị các lịch trình đã |
+---------------------+     |  - Bấm [LƯU VÀO DANH SÁCH]     |     |    lưu trong tài khoản        |
                            +--------------------------------+     +---------------+---------------+
                                                                                   |
                                                                                   v (Người dùng bấm mở xem chi tiết)
                                                                   +-------------------------------+
                                                                   |  SCR-10: CẨM NANG HÀNH TRÌNH  |
                                                                   |  - Dòng thời gian từng ngày   |
                                                                   |  - Đánh dấu [x] Đã đặt vé/phòng|
                                                                   |  - Checklist [x] Soạn hành lý |
                                                                   |  - Nhờ AI sửa / Chốt kế hoạch |
                                                                   +-------------------------------+
```

---

## 1. Màn Hình SCR-08: Trực Quan Hóa Quá Trình AI Lập Kế Hoạch (AI Progress Stream)

### 1.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Biến thời gian chờ đợi thành trải nghiệm thú vị và minh bạch, cho người dùng thấy AI đang làm việc cần mẫn và có bước thẩm định an toàn độc lập trước khi đưa ra kết quả.
- **Mục tiêu:** Hiển thị từng nấc thang tiến độ (Đang lập phương án $\rightarrow$ Đang kiểm tra an toàn/ngân sách $\rightarrow$ Hoàn tất) mà không gây cảm giác màn hình bị đơ.

### 1.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
|               AI ĐANG THIẾT KẾ LỘ TRÌNH TỐI ƯU CHO GIA ĐÌNH BẠN                   |
|                   Thời gian ước tính: khoảng 10 - 15 giây                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [V] Bước 1: Nạp nhu cầu & thông tin gia đình                         (Đã xong)   |
|      -> Đà Lạt 3N2Đ, 2 người lớn + 1 bé 4 tuổi, ngân sách 8.000.000đ              |
|                                                                                   |
|  [V] Bước 2: AI Planner tạo các phương án lịch trình dự kiến          (Đã xong)   |
|      -> Đang sắp xếp các điểm tham quan theo cụm cung đường để tránh kẹt xe       |
|                                                                                   |
|  [*] Bước 3: AI Critic kiểm tra tính an toàn & khả thi thực tế        (Đang chạy) |
|      [========================>                  ] 70%                            |
|      -> Giờ mở cửa: Khớp 100% thời gian mở cửa các điểm                          |
|      -> Độ an toàn cho trẻ nhỏ: ĐÃ KIỂM TRA (Không có đoạn dốc trơn trượt)        |
|      -> Kiểm tra tổng chi phí: Nằm trong hạn mức (Dự trù 7.2tr / 8tr)             |
|                                                                                   |
|  [ ] Bước 4: Hoàn thiện các phương án so sánh & checklist hành lý     (Đang chờ)  |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | (Mẹo nhỏ): Trong lúc chờ, AI đang kiểm tra thêm dự báo thời tiết Đà Lạt tuần tới| |
| |            để gợi ý mang theo trang phục phù hợp cho bé.                        | |
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
|                                [ DỪNG LẠI / HỦY TÁC VỤ ]                          |
+-----------------------------------------------------------------------------------+
```

### 1.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `agent_runs`**:
  - Trạng thái tiến trình $\rightarrow$ `agent_runs.status` (`RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`)
  - Loại tác nhân $\rightarrow$ `agent_runs.agent_type` (`PLANNER`, `CRITIC`)
  - Tóm tắt quyết định $\rightarrow$ `agent_runs.decision_summary`
- **Bảng `evaluation_results`**:
  - Kết quả thẩm định $\rightarrow$ `budget_status`, `opening_hours_status`, `travel_time_status`, `safety_status`, `hard_failures`, `soft_warnings`

---

## 2. Màn Hình SCR-09: Bảng So Sánh Các Phương Án AI Đề Xuất (Itinerary Comparison Matrix)

### 2.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Sau khi AI tạo xong, người dùng được xem bảng so sánh tổng quan giữa các phương án (chi phí, điểm nổi bật, nhịp độ, đánh đổi).
- **Mục tiêu:** Người dùng tick chọn một hoặc nhiều phương án mình thích rồi nhấn **[LƯU VÀO DANH SÁCH LỊCH TRÌNH]**. Hệ thống sẽ lưu dữ liệu và **tự động chuyển hướng (navigate) sang trang Danh sách lịch trình (`SCR-09B`)**.

### 2.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| CÁC PHƯƠNG ÁN LỘ TRÌNH AI ĐỀ XUẤT CHO BẠN                       [Yêu cầu AI tạo lại]|
| Vui lòng tick chọn các phương án bạn thấy ưng ý để lưu vào Danh sách lịch trình:   |
+-----------------------------------------------------------------------------------+
| TIÊU CHÍ             | PHƯƠNG ÁN 1: NGHỈ DƯỠNG      | PHƯƠNG ÁN 2: TRẢI NGHIỆM     | PHƯƠNG ÁN 3: CHECK-IN NHẸ     |
+----------------------+------------------------------+------------------------------+-------------------------------+
| CHỌN LƯU PHƯƠNG ÁN   | [x] CHỌN LƯU PHƯƠNG ÁN NÀY   | [x] CHỌN LƯU PHƯƠNG ÁN NÀY   | [ ] CHỌN LƯU PHƯƠNG ÁN NÀY    |
| Phù hợp với          | [★ KHUYÊN DÙNG CÓ BÉ NHỎ]    | [DÀNH CHO NGƯỜI NĂNG ĐỘNG]   | [TIẾT KIỆM CHI PHÍ]           |
| Tổng chi phí dự kiến | 7.250.000 VNĐ (~90% budget)  | 7.850.000 VNĐ (~98% budget)  | 6.100.000 VNĐ (~76% budget)   |
| Nhịp độ di chuyển    | Thong thả (2 điểm/ngày)      | Năng động (4 điểm/ngày)      | Vừa phải (2-3 điểm/ngày)      |
| Điểm nổi bật         | Puppy Farm, Cà phê hoàng hôn | Trekking đồi chè, Thác nước  | Chợ đêm, Quảng trường Lâm Viên|
| Cảnh báo & Đánh đổi  | Bỏ qua điểm trekking dốc     | Di chuyển nhiều, bé dễ mệt   | Ít trải nghiệm thiên nhiên    |
+----------------------+------------------------------+------------------------------+-------------------------------+
|                                                                                                                   |
| [x] Chọn tất cả các phương án (3 phương án)                                                                      |
|                                                                                                                   |
| +---------------------------------------------------------------------------------------------------------------+ |
| |        [V] LƯU CÁC PHƯƠNG ÁN ĐÃ CHỌN VÀO DANH SÁCH LỊCH TRÌNH (2) -> Chuyển đến Danh Sách Lịch Trình          | |
| +---------------------------------------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 2.3. Luồng Hoạt Động & Tương Tác Trực Quan:
1. **Tick chọn phương án**: Người dùng tick chọn 1, 2 hoặc tất cả phương án.
2. **Lưu & Tự động điều hướng**: Khi bấm nút `[LƯU CÁC PHƯƠNG ÁN ĐÃ CHỌN]`:
   - Hệ thống lưu các phương án đã tick vào cơ sở dữ liệu (`itineraries`).
   - Giao diện **tự động chuyển hướng ngay sang Màn hình Danh sách lịch trình (`SCR-09B`)**.
   - Tại màn hình danh sách, các phương án vừa lưu sẽ hiển thị nổi bật ở đầu trang kèm nhãn: *"Vừa tạo mới"*.

### 2.4. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `itineraries`**:
  - Các phương án được tick chọn $\rightarrow$ Lưu vào bảng `itineraries` với trạng thái `status = ItineraryStatus.DRAFT` (kế hoạch đã lưu), gắn với `trip_request_id`.
  - Các trường chi tiết $\rightarrow$ `option_index`, `title`, `summary`, `total_days`, `estimated_total_cost`, `cost_breakdown` (JSONB), `highlights` (JSONB), `warnings` (JSONB), `trade_offs` (TEXT), `luggage_checklist` (JSONB).

---

## 3. Màn Hình SCR-09B: Danh Sách & Thư Viện Lịch Trình Của Tôi (My Itineraries Hub)

### 3.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Nơi người dùng quản lý toàn bộ các lịch trình đã lưu trong tài khoản. Người dùng không bị ép phải "sử dụng ngay", mà có thể thong thả xem danh sách, khi nào muốn xem chi tiết hoặc bắt đầu đi thì mới nhấn vào từng thẻ.
- **Mục tiêu:** Cung cấp trung tâm quản lý rõ ràng, phân loại theo trạng thái (Vừa tạo, Đã chốt, Bản nháp, Chuyến đi cũ).

### 3.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| DANH SÁCH LỊCH TRÌNH CỦA TÔI                              [ + TẠO LỊCH TRÌNH MỚI ]|
| Bạn có 4 lịch trình đã lưu. Nhấp vào từng lịch trình để xem chi tiết hoặc điều chỉnh|
+-----------------------------------------------------------------------------------+
| [ Lọc: Tất cả (4) ]     [ Vừa tạo mới (2) ]     [ Kế hoạch đã chốt (1) ]    [ Đã đi (1) ]|
+-----------------------------------------------------------------------------------+
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [Ảnh bìa] ĐÀ LẠT THƯ GIÃN CHO GIA ĐÌNH (3N2Đ)             [ * VỪA TẠO MỚI ]   | |
| | * Điểm đến: TP. Đà Lạt, Lâm Đồng  | Thời gian dự kiến: 15/10 - 17/10/2026       | |
| | * Dự trù kinh phí: ~7.250.000 VNĐ | Thành viên: 2 Người lớn + 1 Bé 4 tuổi       | |
| | * Điểm nổi bật: Nông trại Puppy Farm, Cà phê ngắm hoàng hôn, Khách sạn Colline  | |
| |                                                                               | |
| | [ MỞ XEM CHI TIẾT & CHỈNH SỬA >> ]                [ Xóa khỏi danh sách ]      | |
| +-------------------------------------------------------------------------------+ |
|                                                                                   |
| +-------------------------------------------------------------------------------+ |
| | [Ảnh bìa] ĐÀ LẠT TRẢI NGHIỆM NĂNG ĐỘNG (3N2Đ)           [ * VỪA TẠO MỚI ]   | |
| | * Điểm đến: TP. Đà Lạt | Dự trù kinh phí: ~7.850.000 VNĐ                        | |
| | * Điểm nổi bật: Trekking đồi chè Cầu Đất, Chợ đêm, Thác Datanla                 | |
| |                                                                               | |
| | [ MỞ XEM CHI TIẾT & CHỈNH SỬA >> ]                [ Xóa khỏi danh sách ]      | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 4. Màn Hình SCR-10: Cẩm Nang Kế Hoạch Chi Tiết & Chuẩn Bị Hành Trình (Itinerary Workspace & Packing Checklist)

### 4.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Đóng vai trò là **"Tờ cẩm nang quan trọng nhất của chuyến đi" (Single Source of Truth)**. Nơi tập hợp mọi thông tin cốt lõi:
  1. **Dòng thời gian & Đánh dấu dịch vụ đã đặt trước**: Cho phép du khách tick chọn `[x] Đã đặt vé/phòng` (kèm mã booking / ghi chú) để quản lý tiến độ đặt chỗ rõ ràng.
  2. **Checklist Hành lý & Đồ dùng cần mang (`luggage_checklist`)**: Danh sách do AI gợi ý theo thời tiết và đối tượng (như bé 4 tuổi), người dùng vừa xếp vali vừa tick `[x] Đã chuẩn bị` hoặc tự thêm đồ đạc riêng.
  3. **Chỉnh sửa linh hoạt**: Người dùng có thể tự sửa tay, thêm/bớt điểm hoặc bấm **[NHỜ AI ĐIỀU CHỈNH]**.
- **Mục tiêu:** Du khách kiểm soát 100% sự chuẩn bị trước khi xách vali lên đường.

### 4.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| < Quay lại Danh Sách Lịch Trình | ĐÀ LẠT THƯ GIÃN (3N2Đ - v1)   [NHỜ AI ĐIỀU CHỈNH]|
| Dự trù: 7.250.000đ | 2 Lớn 1 Bé | Tiến độ: [Đã đặt 2/3 Dịch vụ | Đã soạn 4/6 Đồ]  |
+-----------------------------------------------------------------------------------+
| [ TAB: NGÀY 1 (15/10) ]   [ TAB: NGÀY 2 (16/10) ]   [ TAB: NGÀY 3 (17/10) ]       |
| [ TAB: CHECKLIST HÀNH LÝ & ĐỒ DÙNG CẦN MANG (Đã soạn: 4/6 món) ]                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
| (NỘI DUNG 1: DÒNG THỜI GIAN NGÀY 1 & TRẠNG THÁI ĐẶT DỊCH VỤ)                      |
|                                                                                   |
| [08:00 - 11:30] DI CHUYỂN: Xe Limousine VIP Sài Gòn -> Đà Lạt                     |
|                 Chi phí: 1.200.000đ | [x] ĐÃ ĐẶT VÉ (Mã: VX-8812)     [Sửa] [Xóa] |
|                                                                                   |
| [12:00 - 13:30] NGHỈ NGƠI: Khách sạn Colline Đà Lạt (2 đêm)                       |
|                 Chi phí: 1.850.000đ | [x] ĐÃ ĐẶT PHÒNG (Agoda #992)   [Sửa] [Xóa] |
|                                                                                   |
| [14:30 - 17:00] THAM QUAN: Nông trại Cún Puppy Farm (Bé chơi với cún)             |
|                 Vé cổng: 300.000đ   | [ ] CHƯA MUA (Mua tại cổng)     [Sửa] [Xóa] |
|                                                                                   |
| [17:30 - 19:30] ĂN UỐNG & NGẮM CẢNH: Tiệm cà phê Hoàng Hôn                        |
|                 Dự kiến: 250.000đ   | [ ] Tự do ghé quán              [Sửa] [Xóa] |
|                                                                                   |
| [+ THÊM HOẠT ĐỘNG HOẶC ĐIỂM DỪNG MỚI VÀO NGÀY 1]                                  |
| --------------------------------------------------------------------------------- |
| (NỘI DUNG 2: TAB CHECKLIST HÀNH LÝ & ĐỒ DÙNG - itineraries.luggage_checklist)    |
|                                                                                   |
| [TRANG PHỤC THEO THỜI TIẾT ĐÀ LẠT 16-18°C]                                        |
| [x] Áo khoác ấm & mũ len cho bé 4 tuổi (Đà Lạt chiều tối se lạnh)                 |
| [x] Giày thể thao êm chân cho bố mẹ đi dạo                                        |
| [ ] Áo mưa tiện lợi hoặc ô che mưa nhẹ                                            |
|                                                                                   |
| [Y TẾ & ĐỒ DÙNG CHO BÉ]                                                           |
| [x] Thuốc chống say xe & hạ sốt cho bé                                            |
| [x] Bình giữ nhiệt đựng nước ấm                                                   |
| [ ] Khăn ướt & xịt chống muỗi                                                     |
|                                                                                   |
| [+ THÊM VẬT DỤNG RIÊNG VÀO CHECKLIST...]                                          |
+-----------------------------------------------------------------------------------+
```

### 4.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Checklist đồ dùng cần mang**:
  - Lưu trực tiếp trong trường **`itineraries.luggage_checklist`** (JSONB).
  - Cấu trúc dữ liệu lưu trữ:
    ```json
    [
      {"category": "clothing", "item": "Áo khoác ấm & mũ len cho bé", "is_checked": true},
      {"category": "medical", "item": "Thuốc chống say xe cho bé", "is_checked": true},
      {"category": "medical", "item": "Khăn ướt & xịt chống muỗi", "is_checked": false}
    ]
    ```
- **Đánh dấu dịch vụ đã đặt trước**:
  - Các mục lưu trú và di chuyển nằm trong bảng `itinerary_activities` và `itinerary_transits`.
  - Trạng thái `is_booked` và mã đặt chỗ được lưu trong mô tả `itinerary_activities.description` hoặc metadata hoạt động.
- **Bảng `itinerary_days` & `itinerary_activities`**: Quản lý dòng thời gian chi tiết từng ngày, giờ giấc và chi phí.

---

## 5. Màn Hình SCR-11: Bảng Xem Trước Đề Xuất Thay Đổi Của AI (AI Proposal Diff Viewer)

### 5.1. Ý Tưởng & Mục Tiêu Trải Nghiệm
- **Ý tưởng:** Khi người dùng đang ở `SCR-10` và yêu cầu AI sửa một phần lịch trình, AI sẽ mở bảng so sánh trước/sau để người dùng duyệt.
- **Mục tiêu:** Thể hiện trọn vẹn nguyên tắc *Human-in-the-loop*: Người dùng luôn là người ra quyết định cuối cùng.

### 5.2. Bố Cục & Phác Thảo Giao Diện (Wireframe)
```text
+-----------------------------------------------------------------------------------+
| ĐỀ XUẤT ĐIỀU CHỈNH TỪ AI PLANNER                                     [ Đóng (X) ] |
| Yêu cầu của bạn: "Đổi điểm ngắm hoàng hôn sang ngày 2 vì sợ ngày 1 đến trễ"       |
+-----------------------------------------------------------------------------------+
| LÝ DO ĐỀ XUẤT CỦA AI:                                                             |
| Đã dời 'Tiệm cà phê Hoàng Hôn' sang chiều Ngày 2; thay thế chiều Ngày 1 bằng hoạt  |
| động đi dạo nhẹ nhàng quanh Hồ Xuân Hương (cách KS 200m) để bé không bị mệt.     |
|                                                                                   |
| [BẢNG ĐỐI CHIẾU THAY ĐỔI (TRƯỚC VÀ SAU)]:                                         |
|                                                                                   |
|  CHIỀU NGÀY 1:                                                                    |
|  [-] BỎ: Tiệm cà phê Hoàng Hôn (Cách khách sạn 6.2 km)                            |
|  [+] MỚI: Dạo mát Hồ Xuân Hương & Thưởng thức bánh tráng nướng (Gần khách sạn)    |
|                                                                                   |
|  CHIỀU NGÀY 2:                                                                    |
|  [+] MỚI: Tiệm cà phê Hoàng Hôn (Thời tiết dự báo nắng đẹp, ngắm hoàng hôn lý tưởng)|
|                                                                                   |
|  ẢNH HƯỞNG ĐẾN TỔNG THỂ:                                                          |
|  - Tổng chi phí: 7.250.000đ -> 7.150.000đ (Tiết kiệm 100.000đ tiền xe taxi)       |
|  - Tính an toàn: [V] Đã kiểm tra giờ mở cửa và thời tiết phù hợp                  |
|                                                                                   |
| +-----------------------------------+     +-------------------------------------+ |
| |    [V] ĐỒNG Ý ÁP DỤNG THAY ĐỔI    |     |      [X] GIỮ NGUYÊN NHƯ CŨ          | |
| +-----------------------------------+     +-------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

### 5.3. Khớp Nối Dữ Liệu Với Database (Database Alignment)
- **Bảng `itinerary_proposals`**:
  - Phiên bản đề xuất $\rightarrow$ `itinerary_proposals.target_version`
  - Tác nhân đề xuất $\rightarrow$ `itinerary_proposals.proposed_by`
  - Chi tiết đối chiếu (Diff) $\rightarrow$ `itinerary_proposals.diff_payload` (JSONB)
  - Lý do thay đổi $\rightarrow$ `itinerary_proposals.rationale` (TEXT)
  - Cảnh báo phát sinh $\rightarrow$ `itinerary_proposals.warnings` (JSONB)
  - Trạng thái người dùng duyệt $\rightarrow$ `itinerary_proposals.status` (`pending` $\rightarrow$ `accepted` hoặc `rejected`), `user_decision_at`
