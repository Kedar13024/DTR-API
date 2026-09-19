# Disaster Response Tracker API

FastAPI backend for reporting, managing, and voting on disaster incidents.

## Layout

- `app/main.py` — FastAPI application entry point.
- `app/api/core/` — configuration.
- `app/api/db/` — SQLAlchemy engine, sessions, and ORM base.
- `app/api/models/` — database models.
- `app/api/schemas/` — request and response schemas.
- `app/api/services/` — reusable services such as password hashing.
- `app/api/v1/endpoints/` — versioned route handlers.
- `alembic/` — database migrations.
- `tests/` — automated tests.

## Configuration

Copy `.env.example` to `.env` and replace the placeholder values with your local
PostgreSQL credentials and a strong JWT secret. Do not commit `.env`.

## Run locally

From the repository root, install dependencies and start the API:

```powershell
uv sync --project backend
uv run --project backend fastapi dev backend/app/main.py
```

Apply migrations with:

```powershell
uv run --project backend alembic -c backend/alembic.ini upgrade head
```
