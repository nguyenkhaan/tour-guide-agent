# User Story

## Tiếp nhận yêu cầu chuyến đi (Thái)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US01 — Là một người dùng, tôi muốn lập yêu cầu chuyến đi bằng prompt ngôn ngữ tự nhiên trong khung chat. Ví dụ: “Tôi muốn đi Đà Lạt 3 ngày cùng gia đình, xuất phát từ TPHCM, ngân sách 8 tỷ”, để hệ thống hiểu mà không cần điền từng trường thông tin. | SYS01 — Là hệ thống, tôi cần phân tích prompt ngôn ngữ tự nhiên của người dùng để trích xuất thông tin như ngày đi, nơi xuất phát, điểm đến, thời lượng, ngân sách và sở thích. |
| US02 — Là người dùng, tôi muốn hệ thống kết hợp nội dung yêu cầu với hồ sơ du lịch của tôi, bao gồm sở thích, nhu cầu đặc biệt và ngân sách thường dùng, để tạo được bản tóm tắt yêu cầu phù hợp. | SYS02 — Là hệ thống, tôi cần kết hợp yêu cầu hiện tại với hồ sơ cá nhân và dữ liệu chuyến đi đã được xác nhận để tạo bản tóm tắt phù hợp với nhu cầu của người dùng. |
| US03 — Là người dùng, tôi muốn cung cấp thông tin người đi cùng qua hội thoại để yêu cầu chuyến đi phản ánh nhu cầu của cả nhóm. | SYS03 — Là hệ thống, tôi cần tiếp nhận và kết hợp thông tin người đi cùng vào bản tóm tắt yêu cầu để phản ánh nhu cầu của cả nhóm. |
| US04 — Là người dùng, tôi muốn trả lời các câu hỏi bổ sung ngay trong hội thoại, để hoàn thiện những thông tin còn thiếu trước khi lập kế hoạch. | SYS04 — Là hệ thống, tôi cần phát hiện thông tin còn thiếu hoặc chưa rõ và tự động đặt câu hỏi bổ sung trong hội thoại, đặc biệt với ngày đi, nơi xuất phát và ngân sách, để bảo đảm có đủ dữ liệu bắt buộc trước khi lập kế hoạch. |
| US05 — Là người dùng, tôi muốn chia sẻ vị trí GPS, ảnh và media, mô tả trong hội thoại, bổ sung context về khu vực, cảnh quan muốn khám phá. | SYS05 — Là hệ thống, tôi cần tiếp nhận vị trí GPS và xác định mục đích sử dụng vị trí trong yêu cầu, để dùng đúng làm nơi xuất phát hoặc tâm tìm kiếm địa điểm. |
| US06 — Là người dùng, tôi muốn chia sẻ ảnh và tệp đa phương tiện trong hội thoại để bổ sung ngữ cảnh cho yêu cầu chuyến đi. | SYS06 — Là hệ thống, tôi cần xử lý ảnh và tệp đa phương tiện thuộc định dạng được hỗ trợ, trích xuất các thông tin liên quan đến nhu cầu du lịch và hỏi lại khi nội dung chưa rõ, để bổ sung ngữ cảnh cho yêu cầu chuyến đi. |
| US07 — Là người dùng, tôi muốn xem bản tóm tắt yêu cầu gồm ngày đi, nơi xuất phát, ngân sách, sở thích và thông tin người đi cùng để kiểm tra hệ thống hiểu đúng ý tôi chưa. | SYS07 — Là hệ thống, tôi cần tạo và hiển thị bản tóm tắt yêu cầu để người dùng kiểm tra trước khi lập kế hoạch. |
| US08 — Là người dùng, tôi muốn bổ sung, chỉnh sửa và xác nhận bản tóm tắt yêu cầu trước khi lập kế hoạch. | SYS08 — Là hệ thống, tôi cần cập nhật bản tóm tắt khi người dùng bổ sung hoặc chỉnh sửa và sử dụng bản tóm tắt đã được xác nhận làm đầu vào lập kế hoạch. |

