import logging
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from metrics.performance import calc_performance_vector
from unstable.commits import get_user_commits

LOGGER = logging.getLogger("uvicorn")


@asynccontextmanager
async def _lifespan(_: FastAPI):
    LOGGER.info("Commit quality service started. Loading model.")
    yield
    LOGGER.info("Commit quality service shutting down.")


app = FastAPI(
    title="Commit Quality Service",
    lifespan=_lifespan,
)

app.add_middleware(TrustedHostMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/commits/score", include_in_schema=True)
async def get_user_commit_score(user: str, since: datetime, until: datetime):
    since = datetime.now(UTC) - timedelta(days=180)
    until = datetime.now(UTC)
    num_days = (until - since).days

    df = get_user_commits(user, since, until)
    return calc_performance_vector(df, num_days)
