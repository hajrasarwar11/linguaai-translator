import streamlit as st
from datetime import datetime
from utils.dictionary import process_input, add_word, delete_word, lookup_word
from utils.groq_client import is_groq_configured


HELP_TEXT = """**LinguaAI Commands:**

| What you type | What happens |
|---|---|
| `hello` | Translate the word "hello" |
| `good morning` | Translate a phrase |
| `add dog = perro` | Add a new word to the dictionary |
| `update dog = can` | Update an existing word |
| `delete dog` | Remove a word |
| `list` | Show all words in the dictionary |
| `search friend` | Search the dictionary |
| `help` | Show this guide |
| `clear` | Clear the chat |
"""


def _timestamp():
    return datetime.now().strftime("%H:%M")


def _parse_command(text: str) -> tuple[str, str]:
    """
    Returns (command_type, payload).
    command_type: "add" | "update" | "delete" | "list" | "search" | "help" | "clear" | "translate"
    """
    t = text.strip()
    tl = t.lower()

    if tl in ("help", "?", "/help"):
        return "help", ""
    if tl in ("list", "show all", "dictionary", "show dictionary"):
        return "list", ""
    if tl in ("clear", "/clear"):
        return "clear", ""

    if tl.startswith("add ") and "=" in t:
        payload = t[4:].strip()
        return "add", payload

    if tl.startswith("update ") and "=" in t:
        payload = t[7:].strip()
        return "update", payload

    if tl.startswith("delete ") or tl.startswith("remove "):
        word = t.split(" ", 1)[1].strip()
        return "delete", word

    if tl.startswith("search ") or tl.startswith("find "):
        query = t.split(" ", 1)[1].strip()
        return "search", query

    return "translate", t


