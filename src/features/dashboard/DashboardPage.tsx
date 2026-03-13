// DashboardPage.tsx
import { useParams } from '@tanstack/react-router'
import { UserIcon } from './components/UserIcon'
import { UserStats } from './components/UserStats'

export function DashboardPage() {
  const { username } = useParams({ from: '/dashboard/$username' })
  return (
    <div className="space-y-4 p-4">
      <UserIcon username={username} />
      <h1 className="text-2xl font-bold">{username}</h1>

      <UserStats username={username} />
    </div>
  )
}
