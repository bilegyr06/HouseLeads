from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String, Index
from datetime import datetime

from app.core.database import Base


class LeadMatch(Base):
	"""
	SQLAlchemy ORM model for lead-to-agent matches.
	Records matching decisions between tenant leads and agents.
	"""

	__tablename__ = "lead_matches"

	id = Column(Integer, primary_key=True, index=True)

	lead_id = Column(Integer, ForeignKey("tenant_leads.id"), nullable=False, index=True)
	agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False, index=True)

	match_score = Column(Float, nullable=False, default=0.0)
	match_reason = Column(String(500), nullable=True)

	status = Column(
		String(20),
		default="matched",
		index=True,
		comment="matched, contacted, interested, purchased, rejected",
	)

	created_at = Column(DateTime, default=datetime.utcnow, index=True, nullable=False)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

	__table_args__ = (
		Index("idx_lead_agent", "lead_id", "agent_id", unique=True),
	)

	def __repr__(self) -> str:
		return f"<LeadMatch(id={self.id}, lead_id={self.lead_id}, agent_id={self.agent_id}, score={self.match_score})>"
