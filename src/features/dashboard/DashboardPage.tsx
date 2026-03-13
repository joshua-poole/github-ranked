// DashboardPage.tsx
import { useQuery } from '@tanstack/react-query'
import { useTRPC } from '#/integrations/trpc/react'
import { UserMetrics } from './components/UserMetrics'
import { UserRanking } from './components/UserRanking'
import { useParams } from '@tanstack/react-router'

export function DashboardPage() {
  const { username } = useParams({ from: '/dashboard/$username' })
  const trpc = useTRPC()
  const { data, isLoading } = useQuery(
    trpc.dashboard.getDashboardData.queryOptions({ username }),
  )

  if (isLoading) return <div>Loading...</div>
  return (
    <div className="space-y-4 p-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <UserMetrics metrics={data?.stats} />
      <UserRanking data={data} />
    </div>
  )
}
