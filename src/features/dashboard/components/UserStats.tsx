import { useQuery } from '@tanstack/react-query'
import { useTRPC } from '#/integrations/trpc/react'
import type { UserStats } from '../types'

interface UserStatsProps {
  username: string
}

export function UserStats({ username }: UserStatsProps) {
  const trpc = useTRPC()
  const { data, isLoading, isError } = useQuery(
    trpc.dashboard.getUserStats.queryOptions({ username }),
  )

  if (isLoading) return <div>Loading stats...</div>
  if (isError) return <div>Failed to load stats.</div>
  if (!data) return null

  return (
    <div>
      <p>Public Repos: {data.publicRepos}</p>
      <p>Followers: {data.followers}</p>
      <p>Following: {data.following}</p>
      <p>Total Stars: {data.totalStars}</p>
      <p>Total Forks: {data.totalForks}</p>
      <p>Top Language: {data.topLanguage ?? 'N/A'}</p>
      <p>
        Most Starred Repo:{' '}
        {data.mostStarredRepo
          ? `${data.mostStarredRepo.name} (${data.mostStarredRepo.stars} ⭐)`
          : 'N/A'}
      </p>
      <p>Member Since: {new Date(data.accountCreatedAt).getFullYear()}</p>
      {data.bio && <p>Bio: {data.bio}</p>}
      {data.location && <p>Location: {data.location}</p>}
      {data.company && <p>Company: {data.company}</p>}
      {data.website && (
        <p>
          Website:{' '}
          <a href={data.website} target="_blank" rel="noreferrer">
            {data.website}
          </a>
        </p>
      )}
    </div>
  )
}
