import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

import { useTRPC } from '#/integrations/trpc/react'
import { useQuery } from '@tanstack/react-query'

export default function Compare({
  user1,
  user2,
}: {
  user1: string
  user2: string
}) {
  const trpc = useTRPC()

  const { data } = useQuery({
    ...trpc.user.compareUsers.queryOptions({
      username1: user1,
      username2: user2,
    }),
    networkMode: 'always',
    enabled: !!user1 && !!user2,
  })

  if (!data) return null

  const users = [data.user1, data.user2]

  return (
    <main className="flex flex-row gap-2">
      {users.map((user) => (
        <Card key={user.username} className="w-96">
          <CardHeader>
            <img src={user.icon} className="w-12 h-12 rounded-full mb-2" />
            <CardTitle className="text-2xl">{user.username}</CardTitle>
          </CardHeader>
          <CardContent className="text-base">
            <div className="flex justify-between items-center py-1">
              <span>Repos</span>
              <span>{user.publicRepos}</span>
            </div>
            <hr className="my-2" />
            <div className="flex justify-between items-center py-1">
              <span>Commits</span>
              <span>{user.commits}</span>
            </div>
            <hr className="my-2" />
            <div className="flex justify-between items-center py-1">
              <span>Followers</span>
              <span>{user.followers}</span>
            </div>
            <hr className="my-2" />
            <div className="flex justify-between items-center py-1">
              <span>Stars</span>
              <span>{user.totalStars}</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </main>
  )
}
