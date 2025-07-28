def _extract_basic_profile(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and validate anonymized profile information with PII safety checks"""
    
    # PII VALIDATION - Ensure no personally identifiable information is present
    pii_fields = ["first_name", "last_name", "name", "full_name", "email", "phone", "ssn", "address"]
    detected_pii = [field for field in pii_fields if patient_profile.get(field)]
    
    if detected_pii:
        logger.warning(f"🚨 PII DETECTED in profile: {detected_pii}. Rejecting request for compliance.")
        raise ValueError(f"Profile contains PII fields: {detected_pii}. Only anonymized data is accepted.")
    
    # LOCATION VALIDATION - Ensure no precise location data
    location_pii = ["city", "state", "zip_code", "postal_code", "address", "street", "coordinates", "latitude", "longitude"]
    detected_location_pii = [field for field in location_pii if patient_profile.get(field)]
    
    if detected_location_pii:
        logger.warning(f"🚨 LOCATION PII DETECTED: {detected_location_pii}. Rejecting request for compliance.")
        raise ValueError(f"Profile contains location PII: {detected_location_pii}. Location data not permitted.")
    
    # EXTRACT SAFE, ANONYMIZED FIELDS ONLY
    birth_year = patient_profile.get("birth_year")
    age_group = patient_profile.get("age_group", "senior")  # Accept pre-calculated age_group
    cultural_heritage = patient_profile.get("cultural_heritage", "American")
    interests = patient_profile.get("interests", [])
    profile_complete = patient_profile.get("profile_complete", False)
    
    # VALIDATE BIRTH YEAR RANGE (prevent unrealistic ages)
    current_year = datetime.now().year
    if birth_year:
        if not isinstance(birth_year, int) or birth_year < 1900 or birth_year > current_year:
            logger.warning(f"🚨 Invalid birth_year: {birth_year}. Must be between 1900 and {current_year}")
            birth_year = None
            age_group = "senior"  # Default safe assumption
    
    # CALCULATE AGE SAFELY (fallback if age_group not provided)
    current_age = None
    if birth_year:
        current_age = current_year - birth_year
        # Double-check age_group calculation if not provided or invalid
        if age_group not in ["adult", "senior", "oldest_senior"]:
            if current_age >= 80:
                age_group = "oldest_senior"
            elif current_age >= 65:
                age_group = "senior"
            else:
                age_group = "adult"
    
    # VALIDATE CULTURAL HERITAGE (ensure it's a safe string)
    if cultural_heritage and (len(cultural_heritage) > 100 or not isinstance(cultural_heritage, str)):
        logger.warning(f"🚨 Invalid cultural_heritage format: {cultural_heritage}")
        cultural_heritage = "American"  # Safe default
    
    # VALIDATE INTERESTS (ensure safe list of strings)
    if not isinstance(interests, list):
        interests = []
    else:
        # Filter interests to safe strings only
        safe_interests = []
        for interest in interests[:10]:  # Limit to 10 interests max
            if isinstance(interest, str) and len(interest) <= 50 and interest.isalnum() or ' ' in interest:
                safe_interests.append(interest.strip())
        interests = safe_interests
    
    # ANONYMIZED LOGGING (no PII)
    logger.info(f"📝 Anonymized profile validated: age_group={age_group}, heritage={cultural_heritage}, interests_count={len(interests)}")
    
    # RETURN ONLY SAFE, ANONYMIZED DATA
    return {
        # NO PII FIELDS - completely removed
        "birth_year": birth_year,
        "current_age": current_age,
        "age_group": age_group,
        "cultural_heritage": cultural_heritage,
        "interests": interests,
        "profile_complete": profile_complete,
        # NO LOCATION DATA - removed for privacy
        # Anonymization metadata
        "anonymized": True,
        "pii_validated": True,
        "validation_timestamp": datetime.now().isoformat()
    }

def _validate_anonymized_profile(self, patient_profile: Dict[str, Any]) -> bool:
    """Additional validation method to ensure profile is properly anonymized"""
    
    # Define all possible PII fields that should never be present
    forbidden_fields = [
        # Name fields
        "first_name", "last_name", "name", "full_name", "given_name", "family_name",
        "middle_name", "nickname", "preferred_name", "maiden_name",
        
        # Contact information
        "email", "phone", "phone_number", "mobile", "telephone",
        
        # Identification
        "ssn", "social_security", "passport", "license", "id_number", "patient_id",
        
        # Location data
        "address", "street", "city", "state", "zip_code", "postal_code", "country",
        "coordinates", "latitude", "longitude", "geolocation",
        
        # Medical identifiers
        "medical_record", "insurance", "doctor", "hospital", "clinic"
    ]
    
    # Check for any forbidden fields
    profile_keys = set(patient_profile.keys())
    forbidden_present = profile_keys.intersection(forbidden_fields)
    
    if forbidden_present:
        logger.error(f"🚨 ANONYMIZATION FAILURE: Forbidden PII fields detected: {forbidden_present}")
        return False
    
    # Validate required anonymized fields are present and valid
    required_fields = ["age_group", "cultural_heritage"]
    for field in required_fields:
        if field not in patient_profile or not patient_profile[field]:
            logger.warning(f"🚨 Missing required anonymized field: {field}")
            return False
    
    logger.info("✅ Profile anonymization validation PASSED")
    return True