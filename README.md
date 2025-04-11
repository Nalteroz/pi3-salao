# Projeto Integrador 3 - Sistema de agendamento Studio HEMA

## Como executar

### Pré-requisitos

1. Crie um ambiente virtual
2. Instale os requisitos em `requirements.txt`
3. Tenha um banco de dados PostgreSQL em branco.
4. Crie um arquivo .env e insira a connection string do banco junto com a chave jwt. Exemplo:
``` dotenv
BI_DATABASE_URI = postgresql://<user>:<senha>@localhost:5432/<banco>
JWT_SECRET_KEY = <token jwt>
```
5. Aplique as migrations com `flask db upgrade`
6. Rode o programa com `flask run`
