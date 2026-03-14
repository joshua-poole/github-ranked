# GitHub Ranked: Comprehensive Scoring Guide

## Elo (0-5000)

| Score Range | Tier | Rank | Description |
|------------|------|------|-------------|
| 0-500 | Zen Master | PLASTIC | Perfectly balanced, healthy work patterns |
| 501-1500 | Mildly Caffeinated | BRONZE | Slight intensity, still sustainable |
| 1501-2500 | Commit Addict | SILVER | Regularly engaged, watch your pace |
| 2501-3500 | Chronically Online | GOLD | High intensity, burnout risk elevated |
| 3501-4500 | MAXIMUM BURNOUT | DIAMOND | Critical levels, need immediate break |
| 4501-5000 | Linus Torvalds Mode | LINUS | Legendary intensity, please sleep |

---

## Point Calculation Breakdown

### Base Score: Log-Scaled Commit Size

| Lines Changed (additions+deletions) | Base Points |
|-------------------------------------|-------------|
| 0-9 | 0-8 |
| 10-99 | 8-16 |
| 100-999 | 16-24 |
| 1000-9999 | 24-32 |
| 10000+ | 32-40 |

Formula: `log10(changes + 1) * 8`

---

### Stress Multiplier (0.85x - 1.35x)

| Stress Signal | Message Quality | Multiplier |
|---------------|-----------------|------------|
| 0.0 (chill) | 1.0 (perfect) | 0.85x |
| 0.3 | 0.7 | ~1.0x |
| 0.7 | 0.3 | ~1.2x |
| 1.0 (stressed) | 0.0 (terrible) | 1.35x |

Formula: `lerp(0.85, 1.35, stressSignal * (1 - msgQuality))`

---

### Late Night Penalties (0 to +10)

| Time | Penalty Factor | Added Points |
|------|----------------|--------------|
| 10am-10pm | 0 | 0 |
| 11pm | 0.4 | 4 |
| 12am | 0.6 | 6 |
| 1am | 0.8 | 8 |
| 2am-4am | 1.0 | 10 |
| 5am | 0.6 | 6 |

---

### Weekend Penalty

| Day | Penalty |
|-----|---------|
| Monday-Friday | 0 |
| Saturday | +8 |
| Sunday | +8 |

---

### Burstiness Penalty (0-15 points)

| Coefficient of Variation | Interpretation | Added Points |
|--------------------------|----------------|--------------|
| 0-0.2 | Regular, sustainable pace | 0-3 |
| 0.2-0.4 | Slightly erratic | 3-6 |
| 0.4-0.6 | Irregular pattern | 6-9 |
| 0.6-0.8 | Chaotic bursts | 9-12 |
| 0.8-1.0 | Extreme inconsistency | 12-15 |

Formula: `burstiness * 15`

---

## Message Quality Scoring

| Quality Factor | Condition | Score Adjustment |
|----------------|-----------|------------------|
| Base | All messages | 0.5 |
| Length > 50 chars | Descriptive | +0.3 |
| Length > 20 chars | Good length | +0.2 |
| Length > 10 chars | Minimum | +0.1 |
| Conventional prefix | feat/fix/docs/etc | +0.2 |
| < 3 words | Too short | -0.2 |

Final Range: 0.0 (terrible) -> 1.0 (perfect)

---

## Time Decay (90-day window)

| Commit Age | Weight Multiplier |
|------------|-------------------|
| Today | 1.0x |
| 7 days ago | 0.93x |
| 30 days ago | 0.74x |
| 60 days ago | 0.55x |
| 90 days ago | 0.40x |
| >90 days | 0x (ignored) |

Formula: `0.99 ^ daysOld`

---

## Example Calculations

### Scenario A: Healthy Developer
- 10 commits over 5 days
- All between 9am-5pm
- Good messages (feat/fix with descriptions)
- Consistent pacing

Result: ~200-400 -> Zen Master

### Scenario B: Crunch Mode
- 30 commits in 48 hours
- Many at 2-4am
- Rushed messages ("fix", "wip", "update")
- Erratic bursts

Result: ~3000-4000 -> Chronically Online

### Scenario C: Weekend Warrior
- Open source maintainer
- Regular weekday work + weekend contributions
- Good messages, consistent pace
- Some late nights

Result: ~1500-2500 -> Commit Addict

---

## Breakdown Components

| Component | Range | What It Measures |
|-----------|-------|-------------------|
| stressContribution | 0-100 | Input signal + msg quality interaction |
| lateNightContribution | 0-100 | Percentage of commits outside 10pm-6am |
| burstContribution | 0-100 | Irregularity of commit timing |
| messageQualityDeduction | 0-100 | Poor commit messages (inverted) |

---

## Interpretation Guide

| Score | What It Means | Recommendation |
|-------|---------------|----------------|
| 0-500 | Balanced, sustainable | Keep doing what you're doing |
| 500-1500 | Slightly elevated | Check your work-life balance |
| 1500-2500 | Moderately intense | Take regular breaks |
| 2500-3500 | High intensity | Consider a day off |
| 3500-4500 | Critical | Seriously, take a break |
| 4500-5000 | Emergency | Step away from the keyboard |

---

High scores just mean you're dedicated - too much love for the game.

