from __future__ import annotations

import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {background: linear-gradient(180deg, #0a0f1f 0%, #10182d 100%); color: #f5f7fb;}
        .block-container {padding-top: 1rem; padding-bottom: 7rem; max-width: 900px;}
        h1, h2, h3 {color: #f8fafc;}
        .app-hero {padding: 1.1rem 1.2rem; border-radius: 22px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-bottom: 1rem; box-shadow: 0 10px 30px rgba(0,0,0,.18);}
        .hero-title {font-size: 1.55rem; font-weight: 800; margin-bottom: 0.25rem;}
        .hero-sub {opacity: 0.85;}
        .metric-card {display:flex; flex-direction:column; gap: .35rem; padding:1rem; border-radius:20px; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.10); min-height: 120px; justify-content:center;}
        .metric-label {font-size: .9rem; opacity: .8;}
        .metric-value {font-size: 1.45rem; font-weight: 800;}
        .list-card {padding: .9rem 1rem; border-radius: 16px; background: rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,.08); margin-bottom: .6rem;}
        .muted {opacity: .75; font-size: .9rem;}
        .nav-wrap {position: fixed; left: 0; right: 0; bottom: 0; z-index: 9999; padding: .75rem .9rem; background: rgba(10,15,31,.97); border-top:1px solid rgba(255,255,255,.08); backdrop-filter: blur(10px);}
        .nav-grid {display:grid; grid-template-columns: repeat(4, 1fr); gap:.55rem; max-width: 900px; margin:0 auto;}
        .stButton > button, .stFormSubmitButton > button {border-radius: 16px; min-height: 48px; font-weight: 700; width:100%;}
        div[data-testid="stSidebar"] {display:none;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def app_header(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class='app-hero'>
            <div class='hero-title'>{title}</div>
            <div class='hero-sub'>{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def success_toast(message: str) -> None:
    st.success(message)


def render_bottom_nav(current_view: str) -> None:
    st.markdown("<div class='nav-wrap'><div class='nav-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    items = [
        ("🏠 Início", "home"),
        ("📅 Agenda", "agenda"),
        ("💸 Financeiro", "financeiro"),
        ("📊 Resumo", "resumo"),
    ]
    for col, (label, target) in zip(cols, items):
        with col:
            kind = "primary" if current_view == target else "secondary"
            if st.button(label, key=f"nav_{target}", use_container_width=True, type=kind):
                st.session_state.current_view = target
                st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)
