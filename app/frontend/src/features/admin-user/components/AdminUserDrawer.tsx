import { AccountStatus, UserRole, type AdminUser, type AdminUserAction } from '@/features/admin-user/admin-user.types';
import { RoleBadge, StatusBadge } from '@/features/admin-user/components/UserBadges';

const formatDate = (value: string) =>
  new Intl.DateTimeFormat('en-US', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value));

export function AdminUserDrawer({
  user,
  onClose,
  onAction,
}: {
  user: AdminUser | null;
  onClose: () => void;
  onAction: (user: AdminUser, action: AdminUserAction) => void;
}) {
  if (!user) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden" role="dialog" aria-modal="true" aria-labelledby="user-detail-title">
      <button type="button" onClick={onClose} className="fixed inset-0 bg-slate-900/50" aria-label="Close user details" />
      <aside className="fixed inset-y-0 right-0 flex w-full max-w-md flex-col border-l border-slate-200 bg-white shadow-2xl">
        <div className="flex items-start justify-between border-b border-slate-200 bg-slate-50 p-6">
          <div>
            <div className="mb-2 flex gap-2">
              <RoleBadge role={user.role} />
              <StatusBadge status={user.status} />
            </div>
            <h2 id="user-detail-title" className="text-xl font-bold text-slate-900">{user.full_name ?? 'Unnamed user'}</h2>
            <p className="mt-0.5 text-xs text-slate-500">{user.email}</p>
          </div>
          <button type="button" onClick={onClose} className="rounded-lg p-2 text-slate-500 hover:bg-slate-200" aria-label="Close user details">✕</button>
        </div>

        <dl className="grid grid-cols-1 gap-4 overflow-y-auto p-6 sm:grid-cols-2">
          <Detail label="Email" value={user.email} />
          <Detail label="Full name" value={user.full_name ?? '—'} />
          <Detail label="Role" value={user.role ?? '—'} />
          <Detail label="Status" value={user.status ?? '—'} />
          <Detail label="Created at" value={formatDate(user.created_at)} />
          <Detail label="Updated at" value={formatDate(user.updated_at)} />
        </dl>

        <div className="mt-auto space-y-2 border-t border-slate-200 bg-slate-50 p-4">
          {user.role !== UserRole.ADMIN && (
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => onAction(user, user.role === UserRole.OPERATOR ? 'REVOKE_OPERATOR' : 'MAKE_OPERATOR')}
                className="flex-1 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs font-semibold text-amber-800 hover:bg-amber-100"
              >
                {user.role === UserRole.OPERATOR ? 'Revoke operator' : 'Make operator'}
              </button>
              <button
                type="button"
                onClick={() => onAction(user, user.status === AccountStatus.BANNED ? 'UNBAN' : 'BAN')}
                className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100"
              >
                {user.status === AccountStatus.BANNED ? 'Unban account' : 'Ban account'}
              </button>
            </div>
          )}
          <button type="button" onClick={onClose} className="w-full rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-100">
            Close details
          </button>
        </div>
      </aside>
    </div>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-200/60 bg-slate-50 p-3">
      <dt className="text-xs text-slate-400">{label}</dt>
      <dd className="mt-1 break-words text-sm font-medium text-slate-800">{value}</dd>
    </div>
  );
}
