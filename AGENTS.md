# AGENTS.md – Cursor AI project guide

This file helps AI assistants (e.g. Cursor) understand and work with this codebase.

## Project overview

**Data Wellness Q&A Chatbot** – A reverse chatbot that asks users questions about data integration practices and gives advice from a knowledge base. It behaves like an agent that gathers information through an unspecified number of questions before giving advice.

- **Backend**: Python 3.13, aiohttp, Socket.IO, LangChain/OpenAI, PostgreSQL
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS – lives in the **git submodule** `data-wellness-companion-ui`
- **Served UI**: Built output is copied to `ui/` at repo root; the Python server serves static files from there

## Repository structure

```
data-questionnaire-agent/
├── data_questionnaire_agent/     # Main Python package
│   ├── bootstrap/                # Startup: config loader, consultant loader, SQL scripts
│   ├── cli/                      # CLI tools (e.g. prompt_to_db_loader)
│   ├── model/                    # Pydantic/data models
│   ├── server/                   # aiohttp app, routes, Socket.IO
│   ├── service/                  # Business logic (advice, persistence, reports, etc.)
│   ├── test/                     # Pytest tests
│   ├── ui/                       # Chainlit/playground UI helpers (not the web UI)
│   ├── utils/
│   ├── config.py                 # Runtime config (reads from DB global config)
│   ├── config_support.py         # DB connection string from env
│   ├── db_config.py              # DB config, loads .env
│   ├── build.py                  # Builds UI from submodule → ui/
│   └── ...
├── data-wellness-companion-ui/   # Git submodule – React/TS frontend source
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── hooks/
│   │   ├── i18n/
│   │   ├── model/
│   │   └── ...
│   ├── config/                   # index-template.html, ui-configs.json
│   └── package.json              # Yarn, Vite, React, TypeScript
├── ui/                           # Built frontend (generated; do not edit here)
├── sql/                          # PostgreSQL schema and setup (db_setup.sql, etc.)
├── i18n/                         # Backend translations (messages.*.yml)
├── prompts_*.toml                # Per-language prompts
├── pyproject.toml                # Python deps (uv), scripts, ruff config
└── .env                          # Not committed; copy from .env.local
```

## Setup and tooling

### Python

- **Package manager**: **uv** (create venv and install deps).
- **Python version**: 3.13 (see `pyproject.toml`).
- **Commands**:
  - `uv venv` then activate (e.g. `.\.venv\Scripts\activate` on Windows).
  - `uv sync` to install dependencies.

### Frontend (submodule)

- **Package manager**: **Yarn**.
- **Node**: 18.18.0 or later.
- **Submodule**: Run `git submodule init` and `git submodule update` after clone.

### Database

- **PostgreSQL** required. Create DB (e.g. `data_wellness_companion`), then run `sql/db_setup.sql`.
- Connection uses env: `DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PORT`, `DB_PASSWORD` (see `config_support.create_db_conn_str`).

### Configuration

- **`.env`**: Copy from `.env.local` and adjust. Used for DB and for loading into **global configuration** in the DB.
- **Runtime config**: Most app settings come from the **database** table `TB_GLOBAL_CONFIGURATION`, not only from `.env`. Use `data_questionnaire_agent.bootstrap.global_config_loader` to sync `.env` (non-DB keys) into that table.
- **Knowledge base**: `RAW_TEXT_FOLDER` must point to a directory containing `*.txt` documents; server fails if it’s empty.

## Running the application

1. **Database**: Ensure Postgres is running and `sql/db_setup.sql` has been applied.
2. **Backend**:  
   `python ./data_questionnaire_agent/server/questionnaire_server_main.py`  
   Or on Windows: `.\start.ps1`
3. **Ports**: Server/WebSocket default port is **8080** (configurable via `WEBSOCKET_PORT` in global config). The built UI is typically set to connect to port **8085**; if the server uses another port, update the UI config so the client connects to the same one.
4. **UI**: Open `http://localhost:8085/index.html` (or the port you use).

## Building the UI

- From **repo root**:  
  `python .\data_questionnaire_agent\build.py`  
  This runs `yarn` and `yarn run build` in `data-wellness-companion-ui` and copies the result to `ui/`.
- Do **not** edit files under `ui/` by hand; they are generated from `data-wellness-companion-ui`.

## Tests

- **Python**: `pytest` (from repo root or package directory).
- **Frontend**: In `data-wellness-companion-ui`, run `yarn test` (Jest).

## Code style and formatting

- **Python**:  
  - **black** and **ruff** (line-length 120, see `pyproject.toml` and `format.ps1`).  
  - Format/lint: `.\format.ps1` or `black .` and `ruff check --fix .`
- **Frontend**:  
  - **Prettier** and **ESLint** in `data-wellness-companion-ui` (`yarn format`, `yarn lint`).

## VS Code / Cursor

- **Launch configs** in `.vscode/launch.json`:
  - **Python Debugger: Start Server** – runs `questionnaire_server_main.py`.
  - **Python Debugger: Consultant Loader** – runs consultant loader with args (e.g. `bootstrap-photos`).
  - **Python Debugger: Current File** – runs the active file.

## Important conventions for edits

1. **Python**: Prefer `pathlib.Path`, type hints, and the existing patterns in `config.py` and `server/` (aiohttp, middleware, route registration).
2. **Config**: Add new runtime options via **global configuration** (DB) and/or `.env` as appropriate; document in README or here if they affect setup.
3. **UI**: All React/TS source lives in `data-wellness-companion-ui`; build with `build.py` to refresh `ui/`.
4. **i18n**: Backend uses `i18n/messages.*.yml`; frontend uses `data-wellness-companion-ui/src/i18n/` and related config.
5. **Prompts**: Edit `prompts_*.toml` for per-language prompt changes.

## Useful entry points

| Purpose              | Location |
|----------------------|----------|
| Server entry         | `data_questionnaire_agent/server/questionnaire_server_main.py` |
| App and routes       | `data_questionnaire_agent/server/questionnaire_server.py` (+ other `questionnaire_server_*.py` files) |
| Main config          | `data_questionnaire_agent/config.py` |
| DB connection        | `data_questionnaire_agent/config_support.py`, `db_config.py` |
| Load global config   | `data_questionnaire_agent/bootstrap/global_config_loader.py` |
| UI build script      | `data_questionnaire_agent/build.py` |
| Frontend app entry   | `data-wellness-companion-ui/src/main.tsx`, `App.tsx` |

When making changes, run the relevant tests (`pytest` and/or `yarn test` in the submodule) and keep `AGENTS.md` and README in sync if you add new setup or run steps.
