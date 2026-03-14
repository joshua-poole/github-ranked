export interface Tier {
  name: string
  emoji?: string
  color?: string
  description?: string
  warning?: string
}

export const TIERS = [
  { name: 'Zen Master' },
  { name: 'Mildly Caffeinated' },
  { name: 'Commit Addict' },
  { name: 'Chronically Online' },
  { name: 'MAXIMUM BURNOUT' },
]

export function getTierFromLevel(level: number): Tier {
  if (level < 500) return TIERS[0] // Zen Master
  if (level < 1500) return TIERS[1] // Mildly Caffeinated
  if (level < 2500) return TIERS[2] // Commit Addict
  if (level < 4000) return TIERS[3] // Chronically Online
  return TIERS[4]
}
