# SmartBank Assistant

A minimal, secure-ish banking web API built with FastAPI and SQLAlchemy. Includes JWT auth, account dashboard, simulated transfers, a simple chatbot endpoint, and admin seed/logs. Designed for teaching/demo purposes.

## Quickstart

1. Python 3.11+
2. Install deps:

```bash
pip install -r requirements.txt
```

3. Run the API:

```bash
uvicorn app.main:app --reload
```

The API will default to SQLite at `./smartbank.db`. To use MySQL, set `DB_URL` env var, e.g.:

```bash
export DB_URL="mysql+pymysql://user:password@localhost:3306/smartbank"
```

Open docs at `http://localhost:8000/docs`.

## Testing

```bash
pytest -q
```

## Environment

- `DB_URL`: Database URL (defaults to SQLite file)
- `SECRET_KEY`: JWT secret (dev default is used if unset)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry (default 60)
- `ADMIN_EMAIL`: Email that is treated as admin for `/admin/*` endpoints

## Security Notes
- Passwords are hashed with bcrypt via passlib.
- SQLAlchemy ORM uses parameterized queries by default.
- Do not use the default `SECRET_KEY` in production.