## Khám phá địa điểm du lịch (Thái)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US09 — Là người dùng, tôi muốn được gợi ý địa điểm dựa trên sở thích, vị trí, thời gian, ngân sách và thông tin người tham gia, để lựa chọn địa điểm phù hợp với chuyến đi. | SYS09 — Là hệ thống, tôi cần tìm và đề xuất địa điểm trong phạm vi dữ liệu du lịch Việt Nam dựa trên sở thích, vị trí, thời gian, ngân sách và thông tin người tham gia, để cung cấp các lựa chọn phù hợp với yêu cầu chuyến đi. |
| US10 — Là người dùng, tôi muốn tìm địa điểm trong một bán kính cụ thể quanh vị trí GPS hiện tại hoặc vị trí do tôi cung cấp để có thể khám phá khu vực mong muốn. | SYS10 — Là hệ thống, tôi cần xác định tâm tìm kiếm từ GPS hoặc vị trí người dùng cung cấp, tính khoảng cách và lọc địa điểm theo bán kính được yêu cầu, để trả về các kết quả nằm trong khu vực mong muốn. |
| US11 — Là người dùng, tôi muốn gửi ảnh và yêu cầu tìm địa điểm có cảnh quan hoặc đặc điểm tương tự. | SYS11 — Là hệ thống, tôi cần phân tích đặc điểm cảnh quan trong ảnh đầu vào và đối chiếu với dữ liệu địa điểm, để đề xuất những nơi có đặc điểm tương đồng và nêu rõ điểm tương đồng đó. |
| US12 — Là người dùng, tôi muốn xem danh sách địa điểm được xếp hạng kèm thông tin đánh giá và lý do đề xuất, để so sánh mức độ phù hợp của từng lựa chọn. | SYS12 — Là hệ thống, tôi cần xếp hạng địa điểm dựa trên mức độ phù hợp với yêu cầu và các đánh giá công khai đã được xác minh, để ưu tiên hiển thị những lựa chọn có cơ sở phù hợp nhất với người dùng. |
| US13 — Là người dùng, tôi muốn biết lý do từng địa điểm được đề xuất để hiểu và so sánh các lựa chọn. | SYS13 — Là hệ thống, tôi cần tạo lý do đề xuất ngắn gọn cho từng địa điểm, liên hệ với các tiêu chí cụ thể như ngân sách, khoảng cách, cảnh quan và nhu cầu người đi cùng, để người dùng hiểu và so sánh các lựa chọn. |
| US14 — Là người dùng, tôi muốn xem nguồn, thời điểm kiểm tra và mức độ tin cậy của các thông tin có thể thay đổi để có cơ sở đánh giá trước khi lựa chọn địa điểm. | SYS14 — Là hệ thống, tôi cần hiển thị nguồn, thời điểm kiểm tra và mức độ tin cậy cho các thông tin có thể thay đổi như giá vé và giờ mở cửa, để người dùng có cơ sở đánh giá trước khi lựa chọn địa điểm. |
| US15 — Là người dùng, tôi muốn chọn, bỏ chọn hoặc thay đổi các địa điểm quan tâm trong danh sách gợi ý, để đưa những lựa chọn mong muốn vào yêu cầu chuyến đi. | SYS15 — Là hệ thống, tôi cần cập nhật các địa điểm người dùng chọn hoặc bỏ chọn vào bản tóm tắt yêu cầu, để bước lập kế hoạch sử dụng đúng lựa chọn hiện tại của người dùng. |

