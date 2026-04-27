from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Index
from datetime import datetime

from app.core.database import Base


class Agent(Base):
    """
    SQLAlchemy ORM model for real estate agents.
    Represents agents who will receive matched leads.
    """
    
    __tablename__ = "agents"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Personal Information
    full_name = Column(String(100), nullable=False, index=True)
    phone_number = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    
    # Authentication
    password_hash = Column(String(255), nullable=False, index=True, comment="Hashed password using bcrypt")
    
    # Agent Details
    location_area = Column(String(100), nullable=False, index=True, comment="Geographic area they operate in")
    agency_name = Column(String(100), nullable=True)
    
    # Performance Metrics
    rating = Column(Float, default=0.0, comment="Rating out of 5.0")
    total_leads_matched = Column(Integer, default=0)
    total_leads_converted = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes for common queries
    __table_args__ = (
        Index("idx_location_active", "location_area", "is_active"),
        Index("idx_rating", "rating"),
    )
    
    def __repr__(self) -> str:
        return f"<Agent(id={self.id}, full_name='{self.full_name}', location='{self.location_area}')>"