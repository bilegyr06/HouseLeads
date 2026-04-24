from sqlalchemy import Column, ForeignKey, DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class LeadPurchase(Base):
    __tablename__ = "lead_purchases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    tenant_lead_id = Column(UUID(as_uuid=True), ForeignKey("tenant_leads.id"), nullable=False)
    price_paid = Column(Float, nullable=False)
    payment_reference = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    agent = relationship("Agent")
    tenant_lead = relationship("TenantLead")