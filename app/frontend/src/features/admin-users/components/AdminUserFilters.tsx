import {
  AccountStatus,
  UserRole,
  type AdminUserRoleFilter,
  type AdminUserStatusFilter,
} from '../admin-users.types';

export function AdminUserFilters({
  searchQuery,
  selectedRole,
  selectedStatus,
  onSearchChange,
  onRoleChange,
  onStatusChange,
  onReset,
}: {
  searchQuery: string;
  selectedRole: AdminUserRoleFilter;
  selectedStatus: AdminUserStatusFilter;
  onSearchChange: (value: string) => void;
  onRoleChange: (value: AdminUserRoleFilter) => void;
  onStatusChange: (value: AdminUserStatusFilter) => void;
  onReset: () => void;
}) {
  const hasFilters = searchQuery !== '' || selectedRole !== 'ALL' || selectedStatus !== 'ALL';

  return (
    <section className="mb-6 rounded-xl border border-slate-200/80 bg-white p-4 shadow-xs">
      <div className="flex flex-col items-stretch justify-between gap-3 md:flex-row md:items-center">
        <label className="flex-1">
          <span className="sr-only">Search accounts</span>
          <input
            type="search"
            value={searchQuery}
            onChange={(event) => onSearchChange(event.target.value)}
            placeholder="Search by name, email, or account ID..."
            className="w-full rounded-lg border border-slate-200 bg-slate-50 px-3.5 py-2 text-sm focus:bg-white focus:outline-none focus:ring-2 focus:ring-teal-500"
          />
        </label>

        <div className="flex flex-wrap items-center gap-3">
          <label className="flex items-center gap-1.5 text-xs font-medium text-slate-600">
            Role:
            <select
              value={selectedRole}
              onChange={(event) => onRoleChange(event.target.value as AdminUserRoleFilter)}
              className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="ALL">All roles</option>
              {Object.values(UserRole).map((role) => (
                <option key={role} value={role}>{role}</option>
              ))}
            </select>
          </label>

          <label className="flex items-center gap-1.5 text-xs font-medium text-slate-600">
            Status:
            <select
              value={selectedStatus}
              onChange={(event) => onStatusChange(event.target.value as AdminUserStatusFilter)}
              className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-2 text-xs text-slate-800 focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="ALL">All statuses</option>
              {Object.values(AccountStatus).map((status) => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </label>

          {hasFilters && (
            <button
              type="button"
              onClick={onReset}
              className="rounded-lg bg-slate-100 px-3 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-200"
            >
              Reset filters
            </button>
          )}
        </div>
      </div>
    </section>
  );
}
