"""
Full RAG Pipeline
1) User asks question
2) Convert to embedding (384D vector)
3) Search ChromaDB (semantic similarity)
4) Retrieve top 3 chunks (with metadata)
5) Build context prompt (system + context + query)
6) Generate with LLM (gpt-4.1-mini)
7) Return answer with sources
"""

#!/usr/bin/env python3
"""
Task 5: Complete RAG Pipeline
Wire everything together - Retrieve, Augment, Generate!
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_openai import ChatOpenAI

# Initialize all components
client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection("techcorp_rag")
model = SentenceTransformer("all-MiniLM-L6-v2")

api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")
client_llm = ChatOpenAI(
    api_key=api_key,
    base_url=api_base,
    model="openai/gpt-4.1-mini",
    temperature=0.3,
    max_tokens=500
)

def rag_pipeline(user_question):
    """Complete RAG pipeline: Retrieve → Augment → Generate"""

    print(f"\n📝 Question: '{user_question}'")
    print("-" * 50)

    # Step 1: RETRIEVE
    print("1️⃣ RETRIEVE: Converting to embedding...")
    query_embedding = model.encode(user_question).tolist()

    # Perform semantic search to find relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_chunks = results['documents'][0]
    metadatas = results['metadatas'][0]

    print(f"   ✅ Retrieved {len(retrieved_chunks)} relevant chunks")
    for i, meta in enumerate(metadatas):
        print(f"      - {meta['source']} ({meta['section']})")

    # Step 2: AUGMENT
    print("\n2️⃣ AUGMENT: Building context...")

    # Define system prompt for context-aware answers
    system_prompt = """You are TechCorp's helpful AI assistant.
Answer ONLY based on the provided context.
If the answer is not in the context, say: 'I don't have that information in the provided documents.'"""

    context_text = "Context from TechCorp documents:\n\n"
    for i, chunk in enumerate(retrieved_chunks, 1):
        context_text += f"[Document {i}]\n{chunk}\n\n"

    # Complete the user prompt with question
    user_prompt = f"{context_text}\nQuestion: {user_question}\n\nAnswer:"

    print("   ✅ Context prepared with retrieved documents")

    # Step 3: GENERATE
    print("\n3️⃣ GENERATE: Creating answer...")

    # Create messages for LLM with system and user prompts
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client_llm.invoke(messages)
    answer = response.content

    # Format response with source citations
    sources = [meta['source'] for meta in metadatas]
    unique_sources = list(set(sources))

    final_response = f"{answer}\n\n📎 Sources: {', '.join(unique_sources)}"

    return final_response

# Test the complete pipeline
def test_rag_pipeline():
    """Test with sample questions"""

    test_questions = [
        "Can I bring my dog to the office?",
        "How many vacation days do I get?",
        "What is the remote work policy?"
    ]

    for question in test_questions:
        answer = rag_pipeline(question)
        print("\n" + "=" * 50)
        print("💬 ANSWER:")
        print(answer)
        print("=" * 50)

# Run the test
try:
    # First ensure we have documents in the database
    if collection.count() == 0:
        print("\n⚠️ No documents in database. Please run Task 2 first!")
    else:
        print(f"\n📚 Database has {collection.count()} chunks ready")
        test_rag_pipeline()

        print("\n" + "=" * 50)
        print("🎉 RAG Pipeline Complete!")
        print("   - Retrieval: Semantic search working")
        print("   - Augmentation: Context injection ready")
        print("   - Generation: LLM producing answers")
        print("   - Citations: Sources included")
        print("=" * 50)

except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n🎯 You've built a complete RAG system - from search to answers!")
