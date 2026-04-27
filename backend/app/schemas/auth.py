"""
Pydantic schemas for authentication endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Agent login request."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")


class LoginResponse(BaseModel):
    """Agent login response with JWT token."""
    access_token: str
    token_type: str = "bearer"
    agent_id: int
    email: str
    full_name: str


class SignupRequest(BaseModel):
    """Agent signup request."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=15, description="Phone number")
    location_area: str = Field(..., min_length=2, max_length=100)


class SignupResponse(BaseModel):
    """Agent signup response."""
    agent_id: int
    email: str
    full_name: str
    message: str = "Agent created successfully. Please log in."


class TokenData(BaseModel):
    """JWT token payload data."""
    sub: str  # Agent ID as string
    exp: int  # Expiry timestamp
