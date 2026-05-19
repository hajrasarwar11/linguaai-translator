import streamlit as st
import pandas as pd
import json
from utils.helpers import page_header, section_label, gold_divider
from utils.dictionary import add_word, update_word, delete_word


def render_dictionary_panel():
    page_header("Word Database", "Dictionary", "View and manage all your English → Spanish word pairs.")

    # Stats
    total = len(st.session_state.dictionary)
    hits = st.session_state.total_local_hits
    api = st.session_state.total_api_calls

    c1, c2, c3 = st.columns(3)
    for col, icon, val, label, variant in [
        (c1, "📖", total, "Total Words", "gold"),
        (c2, "⚡", hits, "Local Hits", "purple"),
        (c3, "🤖", api, "AI Lookups", "maroon"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card {variant}" style="background:linear-gradient(145deg,rgba(28,24,38,0.9),rgba(14,14,21,0.95));
                border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.2rem 1.4rem;
                text-align:center;position:relative;overflow:hidden;">
                <div style="position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,{'#C9A050' if variant=='gold' else '#7B3FA0' if variant=='purple' else '#8B1A2A'},transparent);"></div>
                <div style="font-size:1.4rem;margin-bottom:0.3rem;">{icon}</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:600;color:#C9A050;line-height:1;">{val}</div>
                <div style="font-size:0.65rem;color:#6E6358;text-transform:uppercase;letter-spacing:0.14em;margin-top:0.2rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["📋  All Words", "➕  Add", "✏️  Update", "🗑  Delete"])

    # ── ALL WORDS ─────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        search_q = st.text_input("Filter", placeholder="Type to filter…", key="dict_view_filter",
                                 label_visibility="collapsed")

        d = st.session_state.dictionary
        items = sorted(d.items())
        if search_q:
            q = search_q.lower()
            items = [(k, v) for k, v in items if q in k or q in v]

        df = pd.DataFrame(
            [(k.title(), v.title()) for k, v in items],
            columns=["English", "Español"]
        )
        st.dataframe(df, use_container_width=True, height=380, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_csv, col_json, _ = st.columns([1, 1, 3])
        with col_csv:
            st.download_button("⬇ CSV", df.to_csv(index=False).encode(),
                               "dictionary.csv", "text/csv", use_container_width=True)
        with col_json:
            st.download_button("⬇ JSON",
                               json.dumps(st.session_state.dictionary, indent=2, ensure_ascii=False).encode(),
                               "dictionary.json", "application/json", use_container_width=True)

    # ── ADD ───────────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="lingua-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            new_eng = st.text_input("English Word / Phrase", placeholder="e.g. serenity", key="add_eng")
        with c2:
            new_esp = st.text_input("Spanish Translation", placeholder="e.g. serenidad", key="add_esp")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦  Add Word", key="add_btn"):
            if not new_eng.strip() or not new_esp.strip():
                st.error("Both fields are required.")
            elif add_word(new_eng, new_esp):
                st.success(f"✓ Added: **{new_eng.strip().title()}** → **{new_esp.strip().title()}**")
                st.rerun()
            else:
                st.warning(f'"{new_eng.strip()}" already exists. Use the Update tab to change it.')
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:0.76rem;color:#6E6358;margin-top:0.8rem;line-height:1.7;">
            💡 Tip: You can also add words directly from the chat by typing<br>
            <code style="color:#C9A050;background:rgba(201,160,80,0.08);padding:0.1rem 0.4rem;
            border-radius:4px;">add word = translation</code>
        </div>
        """, unsafe_allow_html=True)

    # ── UPDATE ────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="lingua-card">', unsafe_allow_html=True)
        words = sorted(st.session_state.dictionary.keys())
        sel = st.selectbox("Select word to update", words, key="upd_sel")
        if sel:
            cur = st.session_state.dictionary.get(sel, "")
            st.markdown(f'<div style="font-size:0.76rem;color:#6E6358;margin:0.5rem 0;">Current: '
                        f'<strong style="color:#C9A050;">{cur}</strong></div>', unsafe_allow_html=True)
            new_t = st.text_input("New Spanish translation", placeholder=cur, key="upd_trans")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✦  Update", key="upd_btn"):
            if not new_t.strip():
                st.error("Enter a new translation.")
            elif update_word(sel, new_t):
                st.success(f"✓ Updated: **{sel.title()}** → **{new_t.strip().title()}**")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── DELETE ────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="lingua-card">', unsafe_allow_html=True)
        words_d = sorted(st.session_state.dictionary.keys())
        sel_d = st.selectbox("Select word to delete", words_d, key="del_sel")
        if sel_d:
            esp_d = st.session_state.dictionary.get(sel_d, "")
            st.markdown(f"""
            <div style="background:rgba(139,26,42,0.08);border:1px solid rgba(139,26,42,0.2);
                        border-radius:8px;padding:0.75rem 1rem;margin:0.7rem 0;font-size:0.84rem;">
                <strong style="color:#E07070;">Remove:</strong>
                <span style="color:#B8AA98;"> "{sel_d}" → "{esp_d}"</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("🗑  Delete Word", key="del_btn"):
            if delete_word(sel_d):
                st.success(f"✓ Removed: **{sel_d}**")
                st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)
