from __future__ import annotations

import streamlit as st
from utils.auth import init_session, require_login
from utils.db import init_db, get_dashboard_summary, list_schedules, list_financial_entries
from utils.ui import inject_global_css, app_header

st.set_page_config(page_title="Resumo do Dia | DS STUDIO GO", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()
init_db()
init_session()
require_login()

app_header("Resumo do dia", "Visão rápida da agenda e do financeiro")
summary = get_dashboard_summary()

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Agendamentos hoje", summary["today_schedule_count"])
with c2:
    st.metric("Recebido hoje", f"R$ {summary['received_today']:.2f}")
with c3:
    st.metric("Saldo do dia", f"R$ {summary['balance_today']:.2f}")

st.markdown("### Agenda")
for row in list_schedules(limit=10):
    st.write(f"{row['date']} {row['time']} • {row['client']} • {row['status']}")

st.markdown("### Financeiro")
for row in list_financial_entries(limit=10):
    st.write(f"{row['date']} • {row['type']} • {row['description']} • R$ {row['amount']:.2f}")
