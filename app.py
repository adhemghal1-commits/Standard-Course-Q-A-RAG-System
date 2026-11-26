"""
Streamlit App – Course Q&A RAG System
Deploy with:  streamlit run app.py
"""
import os
import streamlit as st

from config import VECTOR_DB_DIR, COURSE_MATERIALS_DIR
from document_loader import load_all_documents
from text_processing import chunk_documents
from vector_store import VectorStore
from rag_pipeline import RAGPipeline

# ── Page Config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="📚 Course Q&A – RAG System",
    page_icon="📚",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .source-card {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-left: 4px solid #4A90D9;
    }
    .chunk-card {
        background-color: #fafafa;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e0e0e0;
        font-size: 0.9rem;
    }
    .metric-box {
        background-color: #e8f4f8;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ── Initialize Session State ────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading knowledge base and models…")
def initialize_system():
    """Load documents, build vector store, and initialize RAG pipeline."""
    # 1. Load documents
    docs = load_all_documents()
    if not docs:
        return None, None, [], []

    # 2. Chunk documents
    chunks = chunk_documents(docs)

    # 3. Build vector store
    vs = VectorStore()
    vs.build_index(chunks)

    # 4. Initialize RAG pipeline
    rag = RAGPipeline(vs)

    # 5. Get available courses
    courses = vs.list_courses()

    return rag, vs, courses, docs


# ── Main App ─────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown("<h1 class='main-header'>📚 Course Q&A – RAG System</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:gray;'>"
        "Ask questions about your course materials and get answers with source attribution."
        "</p>",
        unsafe_allow_html=True,
    )

    # Initialize
    rag, vs, courses, docs = initialize_system()

    if rag is None:
        st.error("❌ No course materials found. Please add files to the 'Course files' directory.")
        return

    # ── Sidebar ──────────────────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Settings")

        # Course filter
        course_options = ["All Courses"] + courses
        selected_course = st.selectbox("📂 Filter by Course", course_options)

        # Number of results
        top_k = st.slider("🔎 Number of chunks to retrieve", 1, 10, 5)

        st.divider()

        # Knowledge base stats
        st.header("📊 Knowledge Base Stats")
        col1, col2 = st.columns(2)
        col1.metric("Documents", len(docs))
        col2.metric("Chunks", vs.count())

        st.divider()

        st.header("📁 Loaded Files")
        for d in docs:
            st.markdown(
                f"<div class='source-card'>"
                f"<strong>{d['source']}</strong><br>"
                f"<small>📘 {d['course']} &nbsp;|&nbsp; 📄 {d['file_type']}</small>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.divider()

        # Rebuild button
        if st.button("🔄 Rebuild Knowledge Base", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()

    # ── Chat Interface ───────────────────────────────────────────────
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander("📎 Sources"):
                    for s in msg["sources"]:
                        st.markdown(f"- **{s['file']}** ({s['course']}) [{s['type']}]")
            if "chunks" in msg and msg["chunks"]:
                with st.expander("📄 Retrieved Chunks"):
                    for i, c in enumerate(msg["chunks"], 1):
                        st.markdown(
                            f"<div class='chunk-card'>"
                            f"<strong>Chunk {i}</strong> — {c['source']} "
                            f"<em>(distance: {c['distance']:.4f})</em><br><br>"
                            f"{c['text'][:300]}{'…' if len(c['text']) > 300 else ''}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

    # Question input
    question = st.chat_input("Ask a question about your courses…")

    if question:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Generate answer
        with st.chat_message("assistant"):
            with st.spinner("Searching course materials and generating answer…"):
                result = rag.answer(
                    question=question,
                    course_filter=selected_course,
                    top_k=top_k,
                )

            # Display answer
            st.markdown(result["answer"])

            # Display sources
            if result["sources"]:
                with st.expander("📎 Sources", expanded=True):
                    for s in result["sources"]:
                        st.markdown(f"- **{s['file']}** ({s['course']}) [{s['type']}]")

            # Display retrieved chunks
            if result["retrieved_chunks"]:
                with st.expander("📄 Retrieved Chunks"):
                    for i, c in enumerate(result["retrieved_chunks"], 1):
                        st.markdown(
                            f"<div class='chunk-card'>"
                            f"<strong>Chunk {i}</strong> — {c['source']} "
                            f"<em>(distance: {c['distance']:.4f})</em><br><br>"
                            f"{c['text'][:300]}{'…' if len(c['text']) > 300 else ''}"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
            "chunks": result["retrieved_chunks"],
        })

    # ── Example Questions ────────────────────────────────────────────
    if not st.session_state.messages:
        st.markdown("### 💡 Example Questions")
        example_cols = st.columns(3)
        examples = [
            ("Machine Learning", [
                "What is overfitting and how can it be prevented?",
                "Explain the bias-variance tradeoff.",
                "What are ensemble methods?",
            ]),
            ("Data Science", [
                "How do you handle missing data in Pandas?",
                "What is the data science workflow?",
                "Explain the groupby operation in Pandas.",
            ]),
            ("NLP", [
                "What is the Transformer architecture?",
                "Explain the difference between BERT and GPT.",
                "What are word embeddings?",
            ]),
        ]
        for col, (topic, questions) in zip(example_cols, examples):
            with col:
                st.markdown(f"**📘 {topic}**")
                for q in questions:
                    if st.button(q, key=q, use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": q})
                        st.rerun()


if __name__ == "__main__":
    main()

