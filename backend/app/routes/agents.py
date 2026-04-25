from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_session
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from app.utils.helpers import normalize_phone_number, standardize_location

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new real estate agent.
    """
    # Check for duplicate phone number
    existing_phone = await session.execute(
        select(Agent).where(Agent.phone_number == agent_data.phone_number)
    )
    if existing_phone.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered"
        )
    
    # Check for duplicate email
    existing_email = await session.execute(
        select(Agent).where(Agent.email == agent_data.email)
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Normalize and standardize input
    normalized_phone = normalize_phone_number(agent_data.phone_number)
    standardized_location = standardize_location(agent_data.location_area)
    
    # Create agent record
    new_agent = Agent(
        full_name=agent_data.full_name,
        phone_number=normalized_phone,
        email=agent_data.email,
        location_area=standardized_location,
        agency_name=agent_data.agency_name,
        is_active=True
    )
    
    session.add(new_agent)
    await session.commit()
    
    return AgentResponse.model_validate(new_agent)


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    location_filter: str = None,
    is_active_only: bool = True,
    skip: int = 0,
    limit: int = 20,
    session: AsyncSession = Depends(get_session)
):
    """
    List all agents with optional filtering.
    
    Query parameters:
    - location_filter: Filter by operating location
    - is_active_only: Only return active agents (default: true)
    - skip: Number of records to skip (pagination)
    - limit: Number of records to return (max 100)
    """
    limit = min(limit, 100)  # Cap limit at 100
    
    query = select(Agent)
    
    if is_active_only:
        query = query.where(Agent.is_active == True)
    
    if location_filter:
        standardized = standardize_location(location_filter)
        query = query.where(Agent.location_area == standardized)
    
    # Order by rating descending
    query = query.order_by(desc(Agent.rating)).offset(skip).limit(limit)
    
    result = await session.execute(query)
    agents = result.scalars().all()
    
    return [AgentResponse.model_validate(agent) for agent in agents]


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific agent by ID.
    """
    agent = await session.get(Agent, agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    return AgentResponse.model_validate(agent)


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_update: AgentUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Update agent information.
    """
    agent = await session.get(Agent, agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Check for duplicate email if updating
    if agent_update.email and agent_update.email != agent.email:
        existing = await session.execute(
            select(Agent).where(Agent.email == agent_update.email)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
    
    # Update fields
    update_data = agent_update.model_dump(exclude_unset=True)
    
    if "phone_number" in update_data and update_data["phone_number"]:
        update_data["phone_number"] = normalize_phone_number(update_data["phone_number"])
    
    if "location_area" in update_data and update_data["location_area"]:
        update_data["location_area"] = standardize_location(update_data["location_area"])
    
    for key, value in update_data.items():
        setattr(agent, key, value)
    
    await session.commit()
    
    return AgentResponse.model_validate(agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Delete an agent (soft delete via is_active=False).
    """
    agent = await session.get(Agent, agent_id)
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Soft delete
    agent.is_active = False
    await session.commit()