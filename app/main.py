from __future__ import annotations

import os
import uuid
from decimal import Decimal
from typing import Dict

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud
from .auth import create_access_token, verify_password
from .database import engine, get_db
from .models import Base, User
from .schemas import (
    ChatRequest,
    ChatResponse,
    DashboardResponse,
    LoginRequest,
    Token,
    TransferConfirmResponse,
    TransferCreate,
    TransferPendingResponse,
    UserCreate,
    UserOut,
    AccountOut,
    TransactionOut,
)
from .deps import get_current_user, require_admin

# Create all tables on startup for simplicity (alembic optional later)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartBank Assistant")

# CORS (open for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory pending transfer store
PENDING_TRANSFERS: Dict[str, TransferCreate] = {}


# Auth routes
@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, email=payload.email, password=payload.password, name=payload.name)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm expects username field; using email as username
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


# Accounts / Dashboard
@app.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    accounts = crud.get_user_accounts(db, current_user.id)
    transactions = crud.get_recent_transactions(db, current_user.id, limit=20)
    return {
        "accounts": [AccountOut.model_validate(a) for a in accounts],
        "recent_transactions": [TransactionOut.model_validate(t) for t in transactions],
    }


@app.get("/accounts/{account_id}/transactions", response_model=list[TransactionOut])
def account_transactions(account_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    account = crud.get_account_for_user(db, current_user.id, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    txs = [t for t in crud.get_recent_transactions(db, current_user.id, limit=100) if t.account_from_id == account.id or t.account_to_id == account.id]
    return txs


# Transfers (simulated)
@app.post("/transfers", response_model=TransferPendingResponse)
def initiate_transfer(payload: TransferCreate, current_user: User = Depends(get_current_user)):
    transfer_id = str(uuid.uuid4())
    PENDING_TRANSFERS[transfer_id] = payload
    return TransferPendingResponse(transfer_id=transfer_id)


@app.post("/transfers/{transfer_id}/confirm", response_model=TransferConfirmResponse)
def confirm_transfer(transfer_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if transfer_id not in PENDING_TRANSFERS:
        raise HTTPException(status_code=404, detail="Pending transfer not found")
    payload = PENDING_TRANSFERS.pop(transfer_id)
    try:
        tx = crud.apply_transfer(
            db,
            user_id=current_user.id,
            source_account_id=payload.source_account_id,
            destination_account_id=payload.destination_account_id,
            amount=Decimal(payload.amount),
        )
        return TransferConfirmResponse(id=tx.id, simulated=tx.simulated, amount=tx.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Chat (very simple rule-based)
@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = payload.query.lower()
    accounts = crud.get_user_accounts(db, current_user.id)

    reply = "Sorry, I didn't understand."
    if "balance" in query:
        # Prefer checking account if present
        checking = next((a for a in accounts if a.type.lower() == "checking"), None)
        if checking:
            reply = f"Your checking balance is {checking.balance} (live data)."
        else:
            total = sum([Decimal(a.balance) for a in accounts])
            reply = f"Your total balance across accounts is {total} (live data)."
    elif "transfer" in query:
        reply = "I can help you simulate a transfer. Please use the Transfers page to proceed."

    crud.record_chat(db, current_user.id, payload.query, reply)
    return ChatResponse(reply=reply)


# Admin (dev-only)
@app.post("/admin/seed")
def admin_seed(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    # Create a couple of demo users if not existing
    created = []
    for idx in range(1, 3):
        email = f"demo{idx}@example.com"
        if not crud.get_user_by_email(db, email):
            crud.create_user(db, email=email, password="DemoPass123!", name=f"Demo {idx}")
            created.append(email)
    return {"created": created}


@app.get("/admin/logs")
def admin_logs(_: User = Depends(require_admin)):
    # Minimal dev logs endpoint; in real system, stream from centralized logging
    logs_path = os.path.join("logs", "app.log")
    if not os.path.exists(logs_path):
        return {"logs": []}
    with open(logs_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()][-200:]
    # Mask any tokens
    masked = [line.replace("Bearer ", "Bearer ***").replace("token=", "token=***") for line in lines]
    return {"logs": masked}


@app.get("/")
def root():
    return {"status": "ok", "service": "smartbank-assistant"}
