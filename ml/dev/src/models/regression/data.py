import json
import random
from pathlib import Path
from typing import NamedTuple

import numpy as np
import polars as pl
import torch
from core.config import ARTEFACTS_DIR, DATA_DIR
from core.utils import timestamp
from models.transformer.build import embed, load_session
from rich import print as rprint

DATASET_PATH = DATA_DIR / "dhruvildave_github-commit-messages-dataset.csv"
SIGNALS_PATH = DATA_DIR / "signals.json"
TRUNCATE_SIZE = 100

SESSION, TOKENIZER = load_session()


class SplitSignals(NamedTuple):
    pos_train: list[str]
    pos_test: list[str]
    neg_train: list[str]
    neg_test: list[str]


def _create_embeddings_file(output: Path | None = None):
    df = (
        pl.scan_csv(DATASET_PATH)
        .select(pl.col("message").fill_null("").str.slice(0, TRUNCATE_SIZE))
        .collect()
    )
    messages = df["message"].to_list()
    rprint(f"[bold green]Dataset Row Count:[/bold green] {len(messages):,}")

    embs = embed(messages, SESSION, TOKENIZER)
    if output is None:
        output = ARTEFACTS_DIR / f"{timestamp()}_embeddings.npy"

    np.save(output, embs)
    rprint(f"[bold green]Saved embeddings to[/bold green] '{output}'")
    return embs


def encode(messages: str | list[str]) -> np.ndarray:
    if isinstance(messages, str):
        messages = [messages]

    messages = [m[:TRUNCATE_SIZE] for m in messages]
    return embed(messages, SESSION, TOKENIZER)


def load_raw_embs(embs_path: Path) -> np.ndarray:
    if not embs_path.exists():
        rprint("[bold green]Creating new embeddings file[/bold green]")
        return _create_embeddings_file(output=embs_path)

    rprint(f"[bold green]Loading cached embeddings from[/bold green] '{embs_path}'")

    # Legacy: embeddings saved as .pt files via PyTorch. Post-refactor uses ONNX
    # CPU-only inference with numpy. Load .pt files via torch for backward
    # compatibility only.
    if embs_path.suffix == ".pt":
        return torch.load(embs_path, map_location="cpu", weights_only=True).numpy()

    return np.load(embs_path)


def load_split_signals(seed: int = 42, split_ratio: float = 0.7) -> SplitSignals:
    signals = json.loads(SIGNALS_PATH.read_text())
    pos_signals = [
        msg for source in signals.get("positive", []) for msg in signals.get(source, [])
    ]
    neg_signals = [
        msg for source in signals.get("negative", []) for msg in signals.get(source, [])
    ]

    rng = random.Random(seed)
    rng.shuffle(pos_signals)
    rng.shuffle(neg_signals)

    pos_idx = int(len(pos_signals) * split_ratio)
    neg_idx = int(len(neg_signals) * split_ratio)

    return SplitSignals(
        pos_signals[:pos_idx],
        pos_signals[pos_idx:],
        neg_signals[:neg_idx],
        neg_signals[neg_idx:],
    )


if __name__ == "__main__":
    load_raw_embs(embs_path=ARTEFACTS_DIR / "20260314_221349_embeddings.pt")
