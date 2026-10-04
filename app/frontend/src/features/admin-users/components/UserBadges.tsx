import { AccountStatus, UserRole } from '@/features/admin-users/admin-users.types';

const badgeClass = 'inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold';

export function RoleBadge({ role }: { role: UserRole | null }) {
  const styles = {
    [UserRole.ADMIN]: 'border-purple-200 bg-purple-50 text-purple-700',
    [UserRole.OPERATOR]: 'border-amber-200 bg-amber-50 text-amber-800',
    [UserRole.USER]: 'border-sky-200 bg-sky-50 text-sky-800',
  };

  if (!role) return <span className={`${badgeClass} border-slate-200 bg-slate-50 text-slate-500`}>—</span>;

  return <span className={`${badgeClass} ${styles[role]}`}>{role}</span>;
}

export function StatusBadge({ status }: { status: AccountStatus | null }) {
  const styles = {
    [AccountStatus.ACTIVE]: 'border-emerald-200 bg-emerald-50 text-emerald-700',
    [AccountStatus.BANNED]: 'border-rose-200 bg-rose-50 text-rose-700',
    [AccountStatus.DISABLED]: 'border-slate-300 bg-slate-100 text-slate-700',
  };

  if (!status) return <span className={`${badgeClass} border-slate-200 bg-slate-50 text-slate-500`}>—</span>;

  return <span className={`${badgeClass} ${styles[status]}`}>{status}</span>;
}
