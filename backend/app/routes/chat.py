from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..db import get_db
from ..schemas.chatlog import ChatLogCreate, ChatLogOut, ChatMessage
from ..crud import chatlog as chatlog_crud, account as account_crud, transaction as transaction_crud
from ..auth.dependencies import get_current_user
from models.models import User
from ..services.gemini_service import GeminiService

router = APIRouter()
gemini_service = GeminiService()

@router.post("/message", response_model=ChatLogOut)
async def send_message(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a message to the chatbot and get response"""
    
    # Create chat log entry for user message
    chat_log = ChatLogCreate(message=message.message, is_user=True)
    db_chat_log = await chatlog_crud.create_chat_log(db, chat_log, str(current_user.id))
    
    # Get user context (accounts, recent transactions)
    user_accounts = await account_crud.get_user_accounts(db, str(current_user.id))
    user_transactions = await transaction_crud.get_user_transactions(db, str(current_user.id), limit=10)
    
    # Prepare context for AI
    user_context = {
        "accounts": [
            {
                "id": str(acc.id),
                "type": acc.account_type,
                "balance": acc.balance,
                "currency": acc.currency
            } for acc in user_accounts
        ],
        "transactions": [
            {
                "id": str(trans.id),
                "amount": trans.amount,
                "type": trans.type,
                "description": trans.description,
                "timestamp": trans.timestamp.isoformat()
            } for trans in user_transactions
        ],
        "total_balance": sum(acc.balance for acc in user_accounts)
    }
    
    # Process message with Gemini AI
    ai_response = await gemini_service.process_banking_query(message.message, user_context)
    
    # Update chat log with bot response
    updated_chat_log = await chatlog_crud.update_chat_log_response(
        db, str(db_chat_log.id), ai_response["response"], ai_response["intent"]
    )
    
    return updated_chat_log

@router.get("/history", response_model=List[ChatLogOut])
async def get_chat_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get chat history for the current user"""
    chat_history = await chatlog_crud.get_chat_history(db, str(current_user.id), skip, limit)
    return chat_history
