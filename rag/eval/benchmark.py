"""Benchmark runner for retrieval evaluation."""
from __future__ import annotations
from typing import List, Dict, Any, Callable
from time import perf_counter
import numpy as np

from .metrics import term_match_relevance, aggregate_retrieval_metrics

__all__ = [
    "evaluate_query_results",
    "run_retrieval_benchmark",
]

def evaluate_query_results(query_data: Dict, results: List[Dict], top_k: int = 5) -> Dict[str, Any]:
    expected_terms = query_data.get("expected_terms", [])
    relevance_scores = []
    for r in results[:top_k]:
        combined = f"{r.get('ctx_header','')} {r.get('raw_chunk','')}"
        relevance_scores.append(term_match_relevance(combined, expected_terms))
    evaluation = {
        "query": query_data["query"],
        "category": query_data.get("category", "uncategorized"),
        "num_results": len(results),
        "relevance_scores": relevance_scores,
        "avg_relevance": float(np.mean(relevance_scores)) if relevance_scores else 0.0,
        "max_relevance": float(max(relevance_scores)) if relevance_scores else 0.0,
        "top_3_avg_relevance": float(np.mean(relevance_scores[:3])) if relevance_scores else 0.0,
        "precision_at_1": relevance_scores[0] if relevance_scores else 0.0,
        "has_relevant_result": any(s > 0.3 for s in relevance_scores),
        "avg_similarity_score": float(np.mean([r.get("similarity_score", 0) for r in results[:top_k]])) if results else 0.0,
    }
    return evaluation

def run_retrieval_benchmark(queries: List[Dict], retriever, top_k: int = 5, progress: Callable[[int,int,str], None] | None = None):
    evaluations = []
    start = perf_counter()
    for i, qd in enumerate(queries, 1):
        results = retriever.search(qd["query"], top_k=top_k)
        eval_row = evaluate_query_results(qd, results, top_k)
        evaluations.append(eval_row)
        if progress:
            progress(i, len(queries), qd["query"])
    elapsed = perf_counter() - start
    aggregates = aggregate_retrieval_metrics(evaluations)
    aggregates["benchmark_time_seconds"] = elapsed
    aggregates["avg_time_per_query"] = elapsed / len(queries) if queries else 0.0
    # Category breakdown
    categories = {}
    for cat in {e["category"] for e in evaluations}:
        cat_evals = [e for e in evaluations if e["category"] == cat]
        categories[cat] = {
            "count": len(cat_evals),
            "avg_relevance": float(np.mean([e["avg_relevance"] for e in cat_evals])),
            "avg_max_relevance": float(np.mean([e["max_relevance"] for e in cat_evals])),
            "percent_relevant": float(np.mean([e["has_relevant_result"] for e in cat_evals]) * 100),
        }
    return {
        "aggregate_metrics": aggregates,
        "category_metrics": categories,
        "individual_evaluations": evaluations,
    }
