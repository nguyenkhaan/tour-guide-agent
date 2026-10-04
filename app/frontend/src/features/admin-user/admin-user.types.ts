import type { components, paths } from '@/types/api-contract';

export type AdminUsersResponse = paths['/api/admin/users']['get']['responses'][200]['content']['application/json'];
export type AdminUser = AdminUsersResponse[number];

export type UserRole = components['schemas']['UserRole'];
export const UserRole = {
  USER: 'USER',
  ADMIN: 'ADMIN',
  OPERATOR: 'OPERATOR',
} as const satisfies Record<string, UserRole>;

export type AccountStatus = components['schemas']['AccountStatus'];
export const AccountStatus = {
  DISABLED: 'DISABLED',
  BANNED: 'BANNED',
  ACTIVE: 'ACTIVE',
} as const satisfies Record<string, AccountStatus>;

export type AdminUserAction = 'BAN' | 'UNBAN' | 'MAKE_OPERATOR' | 'REVOKE_OPERATOR';
export type AdminUserSortField = 'full_name' | 'role' | 'status' | 'created_at';
export type AdminUserRoleFilter = UserRole | 'ALL';
export type AdminUserStatusFilter = AccountStatus | 'ALL';
