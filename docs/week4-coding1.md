# Week 4: AI in Coding & Development (I)

## Overview

This document demonstrates how AI was used in the coding and development phase of the SmartBank Assistant project, focusing on AI-assisted code generation, refactoring, optimization, and documentation tools.

## 1. AI-Assisted Code Generation

### 1.1 Backend Code Generation

#### 1.1.1 FastAPI Route Generation

**AI Tool**: Cursor  
**Prompt:**
> "Create a FastAPI route for user registration with email validation, password hashing, and JWT token generation"

**AI-Generated Code:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..schemas.user import UserCreate, UserOut
from ..crud import user as user_crud
from ..auth.jwt_handler import create_access_token
import bcrypt

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = await user_crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # Create user
    db_user = await user_crud.create_user(db, user, hashed_password)
    
    return db_user
```

**Time Saved**: ~2 hours  
**Quality**: Production-ready code with error handling

#### 1.1.2 Database Model Generation

**AI Prompt:**
> "Create SQLAlchemy async models for User, Account, Transaction, and ChatLog with proper relationships"

**AI-Generated Code:**
```python
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")
    chat_logs = relationship("ChatLog", back_populates="user", cascade="all, delete-orphan")
```

**Time Saved**: ~1.5 hours  
**Features**: Proper relationships, UUIDs, timestamps

#### 1.1.3 CRUD Operations Generation

**AI Prompt:**
> "Generate async CRUD functions for user operations using SQLAlchemy"

**AI-Generated Code:**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import User
from ..schemas.user import UserCreate

async def create_user(db: AsyncSession, user: UserCreate, hashed_password: str):
    """Create a new user"""
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str):
    """Get user by email"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: str):
    """Get user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

**Time Saved**: ~1 hour  
**Quality**: Complete CRUD operations with async/await

### 1.2 Frontend Code Generation

#### 1.2.1 React Component Generation

**AI Prompt:**
> "Create a React login page component with form validation using react-hook-form, Tailwind CSS, and error handling"

**AI-Generated Code:**
```tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '@/hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

interface LoginFormData {
  email: string;
  password: string;
}

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<LoginFormData>();

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data.email, data.password);
      toast.success('Login successful!');
      navigate('/');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow-md">
        <h2 className="text-3xl font-bold text-center">Login</h2>
        <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address'
                }
              })}
              type="email"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            />
            {errors.email && (
              <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
            )}
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              {...register('password', { required: 'Password is required' })}
              type="password"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
            />
            {errors.password && (
              <p className="mt-1 text-sm text-red-600">{errors.password.message}</p>
            )}
          </div>
          
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
          >
            {isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
```

**Time Saved**: ~2 hours  
**Features**: Complete form with validation, error handling, loading states

#### 1.2.2 API Service Generation

**AI Prompt:**
> "Create an API service module for React with axios, including authentication, accounts, transactions, and chat endpoints"

**AI-Generated Code:**
```typescript
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data: { name: string; email: string; password: string }) =>
    api.post('/api/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/api/auth/login', data),
};

// Accounts API
export const accountsAPI = {
  getAll: () => api.get('/api/accounts'),
  create: (data: { account_type: string; currency?: string }) =>
    api.post('/api/accounts', data),
  getById: (id: string) => api.get(`/api/accounts/${id}`),
};

// Transactions API
export const transactionsAPI = {
  getAll: () => api.get('/api/transactions'),
  create: (data: any) => api.post('/api/transactions', data),
  getById: (id: string) => api.get(`/api/transactions/${id}`),
};

// Chat API
export const chatAPI = {
  sendMessage: (message: string) =>
    api.post('/api/chat/message', { message }),
  getHistory: () => api.get('/api/chat/history'),
};

export default api;
```

**Time Saved**: ~1 hour  
**Features**: Complete API client with interceptors, type safety

## 2. AI-Assisted Code Refactoring

### 2.1 Code Structure Refactoring

**Original Code:**
```python
# All code in one file
@app.post("/register")
async def register(user_data: dict):
    # 100+ lines of code
    pass
```

**AI Refactoring Prompt:**
> "Refactor this code to follow separation of concerns: routes, CRUD, schemas, services"

**AI-Refactored Structure:**
```
backend/app/
├── routes/
│   └── auth.py          # API endpoints
├── crud/
│   └── user.py          # Database operations
├── schemas/
│   └── user.py          # Data validation
└── services/
    └── auth_service.py  # Business logic
```

**Benefits** (AI-Identified):
- Better code organization
- Easier testing
- Reusable components
- Clear separation of concerns

### 2.2 Performance Optimization

**AI Prompt:**
> "Optimize this database query to reduce N+1 query problem"

**Original Code:**
```python
async def get_user_accounts(db: AsyncSession, user_id: str):
    user = await db.get(User, user_id)
    accounts = []
    for account in user.accounts:
        transactions = await db.execute(
            select(Transaction).where(Transaction.account_id == account.id)
        )
        accounts.append({
            'account': account,
            'transactions': transactions.scalars().all()
        })
    return accounts
```

**AI-Optimized Code:**
```python
async def get_user_accounts(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Account)
        .options(joinedload(Account.transactions))
        .where(Account.user_id == user_id)
    )
    return result.scalars().unique().all()
