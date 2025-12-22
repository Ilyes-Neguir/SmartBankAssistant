from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..db import get_db
from ..schemas.account import AccountCreate, AccountOut, AccountUpdate
from ..crud import account as account_crud
from ..auth.dependencies import get_current_user
from models.models import User

router = APIRouter()

@router.get("/", response_model=List[AccountOut])
async def get_accounts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all accounts for the current user"""
    accounts = await account_crud.get_user_accounts(db, str(current_user.id), skip, limit)
    return accounts

@router.post("/", response_model=AccountOut)
async def create_account(
    account: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new account for the current user"""
    db_account = await account_crud.create_account(db, account, str(current_user.id))
    return db_account

@router.get("/{account_id}", response_model=AccountOut)
async def get_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific account"""
    account = await account_crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Check if account belongs to user
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    return account

@router.put("/{account_id}", response_model=AccountOut)
async def update_account(
    account_id: str,
    account_update: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an account"""
    account = await account_crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Check if account belongs to user
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    updated_account = await account_crud.update_account(db, account_id, account_update)
    return updated_account

@router.delete("/{account_id}")
async def delete_account(
    account_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an account"""
    account = await account_crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Check if account belongs to user
    if str(account.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    await account_crud.delete_account(db, account_id)
    return {"message": "Account deleted successfully"}
