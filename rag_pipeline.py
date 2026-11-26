"""
RAG Pipeline – Retriever + LLM answer generation.
Uses a local Hugging Face model (no API key required) to generate answers
based solely on retrieved course materials with source attribution.
"""
from typing import List, Dict, Optional

from vector_store import VectorStore


# ── Prompt Template ──────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful course assistant. Answer the student's question using ONLY the provided course materials below. If the answer cannot be found in the materials, say "I don't have enough information in the course materials to answer this question."

Always cite which source file(s) your answer comes from.

Course Materials:
{context}

Student Question: {question}

Answer:"""


# ── RAG Pipeline ─────────────────────────────────────────────────────────

class RAGPipeline:
    """End-to-end Retrieval-Augmented Generation pipeline."""

    def __init__(self, vector_store: VectorStore = None, model_name: str = "google/flan-t5-base"):
        self.vector_store = vector_store or VectorStore()
        self.model_name = model_name
        self._tokenizer = None
        self._model = None

    # ── LLM (lazy-loaded) ────────────────────────────────────────────
    def _ensure_model_loaded(self):
        """Load tokenizer and model using transformers Auto classes."""
        if self._tokenizer is None or self._model is None:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            print(f"  Loading LLM ({self.model_name}) …")
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            print(f"  ✓ LLM loaded: {self.model_name}")

    def generate_answer(self, prompt: str) -> str:
        """Generate answer text from the prompt."""
        self._ensure_model_loaded()
        inputs = self._tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        outputs = self._model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
        )
        return self._tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # ── Build Context String ─────────────────────────────────────────
    @staticmethod
    def _build_context(retrieved: List[Dict]) -> str:
        parts = []
        for i, r in enumerate(retrieved, 1):
            parts.append(
                f"[Source {i}: {r['source']} | Course: {r['course']}]\n{r['text']}"
            )
        return "\n\n---\n\n".join(parts)

    # ── Answer a Question ────────────────────────────────────────────
    def answer(self, question: str, course_filter: Optional[str] = None,
               top_k: int = 5) -> Dict:
        """
        Run the full RAG pipeline:
          1. Retrieve relevant chunks
          2. Build prompt with context
          3. Generate answer with LLM

        Returns:
            {answer, sources, retrieved_chunks, question}
        """
        # 1. Retrieve
        retrieved = self.vector_store.search(
            query=question, top_k=top_k, course_filter=course_filter
        )

        if not retrieved:
            return {
                "answer": "I couldn't find any relevant course materials for your question.",
                "sources": [],
                "retrieved_chunks": [],
                "question": question,
            }

        # 2. Build prompt
        context = self._build_context(retrieved)
        prompt = SYSTEM_PROMPT.format(context=context, question=question)

        # 3. Generate answer
        answer_text = self.generate_answer(prompt)

        # 4. Collect unique sources
        sources = []
        seen = set()
        for r in retrieved:
            key = (r["source"], r["course"])
            if key not in seen:
                seen.add(key)
                sources.append({
                    "file": r["source"],
                    "course": r["course"],
                    "type": r["file_type"],
                })

        return {
            "answer": answer_text,
            "sources": sources,
            "retrieved_chunks": retrieved,
            "question": question,
        }


# ── CLI helper ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    from document_loader import load_all_documents
    from text_processing import chunk_documents

    # Build knowledge base
    docs = load_all_documents()
    chunks = chunk_documents(docs)
    vs = VectorStore()
    vs.build_index(chunks)

    # Test question
    rag = RAGPipeline(vs)
    result = rag.answer("What is overfitting in machine learning?")
    print(f"\nQ: {result['question']}")
    print(f"A: {result['answer']}")
    print(f"\nSources:")
    for s in result["sources"]:
        print(f"  - {s['file']} ({s['course']}) [{s['type']}]")

