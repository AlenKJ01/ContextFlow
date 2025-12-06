# backend/routes/personality_routes.py

from flask import Blueprint, request, jsonify
from backend.services.gemini_client import generate_text
from backend.personality.engine import apply_tone
from backend.memory.storage import retrieve_memories, retrieve_facts

personality_bp = Blueprint("personality", __name__)

@personality_bp.route("/transform", methods=["POST"])
def transform():
    payload = request.get_json(force=True)
    text = payload.get("text", "").strip()
    tone = payload.get("tone", "").strip()

    if not text:
        return jsonify({"error": "Missing 'text'"}), 400

    # ---------------------------
    # MEMORY RETRIEVAL
    # ---------------------------
    memories = retrieve_memories(text, k=5)
    facts = retrieve_facts()

    # Build context block
    context_block = ""

    if memories:
        context_block += "Relevant Memories:\n"
        for m in memories:
            try:
                memories = retrieve_memories(text, 5)
            except Exception as e:
                memories = []
                print("MEMORY ERROR:", e)



    if facts:
        context_block += "\nKnown Facts:\n"
        for f in facts:
            context_block += f"- {f}\n"

    # ---------------------------
    # MAIN PROMPT
    # ---------------------------
    before_prompt = f"""
You are an assistant with access to user memory.

Answer the user's question in <= 6 lines.

USER QUESTION:
{text}

{context_block}

Respond naturally, and if memories are irrelevant, ignore them.
"""

    # Raw answer
    before = generate_text(before_prompt, max_output_tokens=180)

    # Personality rewrite
    after = apply_tone(before, tone)

    return jsonify({
        "before": before,
        "after": after
    }), 200
