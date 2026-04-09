## DS STUDIO GO v2.1

Correção de navegação para Streamlit Cloud: substituído `st.page_link()` por `st.switch_page()` com botões.

# DS STUDIO GO — V2

Versão inicial premium do app mobile do DSYSTEM, feita em Streamlit para validação rápida.

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
Esta V2 usa SQLite local apenas para demonstração.

O caminho correto para sincronizar com o banco do DSYSTEM é:

### Opção recomendada
**DS STUDIO GO (mobile) -> API segura -> Banco do DSYSTEM**

Não é recomendado conectar o app mobile direto no banco principal.

### Fluxo ideal
1. O app envia login, agendamento e financeiro para uma API.
2. A API valida usuário, permissões e dados.
3. A API grava e consulta no banco oficial do DSYSTEM.
4. O app exibe o retorno já tratado.

### Por que isso é melhor
- mais segurança
- menos risco de corromper o banco
- regras centralizadas
- auditoria mais fácil
- evolução futura mais organizada

### Fases práticas
#### Fase 1
Demo local com SQLite.

#### Fase 2
Criar API em Flask ou FastAPI com rotas como:
- POST /login
- GET /agenda/hoje
- POST /agenda
- GET /financeiro/hoje
- POST /financeiro

#### Fase 3
Conectar a API ao banco real do DSYSTEM.

#### Fase 4
Publicar o mobile apontando para a API oficial.

## Onde alocar
### GitHub
Guardar código, versionar e atualizar.

### Streamlit Cloud
Publicar a V2 para testes e validação visual.

### Produção real
Quando for integrar de verdade ao banco principal, o ideal é hospedar a **API** em um servidor próprio/VPS/Render/Railway e deixar o Streamlit ou frontend consumindo essa API.
