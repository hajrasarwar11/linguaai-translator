import streamlit as st


def render_hero():
    st.markdown("""
    <div class="hero-wrapper animate-in">
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            AI-Powered · Real-Time Translation
        </div>

        <h1 class="hero-title">
            Translate with the<br>
            <span class="hero-title-accent">Intelligence of AI</span>
        </h1>

        <p class="hero-subtitle">
            LinguaAI brings enterprise-grade English to Spanish translation
            to your fingertips — powered by advanced language models,
            ready for your custom AI integration.
        </p>

        <div class="hero-divider">
            <div class="hero-divider-line"></div>
            <span class="hero-divider-icon">◆</span>
            <div class="hero-divider-line right"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    stats = [
        ("10K+", "Words in Database"),
        ("99%", "Accuracy Rate"),
        ("< 1s", "Response Time"),
        ("24/7", "Availability"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4], stats):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding: 1.2rem; border: 1px solid rgba(255,255,255,0.06);
                        border-radius: 12px; background: rgba(201,160,80,0.04);">
                <div style="font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600;
                            color:#C9A050; line-height:1;">{val}</div>
                <div style="font-size:0.7rem; color:#6E6358; text-transform:uppercase;
                            letter-spacing:0.12em; margin-top:0.4rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature highlights
    st.markdown('<div class="section-label">Core Capabilities</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    highlights = [
        ("🔤", "Instant Translation",
         "Real-time English to Spanish translation with AI confidence scoring and phonetic guides."),
        ("📖", "Smart Dictionary",
         "Build, manage, and search your personal word database. Import/export ready for deployment."),
        ("📊", "Usage Analytics",
         "Track translation patterns, word frequency, session activity, and system performance metrics."),
    ]

    for col, (icon, title, desc) in zip(cols, highlights):
        with col:
            st.markdown(f"""
            <div class="lingua-card" style="text-align:center; padding: 2rem 1.5rem;">
                <div style="font-size:2.2rem; margin-bottom:1rem;">{icon}</div>
                <div style="font-size:0.95rem; font-weight:600; color:#F0E8DC;
                            margin-bottom:0.6rem; letter-spacing:0.02em;">{title}</div>
                <div style="font-size:0.8rem; color:#6E6358; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA row
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown("""
        <div style="text-align:center; padding: 2rem; border: 1px solid rgba(201,160,80,0.15);
                    border-radius: 16px; background: linear-gradient(145deg, rgba(35,28,14,0.4), rgba(14,14,21,0.6));
                    margin-top: 1rem;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:1.5rem; color:#E4C47A;
                        margin-bottom:0.6rem;">Ready to Start?</div>
            <div style="font-size:0.82rem; color:#6E6358; margin-bottom:1.2rem;">
                Navigate to <strong style="color:#B8AA98;">Translate</strong> in the sidebar
                to begin your first translation.
            </div>
            <div style="display:flex; align-items:center; justify-content:center; gap:0.5rem;
                        font-size:0.72rem; color:#4CAF7A;">
                <span style="width:8px;height:8px;border-radius:50%;background:#4CAF7A;
                              box-shadow:0 0 8px rgba(76,175,122,0.5);display:inline-block;
                              animation:pulse-status 2.5s infinite;"></span>
                System Online · All Services Operational
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer credits
    st.markdown("""
    <div style="text-align:center; margin-top:3rem; padding-top:1.5rem;
                border-top:1px solid rgba(255,255,255,0.05);">
        <span style="font-size:0.7rem; color:#3A342C; letter-spacing:0.1em;">
            LINGUAAI TRANSLATOR · v1.0.0-BETA · BUILT FOR AI INTEGRATION
        </span>
    </div>
    """, unsafe_allow_html=True)