## Lập lịch trình (Minh)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US16 — Là một người dùng, tôi muốn được gợi ý từ 1 đến 4 lộ trình phù hợp để có thể xem và so sánh các phương án hiện có. | SYS16 — Là hệ thống, tôi cần tạo từ 1 đến 4 lộ trình phù hợp để người dùng xem, so sánh và lựa chọn. |
| US17 — Là một người dùng, tôi muốn tự do lập lịch mọi lúc với địa điểm tham quan, nơi lưu trú, hoạt động, chặng di chuyển và thời gian dự kiến, để tôi tự do điều chỉnh lịch trình nếu kế hoạch có thay đổi. | SYS17 — Là hệ thống, tôi cần lập lịch theo từng ngày với điểm tham quan, nơi lưu trú, hoạt động, chặng di chuyển và thời gian dự kiến. |
| US18 — Là một người dùng, tôi muốn được đề xuất phương tiện và cách thức di chuyển cho từng chặng, để tôi di chuyển thoải mái và tiện lợi nhất. | SYS18 — Là hệ thống, tôi cần đề xuất phương tiện phù hợp cho từng chặng di chuyển dựa trên lịch trình và nhu cầu của người dùng. |
| US19 — Là một người dùng, tôi muốn được cung cấp danh sách các hành lý hoặc vật dụng cần thiết cho chuyến du lịch, các vật dụng này phải phù hợp với các điều kiện thực tế như thời tiết, thời gian hoạt động và số lượng người tham gia, để tôi chủ động chuẩn bị cho chuyến du lịch. | SYS19 — Là hệ thống, tôi cần tạo danh sách hành lý và vật dụng dựa trên thời tiết, hoạt động, thời lượng và người tham gia. |
| US20 — Là một người dùng, tôi muốn có bảng dự trù kinh phí với kế hoạch chi tiêu chi tiết từng phần và cả tổng chi phí, kèm các điểm nổi bật, cảnh báo cho từng chặng trong lộ trình, để tôi dễ dàng hơn trong việc lựa chọn lộ trình. | SYS20 — Là hệ thống, tôi cần dự trù tổng chi phí và các nhóm chi phí chính, đồng thời hiển thị thời lượng, điểm nổi bật, cảnh báo và đánh đổi của từng lộ trình để người dùng dễ lựa chọn. |
| US21 — Là một người dùng, tôi muốn bản kế hoạch lộ trình được giải thích bằng ngôn ngữ tự nhiên, để tôi dễ hiểu, theo dõi và điều chỉnh. | SYS21 — Là hệ thống, tôi cần giải thích lý do xếp hạng và đề xuất lộ trình bằng ngôn ngữ dễ hiểu. |
| US22 — Là người dùng, tôi muốn chỉ nhận các lộ trình khả thi và được cảnh báo về những rủi ro cần cân nhắc trước khi lựa chọn. | SYS22 — Là hệ thống, tôi cần kiểm tra ngân sách, giờ mở cửa, thời gian di chuyển và rủi ro an toàn trước khi hiển thị lộ trình; chặn lộ trình không khả thi và trả lại cho Planner Agent để điều chỉnh. |

## Tùy chỉnh lại kế hoạch (Minh)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US23 — Là một người dùng, tôi muốn tự tay điều chỉnh một phần nào đó trong lịch trình, thêm, xóa, sửa các địa điểm hoặc hoạt động. | SYS23 — Là hệ thống, tôi cần cho phép người dùng chỉnh tay bằng thao tác thêm, sửa hoặc xóa từng điểm tham quan, nơi lưu trú, chặng di chuyển, hoạt động và vật dụng. |
| US24 — Là một người dùng, tôi muốn yêu cầu Agent thêm, xóa, thay thế hoặc sắp xếp lại từng phần của kế hoạch bằng hội thoại để điều chỉnh kế hoạch theo nhu cầu. | SYS24 — Là hệ thống, tôi cần nhận biết yêu cầu chỉnh sửa của người dùng ở phạm vi nào và phạm vi nào không được chỉnh sửa, để không tự ý thay đổi phần trong kế hoạch không được người dùng yêu cầu. |
| US25 — Là người dùng, tôi muốn xem phần bị ảnh hưởng, lý do và cảnh báo của đề xuất chỉnh sửa do Agent tạo ra, sau đó xác nhận chấp nhận hoặc từ chối đề xuất. | SYS25 — Là hệ thống, tôi cần trình bày đề xuất chỉnh sửa của Agent và chỉ áp dụng thay đổi sau khi người dùng xác nhận chấp nhận; nếu người dùng từ chối thì giữ nguyên kế hoạch hiện tại. |
| US26 — Là người dùng, tôi muốn kế hoạch được kiểm tra lại sau các thay đổi quan trọng để bảo đảm lịch trình vẫn khả thi. | SYS26 — Là hệ thống, tôi cần kiểm tra lại tính khả thi sau các thay đổi quan trọng và yêu cầu Agent liên quan xử lý lại khi kết quả không đạt điều kiện kiểm chứng. |
| US27 — Là người dùng, tôi muốn các nội dung liên quan được tính lại sau khi chỉnh sửa để kế hoạch luôn nhất quán. | SYS27 — Là hệ thống, tôi cần tính lại lịch trình, chi phí, phương tiện, nơi lưu trú, hành lý và hoạt động sau khi kế hoạch thay đổi. |
| US28 — Là một người dùng, tôi muốn lưu lại kế hoạch cuối, để dễ dàng theo dõi thông qua thiết bị di động suốt chuyến đi mà không cần tạo lại lịch trình. | SYS28 — Là hệ thống, tôi cần cho phép người dùng xác nhận và lưu kế hoạch cuối để sử dụng trong chuyến đi. |

