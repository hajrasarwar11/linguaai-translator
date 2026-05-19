import streamlit as st
import pandas as pd
import json
from utils.helpers import page_header, section_label, gold_divider


def render_features_panel():
    page_header("Features Panel", "Features", "Favorites, history, exports, and system controls.")

    tabs = st.tabs(["♡  Favorites", "🕐  History", "⬇  Export", "↺  Reset"])

    # ── FAVORITES ─────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        favs = st.session_state.favorites

        if not favs:
            st.markdown("""
            <div class="lingua-card" style="text-align:center;padding:3rem 2rem;">
                <div style="font-size:2.5rem;margin-bottom:0.8rem;opacity:0.35;">♡</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;
                            color:#B8AA98;margin-bottom:0.5rem;">No favorites yet</div>
                <div style="font-size:0.8rem;color:#6E6358;">
                    Use the ♡ Save Favorite button in the chat to save translations.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-size:0.76rem;color:#6E6358;margin-bottom:1rem;">
                <strong style="color:#C9A050;">{len(favs)}</strong> saved favorite(s)
            </div>
            """, unsafe_allow_html=True)

            for i, fav in enumerate(favs):
                col_card, col_del = st.columns([6, 1])
                with col_card:
                    st.markdown(f"""
                    <div class="lingua-card" style="padding:1rem 1.3rem;margin-bottom:0.5rem;">
                        <div style="display:flex;align-items:center;gap:1.2rem;">
                            <div style="flex:1;">
                                <div style="font-size:0.95rem;color:#F0E8DC;font-weight:500;">{fav['english']}</div>
                                <div style="font-size:0.82rem;color:#6E6358;margin-top:0.1rem;">{fav['timestamp']}</div>
                            </div>
                            <div style="color:#C9A050;font-size:1rem;">→</div>
                            <div style="flex:1;">
                                <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;
                                            color:#E4C47A;">{fav['spanish']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_del:
                    st.markdown('<div class="btn-secondary" style="padding-top:0.3rem;">', unsafe_allow_html=True)
                    if st.button("✕", key=f"del_fav_{i}", use_container_width=True):
                        st.session_state.favorites.pop(i)
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    # ── HISTORY ───────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        history = st.session_state.word_lookup_history

        if not history:
            st.markdown("""
            <div class="lingua-card" style="text-align:center;padding:3rem 2rem;">
                <div style="font-size:2.5rem;margin-bottom:0.8rem;opacity:0.35;">🕐</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.3rem;
                            color:#B8AA98;margin-bottom:0.5rem;">No history yet</div>
                <div style="font-size:0.8rem;color:#6E6358;">
                    Your lookup history will appear here as you translate words.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Filter controls
            col_filter, _ = st.columns([2, 4])
            with col_filter:
                source_filter = st.selectbox(
                    "Filter by source",
                    ["All", "Local Dictionary", "Groq AI"],
                    key="hist_filter"
                )

            filtered = history
            if source_filter == "Local Dictionary":
                filtered = [h for h in history if h["source"] == "local"]
            elif source_filter == "Groq AI":
                filtered = [h for h in history if h["source"] == "ai"]

            st.markdown(f'<div style="font-size:0.76rem;color:#6E6358;margin:0.5rem 0 1rem;">'
                        f'Showing <strong style="color:#C9A050;">{len(filtered)}</strong> entries</div>',
                        unsafe_allow_html=True)

            html_rows = ""
            for item in filtered[:20]:
                src_class = "source-local" if item["source"] == "local" else "source-ai"
                src_label = "Local" if item["source"] == "local" else "AI"
                html_rows += f"""
                <div class="history-item">
                    <div class="history-dot"></div>
                    <div style="flex:1;">
                        <div class="history-text">
                            <strong style="color:#F0E8DC;">{item['word']}</strong>
                            <span style="color:#6E6358;margin:0 0.4rem;">→</span>
                            <span style="color:#E4C47A;">{item['result']}</span>
                        </div>
                        <div class="history-sub">
                            {item['date']} · {item['timestamp']}
                            <span class="source-badge {src_class}" style="margin-left:0.5rem;">{src_label}</span>
                        </div>
                    </div>
                </div>
                """
            st.markdown(f'<div class="lingua-card">{html_rows}</div>', unsafe_allow_html=True)

            if len(filtered) > 20:
                st.markdown(f'<div style="font-size:0.72rem;color:#6E6358;text-align:center;margin-top:0.8rem;">'
                            f'Showing 20 of {len(filtered)} entries</div>', unsafe_allow_html=True)

    # ── EXPORT ────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown('<div class="lingua-card">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem;color:#C9A050;text-transform:uppercase;
                        letter-spacing:0.14em;margin-bottom:0.8rem;font-weight:600;">
                Dictionary Export
            </div>
            <div style="font-size:0.82rem;color:#9B8E7E;line-height:1.7;margin-bottom:1rem;">
                Export your full local dictionary as CSV or JSON for use in other apps.
            </div>
            """, unsafe_allow_html=True)
            df_dict = pd.DataFrame(
                [(k, v) for k, v in sorted(st.session_state.dictionary.items())],
                columns=["English", "Spanish"]
            )
            st.download_button(
                "⬇  Dictionary (CSV)", df_dict.to_csv(index=False).encode(),
                "lingua_dictionary.csv", "text/csv", use_container_width=True,
            )
            st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
            st.download_button(
                "⬇  Dictionary (JSON)",
                json.dumps(st.session_state.dictionary, indent=2, ensure_ascii=False).encode(),
                "lingua_dictionary.json", "application/json", use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="lingua-card">', unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:0.72rem;color:#C9A050;text-transform:uppercase;
                        letter-spacing:0.14em;margin-bottom:0.8rem;font-weight:600;">
                History Export
            </div>
            <div style="font-size:0.82rem;color:#9B8E7E;line-height:1.7;margin-bottom:1rem;">
                Export your full translation lookup history as CSV.
            </div>
            """, unsafe_allow_html=True)
            if st.session_state.word_lookup_history:
                df_hist = pd.DataFrame(st.session_state.word_lookup_history)
                st.download_button(
                    "⬇  History (CSV)", df_hist.to_csv(index=False).encode(),
                    "lingua_history.csv", "text/csv", use_container_width=True,
                )
            else:
                st.markdown('<div style="font-size:0.82rem;color:#6E6358;">No history to export yet.</div>',
                            unsafe_allow_html=True)

            if st.session_state.favorites:
                st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
                df_favs = pd.DataFrame(st.session_state.favorites)
                st.download_button(
                    "⬇  Favorites (CSV)", df_favs.to_csv(index=False).encode(),
                    "lingua_favorites.csv", "text/csv", use_container_width=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

    # ── RESET ─────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        col_l2, _ = st.columns([2, 2])
        with col_l2:
            st.markdown("""
            <div style="background:rgba(139,26,42,0.08);border:1px solid rgba(139,26,42,0.25);
                        border-radius:12px;padding:1.4rem;margin-bottom:1.2rem;">
                <div style="font-size:0.8rem;color:#E07070;font-weight:600;margin-bottom:0.4rem;">
                    ⚠ Reset Options
                </div>
                <div style="font-size:0.8rem;color:#9B8E7E;line-height:1.7;">
                    Choose what to reset. Dictionary words will be restored to defaults.
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("Clear Chat History", use_container_width=True, key="reset_chat"):
                st.session_state.messages = []
                st.success("Chat cleared.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("Clear Favorites", use_container_width=True, key="reset_favs"):
                st.session_state.favorites = []
                st.success("Favorites cleared.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("Clear Lookup History", use_container_width=True, key="reset_hist"):
                st.session_state.word_lookup_history = []
                st.success("History cleared.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("↺  Reset Everything", use_container_width=True, key="reset_all"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
