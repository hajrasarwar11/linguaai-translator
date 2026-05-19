import streamlit as st
from utils.helpers import page_header, section_label, gold_divider, feature_tile


def render_smart_features():
    page_header("AI Capabilities", "Smart Features", "Advanced features powered by your AI model integration.")

    # ── AI Suggestions ────────────────────────────────────────────────────
    section_label("AI-Powered Suggestions")

    recs = st.session_state.recommendation_pool
    cols = st.columns(len(recs))
    for col, (eng, esp) in zip(cols, recs):
        with col:
            st.markdown(f"""
            <div class="lingua-card" style="text-align:center;padding:1.2rem 0.8rem;cursor:pointer;">
                <div style="font-size:0.95rem;font-weight:600;color:#F0E8DC;margin-bottom:0.3rem;">
                    {eng}
                </div>
                <div style="font-size:0.82rem;color:#C9A050;font-style:italic;
                            font-family:'Cormorant Garamond',serif;">{esp}</div>
                <div style="margin-top:0.8rem;">
                    <span class="feature-badge">Suggested</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    gold_divider()

    # ── Favorites ─────────────────────────────────────────────────────────
    section_label("Saved Favorites")
    favs = st.session_state.favorites

    if favs:
        fav_cols = st.columns(min(len(favs), 4))
        for i, word in enumerate(favs[:8]):
            with fav_cols[i % 4]:
                translation = st.session_state.dictionary.get(word, "—")
                st.markdown(f"""
                <div class="lingua-card" style="padding:0.9rem;margin-bottom:0.6rem;">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:0.85rem;color:#F0E8DC;font-weight:500;">{word}</div>
                            <div style="font-size:0.78rem;color:#C9A050;margin-top:0.2rem;
                                        font-style:italic;">{translation}</div>
                        </div>
                        <span style="color:#6E6358;font-size:1rem;">♡</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="lingua-card" style="text-align:center;padding:2rem;">
            <div style="font-size:1.5rem;margin-bottom:0.6rem;">♡</div>
            <div style="color:#6E6358;font-size:0.85rem;">
                No favorites yet. Use the ♡ Favorite button in the Translate panel.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    gold_divider()

    # ── Feature grid ──────────────────────────────────────────────────────
    section_label("Feature Modules")

    row1 = st.columns(3)
    row2 = st.columns(3)

    features = [
        ("🤖", "AI Suggestions", "Context-aware word recommendations powered by your language model.",
         "Active", "active"),
        ("📈", "Confidence Scoring", "Probability scores for each translation with source confidence breakdown.",
         "Active", "active"),
        ("🗣", "Voice Translation", "Speak English, get spoken Spanish — browser speech API integration.",
         "Coming Soon", "coming-soon"),
        ("🕐", "Translation History", "Persistent log of all translations with timestamps and search.",
         "Active", "active"),
        ("🔊", "Audio Pronunciation", "Native speaker pronunciation audio for every translated word.",
         "Coming Soon", "coming-soon"),
        ("🌐", "Multi-Language", "Expand beyond Spanish — connect additional language models easily.",
         "Planned", "coming-soon"),
    ]

    all_rows = [row1, row2]
    for row_idx, row in enumerate(all_rows):
        for col_idx, col in enumerate(row):
            feat_idx = row_idx * 3 + col_idx
            if feat_idx < len(features):
                icon, title, desc, badge, badge_type = features[feat_idx]
                with col:
                    st.markdown(feature_tile(icon, title, desc, badge, badge_type), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── AI Model Integration placeholder ─────────────────────────────────
    gold_divider()
    section_label("AI Model Integration")

    st.markdown("""
    <div class="lingua-card lingua-card-purple" style="padding:2rem;">
        <div style="display:flex;gap:2rem;align-items:flex-start;">
            <div style="font-size:2.5rem;opacity:0.8;">🧠</div>
            <div style="flex:1;">
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;
                            color:#F0E8DC;margin-bottom:0.5rem;font-weight:400;">
                    Ready for Your AI Model
                </div>
                <div style="font-size:0.85rem;color:#9B8E7E;line-height:1.7;margin-bottom:1.2rem;">
                    The translation engine is fully modular — connect your model in <strong
                    style="color:#C9A050;">utils/helpers.py</strong> inside the
                    <code style="background:rgba(255,255,255,0.06);padding:0.1rem 0.4rem;
                    border-radius:4px;font-size:0.82rem;">mock_translate()</code> function.
                    The frontend, session state, history, analytics, and confidence display
                    will all work automatically once connected.
                </div>
                <div style="display:flex;flex-wrap:wrap;gap:0.5rem;">
    """, unsafe_allow_html=True)

    hooks = ["OpenAI GPT-4", "Google Gemini", "Anthropic Claude", "HuggingFace", "Custom Model API",
             "LangChain", "Ollama Local"]
    badges_html = "".join([
        f'<span class="about-tech-badge">{h}</span>' for h in hooks
    ])
    st.markdown(badges_html + "</div></div></div></div>", unsafe_allow_html=True)

    # ── Word Recommendation Engine ────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    section_label("Word Recommendation Engine")

    col_a, col_b = st.columns([2, 3])
    with col_a:
        reco_query = st.text_input(
            "Find related words",
            placeholder="Type a word…",
            key="reco_input"
        )
        if reco_query:
            matches = [
                w for w in st.session_state.dictionary
                if reco_query.lower() in w or w.startswith(reco_query.lower()[0])
            ][:6]
            if matches:
                st.markdown("""
                <div style="font-size:0.72rem;color:#6E6358;letter-spacing:0.1em;
                            text-transform:uppercase;margin:0.6rem 0 0.4rem;">Suggestions</div>
                """, unsafe_allow_html=True)
                for m in matches:
                    esp = st.session_state.dictionary[m]
                    st.markdown(f"""
                    <div class="history-item" style="padding:0.5rem 0;">
                        <div class="history-dot"></div>
                        <div>
                            <span style="color:#F0E8DC;font-size:0.85rem;">{m}</span>
                            <span style="color:#6E6358;"> → </span>
                            <span style="color:#C9A050;font-size:0.85rem;">{esp}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="lingua-card" style="padding:1.4rem;">
            <div style="font-size:0.78rem;color:#C9A050;text-transform:uppercase;
                        letter-spacing:0.14em;margin-bottom:0.8rem;font-weight:600;">
                Word of the Day
            </div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;
                        color:#F0E8DC;font-weight:400;">ephemeral</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;
                        color:#C9A050;font-style:italic;margin:0.2rem 0 0.8rem;">efímero</div>
            <div style="font-size:0.8rem;color:#6E6358;line-height:1.6;">
                <em>adjective</em> — Lasting for a very short time; transitory.<br>
                <span style="color:#9B8E7E;">"an ephemeral pleasure"</span>
            </div>
            <div style="margin-top:0.8rem;">
                <span class="feature-badge">AI Curated</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
