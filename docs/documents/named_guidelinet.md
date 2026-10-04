
# Nguyên tắc đặt tên trong dự án

Mỗi tên hàm/dto/hook phải được đặt tên theo nguyên tắc chuyên suốt vòng đời dự án

Công thức chung:

```text
<HTTP Method> + <Operation Name> + <Suffix>
```

Ví dụ với thao tác lấy danh sách user trong hệ thống (cho admin). Tôi sẽ tự đặt operation name là: AdminUsers

```text
HTTP method:     Get
Operation name:  AdminUsers
```

Ứng với thao tác lấy danh sách user trong hệ thống. Chúng ta sẽ có các cách đặt tên dưới đây

```text
get_admin_users_handler # Hàm controller trong Backend 
get_admin_users # Hàm service tương ứng với controller này trong backend 
GetAdminUsersResponse # dto response 
getAdminUsers # Hàm service tương ứng bên trong frontend 
useGetAdminUsersQuery # Tanstack hook
```

Sau đây tôi sẽ trình bày một số thành phần trong dự án, kèm theo nguyên tắc đặt tên cho chúng. 

## 1. API route

Route sử dụng danh từ số nhiều và không chứa động từ:

```http
GET    /api/admin/users
POST   /api/admin/users
GET    /api/admin/users/{user_id}
PUT    /api/admin/users/{user_id}
PATCH  /api/admin/users/{user_id}
DELETE /api/admin/users/{user_id}
```

Không sử dụng:

```http
GET /api/admin/get-users
POST /api/admin/create-user
```

HTTP method đã biểu diễn hành động.

## 2. Backend controller

Sử dụng `snake_case`, bắt đầu bằng HTTP method và kết thúc bằng hậu tố `_handler`:

```text
<http_method>_<operation>_handler
```

Ví dụ:

```python
get_admin_users_handler
get_admin_user_handler
post_admin_user_handler
put_admin_user_handler
patch_admin_user_handler
delete_admin_user_handler
```

## 3. Backend service function

Ứng với mỗi controller, chúng ta sẽ có 1 hàm service để xử lý logic. Chúng ta sử dụng cùng tên với controller nhưng bỏ hậu tố `_handler`:

```text
<method>_<operation>
```

Ví dụ:

```python
get_admin_users
get_admin_user
post_admin_user
put_admin_user
patch_admin_user
delete_admin_user
```

Quan hệ giữa controller và service:

```python
async def get_admin_users_handler(service: AdminService):
    return await service.get_admin_users()
```

## 4. DTO

DTO sử dụng `PascalCase` và phải kết thúc bằng `Request` hoặc `Response`:

```text
<Method><Operation>Request
<Method><Operation>Response
```

Ví dụ:

```python
GetAdminUsersResponse
GetAdminUserResponse

PostAdminUserRequest
PostAdminUserResponse

PutAdminUserRequest
PutAdminUserResponse

PatchAdminUserRequest
PatchAdminUserResponse
```

Không tạo DTO không cần thiết. Ví dụ GET không có query parameters hoặc request body thì không cần `GetAdminUsersRequest`.

## 5. Kiểu dữ liệu nghiệp vụ

Type/interface thông thường không có tiền tố hoặc hậu tố kỹ thuật:

```ts
AdminUser
AdminUserAction
AdminUserSortField
AdminUserRoleFilter
AccountStatus
UserRole
```

Các type này được sinh ra từ backend, dựa trên các API route. Nội dung được lưu vào `api-contract.ts`. Các KDL, enum... này nên được tái sử dụng, không khai báo lại cấu trúc.

## 6. Frontend API service

Sử dụng `camelCase`, bắt đầu bằng HTTP method:

```text
<method><Operation>
```

Ví dụ:

```ts
getAdminUsers()
getAdminUser()
postAdminUser()
putAdminUser()
patchAdminUser()
deleteAdminUser()
```

Tên frontend service phải tương ứng với backend service:

```text
Backend:  get_admin_users
Frontend: getAdminUsers
```

Chúng không giống hoàn toàn về cách viết vì Python dùng `snake_case`, TypeScript dùng `camelCase`, nhưng phải có cùng ý nghĩa và cùng operation name.

## 7. TanStack Query hook

GET sử dụng hậu tố `Query`:

```text
use<GetOperation>Query
```

Ví dụ:

```ts
useGetAdminUsersQuery()
useGetAdminUserQuery(userId)
```

POST, PUT, PATCH và DELETE sử dụng hậu tố `Mutation`:

```text
use<WriteOperation>Mutation
```

Ví dụ:

```ts
usePostAdminUserMutation()
usePutAdminUserMutation()
usePatchAdminUserMutation()
useDeleteAdminUserMutation()
```

Hook phải gọi đúng frontend service tương ứng:

```ts
export function useGetAdminUsersQuery() {
  return useQuery({
    queryKey: ['admin-users'],
    queryFn: getAdminUsers,
  });
}
```

Chuỗi tên xuyên suốt:

```text
Backend controller: get_admin_users_handler
Backend service:    get_admin_users
Response DTO:       GetAdminUsersResponse
Frontend service:   getAdminUsers
TanStack hook:      useGetAdminUsersQuery
```

## 8. Tên file frontend

Tên file dựa trên nghiệp vụ logic, không dựa trên từng HTTP method:

```text
admin-user/
├── AdminUsersPage.tsx
├── admin-user.service.ts
├── admin-user.hook.ts
├── admin-user.types.ts
└── components/
```

Không tạo riêng:

```text
get-admin-users.service.ts
patch-admin-user.service.ts
```

Một file service hoặc hook có thể chứa nhiều thao tác cùng domain.

Các file bên trong có chứa nhiều hàm con (ví dụ: file service bên trong chứa nhiều hàm) thì thêm s vào cuối. Ngược lại thì không (ví dụ: file service nhưng bên trong chứa 1 class Service duy nhất, trong đó có các static function).

Khi làm dự án thì tôi quy ước luôn `hook`, `service`, `types`. Các file page (UI) thì đặt số ít. Các folder danh sách (Ví dụ: `types` , `components`, `modules`)

## Quy tắc tổng kết

```text
Controller:       <method>_<operation>_handler
Backend service:  <method>_<operation>
DTO:              <Method><Operation><Request|Response>
Frontend service: <method><Operation>
TanStack GET:     use<GetOperation>Query
TanStack write:   use<Post|Put|Patch|DeleteOperation>Mutation
Domain type:      <DomainName>
```

Quy tắc quan trọng nhất: giữ nguyên cùng một operation name giữa tất cả các layer; chỉ thay đổi casing và suffix theo ngôn ngữ hoặc trách nhiệm.
