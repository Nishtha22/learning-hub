# RAG Pipeline: Step 2-5 Comprehensive Guide

## Overview
This document explains the RAG (Retrieval-Augmented Generation) pipeline from text chunking to complete Q&A system with LangChain.

---

## STEP 2: TEXT CHUNKING WITH LANGCHAIN

### What are we doing?
Breaking large documents into smaller, manageable chunks that can be embedded and searched effectively.

### Why chunking matters
- Documents are too large to embed as a whole
- Chunks should be small enough for relevant context but large enough to be meaningful
- Overlapping chunks help capture context across boundaries

### How we're doing it

**Tool Used:** `RecursiveCharacterTextSplitter` (from langchain_text_splitters)

**Key Parameters:**
- `chunk_size=500`: Each chunk is ~500 characters
- `chunk_overlap=50`: 50 character overlap between consecutive chunks (prevents losing context at boundaries)
- `separators=["\n\n", "\n", ". ", " ", ""]`: Try these separators in order
  - First try splitting on double newlines (paragraph breaks)
  - Then single newlines
  - Then sentences
  - Then words
  - Finally, characters as last resort

**Why this approach?**
- Respects natural text boundaries (paragraphs → sentences → words)
- Prevents splitting meaningful content
- Better for semantic search later

### Output
- File: `data/step2/chunks_langchain_500.json`
- Contains: List of chunks with metadata (source, file name, char count)
- Format:
```json
{
  "id": "doc_001_chunk_000",
  "text": "chunk content here...",
  "metadata": {
    "source_url": "source URL",
    "source_file": "doc_001.txt",
    "chunk_index": 0,
    "total_chunks": 45,
    "char_count": 487
  }
}
```

---

## STEP 3: EMBEDDINGS WITH LANGCHAIN

### What are we doing?
Converting text chunks into numerical vectors (embeddings) that capture semantic meaning.

### Why embeddings matter
- Embeddings represent meaning in a vector space
- Similar texts have embeddings close to each other
- Enable semantic search (not just keyword matching)

### Embedding Model Used

**Model:** `BAAI/bge-base-en-v1.5` (Hugging Face)

**Why this model?**
- Lightweight and fast
- Good semantic understanding (768-dimensional vectors)
- Works well for document retrieval
- Free and runs locally (no API calls)
- Already optimized for BGE (Bidirectional General Embedding)

**Model Details:**
- **Dimension:** 768 (each chunk becomes a 768-element vector)
- **Type:** Dense embeddings (as opposed to sparse)
- **Normalization:** L2-normalized (unit vectors)
- **Use Cases:** Document retrieval, semantic search

### How embeddings are generated

Using `HuggingFaceEmbeddings` from LangChain:
```
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

**Key features:**
- `embed_documents()`: For indexing documents (one prompt style)
- `embed_query()`: For queries (different prompt style)
- LangChain handles batching automatically

### Output
- File: `data/step3/chunks_with_embeddings.json`
- Each chunk now has an `embedding` field with 768 floating-point values
- Example:
```json
{
  "id": "doc_001_chunk_000",
  "text": "...",
  "embedding": [0.023, -0.156, 0.089, ..., 0.042],  // 768 values
  "metadata": {...}
}
```

---

## STEP 4: VECTOR SEARCH WITH LANGCHAIN FAISS

### What are we doing?
Building an efficient search index from embeddings so we can quickly find similar documents.

### Why FAISS (Facebook AI Similarity Search)?
- **Fast:** Optimized C++ implementation
- **Scalable:** Handles millions of vectors
- **Local:** No API calls or remote dependencies
- **Free:** Open source
- **Efficient:** Multiple index types for speed/accuracy trade-offs

### How FAISS Embeds and Indexes Documents

**Important:** FAISS doesn't create embeddings - it receives pre-computed embeddings from Step 3!

#### Step-by-Step Embedding & Indexing Process

Using `FAISS.from_documents()`:
```python
vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embeddings  # Pre-computed 768D vectors
)
```

**What happens internally:**

1. **Receive Pre-computed Embeddings**
   - Each document already has a 768D embedding from Step 3
   - Example: doc_001_chunk_000 → [0.023, -0.156, 0.089, ..., 0.042]

2. **Normalize Vectors (L2 Normalization)**
   ```
   normalized_vec = original_vec / ||original_vec||
   where ||vec|| = sqrt(sum(vec[i]^2))
   ```
   - Converts vectors to unit length (magnitude = 1)
   - Allows cosine similarity to be computed as simple dot product
   - Result: All vectors on the surface of a unit hypersphere in 768D space

3. **Build FAISS Index Structure (IndexFlatIP)**
   - Stores all normalized vectors in a flat array
   - IndexFlatIP = Flat index with Inner Product metric
   - Internal structure:
     ```
     Index Memory Layout:
     [Vector 1: 768 floats] [Vector 2: 768 floats] ... [Vector N: 768 floats]
     Metadata Mapping:
     {
       "0": {"source": "doc_001.txt", "chunk_index": 0, ...},
       "1": {"source": "doc_001.txt", "chunk_index": 1, ...},
       ...
     }
     ```

4. **Store Document Metadata**
   - Maps vector index to original document content
   - Includes: source file, chunk index, source URL, etc.
   - Allows retrieval of original text after search

#### FAISS Index Type: IndexFlatIP

- **Type:** Flat (no compression or approximation)
- **Metric:** IP (Inner Product)
- **Why IP for normalized vectors?**
  - For L2-normalized vectors, cosine similarity = dot product
  - Cosine similarity formula: 
    ```
    cos(A, B) = (A · B) / (||A|| × ||B||)
    
    When ||A|| = ||B|| = 1 (normalized):
    cos(A, B) = A · B  (simple dot product!)
    ```
- **Exact vs Approximate:**
  - IndexFlatIP performs exhaustive search (checks all vectors)
  - Accuracy: 100% (exact results)
  - Speed: O(n) where n = number of vectors
  - Best for: datasets < 1 million vectors (which FAISS is optimized for)

#### How FAISS Stores Data in Memory

```
FAISS Index Structure:
├── index.faiss (binary file)
│   └── Contains:
│       - All normalized vectors (768 × num_chunks floats)
│       - Index metadata
│       - Dimension info (768)
│       - Total vector count
│
└── metadata pickle files
    └── Contains:
        - Mapping: vector_id → document info
        - Original text content
        - Metadata (source, timestamp, etc.)
