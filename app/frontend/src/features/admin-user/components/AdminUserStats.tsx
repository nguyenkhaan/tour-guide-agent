import { AccountStatus, UserRole, type AdminUser } from '@/features/admin-user/admin-user.types';

export function AdminUserStats({ users }: { users: AdminUser[] }) {
  const cards = [
    { label: 'Total accounts', value: users.length, className: 'text-slate-900' },
    {
      label: 'Active accounts',
      value: users.filter((user) => user.status === AccountStatus.ACTIVE).length,
      className: 'text-emerald-700',
    },
    {
      label: 'Operators',
      value: users.filter((user) => user.role === UserRole.OPERATOR).length,
      className: 'text-amber-700',
    },
    {
      label: 'Banned accounts',
      value: users.filter((user) => user.status === AccountStatus.BANNED).length,
      className: 'text-rose-700',
    },
  ];

  return (
    <section className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4" aria-label="Account metrics">
      {cards.map((card) => (
        <article key={card.label} className="rounded-xl border border-slate-200/80 bg-white p-5 shadow-xs">
          <p className="text-xs font-medium text-slate-500">{card.label}</p>
          <p className={`mt-3 text-2xl font-bold ${card.className}`}>{card.value}</p>
        </article>
      ))}
    </section>
  );
}
