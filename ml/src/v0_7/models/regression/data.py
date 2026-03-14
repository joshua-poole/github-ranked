import polars as pl
import torch
from rich import print as rprint
from sentence_transformers import SentenceTransformer

from v0_7.core import ARTEFACTS_DIR, DATA_DIR, DEVICE
from v0_7.core.utils import timestamp

DATASET_PATH = DATA_DIR / "dhruvildave_github-commit-messages-dataset.csv"
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=DEVICE)
MODEL.to(torch.float16)
MODEL = torch.compile(MODEL, mode="reduce-overhead")


def _create_embeddings_file(truncate_size: int = 100, batch_size: int = 4096):
    df = (
        pl.scan_csv(DATASET_PATH)
        .select(pl.col("message").fill_null("").str.slice(0, truncate_size))
        .collect()
    )
    messages = df["message"].to_numpy()
    rprint(f"[bold green]Dataset Row Count:[/bold green] {len(messages):,}")

    with torch.inference_mode():
        embs = MODEL.encode(
            messages,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_tensor=True,
            normalize_embeddings=True,
        ).cpu()

    export_path = ARTEFACTS_DIR / f"{timestamp()}_embeddings.pt"
    torch.save(embs.half(), export_path)
    rprint(f"[bold green]Saved embeddings to:[/bold green] {export_path}")
    return embs.float()


if __name__ == "__main__":
    _create_embeddings_file()
