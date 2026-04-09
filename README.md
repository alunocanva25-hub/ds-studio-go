## DS STUDIO GO v2.2

Versão corrigida para evitar os erros de atalhos e navegação no Streamlit Cloud.

### O que mudou nesta versão
- removida a dependência de multipage com `st.page_link()` e `st.switch_page()`
- agora toda a navegação acontece dentro de um único `app.py`
- atalhos da home levam para as telas sem quebrar no Streamlit Cloud
- adicionados botões de voltar
- adicionada navegação inferior estilo app

## Módulos
- Login
- Agendamento rápido
- Financeiro rápido
- Resumo do dia

## Usuários de teste
- admin / 123456
- operacional / 123456

## Rodar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publicar
1. Suba este projeto para um repositório no GitHub.
2. Conecte o repositório no Streamlit Community Cloud.
3. Escolha `app.py` como arquivo principal.

## Como sincronizar com o DSYSTEM de verdade
Esta versão continua usando SQLite local apenas para demonstração.

Fluxo profissional recomendado:

**DS STUDIO GO -> API segura -> Banco do DSYSTEM**

- o app envia login, agendamento e financeiro para uma API
- a API valida usuário, permissões e regras
- a API consulta ou grava no banco oficial do DSYSTEM
- o app exibe o retorno já tratado
