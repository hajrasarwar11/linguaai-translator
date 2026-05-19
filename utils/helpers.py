import streamlit as st


def page_header(eyebrow: str, title: str, desc: str = ""):
    desc_html = f'<p class="page-desc">{desc}</p>' if desc else ""
    st.markdown(f"""
    <div class="page-header animate-in">
        <div class="page-eyebrow">{eyebrow}</div>
        <h1 class="page-title">{title}</h1>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


def section_label(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def gold_divider():
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
