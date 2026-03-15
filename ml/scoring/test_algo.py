from datetime import datetime, timedelta

from ml.scoring.algo import ELO
from ml.scoring.types import CommitData

now = datetime.now()


# Helper to create commits with proper spacing AND per-commit ML signals
def create_commit(
    hash: str,
    days_ago: float,
    msg: str,
    additions: int,
    deletions: int,
    commit_score: float = 0.75,  # Default good message
    commit_frequency: float = 8.5,  # Default frequency
    commit_consistency: float = 0.7,  # Default consistency
) -> CommitData:
    return {
        "hash": hash,
        "timestamp": now - timedelta(days=days_ago),
        "message": msg,
        "additions": additions,
        "deletions": deletions,
        "commit_score": commit_score,
        "commit_frequency": commit_frequency,
        "commit_consistency": commit_consistency,
    }


# Based on the actual git log patterns with realistic per-commit ML signals
commits = [
    create_commit("a1", 1.0, "initial commit", 50, 0, 0.85, 5.2, 0.6),
    create_commit(
        "a2", 0.98, "added ml directory for the model", 30, 0, 0.92, 5.2, 0.6
    ),
    create_commit("a3", 0.97, "re-setup", 100, 50, 0.45, 5.2, 0.6),
    create_commit("a4", 0.96, "feat: initial commit", 200, 0, 0.88, 5.2, 0.6),
    create_commit("a5", 0.95, "feat: completed nav", 150, 20, 0.91, 5.2, 0.6),
    create_commit("a6", 0.94, "feat: footer complete", 80, 10, 0.87, 5.2, 0.6),
    create_commit(
        "a7", 0.93, "feat: scaffolded frontend route structures", 120, 0, 0.94, 5.2, 0.6
    ),
    create_commit("a8", 0.92, "run pnpm install", 5, 5, 0.75, 5.2, 0.6),
    create_commit("a9", 0.91, "feat: complete schema", 300, 0, 0.89, 5.2, 0.6),
    create_commit("b1", 0.90, "feat: completed opening page", 250, 30, 0.93, 5.2, 0.6),
    create_commit("b2", 0.89, "resolved merge conflicts", 20, 20, 0.65, 5.2, 0.6),
    create_commit("b3", 0.88, "Merge pull request #1", 0, 0, 0.5, 5.2, 0.6),
    create_commit(
        "c1", 0.5, "re-run pnpm i to add modified dependencies", 10, 5, 0.78, 12.1, 0.8
    ),
    create_commit(
        "c2", 0.48, "feat: added routers for trpc backend", 180, 0, 0.95, 12.1, 0.8
    ),
    create_commit(
        "c3", 0.47, "feat: added direct url to prisma config", 15, 5, 0.82, 12.1, 0.8
    ),
    create_commit(
        "c4", 0.46, "fix: fixed build by changing the import", 30, 20, 0.71, 12.1, 0.8
    ),
    create_commit(
        "c5",
        0.45,
        "fix: added package.json postinstall script",
        25,
        10,
        0.69,
        12.1,
        0.8,
    ),
    create_commit(
        "c6", 0.44, "fix: fixed deprecation package warning", 15, 15, 0.73, 12.1, 0.8
    ),
    create_commit(
        "c7",
        0.43,
        "fix: remove cloudflare mentions to make deploying to vercel work",
        40,
        30,
        0.84,
        12.1,
        0.8,
    ),
    create_commit(
        "c8",
        0.42,
        "fix: removed unneeded import causing lint error",
        10,
        10,
        0.77,
        12.1,
        0.8,
    ),
    create_commit(
        "c9", 0.41, "fix: add vercel.json with correct presets", 35, 0, 0.81, 12.1, 0.8
    ),
    create_commit(
        "c10",
        0.40,
        "fix: added nitro plugin to allow vercel deployment",
        45,
        5,
        0.79,
        12.1,
        0.8,
    ),
    create_commit("d1", 0.35, "setting up leaderboard page", 120, 0, 0.86, 12.1, 0.8),
    create_commit(
        "d2", 0.34, "Merge branch 'main' into leaderboard-page", 0, 0, 0.5, 12.1, 0.8
    ),
    create_commit("e1", 0.3, "scoring algo", 500, 100, 0.96, 8.5, 0.9),
    create_commit("f1", 0.28, "Merge pull request #3", 0, 0, 0.5, 6.3, 0.5),
    create_commit(
        "f2", 0.27, "feat: completed leaderboards table", 200, 50, 0.94, 6.3, 0.5
    ),
    create_commit("f3", 0.26, "feat: leaderboards completed", 180, 40, 0.92, 6.3, 0.5),
    create_commit("f4", 0.25, "Merge branch 'main'", 0, 0, 0.5, 6.3, 0.5),
    create_commit(
        "f5", 0.24, "fix: update prisma.config to use .env", 20, 10, 0.76, 6.3, 0.5
    ),
    create_commit("f6", 0.23, "Merge pull request #4", 0, 0, 0.5, 6.3, 0.5),
    create_commit("f7", 0.22, "feat: branding change", 150, 80, 0.88, 6.3, 0.5),
]

# Run calculation
elo = ELO()
result = elo.calculate(commits)

print(f"Total commits analyzed: {len(commits)}")
print(f"ELO Delta: {result['eloDelta']}")
print("\nBreakdown:")
for key, value in result["breakdown"].items():
    print(f"  {key}: {value}")

avg_score = sum(c["commit_score"] for c in commits) / len(commits)
avg_freq = sum(c["commit_frequency"] for c in commits) / len(commits)
avg_consistency = sum(c["commit_consistency"] for c in commits) / len(commits)

print(f"\nAvg commit_score: {avg_score:.2f}")
print(f"Avg commit_frequency: {avg_freq:.2f}")
print(f"Avg commit_consistency: {avg_consistency:.2f}")
