"""
STEP 3: Embeddings with LangChain
Learn how LangChain simplifies embedding generation.
"""

import json
from pathlib import Path
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings


class LangChainEmbedder:
    """
    Wrapper around LangChain's HuggingFaceEmbeddings.
    
    Advantages over raw SentenceTransformer:
    - Consistent interface
    - Easy to swap models
    - Built-in caching
    - Better error handling
    """
    
    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        print(f"🔧 Loading embedding model: {model_name}")
        
        # Initialize LangChain embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}  # For cosine similarity
        )
        
        # Test to get dimension
        test_embedding = self.embeddings.embed_query("test")
        self.dimension = len(test_embedding)
        
        print(f"✅ Model loaded. Dimension: {self.dimension}")
        
    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        
        LangChain distinguishes between:
        - embed_query: For search queries
        - embed_documents: For documents to be stored
        
        Some models use different prompts for each!
        """
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple documents.
        
        LangChain handles batching automatically!
        """
        print(f"\n📊 Generating embeddings for {len(texts)} documents...")
        
        # LangChain's batch method
        embeddings = self.embeddings.embed_documents(texts)
        
        print(f"✅ Generated {len(embeddings)} embeddings")
        return embeddings


def process_chunks_with_embeddings(input_file: Path, output_dir: Path):
    """Process chunks and add embeddings using LangChain."""
    print("\n" + "=" * 80)
    print("GENERATING EMBEDDINGS WITH LANGCHAIN")
    print("=" * 80)
    
    # Load chunks
    print(f"\n📂 Loading chunks from: {input_file}")
    with open(input_file) as f:
        chunks = json.load(f)
    
    print(f"✅ Loaded {len(chunks)} chunks")
    
    # Initialize embedder
    embedder = LangChainEmbedder()
    
    # Extract texts
    texts = [chunk['text'] for chunk in chunks]
    
    # Generate embeddings (ONE LINE!)
    embeddings = embedder.embed_documents(texts)
    
    # Add embeddings to chunks
    for chunk, embedding in zip(chunks, embeddings):
        chunk['embedding'] = embedding
    
    # Save
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / 'chunks_with_embeddings.json'
    
    print(f"\n💾 Saving chunks with embeddings to: {output_file}")
    with open(output_file, 'w') as f:
        json.dump(chunks, f, indent=2)
    
    print(f"\n📊 File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
    
    return chunks

def main():
    print("\n" + "=" * 80)
    print("🦜 STEP 3: EMBEDDINGS WITH LANGCHAIN")
    print("=" * 80)
    

    
    # Then, process real chunks
    input("\n👉 Press Enter to embed actual chunks...")
    
    input_file = Path("data/step2/chunks_langchain_500.json")
    output_dir = Path("data/step3")
    
    if not input_file.exists():
        print(f"\n❌ ERROR: {input_file} not found!")
        print("   Run step2_basic_chunking.py first!")
        return
    
    chunks = process_chunks_with_embeddings(input_file, output_dir)
    
    if chunks:
        print("\n" + "=" * 80)
        print("✅ COMPLETE!")
        print("=" * 80)
        
        print("\n" + "=" * 80)
        print("🎓 WHAT YOU LEARNED")
        print("=" * 80)
        print("""
✅ LangChain provides HuggingFaceEmbeddings wrapper
✅ Distinguishes between queries and documents
✅ Handles batching automatically
✅ Easy to swap embedding models
✅ Simpler than raw SentenceTransformer

Next: Step 4 - Vector Search with LangChain FAISS
""")

if __name__ == "__main__":
    main()