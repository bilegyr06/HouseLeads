from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class AgentCreate(BaseModel):
    """Schema for creating a new agent."""
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    location_area: str = Field(..., min_length=2, max_length=100, example="Lekki")
    agency_name: Optional[str] = Field(None, max_length=100)


class AgentUpdate(BaseModel):
    """Schema for updating agent information."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    location_area: Optional[str] = Field(None, min_length=2, max_length=100)
    agency_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class AgentResponse(BaseModel):
    """Response schema for agent data."""
    id: int
    full_name: str
    phone_number: str
    email: str
    location_area: str
    agency_name: Optional[str] = None
    rating: float
    total_leads_matched: int
    total_leads_converted: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True