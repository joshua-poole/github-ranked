// types.ts

import type { Tier } from './tiers'

export interface CommitData {
  hash: string
  timestamp: Date
  message: string
  additions: number
  deletions: number
  filesChanged: number
}

export interface MLSignals {
  stressLevel: number
}

export interface SpikeResult {
  glucoseLevel: number
  tier: Tier
  breakdown: {
    stressContribution: number
    lateNightContribution: number
    burstContribution: number
    messageQualityDeduction: number
  }
  recommendation: string
}