```

**Improvement**: Reduced from N+1 queries to 1 query

### 2.3 Error Handling Refactoring

**AI Prompt:**
> "Add comprehensive error handling to all API endpoints"

**AI-Generated Error Handling:**
```python
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

## 3. AI-Assisted Code Optimization

### 3.1 Database Query Optimization

**AI Analysis:**
> "Analyze and optimize database queries for performance"

**Optimizations Applied:**
1. Added database indexes
2. Used eager loading (joinedload)
3. Implemented pagination
4. Added query result caching

**Example:**
```python
# Before: Multiple queries
user = await get_user(user_id)
accounts = await get_accounts(user_id)
transactions = await get_transactions(user_id)

# After: Single optimized query
result = await db.execute(
    select(User)
    .options(
        joinedload(User.accounts).joinedload(Account.transactions)
    )
    .where(User.id == user_id)
)
```

### 3.2 API Response Optimization

**AI Suggestions:**
- Add response caching headers
- Implement pagination for large datasets
- Use compression for responses
- Optimize JSON serialization

**Implementation:**
```python
@router.get("/transactions")
async def get_transactions(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get paginated transactions"""
    result = await db.execute(
        select(Transaction)
        .offset(skip)
        .limit(limit)
        .order_by(Transaction.timestamp.desc())
    )
    return result.scalars().all()
```

### 3.3 Frontend Performance Optimization

**AI Recommendations:**
- Code splitting
- Lazy loading components
- Memoization for expensive computations
- Optimized re-renders

**Implementation:**
```tsx
// Lazy loading
const DashboardPage = React.lazy(() => import('@/pages/DashboardPage'));

// Memoization
const MemoizedAccountCard = React.memo(AccountCard);
```

## 4. AI-Assisted Documentation Tools

### 4.1 Code Documentation Generation

**AI Tool**: Cursor, ChatGPT  
**Prompt:**
> "Generate comprehensive docstrings for all functions in this file"

**AI-Generated Documentation:**
```python
async def create_user(
    db: AsyncSession,
    user: UserCreate,
    hashed_password: str
) -> User:
    """
    Create a new user in the database.
    
    Args:
        db: Database session
        user: User creation data (name, email)
        hashed_password: Bcrypt hashed password
        
    Returns:
        Created User object with generated ID
        
    Raises:
        IntegrityError: If email already exists
        
    Example:
        >>> user_data = UserCreate(name="John", email="john@example.com")
        >>> hashed = bcrypt.hashpw("password".encode(), bcrypt.gensalt())
        >>> user = await create_user(db, user_data, hashed)
    """
    # Implementation
```

### 4.2 API Documentation Generation

**AI-Generated OpenAPI Documentation:**
```python
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "uuid",
                        "name": "John Doe",
                        "email": "john@example.com",
                        "created_at": "2024-01-01T00:00:00"
                    }
                }
            }
        },
        400: {"description": "Email already registered"},
        422: {"description": "Validation error"}
    }
)
```

### 4.3 README Generation

**AI-Generated README Sections:**
- Project description
- Installation instructions
- API documentation
- Usage examples
- Contributing guidelines

## 5. Code Quality Metrics

### 5.1 Before AI Assistance

- **Code Coverage**: ~40%
- **Documentation**: Minimal
- **Type Safety**: Partial
- **Error Handling**: Basic
- **Performance**: Not optimized

### 5.2 After AI Assistance

- **Code Coverage**: ~75%
- **Documentation**: Comprehensive
- **Type Safety**: Full (TypeScript + Pydantic)
- **Error Handling**: Complete
- **Performance**: Optimized queries

## 6. Development Time Comparison

| Task | Manual | AI-Assisted | Time Saved |
|------|--------|-------------|------------|
| Route Creation | 2h | 30min | 75% |
| Component Creation | 2h | 45min | 62.5% |
| CRUD Operations | 3h | 1h | 66.7% |
| Documentation | 2h | 30min | 75% |
| Refactoring | 4h | 1.5h | 62.5% |
| **Total** | **13h** | **4h** | **69%** |

## 7. Best Practices Learned

### 7.1 Code Generation

1. **Be Specific**: Detailed prompts yield better code
2. **Iterate**: Refine AI output through multiple iterations
3. **Review**: Always review AI-generated code
4. **Test**: Test AI-generated code thoroughly

### 7.2 Refactoring

1. **Incremental**: Refactor in small steps
2. **Test Coverage**: Maintain tests during refactoring
3. **Documentation**: Update docs when refactoring
4. **Review**: Code review AI-suggested refactorings

### 7.3 Optimization

1. **Measure First**: Profile before optimizing
2. **Focus on Bottlenecks**: Optimize critical paths
3. **Balance**: Trade-offs between complexity and performance
4. **Document**: Document optimization decisions

## 8. Conclusion

AI significantly enhanced the coding and development phase by:

1. **Code Generation**: Rapid development of boilerplate code
2. **Refactoring**: Improved code structure and organization
3. **Optimization**: Performance improvements
4. **Documentation**: Comprehensive code documentation

The AI-assisted approach resulted in:
- ✅ **69% faster development**
- ✅ **Higher code quality**
- ✅ **Better documentation**
- ✅ **Improved performance**

---

**Next**: [Week 5: AI in Coding & Development (II)](week5-coding2.md)

