"""
Security utilities for JWT token management and password hashing.
Handles authentication, authorization, and token verification.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request

from app.core.config import settings
from app.core.database import get_session
from app.models.agent import Agent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================================
# Password Hashing
# ============================================================================

def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# JWT Token Management
# ============================================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dict to encode in token (typically {"sub": agent_id})
        expires_delta: Optional expiry time. Defaults to 30 minutes from settings.
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload
        
    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        raise JWTError("Invalid or expired token")


# ============================================================================
# Token Extraction
# ============================================================================

def get_token_from_request(request: Request) -> str:
    """
    Extract JWT token from Authorization header.
    
    Args:
        request: FastAPI Request object
        
    Returns:
        JWT token string
        
    Raises:
        HTTPException: If no valid Authorization header
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parts[1]


# ============================================================================
# Dependency Injection
# ============================================================================

async def get_current_user(
    request: Request = Depends(),
    session: AsyncSession = Depends(get_session)
) -> Agent:
    """
    Dependency to verify JWT token and get current authenticated agent.
    
    Args:
        request: FastAPI Request object
        session: Database session
        
    Returns:
        Agent object for the authenticated user
        
    Raises:
        HTTPException: If token is invalid or agent not found
    """
    # Extract token from header
    token = get_token_from_request(request)
    
    # Verify token
    try:
        payload = verify_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    agent_id: str = payload.get("sub")
    if agent_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get agent from database
    try:
        agent_id = int(agent_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    agent = await session.get(Agent, agent_id)
    
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Agent not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not agent.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent account is inactive",
        )
    
    return agent


# ============================================================================
# Optional Dependencies (for protected routes)
# ============================================================================

async def get_current_active_user(
    current_user: Agent = Depends(get_current_user),
) -> Agent:
    """
    Verify that current user is active.
    Used as dependency in protected routes.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive agent"
        )
    return current_user