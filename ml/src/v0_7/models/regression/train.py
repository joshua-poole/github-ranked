from v0_7.core import ARTEFACTS_DIR
from v0_7.core.utils import timestamp

MODEL_PATH = ARTEFACTS_DIR / f"{timestamp()}.pkl"

K_POSITIVE = 20_000
K_NEGATIVE = 10_000