## Đặt dịch vụ và logistics (Khánh)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US29 — Là một người dùng, tôi muốn được tìm khách sạn, chuyến bay, phương tiện và dịch vụ liên quan đến lịch trình để tham khảo các lựa chọn phù hợp. | SYS29 — Là hệ thống, tôi cần tìm được khách sạn, chuyến bay, phương tiện và dịch vụ liên quan đến lịch trình qua API đối tác. |
| US30 — Là một người dùng, tôi muốn được tìm và so sánh khách sạn, chuyến bay, phương tiện từ nhiều hãng, để tự quyết định và tự đặt chỗ dựa trên gợi ý từ hệ thống về chi phí và sở thích cá nhân. | SYS30 — Là hệ thống, tôi cần so sánh các lựa chọn theo giá, độ phù hợp, nhà cung cấp và điều kiện hủy hoặc đổi. |
| US31 — Là người dùng, tôi muốn thông tin hành khách và thông tin đăng ký cần thiết được chuẩn bị cho dịch vụ đã chọn để thuận tiện hoàn tất việc đặt dịch vụ. | SYS31 — Là hệ thống, tôi cần chuẩn bị thông tin hành khách và thông tin đăng ký cần thiết cho dịch vụ được chọn. |
| US32 — Là người dùng, tôi muốn xem giá cuối, nhà cung cấp và điều kiện hủy hoặc đổi rõ ràng trước khi tiếp tục. | SYS32 — Là hệ thống, tôi cần hiển thị giá cuối, nhà cung cấp và điều kiện hủy hoặc đổi rõ ràng trước khi chuyển hướng. |
| US33 — Là người dùng, tôi muốn tự xác nhận và thanh toán trực tiếp với nhà cung cấp dịch vụ để chủ động kiểm soát giao dịch. | SYS33 — Là hệ thống, tôi không tự đặt, giữ tiền hoặc thanh toán thay người dùng. |
| US34 — Là người dùng, tôi muốn được chuyển đến trang của đối tác kèm hướng dẫn để hoàn tất đăng ký hoặc thanh toán. | SYS34 — Là hệ thống, tôi cần chuyển người dùng sang trang đối tác kèm hướng dẫn hoàn tất đăng ký hoặc thanh toán. |

## Theo dõi thời gian thực trong chuyến đi

### Khám phá địa điểm du lịch (Khánh)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US35 — Là người dùng, tôi muốn được gợi ý các hoạt động nên làm tại địa điểm để biết những trải nghiệm đáng chú ý. | SYS35 — Là hệ thống, tôi cần gợi ý hoạt động nên làm tại địa điểm như tham quan điểm nổi bật hoặc mua quà lưu niệm. |
| US36 — Là người dùng, tôi muốn hỏi thông tin về lịch sử, văn hóa, giá vé, giờ mở cửa và điều kiện tham quan để hiểu rõ địa điểm trong hoặc ngoài lịch trình. | SYS36 — Là hệ thống, tôi cần trả lời được câu hỏi về lịch sử, văn hóa, giá vé, giờ mở cửa và điều kiện tham quan. |
| US37 — Là một người dùng, tôi muốn hỏi thông tin hoặc gửi ảnh để nhận diện địa điểm và nghe thuyết minh về lịch sử, văn hóa để hiểu nơi mình đang ở mà không cần tra cứu thủ công. | SYS37 — Là hệ thống, tôi cần nhận diện địa điểm từ ảnh hoặc văn bản; nếu độ tin cậy thấp thì đưa ra nhiều khả năng và hỏi lại người dùng. |
| US38 — Là người dùng, tôi muốn nhận gợi ý thuyết minh khi đến gần một điểm trong lịch trình để chủ động khám phá địa điểm đó. | SYS38 — Là hệ thống, tôi cần gợi ý nội dung thuyết minh khi người dùng đến gần điểm trong lịch trình. |
| US39 — Là người dùng, tôi muốn nghe thuyết minh bằng âm thanh khi tôi xác nhận thông báo hoặc chủ động yêu cầu. | SYS39 — Là hệ thống, tôi cần phát thuyết minh bằng âm thanh khi người dùng xác nhận hoặc yêu cầu. |
| US40 — Là người dùng, tôi muốn xem nguồn, thời điểm kiểm tra và mức độ tin cậy của thông tin biến động để đánh giá tính cập nhật của thông tin. | SYS40 — Là hệ thống, tôi cần cung cấp mọi thông tin biến động kèm nguồn, thời điểm kiểm tra và mức độ tin cậy. |
| US41 — Là người dùng, tôi muốn bật hoặc tắt theo dõi GPS chủ động cho từng chuyến đi để kiểm soát việc sử dụng vị trí của mình. | SYS41 — Là hệ thống, tôi cần cho phép bật hoặc tắt theo dõi GPS chủ động theo từng chuyến đi. |

