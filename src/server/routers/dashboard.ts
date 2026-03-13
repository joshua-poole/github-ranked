import { z } from 'zod'
import { createTRPCRouter, publicProcedure } from '@/integrations/trpc/init'
import { TRPCError } from '@trpc/server'
import { getUserIcon } from '../services/dashboard/getUserIcon'
import { getUserStats } from '../services/dashboard/getUserStats'

export const dashboardRouter = createTRPCRouter({
  searchUser: publicProcedure
    .input(z.object({ username: z.string().min(1) }))
    .query(async ({ input }) => {
      const res = await fetch(
        `https://api.github.com/users/${input.username}`,
        {
          headers: {
            Accept: 'application/vnd.github+json',
            'User-Agent': 'github-ranked-app',
            ...(process.env.GITHUB_TOKEN && {
              Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
            }),
          },
        },
      )

      if (res.status === 404) {
        throw new TRPCError({
          code: 'NOT_FOUND',
          message: `GitHub user "${input.username}" not found`,
        })
      }

      if (!res.ok) {
        throw new TRPCError({
          code: 'INTERNAL_SERVER_ERROR',
          message: 'GitHub API error',
        })
      }

      const user = await res.json()
      return { login: user.login as string }
    }),

  getUserStats: publicProcedure
    .input(z.object({ username: z.string().min(1) }))
    .query(async ({ input }) => {
      const stats = await getUserStats(input.username)
      return stats
    }),

  getUserIcon: publicProcedure
    .input(z.object({ username: z.string().min(1) }))
    .query(async ({ input }) => {
      const avatarUrl = await getUserIcon(input.username)
      return avatarUrl
    }),
})
