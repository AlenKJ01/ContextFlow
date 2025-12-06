"""
Personality engine that rewrites raw LLM responses into a chosen tone.
Supports:
- Calm Mentor
- Witty Friend
- Therapist-Style
- Strict Analyst
- Professional Corporate Tone
"""

from backend.services.gemini_client import generate_text

TONE_INSTRUCTIONS = {
    "Calm Mentor": (
        "Rewrite the following reply in a calm, steady, and encouraging tone. "
        "Keep it concise, warm, and reassuring."
    ),

    "Witty Friend": (
        "Rewrite the reply in a playful, casually witty tone, like a friendly companion. "
        "Add one light, non-cringe joke if appropriate. Keep it friendly and modern."
    ),

    "Therapist-Style": (
        "Rewrite the reply in a gentle, reflective, therapist-like tone. "
        "Validate feelings, soften the language, avoid prescriptive advice."
    ),

    "Strict Analyst": (
        "Rewrite the reply in a highly structured, analytical, impartial tone. "
        "Prioritize logic, clarity, and concise breakdown. No emotional language. "
        "Sound like a senior data analyst reviewing evidence."
    ),

    "Professional Corporate Tone": (
        "Rewrite the reply in polished, formal corporate communication style. "
        "Use clear business language, maintain professionalism, avoid casual phrasing. "
        "Sound like a well-written internal memo or executive response."
    )
}


def transform_with_personality(text: str, tone: str):
    """Rewrite Gemini's raw answer using the selected tone template."""
    tone_key = tone if tone in TONE_INSTRUCTIONS else "Calm Mentor"
    instruction = TONE_INSTRUCTIONS[tone_key]

    prompt = f"""{instruction}

Rewrite the following reply. Limit the rewritten answer to **6 lines or fewer**.

Original:
\"\"\"{text}\"\"\" 

Rewritten:
"""

    try:
        rewritten = generate_text(prompt, max_output_tokens=400, temperature=0.35)
    except Exception as e:
        return {
            "before": text,
            "after": f"[transform failed: {str(e)}]"
        }

    return {"before": text, "after": rewritten}


def apply_tone(text: str, tone: str) -> str:
    """Return ONLY the rewritten output for the 'after' section."""
    result = transform_with_personality(text, tone)
    return result["after"]
