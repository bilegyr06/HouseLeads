from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Index
from datetime import datetime

from app.core.database import Base

class TenantLead(Base):
    """
    SQLAlchemy ORM model for tenant leads.
    Represents a tenant looking for rental properties.
    """
    
    __tablename__ = "tenant_leads"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    full_name = Column(String(100), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=True)
    
    # Lead Preferences
    location_preference = Column(String(100), nullable=False, index=True)
    budget_min = Column(Integer, nullable=True)
    budget_max = Column(Integer, nullable=False)
    property_type = Column(String(50), nullable=False)
    move_in_date = Column(Date, nullable=False)
    
    # Scoring & Status
    lead_score = Column(Float, default=0.0)
    status = Column(
        String(20),
        default="new",
        index=True,
        comment="new, contacted, interested, matched, closed"
    )
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes for common queries
    __table_args__ = (
        Index("idx_location_status", "location_preference", "status"),
        Index("idx_budget_type", "budget_max", "property_type"),
        Index("idx_move_in_date", "move_in_date"),
    )
    
    def __repr__(self) -> str:
        return f"<TenantLead(id={self.id}, full_name='{self.full_name}', phone='{self.phone_number}')>"