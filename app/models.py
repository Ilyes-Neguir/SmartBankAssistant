from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, DECIMAL, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    accounts: Mapped[List["Account"]] = relationship(
        "Account", back_populates="user", cascade="all, delete-orphan"
    )
    chats: Mapped[List["ChatSession"]] = relationship(
        "ChatSession", back_populates="user", cascade="all, delete-orphan"
    )


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    type: Mapped[str] = mapped_column(String(50), default="checking")
    balance: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), default=Decimal("0"))

    user: Mapped[User] = relationship("User", back_populates="accounts")
    transactions_from: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.account_from_id",
        back_populates="account_from",
        cascade="all, delete-orphan",
    )
    transactions_to: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.account_to_id",
        back_populates="account_to",
        cascade="all, delete-orphan",
    )


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_from_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("accounts.id"), nullable=True
    )
    account_to_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("accounts.id"), nullable=True
    )
    amount: Mapped[Decimal] = mapped_column(DECIMAL(12, 2), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    simulated: Mapped[bool] = mapped_column(Boolean, default=True)

    account_from: Mapped[Optional["Account"]] = relationship(
        "Account", foreign_keys=[account_from_id], back_populates="transactions_from"
    )
    account_to: Mapped[Optional["Account"]] = relationship(
        "Account", foreign_keys=[account_to_id], back_populates="transactions_to"
    )


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user_query: Mapped[str] = mapped_column(Text)
    bot_response: Mapped[str] = mapped_column(Text)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship("User", back_populates="chats")
