"""
Task 2: Smart Document Processing
Implement paragraph-based chunking for better RAG context
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

print("Setting up Vector Store for RAG")
print("=" * 50)

# Initialize ChromaDB client for persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection named "techcorp_rag"
collection = client.get_or_create_collection(name="techcorp_rag")

# Initialize embedding model for 384-dimension vectors
model = SentenceTransformer("all-MiniLM-L6-v2")

def smart_chunk_document(text, overlap_ratio=0.2):
    """
    Smart paragraph-based chunking with overlap
    """
    # Split document into paragraphs
    # Hint: Use text.split("\n\n") to split by double newlines
    paragraphs = text.split("\n\n")

    chunks = []
    for i in range(len(paragraphs)):
        chunk_parts = []

        # Add current paragraph
        chunk_parts.append(paragraphs[i])

        # Add next paragraph if exists
        if i + 1 < len(paragraphs):
            chunk_parts.append(paragraphs[i + 1])

        # Calculate overlap characters (20% of previous paragraph)
        # Use int(len(paragraphs[i-1]) * overlap_ratio)
        if i > 0 and overlap_ratio > 0:
            overlap_chars = int(len(paragraphs[i-1]) * overlap_ratio)
            if overlap_chars > 0:
                chunk_parts.insert(0, paragraphs[i-1][-overlap_chars:])

        chunk = " ".join(chunk_parts)
        chunks.append(chunk)

    return chunks

# Process documents
doc_dir = Path("/root/techcorp-docs")
total_chunks = 0
docs_processed = 0

for category_dir in doc_dir.iterdir():
    if category_dir.is_dir():
        print(f"\n📂 Processing {category_dir.name}:")

        for doc_file in category_dir.glob("*.md"):
            # Create metadata for document tracking
            # Hint: Use doc_file.name for source, category_dir.name for section
            metadata = {
                "source": doc_file.name,
                "section": category_dir.name
            }

            # Read and process document
            with open(doc_file, "r") as f:
                content = f.read()

            # Chunk the document
            chunks = smart_chunk_document(content)

            # Store chunks in vector database
            for i, chunk in enumerate(chunks):
                chunk_id = f"{category_dir.name}_{doc_file.stem}_chunk_{i}"
                embedding = model.encode(chunk).tolist()

                collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[metadata]
                )
                total_chunks += 1

            docs_processed += 1
            print(f"   ✅ {doc_file.name}: {len(chunks)} chunks")

print("🎉 Document Processing Complete!")
print(f"   - Documents processed: {docs_processed}")
print(f"   - Total chunks created: {total_chunks}")
print(f"   - Collection size: {collection.count()}")