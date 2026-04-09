from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'data' / 'ds_studio_go.db'

st.set_page_config(
    page_title='DS STUDIO GO',
    page_icon='📱',
    layout='centered',
    initial_sidebar_state='collapsed',
)

CUSTOM_CSS = """
<style>
    .block-container {padding-top: 1rem; padding-bottom: 5rem; max-width: 760px;}
    .main-card {
        background: linear-gradient(145deg, #121212 0%, #1d1d1d 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,.18);
        margin-bottom: 12px;
    }
    .metric-card {
        background: #171717;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 14px;
        text-align: center;
        min-height: 100px;
    }
    .metric-title {font-size: .85rem; opacity: .75; margin-bottom: 8px;}
    .metric-value {font-size: 1.35rem; font-weight: 700;}
    .section-title {font-size: 1.05rem; font-weight: 700; margin-bottom: .35rem;}
    .muted {opacity: .75; font-size: .92rem;}
    .hero {
        background: linear-gradient(135deg, #7a1424 0%, #30050d 100%);
        border-radius: 22px;
        padding: 20px;
        color: white;
        margin-bottom: 14px;
        border: 1px solid rgba(255,255,255,0.10);
    }
    .hero h1 {font-size: 1.5rem; margin: 0 0 .2rem 0;}
    .hero p {margin: 0; opacity: .85;}
    div[data-testid='stForm'] {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px;
        background: #141414;
    }
    .stButton > button, div[data-testid='stFormSubmitButton'] > button {
        width: 100%; border-radius: 14px; min-height: 46px; font-weight: 700;
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(get_connection()) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                display_name TEXT NOT NULL,
                role TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                service_name TEXT NOT NULL,
                professional_name TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                notes TEXT,
                status TEXT NOT NULL DEFAULT 'Agendado',
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS finance_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_type TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_method TEXT NOT NULL,
                entry_date TEXT NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute('SELECT COUNT(*) AS total FROM users')
        total_users = cur.fetchone()['total']
        if total_users == 0:
            cur.execute(
                'INSERT INTO users (username, password, display_name, role) VALUES (?, ?, ?, ?)',
                ('admin', '123456', 'Administrador', 'admin'),
            )
            cur.execute(
                'INSERT INTO users (username, password, display_name, role) VALUES (?, ?, ?, ?)',
                ('operacional', '123456', 'Operacional', 'operational'),
            )
        cur.execute('SELECT COUNT(*) AS total FROM appointments')
        if cur.fetchone()['total'] == 0:
            today = date.today()
            samples = [
                ('Maria Oliveira', 'Corte Feminino', 'Ana', today.isoformat(), '09:00', 'Cliente recorrente', 'Agendado'),
                ('João Silva', 'Barba', 'Carlos', today.isoformat(), '10:30', '', 'Agendado'),
                ('Beatriz Souza', 'Escova', 'Ana', (today + timedelta(days=1)).isoformat(), '14:00', '', 'Agendado'),
            ]
            cur.executemany(
                '''INSERT INTO appointments
                (client_name, service_name, professional_name, appointment_date, appointment_time, notes, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                [(*row, datetime.now().isoformat(timespec='seconds')) for row in samples],
            )
        cur.execute('SELECT COUNT(*) AS total FROM finance_entries')
        if cur.fetchone()['total'] == 0:
            today = date.today().isoformat()
            finance = [
                ('Entrada', 'Atendimento Maria Oliveira', 120.0, 'Pix', today, 'Pagamento concluído'),
                ('Saída', 'Compra de materiais', 45.0, 'Dinheiro', today, ''),
                ('Entrada', 'Atendimento João Silva', 60.0, 'Cartão', today, ''),
            ]
            cur.executemany(
                '''INSERT INTO finance_entries
                (entry_type, description, amount, payment_method, entry_date, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                [(*row, datetime.now().isoformat(timespec='seconds')) for row in finance],
            )
        conn.commit()


def authenticate(username: str, password: str) -> dict | None:
    with closing(get_connection()) as conn:
        row = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username.strip(), password.strip()),
        ).fetchone()
    return dict(row) if row else None


def add_appointment(client_name: str, service_name: str, professional_name: str, appointment_date: date, appointment_time: str, notes: str) -> None:
    with closing(get_connection()) as conn:
        conn.execute(
            '''INSERT INTO appointments
               (client_name, service_name, professional_name, appointment_date, appointment_time, notes, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, 'Agendado', ?)''',
            (
                client_name.strip(),
                service_name.strip(),
                professional_name.strip(),
                appointment_date.isoformat(),
                appointment_time,
                notes.strip(),
                datetime.now().isoformat(timespec='seconds'),
            ),
        )
        conn.commit()


def add_finance_entry(entry_type: str, description: str, amount: float, payment_method: str, entry_date: date, notes: str) -> None:
    with closing(get_connection()) as conn:
        conn.execute(
            '''INSERT INTO finance_entries
               (entry_type, description, amount, payment_method, entry_date, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (
                entry_type,
                description.strip(),
                amount,
                payment_method,
                entry_date.isoformat(),
                notes.strip(),
                datetime.now().isoformat(timespec='seconds'),
            ),
        )
        conn.commit()


def get_appointments_df() -> pd.DataFrame:
    with closing(get_connection()) as conn:
        df = pd.read_sql_query(
            '''SELECT id, client_name, service_name, professional_name,
                      appointment_date, appointment_time, status, notes
               FROM appointments
               ORDER BY appointment_date ASC, appointment_time ASC''',
            conn,
        )
    return df


def get_finance_df() -> pd.DataFrame:
    with closing(get_connection()) as conn:
        df = pd.read_sql_query(
            '''SELECT id, entry_type, description, amount, payment_method,
                      entry_date, notes
               FROM finance_entries
               ORDER BY entry_date DESC, id DESC''',
            conn,
        )
    return df


def currency_br(value: float) -> str:
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def render_login() -> None:
    st.markdown(
        """
        <div class='hero'>
            <h1>DS STUDIO GO</h1>
            <p>Versão mobile operacional para agendamentos e financeiro rápido.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader('Entrar')
    st.caption('Usuários de teste: admin / 123456 ou operacional / 123456')
    with st.form('login_form', clear_on_submit=False):
        username = st.text_input('Usuário', placeholder='Digite seu usuário')
        password = st.text_input('Senha', type='password', placeholder='Digite sua senha')
        submitted = st.form_submit_button('Acessar')
    if submitted:
        user = authenticate(username, password)
        if user:
            st.session_state['user'] = user
            st.success(f"Bem-vindo, {user['display_name']}.")
            st.rerun()
        else:
            st.error('Usuário ou senha inválidos.')
    st.markdown('</div>', unsafe_allow_html=True)


