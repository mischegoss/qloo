"""
Agent 1: Information Consolidator - SIMPLIFIED VERSION
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

Simplified to extract cultural heritage directly from input, calculate age from birth_year,
and parse additional_context for preferences. No database lookups - just in-memory processing.
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class InformationConsolidatorAgent(Agent):
    """
    Agent 1: Information Consolidator - SIMPLIFIED
    
    SIMPLIFICATIONS:
    - Extract cultural heritage directly from input
    - Calculate age from birth_year 
    - Parse additional_context and caregiver_notes for preferences
    - No database lookups - just in-memory processing
    - Focus on the curl input structure format
    """
    
    def __init__(self):
        super().__init__(
            name="information_consolidator_simplified",
            description="Consolidates patient information with direct extraction approach"
        )
        logger.info("Information Consolidator Agent initialized in simplified mode")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  feedback_data: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None,
                  session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Consolidate patient information using direct extraction.
        
        Args:
            patient_profile: Direct patient information from request
            request_type: Type of request (dashboard, activity, etc.)
            feedback_data: Optional feedback history
            photo_data: Optional photo data
            session_id: Optional session identifier
            
        Returns:
            Consolidated information package
        """
        
        try:
            logger.info(f"Consolidating information for {request_type} request")
            
            # STEP 1: Extract cultural heritage directly
            cultural_heritage = self._extract_cultural_heritage(patient_profile)
            
            # STEP 2: Calculate age from birth_year
            age_info = self._extract_age_information(patient_profile)
            
            # STEP 3: Extract location context
            location = self._extract_location_context(patient_profile)
            
            # STEP 4: Parse preferences from additional context
            preferences = self._parse_preferences(patient_profile)
            
            # STEP 5: Process feedback patterns
            feedback_patterns = self._process_feedback_patterns(feedback_data or {})
            
            # STEP 6: Process photo context
            photo_context = self._process_photo_context(photo_data)
            
            # STEP 7: Build consolidated information
            consolidated_info = {
                "patient_profile": {
                    "cultural_heritage": cultural_heritage,
                    "birth_year": patient_profile.get("birth_year"),
                    "age": age_info.get("current_age"),
                    "age_demographic": age_info.get("age_demographic"),
                    "location": location,
                    "preferences": preferences,
                    "additional_context": patient_profile.get("additional_context", ""),
                    "caregiver_notes": patient_profile.get("caregiver_notes", "")
                },
                "request_context": {
                    "request_type": request_type,
                    "session_id": session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "timestamp": datetime.now().isoformat()
                },
                "feedback_patterns": feedback_patterns,
                "photo_context": photo_context,
                "session_metadata": {
                    "data_sources": ["direct_input"],
                    "cultural_heritage_source": "patient_profile",
                    "age_calculation_method": "birth_year" if patient_profile.get("birth_year") else "direct",
                    "preferences_source": "additional_context_parsing",
                    "consolidation_timestamp": datetime.now().isoformat()
                }
            }
            
            # STEP 8: Validate privacy compliance
            self._validate_privacy_compliance(consolidated_info)
            
            logger.info(f"Information consolidated: {cultural_heritage} heritage, {age_info.get('current_age')} years old")
            
            return {"consolidated_info": consolidated_info}
            
        except Exception as e:
            logger.error(f"❌ Information consolidation failed: {e}")
            return self._create_fallback_consolidation(patient_profile, request_type)
    
    def _extract_cultural_heritage(self, patient_profile: Dict[str, Any]) -> str:
        """Extract cultural heritage directly from patient profile."""
        
        heritage = patient_profile.get("cultural_heritage")
        
        if heritage:
            heritage_clean = heritage.strip()
            logger.info(f"Cultural heritage extracted: {heritage_clean}")
            return heritage_clean
        
        # Fallback to American if not specified
        logger.warning("No cultural heritage specified, defaulting to American")
        return "American"
    
    def _extract_age_information(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate age information from birth_year or direct age."""
        
        birth_year = patient_profile.get("birth_year")
        current_year = 2024
        
        if birth_year:
            current_age = current_year - birth_year
            
            # Map to Qloo age demographics
            if current_age <= 35:
                age_demographic = "35_and_younger"
            elif current_age <= 55:
                age_demographic = "36_to_55"
            else:
                age_demographic = "55_and_older"
            
            logger.info(f"Age calculated from birth year {birth_year}: {current_age} → {age_demographic}")
            
            return {
                "birth_year": birth_year,
                "current_age": current_age,
                "age_demographic": age_demographic,
                "calculation_method": "birth_year"
            }
        
        # Try direct age
        age = patient_profile.get("age")
        if age:
            if age <= 35:
                age_demographic = "35_and_younger"
            elif age <= 55:
                age_demographic = "36_to_55"
            else:
                age_demographic = "55_and_older"
            
            return {
                "current_age": age,
                "age_demographic": age_demographic,
                "calculation_method": "direct_age"
            }
        
        # Default fallback
        logger.warning("No age information found, defaulting to 55_and_older")
        return {
            "current_age": 75,  # Conservative estimate for dementia care
            "age_demographic": "55_and_older",
            "calculation_method": "default_fallback"
        }
    
    def _extract_location_context(self, patient_profile: Dict[str, Any]) -> str:
        """Extract and combine location information."""
        
        city = patient_profile.get("city", "").strip()
        state = patient_profile.get("state", "").strip()
        
        if city and state:
            location = f"{city}, {state}"
        elif city:
            location = city
        elif state:
            location = state
        else:
            location = "United States"  # Default
        
        logger.info(f"Location context: {location}")
        return location
    
    def _parse_preferences(self, patient_profile: Dict[str, Any]) -> List[str]:
        """Parse preferences from additional_context and caregiver_notes."""
        
        preferences = []
        
        # Parse additional_context
        additional_context = patient_profile.get("additional_context", "").lower()
        if additional_context:
            if "music" in additional_context:
                preferences.append("music")
            if "cook" in additional_context:
                preferences.append("cooking")
            if "family" in additional_context:
                preferences.append("family activities")
            if "read" in additional_context:
                preferences.append("reading")
            if "garden" in additional_context:
                preferences.append("gardening")
        
        # Parse caregiver_notes
        caregiver_notes = patient_profile.get("caregiver_notes", "").lower()
        if caregiver_notes:
            if "music" in caregiver_notes:
                preferences.append("music")
            if "cook" in caregiver_notes:
                preferences.append("cooking")
            if "family" in caregiver_notes:
                preferences.append("family activities")
        
        # Remove duplicates
        preferences = list(set(preferences))
        
        logger.info(f"Parsed preferences: {preferences}")
        return preferences
    
    def _process_feedback_patterns(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process feedback data into patterns for future agents."""
        
        if not feedback_data:
            return {
                "has_feedback": False,
                "blocked_content": {},
                "positive_patterns": [],
                "negative_patterns": []
            }
        
        # Extract blocked content
        blocked_content = feedback_data.get("blocked_content", {})
        
        # Extract feedback history
        feedback_history = feedback_data.get("feedback_history", [])
        
        positive_patterns = []
        negative_patterns = []
        
        for feedback in feedback_history:
            if feedback.get("rating") == "positive":
                positive_patterns.append(feedback.get("content_type", "unknown"))
            elif feedback.get("rating") == "negative":
                negative_patterns.append(feedback.get("content_type", "unknown"))
        
        return {
            "has_feedback": True,
            "blocked_content": blocked_content,
            "positive_patterns": list(set(positive_patterns)),
            "negative_patterns": list(set(negative_patterns)),
            "feedback_count": len(feedback_history)
        }
    
    def _process_photo_context(self, photo_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process photo data context for Agent 5."""
        
        if not photo_data:
            return {"has_photo": False}
        
        return {
            "has_photo": True,
            "photo_metadata": {
                "upload_timestamp": photo_data.get("timestamp", datetime.now().isoformat()),
                "photo_type": photo_data.get("type", "family_photo"),
                "caregiver_description": photo_data.get("description", "")[:200]  # Limit length
            },
            "photo_processing_ready": True
        }
    
    def _validate_privacy_compliance(self, consolidated_info: Dict[str, Any]) -> None:
        """Validate that consolidated information meets privacy standards."""
        
        # Check for any personally identifiable information that shouldn't be there
        patient_profile = consolidated_info.get("patient_profile", {})
        
        # These fields should not contain PII
        restricted_fields = ["additional_context", "caregiver_notes"]
        
        for field in restricted_fields:
            content = patient_profile.get(field, "")
            if content:
                # Basic check for potential PII patterns (names, addresses, etc.)
                content_lower = content.lower()
                if any(word in content_lower for word in ["ssn", "social security", "phone", "address"]):
                    logger.warning(f"Potential PII detected in {field}")
        
        logger.info("Privacy compliance validation completed")
    
    def _create_fallback_consolidation(self, 
                                     patient_profile: Dict[str, Any], 
                                     request_type: str) -> Dict[str, Any]:
        """Create fallback consolidation when extraction fails."""
        
        logger.warning("Creating fallback consolidation")
        
        return {
            "consolidated_info": {
                "patient_profile": {
                    "cultural_heritage": "American",
                    "age": 75,
                    "age_demographic": "55_and_older",
                    "location": "United States",
                    "preferences": ["family activities"],
                    "additional_context": patient_profile.get("additional_context", ""),
                    "caregiver_notes": patient_profile.get("caregiver_notes", "")
                },
                "request_context": {
                    "request_type": request_type,
                    "session_id": f"fallback_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "timestamp": datetime.now().isoformat()
                },
                "feedback_patterns": {"has_feedback": False},
                "photo_context": {"has_photo": False},
                "session_metadata": {
                    "data_sources": ["fallback"],
                    "consolidation_timestamp": datetime.now().isoformat()
                }
            }
        }

# Test function
def test_information_consolidator():
    """Test the simplified information consolidator."""
    
    agent = InformationConsolidatorAgent()
    
    # Test data matching the curl example
    test_patient_profile = {
        "cultural_heritage": "Italian-American",
        "birth_year": 1945,
        "city": "Brooklyn",
        "state": "New York",
        "additional_context": "Loves music and cooking"
    }
    
    # Run the test
    import asyncio
    
    async def run_test():
        result = await agent.run(
            patient_profile=test_patient_profile,
            request_type="dashboard"
        )
        
        consolidated = result.get("consolidated_info", {})
        patient = consolidated.get("patient_profile", {})
        
        print("Information Consolidator Test Results:")
        print(f"Heritage: {patient.get('cultural_heritage')}")
        print(f"Age: {patient.get('age')} ({patient.get('age_demographic')})")
        print(f"Location: {patient.get('location')}")
        print(f"Preferences: {patient.get('preferences')}")
        
        return result
    
    return asyncio.run(run_test())

if __name__ == "__main__":
    test_information_consolidator()