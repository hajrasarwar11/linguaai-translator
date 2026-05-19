import streamlit as st
import os
from utils.helpers import page_header
from utils.groq_client import is_groq_configured


def render_settings():
    page_header("Configuration", "Settings", "Set up Groq AI and customize app behavior.")

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="settings-group">', unsafe_allow_html=True)
        st.markdown('<div class="settings-group-title">Groq API (AI Translation)</div>', unsafe_allow_html=True)

        configured = is_groq_configured()
        dot = "online" if configured else "offline"
        label = "Connected — AI translation active" if configured else "Not connected — using local dictionary only"
        color = "#4CAF7A" if configured else "#6E6358"

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.7rem;padding:0.75rem;
                    background:rgba(255,255,255,0.03);border-radius:8px;margin-bottom:1rem;">
            <span class="status-dot {dot}"></span>
            <div style="font-size:0.82rem;color:{color};">{label}</div>
        </div>
        """, unsafe_allow_html=True)

        if not configured:
            st.markdown("""
            <div style="font-size:0.8rem;color:#9B8E7E;line-height:1.7;margin-bottom:0.8rem;">
                Get a free API key at <strong style="color:#E4C47A;">console.groq.com</strong>
                and paste it below. Without it, only your local dictionary is used.
            </div>
            """, unsafe_allow_html=True)

        api_key_input = st.text_input(
            "Groq API Key",
            placeholder="gsk_…",
            type="password",
            key="settings_api_key"
        )
        if st.button("⚡  Apply API Key", key="apply_key_btn"):
            if api_key_input.strip():
                os.environ["GROQ_API_KEY"] = api_key_input.strip()
                st.success("✓ API key applied. AI translation is now active!")
                st.rerun()
            else:
                st.error("Please paste your Groq API key.")

        st.markdown("<br>", unsafe_allow_html=True)
        model_opts = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "gemma2-9b-it", "mixtral-8x7b-32768"]
        st.session_state.groq_model = st.selectbox(
            "AI Model", model_opts,
            index=model_opts.index(st.session_state.groq_model)
            if st.session_state.groq_model in model_opts else 0,
            key="settings_model"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="settings-group">', unsafe_allow_html=True)
        st.markdown('<div class="settings-group-title">Behavior</div>', unsafe_allow_html=True)
        st.session_state.save_new_words = st.toggle(
            "Auto-save AI translations to dictionary",
            value=st.session_state.save_new_words,
            help="Single words/short phrases from AI responses are saved automatically."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="settings-group">', unsafe_allow_html=True)
        st.markdown('<div class="settings-group-title">Reset</div>', unsafe_allow_html=True)
        col_rc, col_ra = st.columns(2)
        with col_rc:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("Clear Chat", use_container_width=True, key="rst_chat"):
                st.session_state.messages = []
                st.success("Chat cleared.")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_ra:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("Reset All", use_container_width=True, key="rst_all"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown(f"""
        <div class="settings-group">
            <div class="settings-group-title">App Info</div>
            <div style="font-size:0.81rem;color:#9B8E7E;line-height:2.2;">
                <div style="display:flex;justify-content:space-between;">
                    <span>Version</span><span style="color:#F0E8DC;">{st.session_state.app_version}</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span>Dictionary Words</span><span style="color:#C9A050;font-weight:600;">{len(st.session_state.dictionary)}</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span>Chat Messages</span><span style="color:#F0E8DC;">{len(st.session_state.messages)}</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span>Local Hits</span><span style="color:#F0E8DC;">{st.session_state.total_local_hits}</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span>AI Calls</span><span style="color:#F0E8DC;">{st.session_state.total_api_calls}</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span>Model</span><span style="color:#C9A050;font-size:0.74rem;">{st.session_state.groq_model}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="lingua-card lingua-card-purple" style="background:linear-gradient(145deg,rgba(28,14,42,0.9),rgba(14,8,22,0.95));
             border:1px solid rgba(123,63,160,0.3);padding:1.3rem;">
            <div style="font-size:0.7rem;color:#9B5BC0;text-transform:uppercase;letter-spacing:0.14em;
                        font-weight:600;margin-bottom:0.7rem;">Get Groq API Key (Free)</div>
            <div style="font-size:0.79rem;color:#9B8E7E;line-height:1.9;">
                1. Go to <strong style="color:#E4C47A;">console.groq.com</strong><br>
                2. Sign up (free)<br>
                3. API Keys → Create key<br>
                4. Copy & paste above<br>
                5. Click Apply
            </div>
        </div>
        """, unsafe_allow_html=True)
