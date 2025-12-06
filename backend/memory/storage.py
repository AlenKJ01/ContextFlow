# backend/memory/storage.py

import os
import sqlite3

os.makedirs("backend/database", exist_ok=True)

DB_PATH = "backend/database/facts.db"
MEMORY_DB = "backend/database/memory.db"

# -------------------------------------------
# SIMPLE SQLITE MEMORY STORE (RENDER-SAFE)
# -------------------------------------------

# Create memory DB
conn = sqlite3.connect(MEMORY_DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,        -- "preference", "pattern", "fact"
    content TEXT
)
""")

conn.commit()
conn.close()


# ----------------------------------------------------
# STORE FUNCTIONS
# ----------------------------------------------------
def store_preferences_patterns(preferences, patterns):
    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    for p in preferences:
        cur.execute("INSERT INTO memory (type, content) VALUES (?, ?)", ("preference", p))

    for ep in patterns:
        cur.execute("INSERT INTO memory (type, content) VALUES (?, ?)", ("pattern", ep))

    conn.commit()
    conn.close()


def store_facts(facts):
    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    for f in facts:
        cur.execute("INSERT INTO memory (type, content) VALUES (?, ?)", ("fact", f))

    conn.commit()
    conn.close()


# ----------------------------------------------------
# RETRIEVAL FUNCTIONS (simple LIKE search)
# ----------------------------------------------------
def retrieve_memories(query_text, limit=5):
    if not query_text.strip():
        return []

    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    # Very fast, zero ML, Render-safe
    cur.execute("""
        SELECT content
        FROM memory
        WHERE content LIKE ?
        ORDER BY id DESC
        LIMIT ?
    """, (f"%{query_text}%", limit))

    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]

def retrieve_facts(limit=10):
    conn = sqlite3.connect(MEMORY_DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT content
        FROM memory
        WHERE type = 'fact'
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]
