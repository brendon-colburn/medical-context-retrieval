"""Semantic chunking utilities.

Initial simple implementation mirrors existing logic (paragraph grouping) but
is modular so it can be swapped for more advanced approaches later.
"""
from __future__ import annotations
from typing import List, Dict
import re

from .config import SEMANTIC_MAX_WORDS

__all__ = ["split_by_semantic_boundaries"]

def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def split_by_semantic_boundaries(text: str, max_words: int = SEMANTIC_MAX_WORDS) -> List[Dict]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[Dict] = []
    cur = []
    cur_words = 0
    for para in paragraphs:
        w = len(para.split())
        if cur and cur_words + w > max_words:
            combined = "\n\n".join(cur).strip()
            chunks.append({"text": _normalize_whitespace(combined), "word_count": cur_words})
            cur = [para]
            cur_words = w
        else:
            cur.append(para)
            cur_words += w
    if cur:
        combined = "\n\n".join(cur).strip()
        chunks.append({"text": _normalize_whitespace(combined), "word_count": cur_words})
    return chunks