### Cập nhật thời gian thực (Nhân)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US42 — Là người dùng đang trong chuyến đi, tôi muốn theo dõi thời tiết, thời gian di chuyển và giờ mở cửa để chủ động điều chỉnh lịch trình trong chuyến đi. | SYS42 — Là hệ thống, tôi cần dùng background job định kỳ để kiểm tra các thông tin có thể ảnh hưởng đến những chuyến đi đang hoạt động như thời tiết, thời gian di chuyển và giờ mở cửa. |
| US43 — Là người dùng, tôi muốn được cảnh báo khi có sự cố ảnh hưởng đến lịch trình và nhận các phương án thay thế phù hợp. | SYS43 — Là hệ thống, tôi cần gửi cảnh báo kịp thời và đề xuất địa điểm, phương tiện hoặc lộ trình thay thế. |
| US44 — Là người dùng, tôi muốn xem và chấp thuận mọi thay đổi trước khi hệ thống cập nhật kế hoạch đã chốt. | SYS44 — Là hệ thống, tôi chỉ cập nhật kế hoạch đã chốt sau khi nhận được sự đồng ý của người dùng. |
| US45 — Là người dùng, tôi muốn biết rõ địa điểm nào không thể ghé thăm do đóng cửa hoặc có rủi ro an toàn. | SYS45 — Là hệ thống, tôi cần đánh dấu địa điểm không thể thực hiện khi đã đóng cửa hoặc có rủi ro an toàn rõ ràng. |

## Đánh giá và nhận xét (Nhân)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US46 — Là người dùng, tôi muốn chấm điểm và viết nhận xét về địa điểm hoặc trải nghiệm của mình. | SYS46 — Là hệ thống, tôi cần tiếp nhận và lưu điểm số cùng nhận xét của người dùng về địa điểm hoặc trải nghiệm. |
| US47 — Là người dùng, tôi muốn bài đánh giá được lưu ở chế độ riêng tư mặc định và chỉ công khai khi tôi chủ động lựa chọn. | SYS47 — Là hệ thống, tôi cần lưu bài đánh giá mới ở chế độ riêng tư mặc định. |
| US48 — Là người dùng, tôi muốn có thể công khai hoặc chuyển lại thành riêng tư đối với từng bài đánh giá. | SYS48 — Là hệ thống, tôi cần cho phép người dùng công khai hoặc chuyển lại thành riêng tư đối với từng bài đánh giá. |
| US49 — Là người dùng, tôi muốn có thể báo cáo những bài đánh giá chứa nội dung vi phạm. | SYS49 — Là hệ thống, tôi cần tiếp nhận và xử lý báo cáo về các bài đánh giá vi phạm. |
| US50 — Là người dùng, tôi muốn các đánh giá công khai được kiểm duyệt để có thể tham khảo nội dung phù hợp và đáng tin cậy. | SYS50 — Là hệ thống, tôi cần kiểm duyệt, phát hiện spam và xác minh mức độ liên quan của đánh giá công khai. |
| US51 — Là người dùng, tôi muốn tham khảo các đánh giá đáng tin cậy để lựa chọn địa điểm phù hợp hơn. | SYS51 — Là hệ thống, tôi chỉ sử dụng các đánh giá công khai hợp lệ làm tín hiệu xếp hạng địa điểm. |

