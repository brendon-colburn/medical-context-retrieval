"""Lightweight smoke test for the modular RAG refactor.

Run: `python smoke_test.py`

What it validates:
1. Modules import without errors
2. Can build a FAISS index from synthetic embeddings
3. EmbeddingRetriever.search returns structured results

This does NOT call external APIs; embeddings are random to keep it offline.
"""
from __future__ import annotations
import numpy as np

from rag import config  # noqa: F401 - ensure accessible
from rag.index import build_faiss_index
from rag.retrieval import EmbeddingRetriever

# Create synthetic metadata + embeddings
N = 5
DIM = 16
rng = np.random.default_rng(42)
embeddings = (rng.random((N, DIM)) * 2 - 1).astype("float32")
# Normalize like production code does before add
from faiss import normalize_L2  # type: ignore
normalize_L2(embeddings)

metadata = [
    {
        "chunk_id": i,
        "doc_id": f"doc_{i}",
        "doc_title": f"Doc Title {i}",
        "source_org": "TEST",
        "source_url": "https://example.org/doc",
        "section_path": f"Section {i+1}",
        "ctx_header": f"Header {i}",
        "raw_chunk": f"This is synthetic chunk {i} with keyword alpha beta gamma.",
    }
    for i in range(N)
]

index = build_faiss_index(embeddings.tolist(), index_type="flat")
def _fake_embed(batch, model=None):
    out = []
    for text in batch:
        vec = np.zeros(DIM, dtype="float32")
        for j, c in enumerate(text.encode("utf-8")):
            vec[j % DIM] += c
        norm = np.linalg.norm(vec) or 1.0
        out.append((vec / norm).tolist())
    return out

retriever = EmbeddingRetriever(index, metadata, embed_fn=_fake_embed)

query = "alpha guidance"
results = retriever.search(query, top_k=3)
print("Smoke test query:", query)
print("Results returned:", len(results))
for r in results:
    print(f"Rank {r['rank']} | score={r['similarity_score']:.4f} | title={r['doc_title']} | section={r['section_path']}")

assert results, "No results returned"
print("\n✅ Smoke test passed.")
