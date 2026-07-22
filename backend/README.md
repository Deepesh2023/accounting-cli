# Printos Accounting API — Backend

A FastAPI-based accounting backend with inventory, sales, purchases, party management, expenses, quotations, ledgers, and reports.

---

## Requirements

- **Python 3.14+**
- **uv** (package manager) — install once:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  or `pip install uv`

---

## Quick start

```bash
# Get in the backend folder
cd backend

# Install everything (one time)
uv sync

# Run the dev server (with auto-reload)
uv run fastapi dev
```

Open `http://127.0.0.1:8000/docs` in your browser — that's the interactive API explorer.

---

## Project layout

```
backend/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── api/                  # Route handlers (REST endpoints)
│   ├── inventory/            # Products & stock
│   ├── sale/                 # Sales (invoices)
│   ├── purchase/             # Purchases (bills)
│   ├── parties/              # Customers & suppliers
│   ├── expenses/             # Expenses
│   ├── quotation/            # Quotations
│   ├── company/              # Company profile
│   ├── ledger/               # Double-entry bookkeeping
│   ├── reports/              # Trading, P&L, balance sheet
│   ├── shared/               # Shared utilities & constants
│   └── storage/              # Database engine
├── tests/                    # Test files (pytest)
├── pyproject.toml            # Dependencies & config
└── uv.lock                   # Locked dependency versions
```

Each domain follows a **service → repository → model** pattern:

| Layer | What it does | Example |
|---|---|---|
| `api/` | HTTP routes — receives requests, returns JSON | `GET /api/inventory` |
| `service/` | Business logic — tax calc, validation, ledger | `SaleService.record_sale()` |
| `repository/` | Database queries — talks to SQLite/SQLModel | `InventoryRepository.get_product()` |
| `models/` | Database table definitions | `class Product(SQLModel, table=True)` |

---

## Useful commands

All commands run from the **`backend/`** folder.

### Run tests
```bash
uv run pytest                    # all tests
uv run pytest -q                 # quiet mode (just dots)
uv run pytest tests/test_sale_service.py  # a specific file
```

### Run the dev server
```bash
uv run fastapi dev               # auto-reload on file changes
uv run fastapi dev --port 9000   # different port
```

### Add a dependency
```bash
uv add numpy
```

### Check types / lint
```bash
uv run mypy src/
uv run ruff check src/
```

---

## Generate a TypeScript client for the frontend

```bash
bash scripts/generate-frontend-client.sh
```

This spins up the server, downloads the OpenAPI spec, and runs
[`openapi-typescript`](https://npmjs.com/package/openapi-typescript) to
generate `frontend/src/lib/api/schema.d.ts` with full TypeScript types for
every endpoint, request body, and response.

If `npx` isn't installed yet, it copies the raw `openapi.json` instead.

---

## API overview

| Endpoint | Purpose |
|---|---|
| `GET /api/inventory` | List products |
| `POST /api/inventory` | Add a product |
| `GET /api/sales` | List invoices |
| `POST /api/sales` | Create a sale |
| `GET /api/parties` | List customers & suppliers |
| `GET /api/reports/profit-and-loss` | P&L statement |
| `GET /api/ledger/gst-summary` | GST summary |

Full docs at `http://127.0.0.1:8000/docs` when the server is running.

---

## Database

By default it uses an **in-memory SQLite database** (resets when you stop the server).

To use a persistent database:
```bash
export DATABASE_URL="sqlite:///data.db"
uv run fastapi dev
```

---

## Common "help I'm stuck" fixes

| Problem | Fix |
|---|---|
| `uv: command not found` | Install uv (see **Requirements**) |
| `ModuleNotFoundError` | Did you run `uv sync`? |
| `port 8000 already in use` | Use `--port 9000` |
| Tests fail after pulling from git | `uv sync` to update deps |