## Tổng kết chuyến đi (An)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US52 — Là một người dùng, tôi muốn nhận thông báo và xem bản nháp tổng kết tự động khi chuyến đi kết thúc hoặc khi tôi chủ động bấm kết thúc sớm, để tôi dễ dàng xem lại toàn bộ trải nghiệm mà không cần tự ghi nhớ hay tạo mới từ đầu. | SYS52 — Là hệ thống, tôi cần dùng background job định kỳ để quét chuyến đi đến thời điểm kết thúc hoặc nhận tín hiệu kết thúc sớm và tạo đúng một bản nháp tổng kết có cấu trúc cho người dùng xem xét. |
| US53 — Là một người dùng, tôi muốn xem danh sách các địa điểm trong kế hoạch được phân loại trực quan thành địa điểm đã đi, địa điểm đã bỏ qua và địa điểm phát sinh thực tế, để tôi nắm rõ mức độ bám sát kế hoạch ban đầu. | SYS53 — Là hệ thống, tôi cần tự động đối chiếu lịch trình đã chốt với dữ liệu tương tác, thông báo xác nhận và tọa độ GPS nếu người dùng bật để phân loại các điểm đã đi, điểm bị bỏ qua và các điểm phát sinh. |
| US54 — Là một người dùng, tôi muốn có thể đánh dấu lại hoặc thêm, bớt các điểm đến trong danh sách đã đi hoặc bỏ qua nếu hệ thống nhận diện chưa chính xác để bản tổng kết phản ánh chính xác nhất hành trình thực tế của tôi. | SYS54 — Là hệ thống, tôi cần cho phép người dùng điều chỉnh danh sách địa điểm đã đi, đã bỏ qua và phát sinh thực tế trong bản tổng kết. |
| US55 — Là một người dùng, tôi muốn tự nhập số tiền thực tế mình đã chi tiêu cho từng hạng mục như lưu trú, di chuyển, ăn uống, vé tham quan và chi phí phát sinh để quản lý và lưu trữ dữ liệu tài chính của chuyến đi. | SYS55 — Là hệ thống, tôi cần tiếp nhận và lưu chi phí thực tế do người dùng nhập theo từng hạng mục của chuyến đi. |
| US56 — Là một người dùng, tôi muốn hệ thống tự động so sánh chi phí thực tế tôi đã nhập với ngân sách dự kiến ban đầu kèm phân tích chênh lệch để tôi đánh giá mức độ chi tiêu và rút kinh nghiệm cho các chuyến đi sau. | SYS56 — Là hệ thống, tôi cần tự động tính toán tổng số tiền thực chi, mức chênh lệch tuyệt đối và tỷ lệ phần trăm bội chi hoặc tiết kiệm theo từng danh mục so với dự trù ban đầu. |
| US57 — Là một người dùng, tôi muốn có thể chọn bỏ qua việc nhập chi phí thực tế nếu không nhớ rõ hoặc không có nhu cầu để tiếp tục hoàn thành bản tổng kết mà không bị bắt buộc điền số liệu tài chính. | SYS57 — Là hệ thống, tôi cần cho phép người dùng hoàn thành bản tổng kết mà không bắt buộc nhập chi phí thực tế. |
| US58 — Là một người dùng, tôi muốn chấm điểm số sao tổng thể, viết nhật ký cảm nhận và đính kèm ảnh kỷ niệm vào chuyến đi để lưu giữ kỷ niệm đáng nhớ của chuyến đi. | SYS58 — Là hệ thống, tôi cần ghi nhận điểm số tổng thể, nhật ký cảm nhận và ảnh kỷ niệm vào bản tổng kết chuyến đi. |
| US59 — Là một người dùng, tôi muốn viết nhận xét và chấm điểm riêng cho từng điểm đến đã ghé thăm, và các bài đánh giá này mặc định được lưu ở chế độ riêng tư để tôi tự ghi nhớ trải nghiệm mà không bị lộ thông tin riêng tư. | SYS59 — Là hệ thống, tôi cần lưu nhận xét và điểm số cho từng điểm đến ở chế độ riêng tư mặc định. |
| US60 — Là một người dùng, tôi muốn có tùy chọn gạt nút chuyển từng bài đánh giá địa điểm từ chế độ riêng tư sang công khai để hỗ trợ cộng đồng du lịch có thêm thông tin tham khảo hữu ích và đóng góp vào điểm xếp hạng địa điểm. | SYS60 — Là hệ thống, tôi cần tự động quét nội dung bài đánh giá mà người dùng yêu cầu công khai để kiểm tra vi phạm tiêu chuẩn cộng đồng, chống spam và xác thực chuyến đi hợp lệ trước khi hiển thị cho cộng đồng. |
| US61 — Là một người dùng, tôi muốn tự do điều chỉnh bất kỳ nội dung nào trong bản tổng kết trước khi chốt dữ liệu cuối cùng để bản tổng kết đạt độ chính xác và trọn vẹn nhất theo ý tôi. | SYS61 — Là hệ thống, tôi cần cho phép người dùng chỉnh sửa bản tổng kết trước khi xác nhận dữ liệu cuối cùng. |
| US62 — Là một người dùng, tôi muốn bấm nút xác nhận chốt bản tổng kết chuyến đi để khóa dữ liệu chuyến đi vào lịch sử và đồng ý cho hệ thống học hỏi từ dữ liệu này để cá nhân hóa các chuyến đi sau. | SYS62 — Là hệ thống, tôi cần tự động trích xuất các đặc điểm sở thích, thói quen tài chính và nhịp độ di chuyển thực tế từ bản tổng kết sau khi người dùng xác nhận để cập nhật vào hồ sơ du lịch. |
| US63 — Là một người dùng, tôi muốn nhận được 1 đến 3 gợi ý ý tưởng chuyến đi mới ngay sau khi xác nhận bản tổng kết, dựa trên sở thích và dữ liệu lịch sử vừa được cập nhật để tôi có thêm cảm hứng lên kế hoạch cho kỳ nghỉ kế tiếp. | SYS63 — Là hệ thống, tôi cần phân tích hồ sơ du lịch vừa được cập nhật và dữ liệu chuyến đi vừa hoàn thành để tự động sinh ra các kịch bản chuyến đi tiếp theo phù hợp. |
| US64 — Là một người dùng, tôi muốn có thể bấm nút bắt đầu lập kế hoạch ngay từ thẻ gợi ý chuyến đi tiếp theo để hệ thống mở khung hội thoại mới và tự động điền sẵn các sở thích đã tích lũy mà tôi không cần mô tả lại từ đầu. | SYS64 — Là hệ thống, tôi cần mở khung hội thoại lập kế hoạch mới và điền sẵn các sở thích đã tích lũy khi người dùng chọn bắt đầu từ một thẻ gợi ý chuyến đi tiếp theo. |

