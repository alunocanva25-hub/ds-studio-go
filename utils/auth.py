from __future__ import annotations

import streamlit as st
from utils.db import validate_user


def init_session() -> None:
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("user", None)


def login_box() -> None:
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar", use_container_width=True)

    st.caption("Usuários de teste: admin / 123456 | operacional / 123456")

    if submitted:
        user = validate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.rerun()
        st.error("Usuário ou senha inválidos.")


def require_login() -> None:
    if not st.session_state.get("logged_in"):
        st.switch_page("app.py")


def current_user() -> dict:
    return st.session_state.get("user") or {}


def logout_button() -> None:
    if st.button("Sair", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
