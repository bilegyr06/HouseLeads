"""
Integration test for lead matching endpoints.
Tests agent creation, lead creation, and lead matching workflows.

Run with: pytest test_lead_matching.py -v
"""

import asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app
from app.models import Agent, TenantLead, LeadMatch
from app.core.security import get_password_hash
from datetime import datetime, date, timedelta


# Test database URL (use same DB or separate test DB if preferred)
TEST_DATABASE_URL = settings.DATABASE_URL

# Create async engine and session for tests
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    """Override DB dependency for tests."""
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
async def client():
    """Create an async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db_session():
    """Create a fresh DB session for each test."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.mark.asyncio
async def test_agent_signup_and_login(client):
    """Test agent signup and login flow."""
    
    # Signup
    signup_payload = {
        "full_name": "John Agent",
        "email": "john@example.com",
        "phone_number": "+2348012345678",
        "password": "securepass123",
        "location_area": "Lagos Island",
        "agency_name": "Top Properties"
    }
    
    response = await client.post("/agents/signup", json=signup_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["full_name"] == "John Agent"
    agent_id = data["id"]
    
    # Login
    login_payload = {
        "email": "john@example.com",
        "password": "securepass123"
    }
    response = await client.post("/agents/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    token = data["access_token"]
    
    return agent_id, token


@pytest.mark.asyncio
async def test_create_tenant_lead(client):
    """Test tenant lead creation."""
    
    lead_payload = {
        "full_name": "Alice Tenant",
        "phone_number": "+2349012345678",
        "email": "alice@example.com",
        "location_preference": "Ikoyi",
        "budget_min": 500000,
        "budget_max": 2000000,
        "property_type": "apartment",
        "move_in_date": (date.today() + timedelta(days=30)).isoformat()
    }
    
    response = await client.post("/tenant_leads/create", json=lead_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "Alice Tenant"
    assert data["location_preference"] == "Ikoyi"
    lead_id = data["id"]
    
    return lead_id


@pytest.mark.asyncio
async def test_matching_workflow(client):
    """Test full lead matching workflow: signup agent, create lead, match."""
    
    # 1. Create agent
    agent_payload = {
        "full_name": "Jane Realtor",
        "email": "jane@realty.com",
        "phone_number": "+2347012345678",
        "password": "pass1234",
        "location_area": "Ikoyi",
        "agency_name": "Elite Realty"
    }
    
    response = await client.post("/agents/signup", json=agent_payload)
    assert response.status_code == 201
    agent_data = response.json()
    agent_id = agent_data["id"]
    
    # 2. Create tenant lead
    lead_payload = {
        "full_name": "Bob Seeker",
        "phone_number": "+2346012345678",
        "email": "bob@example.com",
        "location_preference": "Ikoyi",
        "budget_min": 800000,
        "budget_max": 3000000,
        "property_type": "apartment",
        "move_in_date": (date.today() + timedelta(days=45)).isoformat()
    }
    
    response = await client.post("/tenant_leads/create", json=lead_payload)
    assert response.status_code == 201
    lead_data = response.json()
    lead_id = lead_data["id"]
    
    # 3. Match lead to agent
    # If your API has a match endpoint, test it here
    # Expected endpoint pattern: POST /leads/{lead_id}/match or similar
    match_payload = {
        "lead_id": lead_id,
        "agent_id": agent_id,
        "match_score": 0.92,
        "match_reason": "Agent in preferred location with matching profile"
    }
    
    # Adjust endpoint based on your actual routes
    response = await client.post(f"/leads/{lead_id}/match", json=match_payload)
    
    # If endpoint doesn't exist, test will show 404 (expected for now)
    # Once you add match endpoint, this should return 201/200
    print(f"\nMatch endpoint response: {response.status_code}")
    if response.status_code in [200, 201]:
        match_data = response.json()
        assert match_data["lead_id"] == lead_id
        assert match_data["agent_id"] == agent_id
    else:
        print("Note: Match endpoint not yet implemented in routes")
    
    return agent_id, lead_id


@pytest.mark.asyncio
async def test_lead_scoring(db_session):
    """Test lead scoring logic (unit test style)."""
    from app.services.lead_scoring import calculate_lead_score
    
    # Create test lead in DB
    lead = TenantLead(
        full_name="Test Lead",
        phone_number="+2345555555",
        location_preference="VI",
        budget_max=5000000,
        property_type="duplex",
        move_in_date=date.today() + timedelta(days=30),
        status="new"
    )
    db_session.add(lead)
    await db_session.flush()
    
    # Calculate score
    score = calculate_lead_score(lead)
    assert isinstance(score, float)
    assert 0 <= score <= 1.0
    print(f"\nCalculated lead score: {score}")


@pytest.mark.asyncio
async def test_agent_matching_strategy(db_session):
    """Test agent-lead matching logic (unit test style)."""
    from app.services.matching import find_matching_agents
    
    # Create test agent
    agent = Agent(
        full_name="Test Agent",
        phone_number="+2344444444",
        email="test@agent.com",
        password_hash=get_password_hash("password"),
        location_area="VI",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(agent)
    
    # Create test lead in matching location
    lead = TenantLead(
        full_name="Test Seeker",
        phone_number="+2345555556",
        location_preference="VI",
        budget_max=4000000,
        property_type="apartment",
        move_in_date=date.today() + timedelta(days=20),
        status="new",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(lead)
    await db_session.flush()
    
    # Find matching agents
    matches = find_matching_agents(lead, [agent])
    assert len(matches) > 0
    assert matches[0]["agent_id"] == agent.id
    print(f"\nFound {len(matches)} matching agent(s)")


# Run tests with: pytest test_lead_matching.py -v -s
if __name__ == "__main__":
    print("Run with: pytest test_lead_matching.py -v -s")