## Nhật ký kiểm toán (An)

| User story phía người dùng | User story phía hệ thống |
| --- | --- |
| US65 — Là một người dùng, tôi muốn xem phần giải thích ngắn gọn bằng ngôn ngữ dễ hiểu về lý do Agent đề xuất một lộ trình, địa điểm hoặc sự thay đổi cụ thể để tôi hiểu căn cứ lựa chọn và tin tưởng hơn vào quyết định của Agent. | SYS65 — Là hệ thống kiểm toán, tôi cần lưu và hiển thị phần tóm tắt lý do quyết định của Agent bằng ngôn ngữ dễ hiểu. |
| US66 — Là một người dùng, tôi muốn kiểm tra nguồn gốc của thông tin biến động như thời tiết, giá vé, giờ mở cửa, cùng với thời gian kiểm tra gần nhất và mức độ tin cậy để tôi an tâm lên lịch trình mà không lo thông tin bị lỗi thời. | SYS66 — Là hệ thống kiểm toán, tôi cần lưu và cho phép người dùng xem nguồn dữ liệu, thời điểm kiểm tra và mức độ tin cậy của thông tin biến động. |
| US67 — Là một người dùng, tôi muốn xem rõ các cảnh báo rủi ro hoặc sự đánh đổi khi Agent đưa ra hoặc thay đổi một phương án để tôi tự cân nhắc và lựa chọn phương án tối ưu nhất cho mình. | SYS67 — Là hệ thống kiểm toán, tôi cần lưu và cho phép người dùng xem các cảnh báo, thay đổi và sự đánh đổi liên quan đến quyết định của Agent. |
| US68 — Là một nhân viên vận hành, tôi muốn tra cứu và lọc nhật ký kỹ thuật theo mã chuyến đi, loại Agent (Planner, Critic, Booking), mã lỗi hoặc mốc thời gian dựa trên quyền hạn được cấp để nhanh chóng khoanh vùng và xử lý các vấn đề phát sinh trong hệ thống. | SYS68 — Là hệ thống kiểm toán, tôi cần cho phép đội vận hành tra cứu và lọc nhật ký kỹ thuật theo phân quyền, mã chuyến đi, loại Agent, mã lỗi và mốc thời gian. |
| US69 — Là một nhân viên vận hành, tôi muốn có giao diện bắt buộc khai báo mục đích truy cập và mã yêu cầu hỗ trợ (Ticket ID) trước khi hệ thống mở chi tiết log kỹ thuật của người dùng để thực hiện đúng quy trình an toàn thông tin và bảo vệ quyền riêng tư của khách hàng. | SYS69 — Là hệ thống giám sát an ninh, tôi cần bắt buộc có cả mục đích truy cập và Ticket ID, đồng thời lưu danh tính nhân viên, thời gian truy cập chính xác, địa chỉ IP, mục đích và Ticket ID mỗi khi có người mở xem chi tiết log kỹ thuật. |
| US70 — Là một Quản trị viên (Admin) phụ trách kỹ thuật hệ thống, tôi muốn xem biểu đồ dòng thực thi thể hiện dữ liệu đầu vào, các công cụ đã gọi, kết quả trả về và việc bàn giao nhiệm vụ giữa các Agent để giám sát kỹ thuật, truy vết nguyên nhân gốc rễ khi xảy ra lỗi hoặc phản hồi chậm trễ. | SYS70 — Là hệ thống kiểm toán, tôi cần tự động bắt và lưu trữ đầy đủ dữ liệu đầu vào, phản hồi, nguồn dữ liệu, công cụ đã gọi, kết quả công cụ, tóm tắt lý do quyết định, mã lỗi và phiên bản Agent để hỗ trợ truy vết và kiểm tra lại quyết định. |

