from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String, Index
from datetime import datetime

from app.core.database import Base


class LeadPurchase(Base):
    """
    SQLAlchemy ORM model for lead purchases.
    Records when an agent purchases access to a tenant lead.
    """
    
    __tablename__ = "lead_purchases"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)
    lead_id = Column(Integer, ForeignKey("tenant_leads.id"), nullable=False, index=True)
    
    # Payment Information
    amount = Column(Float, nullable=False, comment="Amount paid in Naira")
    payment_reference = Column(String(100), nullable=True, unique=True, index=True)
    
    # Status
    status = Column(
        String(20),
        default="pending",
        index=True,
        comment="pending, completed, failed, refunded"
    )
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Indexes for common queries
    __table_args__ = (
        Index("idx_agent_lead", "agent_id", "lead_id", unique=True),
        Index("idx_payment_status", "payment_reference", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<LeadPurchase(id={self.id}, agent_id={self.agent_id}, lead_id={self.lead_id}, amount={self.amount})>"