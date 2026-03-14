import json
import random
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
ARTEFACTS_DIR = Path(__file__).resolve().parents[2] / "artefacts"

DATASET_PATH = DATA_DIR / "dhruvildave_github-commit-messages-dataset.csv"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=DEVICE)

SPLIT_RATIO = 0.7


def load_embeddings(
    chunk_size: int,
    export_path: Path | None = None,
    total_rows: int | None = None,
    batch_size: int = 1024,
) -> torch.Tensor:
    if export_path is None:
        export_path = ARTEFACTS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pt"

    if export_path.exists():
        print("Loading cached embeddings")
        return torch.load(export_path, map_location=DEVICE)

    print("Computing embeddings")
    total_chunks = (total_rows // chunk_size) if total_rows is not None else None
    chunks = []
    for chunk in tqdm(
        pd.read_csv(DATASET_PATH, chunksize=chunk_size, usecols=["message"]),
        total=total_chunks,
    ):
        msgs = (
            chunk["message"]
            .fillna("")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str[:100]
            .tolist()
        )
        if not msgs:
            continue
        with torch.no_grad():
            chunks.append(
                MODEL.encode(
                    msgs,
                    normalize_embeddings=True,
                    batch_size=batch_size,
                    show_progress_bar=False,
                    convert_to_tensor=True,
                ).cpu()
            )
    embs = torch.cat(chunks)
    torch.save(embs, export_path)
    return embs.to(DEVICE)


def load_messages(
    export_path: Path | None = None,
) -> np.ndarray:
    if export_path is None:
        export_path = ARTEFACTS_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.npy"

    if export_path.exists():
        print("Loading cached messages")
        return np.load(export_path, allow_pickle=True)

    print("Computing messages")
    msgs = (
        pd.read_csv(DATASET_PATH, usecols=["message"])["message"]
        .fillna("")
        .str.strip()
        .to_numpy(dtype=object)
    )
    np.save(export_path, msgs)
    return msgs


@lru_cache(maxsize=1)
def get_signals() -> dict:
    random.seed(42)
    signals = json.loads((DATA_DIR / "signals.json").read_text())
    positive_all = [msg for key in signals["positive_sources"] for msg in signals[key]]
    negative_all = [msg for key in signals["negative_sources"] for msg in signals[key]]
    random.shuffle(positive_all)
    random.shuffle(negative_all)
    pos_split = int(len(positive_all) * SPLIT_RATIO)
    neg_split = int(len(negative_all) * SPLIT_RATIO)
    return {
        "positive_train": positive_all[:pos_split],
        "positive_test": positive_all[pos_split:],
        "negative_train": negative_all[:neg_split],
        "negative_test": negative_all[neg_split:],
    }


@lru_cache(maxsize=1)
def get_train_queries() -> tuple[np.ndarray, np.ndarray]:
    signals = get_signals()
    with torch.no_grad():
        pos = MODEL.encode(
            signals["positive_train"],
            normalize_embeddings=True,
            convert_to_tensor=False,
            show_progress_bar=True,
        ).astype(np.float32)
        neg = MODEL.encode(
            signals["negative_train"],
            normalize_embeddings=True,
            convert_to_tensor=False,
            show_progress_bar=True,
        ).astype(np.float32)
    return pos, neg


@lru_cache(maxsize=1)
def get_test_embeddings() -> tuple[np.ndarray, np.ndarray]:
    signals = get_signals()
    with torch.no_grad():
        pos = MODEL.encode(
            signals["positive_test"], normalize_embeddings=True, convert_to_tensor=False
        )
        neg = MODEL.encode(
            signals["negative_test"], normalize_embeddings=True, convert_to_tensor=False
        )
    return pos, neg
