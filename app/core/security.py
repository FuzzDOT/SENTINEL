from datetime import datetime, timedelta
from typing import Optional, List
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .settings import settings

security = HTTPBearer()


def create_access_token(subject: str, scopes: Optional[List[str]] = None, expires_minutes: Optional[int] = None):
    expires = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expires}
    if scopes:
        payload["scopes"] = scopes
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


def verify_token(token: str, required_scopes: Optional[List[str]] = None):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if required_scopes:
        token_scopes = payload.get("scopes", [])
        for s in required_scopes:
            if s not in token_scopes:
                raise HTTPException(status_code=403, detail="Missing required scope")
    return payload


def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    return verify_token(creds.credentials)
