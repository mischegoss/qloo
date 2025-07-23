"""
Cultural Heritage Mapping System
File: backend/config/cultural_mappings.py

Provides reliable hardcoded mappings from cultural heritage to Qloo tags.
This replaces complex keyword extraction with simple, testable mappings.
"""

# Hardcoded reliable tag mappings for cultural heritage
# Using correct Qloo tag formats from documentation
HERITAGE_TO_TAGS = {
    "Italian-American": {
        "cuisine": "urn:tag:genre:place:restaurant:italian",
        "music": "urn:tag:genre:music:classical",
        "movies": "urn:tag:genre:media:family"
    },
    "Irish-American": {
        "cuisine": "urn:tag:genre:place:restaurant:irish", 
        "music": "urn:tag:genre:music:folk",
        "movies": "urn:tag:genre:media:classic"
    },
    "Mexican-American": {
        "cuisine": "urn:tag:genre:place:restaurant:mexican",
        "music": "urn:tag:genre:music:latin",
        "movies": "urn:tag:genre:media:family"
    },
    "German-American": {
        "cuisine": "urn:tag:genre:place:restaurant:german",
        "music": "urn:tag:genre:music:classical",
        "movies": "urn:tag:genre:media:classic"
    },
    "Chinese-American": {
        "cuisine": "urn:tag:genre:place:restaurant:chinese",
        "music": "urn:tag:genre:music:classical",
        "movies": "urn:tag:genre:media:family"
    },
    "Jewish-American": {
        "cuisine": "urn:tag:genre:place:restaurant:kosher",
        "music": "urn:tag:genre:music:classical",
        "movies": "urn:tag:genre:media:classic"
    },
    "African-American": {
        "cuisine": "urn:tag:genre:place:restaurant:southern",
        "music": "urn:tag:genre:music:jazz",
        "movies": "urn:tag:genre:media:classic"
    },
    "Polish-American": {
        "cuisine": "urn:tag:genre:place:restaurant:eastern_european",
        "music": "urn:tag:genre:music:folk",
        "movies": "urn:tag:genre:media:classic"
    },
    "Greek-American": {
        "cuisine": "urn:tag:genre:place:restaurant:mediterranean",
        "music": "urn:tag:genre:music:classical",
        "movies": "urn:tag:genre:media:family"
    },
    "Indian-American": {
        "cuisine": "urn:tag:genre:place:restaurant:indian",
        "music": "urn:tag:genre:music:classical",
        "movies": "urn:tag:genre:media:family"
    }
}

# Additional interest-based tag mappings (using correct Qloo format)
INTEREST_TO_TAGS = {
    "loves music": "urn:tag:genre:music:classical",
    "loves cooking": "urn:tag:genre:place:restaurant:american",
    "family activities": "urn:tag:genre:media:family",
    "gardening": "urn:tag:activity:outdoor",
    "reading": "urn:tag:genre:media:books",
    "dancing": "urn:tag:genre:music:dance",
    "movies": "urn:tag:genre:media:classic",
    "travel": "urn:tag:activity:travel",
    "sports": "urn:tag:activity:sports",
    "arts and crafts": "urn:tag:activity:creative"
}

# Fallback tags for when heritage is not found (using correct Qloo format)
FALLBACK_TAGS = {
    "cuisine": "urn:tag:genre:place:restaurant:american",
    "music": "urn:tag:genre:music:popular",
    "movies": "urn:tag:genre:media:family"
}

def get_heritage_tags(heritage: str) -> dict:
    """
    Get Qloo tags for a specific cultural heritage.
    
    Args:
        heritage: Cultural heritage string (e.g., "Italian-American")
        
    Returns:
        Dictionary with cuisine, music, and movies tags
    """
    heritage_clean = heritage.strip()
    
    # Direct match
    if heritage_clean in HERITAGE_TO_TAGS:
        return HERITAGE_TO_TAGS[heritage_clean].copy()
    
    # Partial match (e.g., "Italian" matches "Italian-American")
    for heritage_key, tags in HERITAGE_TO_TAGS.items():
        if heritage_clean.lower() in heritage_key.lower():
            return tags.copy()
        if heritage_key.split('-')[0].lower() == heritage_clean.lower():
            return tags.copy()
    
    # Return fallback tags
    return FALLBACK_TAGS.copy()

def get_interest_tags(interests: list) -> list:
    """
    Get Qloo tags for specific interests.
    
    Args:
        interests: List of interest strings
        
    Returns:
        List of matching Qloo tags
    """
    tags = []
    
    for interest in interests:
        interest_clean = interest.strip().lower()
        
        # Direct match
        if interest_clean in INTEREST_TO_TAGS:
            tags.append(INTEREST_TO_TAGS[interest_clean])
            continue
        
        # Partial match
        for interest_key, tag in INTEREST_TO_TAGS.items():
            if interest_clean in interest_key.lower() or interest_key.lower() in interest_clean:
                tags.append(tag)
                break
    
    return list(set(tags))  # Remove duplicates

def get_age_demographic(birth_year: int, current_year: int = 2024) -> str:
    """
    Convert birth year to Qloo age demographic.
    
    Args:
        birth_year: Year of birth
        current_year: Current year for calculation
        
    Returns:
        Qloo age demographic string
    """
    age = current_year - birth_year
    
    if age <= 35:
        return "35_and_younger"
    elif age <= 55:
        return "36_to_55"
    else:
        return "55_and_older"

def validate_heritage_coverage() -> dict:
    """
    Validate that all heritage mappings have required tags.
    
    Returns:
        Validation report
    """
    required_keys = {"cuisine", "music", "movies"}
    validation_report = {
        "valid_heritages": [],
        "invalid_heritages": [],
        "total_heritages": len(HERITAGE_TO_TAGS)
    }
    
    for heritage, tags in HERITAGE_TO_TAGS.items():
        if set(tags.keys()) == required_keys:
            validation_report["valid_heritages"].append(heritage)
        else:
            validation_report["invalid_heritages"].append({
                "heritage": heritage,
                "missing_keys": required_keys - set(tags.keys()),
                "extra_keys": set(tags.keys()) - required_keys
            })
    
    return validation_report

# Test the mappings
if __name__ == "__main__":
    # Test heritage mapping
    print("Testing heritage mappings:")
    test_heritage = "Italian-American"
    tags = get_heritage_tags(test_heritage)
    print(f"{test_heritage}: {tags}")
    
    # Test interest mapping
    print("\nTesting interest mappings:")
    test_interests = ["loves music", "cooking", "family activities"]
    interest_tags = get_interest_tags(test_interests)
    print(f"{test_interests}: {interest_tags}")
    
    # Test age demographic
    print("\nTesting age demographic:")
    age_demo = get_age_demographic(1945)
    print(f"Born 1945: {age_demo}")
    
    # Validate coverage
    print("\nValidation report:")
    validation = validate_heritage_coverage()
    print(f"Valid heritages: {len(validation['valid_heritages'])}/{validation['total_heritages']}")
    if validation["invalid_heritages"]:
        print("Invalid heritages:", validation["invalid_heritages"])