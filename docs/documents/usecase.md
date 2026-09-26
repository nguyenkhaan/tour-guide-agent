# Sơ đồ use case — Tour Guide Agent

Tài liệu mô tả các chức năng của hệ thống hỗ trợ khách du lịch tự túc tại Việt Nam, từ chuẩn bị đến tổng kết chuyến đi. Một tài khoản có thể lập kế hoạch cho nhiều người; không bao gồm cộng tác nhiều tài khoản, quản trị đoàn hoặc điều hành tour.

**Tài liệu tham chiếu:** [Yêu cầu nghiệp vụ](../business-requirement.md) và [User story](user-story.md).

**Cách đọc sơ đồ:** Mermaid được biểu diễn bằng `flowchart` với các nút bo tròn mô phỏng use case; khung bao quanh là phạm vi hệ thống. Nút bên ngoài là tác nhân; đường liền thể hiện tác nhân tham gia chức năng, không biểu diễn thứ tự thao tác. Mũi tên `«include»` đi từ chức năng chính đến chức năng bắt buộc dùng chung; `«extend»` đi từ chức năng bổ sung đến chức năng chính, chỉ xảy ra khi điều kiện ghi trên đường nối được đáp ứng. Planner, Critic/Evaluator và Booking & Logistics là thành phần nội bộ, không phải tác nhân bên ngoài.

## 1. Tài khoản và hồ sơ du lịch

**Mô tả:** Người dùng quản lý tài khoản, sở thích, nhu cầu đặc biệt và ngân sách thường dùng, đồng thời xem lại hội thoại và chuyến đi. Hồ sơ và dữ liệu chuyến đi đã xác nhận được dùng để cá nhân hóa đề xuất.

**Đối chiếu:** Mục “Tài khoản và cá nhân hóa” trong yêu cầu nghiệp vụ; US02, US62, US64. Đăng ký và đăng nhập được quản lý trực tiếp từ yêu cầu nghiệp vụ, không tách thành user story riêng trong phạm vi hiện tại.

```mermaid
flowchart LR
    U["Người dùng"]
    subgraph S["Tour Guide Agent — Tài khoản và hồ sơ"]
        A([Đăng ký tài khoản])
        B([Đăng nhập])
        C([Quản lý tài khoản cá nhân])
        D([Cập nhật hồ sơ du lịch])
        E([Xem lịch sử hội thoại, kế hoạch,<br/>chuyến đi và tổng kết])
    end
    U --- A
    U --- B
    U --- C
    U --- D
    U --- E
```

## 2. Tiếp nhận và xác nhận yêu cầu chuyến đi

**Mô tả:** Người dùng mô tả chuyến đi bằng hội thoại, bổ sung thông tin người đi cùng và ngữ cảnh từ GPS hoặc media. Hệ thống hỏi lại thông tin thiếu hoặc chưa rõ; ngày đi, nơi xuất phát và ngân sách phải đầy đủ trước khi lập kế hoạch từ bản tóm tắt đã xác nhận.

**Đối chiếu:** US01–US08.

```mermaid
flowchart LR
    U["Người dùng"]
    subgraph S["Tour Guide Agent — Yêu cầu chuyến đi"]
        A([Mô tả yêu cầu qua hội thoại])
        B([Phân tích yêu cầu, hồ sơ<br/>và thông tin người đi cùng])
        C([Xem bản tóm tắt yêu cầu])
        D([Bổ sung hoặc chỉnh sửa yêu cầu])
        E([Xác nhận bản tóm tắt])
        F([Hỏi và trả lời thông tin bổ sung])
        G([Chia sẻ GPS, ảnh hoặc media<br/>và làm rõ mục đích sử dụng])
    end
    U --- A
    U --- C
    U --- D
    U --- E
    U --- F
    U --- G
    A -.->|«include»| B
    F -.->|«extend»: thông tin thiếu hoặc chưa rõ| A
    G -.->|«extend»: cần bổ sung ngữ cảnh| A
    D -.->|«extend»: cần sửa bản tóm tắt| C
```

## 3. Tìm kiếm và lựa chọn địa điểm du lịch

