"""
Agent 1: Information Consolidator - NULL-SAFE VERSION
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

Fixed to handle None/null values safely from JSON input
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class InformationConsolidatorAgent(Agent):
    """
    Agent 1: Information Consolidator - NULL-SAFE
    
    Fixed to handle None/null values from JSON input safely
    """
    
    def __init__(self):
        super().__init__(
            name="information_consolidator_safe",
            description="Consolidates patient information with null-safe processing"
        )
        logger.info("Information Consolidator Agent initialized in null-safe mode")
    
    def _safe_string(self, value: Any, default: str = "") -> str:
        """Safely convert any value to string, handling None values."""
        if value is None:
            return default
        return str(value).strip()
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  feedback_data: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None,
                  session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Consolidate patient information using null-safe extraction.
        """
        
        try:
            logger.info(f"Consolidating information for {request_type} request")
            
            # STEP 1: Extract cultural heritage safely
            cultural_heritage = self._extract_cultural_heritage(patient_profile)
            
            # STEP 2: Calculate age from birth_year safely
            age_info = self._extract_age_information(patient_profile)
            
            # STEP 3: Extract location context safely
            location = self._extract_location_context(patient_profile)
            
            # STEP 4: Parse preferences safely
            preferences = self._parse_preferences(patient_profile)
            
            # STEP 5: Process feedback patterns
            feedback_patterns = self._process_feedback_patterns(feedback_data or {})
            
            # STEP 6: Process photo context
            photo_context = self._process_photo_context(photo_data)
            
            # STEP 7: Build consolidated information safely
            consolidated_info = {
                "patient_profile": {
                    "cultural_heritage": cultural_heritage,
                    "birth_year": patient_profile.get("birth_year"),
                    "age": age_info.get("current_age"),
                    "age_demographic": age_info.get("age_demographic"),
                    "location": location,
                    "preferences": preferences,
                    "additional_context": self._safe_string(patient_profile.get("additional_context")),
                    "caregiver_notes": self._safe_string(patient_profile.get("caregiver_notes"))
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
            
            logger.info(f"✅ Information consolidated: {cultural_heritage} heritage, {age_info.get('current_age')} years old")
            
            return {"consolidated_info": consolidated_info}
            
        except Exception as e:
            logger.error(f"❌ Information consolidation failed: {e}")
            return self._create_fallback_consolidation(patient_profile, request_type)
    
    def _extract_cultural_heritage(self, patient_profile: Dict[str, Any]) -> str:
        """Extract cultural heritage safely from patient profile."""
        
        heritage = self._safe_string(patient_profile.get("cultural_heritage"))
        
        if heritage:
            logger.info(f"Cultural heritage extracted: {heritage}")
            return heritage
        
        # Fallback to American if not specified
        logger.warning("No cultural heritage specified, defaulting to American")
        return "American"
    
    def _extract_age_information(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate age information safely from birth_year or direct age."""
        
        birth_year = patient_profile.get("birth_year")
        current_year = 2024
        
        if birth_year and isinstance(birth_year, (int, float)):
            current_age = current_year - int(birth_year)
            
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
        if age and isinstance(age, (int, float)):
            age = int(age)
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
        """Extract and combine location information safely."""
        
        # FIXED: Handle None values properly using _safe_string
        city = self._safe_string(patient_profile.get("city"))
        state = self._safe_string(patient_profile.get("state"))
        
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
        """Parse preferences safely from additional_context and caregiver_notes."""
        
        preferences = []
        
        # Parse additional_context safely
        additional_context = self._safe_string(patient_profile.get("additional_context")).lower()
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
        
        # Parse caregiver_notes safely
        caregiver_notes = self._safe_string(patient_profile.get("caregiver_notes")).lower()
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
        """Process photo data context safely for Agent 5."""
        
        if not photo_data:
            return {"has_photo": False}
        
        return {
            "has_photo": True,
            "photo_metadata": {
                "upload_timestamp": photo_data.get("timestamp", datetime.now().isoformat()),
                "photo_type": photo_data.get("type", "family_photo"),
                "caregiver_description": self._safe_string(photo_data.get("description"))[:200]
            },
            "photo_processing_ready": True
        }
    
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
                    "additional_context": self._safe_string(patient_profile.get("additional_context")),
                    "caregiver_notes": self._safe_string(patient_profile.get("caregiver_notes"))
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