from __future__ import annotations

from decimal import Decimal


def _login(client, email: str, password: str) -> str:
    r = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def test_dashboard_returns_balances_and_recent_transactions(client):
    email = "carol@example.com"
    client.post("/auth/register", json={"email": email, "password": "SafePass123!", "name": "Carol"})
    token = _login(client, email, "SafePass123!")

    r = client.get("/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["accounts"]) >= 2
    assert isinstance(body["recent_transactions"], list)


def test_simulated_transfer_updates_balances_and_flags_simulated(client):
    email = "dave@example.com"
    client.post("/auth/register", json={"email": email, "password": "SafePass123!", "name": "Dave"})
    token = _login(client, email, "SafePass123!")

    dash = client.get("/dashboard", headers={"Authorization": f"Bearer {token}"}).json()
    a1, a2 = dash["accounts"][0], dash["accounts"][1]

    # Initiate
    init = client.post(
        "/transfers",
        json={"source_account_id": a1["id"], "destination_account_id": a2["id"], "amount": "25.50"},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    assert init["status"] == "pending"

    # Confirm
    conf = client.post(
        f"/transfers/{init['transfer_id']}/confirm",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert conf.status_code == 200, conf.text
    conf_body = conf.json()
    assert conf_body["simulated"] is True

    dash2 = client.get("/dashboard", headers={"Authorization": f"Bearer {token}"}).json()
    # Verify balances changed as expected
    # Since initial balances: 1000 and 5000
    expected_a1 = Decimal("1000.00") - Decimal("25.50")
    expected_a2 = Decimal("5000.00") + Decimal("25.50")

    # Find updated accounts by id
    updated_a1 = next(x for x in dash2["accounts"] if x["id"] == a1["id"])
    updated_a2 = next(x for x in dash2["accounts"] if x["id"] == a2["id"])

    assert Decimal(str(updated_a1["balance"])) == expected_a1
    assert Decimal(str(updated_a2["balance"])) == expected_a2
