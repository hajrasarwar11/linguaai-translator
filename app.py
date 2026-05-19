import streamlit as st

st.set_page_config(
    page_title="LinguaAI Translator",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)

from utils.session_state import init_session_state
from utils.groq_client import is_groq_configured
from components.chat_ui import render_chat_ui
from components.dictionary_panel import render_dictionary_panel
from components.settings import render_settings
from components.about import render_about


def load_css():
    with open("styles/custom.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()
init_session_state()

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div class="sidebar-logo">🌐 LinguaAI</div>'
        '<div class="sidebar-subtitle">EN → ES Dictionary</div>'
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    nav_items = [
        ("💬", "Chat", "chat"),
        ("📖", "Dictionary", "dictionary"),
        ("⚙️", "Settings", "settings"),
        ("ℹ️", "About", "about"),
    ]

    for icon, label, page_key in nav_items:
        active = st.session_state.page == page_key
        if active:
            st.markdown('<div class="nav-active">', unsafe_allow_html=True)
        if st.button(f"{icon}  {label}", key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.rerun()
        if active:
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider" style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)

    # ── Live stats ────────────────────────────────────────────────────────
    groq_ok = is_groq_configured()
    st.markdown(f"""
    <div style="padding: 0 1.2rem;">
        <div style="font-size:0.68rem;color:#6E6358;margin-bottom:0.9rem;">
            <span class="status-dot {'online' if groq_ok else 'offline'}"></span>
            {'Groq AI Active' if groq_ok else 'Local Dictionary Only'}
        </div>
        <div style="display:flex;flex-direction:column;gap:0.4rem;margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;font-size:0.72rem;">
                <span style="color:#6E6358;">Words in dict</span>
                <span style="color:#C9A050;font-weight:600;">{len(st.session_state.dictionary)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.72rem;">
                <span style="color:#6E6358;">Local hits</span>
                <span style="color:#C9A050;font-weight:600;">{st.session_state.total_local_hits}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.72rem;">
                <span style="color:#6E6358;">AI lookups</span>
                <span style="color:#C9A050;font-weight:600;">{st.session_state.total_api_calls}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick Groq key input if not configured
    if not groq_ok:
        st.markdown("""
        <div style="padding:0 1.2rem;margin-bottom:0.5rem;">
            <div style="font-size:0.68rem;color:#E09040;margin-bottom:0.3rem;">
                ⚡ Add Groq key for AI translation
            </div>
        </div>
        """, unsafe_allow_html=True)
        api_sidebar = st.text_input(
            "groq_key_sidebar",
            placeholder="gsk_…",
            type="password",
            label_visibility="collapsed",
            key="sidebar_apikey"
        )
        if st.button("Apply", key="sidebar_apply", use_container_width=True):
            if api_sidebar.strip():
                import os
                os.environ["GROQ_API_KEY"] = api_sidebar.strip()
                st.rerun()

    st.markdown('<div class="sidebar-footer">LinguaAI · v2.0</div>', unsafe_allow_html=True)

# ── Page routing ──────────────────────────────────────────────────────────
page = st.session_state.page

if page == "chat":
    render_chat_ui()
elif page == "dictionary":
    render_dictionary_panel()
elif page == "settings":
    render_settings()
elif page == "about":
    render_about()
else:
    st.session_state.page = "chat"
    st.rerun()
