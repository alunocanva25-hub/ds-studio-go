from __future__ import annotations

import streamlit as st

from utils.auth import init_session, login_box, require_login, logout_button, current_user
from utils.db import (
    init_db,
    get_dashboard_summary,
    add_schedule,
    list_schedules,
    update_schedule_status,
    add_financial_entry,
    list_financial_entries,
)
from utils.ui import inject_global_css, app_header, render_bottom_nav, success_toast

st.set_page_config(
    page_title="DS STUDIO GO",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_global_css()
init_db()
init_session()


def go(view: str) -> None:
    st.session_state.current_view = view
    st.rerun()


def render_home() -> None:
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

    st.markdown("### Atalhos rápidos")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📅 Novo agendamento", use_container_width=True, key="home_agenda"):
            go("agenda")
    with c2:
        if st.button("💸 Novo lançamento", use_container_width=True, key="home_financeiro"):
            go("financeiro")
    with c3:
        if st.button("📊 Ver resumo", use_container_width=True, key="home_resumo"):
            go("resumo")

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



def render_agenda() -> None:
    app_header("Agendamento rápido", "Crie e acompanhe agendamentos em poucos toques")

    if st.button("← Voltar ao início", use_container_width=True, key="voltar_inicio_agenda"):
        go("home")

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
        if not all([client.strip(), service.strip(), professional.strip()]):
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
                    statuses = ["Agendado", "Confirmado", "Concluído", "Cancelado"]
                    current_idx = statuses.index(row['status']) if row['status'] in statuses else 0
                    new_status = st.selectbox(
                        "Status",
                        statuses,
                        index=current_idx,
                        key=f"status_{row['id']}",
                        label_visibility="collapsed",
                    )
                    if new_status != row['status'] and st.button("Atualizar", key=f"btn_{row['id']}", use_container_width=True):
                        update_schedule_status(row['id'], new_status)
                        success_toast("Status atualizado.")
                        st.rerun()



def render_financeiro() -> None:
    app_header("Lançamento rápido", "Registre entrada ou saída com poucos campos")

    if st.button("← Voltar ao início", use_container_width=True, key="voltar_inicio_fin"):
        go("home")

    with st.form("novo_lancamento", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            entry_type = st.selectbox("Tipo*", ["Entrada", "Saída"])
            description = st.text_input("Descrição*")
            payment_method = st.selectbox("Forma de pagamento*", ["Dinheiro", "Pix", "Cartão", "Transferência"])
        with c2:
            amount = st.number_input("Valor*", min_value=0.0, format="%.2f")
            date = st.date_input("Data*")
            notes = st.text_input("Observação")
        submitted = st.form_submit_button("Salvar lançamento", use_container_width=True)

    if submitted:
        if not description.strip() or amount <= 0:
            st.error("Informe descrição e valor válido.")
        else:
            add_financial_entry(entry_type, description, amount, payment_method, str(date), notes)
            success_toast("Lançamento salvo com sucesso.")
            st.rerun()

    st.markdown("### Últimos lançamentos")
    entries = list_financial_entries(limit=20)
    if not entries:
        st.info("Nenhum lançamento cadastrado ainda.")
    else:
        for row in entries:
            badge = "🟢" if row["type"] == "Entrada" else "🔴"
            with st.container(border=True):
                st.markdown(f"**{badge} {row['type']}** — {row['description']}")
                st.caption(f"{row['date']} • {row['payment_method']} • R$ {row['amount']:.2f}")
                if row['notes']:
                    st.write(row['notes'])



def render_resumo() -> None:
    app_header("Resumo do dia", "Visão rápida da agenda e do financeiro")
    if st.button("← Voltar ao início", use_container_width=True, key="voltar_inicio_resumo"):
        go("home")

    summary = get_dashboard_summary()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Agendamentos hoje", summary["today_schedule_count"])
    with c2:
        st.metric("Recebido hoje", f"R$ {summary['received_today']:.2f}")
    with c3:
        st.metric("Saldo do dia", f"R$ {summary['balance_today']:.2f}")

    st.markdown("### Agenda")
    schedules = list_schedules(limit=10)
    if schedules:
        for row in schedules:
            st.write(f"{row['date']} {row['time']} • {row['client']} • {row['status']}")
    else:
        st.info("Sem agendamentos cadastrados.")

    st.markdown("### Financeiro")
    entries = list_financial_entries(limit=10)
    if entries:
        for row in entries:
            st.write(f"{row['date']} • {row['type']} • {row['description']} • R$ {row['amount']:.2f}")
    else:
        st.info("Sem lançamentos cadastrados.")


if not st.session_state.get("logged_in"):
    app_header("DS STUDIO GO", "Operação rápida do DSYSTEM no celular")
    login_box()
    st.stop()

require_login()
view = st.session_state.get("current_view", "home")

if view == "agenda":
    render_agenda()
elif view == "financeiro":
    render_financeiro()
elif view == "resumo":
    render_resumo()
else:
    render_home()

render_bottom_nav(view)
