import { publicClient } from '@/api/client';
import type { AdminUsersResponse } from '@/features/admin-user/admin-user.types';

export async function getAdminUsers(): Promise<AdminUsersResponse> {
  const { data } = await publicClient.get<AdminUsersResponse>('/api/admin/users');
  return data;
}
