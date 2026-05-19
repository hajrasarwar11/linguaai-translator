import streamlit as st
import time
from utils.helpers import page_header, section_label, gold_divider
from utils.session_state import add_to_history
from utils.helpers import mock_translate


def render_translation_panel():
    page_header("AI Translation Engine", "Translate", "English to Spanish — powered by your AI model.")

    # ── Main translation columns ──────────────────────────────────────────
    col_left, col_arrow, col_right = st.columns([5, 1, 5])

    with col_left:
        st.markdown('<span class="lang-badge">🇬🇧  English — Source</span>', unsafe_allow_html=True)
        english_input = st.text_area(
            label="english_input_hidden",
            label_visibility="collapsed",
            placeholder="Enter English text here…",
            height=180,
            key="english_input_area",
            value=st.session_state.english_input,
        )
        st.session_state.english_input = english_input

        # Character count
        char_count = len(english_input)
        word_count = len(english_input.split()) if english_input.strip() else 0
        st.markdown(
            f'<div style="font-size:0.7rem;color:#6E6358;text-align:right;margin-top:0.3rem;">'
            f'{word_count} words · {char_count} chars</div>',
            unsafe_allow_html=True
        )

    with col_arrow:
        st.markdown("""
        <div style="display:flex; align-items:center; justify-content:center;
                    height:100%; padding-top:2.5rem;">
            <div style="width:40px;height:40px;border-radius:50%;
                        background:rgba(201,160,80,0.08);border:1px solid rgba(201,160,80,0.25);
                        display:flex;align-items:center;justify-content:center;
                        font-size:1rem; color:#C9A050;">→</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown('<span class="lang-badge">🇪🇸  Español — Output</span>', unsafe_allow_html=True)

        output = st.session_state.spanish_output
        if output:
            st.markdown(
                f'<div class="translate-output-box">{output}</div>',
                unsafe_allow_html=True
            )
            # Confidence bar
            conf = st.session_state.confidence_score
            conf_color = "#4CAF7A" if conf >= 85 else "#E09040" if conf >= 60 else "#C04040"
            st.markdown(f"""
            <div class="confidence-bar">
                <span>Confidence</span>
                <div class="confidence-track">
                    <div class="confidence-fill" style="width:{conf}%;background:{conf_color};"></div>
                </div>
                <span style="color:{conf_color};font-weight:600;">{conf}%</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="translate-output-box">'
                '<span class="translate-placeholder">Translation will appear here…</span>'
                '</div>',
                unsafe_allow_html=True
            )

    gold_divider()

    # ── Action buttons ────────────────────────────────────────────────────
    btn_col1, btn_col2, btn_col3, btn_col4, spacer = st.columns([2, 2, 2, 2, 4])

    with btn_col1:
        translate_clicked = st.button("✦  Translate", use_container_width=True, key="translate_btn")

    with btn_col2:
        with st.container():
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            clear_clicked = st.button("✕  Clear", use_container_width=True, key="clear_btn")
            st.markdown('</div>', unsafe_allow_html=True)

    with btn_col3:
        with st.container():
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            copy_clicked = st.button("⧉  Copy", use_container_width=True, key="copy_btn")
            st.markdown('</div>', unsafe_allow_html=True)

    with btn_col4:
        with st.container():
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            save_clicked = st.button("♡  Favorite", use_container_width=True, key="fav_btn")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Handle actions ────────────────────────────────────────────────────
    if translate_clicked:
        if not st.session_state.english_input.strip():
            st.warning("Please enter some text to translate.")
        else:
            with st.spinner("Translating…"):
                time.sleep(0.6)  # Simulate network latency
                translation, confidence = mock_translate(
                    st.session_state.english_input,
                    st.session_state.dictionary
                )
            st.session_state.spanish_output = translation
            st.session_state.confidence_score = confidence
            add_to_history(
                st.session_state.english_input,
                translation,
                confidence
            )
            st.rerun()

    if clear_clicked:
        st.session_state.english_input = ""
        st.session_state.spanish_output = ""
        st.session_state.confidence_score = 0
        st.rerun()

    if copy_clicked and st.session_state.spanish_output:
        st.success(f"Copied: \"{st.session_state.spanish_output}\"")

    if save_clicked:
        word = st.session_state.english_input.strip().lower()
        if word and word not in st.session_state.favorites:
            st.session_state.favorites.append(word)
            st.success(f"Added \"{word}\" to favorites.")
        elif not word:
            st.warning("Enter a word first.")
        else:
            st.info("Already in favorites.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Voice input placeholder ───────────────────────────────────────────
    section_label("Voice Input")
    st.markdown("""
    <div class="lingua-card" style="text-align:center; padding: 1.8rem;">
        <div class="voice-btn-wrapper">
            <div class="voice-btn">🎙</div>
        </div>
        <div style="font-size:0.82rem; color:#6E6358; margin-top:0.6rem;">
            Voice input placeholder — connect your speech-to-text API here
        </div>
        <div style="margin-top:0.8rem;">
            <span class="feature-badge coming-soon">Coming Soon</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recent translations ───────────────────────────────────────────────
    if st.session_state.translation_history:
        section_label("Recent Translations")
        st.markdown('<div class="lingua-card">', unsafe_allow_html=True)

        for item in st.session_state.translation_history[:6]:
            conf = item["confidence"]
            conf_color = "#4CAF7A" if conf >= 85 else "#E09040" if conf >= 60 else "#C04040"
            st.markdown(f"""
            <div class="history-item">
                <div class="history-dot"></div>
                <div style="flex:1;">
                    <div class="history-text">
                        <strong style="color:#F0E8DC;">{item['english']}</strong>
                        <span style="color:#6E6358; margin:0 0.5rem;">→</span>
                        <span style="color:#E4C47A;">{item['spanish']}</span>
                    </div>
                    <div class="history-sub">{item['date']} · {item['timestamp']}
                        <span style="color:{conf_color}; margin-left:0.6rem;">{conf}% confidence</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
