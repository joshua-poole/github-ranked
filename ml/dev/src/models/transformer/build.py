from pathlib import Path

import numpy as np
import onnx
import onnxruntime as ort
from core.config import ARTEFACTS_DIR
from onnxruntime.quantization import QuantType, quantize_dynamic
from onnxruntime.transformers import optimizer
from onnxruntime.transformers.fusion_options import FusionOptions
from optimum.onnxruntime import ORTModelForFeatureExtraction
from tqdm import tqdm
from transformers import AutoTokenizer, PreTrainedTokenizerBase

MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

RAW_DIR = ARTEFACTS_DIR / "transformer_raw"
OPT_DIR = ARTEFACTS_DIR / "transformer_opt"

RAW_DIR.mkdir(parents=True, exist_ok=True)
OPT_DIR.mkdir(parents=True, exist_ok=True)

QUANTIZED_ONNX = OPT_DIR / "model_quant_int8.onnx"
QUANTIZED_OPTIMIZED_ONNX = OPT_DIR / "model_quantd_int8_opt.onnx"


def _download_model(output: Path):
    model = ORTModelForFeatureExtraction.from_pretrained(MODEL_ID, export=True)
    model.save_pretrained(str(output))

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    tokenizer.save_pretrained(str(output))


def _get_model_params(onnx_path: Path) -> tuple[int, int]:
    model = onnx.load(str(onnx_path))
    config = {prop.key: prop.value for prop in model.metadata_props}

    num_heads = int(config.get("num_attention_heads", 12))
    hidden_size = int(config.get("hidden_size", 384))

    return num_heads, hidden_size


def _optimize_model(raw_onnx: Path, output: Path):
    num_heads, hidden_size = _get_model_params(raw_onnx)

    opt_options = FusionOptions("bert")
    opt_options.enable_gelu_approximation = True

    opt_model = optimizer.optimize_model(
        str(raw_onnx),
        model_type="bert",
        num_heads=num_heads,
        hidden_size=hidden_size,
        optimization_options=opt_options,
    )
    opt_model.save_model_to_file(str(output))


def _quantize_model(optimized_onnx: Path, output: Path):
    quantize_dynamic(
        model_input=str(optimized_onnx),
        model_output=str(output),
        weight_type=QuantType.QInt8,
    )


def _build_model():
    if not QUANTIZED_ONNX.exists():
        _download_model(RAW_DIR)
        _quantize_model(RAW_DIR / "model.onnx", QUANTIZED_ONNX)
        _optimize_model(QUANTIZED_ONNX, QUANTIZED_OPTIMIZED_ONNX)


def load_session(
    model_dir: Path = OPT_DIR, onnx_name: str = "model_quantd_int8_opt.onnx"
) -> tuple[ort.InferenceSession, PreTrainedTokenizerBase]:
    if not model_dir.exists() or not (model_dir / onnx_name).exists():
        _build_model()

    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
    sess_options.intra_op_num_threads = 1

    session = ort.InferenceSession(
        str(QUANTIZED_OPTIMIZED_ONNX),
        sess_options=sess_options,
        providers=["CPUExecutionProvider"],
    )
    tokenizer = AutoTokenizer.from_pretrained(str(RAW_DIR))
    return session, tokenizer


def _mean_pooling(
    token_embeddings: np.ndarray, attention_mask: np.ndarray
) -> np.ndarray:
    mask = attention_mask[..., np.newaxis].astype(np.float32)
    return (token_embeddings * mask).sum(1) / mask.sum(1).clip(min=1e-9)


def _embed(
    texts: str | list[str],
    session: ort.InferenceSession,
    tokenizer: PreTrainedTokenizerBase,
) -> np.ndarray:
    if isinstance(texts, str):
        texts = [texts]

    encoded = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="np",
    )
    outputs = session.run(None, dict(encoded))

    token_embeddings = np.array(outputs[0])
    attention_mask = np.array(encoded["attention_mask"])

    embeddings = _mean_pooling(token_embeddings, attention_mask)
    norms = np.linalg.norm(embeddings, ord=2, axis=1, keepdims=True)
    return embeddings / np.maximum(norms, 1e-9)


def embed(
    texts: str | list[str],
    session: ort.InferenceSession,
    tokenizer: PreTrainedTokenizerBase,
    batch_size: int = 32,
    show_progress: bool = True,
) -> np.ndarray:
    if isinstance(texts, str):
        texts = [texts]

    batches = range(0, len(texts), batch_size)
    results = []
    for i in tqdm(batches, desc="Embedding", unit="batch", disable=not show_progress):
        results.append(_embed(texts[i : i + batch_size], session, tokenizer))
    return np.vstack(results)


if __name__ == "__main__":
    session, tokenizer = load_session()
    print(embed(texts="Test", session=session, tokenizer=tokenizer))
