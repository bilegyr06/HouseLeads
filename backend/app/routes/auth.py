"""
Authentication routes for agent login and signup.
Provides endpoints for agent authentication with JWT tokens.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.database import get_session
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.agent import Agent
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    SignupRequest,
    SignupResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    data: SignupRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new agent account.
    
    Validates email uniqueness and creates agent with hashed password.
    
    Args:
        data: SignupRequest with email, password, name, phone, location
        session: Database session
        
    Returns:
        SignupResponse with agent_id and confirmation message
        
    Raises:
        HTTPException: If email or phone already registered
    """
    try:
        logger.info(f"Signup request for email: {data.email}, phone: {data.phone_number}")
        
        # Check if email already exists
        logger.debug("Checking if email already exists...")
        result = await session.execute(
            select(Agent).where(Agent.email == data.email)
        )
        if result.scalar_one_or_none():
            logger.warning(f"Signup attempt with existing email: {data.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        logger.debug("Email check passed")
        
        # Check if phone number already exists
        logger.debug("Checking if phone number already exists...")
        result = await session.execute(
            select(Agent).where(Agent.phone_number == data.phone_number)
        )
        if result.scalar_one_or_none():
            logger.warning(f"Signup attempt with existing phone: {data.phone_number}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
        logger.debug("Phone number check passed")
        
        # Hash password
        logger.debug("Hashing password...")
        try:
            password_hash = hash_password(data.password)
            logger.debug("Password hashed successfully")
        except Exception as hash_err:
            logger.error(f"Error hashing password: {str(hash_err)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing password. Please try again."
            )
        
        # Create new agent with hashed password
        logger.debug("Creating Agent object...")
        agent = Agent(
            email=data.email,
            password_hash=password_hash,
            full_name=data.full_name,
            phone_number=data.phone_number,
            location_area=data.location_area,
            is_active=True,
            rating=0.0,
            total_leads_matched=0,
            total_leads_converted=0,
        )
        
        logger.debug("Adding agent to session...")
        session.add(agent)
        
        logger.debug("Committing session...")
        await session.commit()
        logger.info(f"Agent committed to database")
        
        logger.debug("Refreshing agent object...")
        await session.refresh(agent)
        logger.info(f"Agent signup successful: id={agent.id}, email={agent.email}")
        
        return SignupResponse(
            agent_id=agent.id,
            email=agent.email,
            full_name=agent.full_name,
            message="Agent created successfully. Please log in."
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions (already have proper error messages)
        raise
    except IntegrityError as integrity_err:
        logger.error(f"IntegrityError during signup: {str(integrity_err)}", exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email or phone number already exists"
        )
    except Exception as err:
        logger.error(f"Unexpected error during signup: {str(err)}", exc_info=True)
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Signup failed: {str(err)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate agent and return JWT token.
    
    Verifies email and password, returns access token if valid.
    
    Args:
        credentials: LoginRequest with email and password
        session: Database session
        
    Returns:
        LoginResponse with JWT access_token and agent info
        
    Raises:
        HTTPException: If credentials invalid or account inactive
    """
    # Get agent by email
    result = await session.execute(
        select(Agent).where(Agent.email == credentials.email)
    )
    agent = result.scalar_one_or_none()
    
    if not agent or not verify_password(credentials.password, agent.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not agent.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(agent.id)})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        agent_id=agent.id,
        email=agent.email,
        full_name=agent.full_name,
    )
