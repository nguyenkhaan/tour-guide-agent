export enum AccountStatus {
  DISABLED = 'DISABLED',
  BANNED = 'BANNED',
  ACTIVE = 'ACTIVE',
}

export enum UserRole {
  USER = 'USER',
  ADMIN = 'ADMIN',
  OPERATOR = 'OPERATOR',
}

export interface AdminUser {
  id: string;
  email: string;
  full_name: string | null;
  status: AccountStatus | null;
  role: UserRole | null;
  created_at: string;
  updated_at: string;
}

export type AdminUserAction = 'BAN' | 'UNBAN' | 'MAKE_OPERATOR' | 'REVOKE_OPERATOR';
export type AdminUserSortField = 'full_name' | 'role' | 'status' | 'created_at';
export type AdminUserRoleFilter = UserRole | 'ALL';
export type AdminUserStatusFilter = AccountStatus | 'ALL';
