from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"

    # Use string UUIDs for cross-database compatibility (SQLite doesn't support native UUID type)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")
    chat_logs = relationship("ChatLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    account_type = Column(String, nullable=False)  # checking, savings, credit
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    account_number = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", foreign_keys="[Transaction.account_id]", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Account(id={self.id}, type={self.account_type}, balance={self.balance})>"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    account_id = Column(String(36), ForeignKey("accounts.id"))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # deposit, withdrawal, transfer
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(Text)
    category = Column(String)  # food, transportation, etc.
    from_account_id = Column(String(36), ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(String(36), ForeignKey("accounts.id"), nullable=True)

    account = relationship("Account", back_populates="transactions", foreign_keys=[account_id])
    from_account = relationship("Account", foreign_keys=[from_account_id])
    to_account = relationship("Account", foreign_keys=[to_account_id])

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, type={self.type})>"

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    message = Column(Text, nullable=False)
    bot_response = Column(Text)
    intent_detected = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    is_user = Column(String, default="true")  # true for user, false for bot

    user = relationship("User", back_populates="chat_logs")

    def __repr__(self):
        return f"<ChatLog(id={self.id}, user_id={self.user_id}, intent={self.intent_detected})>"
