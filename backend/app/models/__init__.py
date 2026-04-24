"""
SQLAlchemy ORM models for NaijaHomeLeads.
All models are imported here to ensure they're registered with Base.
"""

from app.models.tenant_lead import TenantLead
from app.models.agent import Agent

__all__ = [
    "TenantLead",
    "Agent",
]