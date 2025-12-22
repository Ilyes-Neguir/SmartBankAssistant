from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..db import get_db
from ..schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from ..crud import transaction as transaction_crud, account as account_crud
from ..auth.dependencies import get_current_user
from models.models import User

router = APIRouter()

@router.get("/", response_model=List[TransactionOut])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all transactions for the current user"""
    transactions = await transaction_crud.get_user_transactions(db, str(current_user.id), skip, limit)
    return transactions

@router.post("/", response_model=TransactionOut)
async def create_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new transaction"""
    # Verify account belongs to user
    account = await account_crud.get_account(db, str(transaction.account_id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    db_transaction = await transaction_crud.create_transaction(db, transaction)
    return db_transaction

@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific transaction"""
    transaction = await transaction_crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Verify account belongs to user
    account = await account_crud.get_account(db, str(transaction.account_id))
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    
    return transaction

@router.put("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(
    transaction_id: str,
    transaction_update: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a transaction"""
    transaction = await transaction_crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Verify account belongs to user
    account = await account_crud.get_account(db, str(transaction.account_id))
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    
    updated_transaction = await transaction_crud.update_transaction(db, transaction_id, transaction_update)
    return updated_transaction

@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a transaction"""
    transaction = await transaction_crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Verify account belongs to user
    account = await account_crud.get_account(db, str(transaction.account_id))
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this transaction")
    
    await transaction_crud.delete_transaction(db, transaction_id)
    return {"message": "Transaction deleted successfully"}
