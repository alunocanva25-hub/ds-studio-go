from __future__ import annotations

import streamlit as st
from utils.auth import init_session, login_box, require_login, logout_button, current_user
from utils.db import init_db, get_dashboard_summary
from utils.ui import inject_global_css, app_header, bottom_hint

st.set_page_config(
    page_title="DS STUDIO GO",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()
init_db()
init_session()

if not st.session_state.get("logged_in"):
    app_header("DS STUDIO GO", "Operação rápida do DSYSTEM no celular")
    login_box()
    st.stop()

require_login()
user = current_user()
summary = get_dashboard_summary()

app_header("DS STUDIO GO", f"Bem-vindo, {user['display_name']}")
logout_button()

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Agenda de hoje</span><span class='metric-value'>{summary['today_schedule_count']}</span></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Recebido hoje</span><span class='metric-value'>R$ {summary['received_today']:.2f}</span></div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Saídas hoje</span><span class='metric-value'>R$ {summary['expense_today']:.2f}</span></div>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<div class='metric-card'><span class='metric-label'>Saldo do dia</span><span class='metric-value'>R$ {summary['balance_today']:.2f}</span></div>", unsafe_allow_html=True)

st.markdown("### Atalhos")
shortcut1, shortcut2, shortcut3 = st.columns(3)
with shortcut1:
    st.page_link("pages/1_Agenda.py", label="Novo agendamento", icon="📅")
with shortcut2:
    st.page_link("pages/2_Financeiro.py", label="Novo lançamento", icon="💸")
with shortcut3:
    st.page_link("pages/3_Resumo_do_Dia.py", label="Resumo do dia", icon="📊")

st.markdown("### Próximos agendamentos")
if summary["next_schedules"]:
    for item in summary["next_schedules"]:
        st.markdown(
            f"""
            <div class='list-card'>
                <div><strong>{item['date']} {item['time']}</strong> • {item['client']}</div>
                <div>{item['service']} • {item['professional']}</div>
                <div class='muted'>{item['status']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("Nenhum agendamento futuro cadastrado.")

bottom_hint("V2 com base local SQLite para demonstração. Pronta para futura sincronização com API/DB do DSYSTEM.")