**Mô tả:** Hệ thống gợi ý địa điểm tại Việt Nam theo nhu cầu chuyến đi, hỗ trợ tìm theo bán kính hoặc ảnh tương đồng. Người dùng xem xếp hạng, lý do đề xuất và thông tin kiểm chứng, rồi chọn hoặc bỏ chọn địa điểm để cập nhật yêu cầu.

**Đối chiếu:** US09–US15, US51.

```mermaid
flowchart LR
    U["Người dùng"]
    D["Nguồn dữ liệu du lịch bên thứ ba"]
    subgraph S["Tour Guide Agent — Khám phá địa điểm"]
        A([Tìm và nhận gợi ý địa điểm])
        B([Tìm trong bán kính<br/>quanh GPS hoặc vị trí cung cấp])
        C([Tìm cảnh quan tương đồng với ảnh])
        E([Xem xếp hạng, đánh giá hợp lệ<br/>và lý do đề xuất])
        F([Xem nguồn, thời điểm kiểm tra<br/>và mức độ tin cậy])
        G([Chọn, bỏ chọn hoặc đổi địa điểm])
        H([Cập nhật bản tóm tắt yêu cầu])
    end
    U --- A
    U --- B
    U --- C
    U --- E
    U --- F
    U --- G
    D --- A
    B -.->|«extend»: có tâm tìm kiếm và bán kính| A
    C -.->|«extend»: có ảnh tham chiếu| A
    A -.->|«include»| E
    E -.->|«include»: thông tin biến động| F
    G -.->|«include»| H
```

## 4. Lập lịch trình và so sánh phương án

**Mô tả:** Từ yêu cầu đã xác nhận, hệ thống tạo 1–4 lộ trình gồm lịch từng ngày, nơi lưu trú, hoạt động, phương tiện, dự trù chi phí và hành lý. Mọi lộ trình phải được kiểm tra ngân sách, giờ mở cửa, thời gian di chuyển và an toàn; phương án không khả thi bị chặn và điều chỉnh trước khi hiển thị.

**Đối chiếu:** US16–US22; thống nhất giới hạn từ 1 đến 4 lộ trình.

```mermaid
flowchart LR
    U["Người dùng"]
    D["Nguồn dữ liệu du lịch,<br/>bản đồ và thời tiết"]
    subgraph S["Tour Guide Agent — Lập lịch trình"]
        A([Yêu cầu lập lịch trình])
        B([Tạo 1–4 lộ trình theo từng ngày])
        C([Đề xuất phương tiện,<br/>dự trù chi phí và hành lý])
        E([Kiểm tra tính khả thi và an toàn])
        F([Điều chỉnh phương án không đạt])
        G([So sánh và chọn lộ trình khả thi])
        H([Xem thời lượng, chi phí, điểm nổi bật,<br/>lý do, cảnh báo và đánh đổi])
    end
    U --- A
    U --- G
    D --- C
    D --- E
    A -.->|«include»| B
    B -.->|«include»| C
    B -.->|«include»| E
    F -.->|«extend»: kiểm tra không đạt| E
    G -.->|«include»| H
```

## 5. Tùy chỉnh và lưu kế hoạch

**Mô tả:** Người dùng có thể chỉnh tay hoặc yêu cầu Agent sửa đúng phần được chỉ định, gồm địa điểm, nơi lưu trú, chặng di chuyển, hoạt động và vật dụng. Với thay đổi do Agent đề xuất, hệ thống hiển thị phần bị ảnh hưởng, lý do và cảnh báo nhưng chưa áp dụng ngay. Người dùng phải xác nhận chấp nhận hoặc từ chối; khi từ chối, kế hoạch hiện tại được giữ nguyên.

**Đối chiếu:** US23–US28.

