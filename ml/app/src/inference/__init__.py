from typing import NamedTuple

import joblib
import onnxruntime as ort
from config import ARTEFACTS_DIR
from sklearn.pipeline import Pipeline
from tokenizers import Tokenizer

from .transformer import embed, load_session


class _SentimentModelBundle(NamedTuple):
    clf: Pipeline
    session: ort.InferenceSession
    tokenizer: Tokenizer


_session, _tokenizer = load_session(ARTEFACTS_DIR / "transformer", "model.onnx")
_clf = joblib.load(ARTEFACTS_DIR / "regression.pkl")["model"]

SENTIMENT_MODEL = _SentimentModelBundle(
    clf=_clf, session=_session, tokenizer=_tokenizer
)


def score(
    message: str | list[str],
) -> float | list[float]:
    if isinstance(message, str):
        return float(
            SENTIMENT_MODEL.clf.predict_proba(
                embed([message], SENTIMENT_MODEL.session, SENTIMENT_MODEL.tokenizer)
            )[0, 1]
        )
    return SENTIMENT_MODEL.clf.predict_proba(
        embed(message, SENTIMENT_MODEL.session, SENTIMENT_MODEL.tokenizer)
    )[:, 1].tolist()
