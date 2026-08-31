"""
STEP 2: Text Chunking with LangChain
Learn LangChain's text splitters - much easier than manual chunking!
"""

from pathlib import Path
from typing import List
import json

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)
from langchain_core.documents import Document

def demonstrate_text_splitters():
    """
    Demonstrate different LangChain text splitters.
    """
    print("\n" + "=" * 80)
    print("🔍 EXPLORING LANGCHAIN TEXT SPLITTERS")
    print("=" * 80)
    
    sample_text = """
Apache Spark is a unified analytics engine for large-scale data processing.
It provides high-level APIs in Java, Scala, Python and R.
Spark's advanced DAG execution engine supports acyclic data flow.

DataFrames in Spark provide a powerful API for data manipulation.
You can cache DataFrames using the cache() or persist() methods.
This significantly improves performance for iterative algorithms.

Performance tuning in Spark involves several key considerations.
Memory management is crucial for optimal performance.
Partitioning strategies can dramatically impact job execution time.
"""
    
    # 1. RecursiveCharacterTextSplitter (BEST - Default choice)
    print("\n1️⃣  RecursiveCharacterTextSplitter (Recommended)")
    print("-" * 80)
    
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # Try these in order
    )
    
    recursive_chunks = recursive_splitter.split_text(sample_text)
    
    print(f"Number of chunks: {len(recursive_chunks)}")
    for i, chunk in enumerate(recursive_chunks, 1):
        print(f"\nChunk {i} ({len(chunk)} chars):")
        print(chunk[:100] + "..." if len(chunk) > 100 else chunk)
    
    # 2. CharacterTextSplitter (Simple)
    print("\n\n2️⃣  CharacterTextSplitter (Simple)")
    print("-" * 80)
    
    char_splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        separator="\n\n"  # Split only on double newlines
    )
    
    char_chunks = char_splitter.split_text(sample_text)
    
    print(f"Number of chunks: {len(char_chunks)}")
    
    # 3. TokenTextSplitter (Token-based)
    print("\n\n3️⃣  TokenTextSplitter (Token-aware)")
    print("-" * 80)
    
    token_splitter = TokenTextSplitter(
        chunk_size=100,  # 100 tokens
        chunk_overlap=10
    )
    
    token_chunks = token_splitter.split_text(sample_text)
    
    print(f"Number of chunks: {len(token_chunks)}")
    
    print("\n" + "=" * 80)
    print("📝 KEY INSIGHTS")
    print("=" * 80)
    print("""
RecursiveCharacterTextSplitter (RECOMMENDED):
- Tries multiple separators in order
- Respects natural text boundaries
- Best for general use

CharacterTextSplitter:
- Simple, uses single separator
- Good for structured text (markdown, etc.)

TokenTextSplitter:
- Counts actual tokens
- Best when token count matters (LLM limits)
""")

def process_documents_with_langchain(
    input_dir: Path,
    output_dir: Path,
    chunk_size: int = 500,
    chunk_overlap: int = 50
):
    """
    Process documents using LangChain's RecursiveCharacterTextSplitter.
    
    This is MUCH simpler than manual chunking!
    """
    print("\n" + "=" * 80)
    print(f"CHUNKING DOCUMENTS (chunk_size={chunk_size}, overlap={chunk_overlap})")
    print("=" * 80)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    doc_files = sorted(input_dir.glob("*.txt"))
    
    if not doc_files:
        print(f"❌ No documents found in {input_dir}")
        print("   Run step1_fetch_docs.py first!")
        return []
    
    print(f"\n📚 Found {len(doc_files)} documents")
    
    # Initialize LangChain splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []
    
    for doc_file in doc_files:
        print(f"\n📄 Processing: {doc_file.name}")
        
        # Read document
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract source URL
        lines = content.split('\n')
        source_url = lines[0].replace('SOURCE: ', '') if lines else "unknown"
        text = '\n'.join(lines[3:])  # Skip header
        
        # Create LangChain Document
        doc = Document(
            page_content=text,
            metadata={
                'source_url': source_url,
                'source_file': doc_file.name
            }
        )
        
        # Split using LangChain (ONE LINE!)
        chunks = text_splitter.split_documents([doc])
        
        print(f"  📊 Created {len(chunks)} chunks")
        
        # Convert to our format
        for i, chunk in enumerate(chunks):
            chunk_data = {
                'id': f"{doc_file.stem}_chunk_{i:03d}",
                'text': chunk.page_content,
                'metadata': {
                    'source_url': source_url,
                    'source_file': doc_file.name,
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'char_count': len(chunk.page_content)
                }
            }
            all_chunks.append(chunk_data)
    
    # Save chunks
    output_file = output_dir / f'chunks_langchain_{chunk_size}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Statistics:")
    print(f"   Total chunks: {len(all_chunks)}")
    avg_chars = sum(c['metadata']['char_count'] for c in all_chunks) / len(all_chunks)
    print(f"   Average chars per chunk: {avg_chars:.1f}")
    print(f"   Output file: {output_file}")
    
    return all_chunks

def main():
    print("\n" + "=" * 80)
    print("🦜 STEP 2: TEXT CHUNKING WITH LANGCHAIN")
    print("=" * 80)
    
    # First, demonstrate different splitters
    demonstrate_text_splitters()
    
    # Then, process real documents
    input("\n👉 Press Enter to process actual documents...")
    
    # Use absolute path from script location
    script_dir = Path(__file__).parent
    input_dir = script_dir / "data/step1"
    output_dir = script_dir / "data/step2"
    
    chunks = process_documents_with_langchain(
        input_dir,
        output_dir,
        chunk_size=500,
        chunk_overlap=50
    )
    
    if chunks:
        print("\n" + "=" * 80)
        print("🎓 WHAT YOU LEARNED")
        print("=" * 80)
        print("""
✅ LangChain provides multiple text splitters
✅ RecursiveCharacterTextSplitter is the best general choice
✅ It respects natural text boundaries (paragraphs, sentences)
✅ Much simpler than manual chunking (few lines vs 100+ lines!)
✅ Consistent, well-tested implementation

Next: Step 3 - Embeddings with LangChain
""")

if __name__ == "__main__":
    main()