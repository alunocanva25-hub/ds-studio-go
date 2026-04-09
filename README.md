# DS STUDIO GO

Base inicial mobile em **Streamlit** para o projeto **DS STUDIO GO**.

## O que esta versão entrega
- Login simples
- Novo agendamento
- Novo lançamento financeiro
- Agenda do dia
- Financeiro do dia
- Banco SQLite local para testes
- Layout mobile-friendly

## Usuários de teste
- `admin` / `123456`
- `operacional` / `123456`

## Como rodar localmente
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura
```text
DS_STUDIO_GO/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
└── data/
    └── ds_studio_go.db
```

## Onde publicar
### 1. GitHub
Use o GitHub para armazenar o código-fonte, histórico de versões e futuras melhorias.

### 2. Streamlit Community Cloud
Use o Streamlit Community Cloud para publicar esta V1 rapidamente.

Fluxo:
1. criar repositório no GitHub
2. enviar todos os arquivos
3. abrir Streamlit Community Cloud
4. conectar ao GitHub
5. escolher o repositório
6. selecionar o arquivo `app.py`
7. publicar

## Observação importante
Esta base é ótima para validação rápida e demonstração.

Para ambiente mais profissional no futuro, o ideal é migrar para:
- backend/API própria
- autenticação real
- banco centralizado
- regras de permissão mais fortes
- hospedagem além do Streamlit