```mermaid
flowchart LR
    U["Người dùng"]
    subgraph S["Tour Guide Agent — Tùy chỉnh kế hoạch"]
        A([Chỉnh tay: thêm, sửa hoặc xóa])
        B([Yêu cầu chỉnh sửa qua hội thoại])
        C([Xác định phạm vi được phép sửa])
        P([Tạo đề xuất chỉnh sửa<br/>chưa áp dụng])
        D([Tính lại lịch trình, chi phí, phương tiện,<br/>lưu trú, hành lý và hoạt động liên quan])
        E([Xem phần bị ảnh hưởng,<br/>lý do và cảnh báo phát sinh])
        F([Kiểm tra lại tính khả thi])
        G([Xác nhận chấp nhận<br/>hoặc từ chối đề xuất])
        I([Giữ nguyên kế hoạch hiện tại])
        H([Xác nhận và lưu kế hoạch cuối])
    end
    U --- A
    U --- B
    U --- E
    U --- G
    U --- H
    B -.->|«include»| C
    C -.->|«include»| P
    P -.->|«include»| E
    G -.->|«include»: xem trước khi quyết định| E
    A -.->|«include»| D
    G -.->|chấp nhận| D
    G -.->|từ chối| I
    F -.->|«extend»: thay đổi quan trọng| D
```

## 6. Tìm dịch vụ và hướng dẫn đặt chỗ với đối tác

**Mô tả:** Hệ thống tìm và so sánh khách sạn, chuyến bay, phương tiện và dịch vụ qua API đối tác, chuẩn bị thông tin cần thiết và hiển thị giá cuối cùng cùng điều kiện hủy/đổi. Người dùng tự xác nhận và thanh toán trên trang đối tác; hệ thống không tự đặt chỗ, giữ tiền hoặc thanh toán thay.

**Đối chiếu:** US29–US34.

```mermaid
flowchart LR
    U["Người dùng"]
    P["Nhà cung cấp dịch vụ / API đối tác"]
    subgraph S["Tour Guide Agent — Dịch vụ và logistics"]
        A([Tìm dịch vụ theo lịch trình])
        B([So sánh giá, mức độ phù hợp,<br/>nhà cung cấp và điều kiện hủy/đổi])
        C([Chọn dịch vụ])
        D([Chuẩn bị thông tin hành khách<br/>và thông tin đăng ký cần thiết])
        E([Xem giá cuối, nhà cung cấp<br/>và điều kiện trước khi tiếp tục])
        F([Chuyển sang trang đối tác<br/>và xem hướng dẫn hoàn tất])
    end
    U --- A
    U --- B
    U --- C
    U --- E
    U --- F
    P --- A
    P --- E
    P --- F
    C -.->|«include»| D
    F -.->|«include»| E
```

Việc xác nhận giao dịch và thanh toán nằm ngoài phạm vi Tour Guide Agent, trên hệ thống của nhà cung cấp.

## 7. Khám phá và thuyết minh trong chuyến đi

**Mô tả:** Người dùng hỏi thông tin, gửi ảnh để nhận diện địa điểm và nhận gợi ý hoạt động; khi nhận diện chưa chắc chắn, hệ thống đưa ra các khả năng và hỏi lại. Gợi ý thuyết minh khi đến gần điểm trong lịch trình chỉ sử dụng GPS đã bật; âm thanh chỉ phát khi người dùng xác nhận hoặc chủ động yêu cầu.

**Đối chiếu:** US35–US41.

```mermaid
flowchart LR
    U["Người dùng"]
    D["Nguồn thông tin địa điểm bên thứ ba"]
    G["Dịch vụ GPS trên thiết bị"]
    subgraph S["Tour Guide Agent — Khám phá tại chỗ"]
        A([Hỏi lịch sử, văn hóa, giá vé,<br/>giờ mở cửa và điều kiện tham quan])
        B([Nhận diện địa điểm từ ảnh hoặc văn bản])
        C([Xem các khả năng và trả lời làm rõ])
        E([Nhận gợi ý hoạt động tại địa điểm])
        F([Bật hoặc tắt GPS theo từng chuyến đi])
        H([Nhận gợi ý thuyết minh khi đến gần<br/>điểm trong lịch trình])
        I([Nghe thuyết minh theo yêu cầu<br/>hoặc sau khi xác nhận thông báo])
        J([Xem nguồn, thời điểm kiểm tra<br/>và mức độ tin cậy])
    end
    U --- A
    U --- B
    U --- C
    U --- E
    U --- F
    U --- H
    U --- I
    D --- A
    G --- H
    C -.->|«extend»: độ tin cậy nhận diện thấp| B
    A -.->|«include»: thông tin biến động| J
```

