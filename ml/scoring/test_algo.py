# test_algo.py
from datetime import datetime, timedelta

from ml.scoring.algo import ELO
from ml.scoring.types import CommitData, MLSignals

now = datetime.now()

commit1: CommitData = {
    "hash": "abc123",
    "timestamp": now - timedelta(days=1),
    "message": "feat: add new feature with proper description and everything",
    "additions": 150,
    "deletions": 30,
    "filesChanged": 5,
}

commit2: CommitData = {
    "hash": "def456",
    "timestamp": now - timedelta(hours=2),
    "message": "fix bug",
    "additions": 5,
    "deletions": 2,
    "filesChanged": 1,
}

commit3: CommitData = {
    "hash": "ghi789",
    "timestamp": now - timedelta(hours=5),
    "message": "wip",
    "additions": 200,
    "deletions": 0,
    "filesChanged": 3,
}

commits: list[CommitData] = [commit1, commit2, commit3]

signals: MLSignals = {"stressLevel": 0.3}

elo = ELO()
result = elo.calculate(commits, signals)

print(f"Elo : {result['eloDelta']}")
print("\nBreakdown:")
for key, value in result["breakdown"].items():
    print(f"  {key}: {value}")
print(f"\nRecommendation: {result['recommendation']}")