```

**Memory Usage Example:**
- 500 chunks × 768 dimensions × 4 bytes per float = ~1.5 MB vectors
- + metadata overhead (~0.5-1 MB)
- **Total:** ~2-2.5 MB per 500 chunks

#### Why Separate Embedding from Indexing?

1. **Efficiency:** Embeddings computed once, indexed multiple times
2. **Flexibility:** Can use different embedding models, reindex with same model
3. **Clarity:** Separation of concerns (embedding ≠ search)
4. **Reusability:** Embeddings from Step 3 can be used with different vector DBs

#### During Search: How FAISS Uses Embeddings

```
Query: "How to cache DataFrame in Spark?"
    ↓
Step 1: Embed Query (using same model as indexing)
    query_embedding = embeddings.embed_query(query)
    → [0.045, -0.123, 0.089, ..., 0.067]  // 768D vector
    ↓
Step 2: Normalize Query Vector (L2)
    normalized_query = query_embedding / ||query_embedding||
    ↓
Step 3: Compute Similarity with All Indexed Vectors
    For each stored vector:
        similarity = dot_product(normalized_query, stored_vector)
    ↓
Step 4: Sort by Similarity Score
    results = sorted(similarities, reverse=True)[:k]
    ↓
Step 5: Return Top-K with Metadata
    [
        (doc_content_1, score: 0.87),
        (doc_content_2, score: 0.82),
        ...
    ]
```

### How Similarity is Calculated

**Similarity Metric: Cosine Similarity**

Formula:
```
similarity = dot_product(query_vec, doc_vec)
           = sum(query_vec[i] * doc_vec[i] for all i)
```

**Why Cosine Similarity?**
- Values between -1 and 1 (after normalization: 0 to 1)
- 1.0 = identical vectors
- 0.0 = orthogonal (completely different)
- 0.5-0.9 typically indicates good relevance
- Works in high-dimensional spaces (768D)

**Process:**
1. Query text comes in
2. Convert to embedding (768D vector)
3. Normalize the query vector (L2)
4. Compute dot product with all stored embeddings
5. Sort by highest scores
6. Return top-k results with scores

### Search Methods Available

1. **similarity_search(query, k=5)**
   - Returns top 5 most similar documents
   - No scores shown

2. **similarity_search_with_score(query, k=5)**
   - Returns documents + similarity scores
   - Scores range from 0-1 (higher = more similar)

3. **max_marginal_relevance_search(query, k=5)**
   - Returns diverse results
   - Balances relevance with diversity
   - Useful to avoid redundant results

### Output
- Files: `data/step4/faiss_langchain/` (directory with index files)
- Contains:
  - `index.faiss`: The vector index (binary format)
  - `.pkl` files: Pickle-serialized metadata and mappings
- Total vectors indexed: Number of chunks

---

## STEP 5: COMPLETE RAG WITH LANGCHAIN CHAINS

### What are we doing?
Building a complete Q&A system that combines:
1. Vector search (retrieval)
2. LLM (generation)
3. Prompt engineering

### Architecture

```
User Query
    ↓
