import streamlit as st


def lookup_word(text: str) -> str | None:
    """Case-insensitive local dictionary lookup."""
    key = text.strip().lower()
    d = st.session_state.dictionary
    if key in d:
        st.session_state.total_local_hits += 1
        return d[key]
    return None


def add_word(english: str, spanish: str) -> bool:
    key = english.strip().lower()
    if key in st.session_state.dictionary:
        return False
    st.session_state.dictionary[key] = spanish.strip().lower()
    return True


def update_word(english: str, new_spanish: str) -> bool:
    key = english.strip().lower()
    if key not in st.session_state.dictionary:
        return False
    st.session_state.dictionary[key] = new_spanish.strip().lower()
    return True


def delete_word(english: str) -> bool:
    key = english.strip().lower()
    if key in st.session_state.dictionary:
        del st.session_state.dictionary[key]
        return True
    return False


def process_input(text: str) -> tuple[str, str, str]:
    """
    Hybrid lookup: local dict first, then Groq API.
    Returns (translation, source, error_message).
    source = "local" | "ai"
    """
    local = lookup_word(text)
    if local:
        return local, "local", ""

    # Try Groq API
    from utils.groq_client import is_groq_configured, call_groq_translate
    if not is_groq_configured():
        return "", "ai", "no_api"

    model = st.session_state.groq_model
    translation, note, error = call_groq_translate(text, model)
    if error:
        return "", "ai", error

    # Auto-save single words to dictionary
    if translation and st.session_state.save_new_words:
        key = text.strip().lower()
        if len(key.split()) <= 2 and key not in st.session_state.dictionary:
            st.session_state.dictionary[key] = translation.lower().strip(".")

    return translation, "ai", ""
