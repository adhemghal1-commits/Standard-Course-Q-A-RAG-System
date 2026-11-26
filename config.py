"""
Configuration settings for the Course Q&A RAG System.
"""
import os

# ── Paths ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COURSE_MATERIALS_DIR = os.path.join(BASE_DIR, "Course files")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_store")

# ── Embedding Model ─────────────────────────────────────────────────────
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ── Chunking ─────────────────────────────────────────────────────────────
CHUNK_SIZE = 500          # characters per chunk
CHUNK_OVERLAP = 100       # overlap between consecutive chunks

# ── Retriever ────────────────────────────────────────────────────────────
RETRIEVER_TOP_K = 5       # number of chunks to retrieve

# ── ChromaDB ─────────────────────────────────────────────────────────────
CHROMA_COLLECTION_NAME = "course_materials"

# ── Supported file types ────────────────────────────────────────────────
SUPPORTED_EXTENSIONS = {".pdf", ".csv", ".docx", ".txt"}

# ── Course Mapping (auto-detected from file names / paths) ──────────────
COURSE_KEYWORDS = {
    "Machine Learning Fundamentals": ["lecture", "ML_"],
    "Data Science with Python":      ["DS_Python", "ds_python"],
    "Natural Language Processing":   ["NLP_", "nlp_"],
}

