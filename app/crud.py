from __future__ import annotations

from decimal import Decimal
from typing import List, Optional, Tuple

from sqlalchemy import desc, or_, select
from sqlalchemy.orm import Session

from . import auth
from .models import Account, ChatSession, Transaction, User


# Users

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()


def create_user(db: Session, email: str, password: str, name: Optional[str]) -> User:
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("Email already registered")
    password_hash = auth.hash_password(password)
    user = User(email=email, password_hash=password_hash, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    # Create default accounts
    checking = Account(user_id=user.id, type="checking", balance=Decimal("1000.00"))
    savings = Account(user_id=user.id, type="savings", balance=Decimal("5000.00"))
    db.add_all([checking, savings])
    db.commit()
    return user


# Accounts and Transactions

def get_user_accounts(db: Session, user_id: int) -> List[Account]:
    return db.execute(select(Account).where(Account.user_id == user_id)).scalars().all()


def get_recent_transactions(db: Session, user_id: int, limit: int = 20) -> List[Transaction]:
    # Any transaction where either from or to account belongs to user
    account_ids = [a.id for a in get_user_accounts(db, user_id)]
    if not account_ids:
        return []
    stmt = (
        select(Transaction)
        .where(or_(Transaction.account_from_id.in_(account_ids), Transaction.account_to_id.in_(account_ids)))
        .order_by(desc(Transaction.timestamp))
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


def get_account_for_user(db: Session, user_id: int, account_id: int) -> Optional[Account]:
    return db.execute(select(Account).where(Account.user_id == user_id, Account.id == account_id)).scalar_one_or_none()


def apply_transfer(
    db: Session, *, user_id: int, source_account_id: int, destination_account_id: int, amount: Decimal
) -> Transaction:
    source = get_account_for_user(db, user_id, source_account_id)
    dest = get_account_for_user(db, user_id, destination_account_id)
    if source is None or dest is None or source.id == dest.id:
        raise ValueError("Invalid accounts")
    if Decimal(source.balance) < amount:
        raise ValueError("Insufficient funds")

    # Update balances
    source.balance = Decimal(source.balance) - amount
    dest.balance = Decimal(dest.balance) + amount

    tx = Transaction(account_from_id=source.id, account_to_id=dest.id, amount=amount, simulated=True)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


# Chat

def record_chat(db: Session, user_id: int, user_query: str, bot_response: str) -> ChatSession:
    chat = ChatSession(user_id=user_id, user_query=user_query, bot_response=bot_response)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat
