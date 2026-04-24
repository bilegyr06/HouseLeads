from datetime import date
from app.schemas.tenant_lead import TenantLeadCreate

def calculate_urgency_score(move_in_date: date) -> str:
    """Calculate urgency based on move-in date."""
    if not isinstance(move_in_date, date):
        return "LOW"
    
    days = (move_in_date - date.today()).days
    if days <= 7:
        return "HIGH"
    elif days <= 21:
        return "MEDIUM"
    return "LOW"

def calculate_lead_score(lead: TenantLeadCreate) -> float:
    """Calculate lead quality score (0-100)."""
    if not lead:
        return 0.0
    
    score = 0.0

    # Budget realism (Lagos 2026 rents are insane)
    if lead.budget_max and lead.budget_max >= 800000:
        score += 25
    elif lead.budget_max and lead.budget_max >= 400000:
        score += 15
    elif lead.budget_max and lead.budget_max < 200000:
        score -= 10  # Unrealistically low budget

    # Urgency
    if lead.move_in_date and isinstance(lead.move_in_date, date):
        days = (lead.move_in_date - date.today()).days
        if days <= 10:
            score += 35
        elif days <= 30:
            score += 20
        elif days < 0:
            score -= 50  # Past date is invalid

    # Hot locations (island premium) - case insensitive
    hot_locations = {"lekki", "ikoyi", "victoria island", "ajah", "banana island"}
    if lead.location_preference and lead.location_preference.lower() in hot_locations:
        score += 30

    # High-demand property types
    hot_types = {"self-contain", "1 bedroom", "mini flat", "2 bedroom"}
    if lead.property_type and lead.property_type.lower() in hot_types:
        score += 20

    return min(max(round(score, 1), 0.0), 100.0)