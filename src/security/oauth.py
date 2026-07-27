from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel
from src.config import settings
from src.security.rbac import UserAuthContext

security_bearer = HTTPBearer(auto_error=False)


class TokenPayload(BaseModel):
    sub: str
    role: str = "physician"
    tenant_id: str = "default"
    departments: list[str] = ["cardiology"]
    exp: int


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def get_current_user_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer),
) -> UserAuthContext:
    """
    OAuth2 / OIDC Token Verification & Claims Extraction Dependency.
    Falls back gracefully to default context when unauthenticated for development/testing compatibility.
    """
    if not credentials:
        return UserAuthContext(
            user_id="anonymous_dev",
            role="physician",
            assigned_departments=["cardiology", "endocrinology"],
        )

    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return UserAuthContext(
            user_id=payload.get("sub", "unknown"),
            role=payload.get("role", "physician"),
            assigned_departments=payload.get("departments", ["cardiology"]),
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OAuth2 access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
