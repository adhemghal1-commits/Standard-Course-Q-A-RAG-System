# 📚 Course Q&A – Standard RAG System

A Retrieval-Augmented Generation (RAG) system that answers student questions based on course materials from multiple file types (PDF, CSV, DOCX, TXT).

## 🏗️ Architecture

```
Course Materials (PDF/CSV/DOCX/TXT)
         │
    ┌────▼────┐
    │ Document │  ← Extract text from all file types
    │  Loader  │
    └────┬────┘
         │
    ┌────▼────────┐
    │    Text      │  ← Clean & chunk text (500 chars, 100 overlap)
    │  Processing  │
    └────┬────────┘
         │
    ┌────▼──────────┐
    │  Embeddings    │  ← sentence-transformers/all-MiniLM-L6-v2
    │  + ChromaDB    │  ← Persistent vector database
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │  RAG Pipeline  │  ← Retrieve top-k chunks → LLM generates answer
    │  (flan-t5-base)│
    └────┬──────────┘
         │
    ┌────▼──────────┐
    │  Streamlit UI  │  ← Chat interface with source attribution
    └───────────────┘
```

## 📁 Project Structure

```
Project Standard Course Q&A RAG System/
├── app.py                      # Streamlit web application
├── config.py                   # Configuration settings
├── document_loader.py          # Extract text from PDF/CSV/DOCX/TXT
├── text_processing.py          # Text chunking with LangChain
├── vector_store.py             # ChromaDB embeddings & retrieval
├── rag_pipeline.py             # RAG pipeline (retriever + LLM)
├── create_sample_materials.py  # Generate sample course materials
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── Course files/               # Course materials directory
│   ├── lecture 1 (1).pdf       # ML Fundamentals lectures (PDF)
│   ├── Lecture 2 (1).pdf
│   ├── Lecture 3.pdf
│   ├── Lecture 4.pdf
│   ├── Lecture 5.pdf
│   ├── ML_fundamentals_notes.txt
│   ├── ML_algorithms_reference.csv
│   ├── DS_Python_course_materials.csv
│   ├── DS_Python_notes.txt
│   ├── NLP_course_materials.docx
│   ├── NLP_glossary.csv
│   └── NLP_reference_notes.txt
└── vector_store/               # ChromaDB persistent storage (auto-created)
```

## 📋 Courses Covered

| # | Course | File Types | Description |
|---|--------|-----------|-------------|
| 1 | **Machine Learning Fundamentals** | PDF, TXT, CSV | Supervised/unsupervised learning, model evaluation, ensemble methods, regularization |
| 2 | **Data Science with Python** | CSV, TXT | Pandas, visualization, statistics, data cleaning, feature engineering |
| 3 | **Natural Language Processing** | DOCX, CSV, TXT | Text preprocessing, word embeddings, Transformers, BERT, GPT |

## 🚀 Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Materials (CSV, DOCX, TXT)
```bash
python create_sample_materials.py
```

### 3. Launch the App
```bash
streamlit run app.py
```

The app will:
1. Load all course materials from the `Course files/` directory
2. Extract and clean text from each file
3. Chunk the text into smaller pieces
4. Create embeddings and store them in ChromaDB
5. Start the Streamlit chat interface

## 🔧 Key Components

### Document Loader (`document_loader.py`)
- **PDF**: Uses PyPDF2 to extract text from all pages
- **CSV**: Joins all cells into readable text entries
- **DOCX**: Uses python-docx to extract paragraph text
- **TXT**: Direct text reading
- Auto-detects course from filename keywords

### Text Processing (`text_processing.py`)
- Uses LangChain's `RecursiveCharacterTextSplitter`
- Chunk size: 500 characters with 100-character overlap
- Smart splitting on paragraphs, sentences, and words

### Vector Store (`vector_store.py`)
- Embedding model: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional)
- Database: ChromaDB with persistent storage
- Cosine similarity for retrieval
- Supports filtering by course

### RAG Pipeline (`rag_pipeline.py`)
- Retrieves top-k relevant chunks
- Builds context-aware prompt
- Generates answers using `google/flan-t5-base`
- Returns answer with source attribution

### Streamlit App (`app.py`)
- Chat-based interface
- Course filter in sidebar
- Adjustable number of retrieved chunks
- Expandable source citations and retrieved chunks
- Knowledge base statistics
- Example questions for each course

## ⚙️ Configuration

Edit `config.py` to customize:
- `CHUNK_SIZE` / `CHUNK_OVERLAP` – text chunking parameters
- `EMBEDDING_MODEL_NAME` – sentence-transformers model
- `RETRIEVER_TOP_K` – number of chunks to retrieve
- `COURSE_KEYWORDS` – filename patterns for course detection

## 📝 Notes

- **No API key required** – uses local models (sentence-transformers + flan-t5-base)
- First run downloads models (~500 MB) which are cached locally
- ChromaDB index is persisted to `vector_store/` and reused across sessions
- Click "🔄 Rebuild Knowledge Base" in the sidebar to re-index after adding new files

