from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import Transaction, Account
from ..schemas.transaction import TransactionCreate, TransactionUpdate
from typing import List

async def create_transaction(db: AsyncSession, transaction: TransactionCreate) -> Transaction:
    """Create a new transaction"""
    db_transaction = Transaction(
        amount=transaction.amount,
        type=transaction.type,
        description=transaction.description,
        category=transaction.category,
        account_id=transaction.account_id,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def get_transaction(db: AsyncSession, transaction_id: str) -> Transaction:
    """Get transaction by ID"""
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalars().first()

async def get_account_transactions(db: AsyncSession, account_id: str, skip: int = 0, limit: int = 100) -> List[Transaction]:
    """Get all transactions for an account"""
    result = await db.execute(
        select(Transaction)
        .filter(Transaction.account_id == account_id)
        .offset(skip)
        .limit(limit)
        .order_by(Transaction.timestamp.desc())
    )
    return result.scalars().all()

async def get_user_transactions(db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Transaction]:
    """Get all transactions for a user (across all accounts)"""
    result = await db.execute(
        select(Transaction)
        .join(Account)
        .filter(Account.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .order_by(Transaction.timestamp.desc())
    )
    return result.scalars().all()

async def update_transaction(db: AsyncSession, transaction_id: str, transaction_update: TransactionUpdate) -> Transaction:
    """Update transaction"""
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    db_transaction = result.scalars().first()
    
    if not db_transaction:
        return None
    
    update_data = transaction_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

async def delete_transaction(db: AsyncSession, transaction_id: str) -> Transaction:
    """Delete transaction"""
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    db_transaction = result.scalars().first()
    
    if not db_transaction:
        return None
    
    await db.delete(db_transaction)
    await db.commit()
    return db_transaction
