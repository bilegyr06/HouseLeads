from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PaystackInitializeRequest(BaseModel):
    """Schema for initializing Paystack payment."""
    agent_id: int = Field(..., gt=0)
    lead_id: int = Field(..., gt=0)
    amount: float = Field(..., gt=0, description="Amount in Naira")
    email: str = Field(..., description="Agent's email for Paystack")


class PaystackInitializeResponse(BaseModel):
    """Response from Paystack payment initialization."""
    status: bool
    message: str
    data: dict = Field(..., description="Paystack payment data with authorization_url")


class PaystackWebhookPayload(BaseModel):
    """Schema for Paystack webhook payload."""
    event: str
    data: dict


class LeadPurchaseResponse(BaseModel):
    """Response schema for lead purchase record."""
    id: int
    agent_id: int
    lead_id: int
    amount: float
    payment_reference: Optional[str] = None
    status: str = Field(..., example="pending/completed/failed")
    created_at: datetime
    
    class Config:
        from_attributes = True