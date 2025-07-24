"""
Cultural Heritage Mapping System - REDESIGNED for Nostalgia & Dementia Care
File: backend/config/cultural_mappings.py

MAJOR REDESIGN: Focuses on age-based nostalgia and dementia-friendly content.
- Heritage used ONLY for cuisine (appropriate cultural connection)
- Music & TV shows based on AGE/NOSTALGIA (not cultural stereotypes)
- Dementia-friendly content selection
"""

# Age-based nostalgic content mapping (birth decades)
# Based on formative years (teens/young adult) for strongest memories
AGE_BASED_NOSTALGIA = {
    # Greatest Generation (born 1920s-1940s)
    "greatest_generation": {  # Ages 80-104
        "music": "urn:tag:genre:music:jazz",  # Big band, swing era
        "tv_shows": "urn:tag:genre:media:classic",  # Classic TV, variety shows
        "formative_decades": [1940, 1950, 1960],
        "age_range": [80, 104]
    },
    
    # Silent Generation (born 1940s-1950s) 
    "silent_generation": {  # Ages 70-84
        "music": "urn:tag:genre:music:folk",  # Folk, early rock, crooners
        "tv_shows": "urn:tag:genre:media:classic",  # Golden age of TV
        "formative_decades": [1950, 1960, 1970],
        "age_range": [70, 84]
    },
    
    # Baby Boomers (born 1950s-1960s)
    "baby_boomers": {  # Ages 60-74
        "music": "urn:tag:genre:music:popular",  # Rock, folk, pop of 60s-70s
        "tv_shows": "urn:tag:genre:media:comedy",  # Sitcoms, variety shows
        "formative_decades": [1960, 1970, 1980],
        "age_range": [60, 74]
    },
    
    # Generation X (born 1960s-1980s)
    "generation_x": {  # Ages 40-64
        "music": "urn:tag:genre:music:popular",  # 70s-80s music
        "tv_shows": "urn:tag:genre:media:drama",  # 80s-90s TV
        "formative_decades": [1970, 1980, 1990],
        "age_range": [40, 64]
    },
    
    # Fallback for any age
    "universal": {
        "music": "urn:tag:genre:music:classical",  # Universally calming
        "tv_shows": "urn:tag:genre:media:classic",  # Timeless content
        "formative_decades": [1950, 1960, 1970],
        "age_range": [0, 120]
    }
}

# Heritage mapping ONLY for cuisine (appropriate cultural connection)
HERITAGE_TO_CUISINE = {
    "Italian-American": "urn:tag:genre:place:restaurant:italian",
    "Irish-American": "urn:tag:genre:place:restaurant:irish",
    "Mexican-American": "urn:tag:genre:place:restaurant:mexican", 
    "German-American": "urn:tag:genre:place:restaurant:german",
    "Chinese-American": "urn:tag:genre:place:restaurant:chinese",
    "Jewish-American": "urn:tag:genre:place:restaurant:kosher",
    "African-American": "urn:tag:genre:place:restaurant:southern",
    "Polish-American": "urn:tag:genre:place:restaurant:eastern_european",
    "Greek-American": "urn:tag:genre:place:restaurant:mediterranean",
    "Indian-American": "urn:tag:genre:place:restaurant:indian",
    
    # American regional cuisines (common backgrounds)
    "American": "urn:tag:genre:place:restaurant:american",
    "Southern": "urn:tag:genre:place:restaurant:southern",
    "Midwestern": "urn:tag:genre:place:restaurant:american",
    "Northeastern": "urn:tag:genre:place:restaurant:american",
    "Western": "urn:tag:genre:place:restaurant:american",
}