## Quản trị hệ thống và Vận hành Maker – Checker

| User story phía người dùng / quản trị | User story phía hệ thống |
| --- | --- |
| US71 — Là một nhân viên vận hành (Operator), tôi muốn gửi kiến nghị thay đổi thông tin địa điểm (giá vé, giờ mở cửa), báo cáo sự cố thời tiết thực tế hoặc phản ánh logic AI lên hệ thống để Admin xem xét và phê duyệt. | SYS71 — Là hệ thống, tôi cần lưu trữ các kiến nghị thay đổi của Operator ở trạng thái chờ duyệt (pending) và thông báo đến Admin. |
| US72 — Là một Quản trị viên (Admin), tôi muốn xem danh sách các kiến nghị từ Operator, kiểm tra căn cứ minh chứng và quyết định phê duyệt (áp dụng vào hệ thống) hoặc từ chối kèm ghi chú phản hồi. | SYS72 — Là hệ thống, tôi cần cho phép Admin phê duyệt hoặc từ chối kiến nghị; khi phê duyệt loại địa điểm, hệ thống tự động cập nhật dữ liệu tương ứng vào kho địa điểm du lịch. |
| US73 — Là một Quản trị viên (Admin), tôi muốn toàn quyền thêm mới, chỉnh sửa thông tin, tạm ẩn hoặc xóa địa điểm du lịch, danh mục và nội dung thuyết minh để đảm bảo kho dữ liệu luôn đầy đủ và chính xác. | SYS73 — Là hệ thống, tôi cần cung cấp các công cụ quản trị dữ liệu địa điểm du lịch có kiểm duyệt cho Admin. |
| US74 — Là một Quản trị viên (Admin), tôi muốn khóa (ban) hoặc mở khóa tài khoản người dùng vi phạm tiêu chuẩn cộng đồng, đồng thời phân quyền hoặc thu hồi vai trò Operator cho nhân viên. | SYS74 — Là hệ thống, tôi cần cho phép Admin quản lý trạng thái tài khoản người dùng và phân quyền vai trò theo chính sách an toàn. |
| US75 — Là một Quản trị viên (Admin), tôi muốn tùy chỉnh các tham số cấu hình toàn cục của hệ thống (chu kỳ kiểm tra thời tiết, thời hạn lưu trữ dữ liệu tạm, giới hạn phương án lộ trình) để hệ thống vận hành linh hoạt. | SYS75 — Là hệ thống, tôi cần lưu trữ và áp dụng các cấu hình tham số toàn cục do Admin thiết lập mà không cần khởi động lại ứng dụng. |

## Chính sách dữ liệu dùng chung

- Dữ liệu GPS, tệp media gốc, working/trip memory của Agent và log kỹ thuật chi tiết có thời hạn lưu tối đa 7 ngày.
- Một cron job chạy hằng ngày để đánh dấu dữ liệu hết hạn và dọn dẹp bản ghi hoặc object quá hạn.
- Hồ sơ, kế hoạch, đánh giá, bản tổng kết và các dữ liệu có cấu trúc đã được người dùng xác nhận tiếp tục được lưu trong lịch sử tài khoản.
