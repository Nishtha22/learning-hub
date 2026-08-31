"""
STEP 6: Advanced RAG with LangChain
Learn about conversational RAG with memory and agents!
"""

from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

def build_conversational_rag():
    """
    Build RAG with conversation memory.
    
    This allows follow-up questions like:
    - User: "How to cache DataFrame?"
    - Bot: "Use .cache() method..."
    - User: "What about persist?"  ← Remembers context!
    """
    print("\n" + "=" * 80)
    print("🧠 BUILDING CONVERSATIONAL RAG")
    print("=" * 80)
    
    # Load components
    print("\n🔧 Loading components...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    vectorstore = FAISS.load_local("data/step4/faiss_langchain", embeddings)
    llm = Ollama(model="llama3.2", temperature=0.1)
    
    # Create memory
    print("\n🧠 Creating conversation memory...")
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    # Create conversational chain
    print("\n⛓️  Building conversational chain...")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        memory=memory,
        return_source_documents=True,
        verbose=False
    )
    
    print("✅ Conversational RAG ready!")
    return qa_chain

def demonstrate_conversation(qa_chain):
    """Demonstrate conversation with memory."""
    print("\n" + "=" * 80)
    print("💬 CONVERSATIONAL RAG DEMONSTRATION")
    print("=" * 80)
    
    conversation = [
        "How do I cache a DataFrame in Spark?",
        "What's the difference between cache and persist?",
        "When should I use it?",  # "it" refers to caching!
        "Can you show me an example?"
    ]
    
    for i, question in enumerate(conversation, 1):
        print(f"\n{'='*80}")
        print(f"TURN {i}: {question}")
        print("="*80)
        
        result = qa_chain({"question": question})
        
        print("\n💬 ANSWER:")
        print("-"*80)
        print(result['answer'])
        print("-"*80)
        
        if i < len(conversation):
            input("\n👉 Press Enter for next turn...")
    
    print("\n" + "=" * 80)
    print("🎓 NOTICE HOW IT REMEMBERS CONTEXT!")
    print("=" * 80)
    print("""
Question 3 said "When should I use IT?"
- "IT" refers to caching from previous questions
- The chain remembered the conversation history
- This is possible because of ConversationBufferMemory!
""")

def interactive_conversational_rag(qa_chain):
    """Interactive mode with conversation memory."""
    print("\n" + "=" * 80)
    print("🎮 INTERACTIVE CONVERSATIONAL RAG")
    print("=" * 80)
    print("Ask questions - I'll remember our conversation!")
    print("(Type 'quit' to exit, 'clear' to reset memory)\n")
    
    while True:
        print("-" * 80)
        question = input("\n💬 You: ").strip()
        
        if not question:
            continue
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if question.lower() == 'clear':
            qa_chain.memory.clear()
            print("🧹 Memory cleared!")
            continue
        
        try:
            result = qa_chain({"question": question})
            
            print("\n🤖 Assistant:")
            print(result['answer'])
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    print("\n" + "=" * 80)
    print("🦜 STEP 6: ADVANCED RAG WITH LANGCHAIN")
    print("=" * 80)
    
    # Build conversational RAG
    try:
        qa_chain = build_conversational_rag()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return
    
    # Demonstrate
    input("\n👉 Press Enter to see conversation demonstration...")
    demonstrate_conversation(qa_chain)
    
    # Interactive
    input("\n👉 Press Enter to try it yourself...")
    interactive_conversational_rag(qa_chain)
    
    print("\n" + "=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    
    print("\n" + "=" * 80)
    print("🎓 WHAT YOU LEARNED")
    print("=" * 80)
    print("""
✅ ConversationalRetrievalChain adds memory
✅ Remembers conversation history
✅ Can handle follow-up questions
✅ ConversationBufferMemory stores chat history
✅ Perfect for chatbot interfaces

Advanced Features:
- Memory: Remembers conversation
- Context: Understands references (it, that, etc.)
- Follow-ups: Natural conversation flow

Memory Types:
- ConversationBufferMemory: Stores all messages
- ConversationSummaryMemory: Summarizes old messages
- ConversationBufferWindowMemory: Keeps last N messages

🎉 CONGRATULATIONS!
You've completed the LangChain RAG Learning Path!

You now know:
✅ Text splitting with LangChain
✅ Embeddings with LangChain
✅ Vector stores with LangChain
✅ RAG chains with LangChain
✅ Conversational RAG with memory
✅ How LangChain simplifies RAG by 70%!
""")

if __name__ == "__main__":
    main()