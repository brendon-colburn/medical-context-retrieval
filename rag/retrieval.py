"""Unified retrieval abstraction."""
from __future__ import annotations
from typing import List, Dict, Any, Sequence
import numpy as np
import faiss  # type: ignore

from .embeddings import get_embeddings_batch

class EmbeddingRetriever:
    """Embedding-based retriever with pluggable embedding function.

    Parameters
    ----------
    index : faiss.Index
        FAISS index (vectors assumed already normalized for IP similarity)
    metadata : Sequence[Dict[str, Any]]
        Parallel metadata list aligned with index order.
    embed_fn : callable | None
        Function accepting List[str] -> List[List[float]]. Defaults to
        `rag.embeddings.get_embeddings_batch`. Allows injection of a fake
        embedding function for offline tests.
    """

    def __init__(self, index: faiss.Index, metadata: Sequence[Dict[str, Any]], embed_fn=None):
        self.index = index
        self.metadata = list(metadata)
        self._embed_fn = embed_fn or get_embeddings_batch

    def embed_query(self, query: str):
        emb = self._embed_fn([query])
        if not emb:
            raise RuntimeError("Failed to embed query (empty embedding list)")
        vec = np.array([emb[0]], dtype=np.float32)
        faiss.normalize_L2(vec)
        return vec

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        vec = self.embed_query(query)
        scores, indices = self.index.search(vec, top_k)
        out: List[Dict[str, Any]] = []
        for rank, (score, idx) in enumerate(zip(scores[0], indices[0]), 1):
            if idx < 0:
                break
            meta = self.metadata[idx] if idx < len(self.metadata) else {}
            out.append({
                "rank": rank,
                "similarity_score": float(score),
                **meta
            })
        return out

__all__ = ["EmbeddingRetriever"]
