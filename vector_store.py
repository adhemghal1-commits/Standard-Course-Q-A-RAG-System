"""
Vector Store – Create embeddings and store them in ChromaDB.
Uses sentence-transformers for embedding and ChromaDB as the vector database.
"""
import os
import shutil
from typing import List, Dict, Optional

import chromadb
from chromadb.config import Settings

from config import (
    VECTOR_DB_DIR,
    EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME,
    RETRIEVER_TOP_K,
)


class VectorStore:
    """Manages embedding creation and ChromaDB storage / retrieval."""

    def __init__(self, persist_dir: str = None, model_name: str = None):
        self.persist_dir = persist_dir or VECTOR_DB_DIR
        self.model_name = model_name or EMBEDDING_MODEL_NAME
        self._embedding_fn = None
        self._client = None
        self._collection = None

    # ── Lazy-loaded embedding function ───────────────────────────────
    @property
    def embedding_fn(self):
        if self._embedding_fn is None:
            try:
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer(self.model_name, device="cpu")

                class DirectSentenceTransformerEmbeddings:
                    def __init__(self, st_model):
                        self.model = st_model

                    def embed_documents(self, texts):
                        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True).tolist()

                    def embed_query(self, query):
                        return self.model.encode(query, normalize_embeddings=True).tolist()

                self._embedding_fn = DirectSentenceTransformerEmbeddings(model)
                print(f"  ✓ Loaded embedding model: {self.model_name}")
            except Exception as e:
                from langchain_huggingface import HuggingFaceEmbeddings
                self._embedding_fn = HuggingFaceEmbeddings(
                    model_name=self.model_name,
                    model_kwargs={"device": "cpu"},
                    encode_kwargs={"normalize_embeddings": True},
                )
                print(f"  ✓ Loaded HuggingFaceEmbeddings: {self.model_name}")
        return self._embedding_fn

    # ── ChromaDB client & collection ─────────────────────────────────
    @property
    def client(self):
        if self._client is None:
            os.makedirs(self.persist_dir, exist_ok=True)
            self._client = chromadb.PersistentClient(path=self.persist_dir)
        return self._client

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    # ── Build / Rebuild ──────────────────────────────────────────────
    def build_index(self, chunks: List[Dict], force_rebuild: bool = False):
        """Embed all chunks and store in ChromaDB."""
        if force_rebuild and os.path.exists(self.persist_dir):
            shutil.rmtree(self.persist_dir)
            self._client = None
            self._collection = None
            print("  🗑  Cleared existing vector store")

        existing = self.collection.count()
        if existing > 0 and not force_rebuild:
            print(f"  ℹ Vector store already has {existing} chunks – skipping rebuild")
            return

        texts = [c["text"] for c in chunks]
        ids = [c["chunk_id"] for c in chunks]
        metadatas = [
            {"source": c["source"], "file_type": c["file_type"], "course": c["course"]}
            for c in chunks
        ]

        print(f"  Embedding {len(texts)} chunks …")
        embeddings = self.embedding_fn.embed_documents(texts)
        print(f"  ✓ Embeddings created ({len(embeddings)} × {len(embeddings[0])}d)")

        # ChromaDB add in batches of 500
        batch_size = 500
        for start in range(0, len(texts), batch_size):
            end = start + batch_size
            self.collection.add(
                ids=ids[start:end],
                documents=texts[start:end],
                embeddings=embeddings[start:end],
                metadatas=metadatas[start:end],
            )
        print(f"  ✓ Stored {self.collection.count()} chunks in ChromaDB")

    # ── Retrieval ────────────────────────────────────────────────────
    def search(self, query: str, top_k: int = None,
               course_filter: Optional[str] = None) -> List[Dict]:
        """
        Retrieve the top-k most relevant chunks for a query.
        Optionally filter by course name.
        """
        top_k = top_k or RETRIEVER_TOP_K
        query_embedding = self.embedding_fn.embed_query(query)

        where_filter = None
        if course_filter and course_filter != "All Courses":
            where_filter = {"course": course_filter}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        retrieved = []
        if results and results["documents"]:
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                retrieved.append({
                    "text": doc,
                    "source": meta.get("source", "unknown"),
                    "file_type": meta.get("file_type", ""),
                    "course": meta.get("course", ""),
                    "distance": dist,
                })
        return retrieved

    # ── Utilities ────────────────────────────────────────────────────
    def count(self) -> int:
        return self.collection.count()

    def list_courses(self) -> List[str]:
        """Return a sorted list of unique course names in the store."""
        result = self.collection.get(include=["metadatas"])
        courses = set()
        if result and result["metadatas"]:
            for meta in result["metadatas"]:
                courses.add(meta.get("course", "General"))
        return sorted(courses)


# ── CLI helper ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    from document_loader import load_all_documents
    from text_processing import chunk_documents

    docs = load_all_documents()
    chunks = chunk_documents(docs)
    vs = VectorStore()
    vs.build_index(chunks, force_rebuild=True)

    # Quick test
    results = vs.search("What is gradient descent?")
    for r in results:
        print(f"\n  [{r['source']}] (dist={r['distance']:.4f})")
        print(f"  {r['text'][:120]}...")

