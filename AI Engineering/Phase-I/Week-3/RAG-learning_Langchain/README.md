# RAG Learning — LangChain Examples

This repository contains step-by-step code for building a simple Retrieval-Augmented Generation (RAG) pipeline using LangChain, FAISS, and embeddings.

Quick overview
- Data: `data/` contains example documents and intermediate chunk files.
- Code: `src/` contains the step-by-step Python scripts (`step1_fetch_docs.py` through `step6_advanced_rag.py`).

Prerequisites
- Python 3.9+ recommended
- A virtual environment (venv) or conda environment
- Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Running the examples
1. Prepare documents: `python src/step1_fetch_docs.py`
2. Chunk documents: `python src/step2_basic_chunking.py`
3. Create embeddings: `python src/step3_embeddings.py`
4. Build vector search index: `python src/step4_vector_search.py`
5. Try simple RAG: `python src/step5_simple_rag.py`
6. Advanced RAG: `python src/step6_advanced_rag.py`

Project structure

```
.
├── data/                      # source docs and intermediate chunk files
├── src/                       # step scripts
└── requirements.txt
```

