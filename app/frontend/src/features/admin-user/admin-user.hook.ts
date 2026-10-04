import { useQuery } from '@tanstack/react-query';
import { getAdminUsers } from '@/features/admin-user/admin-user.service';

export function useGetAdminUsersQuery() {
  return useQuery({
    queryKey: ['admin-users'],
    queryFn: getAdminUsers,
  });
}
