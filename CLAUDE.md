# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZenLog is a Django REST API backend for personal wellness tracking. Three roles: patient (records daily wellness entries), coach (read-only access to assigned patients' data), admin (manages indicators and coach-patient assignments). API-only, no frontend.

## Commands

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run all tests
```bash
pytest tests/domain/ -v              # Domain tests (pure Python, no DB needed)
pytest tests/infrastructure/ -v      # Integration tests (requires PostgreSQL)
pytest --cov=zenlog --cov-report=html  # All tests with coverage
```

### Run a single test file or test
```bash
pytest tests/domain/test_tracking_service.py -v
pytest tests/domain/test_tracking_service.py::test_create_valid_entry -v
```

### Lint and format
```bash
ruff check .          # Lint
ruff check --fix .    # Lint with auto-fix
ruff format .         # Format
ruff format --check . # Format check (CI mode)
```

### Django management
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Environment
Requires PostgreSQL. Configure via `.env` file (see `.env.example`):
- `SECRET_KEY`, `DEBUG`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

## Architecture

**Hexagonal architecture (DDD)** with strict domain/infrastructure separation.

### Domain layer (`domain/`) — Pure Python, zero Django imports
- **`entities/`** — Dataclasses: `Indicator`, `WellnessEntry`, `Assignment`, `Trend` (value object)
- **`services/`** — Business logic: `TrackingService` (entry CRUD, trends), `CoachingService` (coach access control, patient data)
- **`ports/`** — Abstract repository interfaces (ABC): `WellnessEntryRepository`, `IndicatorRepository`, `AssignmentRepository`

### Infrastructure layer (`infrastructure/`) — Django/DRF adapters
- **`models.py`** — Django ORM models (implements DB schema from `zenlog_doc/MCD.mermaid`)
- **`repositories/`** — Concrete implementations of domain ports using Django ORM
- **`views/`** — DRF viewsets (API endpoints)
- **`serializers/`** — DRF serializers
- **`permissions/`** — Role-based DRF permissions (`IsPatient`, `IsCoach`, `IsAdmin`)
- **`urls.py`** — API routing

### Two Bounded Contexts
1. **Wellness Tracking** (core) — Patient entry creation, validation (value in indicator range, one entry per indicator per day), history, trend computation
2. **Coaching** — Coach read-only access conditioned on active `Assignment`; admin manages assignments

### Key domain rules
- One wellness entry per patient per indicator per day (uniqueness invariant)
- Entry value must be within indicator's `[min_value, max_value]` range
- Coach access requires an active `Assignment` linking coach to patient
- Trend averages exclude days without entries (no zero-fill)

## Code Conventions

- **Language**: Code in English, documentation in French
- **Commits**: Conventional Commits enforced by Commitizen (`feat(scope):`, `test(scope):`, `fix(scope):`, etc.)
- **Linter**: Ruff (rules: E, W, F, I, N, UP, B, SIM, C4), line length 88, target Python 3.12
- **Testing**: TDD approach. Domain tests use `pytest` with mocks (no DB). Integration tests use `pytest-django` with PostgreSQL.
- **Import order**: stdlib → third-party (django, rest_framework) → first-party (domain, infrastructure)

## Testing Strategy

- Domain tests (`tests/domain/`) — Test business logic with mocked repositories. Fast, no database.
- Integration tests (`tests/infrastructure/`) — Test API endpoints with real PostgreSQL. Use DRF `APIClient`.
- Domain tests MUST NOT import Django. This verifies the hexagonal separation.

## Project Documentation

Detailed specs and design docs are in `zenlog_doc/`:
- `CAHIER_DES_CHARGES.md` — Requirements, user stories (US-1 to US-9), non-functional requirements
- `JUSTIFICATION_PROJET.md` — Technical decision rationale
- `PLAN_DE_TESTS.md` — Full test plan with test IDs (T-D-01 to T-D-21, T-I-01 to T-I-21, T-S-01 to T-S-10)
- `DIAGRAMME_CLASSES.mermaid` / `MCD.mermaid` — Class diagram and ER diagram
