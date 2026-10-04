import type { AdminUser, AdminUserAction } from '@/features/admin-user/admin-user.types';

const actionLabels: Record<AdminUserAction, string> = {
  BAN: 'Ban account',
  UNBAN: 'Unban account',
  MAKE_OPERATOR: 'Make operator',
  REVOKE_OPERATOR: 'Revoke operator',
};

export function AdminUserActionModal({
  user,
  action,
  onCancel,
  onConfirm,
}: {
  user: AdminUser | null;
  action: AdminUserAction | null;
  onCancel: () => void;
  onConfirm: () => void;
}) {
  if (!user || !action) return null;

  return (
    <div className="fixed inset-0 z-60 flex items-center justify-center bg-slate-900/60 p-4" role="dialog" aria-modal="true" aria-labelledby="action-title">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white shadow-2xl">
        <div className="p-6">
          <h2 id="action-title" className="text-base font-bold text-slate-900">{actionLabels[action]}?</h2>
          <p className="mt-2 text-sm text-slate-600">
            Apply this change to <strong>{user.full_name ?? user.email}</strong>?
          </p>
        </div>
        <div className="flex justify-end gap-3 border-t border-slate-200 bg-slate-50 px-6 py-4">
          <button type="button" onClick={onCancel} className="rounded-lg border border-slate-300 bg-white px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-100">Cancel</button>
          <button type="button" onClick={onConfirm} className="rounded-lg bg-teal-600 px-4 py-2 text-xs font-semibold text-white hover:bg-teal-700">Confirm</button>
        </div>
      </div>
    </div>
  );
}
