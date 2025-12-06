# backend/memory/storage.py

import os
import sqlite3
import chromadb
from chromadb.config import Settings

# Make safe directories
os.makedirs("backend/chroma_store", exist_ok=True)
os.makedirs("backend/database", exist_ok=True)

# ------------------------------
# LIGHTWEIGHT, RENDER-SAFE CLIENT
# ------------------------------

# NO embedding model will be downloaded
client = chromadb.PersistentClient(
    path="backend/chroma_store",
    settings=Settings(allow_reset=True)
)

# Create collection WITHOUT embedding_function
collection = client.get_or_create_collection(
    name="memory_vectors",
    metadata={"hnsw:space": "cosine"},
    embedding_function=None
)

def store_preferences_patterns(preferences, patterns):
    """Store items with tiny dummy embeddings to avoid ONNX usage."""
    docs = preferences + patterns
    if not docs:
        return

    ids = [f"mem_{i}" for i in range(len(docs))]

    # 1-dimensional dummy embedding to avoid heavy model load
    embeddings = [[1.0] for _ in docs]

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings
    )

def retrieve_memories(query_text, k=5):
    """Return top memories using same tiny embeddings."""
    if not query_text.strip():
        return []

    # Dummy embedding for similarity
    query_emb = [[1.0]]

    try:
        result = collection.query(
            query_embeddings=query_emb,
            n_results=k
        )
        # Extract list properly
        return result.get("documents", [[]])[0]
    except Exception:
        return []

# ------------------------------
# SQLITE FACT STORAGE
# ------------------------------

DB_PATH = "backend/database/facts.db"

def store_facts(facts):
    if not facts:
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT
        )
    """)

    for f in facts:
        cur.execute("INSERT INTO facts (fact) VALUES (?)", (f,))

    conn.commit()
    conn.close()

def retrieve_facts(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute("SELECT fact FROM facts ORDER BY id DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [r[0] for r in rows]
    except:
        return []
    finally:
        conn.close()
