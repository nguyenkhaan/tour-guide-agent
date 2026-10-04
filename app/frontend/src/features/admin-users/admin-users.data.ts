//Chi dung de thuc hien mock data 
import { AccountStatus, UserRole, type AdminUser } from '@/features/admin-users/admin-users.types';

export const INITIAL_ADMIN_USERS: AdminUser[] = [
  {
    id: 'usr_01HGB89A21',
    email: 'sarah.jenkins@gmail.com',
    full_name: 'Sarah Jenkins',
    role: UserRole.USER,
    status: AccountStatus.ACTIVE,
    created_at: '2026-09-14T00:00:00Z',
    updated_at: '2026-09-14T00:00:00Z',
  },
  {
    id: 'usr_01HGB89A22',
    email: 'linh.ops@tourguide.com',
    full_name: 'Linh Nguyen',
    role: UserRole.OPERATOR,
    status: AccountStatus.ACTIVE,
    created_at: '2026-07-01T00:00:00Z',
    updated_at: '2026-07-01T00:00:00Z',
  },
  {
    id: 'usr_01HGB89A23',
    email: 'spammer99@badmail.io',
    full_name: 'Crypto Bot Promo',
    role: UserRole.USER,
    status: AccountStatus.BANNED,
    created_at: '2026-09-28T00:00:00Z',
    updated_at: '2026-09-28T00:00:00Z',
  },
  {
    id: 'usr_01HGB89A24',
    email: 'alex.chen@tourguide.com',
    full_name: 'Alex Chen',
    role: UserRole.ADMIN,
    status: AccountStatus.ACTIVE,
    created_at: '2026-01-10T00:00:00Z',
    updated_at: '2026-01-10T00:00:00Z',
  },
  {
    id: 'usr_01HGB89A25',
    email: 'marcus.vance@tourguide.com',
    full_name: 'Marcus Vance',
    role: UserRole.OPERATOR,
    status: AccountStatus.ACTIVE,
    created_at: '2026-05-18T00:00:00Z',
    updated_at: '2026-05-18T00:00:00Z',
  },
  {
    id: 'usr_01HGB89A26',
    email: 'emma.stone@outlook.com',
    full_name: 'Emma Watson',
    role: UserRole.USER,
    status: AccountStatus.DISABLED,
    created_at: '2026-08-04T00:00:00Z',
    updated_at: '2026-08-04T00:00:00Z',
  },
];
