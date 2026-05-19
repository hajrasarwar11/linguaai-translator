import os
import streamlit as st

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


SYSTEM_PROMPT = """You are LinguaAI, an English to Spanish translator.

Rules:
- Translate the given English word or phrase into Spanish.
- Respond with ONLY two lines, no extra text:
  TRANSLATION: <spanish text>
  NOTE: <one short usage tip, max 12 words>

- Be accurate and natural. If the input is a phrase, translate the whole phrase."""


def is_groq_configured() -> bool:
    return bool(os.environ.get("GROQ_API_KEY", "").strip())


def call_groq_translate(text: str, model: str = "llama-3.1-8b-instant") -> tuple[str, str, str]:
    """Returns (translation, note, error)."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return "", "", "GROQ_API_KEY not set."
    if not GROQ_AVAILABLE:
        return "", "", "Groq package not installed."

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate to Spanish: {text}"},
            ],
            temperature=0.2,
            max_tokens=80,
        )
        raw = response.choices[0].message.content.strip()
        translation = ""
        note = ""
        for line in raw.splitlines():
            if line.startswith("TRANSLATION:"):
                translation = line.replace("TRANSLATION:", "").strip()
            elif line.startswith("NOTE:"):
                note = line.replace("NOTE:", "").strip()
        if not translation:
            translation = raw
        st.session_state.total_api_calls += 1
        return translation, note, ""
    except Exception as e:
        msg = str(e)
        if "auth" in msg.lower():
            return "", "", "Invalid API key — check your GROQ_API_KEY."
        return "", "", f"API error: {msg[:80]}"
