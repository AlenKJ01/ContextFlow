# backend/services/utils.py
from typing import List

def validate_messages_list(messages, expected_min=1):
    if not isinstance(messages, list):
        return False
    if len(messages) < expected_min:
        return False
    for m in messages:
        if not isinstance(m, str):
            return False
    return True

ALLOWED_TONES = ["Calm Mentor", "Witty Friend", "Therapist-Style"]

def validate_text_and_tone(text, tone):
    if not isinstance(text, str) or text.strip() == "":
        return False, "text must be a non-empty string"
    if tone not in ALLOWED_TONES:
        return False, f"tone must be one of {ALLOWED_TONES}"
    return True, ""