## 8. Theo dõi và ứng phó thay đổi thời gian thực

**Mô tả:** Background Weather Monitor định kỳ quét các chuyến đi đang hoạt động, lấy thời tiết, thời gian di chuyển và giờ mở cửa mới nhất để phát hiện ảnh hưởng đến kế hoạch. Khi có thay đổi đáng kể, hệ thống cảnh báo, đánh dấu điểm không thể ghé và có thể yêu cầu Agent tạo phương án thay thế. Kế hoạch đã chốt chỉ được cập nhật sau khi người dùng xem và chấp thuận thay đổi.

**Đối chiếu:** US42–US45; áp dụng kiểm chứng và tính lại kế hoạch tại US26–US27.

```mermaid
flowchart LR
    U["Người dùng"]
    D["Dịch vụ thời tiết, bản đồ<br/>và thông tin giờ mở cửa"]
    W["Background Weather Monitor"]
    subgraph S["Tour Guide Agent — Cập nhật thời gian thực"]
        A([Theo dõi yếu tố ảnh hưởng lịch trình])
        B([Nhận cảnh báo và phương án thay thế])
        C([Đánh dấu điểm không thể thực hiện])
        E([Xem và chấp thuận thay đổi])
        F([Cập nhật kế hoạch đã chốt])
        G([Kiểm chứng và tính lại<br/>nội dung liên quan])
    end
    D --- A
    W --- A
    U --- B
    U --- E
    B -.->|«extend»: có sự cố ảnh hưởng| A
    C -.->|«extend»: đóng cửa hoặc rủi ro an toàn rõ ràng| A
    F -.->|«include»: bắt buộc có sự đồng ý| E
    F -.->|«include»| G
```

## 9. Đánh giá, quyền riêng tư và kiểm duyệt

**Mô tả:** Người dùng chấm điểm, viết nhận xét và quản lý trạng thái riêng tư/công khai của từng bài; bài mới mặc định riêng tư. Bài yêu cầu công khai phải được kiểm duyệt, chống spam và xác minh tính liên quan, chuyến đi hợp lệ trước khi hiển thị; chỉ bài công khai hợp lệ được dùng để xếp hạng.

**Đối chiếu:** US46–US51, US59–US60.

```mermaid
flowchart LR
    U["Người dùng"]
    subgraph S["Tour Guide Agent — Đánh giá và nhận xét"]
        A([Chấm điểm và viết nhận xét])
        B([Lưu bài ở chế độ riêng tư mặc định])
        C([Yêu cầu công khai từng bài])
        D([Kiểm duyệt, chống spam<br/>và xác minh tính hợp lệ])
        E([Chuyển bài về riêng tư])
        F([Báo cáo bài đánh giá vi phạm])
        G([Tiếp nhận và xử lý báo cáo])
        H([Tham khảo bài công khai hợp lệ])
    end
    U --- A
    U --- C
    U --- E
    U --- F
    U --- H
    A -.->|«include»| B
    C -.->|«include»: trước khi hiển thị công khai| D
    F -.->|«include»| G
```

## 10. Tổng kết hành trình và chi phí thực tế

**Mô tả:** Background Trip Completion job định kỳ quét các chuyến đi đã đến thời điểm kết thúc; tín hiệu kết thúc sớm cũng kích hoạt cùng luồng xử lý. Job có tính idempotent để chỉ tạo một bản nháp tổng kết cho mỗi lần kết thúc chuyến đi. Bản nháp phân loại điểm đã đi, bỏ qua và phát sinh từ dữ liệu tương tác, xác nhận và GPS nếu đã bật. Người dùng sửa lại hành trình, lưu cảm nhận và ảnh; nhập chi phí là tùy chọn, chỉ so sánh khi có số liệu thực tế.

**Đối chiếu:** US52–US59, US61. Việc công khai đánh giá địa điểm được mô tả ở mục 9.

