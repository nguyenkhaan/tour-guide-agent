export function AdminUsersHeader({
  isRefreshing,
  onRefresh,
}: {
  isRefreshing: boolean;
  onRefresh: () => void;
}) {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200/80 bg-white/95 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-600 font-bold text-white">
            TG
          </div>
          <div>
            <span className="rounded bg-teal-50 px-2 py-0.5 text-xs font-semibold uppercase tracking-wider text-teal-700">
              Admin Portal
            </span>
            <h1 className="text-base font-bold leading-tight text-slate-900">
              User Accounts &amp; Role Management
            </h1>
          </div>
        </div>

        <button
          type="button"
          onClick={onRefresh}
          disabled={isRefreshing}
          className="rounded-lg bg-slate-100 px-3 py-2 text-xs font-medium text-slate-700 transition-colors hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isRefreshing ? 'Reloading...' : 'Reload data'}
        </button>
      </div>
    </header>
  );
}
