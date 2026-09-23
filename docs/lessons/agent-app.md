# AGENT ENGINEERING 
## Agent 
Agent là một ứng dụng cho phép model chọn bước tiếp theo sau khi xem xét kết quả được gửi lên. 

Bốn thành phần tối thiểu 
- Goal: Mục tiêu cần đạt 
- Tools: Công cụ cho agent 
- Loop: Đưa kết quả trở lại làm đầu vào
- Termination: Cơ chế quyết định dừng hay là chạy tiếp (quan trọng, phải có không là con agent nó chạy miết)

agent = goal + tools + loop + termination

### Goal 
Tìm commit làm hỏng `test_checkout` và mở issue 

### Tools 
Model gọi qua giao thức tool calling, có name, description và parameters 

### Loop
Chu trình đưa kết quả của hành động vừa thực hiện trở lại, làm đầu vào cho suy luận tiếp theo. 

### Termination
Cơ chế quyết định **chạy tiếp hay dừng lại**

## Phân loại
### Agent truyền thống vs AI Agent  
Input -> Bước 1 -> Bước 2 .... -> Output 
### Agent Loop 
Dòng ngữ cảnh ---- Model đề xuất tool (1) ---- Harness gọi tool ---- Ghi kết quả ----- Xét điều kiện dừng (1)

Bước **Xét điều kiện dừng**: lặp, chờ người, thoát

Model sẽ đề xuất, sinh lời gọi tool, harness thực thi, ghi state và xét điều kiện dừng
### Tool call 
Thực hiện cơ chế quản lý State. 
```py
{
    "name": "weather-forecast",
    "args": ["toon", "city"],
    "id": "city_id"
}
```

### Chuẩn hóa structured output
Khi thực thi một tool thì phải yêu cầu AI luôn trả về một structured output. 
**Output** ngu: 
```
<div>...</div>
```

**Output** tốt: 
```
{

}
```

### Chi phí của lịch sử 
Mỗi vòng lặp thì nó lại nạp toàn bộ lịch sử context => dài thêm sau mỗi vòng => cút, chi phí = 2^số vòng

Thế làm sao để tối đa ngân sách? Bạn hãy thực hiện các câu hỏi sau
- Bước: lặp tối đa bao nhiêu bước? 
- Token: Tối đa bao nhiêu token cho một phiên 
- Thời gian: Tối đa bao nhiêu giây
- Chi phí: Trần chi phí cho 1 tác vụ. 

## ReAct và các mẫu suy luận 
Cách tổ chức suy luận bên trong vòng lặp
### ReAct
ReAct, là kiến trúc cốt lõi giúp AI Agent liên tục suy luận / hành động và quan sát.

Suy luận --- Hành động --- Quan sát 
  |                             |
  |                             |
  -------------------------------


### Plan then exxecute 
- Là mẫu gọi model một lần để sinh trọn kế hoạch, rồi thực thi từng bước theo kế hoạch đó.

### Mẫu lai: ReAct + Plan Then Execute 


Lập kế hoạch, thực thi vài bước, rồi lặp lại kế hoạch dựa trên những gì đã quan sát


### Mẫu reflection 
Là mẫu kiến trúc cho phép Agent tự đánh giá và sửa lỗi kết quả của chính mình. Nó sẽ tự hỏi là output đã ĐẠT YÊU CẦU người dùng chưa, từ đó quyết định quay lại hoặc đi đến kết luận cuối

- Tự động phát hiện và sửa lỗi sai 
- Nâng cao đáng kể chất lượng đầu ra

| Mẫu | Chọn khi | Rủi ro |
| --- | --- | --- |
| React | Không đoán trước được số bước | Lặp vô hạn |
| Plan then execute | Cần duyệt trước | Kế hoạch lỗi thời |
| Mẫu lai | Môi trường biến động | Khó debug |
| Reflection | Có tín hiệu kiểm chứng ngoài | x2 tiền |

