from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class TransactionBase(BaseModel):
    amount: float
    type: str
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionCreate(TransactionBase):
    account_id: UUID
    from_account_id: Optional[UUID] = None
    to_account_id: Optional[UUID] = None

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class TransactionOut(TransactionBase):
    id: UUID
    account_id: UUID
    from_account_id: Optional[UUID] = None
    to_account_id: Optional[UUID] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True
