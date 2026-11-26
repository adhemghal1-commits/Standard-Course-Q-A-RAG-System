"""
Document Loader – Extracts text from PDF, CSV, DOCX, and TXT files.
Each loader returns a list of dicts: {text, source, file_type, course}
"""
import os
import re
import csv
from typing import List, Dict

from config import COURSE_MATERIALS_DIR, COURSE_KEYWORDS, SUPPORTED_EXTENSIONS


# ── Course Detection ─────────────────────────────────────────────────────

def detect_course(filename: str) -> str:
    """Detect which course a file belongs to based on its name."""
    fn_lower = filename.lower()
    for course, keywords in COURSE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in fn_lower:
                return course
    return "General"


# ── Individual Loaders ───────────────────────────────────────────────────

def load_pdf(filepath: str) -> str:
    """Extract text from a PDF file."""
    try:
        from pypdf import PdfReader
    except ImportError:
        from PyPDF2 import PdfReader
    reader = PdfReader(filepath)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)
    return "\n\n".join(pages)


def load_csv(filepath: str) -> str:
    """Extract text from a CSV file by joining all cells."""
    rows = []
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        if headers:
            for row in reader:
                # Create a readable representation for each row
                entry = " | ".join(
                    f"{h}: {v}" for h, v in zip(headers, row) if v.strip()
                )
                rows.append(entry)
    return "\n\n".join(rows)


def load_docx(filepath: str) -> str:
    """Extract text from a DOCX file."""
    from docx import Document
    doc = Document(filepath)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def load_txt(filepath: str) -> str:
    """Extract text from a plain text file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


LOADERS = {
    ".pdf":  load_pdf,
    ".csv":  load_csv,
    ".docx": load_docx,
    ".txt":  load_txt,
}


# ── Clean Text ───────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """Basic text cleaning: collapse whitespace, strip control characters."""
    text = re.sub(r"[^\S\n]+", " ", text)        # collapse spaces / tabs
    text = re.sub(r"\n{3,}", "\n\n", text)        # limit consecutive newlines
    text = re.sub(r"[^\x20-\x7E\n\r\t]", "", text)  # remove non-printable chars
    return text.strip()


# ── Main Loader ──────────────────────────────────────────────────────────

def load_all_documents(directory: str = None) -> List[Dict]:
    """
    Walk the materials directory and load every supported file.
    Returns a list of document dicts.
    """
    if directory is None:
        directory = COURSE_MATERIALS_DIR

    documents = []
    for root, _, files in os.walk(directory):
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            filepath = os.path.join(root, fname)
            loader = LOADERS.get(ext)
            if loader is None:
                continue
            try:
                raw_text = loader(filepath)
                text = clean_text(raw_text)
                if not text:
                    print(f"  ⚠ Empty after cleaning: {fname}")
                    continue
                documents.append({
                    "text": text,
                    "source": fname,
                    "file_type": ext.lstrip(".").upper(),
                    "course": detect_course(fname),
                })
                print(f"  ✓ Loaded {fname}  ({len(text):,} chars)  [{ext.upper()}]")
            except Exception as e:
                print(f"  ✗ Failed to load {fname}: {e}")

    print(f"\n  Total documents loaded: {len(documents)}")
    return documents


# ── CLI helper ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    docs = load_all_documents()
    for d in docs:
        print(f"  {d['source']:40s}  course={d['course']:35s}  chars={len(d['text']):,}")

