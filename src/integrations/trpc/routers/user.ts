import { z } from 'zod'
import { publicProcedure } from '../init'
import { prisma } from '../../../db'
import type { TRPCRouterRecord } from '@trpc/server'
import { getUserStats } from '#/server/services/dashboard/getUserStats'
import { getUserIcon } from '#/server/services/dashboard/getUserIcon'
import { getUserRank } from '#/server/services/dashboard/getUserRank'

export const userRouter = {
  getByUsername: publicProcedure
    .input(z.object({ username: z.string().min(1) }))
    .query(({ input }) =>
      prisma.user.findUnique({
        where: { username: input.username },
        include: { badges: { include: { badge: true } } },
      }),
    ),

  getById: publicProcedure
    .input(z.object({ id: z.bigint() }))
    .query(({ input }) =>
      prisma.user.findUnique({
        where: { id: input.id },
        include: { badges: { include: { badge: true } } },
      }),
    ),

  topByElo: publicProcedure
    .input(z.object({ limit: z.number().min(1).max(100).default(10) }))
    .query(({ input }) =>
      prisma.user.findMany({
        orderBy: { elo: 'desc' },
        take: input.limit,
      }),
    ),

    // in userRouter
  compareUsers: publicProcedure
    .input(z.object({ username1: z.string().min(1), username2: z.string().min(1) }))
    .query(async ({ input }) => {
      const [stats1, stats2, icon1, icon2, rank1, rank2] = await Promise.all([
        getUserStats(input.username1),
        getUserStats(input.username2),
        getUserIcon(input.username1),
        getUserIcon(input.username2),
        getUserRank(input.username1),
        getUserRank(input.username2),
      ])

      return {
        user1: { username: input.username1, icon: icon1, rank: rank1.rank, ...stats1 },
        user2: { username: input.username2, icon: icon2, rank: rank2.rank, ...stats2 },
      }
    })
} satisfies TRPCRouterRecord
