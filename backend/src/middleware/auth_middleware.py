"""
Authentication middleware for the RAG backend system
"""
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from src.config import settings


class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # Get secret key from settings or use default
        self.secret_key = settings.secret_key or "default-secret-key-change-in-production"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a plain password"""
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create an access token with optional expiration"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_access_token(self, token: str) -> Optional[dict]:
        """Verify and decode an access token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return payload
        except jwt.PyJWTError:
            return None

    async def authenticate_request(self, request: Request) -> Optional[dict]:
        """Authenticate an incoming request"""
        # Extract authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header[7:]  # Remove "Bearer " prefix
        payload = self.verify_access_token(token)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload


# Create a global instance of the auth middleware
auth_middleware = AuthMiddleware()


def get_current_user(request: Request) -> Optional[dict]:
    """
    Dependency to get the current authenticated user
    """
    # For now, we'll skip authentication in development mode
    # In production, this would authenticate the user
    if settings.debug_mode:
        # In debug mode, return a mock user
        return {"sub": "debug-user", "role": "user", "exp": datetime.utcnow() + timedelta(hours=1)}

    # In production mode, authenticate the request
    return auth_middleware.authenticate_request(request)