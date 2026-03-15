from pathlib import Path

import numpy as np
import onnxruntime as ort
from config import ARTEFACTS_DIR
from tokenizers import Tokenizer


def load_session(
    model_dir: Path, onnx_name: str
) -> tuple[ort.InferenceSession, Tokenizer]:
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
    sess_options.intra_op_num_threads = 1

    session = ort.InferenceSession(
        str(model_dir / onnx_name),
        sess_options=sess_options,
        providers=["CPUExecutionProvider"],
    )
    tokenizer = Tokenizer.from_file(str(model_dir / "tokenizer.json"))
    tokenizer.enable_padding(pad_token="[PAD]", pad_id=0)
    tokenizer.enable_truncation(max_length=128)
    return session, tokenizer


def _mean_pooling(
    token_embeddings: np.ndarray, attention_mask: np.ndarray
) -> np.ndarray:
    mask = attention_mask[..., np.newaxis].astype(np.float32)
    return (token_embeddings * mask).sum(1) / mask.sum(1).clip(min=1e-9)


def embed(
    texts: str | list[str],
    session: ort.InferenceSession,
    tokenizer: Tokenizer,
) -> np.ndarray:
    if isinstance(texts, str):
        texts = [texts]

    encoded = tokenizer.encode_batch(texts)

    input_ids = np.array([e.ids for e in encoded], dtype=np.int64)
    attention_mask = np.array([e.attention_mask for e in encoded], dtype=np.int64)
    token_type_ids = np.zeros_like(input_ids, dtype=np.int64)

    outputs = session.run(
        None,
        {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
        },
    )

    token_embeddings = np.array(outputs[0])
    embeddings = _mean_pooling(token_embeddings, attention_mask)
    norms = np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)
    return embeddings / np.maximum(norms, 1e-9)


if __name__ == "__main__":
    session, tokenizer = load_session(ARTEFACTS_DIR / "transformer", "model.onnx")
    print(embed(texts="test", session=session, tokenizer=tokenizer))
