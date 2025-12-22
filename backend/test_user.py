import asyncio
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.db import get_db

async def test_user_creation():
    try:
        async for db in get_db():
            user = UserCreate(name='Test', email='test@example.com', password='password123')
            created_user = await create_user(db, user)
            print(f"User created: {created_user.name}, {created_user.email}")
            break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_user_creation())