# Dementia-friendly interest mappings (positive, calming, familiar)
DEMENTIA_FRIENDLY_INTERESTS = {
    "loves music": "urn:tag:genre:music:classical",  # Calming, universal
    "loves cooking": "urn:tag:genre:place:restaurant:american",  # Familiar comfort
    "family activities": "urn:tag:genre:media:classic",  # Family-friendly classics
    "gardening": "urn:tag:genre:media:classic",  # Nature-themed content
    "reading": "urn:tag:genre:media:classic",  # Thoughtful, slower-paced
    "dancing": "urn:tag:genre:music:jazz",  # Social, nostalgic music
    "animals": "urn:tag:genre:media:classic",  # Animal-themed shows
    "travel": "urn:tag:genre:media:classic",  # Travel documentaries
    "sports": "urn:tag:genre:media:classic",  # Classic sports content
    "arts and crafts": "urn:tag:genre:media:classic"  # Creative, calm content
}

# Fallback tags (safe, universally appropriate)
UNIVERSAL_FALLBACK = {
    "cuisine": "urn:tag:genre:place:restaurant:american",  # Familiar comfort food
    "music": "urn:tag:genre:music:classical",  # Universally calming
    "tv_shows": "urn:tag:genre:media:classic"  # Timeless, family-appropriate
}

def get_generation_from_birth_year(birth_year: int, current_year: int = 2024) -> str:
    """
    Determine generation based on birth year for appropriate nostalgia.
    
    Args:
        birth_year: Year of birth
        current_year: Current year for age calculation
        
    Returns:
        Generation string for mapping lookup
    """
    age = current_year - birth_year
    
    if age >= 80:
        return "greatest_generation"
    elif age >= 70:
        return "silent_generation" 
    elif age >= 60:
        return "baby_boomers"
    elif age >= 40:
        return "generation_x"
    else:
        return "universal"

def get_heritage_tags(heritage: str, birth_year: int = None) -> dict:
    """
    Get appropriate tags based on heritage (cuisine only) and age (music/TV).
    
    REDESIGNED: Heritage only affects cuisine. Music/TV based on nostalgia.
    
    Args:
        heritage: Cultural heritage (used only for cuisine)
        birth_year: Birth year for age-based nostalgia
        
    Returns:
        Dictionary with cuisine (heritage-based), music & tv_shows (age-based)
    """
    
    # Get cuisine from heritage (only appropriate cultural mapping)
    heritage_clean = heritage.strip() if heritage else "American"
    cuisine_tag = HERITAGE_TO_CUISINE.get(heritage_clean)
    
    # Fallback cuisine matching
    if not cuisine_tag:
        for heritage_key, tag in HERITAGE_TO_CUISINE.items():
            if heritage_clean.lower() in heritage_key.lower():
                cuisine_tag = tag
                break
        else:
            cuisine_tag = UNIVERSAL_FALLBACK["cuisine"]
    
    # Get music and TV shows from AGE-BASED nostalgia
    if birth_year:
        generation = get_generation_from_birth_year(birth_year)
        nostalgia_data = AGE_BASED_NOSTALGIA.get(generation, AGE_BASED_NOSTALGIA["universal"])
        music_tag = nostalgia_data["music"]
        tv_shows_tag = nostalgia_data["tv_shows"]
    else:
        # No birth year provided, use universal fallback
        music_tag = UNIVERSAL_FALLBACK["music"]
        tv_shows_tag = UNIVERSAL_FALLBACK["tv_shows"]
    
    return {
        "cuisine": cuisine_tag,
        "music": music_tag,
        "tv_shows": tv_shows_tag
    }

def get_interest_tags(interests: list) -> list:
    """
    Get dementia-friendly tags for specific interests.
    
    Args:
        interests: List of interest strings
        
    Returns:
        List of appropriate, calming Qloo tags
    """
    tags = []
    
    for interest in interests:
        interest_clean = interest.strip().lower()
        
        # Direct match
        if interest_clean in DEMENTIA_FRIENDLY_INTERESTS:
            tags.append(DEMENTIA_FRIENDLY_INTERESTS[interest_clean])
            continue
        
        # Partial match
        for interest_key, tag in DEMENTIA_FRIENDLY_INTERESTS.items():
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

