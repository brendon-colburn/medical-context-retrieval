"""Retrieval evaluation metrics utilities."""
from __future__ import annotations
from typing import List, Dict, Sequence
import numpy as np

__all__ = [
    "term_match_relevance",
    "aggregate_retrieval_metrics",
]

def term_match_relevance(text: str, expected_terms: Sequence[str]) -> float:
    if not expected_terms:
        return 0.0
    lower = text.lower()
    matches = sum(1 for t in expected_terms if t.lower() in lower)
    return matches / len(expected_terms)

def aggregate_retrieval_metrics(evaluations: List[Dict]):
    if not evaluations:
        return {}
    avg_relevance_overall = float(np.mean([e["avg_relevance"] for e in evaluations])) if evaluations else 0.0
    return {
        "total_queries": len(evaluations),
        "avg_relevance_overall": avg_relevance_overall,
        "avg_max_relevance": float(np.mean([e["max_relevance"] for e in evaluations])),
        "avg_precision_at_1": float(np.mean([e["precision_at_1"] for e in evaluations])),
        "avg_top_3_relevance": float(np.mean([e["top_3_avg_relevance"] for e in evaluations])),
        "percent_with_relevant_results": float(np.mean([e["has_relevant_result"] for e in evaluations]) * 100),
        "avg_similarity_score": float(np.mean([e["avg_similarity_score"] for e in evaluations])),
    }
