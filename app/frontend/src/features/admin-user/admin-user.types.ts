import type { components } from '@/types/api-contract';

export type AdminUser = components['schemas']['GetAdminUserResponse'];
export type AdminUsersResponse = {
  items: AdminUser[];
  total: number;
};
export type PutAssignRoleRequest = components['schemas']['PutAssignRoleRequest'];
export type PutAssignRoleResponse = components['schemas']['PutAssignRoleResponse'];
export type PutUserStatusRequest = components['schemas']['PutUserStatusRequest'];
export type PutUserStatusResponse = components['schemas']['PutUserStatusResponse'];

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
