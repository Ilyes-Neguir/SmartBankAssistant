from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    DECIMAL,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String(255), unique=True, nullable=False, index=True)
    password_hash: str = Column(String(255), nullable=False)
    name: Optional[str] = Column(String(255))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    accounts: List["Account"] = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    chats: List["ChatSession"] = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type: str = Column(String(50), default="checking")
    balance = Column(DECIMAL(12, 2), default=0)

    user: User = relationship("User", back_populates="accounts")
    transactions_from: List["Transaction"] = relationship(
        "Transaction",
        foreign_keys="Transaction.account_from_id",
        back_populates="account_from",
        cascade="all, delete-orphan",
    )
    transactions_to: List["Transaction"] = relationship(
        "Transaction",
        foreign_keys="Transaction.account_to_id",
        back_populates="account_to",
        cascade="all, delete-orphan",
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: int = Column(Integer, primary_key=True, index=True)
    account_from_id: Optional[int] = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    account_to_id: Optional[int] = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(DECIMAL(12, 2), nullable=False)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)
    simulated: bool = Column(Boolean, default=True)

    account_from: Optional[Account] = relationship("Account", foreign_keys=[account_from_id], back_populates="transactions_from")
    account_to: Optional[Account] = relationship("Account", foreign_keys=[account_to_id], back_populates="transactions_to")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    user_query: str = Column(Text)
    bot_response: str = Column(Text)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow)

    user: User = relationship("User", back_populates="chats")
