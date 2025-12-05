# backend/services/gemini_client.py

import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# MUST include the full prefix
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "models/gemini-2.5-flash")

print("Using model:", GEMINI_MODEL)

# Correct 2025 endpoint
BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/{GEMINI_MODEL}:generateContent"


def generate_text(prompt: str, max_output_tokens: int = 1024, temperature: float = 0.2) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    url = f"{BASE_URL}?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": max_output_tokens,
            "temperature": temperature
        }
    }

    headers = {"Content-Type": "application/json"}

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")

    data = resp.json()

    # ---------- UNIVERSAL TEXT EXTRACTION ----------
    try:
        c = data.get("candidates", [])[0]
        content = c.get("content", {})

        # 1. Standard content.parts
        if isinstance(content, dict) and "parts" in content:
            parts = content.get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"]

        # 2. New Gemini 2.x outputText
        if "outputText" in content and "text" in content["outputText"]:
            return content["outputText"]["text"]

        # 3. prediction.text
        if "prediction" in content and "text" in content["prediction"]:
            return content["prediction"]["text"]

        # 4. direct text field
        if "text" in content:
            return content["text"]

        # fallback
        return json.dumps(data, indent=2)

    except Exception:
        return json.dumps(data, indent=2)
