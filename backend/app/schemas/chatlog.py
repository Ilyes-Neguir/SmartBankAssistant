from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ChatLogBase(BaseModel):
    message: str
    is_user: bool = True

class ChatLogCreate(ChatLogBase):
    pass

class ChatLogOut(ChatLogBase):
    id: UUID
    user_id: UUID
    bot_response: Optional[str] = None
    intent_detected: Optional[str] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str
    user_id: UUID
