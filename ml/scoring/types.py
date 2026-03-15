# types.py
from datetime import datetime
from typing import TypedDict


class CommitData(TypedDict):
    hash: str  # Commit SHA
    timestamp: datetime  # Python datetime object
    message: str  # Commit message
    additions: int  # Lines added
    deletions: int  # Lines deleted
    commit_score: float  # ML
    commit_frequency: float  # ML
    commit_consistency: float  # ML


class Breakdown(TypedDict):
    lateNightContribution: int
    burstContribution: int
    messageQualityDeduction: int
    frequencyContribution: int
    consistencyContribution: int


class Result(TypedDict):
    eloDelta: int
    breakdown: Breakdown
