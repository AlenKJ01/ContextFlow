# backend/memory/storage.py

import chromadb
import sqlite3
import os

os.makedirs("backend/chroma_store", exist_ok=True)
os.makedirs("backend/database", exist_ok=True)

# ------------------------------
# NEW CHROMA CLIENT (2025 syntax)
# ------------------------------

# Creates a local persisted DB folder automatically
client = chromadb.PersistentClient(path="backend/chroma_store")

# Create or load the collection
collection = client.get_or_create_collection(
    name="memory_vectors",
    metadata={"hnsw:space": "cosine"}
)

def store_preferences_patterns(preferences, patterns):
    docs = preferences + patterns
    if not docs:
        return

    # simple ID scheme
    ids = [f"id_{i}" for i in range(len(docs))]

    collection.add(
        documents=docs,
        ids=ids
    )

def retrieve_memories(query_text, k=5):
    if not query_text.strip():
        return []

    result = collection.query(
        query_texts=[query_text],
        n_results=k
    )
    return result.get("documents", [[]])[0]


# --------------------------------
# SQLITE FACT STORAGE + RETRIEVAL
# --------------------------------
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
