from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import ChatLog
from ..schemas.chatlog import ChatLogCreate
from typing import List

async def create_chat_log(db: AsyncSession, chat_log: ChatLogCreate, user_id: str) -> ChatLog:
    """Create a new chat log entry"""
    db_chat_log = ChatLog(
        message=chat_log.message,
        is_user=chat_log.is_user,
        user_id=user_id
    )
    db.add(db_chat_log)
    await db.commit()
    await db.refresh(db_chat_log)
    return db_chat_log

async def get_chat_history(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[ChatLog]:
    """Get chat history for a user"""
    result = await db.execute(
        select(ChatLog)
        .filter(ChatLog.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(ChatLog.timestamp.desc())
    )
    return result.scalars().all()

async def update_chat_log_response(db: AsyncSession, chat_log_id: str, bot_response: str, intent: str = None) -> ChatLog:
    """Update chat log with bot response"""
    result = await db.execute(select(ChatLog).filter(ChatLog.id == chat_log_id))
    db_chat_log = result.scalars().first()
    
    if not db_chat_log:
        return None
    
    db_chat_log.bot_response = bot_response
    if intent:
        db_chat_log.intent_detected = intent
    
    await db.commit()
    await db.refresh(db_chat_log)
    return db_chat_log
