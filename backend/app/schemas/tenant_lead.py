from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date, datetime
from typing import Optional
import re

class TenantLeadCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone_number: str = Field(..., min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    location_preference: str = Field(..., min_length=2, max_length=100, example="Lekki")
    budget_min: Optional[int] = Field(None, ge=50000)
    budget_max: int = Field(..., ge=100000)
    property_type: str = Field(..., min_length=2, max_length=50, example="1 bedroom")
    move_in_date: date
    
    @field_validator('phone_number')
    @classmethod
    def validate_phone(cls, phone_number: str) -> str:
        """Validate Nigerian phone number format."""
        # Accept +234, 0234, or 0 prefix formats
        if not re.match(r'^(\+234|0234|0)[0-9]{9,10}$', phone_number.replace(' ', '').replace('-', '')):
            raise ValueError('Invalid Nigerian phone number format')
        return phone_number
    
    @field_validator('budget_max')
    @classmethod
    def validate_budget_max(cls, max: int, info) -> int:
        """Ensure budget_max >= budget_min if budget_min exists."""
        if 'budget_min' in info.data and info.data['budget_min'] and max < info.data['budget_min']:
            raise ValueError('budget_max must be >= budget_min')
        return max
    
    @field_validator('move_in_date')
    @classmethod
    def validate_move_in_date(cls, move_in_date: date) -> date:
        """Ensure move_in_date is in the future."""
        if move_in_date < date.today():
            raise ValueError('move_in_date must be in the future')
        return move_in_date

class TenantLeadResponse(BaseModel):
    """Response schema - returns complete lead data with system-generated fields."""
    id: int
    full_name: str
    phone_number: str
    email: Optional[str] = None
    location_preference: str
    budget_min: Optional[int] = None
    budget_max: int
    property_type: str
    move_in_date: date
    lead_score: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # ORM mode - allows mapping from SQLAlchemy models