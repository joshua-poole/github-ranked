from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd
from inference import score
from rich import print as rprint
from unstable.commits import get_user_commits


def calc_commit_score(df: pd.DataFrame) -> float:
    if df.empty:
        return 0

    scores = np.atleast_1d(np.array(score(df["message"].tolist())))
    weights = np.exp(np.linspace(0, 1, len(scores)))
    weights /= weights.sum()
    return float(np.dot(weights, scores))


def calc_commit_frequency(df: pd.DataFrame, days: int) -> float:
    return len(df) / days if days > 0 else 0.0


def calc_commit_consistency(df: pd.DataFrame, min_commits: int = 2) -> float:
    if len(df) < min_commits:
        return 0.0
    timestamps = df["date"].sort_values().astype(np.int64) / 1e9
    gaps_days = np.diff(timestamps) / 86400
    cv = np.std(gaps_days) / (np.mean(gaps_days) + 1e-9)
    return float(1 / (cv + 1))


def calc_performance_vector(df: pd.DataFrame, days: int) -> dict:
    return {
        "commit_score": calc_commit_score(df),
        "commit_frequency": calc_commit_frequency(df, days),
        "commit_consistency": calc_commit_consistency(df),
    }


if __name__ == "__main__":
    users = [
        "hello-andrew-yan",
        "joshua-poole",
        "NathanTheDev",
        "imareeq",
    ]

    since = datetime.now(UTC) - timedelta(days=180)
    until = datetime.now(UTC)
    num_days = (until - since).days

    for user in users:
        df = get_user_commits(user, since, until)
        performance = calc_performance_vector(df, num_days)
        rprint(f"'{user}' performance:")
        rprint(performance)
