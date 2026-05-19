import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
from utils.helpers import page_header, section_label, gold_divider


PLOTLY_THEME = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#B8AA98",
    font_family="Inter",
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)"),
)

GOLD = "#C9A050"
PURPLE = "#7B3FA0"
MAROON = "#8B1A2A"
TEAL = "#2A7070"


def _line_chart_data():
    days = 14
    base = datetime.now() - timedelta(days=days)
    dates = [(base + timedelta(days=i)).strftime("%b %d") for i in range(days + 1)]
    translations = [random.randint(4, 20) for _ in range(days + 1)]
    searches = [random.randint(6, 30) for _ in range(days + 1)]
    return dates, translations, searches


def render_analytics_dashboard():
    page_header("Usage & Performance", "Dashboard", "Real-time insights into your translation activity.")

    # ── Top Metric Cards ──────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card gold">
            <span class="metric-icon">📖</span>
            <span class="metric-value">{len(st.session_state.dictionary)}</span>
            <span class="metric-label">Total Words</span>
            <span class="metric-change up">+{st.session_state.words_added_today} today</span>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card purple">
            <span class="metric-icon">🔍</span>
            <span class="metric-value">{st.session_state.total_searches}</span>
            <span class="metric-label">Total Searches</span>
            <span class="metric-change up">+12 this week</span>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card maroon">
            <span class="metric-icon">⚡</span>
            <span class="metric-value">{st.session_state.total_translations}</span>
            <span class="metric-label">Translations</span>
            <span class="metric-change up">+8 today</span>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        history_count = len(st.session_state.translation_history)
        st.markdown(f"""
        <div class="metric-card teal">
            <span class="metric-icon">📊</span>
            <span class="metric-value">{history_count}</span>
            <span class="metric-label">Session Activity</span>
            <span class="metric-change up">Active session</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    gold_divider()

    # ── Activity Chart ────────────────────────────────────────────────────
    section_label("14-Day Activity")

    dates, translations, searches = _line_chart_data()
    # Add session translations
    if st.session_state.translation_history:
        translations[-1] += len(st.session_state.translation_history)
        searches[-1] += st.session_state.total_searches % 10

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=translations, name="Translations",
        line=dict(color=GOLD, width=2.5),
        fill="tozeroy",
        fillcolor="rgba(201,160,80,0.07)",
        mode="lines+markers",
        marker=dict(color=GOLD, size=5),
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=searches, name="Searches",
        line=dict(color=PURPLE, width=2, dash="dot"),
        mode="lines+markers",
        marker=dict(color=PURPLE, size=4),
    ))
    fig.update_layout(
        **PLOTLY_THEME,
        height=260,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#B8AA98", size=11),
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Word Frequency + System Status row ────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        section_label("Top Translated Words")
        history = st.session_state.translation_history
        if history:
            words = [h["english"].split()[0].lower() for h in history[:12]]
            freq = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
            sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:8]

            df_bar = pd.DataFrame(sorted_words, columns=["Word", "Count"])
            fig_bar = px.bar(
                df_bar, x="Count", y="Word", orientation="h",
                color="Count",
                color_continuous_scale=[[0, "#5A3A10"], [0.5, "#9A7535"], [1, "#E4C47A"]],
            )
            fig_bar.update_layout(
                **PLOTLY_THEME,
                height=240,
                coloraxis_showscale=False,
                showlegend=False,
            )
            fig_bar.update_traces(marker_line_width=0)
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""
            <div class="lingua-card" style="text-align:center;padding:2rem;">
                <div style="color:#6E6358;font-size:0.85rem;">
                    Translate some words to see frequency data.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        section_label("System Status")
        statuses = [
            ("API Server", "online", "Operational"),
            ("AI Model", "idle" if not st.session_state.ai_model_connected else "online",
             "Awaiting connection" if not st.session_state.ai_model_connected else "Connected"),
            ("Dictionary DB", "online", "Operational"),
            ("Voice Engine", "offline", "Not configured"),
            ("Export Service", "online", "Operational"),
        ]

        html_items = ""
        for name, status, desc in statuses:
            color_map = {"online": "#4CAF7A", "idle": "#E09040", "offline": "#6E6358"}
            c = color_map[status]
            html_items += f"""
            <div style="display:flex;align-items:center;gap:0.8rem;padding:0.65rem 0;
                        border-bottom:1px solid rgba(255,255,255,0.05);">
                <span class="status-dot {status}"></span>
                <div style="flex:1;">
                    <div style="font-size:0.82rem;color:#F0E8DC;">{name}</div>
                    <div style="font-size:0.7rem;color:#6E6358;">{desc}</div>
                </div>
                <span style="font-size:0.68rem;color:{c};letter-spacing:0.1em;
                             text-transform:uppercase;font-weight:500;">{status}</span>
            </div>
            """
        st.markdown(f'<div class="lingua-card">{html_items}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Recent translations table ─────────────────────────────────────────
    section_label("Recent Translation Log")
    if st.session_state.translation_history:
        recent = st.session_state.translation_history[:10]
        df_hist = pd.DataFrame([{
            "Time": h["timestamp"],
            "English": h["english"],
            "Español": h["spanish"],
            "Confidence": f"{h['confidence']}%",
        } for h in recent])
        st.dataframe(df_hist, use_container_width=True, height=280, hide_index=True)
    else:
        st.markdown("""
        <div class="lingua-card" style="text-align:center;padding:2rem;">
            <div style="font-size:1.5rem;margin-bottom:0.6rem;">📭</div>
            <div style="color:#6E6358;font-size:0.85rem;">
                No translations yet. Use the Translate panel to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Confidence Gauge ─────────────────────────────────────────────────
    if st.session_state.translation_history:
        st.markdown("<br>", unsafe_allow_html=True)
        section_label("Average Confidence Score")
        avg_conf = sum(h["confidence"] for h in st.session_state.translation_history) / len(
            st.session_state.translation_history)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_conf,
            number={"suffix": "%", "font": {"color": GOLD, "size": 36, "family": "Cormorant Garamond"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#6E6358", "tickfont": {"color": "#6E6358"}},
                "bar": {"color": GOLD, "thickness": 0.3},
                "bgcolor": "rgba(255,255,255,0.04)",
                "bordercolor": "rgba(255,255,255,0.08)",
                "steps": [
                    {"range": [0, 60], "color": "rgba(139,26,42,0.12)"},
                    {"range": [60, 85], "color": "rgba(224,144,64,0.08)"},
                    {"range": [85, 100], "color": "rgba(76,175,122,0.08)"},
                ],
                "threshold": {
                    "line": {"color": "#E4C47A", "width": 2},
                    "thickness": 0.8,
                    "value": avg_conf,
                },
            },
        ))
        fig_gauge.update_layout(
            **PLOTLY_THEME,
            height=220,
        )
        col_g, _, _ = st.columns([1, 1, 1])
        with col_g:
            st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})
