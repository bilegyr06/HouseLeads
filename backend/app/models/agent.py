from sqlalchemy import Column, DateTime, String, Enum, ARRAY, Float, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    areas_of_interest = Column(ARRAY(String))  # ["Lekki", "Ikeja"]
    budget_range_focus = Column(String)  # e.g. "500k-2M"
    subscription_plan = Column(Enum("FREE", "BASIC", "PREMIUM", name="plan_enum"), default="FREE")
    wallet_balance = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())