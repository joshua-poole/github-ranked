// src/lib/scoring/algorithm.ts
//
/**
 * CORTISOL METER (0 = dead, 5000 = screaming)
 *
 * Low cortisol = zen (or dead, we'll assume zen).
 *
 * Each commit spikes cortisol based on:
 * - Lines changed (more changes = more stress)
 * - Late night coding (3am = cortisol spike)
 * - Weekend work (no boundaries = chronic stress)
 * - Burstiness (erratic patterns = acute stress)
 *
 * ML provides stress signal from commit messages, which:
 * - Amplifies cortisol when message quality is poor (actual crashout)
 * - Buffers cortisol when message quality is high (passionate != stressed)
 *
 * Time decay: recent cortisol spikes matter more (1% decay per day)
 * Final score: 0-5000 (higher = more cortisol = closer to burnout)
 */

import type { CommitData, MLSignals, SpikeResult } from './types'
import { getTierFromLevel } from './tiers'

export class CortisolMeter {
  private readonly DECAY_PER_DAY = 0.99
  private readonly MAX_AGE_DAYS = 90

  calculate(commits: CommitData[], signals: MLSignals): SpikeResult {
    const now = new Date()
    let totalCortisol = 0
    let totalWeight = 0

    const sorted = [...commits].sort(
      (a, b) => a.timestamp.getTime() - b.timestamp.getTime(),
    )

    const burstiness = this.calcBurstiness(sorted)

    for (const c of commits) {
      const ageDays =
        (now.getTime() - c.timestamp.getTime()) / (1000 * 60 * 60 * 24)
      if (ageDays > this.MAX_AGE_DAYS) continue

      // Recent spikes hit harder
      const weight = Math.pow(this.DECAY_PER_DAY, ageDays)

      const spike = this.calcCortisolSpike(c, burstiness, signals.stressLevel)

      totalCortisol += spike * weight
      totalWeight += weight
    }

    // Normalize to 0-5000 scale
    let cortisol = totalWeight > 0 ? (totalCortisol / totalWeight) * 100 : 0
    cortisol = Math.min(5000, Math.max(0, Math.round(cortisol)))

    return {
      glucoseLevel: cortisol, // Keep field name for compatibility
      tier: getTierFromLevel(cortisol),
      breakdown: {
        stressContribution: Math.round(signals.stressLevel * 100),
        lateNightContribution: this.calcLateNightScore(commits),
        burstContribution: Math.round(burstiness * 100),
        messageQualityDeduction: Math.round(
          this.calcAvgMessageQuality(commits) * 100,
        ),
      },
      recommendation: this.getRecommendation(cortisol, signals),
    }
  }

  private calcCortisolSpike(
    c: CommitData,
    burstiness: number,
    stressSignal: number,
  ): number {
    let spike = 0

    // More code = more cortisol (log scale so 1000 lines isn't 10x worse)
    const changes = c.additions + c.deletions
    spike += Math.log10(changes + 1) * 10

    // Message quality modulates how stress affects cortisol
    const msgQuality = this.calcMessageQuality(c.message)

    // Stress spikes cortisol more when messages are low quality (actual crashout)
    // High quality messages = passionate coding, not stressed coding
    const stressMultiplier = this.lerp(
      0.8,
      1.5,
      stressSignal * (1 - msgQuality),
    )
    spike *= stressMultiplier

    // Late night = cortisol spike
    // NOTE: note sure if this will be accurate due to timezoen
    const hour = c.timestamp.getHours()
    const isLate = hour >= 23 || hour <= 5
    if (isLate) {
      // Peak cortisol at 3-4am
      const factor =
        hour >= 23
          ? this.lerp(0.3, 1.0, (hour - 23) / 5)
          : this.lerp(1.0, 0.5, hour / 5)
      spike += 20 * factor
    }

    // Weekend work = chronic stress
    const day = c.timestamp.getDay()
    if (day === 0 || day === 6) spike += 15

    // Erratic patterns = acute stress spikes
    spike += burstiness * 30

    return spike
  }

  private calcBurstiness(commits: CommitData[]): number {
    if (commits.length < 3) return 0

    const intervals: number[] = []
    for (let i = 1; i < commits.length; i++) {
      const diff =
        commits[i].timestamp.getTime() - commits[i - 1].timestamp.getTime()
      intervals.push(diff / (1000 * 60 * 60))
    }

    const avg = intervals.reduce((a, b) => a + b, 0) / intervals.length
    const variance =
      intervals.reduce((a, b) => a + Math.pow(b - avg, 2), 0) / intervals.length

    // Higher variance = more bursty = higher cortisol
    return Math.min(1, variance / 48)
  }

  private calcLateNightScore(commits: CommitData[]): number {
    if (commits.length === 0) return 0

    const late = commits.filter((c) => {
      const hour = c.timestamp.getHours()
      return hour >= 23 || hour <= 5
    }).length

    return Math.min(100, (late / commits.length) * 200)
  }

  private calcAvgMessageQuality(commits: CommitData[]): number {
    if (commits.length === 0) return 0

    let total = 0
    for (const c of commits) {
      total += this.calcMessageQuality(c.message)
    }
    return total / commits.length
  }

  private calcMessageQuality(msg: string): number {
    let score = 0.5

    if (msg.length > 50) score += 0.3
    else if (msg.length > 20) score += 0.2
    else if (msg.length > 10) score += 0.1

    if (/^(feat|fix|docs|style|refactor|test|chore)/i.test(msg)) {
      score += 0.2
    }

    if (msg.split(' ').length < 3) score -= 0.2

    return Math.max(0, Math.min(1, score))
  }

  private getRecommendation(cortisol: number, signals: MLSignals): string {
    return 'Funny message'
  }

  private lerp(start: number, end: number, t: number): number {
    const clamped = Math.max(0, Math.min(1, t))
    return start + (end - start) * clamped
  }
}
