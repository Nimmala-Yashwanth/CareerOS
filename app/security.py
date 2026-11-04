import os
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

password_hash = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)
SECRET = os.getenv('SECRET_KEY', 'local-development-only-change-before-deploy')

def make_token(user_id: int) -> str:
    return jwt.encode({'sub': str(user_id), 'exp': datetime.now(timezone.utc) + timedelta(hours=12)}, SECRET, algorithm='HS256')

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None:
        raise HTTPException(401, 'Authentication required')
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=['HS256'])
        user_id = int(payload['sub'])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise HTTPException(401, 'Invalid or expired token')
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(401, 'User no longer exists')
    return user
