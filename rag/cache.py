"""Caching utilities for documents, chunks, embeddings, and FAISS index.

Design goals:
- Idempotent: safe to call repeatedly without corrupting state.
- Atomic writes: write to temp then rename to avoid partial files.
- Simple JSON/NumPy/FAISS persistence; no external DB required.
- Layered: documents -> chunks -> embeddings -> index.

Public functions:
- save_documents(docs)
- load_documents()
- save_chunks(chunks)
- load_chunks()
- save_embeddings(emb_matrix)
- load_embeddings()
- save_faiss_index(index)
- load_faiss_index()
- build_or_load_index(texts, embed_fn, force=False)

The build_or_load_index helper derives embeddings (if needed) and returns (index, metadata, embeddings).
"""
from __future__ import annotations
from typing import List, Sequence, Dict, Any, Tuple, Callable, Optional
import json, os, tempfile
from pathlib import Path
import numpy as np
import faiss  # type: ignore

from . import config
from .models import Document, Chunk
from .embeddings import get_embeddings_batch
from .index import build_faiss_index

DOCS_PATH = config.CACHE_DIR / "documents.json"
CHUNKS_PATH = config.CACHE_DIR / "chunks.json"
EMB_PATH = config.CACHE_DIR / "embeddings.npy"
INDEX_PATH = config.CACHE_DIR / "faiss.index"
META_PATH = config.CACHE_DIR / "metadata.json"

# ----------------------- generic helpers -----------------------

def _atomic_write(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)

# ----------------------- documents -----------------------------

def save_documents(docs: Sequence[Document]):
    payload = [doc.__dict__ for doc in docs]
    _atomic_write(DOCS_PATH, json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"))


def load_documents() -> List[Document]:
    if not DOCS_PATH.exists():
        return []
    data = json.loads(DOCS_PATH.read_text("utf-8"))
    return [Document(**d) for d in data]

# ----------------------- chunks --------------------------------

def save_chunks(chunks: Sequence[Chunk]):
    payload = [c.__dict__ for c in chunks]
    _atomic_write(CHUNKS_PATH, json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8"))


def load_chunks() -> List[Chunk]:
    if not CHUNKS_PATH.exists():
        return []
    data = json.loads(CHUNKS_PATH.read_text("utf-8"))
    return [Chunk(**c) for c in data]

# ----------------------- embeddings ----------------------------

def save_embeddings(embeddings: np.ndarray):
    embeddings = np.asarray(embeddings, dtype=np.float32)
    np.save(EMB_PATH, embeddings)


def load_embeddings() -> Optional[np.ndarray]:
    if not EMB_PATH.exists():
        return None
    return np.load(EMB_PATH)

# ----------------------- metadata & index ----------------------

def save_metadata(meta: Sequence[Dict[str, Any]]):
    _atomic_write(META_PATH, json.dumps(list(meta), ensure_ascii=False, indent=2).encode("utf-8"))


def load_metadata() -> List[Dict[str, Any]]:
    if not META_PATH.exists():
        return []
    return json.loads(META_PATH.read_text("utf-8"))


def save_faiss_index(index: faiss.Index):
    faiss.write_index(index, str(INDEX_PATH))


def load_faiss_index() -> Optional[faiss.Index]:
    if not INDEX_PATH.exists():
        return None
    return faiss.read_index(str(INDEX_PATH))

# ----------------------- orchestration -------------------------

def build_or_load_index(
    texts: Sequence[str],
    metadata: Sequence[Dict[str, Any]],
    embed_fn: Optional[Callable[[List[str]], List[List[float]]]] = None,
    force: bool = False,
    index_type: str = "auto",
) -> Tuple[faiss.Index, List[Dict[str, Any]], np.ndarray]:
    """Load cached index+embeddings or build from provided texts.

    Parameters
    ----------
    texts : list of str
        The (augmented) chunk texts to embed.
    metadata : list of dict
        Parallel metadata aligned to texts.
    embed_fn : callable
        Embedding function (defaults to get_embeddings_batch).
    force : bool
        If True, rebuild even if cache exists.
    index_type : str
        Index strategy forwarded to build_faiss_index.
    """
    embed_fn = embed_fn or get_embeddings_batch

    cached_index = load_faiss_index()
    cached_emb = load_embeddings()
    cached_meta = load_metadata()

    if not force and cached_index and cached_emb is not None and cached_meta and len(cached_meta) == len(texts):
        # Assume cache is valid if counts match
        return cached_index, cached_meta, cached_emb

    # Build fresh with batching and delays to avoid rate limits
    batch_size = config.EMBED_BATCH_SIZE
    batch_delay = config.EMBED_DELAY_SECONDS
    embeddings_list = []
    
    print(f"[embeddings] Processing {len(texts)} texts in batches of {batch_size} (delay: {batch_delay}s)")
    for i in range(0, len(texts), batch_size):
        batch = list(texts[i:i + batch_size])
        batch_embeddings = embed_fn(batch)
        if not batch_embeddings:
            raise RuntimeError(f"Failed to generate embeddings for batch {i//batch_size + 1}")
        embeddings_list.extend(batch_embeddings)
        batch_num = i//batch_size + 1
        total_batches = (len(texts) + batch_size - 1)//batch_size
        print(f"[embeddings] Completed batch {batch_num}/{total_batches}")
        
        # Add delay between batches (except for last batch)
        if batch_num < total_batches:
            import time
            time.sleep(batch_delay)
    
    if not embeddings_list:
        raise RuntimeError("Failed to generate embeddings")
    emb_matrix = np.asarray(embeddings_list, dtype=np.float32)
    index = build_faiss_index(embeddings_list, index_type=index_type)

    # Persist
    save_embeddings(emb_matrix)
    save_faiss_index(index)
    save_metadata(metadata)

    return index, list(metadata), emb_matrix

__all__ = [
    "save_documents",
    "load_documents",
    "save_chunks",
    "load_chunks",
    "save_embeddings",
    "load_embeddings",
    "save_faiss_index",
    "load_faiss_index",
    "save_metadata",
    "load_metadata",
    "build_or_load_index",
]
