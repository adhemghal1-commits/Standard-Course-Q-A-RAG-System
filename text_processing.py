"""
Text Processing – Chunk documents into smaller pieces for embedding.
Uses LangChain's RecursiveCharacterTextSplitter for intelligent splitting.
"""
from typing import List, Dict

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(documents: List[Dict],
                    chunk_size: int = None,
                    chunk_overlap: int = None) -> List[Dict]:
    """
    Split each document's text into smaller chunks.
    Each chunk inherits the source metadata.

    Returns list of dicts:
        {text, source, file_type, course, chunk_id}
    """
    chunk_size = chunk_size or CHUNK_SIZE
    chunk_overlap = chunk_overlap or CHUNK_OVERLAP

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunks = []
    for doc in documents:
        text_chunks = splitter.split_text(doc["text"])
        for i, chunk_text in enumerate(text_chunks):
            all_chunks.append({
                "text": chunk_text,
                "source": doc["source"],
                "file_type": doc["file_type"],
                "course": doc["course"],
                "chunk_id": f"{doc['source']}::chunk_{i}",
            })

    print(f"  Created {len(all_chunks)} chunks from {len(documents)} documents")
    print(f"  Avg chunk length: {sum(len(c['text']) for c in all_chunks) // max(len(all_chunks),1)} chars")
    return all_chunks


# ── CLI helper ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    from document_loader import load_all_documents
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    for c in chunks[:5]:
        print(f"  [{c['chunk_id']}]  {c['text'][:80]}...")

