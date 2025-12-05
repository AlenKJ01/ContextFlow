# backend/memory/extractor.py

import json
from services.gemini_client import generate_text

# NOTE: double braces {{ }} are required so .format() treats them as literal braces
MEMORY_EXTRACTION_PROMPT = """
You MUST output ONLY valid JSON. 
No explanations. No markdown. No code fences.

Return EXACTLY this structure:

{{
  "preferences": [...],
  "emotional_patterns": [...],
  "facts": [...]
}}

Rules:
- Keep each list short (each item <= 12 words).
- Only include items explicitly supported by the messages.
- No invented details, no commentary, no trailing commas.
- Respond with a single JSON object and nothing else.

Messages (JSON array, oldest-first):
{messages}
"""

def _safe_extract_json(text):
    text = (text or "").strip()

    # 1. Try direct JSON
    try:
        return json.loads(text)
    except:
        pass

    # 2. Find first {...} block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except:
            pass

    # 3. Handle JSON inside code fences
    if "```" in text:
        for part in text.split("```"):
            part = part.strip()
            if part.startswith("{") and part.endswith("}"):
                try:
                    return json.loads(part)
                except:
                    pass

    return None

def extract_memories(messages):
    """
    messages: list[str] (oldest-first). Returns dict with keys:
      preferences, emotional_patterns, facts, raw_extraction (optional), parsing_error (optional)
    """
    # sanitize messages -> keep at most 30, strip blanks
    safe_messages = [m.strip() for m in (messages or []) if isinstance(m, str) and m.strip()]
    safe_messages = safe_messages[:30]
    safe_messages_json = json.dumps(safe_messages, ensure_ascii=False)

    prompt = MEMORY_EXTRACTION_PROMPT.format(messages=safe_messages_json)

    try:
        raw = generate_text(prompt, max_output_tokens=800, temperature=0.0)
    except Exception as e:
        print("\nGEMINI ERROR:", e, "\n")
        return {
            "preferences": [],
            "emotional_patterns": [],
            "facts": [],
            "error": str(e)
        }

    # debug print (keeps terminal visibility)
    print("\n\n================ RAW GEMINI OUTPUT ================\n")
    print(raw)
    print("\n===================================================\n\n")

    parsed = _safe_extract_json(raw)

    if parsed is None:
        return {
            "preferences": [],
            "emotional_patterns": [],
            "facts": [],
            "raw_extraction": raw,
            "parsing_error": "Could not parse JSON from Gemini output"
        }

    # Normalize results to lists of strings
    prefs = parsed.get("preferences", []) or []
    patterns = parsed.get("emotional_patterns", []) or []
    facts = parsed.get("facts", []) or []

    # ensure they are lists of strings
    def to_str_list(x):
        if isinstance(x, list):
            return [str(i).strip() for i in x if str(i).strip()]
        return []

    return {
        "preferences": to_str_list(prefs),
        "emotional_patterns": to_str_list(patterns),
        "facts": to_str_list(facts),
        "raw_extraction": raw
    }
