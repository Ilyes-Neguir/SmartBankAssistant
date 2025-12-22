from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class AccountBase(BaseModel):
    account_type: str
    balance: float = 0.0
    currency: str = "USD"

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    account_type: Optional[str] = None
    balance: Optional[float] = None
    currency: Optional[str] = None

class AccountOut(AccountBase):
    id: UUID
    user_id: UUID
    account_number: str
    created_at: datetime
    
    class Config:
        from_attributes = True
