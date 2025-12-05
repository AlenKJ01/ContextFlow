# backend/routes/memory_routes.py
from flask import Blueprint, request, jsonify
from memory.extractor import extract_memories
from memory.storage import store_preferences_patterns, store_facts
from services.utils import validate_messages_list

memory_bp = Blueprint("memory", __name__)

@memory_bp.route("/extract", methods=["POST"])
def extract():
    payload = request.get_json(force=True)
    messages = payload.get("messages")
    if not validate_messages_list(messages, expected_min=1):
        return jsonify({"error": "Invalid input. 'messages' must be a list of strings."}), 400

    # Ensure we only process up to 30 messages as per spec
    messages = messages[:30]

    # Extraction returns dictionaries/lists
    result = extract_memories(messages)

    # Store preferences + emotional patterns into ChromaDB (vector memory)
    try:
        store_preferences_patterns(result.get("preferences", []), result.get("emotional_patterns", []))
    except Exception as e:
        # do not fail the whole response; include a warning
        result["storage_warning"] = f"Failed storing to ChromaDB: {str(e)}"

    # Store facts into SQLite
    try:
        store_facts(result.get("facts", []))
    except Exception as e:
        result["storage_warning_facts"] = f"Failed storing facts to SQLite: {str(e)}"

    return jsonify(result)
