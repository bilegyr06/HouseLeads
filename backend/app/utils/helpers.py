import re
from typing import Optional


def normalize_phone_number(phone: str) -> str:
    """
    Normalize Nigerian phone number to international format (+234XXXXXXXXXX).
    
    Accepts formats:
    - 0803 123 4567 (local with spaces)
    - 08031234567 (local without spaces)
    - +2348031234567 (already international)
    - 2348031234567 (without + prefix)
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Normalized phone number in +234XXXXXXXXXX format
        
    Raises:
        ValueError: If phone number format is invalid
    """
    if not phone or not isinstance(phone, str):
        raise ValueError("Phone number must be a non-empty string")
    
    # Remove spaces, hyphens, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Handle different prefixes
    if cleaned.startswith('+234'):
        # Already in international format
        return cleaned
    elif cleaned.startswith('234'):
        # International without +
        return f"+{cleaned}"
    elif cleaned.startswith('0'):
        # Local format - replace 0 with 234
        return f"+234{cleaned[1:]}"
    else:
        raise ValueError(
            f"Invalid phone number format: {phone}. "
            "Must start with 0, 234, or +234"
        )


def standardize_location(location: str) -> str:
    """
    Standardize Lagos location names to canonical forms.
    
    Maps common variations to standard names:
    - "lekki" → "Lekki"
    - "ikeja" → "Ikeja"
    - "VI", "v.i.", "victoria" → "Victoria Island"
    
    Args:
        location: Raw location string
        
    Returns:
        Standardized location name
    """
    if not location or not isinstance(location, str):
        return ""
    
    location_lower = location.strip().lower()
    
    # Location mapping dictionary
    location_map = {
        # Lekki variations
        "lekki": "Lekki",
        "lekki phase 1": "Lekki Phase 1",
        "lekki phase 2": "Lekki Phase 2",
        "lekki phase 3": "Lekki Phase 3",
        
        # Ikoyi variations
        "ikoyi": "Ikoyi",
        
        # Victoria Island variations
        "victoria island": "Victoria Island",
        "vi": "Victoria Island",
        "v.i.": "Victoria Island",
        "v.i": "Victoria Island",
        "victoria": "Victoria Island",
        
        # Ajah variations
        "ajah": "Ajah",
        
        # Banana Island variations
        "banana island": "Banana Island",
        "banana": "Banana Island",
        
        # Yaba variations
        "yaba": "Yaba",
        
        # Ikeja variations
        "ikeja": "Ikeja",
        
        # Surulere variations
        "surulere": "Surulere",
        
        # Shomolu variations
        "shomolu": "Shomolu",
        "somolu": "Shomolu",
        
        # Alimosho variations
        "alimosho": "Alimosho",
        
        # Ikorodu variations
        "ikorodu": "Ikorodu",
    }
    
    return location_map.get(location_lower, location.strip())


def is_valid_nigerian_phone(phone: str) -> bool:
    """
    Validate if a phone number is a valid Nigerian format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid Nigerian phone format, False otherwise
    """
    try:
        normalize_phone_number(phone)
        return True
    except ValueError:
        return False


def calculate_distance_score(agent_location: str, lead_location: str) -> float:
    """
    Calculate location proximity score (0.0 to 1.0).
    
    Same location = 1.0
    Adjacent locations = 0.7
    Different locations = 0.0
    
    Args:
        agent_location: Agent's operating location
        lead_location: Lead's preferred location
        
    Returns:
        Proximity score (0.0 to 1.0)
    """
    agent_loc = standardize_location(agent_location).lower()
    lead_loc = standardize_location(lead_location).lower()
    
    if agent_loc == lead_loc:
        return 1.0
    
    # Adjacent/nearby locations
    adjacent_pairs = {
        ("lekki", "ikoyi"),
        ("lekki", "victoria island"),
        ("lekki", "ajah"),
        ("ikoyi", "victoria island"),
        ("victoria island", "banana island"),
    }
    
    for loc1, loc2 in adjacent_pairs:
        if (agent_loc == loc1 and lead_loc == loc2) or (agent_loc == loc2 and lead_loc == loc1):
            return 0.7
    
    return 0.0