Embed Query (using same model as step 3)
    ↓
Search Vector Store (FAISS similarity search)
    ↓
Retrieve top-5 relevant chunks
    ↓
Build Prompt with context + question
    ↓
Send to LLM (Ollama)
    ↓
Generate Answer
    ↓
Return to User
```

### Components

#### 1. Embeddings (same as Step 3)
```python
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    model_kwargs={'device': 'cpu'}
)
```

#### 2. Vector Store (FAISS from Step 4)
```python
vectorstore = FAISS.load_local(
    "data/step4/faiss_langchain",
    embeddings,
    allow_dangerous_deserialization=True
)
```
**Note:** `allow_dangerous_deserialization=True` needed for pickle files (safe for your own data)

#### 3. Retriever
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)
```
- Retrieves top-5 similar documents
- Similarity metric: cosine similarity

#### 4. LLM
```python
llm = Ollama(model="llama3.2", temperature=0.1)
```
**Local LLM via Ollama:**
- No API keys needed
- Runs on your machine
- `temperature=0.1`: Lower randomness (more deterministic answers)

#### 5. Prompt Template
```
Context: [Retrieved chunks]
Question: [User question]
Answer: [LLM generates this]
```
**Purpose:**
- Instructs LLM how to use context
- Tells LLM to cite sources
- Prevents hallucinations by grounding in context

#### 6. RAG Chain (RetrievalQA)
```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)
```

**Chain Type "stuff":**
- Puts all retrieved documents into the prompt
- Works well for small-medium context windows
- Alternative: "map_reduce" for very large contexts

### Complete Flow Example

**Input:** "How to cache DataFrame in Spark?"

**Step 1: Embed Query**
- Query → 768D vector

**Step 2: Search**
- Find top-5 chunks with highest cosine similarity
- Example scores: [0.87, 0.82, 0.79, 0.75, 0.71]

**Step 3: Retrieved Context**
```
[Source 1] doc_002.txt
Spark DataFrames can be cached using the cache() method...

[Source 2] doc_003.txt
The persist() method provides more control over cache storage...
```

**Step 4: Build Prompt**
```
Context: [Source 1 content], [Source 2 content], ...

Question: How to cache DataFrame in Spark?

Answer:
```

**Step 5: LLM Generates**
```
To cache a DataFrame in Spark, use the cache() method [Source 1]
or persist() for more control [Source 2]. This stores the 
DataFrame in memory for faster access in iterative workloads...
```

---

## Key Concepts Summary

| Concept | Used Where | Details |
|---------|-----------|---------|
| **Chunking** | Step 2 | Split docs into 500-char pieces with 50-char overlap |
| **Embedding Model** | Step 3 & 5 | BAAI/bge-base-en-v1.5 (768-dimensional) |
| **Vector DB** | Step 4 & 5 | FAISS with IndexFlatIP |
| **Similarity Metric** | Step 4 & 5 | Cosine similarity (dot product of normalized vectors) |
| **Retrieval Method** | Step 5 | Top-5 similarity search |
| **LLM** | Step 5 | Ollama with llama3.2 model |
| **Chain Type** | Step 5 | "stuff" (all docs in context) |

---

## Performance Considerations

### Chunk Size Trade-off
- **Smaller chunks (100-200):** More precise, but may miss context
- **Larger chunks (1000+):** More context, but slower search and retrieval
- **Sweet spot: 500:** Good balance for most use cases

### Similarity Score Interpretation
- **0.9-1.0:** Highly relevant
- **0.8-0.9:** Very relevant
- **0.7-0.8:** Relevant
- **0.6-0.7:** Somewhat relevant
- **<0.6:** Likely not relevant

### Why Top-5 Results?
- Too few (k=1-2): Miss relevant information
- Too many (k=10+): Include noise, slow down LLM
- k=5: Sweet spot for quality + speed

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Embeddings take long | First time model download | Model cached after first run |
| Pickle deserialization error | Security restriction | Set `allow_dangerous_deserialization=True` |
| LLM not responding | Ollama not running | Run `ollama serve` in terminal |
| Low relevance scores | Wrong model or poor chunks | Check chunk quality, try different model |
| Slow search | Many vectors | FAISS is optimized; should still be fast |

---

## Files Generated

```
data/
├── step2/
│   └── chunks_langchain_500.json        # Chunked text
├── step3/
│   └── chunks_with_embeddings.json      # Chunks + 768D vectors
├── step4/
│   └── faiss_langchain/
│       ├── index.faiss                  # Vector index (binary)
│       └── *.pkl                        # Metadata (pickle)
└── step5/
    └── (No files - interactive Q&A)
```