def render_chat_ui():
    # ── Header ────────────────────────────────────────────────────────────
    col_title, col_clear = st.columns([5, 1])
    with col_title:
        st.markdown("""
        <div class="page-header animate-in">
            <div class="page-eyebrow">English → Spanish</div>
            <h1 class="page-title">Dictionary Chat</h1>
            <p class="page-desc">Type a word to translate · Use commands to manage your dictionary</p>
        </div>
        """, unsafe_allow_html=True)
    with col_clear:
        st.markdown("<div style='padding-top:2.2rem;'>", unsafe_allow_html=True)
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("Clear", use_container_width=True, key="clear_chat_btn"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ── Welcome message (shown once) ─────────────────────────────────────
    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🌐"):
            st.markdown(
                "**Welcome to LinguaAI!** 👋\n\n"
                "I'm your English → Spanish dictionary assistant.\n\n"
                "- Type any **English word or phrase** to get the Spanish translation\n"
                "- Type **`add word = traducción`** to add a new word\n"
                "- Type **`help`** to see all commands\n\n"
                f"I currently know **{len(st.session_state.dictionary)} words**. Let's begin!"
            )

    # ── Chat history ──────────────────────────────────────────────────────
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = "👤" if role == "user" else "🌐"
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

    # ── Chat input ────────────────────────────────────────────────────────
    user_input = st.chat_input(
        "Type a word to translate, or 'add word = translation' to add…",
        key="chat_input_box"
    )

    if user_input and user_input.strip():
        text = user_input.strip()
        cmd, payload = _parse_command(text)

        # Show user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(text)
        st.session_state.messages.append({
            "role": "user",
            "content": text,
        })

        # ── Process command ───────────────────────────────────────────────
        response = ""

        if cmd == "clear":
            st.session_state.messages = []
            st.rerun()

        elif cmd == "help":
            response = HELP_TEXT

        elif cmd == "list":
            d = st.session_state.dictionary
            if not d:
                response = "📭 Your dictionary is empty. Use `add word = translation` to add words."
            else:
                rows = "\n".join([
                    f"| {k.title()} | {v.title()} |"
                    for k, v in sorted(d.items())
                ])
                response = (
                    f"**📖 Dictionary — {len(d)} words:**\n\n"
                    "| English | Español |\n|---|---|\n"
                    + rows
                )

        elif cmd == "add":
            if "=" not in payload:
                response = "⚠️ Format: `add word = translation`\nExample: `add dog = perro`"
            else:
                parts = payload.split("=", 1)
                eng = parts[0].strip()
                esp = parts[1].strip()
                if not eng or not esp:
                    response = "⚠️ Both English and Spanish are required.\nExample: `add dog = perro`"
                elif add_word(eng, esp):
                    response = (
                        f"✅ **Added successfully!**\n\n"
                        f"**{eng.title()}** → **{esp.title()}**\n\n"
                        f"Dictionary now has **{len(st.session_state.dictionary)} words**."
                    )
                else:
                    existing = st.session_state.dictionary.get(eng.lower(), "")
                    response = (
                        f"⚠️ **\"{eng}\"** already exists → **{existing}**\n\n"
                        f"Use `update {eng} = new_translation` to change it."
                    )

        elif cmd == "update":
            if "=" not in payload:
                response = "⚠️ Format: `update word = new_translation`"
            else:
                parts = payload.split("=", 1)
                eng = parts[0].strip()
                esp = parts[1].strip()
                if eng.lower() in st.session_state.dictionary:
                    old = st.session_state.dictionary[eng.lower()]
                    st.session_state.dictionary[eng.lower()] = esp.lower()
                    response = (
                        f"✅ **Updated!**\n\n"
                        f"**{eng.title()}**: ~~{old}~~ → **{esp.title()}**"
                    )
                else:
                    response = (
                        f"⚠️ **\"{eng}\"** not found in dictionary.\n\n"
                        f"Use `add {eng} = {esp}` to add it instead."
                    )

        elif cmd == "delete":
            if delete_word(payload):
                response = (
                    f"🗑️ **\"{payload.title()}\"** has been removed from the dictionary.\n\n"
                    f"Dictionary now has **{len(st.session_state.dictionary)} words**."
                )
            else:
                response = f"⚠️ **\"{payload}\"** was not found in the dictionary."

        elif cmd == "search":
            query = payload.lower()
            results = {
                w: t for w, t in st.session_state.dictionary.items()
                if query in w or query in t
            }
            if results:
                rows = "\n".join([f"| {k.title()} | {v.title()} |" for k, v in results.items()])
                response = (
                    f"🔍 **Found {len(results)} result(s) for \"{payload}\":**\n\n"
                    "| English | Español |\n|---|---|\n" + rows
                )
            else:
                response = (
                    f"🔍 No results for **\"{payload}\"** in your dictionary.\n\n"
                    f"Tip: Use `add {payload} = translation` to add it."
                )

        elif cmd == "translate":
            with st.spinner("Translating…"):
                translation, source, error = process_input(text)

            if error == "no_api":
                # Local dict miss, no API
                response = (
                    f"🔍 **\"{text.title()}\"** is not in your local dictionary yet.\n\n"
                    "**To add it:**\n"
                    f"`add {text} = <spanish translation>`\n\n"
                    "Or connect your **Groq API key** in Settings for AI translation."
                )
            elif error:
                response = f"⚠️ Translation error: {error}"
            else:
                source_label = "📚 Local Dictionary" if source == "local" else "🤖 Groq AI"
                response = (
                    f"### {translation.title()}\n\n"
                    f"**{text.title()}** → **{translation.title()}**\n\n"
                    f"*Source: {source_label}*\n\n"
                    f"Use `add {text} = {translation}` to save this if it's not already stored."
                    if source == "ai" else
                    f"### {translation.title()}\n\n"
                    f"**{text.title()}** → **{translation.title()}**\n\n"
                    f"*Source: {source_label}*"
                )

        # ── Show AI response ──────────────────────────────────────────────
        if response:
            with st.chat_message("assistant", avatar="🌐"):
                st.markdown(response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
            })
