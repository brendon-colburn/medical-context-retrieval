"""PDF and JSON document ingestion utilities."""
from __future__ import annotations
from pathlib import Path
from typing import List
import uuid
import json

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

from .models import Document


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file."""
    if PyPDF2 is None:
        raise ImportError("PyPDF2 is required for PDF extraction. Install with: pip install PyPDF2")

    text_parts = []
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)

    return "\n\n".join(text_parts)


def extract_text_from_pdfs(pdf_dir: Path) -> List[Document]:
    """Extract text from all PDF files in a directory.

    Args:
        pdf_dir: Directory containing PDF files

    Returns:
        List of Document objects with extracted text
    """
    documents = []
    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return documents

    for pdf_path in pdf_files:
        try:
            print(f"Extracting text from {pdf_path.name}...")
            text = extract_text_from_pdf(pdf_path)

            # Create document
            doc = Document(
                doc_id=uuid.uuid4().hex,
                title=pdf_path.stem,  # Use filename without extension as title
                content=text,
                source_url=pdf_path.name,  # Just the filename, not full path
                source_org="Uploaded PDF"
            )

            documents.append(doc)
            print(f"  ✓ Extracted {len(text)} characters from {pdf_path.name}")

        except Exception as e:
            print(f"  ✗ Error extracting {pdf_path.name}: {str(e)}")
            continue

    return documents


def load_json_documents(json_dir: Path) -> List[Document]:
    """Load documents from JSON files (e.g., web-scraped content).

    Args:
        json_dir: Directory containing JSON document files

    Returns:
        List of Document objects loaded from JSON
    """
    documents = []
    json_files = list(json_dir.glob("*.json"))

    if not json_files:
        print(f"No JSON files found in {json_dir}")
        return documents

    for json_path in json_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Create document from JSON data
            doc = Document(
                doc_id=json_path.stem,  # Use filename as ID
                title=data.get('doc_title', json_path.stem),
                content=data.get('text', ''),
                source_url=data.get('source_url', ''),
                source_org=data.get('source_org', ''),
                pub_date=data.get('pub_date', '')
            )

            documents.append(doc)
            print(f"  ✓ Loaded {len(doc.content)} characters from {json_path.name}")

        except Exception as e:
            print(f"  ✗ Error loading {json_path.name}: {str(e)}")
            continue

    return documents
