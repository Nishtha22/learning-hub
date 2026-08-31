"""
STEP 4: Vector Search with LangChain FAISS
Learn how LangChain makes vector search incredibly simple!
"""

import json
from pathlib import Path
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def build_faiss_index_with_langchain(chunks_file: Path, output_dir: Path):
    """
    Build FAISS index using LangChain.
    
    Compare to manual FAISS:
    - Manual: 50+ lines of numpy, faiss operations
    - LangChain: 5 lines!
    """
    print("\n" + "=" * 80)
    print("🔍 BUILDING FAISS INDEX WITH LANGCHAIN")
    print("=" * 80)
    
    # Load chunks
    print(f"\n📂 Loading chunks from: {chunks_file}")
    with open(chunks_file) as f:
        chunks = json.load(f)
    
    print(f"✅ Loaded {len(chunks)} chunks")
    
    # Initialize embeddings
    print("\n🔧 Initializing embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✅ Embeddings ready")
    
    # Prepare documents for LangChain
    print("\n📄 Preparing documents...")
    documents = []
    for chunk in chunks:
        doc = Document(
            page_content=chunk['text'],
            metadata=chunk['metadata']
        )
        documents.append(doc)
    
    print(f"✅ Prepared {len(documents)} documents")
    
    # Build FAISS index (THIS IS MAGIC - ONE LINE!)
    print("\n🚀 Building FAISS index...")
    print("   (This is where LangChain shines - watch!)")
    
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )
    
    print("✅ FAISS index built!")
    
    # Save index
    output_dir.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(output_dir / "faiss_langchain"))
    
    print(f"\n💾 Index saved to: {output_dir / 'faiss_langchain'}")
    
    return vectorstore

def demonstrate_vector_search(vectorstore: FAISS):
    """Demonstrate different search methods."""
    print("\n" + "=" * 80)
    print("🔍 DEMONSTRATING VECTOR SEARCH")
    print("=" * 80)
    
    test_queries = [
        "How to cache DataFrame in Spark?",
        "Spark performance tuning best practices",
        "Reading CSV files in Spark"
    ]
    
    for query in test_queries:
        print("\n" + "-" * 80)
        print(f"📝 Query: {query}")
        print("-" * 80)
        
        # Method 1: similarity_search (most common)
        print("\n1️⃣  similarity_search (top 3)")
        results = vectorstore.similarity_search(query, k=3)
        
        for i, doc in enumerate(results, 1):
            print(f"\n  [{i}] {doc.page_content[:100]}...")
            print(f"      Source: {doc.metadata.get('source_url', 'Unknown')}")
        
        # Method 2: similarity_search_with_score
        print("\n2️⃣  similarity_search_with_score (with scores)")
        results_with_scores = vectorstore.similarity_search_with_score(query, k=3)
        
        for i, (doc, score) in enumerate(results_with_scores, 1):
            print(f"\n  [{i}] Score: {score:.4f}")
            print(f"      {doc.page_content[:80]}...")
        
        # Method 3: max_marginal_relevance_search (diverse results)
        print("\n3️⃣  max_marginal_relevance_search (diverse)")
        mmr_results = vectorstore.max_marginal_relevance_search(query, k=3)
        
        for i, doc in enumerate(mmr_results, 1):
            print(f"\n  [{i}] {doc.page_content[:80]}...")

def interactive_search(vectorstore: FAISS):
    """Interactive search mode."""
    print("\n" + "=" * 80)
    print("🎮 INTERACTIVE SEARCH MODE")
    print("=" * 80)
    print("Ask your questions! (Type 'quit' to exit)\n")
    
    while True:
        print("-" * 80)
        query = input("\n💬 Your question: ").strip()
        
        if not query:
            continue
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        # Search
        results = vectorstore.similarity_search_with_score(query, k=5)
        
        print("\n🔍 Search Results:")
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n[{i}] Similarity Score: {score:.4f}")
            print(f"    Source: {doc.metadata.get('source_url', 'Unknown')}")
            print(f"    Text: {doc.page_content[:200]}...")

def main():
    print("\n" + "=" * 80)
    print("🦜 STEP 4: VECTOR SEARCH WITH LANGCHAIN")
    print("=" * 80)
    
    chunks_file = Path("data/step3/chunks_with_embeddings.json")
    output_dir = Path("data/step4")
    
    if not chunks_file.exists():
        print(f"\n❌ ERROR: {chunks_file} not found!")
        print("   Run step3_embeddings.py first!")
        return
    
    # Build index
    vectorstore = build_faiss_index_with_langchain(chunks_file, output_dir)
    
    # Demonstrate search
    input("\n👉 Press Enter to see search demonstrations...")
    demonstrate_vector_search(vectorstore)
    
    # Interactive mode
    input("\n👉 Press Enter to try interactive search...")
    interactive_search(vectorstore)
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("🎓 WHAT YOU LEARNED")
    print("=" * 80)
    print("""
✅ LangChain FAISS wrapper is INCREDIBLY simple
✅ from_documents() builds index in ONE line
✅ Multiple search methods: similarity, MMR, etc.
✅ Automatic score normalization
✅ Easy to save and load indices
✅ 90% less code than manual FAISS!

Search Methods:
- similarity_search: Standard vector search
- similarity_search_with_score: With relevance scores
- max_marginal_relevance_search: Diverse results

Next: Step 5 - Complete RAG with LangChain Chains
""")

if __name__ == "__main__":
    main()