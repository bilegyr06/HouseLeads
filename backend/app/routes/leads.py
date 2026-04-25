from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_session
from app.models.tenant_lead import TenantLead
from app.schemas.tenant_lead import TenantLeadCreate, TenantLeadResponse
from app.services.lead_scoring import calculate_lead_score
from app.services.matching import MatchingService
from app.utils.helpers import normalize_phone_number, standardize_location

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=TenantLeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_data: TenantLeadCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new tenant lead.
    
    Calculates lead score and finds matching agents automatically.
    """
    # Check for duplicate phone number
    existing = await session.execute(
        select(TenantLead).where(TenantLead.phone_number == lead_data.phone_number)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered as a lead"
        )
    
    # Normalize and standardize input
    normalized_phone = normalize_phone_number(lead_data.phone_number)
    standardized_location = standardize_location(lead_data.location_preference)
    
    # Calculate lead score
    lead_score = calculate_lead_score(lead_data)
    
    # Create lead record
    new_lead = TenantLead(
        full_name=lead_data.full_name,
        phone_number=normalized_phone,
        email=lead_data.email,
        location_preference=standardized_location,
        budget_min=lead_data.budget_min,
        budget_max=lead_data.budget_max,
        property_type=lead_data.property_type,
        move_in_date=lead_data.move_in_date,
        lead_score=lead_score,
        status="new"
    )
    
    session.add(new_lead)
    await session.flush()  # Flush to get the ID without committing
    
    # Find matching agents
    matches = await MatchingService.find_best_matches(session, new_lead, limit=5)
    
    # TODO: Send WhatsApp notifications to matched agents
    # for agent, score in matches:
    #     await WhatsAppService.send_lead_notification(...)
    
    await session.commit()
    return TenantLeadResponse.model_validate(new_lead)


@router.get("/", response_model=List[TenantLeadResponse])
async def list_leads(
    status_filter: str = None,
    location_filter: str = None,
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
):
    """
    List all tenant leads with optional filtering.
    
    Query parameters:
    - status_filter: Filter by status (new, contacted, interested, matched, closed)
    - location_filter: Filter by location preference
    - skip: Number of records to skip (pagination)
    - limit: Number of records to return (max 100)
    """
    limit = min(limit, 100)  # Cap limit at 100
    
    query = select(TenantLead)
    
    if status_filter:
        query = query.where(TenantLead.status == status_filter)
    
    if location_filter:
        standardized = standardize_location(location_filter)
        query = query.where(TenantLead.location_preference == standardized)
    
    # Order by creation date, newest first
    query = query.order_by(desc(TenantLead.created_at)).offset(skip).limit(limit)
    
    result = await session.execute(query)
    leads = result.scalars().all()
    
    return [TenantLeadResponse.model_validate(lead) for lead in leads]


@router.get("/{lead_id}", response_model=TenantLeadResponse)
async def get_lead(
    lead_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific tenant lead by ID.
    """
    lead = await session.get(TenantLead, lead_id)
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    return TenantLeadResponse.model_validate(lead)


@router.patch("/{lead_id}", response_model=TenantLeadResponse)
async def update_lead_status(
    lead_id: int,
    new_status: str = "interested",
    session: AsyncSession = Depends(get_session)
):
    """
    Update lead status (e.g., mark as contacted, matched, closed).
    
    Valid statuses: new, contacted, interested, matched, closed
    """
    valid_statuses = {"new", "contacted", "interested", "matched", "closed"}
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )
    
    lead = await session.get(TenantLead, lead_id)
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    lead.status = new_status
    await session.commit()
    
    return TenantLeadResponse.model_validate(lead)


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a tenant lead.
    """
    lead = await session.get(TenantLead, lead_id)
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    await session.delete(lead)
    await session.commit()