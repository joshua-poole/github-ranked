# types.py
from datetime import datetime
from typing import NotRequired, Optional, TypedDict


class Tier(TypedDict):
    rank: str
    minElo: int
    maxElo: int
    description: str


class CommitData(TypedDict):
    hash: str  # Commit SHA
    timestamp: datetime  # Python datetime object
    message: str  # Commit message
    additions: int  # Lines added
    deletions: int  # Lines deleted
    filesChanged: int  # Number of files touched
    stressLevel: float  # 0 chill, 1 stressed (from ML)


class Breakdown(TypedDict):
    stressContribution: int
    lateNightContribution: int
    burstContribution: int
    messageQualityDeduction: int


class Result(TypedDict):
    eloDelta: int
    breakdown: Breakdown
