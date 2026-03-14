import { useQuery } from '@tanstack/react-query'
import { useTRPC } from '#/integrations/trpc/react'
import { Card, CardContent } from '#/components/ui/card'
import type { Rank } from '#/server/services/dashboard/getUserRank'

interface UserRankProps {
  username: string
}

const RANK_LABELS: Record<Rank, string> = {
  UNRANKED: 'Unranked',
  PLASTIC: 'Plastic',
  BRONZE: 'Bronze',
  SILVER: 'Silver',
  GOLD: 'Gold',
  PLATINUM: 'Platinum',
  DIAMOND: 'Diamond',
  LINUS: 'Linus',
}

const RANK_IMAGE: Record<Rank, string> = {
  UNRANKED: '/ranks/unranked.png',
  PLASTIC: '/ranks/plastic.png',
  BRONZE: '/ranks/bronze.png',
  SILVER: '/ranks/silver.png',
  GOLD: '/ranks/gold.png',
  PLATINUM: '/ranks/platinum.png',
  DIAMOND: '/ranks/diamond.png',
  LINUS: '/ranks/linus.png',
}

export function UserRank({ username }: UserRankProps) {
  const trpc = useTRPC()
  const { data, isLoading, isError } = useQuery(
    trpc.dashboard.getUserRank.queryOptions({ username }),
  )

  if (isLoading)
    return (
      <Card className="border-[var(--line)] bg-[var(--surface)]">
        <CardContent className="flex items-center gap-4 py-4">
          <div className="w-16 h-16 rounded-full bg-[var(--line)] animate-pulse" />
          <div className="h-6 w-24 rounded bg-[var(--line)] animate-pulse" />
        </CardContent>
      </Card>
    )

  if (isError)
    return <p className="text-sm text-destructive">Failed to load rank.</p>
  if (!data) return null

  const rank = data.rank as Rank

  return (
    <Card className="border-[var(--line)] bg-[var(--surface)]">
      <CardContent className="flex items-center gap-4 py-4">
        <img
          src={RANK_IMAGE[rank]}
          alt={RANK_LABELS[rank]}
          className="w-16 h-16 object-contain"
        />
        <div>
          <p className="text-xs text-[var(--sea-ink-soft)] uppercase tracking-wide font-medium">
            Rank
          </p>
          <p className="text-2xl font-bold text-[var(--sea-ink)]">
            {RANK_LABELS[rank]}
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