```mermaid
flowchart LR
    U["Người dùng"]
    T["Background Trip Completion Job"]
    subgraph S["Tour Guide Agent — Tổng kết chuyến đi"]
        A([Kết thúc chuyến đi sớm])
        B([Tạo nháp tổng kết và thông báo])
        C([Phân loại điểm đã đi,<br/>bỏ qua và phát sinh])
        D([Xem và chỉnh sửa bản tổng kết])
        E([Nhập chi phí thực tế theo hạng mục])
        F([So sánh tổng chi phí, chênh lệch<br/>và tỷ lệ so với dự trù])
        G([Lưu điểm tổng thể, nhật ký,<br/>ảnh và đánh giá từng điểm])
        H([Hoàn thành tổng kết<br/>không nhập chi phí])
    end
    U --- A
    U --- D
    U --- E
    U --- G
    U --- H
    T --- B
    A -.->|«include»| B
    B -.->|«include»| C
    E -.->|«extend»: người dùng chọn nhập chi phí| D
    E -.->|«include»| F
    G -.->|«extend»: người dùng bổ sung trải nghiệm| D
```

Không suy diễn chi phí chưa nhập thành số tiền bằng không. Nhận xét cho từng địa điểm vẫn mặc định riêng tư.

## 11. Xác nhận tổng kết và gợi ý chuyến đi tiếp theo

**Mô tả:** Khi xác nhận tổng kết, người dùng chốt dữ liệu vào lịch sử và đồng ý dùng dữ liệu đó để cập nhật sở thích, thói quen chi tiêu và nhịp độ di chuyển. Hệ thống đưa ra 1–3 ý tưởng chuyến đi tiếp theo; người dùng có thể mở hội thoại lập kế hoạch mới từ thẻ gợi ý với sở thích điền sẵn.

**Đối chiếu:** US62–US64.

```mermaid
flowchart LR
    U["Người dùng"]
    subgraph S["Tour Guide Agent — Cá nhân hóa sau chuyến đi"]
        A([Xác nhận chốt bản tổng kết])
        B([Lưu dữ liệu đã xác nhận vào lịch sử])
        C([Cập nhật hồ sơ du lịch<br/>từ tổng kết đã xác nhận])
        D([Nhận 1–3 ý tưởng chuyến đi tiếp theo])
        E([Bắt đầu lập kế hoạch từ thẻ gợi ý])
        F([Mở hội thoại mới<br/>và điền sẵn sở thích tích lũy])
    end
    U --- A
    U --- D
    U --- E
    A -.->|«include»| B
    A -.->|«include»| C
    A -.->|«include»| D
    E -.->|«include»| F
```

## 12. Minh bạch thông tin và quyết định của Agent

**Mô tả:** Người dùng xem căn cứ của đề xuất hoặc thay đổi, nguồn dữ liệu, thời điểm kiểm tra, mức độ tin cậy, cảnh báo và đánh đổi. Hệ thống lưu nhật ký gồm đầu vào, phản hồi, nguồn, công cụ và kết quả, lỗi, phiên bản Agent cùng lý do tóm tắt có cấu trúc; không lưu hoặc hiển thị chuỗi suy luận thô.

**Đối chiếu:** US65–US67, SYS70; dùng chung cho khám phá, lập lịch trình và cập nhật kế hoạch.

```mermaid
flowchart LR
    U["Người dùng"]
    subgraph S["Tour Guide Agent — Minh bạch quyết định"]
        A([Xem giải thích đề xuất<br/>địa điểm, lộ trình hoặc thay đổi])
        B([Xem lý do quyết định dạng tóm tắt])
        C([Kiểm tra nguồn, thời điểm kiểm tra<br/>và mức độ tin cậy])
        D([Xem cảnh báo, thay đổi và đánh đổi])
    end
    U --- A
    U --- C
    U --- D
    A -.->|«include»| B
```

## 13. Tra cứu nhật ký kỹ thuật và truy vết lỗi

**Mô tả:** Nhân viên vận hành (Operator) hoặc Quản trị viên (Admin) được cấp quyền tra cứu nhật ký, lọc theo mã chuyến đi, Agent, mã lỗi hoặc thời gian; Admin có quyền xem dòng thực thi chi tiết và sự bàn giao giữa các Agent để truy vết lỗi. Trước khi mở chi tiết log của người dùng, bắt buộc phải khai báo cả mục đích truy cập và Ticket ID; mỗi lần truy cập được ghi nhận danh tính, thời gian, IP, mục đích và Ticket ID vào nhật ký an ninh.

