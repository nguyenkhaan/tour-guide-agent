import { useEffect, useMemo, useState } from 'react';
import {
  useGetAdminUsersQuery,
  usePutAssignRoleMutation,
  usePutUserStatusMutation,
} from '@/features/admin-user/admin-user.hook';
import {
  AccountStatus,
  UserRole,
  type AdminUser,
  type AdminUserAction,
  type AdminUserRoleFilter,
  type AdminUserSortField,
  type AdminUserStatusFilter,
} from '@/features/admin-user/admin-user.types';
import { AdminUserActionModal } from '@/features/admin-user/components/AdminUserActionModal';
import { AdminUserDrawer } from '@/features/admin-user/components/AdminUserDrawer';
import { AdminUserFilters } from '@/features/admin-user/components/AdminUserFilters';
import { AdminUserStats } from '@/features/admin-user/components/AdminUserStats';
import { AdminUsersHeader } from '@/features/admin-user/components/AdminUsersHeader';
import { AdminUsersTable } from '@/features/admin-user/components/AdminUsersTable';

export default function AdminUsersPage() {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRole, setSelectedRole] = useState<AdminUserRoleFilter>('ALL');
  const [selectedStatus, setSelectedStatus] = useState<AdminUserStatusFilter>('ALL');
  const [sortBy, setSortBy] = useState<AdminUserSortField>('created_at');
  const [sortAsc, setSortAsc] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(5);
  const offset = (currentPage - 1) * pageSize;
  const { data, isError, isFetching, isLoading, refetch } = useGetAdminUsersQuery(pageSize, offset);
  const assignRoleMutation = usePutAssignRoleMutation();
  const userStatusMutation = usePutUserStatusMutation();
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [actionUser, setActionUser] = useState<AdminUser | null>(null);
  const [action, setAction] = useState<AdminUserAction | null>(null);

  useEffect(() => setUsers(data?.items ?? []), [data]);

  const filteredUsers = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();

    return users
      .filter((user) => {
        const matchesQuery = !query || [user.email, user.full_name ?? '']
          .some((value) => value.toLowerCase().includes(query));
        const matchesRole = selectedRole === 'ALL' || user.role === selectedRole;
        const matchesStatus = selectedStatus === 'ALL' || user.status === selectedStatus;
        return matchesQuery && matchesRole && matchesStatus;
      })
      .slice()
      .sort((first, second) => {
        const comparison = sortBy === 'created_at'
          ? new Date(first.created_at).getTime() - new Date(second.created_at).getTime()
          : (first[sortBy] ?? '').localeCompare(second[sortBy] ?? '');
        return sortAsc ? comparison : -comparison;
      });
  }, [users, searchQuery, selectedRole, selectedStatus, sortBy, sortAsc]);

  const totalUsers = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(totalUsers / pageSize));
  const paginatedUsers = filteredUsers;

  const resetPage = <T,>(setter: (value: T) => void) => (value: T) => {
    setter(value);
    setCurrentPage(1);
  };

  const resetFilters = () => {
    setSearchQuery('');
    setSelectedRole('ALL');
    setSelectedStatus('ALL');
    setCurrentPage(1);
  };

  const toggleSort = (field: AdminUserSortField) => {
    setSortAsc(field === sortBy ? !sortAsc : true);
    setSortBy(field);
  };

  const openAction = (user: AdminUser, nextAction: AdminUserAction) => {
    assignRoleMutation.reset();
    userStatusMutation.reset();
    setActionUser(user);
    setAction(nextAction);
  };

  const closeAction = () => {
    setActionUser(null);
    setAction(null);
  };

  const confirmAction = () => {
    if (!actionUser || !action) return;

    const updateUser = (updatedUser: AdminUser) => {
      setUsers((currentUsers) => currentUsers.map((user) => user.id === updatedUser.id ? updatedUser : user));
      setSelectedUser((currentUser) => currentUser?.id === updatedUser.id ? updatedUser : currentUser);
      closeAction();
      void refetch();
    };

    if (action === 'MAKE_OPERATOR' || action === 'REVOKE_OPERATOR') {
      const role = action === 'MAKE_OPERATOR' ? UserRole.OPERATOR : UserRole.USER;
      assignRoleMutation.mutate(
        { userId: actionUser.id, request: { role } },
        { onSuccess: () => updateUser({ ...actionUser, role }) },
      );
      return;
    }

    const status = action === 'BAN' ? AccountStatus.BANNED : AccountStatus.ACTIVE;
    userStatusMutation.mutate(
      { userId: actionUser.id, request: { status } },
      { onSuccess: () => updateUser({ ...actionUser, status }) },
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-16 text-slate-900">
      <AdminUsersHeader
        isRefreshing={isFetching}
        onRefresh={() => {
          setUsers(data?.items ?? []);
          setSelectedUser(null);
          void refetch();
        }}
      />

      <main className="mx-auto max-w-7xl px-4 pt-8 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">User directory</h2>
          <p className="mt-1 text-sm text-slate-600">Review registered user accounts, roles, and account statuses.</p>
        </div>

        {isLoading ? (
          <p className="rounded-xl border border-slate-200 bg-white p-8 text-center text-sm text-slate-600">
            Loading users...
          </p>
        ) : isError ? (
          <div className="rounded-xl border border-rose-200 bg-rose-50 p-8 text-center">
            <p className="text-sm font-medium text-rose-700">Unable to load users.</p>
            <button type="button" onClick={() => void refetch()} className="mt-3 text-xs font-semibold text-rose-700 underline">
              Try again
            </button>
          </div>
        ) : (
          <>
            <AdminUserStats users={users} />
            <AdminUserFilters
              searchQuery={searchQuery}
              selectedRole={selectedRole}
              selectedStatus={selectedStatus}
              onSearchChange={resetPage(setSearchQuery)}
              onRoleChange={resetPage(setSelectedRole)}
              onStatusChange={resetPage(setSelectedStatus)}
              onReset={resetFilters}
            />
            <AdminUsersTable
              users={paginatedUsers}
              totalUsers={totalUsers}
              currentPage={currentPage}
              pageSize={pageSize}
              totalPages={totalPages}
              sortBy={sortBy}
              sortAsc={sortAsc}
              onSort={toggleSort}
              onView={setSelectedUser}
              onAction={openAction}
              onPageChange={setCurrentPage}
              onPageSizeChange={resetPage(setPageSize)}
              onResetFilters={resetFilters}
            />
          </>
        )}
      </main>

      <AdminUserDrawer user={selectedUser} onClose={() => setSelectedUser(null)} onAction={openAction} />
      <AdminUserActionModal
        user={actionUser}
        action={action}
        isPending={assignRoleMutation.isPending || userStatusMutation.isPending}
        isError={assignRoleMutation.isError || userStatusMutation.isError}
        onCancel={closeAction}
        onConfirm={confirmAction}
      />
    </div>
  );
}
