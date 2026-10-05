import { publicClient } from '@/api/client';
import type {
  AdminUsersResponse,
  PutAssignRoleRequest,
  PutAssignRoleResponse,
  PutUserStatusRequest,
  PutUserStatusResponse,
} from '@/features/admin-user/admin-user.types';

export async function getAdminUsers(limit: number, offset: number): Promise<AdminUsersResponse> {
  const { data } = await publicClient.get<AdminUsersResponse>('/api/admin/users', {
    params: { limit, offset },
  });
  return data;
}

export async function putAssignRole(userId: string, request: PutAssignRoleRequest): Promise<PutAssignRoleResponse> {
  const { data } = await publicClient.put<PutAssignRoleResponse>(`/api/admin/users/role/${userId}`, request);
  return data;
}

export async function putUserStatus(userId: string, request: PutUserStatusRequest): Promise<PutUserStatusResponse> {
  const { data } = await publicClient.put<PutUserStatusResponse>(`/api/admin/users/status/${userId}`, request);
  return data;
}
