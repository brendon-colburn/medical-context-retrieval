"""FAISS index building and persistence helpers."""
from __future__ import annotations
from typing import List
import numpy as np
import faiss  # type: ignore

from .config import EMBED_DIM_FALLBACK


def build_faiss_index(embeddings: List[List[float]], index_type: str = "auto") -> faiss.Index:
    arr = np.asarray(embeddings, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    if arr.size == 0:
        raise ValueError("No embeddings provided")
    n, d = arr.shape
    if d == 0:
        d = EMBED_DIM_FALLBACK
    if index_type == "auto":
        index_type = "ivf" if n > 1000 else "flat"
    if index_type == "flat":
        index = faiss.IndexFlatIP(d)
    elif index_type == "ivf":
        nlist = max(1, min(100, n // 10))
        if n <= nlist:
            index = faiss.IndexFlatIP(d)
        else:
            quantizer = faiss.IndexFlatIP(d)
            index = faiss.IndexIVFFlat(quantizer, d, nlist)
            index.train(arr)
    else:
        raise ValueError(f"Unknown index_type {index_type}")
    faiss.normalize_L2(arr)
    index.add(arr)
    return index


def search_index(index: faiss.Index, query_vec, top_k: int = 5):
    scores, indices = index.search(query_vec, top_k)
    return scores, indices

__all__ = ["build_faiss_index", "search_index"]
