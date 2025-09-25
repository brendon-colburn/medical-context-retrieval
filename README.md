# Medical Context Retrieval (Refactor Skeleton)

This repository contains a Retrieval-Augmented Generation (RAG) prototype for medical guideline ingestion, contextual header generation, semantic search, and evaluation. A refactor is in progress to modularize a previously monolithic notebook.

## Current Modular Layout (in progress)
```
rag/
  config.py        # Central configuration, paths, rate limits
  models.py        # Dataclasses: Document, Chunk, RetrievalResult
  embeddings.py    # Embedding batch helper (Azure OpenAI)
  index.py         # FAISS index build/search helpers
  retrieval.py     # EmbeddingRetriever abstraction
  eval/            # (planned) metrics, benchmarks, A/B tests
```

## Goals of Refactor
- Reduce notebook verbosity; move logic into importable modules
- Eliminate duplicated code across scraping, indexing, and evaluation
- Improve testability and reproducibility (deterministic loading, caching)
- Centralize configuration and secrets handling

## Next Steps
1. Extract scraping + chunking + header generation into modules
2. Add caching/load utilities for processed chunks and embeddings
3. Unify baseline vs enhanced index construction via parameters
4. Modular evaluation (retrieval metrics, header impact, LLM comparison)
5. Slim `main.ipynb` to orchestration + presentation only

## Quick Start
Install dependencies:
```bash
pip install -r requirements.txt
```

(Notebook will be updated to import from `rag.*` modules.)

## Version
Experimental refactor stage (v0.1.0 roadmap).
