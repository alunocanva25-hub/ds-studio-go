from __future__ import annotations

import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {background: linear-gradient(180deg, #0a0f1f 0%, #10182d 100%); color: #f5f7fb;}
        .block-container {padding-top: 1.2rem; padding-bottom: 5rem; max-width: 900px;}
        h1, h2, h3 {color: #f8fafc;}
        .app-hero {padding: 1.1rem 1.2rem; border-radius: 22px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-bottom: 1rem;}
        .hero-title {font-size: 1.6rem; font-weight: 700; margin-bottom: 0.25rem;}
        .hero-sub {opacity: 0.8;}
        .metric-card {display:flex; flex-direction:column; gap: .35rem; padding:1rem; border-radius:20px; background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.10); min-height: 120px; justify-content:center;}
        .metric-label {font-size: .9rem; opacity: .8;}
        .metric-value {font-size: 1.5rem; font-weight: 700;}
        .list-card {padding: .9rem 1rem; border-radius: 16px; background: rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,.08); margin-bottom: .6rem;}
        .muted {opacity: .75; font-size: .9rem;}
        .bottom-hint {position: fixed; left: 0; right: 0; bottom: 0; padding: .8rem 1rem; text-align:center; background: rgba(10,15,31,.96); border-top:1px solid rgba(255,255,255,.08); font-size:.85rem;}
        .stButton > button, .stFormSubmitButton > button {border-radius: 16px; min-height: 48px; font-weight: 700;}
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


def bottom_hint(text: str) -> None:
    st.markdown(f"<div class='bottom-hint'>{text}</div>", unsafe_allow_html=True)
