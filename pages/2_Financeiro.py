from __future__ import annotations

import streamlit as st
from utils.auth import init_session, require_login
from utils.db import init_db, add_financial_entry, list_financial_entries
from utils.ui import inject_global_css, app_header, success_toast

st.set_page_config(page_title="Financeiro | DS STUDIO GO", page_icon="💸", layout="wide", initial_sidebar_state="collapsed")
inject_global_css()
init_db()
init_session()
require_login()

app_header("Lançamento rápido", "Registre entrada ou saída com poucos campos")

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
    if not description or amount <= 0:
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
