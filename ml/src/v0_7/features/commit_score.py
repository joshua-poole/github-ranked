from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd
from rich import print as rprint

from v0_7.core.config import ARTEFACTS_DIR
from v0_7.models.regression.pipeline import SentimentRegressionPipeline
from v0_7.unstable.github.commits import get_user_commits


def compute_stress_score(
    df: pd.DataFrame, pipeline: SentimentRegressionPipeline
) -> float:
    scores = np.array(pipeline.score(df["message"].tolist()))
    weights = np.exp(np.linspace(0, 1, len(scores)))
    weights /= weights.sum()
    return float(np.dot(weights, scores))


if __name__ == "__main__":
    pipeline = SentimentRegressionPipeline()
    pipeline.load_model(model_path=ARTEFACTS_DIR / "20260314_235008.pkl")

    users = [
        "joshua-poole",
        "NathanTheDev",
    ]

    since = datetime.now(UTC) - timedelta(days=180)
    until = datetime.now(UTC)

    for user in users:
        df = get_user_commits(user, since, until)
        score = compute_stress_score(df, pipeline)
        rprint(f"'{user}' commit_score: {score:.4}")
