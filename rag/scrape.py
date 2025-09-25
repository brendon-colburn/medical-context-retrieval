"""Site-agnostic scraping utilities with simple recipe system."""
from __future__ import annotations
import time
from typing import Dict, List, Iterable, Callable
import uuid
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup  # type: ignore

from .config import DATA_DIR
from .models import Document

USER_AGENT = "ContextualRetrievalPilot/0.2 (+contact: you@example.com)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})

__all__ = [
    "fetch",
    "extract_blocks",
    "process_recipe",
    "save_document_json",
]

def fetch(url: str, tries: int = 3, backoff: float = 1.5) -> str | None:
    for i in range(tries):
        try:
            r = SESSION.get(url, timeout=25)
            if r.status_code == 200:
                return r.text
        except requests.RequestException:
            pass
        time.sleep(backoff * (i + 1))
    return None

def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def extract_blocks(html: str, selectors: str, title_selector: str | None = None) -> tuple[str, List[str]]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup.find(attrs={"role": "main"}) or soup
    blocks: List[str] = []
    for el in main.select(selectors):
        txt = clean_text(el.get_text(" ", strip=True))
        if txt:
            blocks.append(txt)
    title_el = (main.select_one(title_selector) if title_selector else None) or main.find("h1") or soup.find("h1") or soup.title
    title = clean_text(title_el.get_text(" ", strip=True)) if title_el else "Untitled"
    return title, blocks

def save_document_json(doc: Document, outdir: Path = DATA_DIR) -> Path:
    outpath = outdir / f"{doc.doc_id}.json"
    import json
    with outpath.open("w", encoding="utf-8") as f:
        json.dump({
            "doc_title": doc.title,
            "text": doc.content,
            "source_url": doc.source_url,
            "source_org": doc.source_org,
            "pub_date": doc.pub_date,
        }, f, ensure_ascii=False, indent=2)
    return outpath

def process_recipe(name: str, urls: Iterable[str], selectors: str, source_org: str, title_selector: str | None = None) -> List[Document]:
    docs: List[Document] = []
    for url in urls:
        html = fetch(url)
        if not html:
            print(f"[{name}] Failed: {url}")
            continue
        title, blocks = extract_blocks(html, selectors, title_selector)
        content = "\n\n".join(blocks)
        doc = Document(
            doc_id=uuid.uuid4().hex,
            title=f"{source_org} — {title}",
            content=content,
            source_url=url,
            source_org=source_org,
        )
        save_document_json(doc)
        docs.append(doc)
        print(f"[{name}] Saved {len(content)} chars -> {doc.doc_id}.json")
        time.sleep(1.0)
    return docs