def render_home() -> None:
    user = st.session_state['user']
    appointments = get_appointments_df()
    finance = get_finance_df()
    today_iso = date.today().isoformat()

    today_appointments = appointments[appointments['appointment_date'] == today_iso].copy()
    today_finance = finance[finance['entry_date'] == today_iso].copy()

    received_today = today_finance.loc[today_finance['entry_type'] == 'Entrada', 'amount'].sum()
    spent_today = today_finance.loc[today_finance['entry_type'] == 'Saída', 'amount'].sum()
    balance_today = received_today - spent_today

    st.markdown(
        f"""
        <div class='hero'>
            <h1>Olá, {user['display_name']}</h1>
            <p>Use o menu abaixo para registrar ações rápidas no DS STUDIO GO.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Agenda de hoje</div><div class='metric-value'>{len(today_appointments)}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Recebido hoje</div><div class='metric-value'>{currency_br(received_today)}</div></div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Saídas hoje</div><div class='metric-value'>{currency_br(spent_today)}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><div class='metric-title'>Saldo do dia</div><div class='metric-value'>{currency_br(balance_today)}</div></div>", unsafe_allow_html=True)

    st.markdown('### Atalhos rápidos')
    action_cols = st.columns(2)
    if action_cols[0].button('Novo agendamento', use_container_width=True):
        st.session_state['nav'] = 'Novo agendamento'
        st.rerun()
    if action_cols[1].button('Novo lançamento', use_container_width=True):
        st.session_state['nav'] = 'Novo lançamento'
        st.rerun()

    st.markdown('### Próximos agendamentos')
    if today_appointments.empty:
        st.info('Nenhum agendamento para hoje.')
    else:
        for _, row in today_appointments.head(5).iterrows():
            st.markdown(
                f"""
                <div class='main-card'>
                    <div class='section-title'>{row['appointment_time']} — {row['client_name']}</div>
                    <div class='muted'>{row['service_name']} • {row['professional_name']} • {row['status']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('### Últimos lançamentos')
    if today_finance.empty:
        st.info('Nenhum lançamento financeiro hoje.')
    else:
        for _, row in today_finance.head(5).iterrows():
            st.markdown(
                f"""
                <div class='main-card'>
                    <div class='section-title'>{row['entry_type']} — {currency_br(float(row['amount']))}</div>
                    <div class='muted'>{row['description']} • {row['payment_method']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_new_appointment() -> None:
    st.subheader('Novo agendamento')
    st.caption('Fluxo rápido para celular.')
    with st.form('appointment_form', clear_on_submit=True):
        client_name = st.text_input('Cliente')
        service_name = st.selectbox('Serviço', ['Corte Feminino', 'Corte Masculino', 'Escova', 'Barba', 'Coloração', 'Outro'])
        professional_name = st.selectbox('Profissional', ['Ana', 'Carlos', 'Marina', 'Equipe 01'])
        appointment_date = st.date_input('Data', value=date.today())
        appointment_time = st.selectbox(
            'Horário',
            ['08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30'],
        )
        notes = st.text_area('Observação curta', max_chars=180)
        submitted = st.form_submit_button('Salvar agendamento')

    if submitted:
        if not client_name.strip():
            st.error('Informe o nome do cliente.')
        else:
            add_appointment(client_name, service_name, professional_name, appointment_date, appointment_time, notes)
            st.success('Agendamento salvo com sucesso.')
            st.balloons()


def render_new_finance() -> None:
    st.subheader('Novo lançamento financeiro')
    st.caption('Registro rápido de entrada ou saída.')
    with st.form('finance_form', clear_on_submit=True):
        entry_type = st.segmented_control('Tipo', options=['Entrada', 'Saída'], default='Entrada')
        description = st.text_input('Descrição')
        amount = st.number_input('Valor', min_value=0.0, step=1.0, format='%.2f')
        payment_method = st.selectbox('Forma de pagamento', ['Pix', 'Dinheiro', 'Cartão', 'Transferência', 'Boleto'])
        entry_date = st.date_input('Data', value=date.today())
        notes = st.text_area('Observação', max_chars=180)
        submitted = st.form_submit_button('Salvar lançamento')

    if submitted:
        if not description.strip():
            st.error('Informe a descrição do lançamento.')
        elif amount <= 0:
            st.error('Informe um valor maior que zero.')
        else:
            add_finance_entry(entry_type, description, float(amount), payment_method, entry_date, notes)
            st.success('Lançamento salvo com sucesso.')


def render_agenda() -> None:
    st.subheader('Agenda')
    df = get_appointments_df()
    selected_date = st.date_input('Filtrar por data', value=date.today(), key='agenda_filter_date')
    filtered = df[df['appointment_date'] == selected_date.isoformat()].copy()
    if filtered.empty:
        st.info('Nenhum agendamento para a data selecionada.')
        return
    for _, row in filtered.iterrows():
        st.markdown(
            f"""
            <div class='main-card'>
                <div class='section-title'>{row['appointment_time']} — {row['client_name']}</div>
                <div class='muted'>Serviço: {row['service_name']}</div>
                <div class='muted'>Profissional: {row['professional_name']}</div>
                <div class='muted'>Status: {row['status']}</div>
                <div class='muted'>Obs.: {row['notes'] or '-'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_finance() -> None:
    st.subheader('Financeiro do dia')
    df = get_finance_df()
    selected_date = st.date_input('Filtrar por data', value=date.today(), key='finance_filter_date')
    filtered = df[df['entry_date'] == selected_date.isoformat()].copy()
    received = filtered.loc[filtered['entry_type'] == 'Entrada', 'amount'].sum()
    spent = filtered.loc[filtered['entry_type'] == 'Saída', 'amount'].sum()
    balance = received - spent

    col1, col2, col3 = st.columns(3)
    col1.metric('Entradas', currency_br(received))
    col2.metric('Saídas', currency_br(spent))
    col3.metric('Saldo', currency_br(balance))

    if filtered.empty:
        st.info('Nenhum lançamento para a data selecionada.')
        return

    for _, row in filtered.iterrows():
        st.markdown(
            f"""
            <div class='main-card'>
                <div class='section-title'>{row['entry_type']} — {currency_br(float(row['amount']))}</div>
                <div class='muted'>{row['description']}</div>
                <div class='muted'>Pagamento: {row['payment_method']}</div>
                <div class='muted'>Obs.: {row['notes'] or '-'}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown('## DS STUDIO GO')
        st.caption('Menu principal')
        options = ['Início', 'Novo agendamento', 'Novo lançamento', 'Agenda', 'Financeiro']
        current = st.session_state.get('nav', 'Início')
        index = options.index(current) if current in options else 0
        nav = st.radio('Navegação', options, index=index)
        st.divider()
        if st.button('Sair', use_container_width=True):
            st.session_state.clear()
            st.rerun()
        return nav


def main() -> None:
    init_db()
    if 'user' not in st.session_state:
        render_login()
        return

    nav = render_sidebar()
    st.session_state['nav'] = nav

    if nav == 'Início':
        render_home()
    elif nav == 'Novo agendamento':
        render_new_appointment()
    elif nav == 'Novo lançamento':
        render_new_finance()
    elif nav == 'Agenda':
        render_agenda()
    elif nav == 'Financeiro':
        render_finance()


if __name__ == '__main__':
    main()
