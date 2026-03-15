from pathlib import Path

ARTEFACTS_DIR = Path(__file__).parents[2] / "artefacts"
DATA_DIR = Path(__file__).parents[2] / "data"

ARTEFACTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
