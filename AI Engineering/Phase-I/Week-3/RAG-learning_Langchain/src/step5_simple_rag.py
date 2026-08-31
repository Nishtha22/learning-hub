"""
STEP 5: Complete RAG with LangChain
This is where LangChain REALLY shines - complete RAG in ~30 lines!
"""

from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

def build_rag_system():
    """
    Build complete RAG system using LangChain.
    
    Compare to manual approach:
    - Manual: 200+ lines (embedder, retriever, prompt builder, LLM wrapper)
    - LangChain: 30 lines!
    """
    print("\n" + "=" * 80)
    print("🦜 BUILDING RAG SYSTEM WITH LANGCHAIN")
    print("=" * 80)
    
    # 1. Load embeddings
    print("\n🔧 Loading embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-base-en-v1.5",
        model_kwargs={'device': 'cpu'}
    )
    print("✅ Embeddings loaded")
    
    # 2. Load vector store
    print("\n📂 Loading vector store...")
    vectorstore = FAISS.load_local(
        "data/step4/faiss_langchain",
        embeddings,
        allow_dangerous_deserialization=True
    )
    print(f"✅ Vector store loaded ({vectorstore.index.ntotal} vectors)")
    
    # 3. Initialize LLM
    print("\n🤖 Initializing LLM (Ollama)...")
    llm = Ollama(
        model="llama3.2",
        temperature=0.1
    )
    print("✅ LLM initialized")
    
    # 4. Create custom prompt
    print("\n📝 Creating prompt template...")
    prompt_template = """You are a helpful assistant for Apache Spark documentation.

Use the following context to answer the question. If you don't know the answer based on the context, say so. Always cite your sources using [Source N] notation.

Context:
{context}

Question: {question}

Answer (cite sources):"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    print("✅ Prompt template created")
    
    # 5. Create RAG chain (THIS IS THE MAGIC!)
    print("\n⛓️  Building RAG chain...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" puts all docs into context
        retriever=vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    print("✅ RAG chain ready!")
    
    return qa_chain

def demonstrate_rag(qa_chain):
    """Demonstrate RAG with example questions."""
    print("\n" + "=" * 80)
    print("🧪 DEMONSTRATING RAG")
    print("=" * 80)
    
    example_questions = [
        "How do I cache a DataFrame in Spark?",
        "What are the best practices for Spark performance tuning?",
        "How do I read a CSV file in PySpark?"
    ]
    
    for i, question in enumerate(example_questions, 1):
        print("\n" + "=" * 80)
        print(f"QUESTION {i}: {question}")
        print("=" * 80)
        
        # Query the RAG chain (ONE LINE!)
        result = qa_chain({"query": question})
        
        # Display answer
        print("\n💬 ANSWER:")
        print("-" * 80)
        print(result['result'])
        print("-" * 80)
        
        # Display sources
        print("\n📚 SOURCES:")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f"  [{i}] {doc.metadata.get('source_url', 'Unknown')}")
        
        if i < len(example_questions):
            input("\n👉 Press Enter for next question...")

def interactive_rag(qa_chain):
    """Interactive RAG mode."""
    print("\n" + "=" * 80)
    print("🎮 INTERACTIVE RAG MODE")
    print("=" * 80)
    print("Ask your questions! (Type 'quit' to exit)\n")
    
    while True:
        print("-" * 80)
        question = input("\n💬 Your question: ").strip()
        
        if not question:
            continue
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        try:
            # Query (ONE LINE!)
            print("\n🔍 Searching and generating answer...\n")
            result = qa_chain({"query": question})
            
            # Display
            print("=" * 80)
            print("💬 ANSWER:")
            print("=" * 80)
            print(result['result'])
            print("=" * 80)
            
            print("\n📚 SOURCES:")
            for i, doc in enumerate(result['source_documents'], 1):
                source = doc.metadata.get('source_url', 'Unknown')
                print(f"  [{i}] {source}")
                print(f"      {doc.page_content[:80]}...")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   Make sure Ollama is running: ollama serve")

def main():
    print("\n" + "=" * 80)
    print("🦜 STEP 5: COMPLETE RAG WITH LANGCHAIN")
    print("=" * 80)
    
    # Check prerequisites
    index_path = Path("data/step4/faiss_langchain")
    if not index_path.exists():
        print(f"\n❌ ERROR: FAISS index not found at {index_path}")
        print("   Run step4_vector_search.py first!")
        return
    
    # Build RAG system
    print("\n🚀 Initializing RAG system...")
    try:
        qa_chain = build_rag_system()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nMake sure:")
        print("  1. Ollama is running: ollama serve")
        print("  2. Model is pulled: ollama pull llama3.2")
        return
    
    # Demonstrate with examples
    input("\n👉 Press Enter to see example questions...")
    demonstrate_rag(qa_chain)
    
    # Interactive mode
    input("\n👉 Press Enter to try interactive mode...")
    interactive_rag(qa_chain)
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("🎓 WHAT YOU LEARNED")
    print("=" * 80)
    print("""
✅ LangChain makes RAG INCREDIBLY simple
✅ RetrievalQA chain handles everything automatically
✅ Custom prompts with PromptTemplate
✅ Automatic source tracking
✅ from_chain_type() builds complete pipeline
✅ Total code: ~30 lines vs 200+ manual!

RAG Chain Components:
- LLM: Ollama (local, free)
- Retriever: FAISS vector store
- Prompt: Custom template
- Chain: RetrievalQA

Key Methods:
- qa_chain({"query": "..."}) - Query the system
- return_source_documents=True - Get sources
- search_kwargs={"k": 5} - Retrieve top 5 docs

Next: Step 6 - Advanced RAG (Memory, Agents)
""")

if __name__ == "__main__":
    main()