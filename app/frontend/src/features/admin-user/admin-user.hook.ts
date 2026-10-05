import { useMutation, useQuery } from '@tanstack/react-query';
import {
  getAdminUsers,
  putAssignRole,
  putUserStatus,
} from '@/features/admin-user/admin-user.service';
import type {
  PutAssignRoleRequest,
  PutUserStatusRequest,
} from '@/features/admin-user/admin-user.types';

export function useGetAdminUsersQuery(limit: number, offset: number) {
  return useQuery({
    queryKey: ['admin-users', limit, offset],
    queryFn: () => getAdminUsers(limit, offset),
  });
}

export function usePutAssignRoleMutation() {
  return useMutation({
    mutationFn: ({ userId, request }: { userId: string; request: PutAssignRoleRequest }) =>
      putAssignRole(userId, request),
  });
}

export function usePutUserStatusMutation() {
  return useMutation({
    mutationFn: ({ userId, request }: { userId: string; request: PutUserStatusRequest }) =>
      putUserStatus(userId, request),
  });
}
