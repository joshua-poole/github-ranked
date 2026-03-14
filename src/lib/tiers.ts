// src/lib/scoring/tiers.ts

export interface Tier {
  name: string
  rank: string // Maps to their DB enum
  minElo: number
  maxElo: number
}

export const TIERS: Tier[] = [
  {
    name: 'Zen Master',
    rank: 'PLASTIC',
    minElo: 0,
    maxElo: 500,
  },
  {
    name: 'Mildly Caffeinated',
    rank: 'BRONZE',
    minElo: 501,
    maxElo: 1500,
  },
  {
    name: 'Commit Addict',
    rank: 'SILVER',
    minElo: 1501,
    maxElo: 2500,
  },
  {
    name: 'Chronically Online',
    rank: 'GOLD',
    minElo: 2501,
    maxElo: 3500,
  },
  {
    name: 'MAXIMUM BURNOUT',
    rank: 'DIAMOND',
    minElo: 3501,
    maxElo: 4500,
  },
  {
    name: 'Linus Torvalds Mode',
    rank: 'LINUS',
    minElo: 4501,
    maxElo: 5000,
  },
]

export function getTierFromLevel(level: number): Tier {
  return TIERS.find((t) => level >= t.minElo && level <= t.maxElo) || TIERS[0]
}

export function getRankFromLevel(level: number): string {
  return getTierFromLevel(level).rank
}
