from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Date
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class TenantLead(Base):
    __tablename__ = "tenant_leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=False)  # we'll normalize
    email = Column(String, nullable=True)

    location_preference = Column(String, nullable=False)  # e.g. "Lekki", "Yaba"
    budget_min = Column(Integer, nullable=True)  # in Naira
    budget_max = Column(Integer, nullable=False)
    property_type = Column(String, nullable=False)  # "self-contain", "1 bedroom", etc.
    move_in_date = Column(Date, nullable=False)

    urgency_score = Column(Enum("LOW", "MEDIUM", "HIGH", name="urgency_enum"), default="MEDIUM")
    lead_score = Column(Float, default=0.0)

    status = Column(Enum("NEW", "VALIDATED", "SENT", "SOLD", "CLOSED", name="lead_status"), default="NEW")

    created_at = Column(DateTime(timezone=True), server_default=func.now())