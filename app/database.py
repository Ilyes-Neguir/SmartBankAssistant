from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def _get_database_url() -> str:
    # Prefer explicit env; default to local SQLite file for easy dev/tests
    return os.getenv("DB_URL", "sqlite:///./smartbank.db")


DATABASE_URL = _get_database_url()

# SQLite needs special connect args
if DATABASE_URL.startswith("sqlite"):  # pragma: no cover
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}, future=True
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
