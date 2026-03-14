# test_algo.py
from datetime import datetime, timedelta

from ml.scoring.algo import ELO
from ml.scoring.types import CommitData

now = datetime.now()

commit1: CommitData = {
    "hash": "abc123",
    "timestamp": now - timedelta(days=1),
    "message": "feat: add new feature with proper description and everything",
    "additions": 150,
    "deletions": 30,
    "filesChanged": 5,
    "stressLevel": 0.3,
}

commit2: CommitData = {
    "hash": "def456",
    "timestamp": now - timedelta(hours=2),
    "message": "fix bug",
    "additions": 5,
    "deletions": 2,
    "filesChanged": 1,
    "stressLevel": 0.0,
}

commit3: CommitData = {
    "hash": "ghi789",
    "timestamp": now - timedelta(hours=5),
    "message": "wip",
    "additions": 200,
    "deletions": 0,
    "filesChanged": 3,
    "stressLevel": 1,
}

commits: list[CommitData] = [commit1, commit2, commit3]


elo = ELO()
result = elo.calculate(commits)

print(f"Elo : {result['eloDelta']}")
