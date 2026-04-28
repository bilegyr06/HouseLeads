from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tenant_lead import TenantLead
from app.models.agent import Agent
from app.utils.helpers import calculate_distance_score, standardize_location


class MatchingService:
    """Service for matching tenant leads to real estate agents."""
    
    @staticmethod
    async def find_best_matches(
        session: AsyncSession,
        lead: TenantLead,
        limit: int = 5
    ) -> List[tuple[Agent, float]]:
        """
        Find best agent matches for a tenant lead.
        
        Scoring factors:
        - Location match: 40% weight
        - Agent rating: 30% weight
        - Lead score: 20% weight
        - Conversion rate: 10% weight
        
        Args:
            session: Database session
            lead: TenantLead object to match
            limit: Maximum number of matches to return
            
        Returns:
            List of (Agent, match_score) tuples, sorted by score descending
        """
        # Get all active agents
        query = select(Agent).where(Agent.is_active == True)
        result = await session.execute(query)
        agents = result.scalars().all()
        
        if not agents:
            return []
        
        matches: List[tuple[Agent, float]] = []
        
        for agent in agents:
            score = MatchingService._calculate_match_score(lead, agent)
            matches.append((agent, score))
        
        # Sort by score descending and limit
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[:limit]
    
    @staticmethod
    def _calculate_match_score(lead: TenantLead, agent: Agent) -> float:
        """
        Calculate match score between lead and agent (0.0 to 1.0).
        
        Weighted scoring:
        - Location: 40%
        - Agent rating: 30%
        - Lead quality: 20%
        - Conversion rate: 10%
        
        Args:
            lead: TenantLead object
            agent: Agent object
            
        Returns:
            Match score (0.0 to 1.0)
        """
        # Location score (40%) - Handle multiple lead locations
        lead_locations = [loc.strip() for loc in lead.location_preference.split(",")]
        # Get the best score among all preferred locations
        location_scores = [calculate_distance_score(agent.location_area, loc) for loc in lead_locations]
        best_location_score = max(location_scores) if location_scores else 0.0
        
        location_weighted = best_location_score * 0.40
        
        # Agent rating score (30%) - normalize to 0.0-1.0 (out of 5.0)
        rating_score = min(agent.rating / 5.0, 1.0)
        rating_weighted = rating_score * 0.30
        
        # Lead quality score (20%) - already 0.0-1.0
        lead_score_normalized = min(lead.lead_score / 100.0, 1.0)
        lead_weighted = lead_score_normalized * 0.20
        
        # Conversion rate (10%)
        total_matches = agent.total_leads_matched or 1  # Avoid division by zero
        conversion_rate = (agent.total_leads_converted / total_matches) if total_matches > 0 else 0.0
        conversion_weighted = min(conversion_rate, 1.0) * 0.10
        
        total_score = location_weighted + rating_weighted + lead_weighted + conversion_weighted
        return round(total_score, 2)
    
    @staticmethod
    async def get_agents_by_location(
        session: AsyncSession,
        location: str,
        is_active_only: bool = True
    ) -> List[Agent]:
        """
        Get agents operating in a specific location.
        
        Args:
            session: Database session
            location: Location to search for
            is_active_only: Only return active agents
            
        Returns:
            List of Agent objects
        """
        standardized_loc = standardize_location(location)
        
        query = select(Agent).where(Agent.location_area == standardized_loc)
        if is_active_only:
            query = query.where(Agent.is_active == True)
        
        result = await session.execute(query)
        return result.scalars().all()