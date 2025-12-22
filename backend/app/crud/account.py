from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Account
from ..schemas.account import AccountCreate, AccountUpdate
from typing import List
import uuid

async def create_account(db: AsyncSession, account: AccountCreate, user_id: str) -> Account:
    """Create a new account for user"""
    db_account = Account(
        account_type=account.account_type,
        balance=account.balance,
        currency=account.currency,
        user_id=user_id,
        account_number=str(uuid.uuid4())[:8]  # Simple account number generation
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def get_account(db: AsyncSession, account_id: str) -> Account:
    """Get account by ID"""
    result = await db.execute(select(Account).filter(Account.id == account_id))
    return result.scalars().first()

async def get_user_accounts(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Account]:
    """Get all accounts for a user"""
    result = await db.execute(
        select(Account)
        .filter(Account.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def update_account(db: AsyncSession, account_id: str, account_update: AccountUpdate) -> Account:
    """Update account"""
    result = await db.execute(select(Account).filter(Account.id == account_id))
    db_account = result.scalars().first()
    
    if not db_account:
        return None
    
    update_data = account_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_account, field, value)
    
    await db.commit()
    await db.refresh(db_account)
    return db_account

async def delete_account(db: AsyncSession, account_id: str) -> Account:
    """Delete account"""
    result = await db.execute(select(Account).filter(Account.id == account_id))
    db_account = result.scalars().first()
    
    if not db_account:
        return None
    
    await db.delete(db_account)
    await db.commit()
    return db_account
