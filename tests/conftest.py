from __future__ import annotations

import os
import pytest
from fastapi.testclient import TestClient

# Ensure test DB is sqlite
os.environ.setdefault("DB_URL", "sqlite:///./test.db")

from app.main import app  # noqa: E402
from app.database import engine  # noqa: E402
from app.models import Base  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)
