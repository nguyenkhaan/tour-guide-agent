
export const AdminUsersKey = {
    base: ["admin-users"] as const,
    list: () => [AdminUsersKey.base , "list"] as const
}