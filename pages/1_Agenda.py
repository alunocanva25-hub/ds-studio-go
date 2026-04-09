from __future__ import annotations

import streamlit as st
from utils.auth import init_session, require_login
from utils.db import init_db, add_schedule, list_schedules, update_schedule_status
from utils.ui import inject_global_css, app_header, success_toast

st.set_page_config(page_title="Agenda | DS STUDIO GO", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()
init_db()
init_session()
require_login()

app_header("Agendamento rápido", "Crie e acompanhe agendamentos em poucos toques")

with st.form("novo_agendamento", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        client = st.text_input("Cliente*")
        service = st.text_input("Serviço*")
        date = st.date_input("Data*")
    with c2:
        professional = st.text_input("Profissional*")
        time = st.time_input("Horário*")
        notes = st.text_input("Observação")
    submitted = st.form_submit_button("Salvar agendamento", use_container_width=True)

if submitted:
    if not all([client, service, professional]):
        st.error("Preencha cliente, serviço e profissional.")
    else:
        add_schedule(client, service, professional, str(date), time.strftime("%H:%M"), notes)
        success_toast("Agendamento salvo com sucesso.")
        st.rerun()

st.markdown("### Lista de agendamentos")
schedules = list_schedules()
if not schedules:
    st.info("Nenhum agendamento cadastrado ainda.")
else:
    for row in schedules:
        with st.container(border=True):
            a, b = st.columns([4, 1])
            with a:
                st.markdown(f"**{row['date']} {row['time']}** — {row['client']}")
                st.caption(f"{row['service']} • {row['professional']} • {row['status']}")
                if row['notes']:
                    st.write(row['notes'])
            with b:
                new_status = st.selectbox(
                    "Status",
                    ["Agendado", "Confirmado", "Concluído", "Cancelado"],
                    index=["Agendado", "Confirmado", "Concluído", "Cancelado"].index(row['status']),
                    key=f"status_{row['id']}",
                    label_visibility="collapsed",
                )
                if new_status != row['status'] and st.button("Atualizar", key=f"btn_{row['id']}", use_container_width=True):
                    update_schedule_status(row['id'], new_status)
                    success_toast("Status atualizado.")
                    st.rerun()
