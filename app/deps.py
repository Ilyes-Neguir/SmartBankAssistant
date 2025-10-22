from __future__ import annotations

import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .auth import decode_token
from .database import get_db
from .models import User
from sqlalchemy import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> User:
    subject = decode_token(token)
    if subject is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # subject is email
    user = db.execute(select(User).where(User.email == subject)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    admin_email: Optional[str] = os.getenv("ADMIN_EMAIL")
    if admin_email and user.email == admin_email:
        return user
    # If no ADMIN_EMAIL configured, allow any authenticated user in dev
    if not admin_email:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
