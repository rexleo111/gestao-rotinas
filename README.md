# Sistema de Gestão de Rotinas

Sistema backend desenvolvido com Python e Flask para gerenciamento de rotinas pessoais. Permite que usuários se cadastrem e registrem atividades recorrentes (como estudo ou exercício), com controle de execução diária e registro de logs.

## Estrutura do Banco de Dados

O sistema possui 4 tabelas com relacionamentos 1:N:

### Tabela `usuarios`
| Coluna     | Tipo         | Descrição                    |
|------------|--------------|------------------------------|
| id         | Integer (PK) | Identificador único          |
| nome       | String(100)  | Nome do usuário              |
| email      | String(150)  | E-mail (único)               |
| criado_em  | DateTime     | Data de criação              |

### Tabela `rotinas`
| Coluna      | Tipo         | Descrição                        |
|-------------|--------------|----------------------------------|
| id          | Integer (PK) | Identificador único              |
| titulo      | String(100)  | Nome da rotina                   |
| descricao   | String(255)  | Descrição da rotina              |
| ativa       | Boolean      | Se a rotina está ativa ou não    |
| usuario_id  | Integer (FK) | Referência ao usuário (1:N)      |
| criada_em   | DateTime     | Data de criação                  |

### Tabela `execucoes`
| Coluna         | Tipo         | Descrição                         |
|----------------|--------------|-----------------------------------|
| id             | Integer (PK) | Identificador único               |
| rotina_id      | Integer (FK) | Referência à rotina (1:N)         |
| data_execucao  | Date         | Data em que a rotina foi executada|
| observacao     | String(255)  | Observação opcional               |

### Tabela `logs`
| Coluna    | Tipo         | Descrição                          |
|-----------|--------------|------------------------------------|
| id        | Integer (PK) | Identificador único                |
| acao      | String(100)  | Tipo da ação registrada            |
| descricao | String(255)  | Detalhes da ação                   |
| data_hora | DateTime     | Data e hora do registro            |

### Relacionamentos
- `usuarios` 1:N `rotinas` — um usuário pode ter várias rotinas
- `rotinas` 1:N `execucoes` — uma rotina pode ter várias execuções

## Rotas Disponíveis

### Usuários (`/usuarios`)
| Método | Rota                    | Descrição               |
|--------|-------------------------|-------------------------|
| GET    | `/usuarios/`            | Listar todos os usuários|
| GET/POST | `/usuarios/criar`     | Criar novo usuário      |
| GET/POST | `/usuarios/<id>/editar` | Editar usuário        |
| GET    | `/usuarios/<id>/deletar`| Deletar usuário         |

### Rotinas (`/rotinas`)
| Método | Rota                      | Descrição                    |
|--------|---------------------------|------------------------------|
| GET    | `/rotinas/`               | Listar todas as rotinas      |
| GET/POST | `/rotinas/criar`        | Criar nova rotina            |
| GET/POST | `/rotinas/<id>/editar`  | Editar rotina                |
| GET    | `/rotinas/<id>/toggle`    | Ativar/desativar rotina      |
| GET    | `/rotinas/<id>/deletar`   | Deletar rotina               |

### Execuções (`/execucoes`)
| Método | Rota                       | Descrição                     |
|--------|----------------------------|-------------------------------|
| GET    | `/execucoes/`              | Listar todas as execuções     |
| GET/POST | `/execucoes/criar`       | Registrar execução de rotina  |
| GET    | `/execucoes/<id>/deletar`  | Deletar execução              |

### Logs (`/logs`)
| Método | Rota      | Descrição                  |
|--------|-----------|----------------------------|
| GET    | `/logs/`  | Listar todos os logs       |

### Páginas (`/`)
| Método | Rota | Descrição       |
|--------|------|-----------------|
| GET    | `/`  | Página inicial  |

## Regras de Negócio

### 1. Execução única por dia
Cada rotina só pode ser executada **uma única vez por dia**. Se o usuário tentar registrar a mesma rotina no mesmo dia, o sistema bloqueia e exibe a mensagem: *"Esta rotina já foi executada hoje."*

### 2. Apenas rotinas ativas podem ser executadas
Somente rotinas com status **ativa** podem receber execuções. Se a rotina estiver desativada, o sistema bloqueia e exibe: *"Rotina inativa. Não é possível registrar execução."*

### 3. Registro de logs
Todas as ações relevantes são registradas automaticamente na tabela de logs, incluindo: criação de usuário, criação de rotina, ativação/desativação de rotina e execução de rotina.

## Instruções para Execução

### Pré-requisitos
- Python 3.10+
- MySQL Server rodando na porta 3306

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/rexleo111/gestao-rotinas.git
cd gestao-rotinas
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Instale as dependências:
```bash
pip install flask flask-sqlalchemy flask-migrate pymysql python-dotenv
```

4. Crie o arquivo `.env` na raiz:

DATABASE_URL=mysql+pymysql://root:@localhost:3306/gestao_rotinas_db
SECRET_KEY=
FLASK_APP=run.py
FLASK_ENV=development


5. Crie o banco no MySQL:
```sql
CREATE DATABASE gestao_rotinas_db;
```

6. Rode as migrations:
```bash
$env:FLASK_APP = "run.py"
flask db init
flask db migrate -m "cria tabelas"
flask db upgrade
```

7. Inicie o servidor:
```bash
flask run
```

8. Acesse no navegador:
http://127.0.0.1:5000/

## Tecnologias Utilizadas
- Python 3.13
- Flask
- Flask-SQLAlchemy (ORM)
- Flask-Migrate (Migrations/Alembic)
- MySQL
- Jinja2 (Templates)