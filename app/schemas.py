from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AccountOut(BaseModel):
    id: int
    type: str
    balance: Decimal

    class Config:
        from_attributes = True


class TransactionOut(BaseModel):
    id: int
    account_from_id: Optional[int]
    account_to_id: Optional[int]
    amount: Decimal
    timestamp: datetime
    simulated: bool

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    accounts: List[AccountOut]
    recent_transactions: List[TransactionOut]


class TransferCreate(BaseModel):
    source_account_id: int
    destination_account_id: int
    amount: Decimal = Field(gt=0)


class TransferPendingResponse(BaseModel):
    transfer_id: str
    status: str = "pending"
    message: str = "SIMULATED - confirm to apply"


class TransferConfirmResponse(BaseModel):
    id: int
    simulated: bool
    amount: Decimal


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    reply: str