**Đối chiếu:** US68–US70. Áp dụng yêu cầu khai báo cả mục đích và Ticket ID của US69; dữ liệu chỉ dùng để cung cấp, hỗ trợ và bảo vệ dịch vụ.

```mermaid
flowchart LR
    O["Nhân viên vận hành (Operator)"]
    AD["Quản trị viên (Admin)"]
    subgraph S["Tour Guide Agent — Nhật ký kỹ thuật"]
        A([Tra cứu và lọc nhật ký kỹ thuật])
        B([Mở chi tiết log của người dùng])
        C([Kiểm tra quyền truy cập])
        D([Khai báo mục đích và Ticket ID])
        F([Ghi nhận danh tính, thời gian, IP,<br/>mục đích và Ticket ID truy cập])
        G([Xem dòng thực thi, công cụ,<br/>kết quả và bàn giao giữa các Agent])
    end
    O --- A
    O --- B
    AD --- A
    AD --- B
    AD --- G
    A -.->|«include»| C
    B -.->|«include»| C
    B -.->|«include»| D
    B -.->|«include»| F
    G -.->|«include»| B
```

## 14. Hết hạn và dọn dẹp dữ liệu tạm thời

**Mô tả:** Dữ liệu GPS, tệp media gốc, working/trip memory của Agent và log kỹ thuật chi tiết được lưu tối đa 7 ngày. Một Retention Cleanup cron job chạy hằng ngày, dùng mốc hết hạn để đánh dấu dữ liệu không còn khả dụng rồi xóa bản ghi hoặc object quá hạn. Hồ sơ, kế hoạch, đánh giá, bản tổng kết và dữ liệu có cấu trúc đã được người dùng xác nhận không thuộc nhóm dữ liệu tạm thời này.

```mermaid
flowchart LR
    C["Retention Cleanup Cron<br/>chạy hằng ngày"]
    subgraph S["Tour Guide Agent — Vòng đời dữ liệu"]
        A([Tìm dữ liệu đã quá 7 ngày])
        B([Đánh dấu hết hạn<br/>và ngăn truy cập])
        D([Xóa hoặc ẩn danh dữ liệu<br/>trong PostgreSQL])
        E([Xóa media quá hạn<br/>trong Object Storage])
        F([Ghi kết quả cleanup])
    end
    C --> A
    A -.->|«include»| B
    B -.->|«include»| D
    B -.->|«include»| E
    D -.->|«include»| F
    E -.->|«include»| F
```

## 15. Quản trị kho dữ liệu và Phê duyệt kiến nghị (Maker – Checker)

**Mô tả:** Nhân viên vận hành (Operator) gửi các kiến nghị thay đổi (cập nhật thông tin địa điểm, báo cáo sự cố khẩn cấp hoặc phản ánh logic AI) lên hệ thống. Quản trị viên (Admin) là người có thẩm quyền duy nhất xem xét, phê duyệt hoặc từ chối kiến nghị; khi phê duyệt, dữ liệu tự động cập nhật vào kho địa điểm. Ngoài ra, Admin toàn quyền thêm mới, chỉnh sửa, xóa địa điểm, quản trị tài khoản người dùng và cấu hình tham số hệ thống.

**Đối chiếu:** US71–US75.

```mermaid
flowchart LR
    O["Nhân viên vận hành (Operator — Maker)"]
    AD["Quản trị viên (Admin — Checker)"]
    subgraph S["Tour Guide Agent — Quản trị & Maker-Checker"]
        A([Tạo và gửi kiến nghị thay đổi])
        B([Xem danh sách kiến nghị chờ duyệt])
        C([Phê duyệt hoặc từ chối kiến nghị])
        D([Tự động cập nhật kho địa điểm])
        E([Toàn quyền CRUD kho địa điểm du lịch])
        F([Quản trị tài khoản và phân quyền])
        G([Cấu hình tham số hệ thống])
    end
    O --- A
    AD --- B
    AD --- C
    AD --- E
    AD --- F
    AD --- G
    C -.->|«include»: khi phê duyệt| D
    C -.->|«include»| B
```
