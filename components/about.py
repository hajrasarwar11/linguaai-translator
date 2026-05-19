import streamlit as st
from utils.helpers import page_header, gold_divider


def render_about():
    page_header("About", "LinguaAI", "An English to Spanish dictionary chatbot with AI integration.")

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown("""
        <div class="lingua-card" style="padding:1.8rem;">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.65rem;
                        color:#F0E8DC;font-weight:300;margin-bottom:0.9rem;">
                Your Personal EN→ES Dictionary
            </div>
            <div style="font-size:0.86rem;color:#9B8E7E;line-height:1.85;">
                LinguaAI is a conversational English to Spanish dictionary.
                You interact with it through a simple chat interface — type a word
                to translate it, or use commands to manage your personal word list.
            </div>
            <div style="margin-top:1rem;font-size:0.86rem;color:#9B8E7E;line-height:1.85;">
                The app uses a <strong style="color:#E4C47A;">hybrid lookup system</strong>:
                your local dictionary is checked first (instant response).
                If the word isn't there and you've connected a Groq API key,
                the AI translates it for you — and can optionally save it back
                to your dictionary automatically.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Commands</div>', unsafe_allow_html=True)
        commands = [
            ("word / phrase", "Translate English → Spanish"),
            ("add word = translation", "Add a new word to your dictionary"),
            ("update word = new", "Update an existing translation"),
            ("delete word", "Remove a word from the dictionary"),
            ("list", "Show all words in your dictionary"),
            ("search query", "Search the dictionary"),
            ("help", "Show the full command reference"),
            ("clear", "Clear the chat history"),
        ]
        rows = "\n".join([f"| `{c}` | {d} |" for c, d in commands])
        st.markdown("| Command | Action |\n|---|---|\n" + rows)

    with col_r:
        st.markdown("""
        <div class="lingua-card" style="border-color:rgba(201,160,80,0.3);
             background:linear-gradient(145deg,rgba(35,28,14,0.9),rgba(20,16,8,0.95));padding:1.4rem;
             margin-bottom:0.9rem;">
            <div style="font-size:0.68rem;color:#6E6358;text-transform:uppercase;
                        letter-spacing:0.14em;font-weight:600;margin-bottom:0.8rem;">Tech Stack</div>
        """, unsafe_allow_html=True)
        techs = ["Python 3.11", "Streamlit", "Groq API", "LLaMA 3.1", "Pandas", "Custom CSS"]
        badges = "".join([f'<span class="about-tech-badge">{t}</span>' for t in techs])
        st.markdown(badges + "</div>", unsafe_allow_html=True)

        features = [
            ("✓", "Chat-style interface", True),
            ("✓", "Local dictionary (CRUD)", True),
            ("✓", "Groq AI translation", True),
            ("✓", "Hybrid lookup engine", True),
            ("✓", "Auto-save AI results", True),
            ("✓", "Export CSV / JSON", True),
            ("✓", "Dark luxury theme", True),
            ("○", "Voice input", False),
        ]
        items = "".join([f"""
        <div style="display:flex;align-items:center;gap:0.6rem;padding:0.35rem 0;
                    border-bottom:1px solid rgba(255,255,255,0.04);">
            <span style="color:{'#4CAF7A' if ok else '#3A342C'};font-size:0.78rem;">{ic}</span>
            <span style="font-size:0.8rem;color:{'#B8AA98' if ok else '#6E6358'};">{label}</span>
        </div>
        """ for ic, label, ok in features])
        st.markdown(f"""
        <div class="lingua-card" style="padding:1.3rem;">
            <div style="font-size:0.68rem;color:#6E6358;text-transform:uppercase;
                        letter-spacing:0.14em;font-weight:600;margin-bottom:0.7rem;">Features</div>
            {items}
        </div>
        """, unsafe_allow_html=True)

    gold_divider()
    st.markdown("""
    <div style="text-align:center;padding:0.6rem 0;">
        <span style="font-size:0.66rem;color:#3A342C;letter-spacing:0.12em;">
            LINGUAAI · v2.0 · ENGLISH TO SPANISH DICTIONARY CHATBOT
        </span>
    </div>
    """, unsafe_allow_html=True)
