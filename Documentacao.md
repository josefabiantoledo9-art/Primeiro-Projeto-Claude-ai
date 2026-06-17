
# Documentação Técnica — Gerenciador de Tarefas (To-Do App)

## Visão Geral

Aplicação web de gerenciamento de tarefas construída com **Streamlit** e **SQLite**, permitindo criar, listar, filtrar, concluir e deletar tarefas com persistência local de dados.

---

## Tecnologias Utilizadas

| Tecnologia | Versão mínima | Finalidade |
|---|---|---|
| Python | 3.8+ | Linguagem principal |
| Streamlit | 1.35.0 | Interface web |
| SQLite | nativo | Banco de dados local |

---

## Estrutura do Projeto

```
Primeiro-Projeto-Claude-ai/
├── app.py           # Interface Streamlit (camada de apresentação)
├── database.py      # Acesso ao banco de dados SQLite (camada de dados)
├── requirements.txt # Dependências do projeto
└── tasks.db         # Banco de dados gerado automaticamente na primeira execução
```

---

## Módulos

### `database.py`

Responsável por toda a comunicação com o banco de dados SQLite.

#### Constante

```python
DB_PATH = "tasks.db"
```

Caminho do arquivo de banco de dados gerado localmente.

#### Funções

| Função | Parâmetros | Retorno | Descrição |
|---|---|---|---|
| `get_connection()` | — | `Connection` | Abre conexão com o SQLite com `row_factory` configurado para retornar dicionários |
| `init_db()` | — | `None` | Cria a tabela `tasks` se não existir |
| `add_task()` | `title`, `description`, `priority` | `int` (id) | Insere uma nova tarefa |
| `get_tasks()` | `priority_filter`, `status_filter` | `list[dict]` | Retorna tarefas com filtros opcionais, ordenadas por prioridade |
| `toggle_task()` | `task_id`, `completed` | `None` | Marca ou desmarca uma tarefa como concluída |
| `delete_task()` | `task_id` | `None` | Remove uma tarefa pelo ID |

#### Schema do Banco de Dados

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    priority    TEXT    NOT NULL CHECK(priority IN ('Alta', 'Média', 'Baixa')),
    completed   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL
);
```

#### Ordenação das tarefas

```sql
ORDER BY
  CASE priority
    WHEN 'Alta'  THEN 1
    WHEN 'Média' THEN 2
    WHEN 'Baixa' THEN 3
  END,
  created_at DESC
```

---

### `app.py`

Camada de apresentação usando Streamlit. Organizado em três funções principais.

#### `render_sidebar()`
- Formulário de criação de tarefa (título obrigatório, descrição opcional, prioridade)
- Filtros de listagem por prioridade e status
- Retorna `(priority_filter, status_filter)`

#### `render_task_card(task)`
- Checkbox para marcar/desmarcar como concluída
- Ícone de prioridade (🔴 Alta / 🟡 Média / 🟢 Baixa)
- Título com tachado quando concluída
- Descrição, data de criação e botão de exclusão

#### `main()`
1. Inicializa o banco de dados
2. Renderiza a sidebar e captura os filtros
3. Busca as tarefas filtradas
4. Exibe métricas (Total / Pendentes / Concluídas)
5. Separa e renderiza tarefas pendentes e concluídas em seções distintas

---

## Funcionalidades

| Funcionalidade | Implementação |
|---|---|
| Adicionar tarefa | Formulário na sidebar com validação de título obrigatório |
| Listar tarefas | `get_tasks()` com ordenação por prioridade |
| Marcar como concluída | Checkbox que chama `toggle_task()` e recarrega a página |
| Deletar tarefa | Botão 🗑️ que chama `delete_task()` e recarrega a página |
| Filtrar por prioridade | Selectbox: Todas / Alta / Média / Baixa |
| Filtrar por status | Selectbox: Todas / Pendentes / Concluídas |
| Persistência de dados | SQLite local no arquivo `tasks.db` |

---

## Como Executar

```bash
git clone https://github.com/josefabiantoledo9-art/Primeiro-Projeto-Claude-ai.git
cd Primeiro-Projeto-Claude-ai
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

---

## Fluxo de Dados

```
Usuário (navegador)
       │
       ▼
   app.py (Streamlit)
       │
       ▼
  database.py
       │
       ▼
   tasks.db (SQLite)
```

---

Selecione tudo desde o `#` do título até o final, cole no editor do GitHub e clique em **Commit changes**.

