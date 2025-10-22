# Statistical Engine for Neural Trading Intelligence and Nonlinear Economic Learning

This repository is a comprehensive backend template for research and engineering workflows that combine deep learning forecasting with financial and economic data. It bundles data ingestion, feature engineering, model training, serving, and walk‑forward backtesting in a single, modular FastAPI service.

The codebase is intentionally opinionated about structure and reproducibility. The README below documents architecture, components, developer workflows, deployment hints, observability, testing, and legal/licensing notes.

---

## Table of contents
- Project overview
- Key features
- Architecture & directory map
- Core components (what's implemented)
- Getting started (dev) — quick install
- Configuration & environment variables
- Running the API locally
- Database, migrations, and Alembic
- Storage & data layout (S3 / MinIO, folder conventions)
- Caching (Redis)
- Models, training and backtesting
- API reference (top-level endpoints)
- Observability & metrics (Prometheus)
- Security and auth
- Tests, CI, and pre-commit
- Contributing and development notes
- Legal & license (see `LICENSE`)

---

## Project overview

This project implements a full-stack pipeline for time-series forecasting and backtesting focused on financial instruments and macro/alternative datasets.

Primary goals:

- Provide reproducible, testable pipelines for feature extraction and model training.
- Offer a simple HTTP API to manage assets, feature-sets, models, training jobs, forecasts, signals, and backtests.
- Keep development ergonomics high (fast local iteration, pre-commit, linters, pinned deps in `requirements.txt`).

Intended users:

- Quant researchers and data scientists building daily/higher-frequency forecasting models.
- Engineers looking for a starter template to ship model training and inference behind an API.

Important: This repository is a template and not financial advice. Any strategy or model built using it should be validated thoroughly before real-world use.

## Key features

- FastAPI-based REST service with structured v1 routers.
- SQLModel (SQLAlchemy) models and Alembic migrations for schema management.
- S3/MinIO client baked in for artifact storage and folder conventions for raw/curated/features/preds/backtests.
- Redis client for caching and lightweight coordination.
- Pydantic v1 schemas for strict validation of API inputs/outputs.
- Global error handler and middleware for request IDs and timing headers.
- Minimal CI workflow (GitHub Actions) and pre-commit hooks recommended for code quality.

## Architecture & directory map

Top-level layout (abbreviated):

- `app/`
	- `main.py` — FastAPI application wiring, middleware and router registration.
	- `core/` — settings, middleware, logging, security, pagination and ids helpers.
	- `routers/v1/` — all v1 API routers (system, catalog, data, models, train, forecast, signals, portfolio, backtest, diagnostics, admin).
	- `models/` — SQLModel data models and any model artifacts.
	- `clients/` — S3 and Redis client factories.
	- `schemas/v1/` — Pydantic schemas for API contracts.
	- `db.py` — engine factory and helpers for SQLModel metadata management.
- `alembic/` — migration scaffold and generated revisions.
- `configs/` — YAML configuration for asset lists, model configs, etc.
- `data/` — local data sources and feature outputs (developer-managed storage layout).
- `tests/` — minimal tests (restore or expand as needed).

Each module is designed to be small and composable. The routers call into the models and DB helper and rely on Pydantic schemas for validation; storage/caching are accessed via client helper functions so they can be mocked in tests.

## Core components (what's implemented)

- app/core/settings.py: Pydantic BaseSettings wrapper (lazy-loading) for safe import in environments that don't set all env vars.
- app/core/middleware.py: RequestID and Timing middleware. Adds `X-Request-ID` and `X-Response-Time` headers.
- app/core/errors.py: `APIError` exception shape and global JSON error handler that includes request_id.
- app/core/logging.py: Central logging configuration invoked at startup.
- app/core/security.py: JWT helpers and HTTPBearer auth scaffolding.
- app/core/pagination.py and ids.py: small helpers for pagination and request_id access.
- app/models/models.py: SQLModel classes (Asset, FeatureSet, ModelRegistry, Job, Forecast, Signal, BacktestRun, Metric, DataSlice).
- app/clients/storage.py and cache.py: S3 & Redis clients (return None when not configured, safe for local dev).
- Routers: v1 endpoints for system (/health, /version, /metrics), catalog (assets & models), data (feature-sets), and stubs for train/forecast/signals/backtest/admin/diagnostics/portfolio.

## Getting started (development)

Prerequisites:

- Python 3.11 (CI targets 3.11) — local development with 3.10+ should work but CI uses 3.11.
- A POSIX shell (zsh on macOS is standard here).

Quick setup:

```bash
# create and activate virtualenv
python -m venv .venv
source .venv/bin/activate

# install pinned dependencies
pip install -r requirements.txt
```

Create a `.env` file with the minimum required environment variables (see next section). For development you can use SQLite for `DATABASE_URL`.

## Configuration & environment variables

Minimum env vars the app expects at runtime:

- DATABASE_URL — SQLAlchemy URL (e.g. `sqlite:///./dev.sqlite3` or a Postgres URL `postgresql://user:pass@host:5432/db`).
- JWT_SECRET — symmetric key for signing JWT tokens used by the security helpers.

Optional env vars:

- REDIS_URL — e.g. `redis://localhost:6379/0`.
- S3_ENDPOINT, S3_ACCESS_KEY, S3_SECRET_KEY, S3_BUCKET — for S3/MinIO artifact storage.
- FRED_API_KEY — optional key for FRED data access.

The project uses `python-dotenv` semantics; `app/core/settings.py` reads `.env` if present.

## Running the API locally

Create DB (SQLite example) and start:

```bash
export DATABASE_URL=sqlite:///./dev.sqlite3
export JWT_SECRET='dev-secret'
.venv/bin/python -c "from app import db; db.init_db()"
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs (FastAPI OpenAPI UI).

## Database & migrations (Alembic)

This repo includes an Alembic scaffold under `alembic/`. During development we used file-backed SQLite for quick iterations; for production you should use PostgreSQL.

Typical local migration workflow (replace placeholders):

```bash
export DATABASE_URL='postgresql://user:pass@host:5432/dbname'
export JWT_SECRET='your-jwt-secret'
.venv/bin/alembic revision --autogenerate -m "describe change"
.venv/bin/alembic upgrade head
```

Note: `app/core/settings.py` is lazy-loaded so `alembic/env.py` can import models without requiring all environment variables to be set at import time. However, running Alembic operations still requires a valid `DATABASE_URL` when connecting to the target DB.

## Storage & folder conventions

S3/MinIO is used for large artifacts and model outputs. The repository includes conventions for object prefixes:

- `raw/` – raw downloaded or ingested files
- `curated/` – cleaned and merged datasets
- `features/` – feature matrix exports
- `preds/` – model predictions / forecast outputs
- `backtests/` – backtest reports and artifacts

`app/clients/storage.py` exposes a `get_s3_client()` factory. When `S3_ENDPOINT` is not set, storage calls are no-ops (None returned) to keep local development cheap.

## Caching & coordination (Redis)

`app/clients/cache.py` exposes `get_redis_client()` which returns a `redis` client when `REDIS_URL` is set. Use Redis to store ephemeral results, lightweight job coordination or rate-limiting counters.

## Models, training, and backtesting

The `pipeline/` and `models/` directories contain skeletons for dataset construction, training loops and deep learning model artifacts.

Key pieces:

- `pipeline/train.py` — training loop (wiring only; extend with actual model & optimization loop).
- `models/dl_model.py` — model class and utilities for saving/loading PyTorch artifacts.
- `backtest/engine.py` — backtest harness that replays forecasts and computes returns/metrics.

The repo purposefully separates the training runtime from the API layer. Training typically reads from `data/features/`, writes model artifacts to S3 or local `artifacts/` folder, and registers models in the DB via `ModelRegistry`.

## API reference (high-level)

Routes are grouped under `/v1` and documented via OpenAPI at `/docs`:

- System
	- `GET /v1/health` — basic liveness check that returns a request ID.
	- `GET /v1/version` — returns the application version.
	- `GET /v1/metrics` — exposes Prometheus metrics (default registry).

- Catalog
	- `GET /v1/catalog/assets` — list assets.
	- `POST /v1/catalog/assets` — create an asset.
	- `GET /v1/catalog/models?stage=` — list registered models; filter by stage.
	- `POST /v1/catalog/models` — register a new model artifact.

- Data
	- `GET /v1/data/feature-sets` — list available feature-sets.

- Training / Forecast / Signals / Backtest / Admin
	- Routers exist as scaffolds under `app/routers/v1/` (train_router, forecast_router, signals_router, backtest_router, admin_router). Extend these with business logic for scheduling jobs, querying runs, and fetching artifacts.

Schemas are enforced via Pydantic models in `app/schemas/v1/`.

## Observability & metrics

- Prometheus metrics exposed at `GET /v1/metrics` via `prometheus_client` default registry.
- Logging is centrally configured and invoked at app startup. Correlate logs with `X-Request-ID` header added by middleware.

## Security

- JWT-based helpers live in `app/core/security.py`. The project uses symmetric HS256 JWT by default; production deployments should use a secure secret stored in a vault.
- All security helpers are dependency-injectable; endpoints should require authentication and validate scopes where needed.

## Testing, CI & pre-commit

- Tests: small smoke tests included under `tests/`. Expand these with unit and integration tests as you add functionality.
- CI: GitHub Actions workflow is configured for Python 3.11 and runs linting with `ruff` and `pytest`. The workflow is defensive and skips `pytest` if no `tests/` folder exists.
- Pre-commit: `.pre-commit-config.yaml` is included and recommends `black`, `ruff`, and `isort` hooks.

Local test run (example):

```bash
export DATABASE_URL=sqlite:///./dev.sqlite3
export JWT_SECRET='dev-secret'
.venv/bin/pytest -q
```

## Contributing and development notes

- Follow pre-commit hooks and run the linter locally (`ruff`) before opening PRs.
- Keep migrations in `alembic/versions/` small and descriptive.
- When adding new endpoints, add a Pydantic schema under `app/schemas/v1/`, update router docs `tags`, and add a unit test.

## Legal & license

This repository contains a `LICENSE` file in the project root. The license is intentionally restrictive; please read it carefully. This README and other documentation are for developer orientation only.