#!/usr/bin/env python3
"""
🧠 Task 1: Embeddings - Teaching Computers to Understand Meaning
"""

import os
from sentence_transformers import SentenceTransformer, util

def main():
    # Initialize model that converts text → meaningful numbers
    model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)

    # Scenario: User searching documentation
    query = "forgot my password"

    docs = [
        "Password recovery: Use the 'Reset Password' link on login page",
        "Vacation policy: Request time off 2 weeks in advance",
        "Account security: Enable two-factor authentication",
        "Login help: Contact IT if you cannot access your account"
    ]

    # Convert query and docs to embeddings
    query_emb = model.encode(query)
    doc_embs = model.encode(docs)

    # Find semantic matches
    scores = util.cos_sim(query_emb, doc_embs)[0]

    print(f"Query: '{query}'\n")
    print("Results (score > 0.3 = relevant):")
    for doc, score in zip(docs, scores):
        marker = "✅" if score > 0.3 else "  "
        print(f"{marker} [{score:.2f}] {doc}")

    print("\n💡 Notice: Found 'Password recovery' and 'Login help'")
    print("   Even though query didn't contain those exact words!")

if __name__ == "__main__":
    main()