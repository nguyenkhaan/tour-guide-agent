import { useMemo, useState } from 'react';
import { INITIAL_ADMIN_USERS } from '@/features/admin-users/admin-users.data';
import {
  AccountStatus,
  UserRole,
  type AdminUser,
  type AdminUserAction,
  type AdminUserRoleFilter,
  type AdminUserSortField,
  type AdminUserStatusFilter,
} from './admin-users.types';
import { AdminUserActionModal } from '@/features/admin-users/components/AdminUserActionModal';
import { AdminUserDrawer } from '@/features/admin-users/components/AdminUserDrawer';
import { AdminUserFilters } from '@/features/admin-users/components/AdminUserFilters';
import { AdminUserStats } from '@/features/admin-users/components/AdminUserStats';
import { AdminUsersHeader } from '@/features/admin-users/components/AdminUsersHeader';
import { AdminUsersTable } from '@/features/admin-users/components/AdminUsersTable';

export default function AdminUsersPage() {
  const [users, setUsers] = useState(INITIAL_ADMIN_USERS);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRole, setSelectedRole] = useState<AdminUserRoleFilter>('ALL');
  const [selectedStatus, setSelectedStatus] = useState<AdminUserStatusFilter>('ALL');
  const [sortBy, setSortBy] = useState<AdminUserSortField>('created_at');
  const [sortAsc, setSortAsc] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(5);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);
  const [actionUser, setActionUser] = useState<AdminUser | null>(null);
  const [action, setAction] = useState<AdminUserAction | null>(null);

  const filteredUsers = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();

    return users
      .filter((user) => {
        const matchesQuery = !query || [user.id, user.email, user.full_name ?? '']
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

  const totalPages = Math.max(1, Math.ceil(filteredUsers.length / pageSize));
  const paginatedUsers = filteredUsers.slice((currentPage - 1) * pageSize, currentPage * pageSize);

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
    setActionUser(user);
    setAction(nextAction);
  };

  const closeAction = () => {
    setActionUser(null);
    setAction(null);
  };

  const confirmAction = () => {
    if (!actionUser || !action) return;

    const updatedUser: AdminUser = {
      ...actionUser,
      status: action === 'BAN'
        ? AccountStatus.BANNED
        : action === 'UNBAN'
          ? AccountStatus.ACTIVE
          : actionUser.status,
      role: action === 'MAKE_OPERATOR'
        ? UserRole.OPERATOR
        : action === 'REVOKE_OPERATOR'
          ? UserRole.USER
          : actionUser.role,
    };

    setUsers((currentUsers) => currentUsers.map((user) => user.id === updatedUser.id ? updatedUser : user));
    setSelectedUser((currentUser) => currentUser?.id === updatedUser.id ? updatedUser : currentUser);
    closeAction();
  };

  return (
    <div className="min-h-screen bg-slate-50 pb-16 text-slate-900">
      <AdminUsersHeader
        isRefreshing={false}
        onRefresh={() => {
          setUsers(INITIAL_ADMIN_USERS);
          setSelectedUser(null);
        }}
      />

      <main className="mx-auto max-w-7xl px-4 pt-8 sm:px-6 lg:px-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900">User directory</h2>
          <p className="mt-1 text-sm text-slate-600">Review registered user accounts, roles, and account statuses.</p>
        </div>

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
          totalUsers={filteredUsers.length}
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
      </main>

      <AdminUserDrawer user={selectedUser} onClose={() => setSelectedUser(null)} onAction={openAction} />
      <AdminUserActionModal user={actionUser} action={action} onCancel={closeAction} onConfirm={confirmAction} />
    </div>
  );
}
