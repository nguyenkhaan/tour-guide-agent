import {
  AccountStatus,
  UserRole,
  type AdminUser,
  type AdminUserAction,
  type AdminUserSortField,
} from '@/features/admin-user/admin-user.types';
import { RoleBadge, StatusBadge } from '@/features/admin-user/components/UserBadges';

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));

export function AdminUsersTable({
  users,
  totalUsers,
  currentPage,
  pageSize,
  totalPages,
  sortBy,
  sortAsc,
  onSort,
  onView,
  onAction,
  onPageChange,
  onPageSizeChange,
  onResetFilters,
}: {
  users: AdminUser[];
  totalUsers: number;
  currentPage: number;
  pageSize: number;
  totalPages: number;
  sortBy: AdminUserSortField;
  sortAsc: boolean;
  onSort: (field: AdminUserSortField) => void;
  onView: (user: AdminUser) => void;
  onAction: (user: AdminUser, action: AdminUserAction) => void;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: number) => void;
  onResetFilters: () => void;
}) {
  const sortLabel = (field: AdminUserSortField) => (sortBy === field ? (sortAsc ? ' ↑' : ' ↓') : '');

  return (
    <section className="overflow-hidden rounded-xl border border-slate-200/80 bg-white shadow-xs">
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left" aria-label="User directory table">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50/80 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
              <SortableHeader label="Account holder" field="full_name" suffix={sortLabel('full_name')} onSort={onSort} />
              <SortableHeader label="Role" field="role" suffix={sortLabel('role')} onSort={onSort} />
              <SortableHeader label="Status" field="status" suffix={sortLabel('status')} onSort={onSort} />
              <SortableHeader label="Created" field="created_at" suffix={sortLabel('created_at')} onSort={onSort} />
              <th scope="col" className="px-4 py-3.5 text-right sm:px-6">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {users.map((user) => (
              <tr key={user.id} className="transition-colors hover:bg-slate-50/70">
                <td className="px-4 py-4 sm:px-6">
                  <p className="font-semibold text-slate-900">{user.full_name ?? '—'}</p>
                  <p className="text-xs text-slate-500">{user.email}</p>
                </td>
                <td className="whitespace-nowrap px-4 py-4"><RoleBadge role={user.role} /></td>
                <td className="whitespace-nowrap px-4 py-4"><StatusBadge status={user.status} /></td>
                <td className="whitespace-nowrap px-4 py-4 text-xs text-slate-600">{formatDate(user.created_at)}</td>
                <td className="whitespace-nowrap px-4 py-4 text-right sm:px-6">
                  <div className="inline-flex items-center gap-1.5">
                    <button
                      type="button"
                      onClick={() => onView(user)}
                      className="rounded-md border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-700 hover:bg-slate-50"
                    >
                      View
                    </button>
                    {user.role !== UserRole.ADMIN && (
                      <>
                        <button
                          type="button"
                          onClick={() => onAction(user, user.role === UserRole.OPERATOR ? 'REVOKE_OPERATOR' : 'MAKE_OPERATOR')}
                          className="rounded-md border border-amber-200 bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-800 hover:bg-amber-100"
                        >
                          {user.role === UserRole.OPERATOR ? 'Revoke operator' : 'Make operator'}
                        </button>
                        <button
                          type="button"
                          onClick={() => onAction(user, user.status === AccountStatus.BANNED ? 'UNBAN' : 'BAN')}
                          className="rounded-md border border-slate-200 bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700 hover:bg-slate-200"
                        >
                          {user.status === AccountStatus.BANNED ? 'Unban' : 'Ban'}
                        </button>
                      </>
                    )}
                  </div>
                </td>
              </tr>
            ))}

            {users.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-16 text-center">
                  <p className="font-semibold text-slate-900">No matching accounts found</p>
                  <button type="button" onClick={onResetFilters} className="mt-3 text-xs font-semibold text-teal-700 hover:text-teal-800">
                    Clear all filters
                  </button>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="flex flex-col items-center justify-between gap-4 border-t border-slate-200 bg-slate-50/80 px-4 py-3.5 text-xs text-slate-600 sm:flex-row sm:px-6">
        <div className="flex items-center gap-3">
          <span>{totalUsers} account{totalUsers === 1 ? '' : 's'}</span>
          <label className="flex items-center gap-1.5">
            Rows:
            <select
              value={pageSize}
              onChange={(event) => onPageSizeChange(Number(event.target.value))}
              className="rounded border border-slate-200 bg-white px-2 py-1 text-xs text-slate-700"
            >
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
            </select>
          </label>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
            className="rounded-md border border-slate-200 bg-white px-3 py-1.5 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Previous
          </button>
          <span>Page {currentPage} of {totalPages}</span>
          <button
            type="button"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
            className="rounded-md border border-slate-200 bg-white px-3 py-1.5 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Next
          </button>
        </div>
      </div>
    </section>
  );
}

function SortableHeader({
  label,
  field,
  suffix,
  onSort,
}: {
  label: string;
  field: AdminUserSortField;
  suffix: string;
  onSort: (field: AdminUserSortField) => void;
}) {
  return (
    <th scope="col" className="px-4 py-3.5 first:sm:px-6">
      <button type="button" onClick={() => onSort(field)} className="hover:text-slate-900">
        {label}{suffix}
      </button>
    </th>
  );
}
