from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import json
import hmac
import hashlib

from app.core.database import get_session
from app.core.config import settings
from app.models.tenant_lead import TenantLead
from app.models.agent import Agent
from app.schemas.payment import (
    PaystackInitializeRequest,
    PaystackInitializeResponse,
    PaystackWebhookPayload,
    LeadPurchaseResponse
)

router = APIRouter(prefix="/payments", tags=["payments"])

# Placeholder for actual Paystack SDK
PAYSTACK_BASE_URL = "https://api.paystack.co"


@router.post("/initialize", response_model=PaystackInitializeResponse)
async def initialize_payment(
    payment_data: PaystackInitializeRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Initialize a Paystack payment transaction.
    
    This endpoint prepares a lead purchase payment and returns
    a Paystack authorization URL for the agent.
    """
    # Verify lead exists
    lead = await session.get(TenantLead, payment_data.lead_id)
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Verify agent exists
    agent = await session.get(Agent, payment_data.agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Validate amount
    if payment_data.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )
    
    # TODO: Call Paystack API to initialize payment
    # For now, return mock response
    
    return PaystackInitializeResponse(
        status=True,
        message="Authorization URL created",
        data={
            "authorization_url": f"https://checkout.paystack.com/mock_{payment_data.lead_id}_{payment_data.agent_id}",
            "access_code": f"mock_access_{payment_data.lead_id}",
            "reference": f"NAIJA_{payment_data.lead_id}_{payment_data.agent_id}"
        }
    )


@router.post("/verify/{reference}")
async def verify_payment(
    reference: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Verify a Paystack payment using transaction reference.
    """
    # TODO: Call Paystack API to verify payment
    # TODO: Update lead purchase record with payment status
    # TODO: Send WhatsApp confirmation to agent
    
    return {
        "status": True,
        "message": "Payment verified",
        "reference": reference
    }


@router.post("/webhook")
async def paystack_webhook(
    x_paystack_signature: str = Header(...),
    session: AsyncSession = Depends(get_session),
):
    """
    Paystack webhook endpoint for payment notifications.
    
    Paystack sends POST requests here with payment status updates.
    Verify signature and process payment accordingly.
    """
    # TODO: Implement webhook signature verification
    # TODO: Process different event types (charge.success, charge.failed)
    # TODO: Update lead purchase status
    # TODO: Trigger WhatsApp notifications
    
    return {"status": "ok"}


def verify_paystack_signature(payload: str, signature: str) -> bool:
    """
    Verify Paystack webhook signature.
    
    Args:
        payload: Raw request body
        signature: X-Paystack-Signature header value
        
    Returns:
        True if signature is valid, False otherwise
    """
    hash_object = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha512
    )
    computed_signature = hash_object.hexdigest()
    return computed_signature == signature