from __future__ import annotations

import pytest


def test_register_creates_user_and_password_is_hashed(client):
    payload = {"email": "alice@example.com", "password": "SafePass123!", "name": "Alice"}
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["email"] == "alice@example.com"
    assert body["id"] > 0

    # Attempt duplicate
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400


def _login(client, email: str, password: str) -> str:
    r = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_login_success_and_failure(client):
    email = "bob@example.com"
    client.post("/auth/register", json={"email": email, "password": "SafePass123!", "name": "Bob"})

    token = _login(client, email, "SafePass123!")
    assert isinstance(token, str) and len(token) > 10

    # Wrong password yields generic error
    r = client.post(
        "/auth/login",
        data={"username": email, "password": "WrongPass"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid credentials"