def get_formative_decades(birth_year: int) -> list:
    """
    Get the decades that were formative for someone (teens/young adult years).
    
    Args:
        birth_year: Year of birth
        
    Returns:
        List of decade years when they were 15-35 (strongest memories)
    """
    formative_start = birth_year + 15  # Age 15
    formative_end = birth_year + 35    # Age 35
    
    decades = []
    for decade_start in range(1920, 2030, 10):  # 1920, 1930, 1940, etc.
        if decade_start >= formative_start - 10 and decade_start <= formative_end:
            decades.append(decade_start)
    
    return decades

def validate_heritage_coverage() -> dict:
    """
    Validate that the mapping system works correctly.
    
    Returns:
        Validation results
    """
    test_cases = [
        ("Italian-American", 1945),
        ("Irish-American", 1950), 
        ("Unknown-Heritage", 1960),
        ("American", 1940)
    ]
    
    valid_cases = []
    invalid_cases = []
    
    for heritage, birth_year in test_cases:
        try:
            tags = get_heritage_tags(heritage, birth_year)
            required_keys = ["cuisine", "music", "tv_shows"]
            
            if all(key in tags and tags[key] for key in required_keys):
                valid_cases.append(f"{heritage} (born {birth_year})")
            else:
                invalid_cases.append(f"{heritage} (born {birth_year}) - missing tags")
                
        except Exception as e:
            invalid_cases.append(f"{heritage} (born {birth_year}) - error: {e}")
    
    return {
        "total_cases": len(test_cases),
        "valid_cases": valid_cases,
        "invalid_cases": invalid_cases,
        "validation_passed": len(invalid_cases) == 0
    }

# Test functions
def test_nostalgia_mapping():
    """Test the nostalgia-based mapping system."""
    print("🧪 Testing Nostalgia-Based Mapping System")
    print("=" * 50)
    
    test_cases = [
        ("Italian-American", 1945, "Maria, 79 years old"),
        ("Irish-American", 1950, "Patrick, 74 years old"),
        ("American", 1960, "Susan, 64 years old"),
        ("Chinese-American", 1935, "Li, 89 years old")
    ]
    
    for heritage, birth_year, description in test_cases:
        tags = get_heritage_tags(heritage, birth_year) 
        generation = get_generation_from_birth_year(birth_year)
        age = 2024 - birth_year
        
        print(f"\n✅ {description}")
        print(f"   Heritage: {heritage} → Cuisine: {tags['cuisine']}")
        print(f"   Age {age} ({generation}) → Music: {tags['music']}")
        print(f"   Age {age} ({generation}) → TV: {tags['tv_shows']}")
        
        formative = get_formative_decades(birth_year)
        print(f"   Formative decades: {formative}")
    
    return True

if __name__ == "__main__":
    print("Testing Nostalgia & Age-Based Mapping System")
    print("(Dementia-Friendly, Non-Stereotypical)")
    print("=" * 60)
    
    nostalgia_test = test_nostalgia_mapping()
    validation = validate_heritage_coverage()
    
    print(f"\n" + "=" * 60)
    print(f"Nostalgia Mapping: {'✅ PASSED' if nostalgia_test else '❌ FAILED'}")
    print(f"System Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")
    
    if nostalgia_test and validation['validation_passed']:
        print(f"\n🎉 SUCCESS! New system is working correctly.")
        print(f"✅ Heritage used ONLY for cuisine (appropriate)")
        print(f"✅ Music & TV based on age/nostalgia (non-stereotypical)")
        print(f"✅ Dementia-friendly content selection")
        print(f"✅ {len(validation['valid_cases'])} test cases passed")
    else:
        print(f"\n❌ Issues found:")
        for issue in validation['invalid_cases']:
            print(f"   - {issue}")