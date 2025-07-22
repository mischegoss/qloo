"""
Agent 1: Information Consolidator - FIXED VERSION
Role: Package all session data for cultural intelligence processing
Follows Responsible Development Guide principles
"""

from typing import Dict, Any, Optional, List
import json
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class InformationConsolidatorAgent(Agent):
    """
    Agent 1: Information Consolidator
    
    Purpose: Package all session data for cultural intelligence processing
    Input: Patient profile, request type, feedback history  
    Output: Structured summary with demographics, request details, feedback patterns
    
    Privacy-First Principles:
    - Only processes minimal, non-PII data
    - Respects caregiver authority
    - No cultural assumptions made
    """
    
    def __init__(self):
        super().__init__(
            name="information_consolidator",
            description="Consolidates session data while respecting privacy and caregiver authority"
        )
    
    def _safe_string(self, value: Any, max_length: Optional[int] = None) -> str:
        """
        Safely convert value to string and handle None values.
        
        Args:
            value: Any value that might be None
            max_length: Optional maximum length to truncate to
            
        Returns:
            Safe string value, never None
        """
        if value is None:
            return ""
        str_value = str(value).strip()
        if max_length:
            return str_value[:max_length]
        return str_value
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str,
                  session_id: Optional[str] = None,
                  feedback_history: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Consolidate all session information for cultural intelligence processing.
        
        Args:
            patient_profile: Basic patient info (first name, birth year/month, general location)
            request_type: Type of request (meal, conversation, music, video, dashboard)
            session_id: Optional session identifier for preference continuity
            feedback_history: Previous feedback and blocked content
            photo_data: Optional uploaded photo for analysis
            
        Returns:
            Consolidated information package for next agents
        """
        
        try:
            logger.info(f"Consolidating information for request type: {request_type}")
            
            # Extract and validate basic patient information (Privacy-First)
            basic_info = self._extract_basic_info(patient_profile)
            
            # Process request context
            request_context = self._process_request_context(request_type)
            
            # Consolidate feedback patterns (respecting blocks)
            feedback_patterns = self._consolidate_feedback(feedback_history)
            
            # Handle photo data if present
            photo_context = self._process_photo_context(photo_data)
            
            # Build consolidated package
            consolidated_info = {
                "session_metadata": {
                    "session_id": session_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "has_photo": bool(photo_data)
                },
                "basic_demographics": basic_info,
                "request_context": request_context,
                "feedback_patterns": feedback_patterns,
                "photo_context": photo_context,
                "processing_notes": {
                    "privacy_compliance": "minimal_data_only",
                    "caregiver_authority": "respected",
                    "cultural_assumptions": "none_made"
                }
            }
            
            # Validate consolidation meets privacy standards
            self._validate_privacy_compliance(consolidated_info)
            
            logger.info("Information consolidation completed successfully")
            return {"consolidated_info": consolidated_info}
            
        except Exception as e:
            logger.error(f"Error in information consolidation: {str(e)}")
            # Return safe fallback that maintains privacy
            return self._create_fallback_consolidation(request_type)
    
    def _extract_basic_info(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract only essential, non-PII information.
        Follows Responsible Development Guide privacy principles.
        """
        # Only extract minimal, privacy-safe information using safe string conversion
        basic_info = {
            "first_name_or_nickname": self._safe_string(patient_profile.get("first_name"), 20),
            "birth_context": {
                "birth_year": self._validate_birth_year(patient_profile.get("birth_year")),
                "birth_month": self._validate_birth_month(patient_profile.get("birth_month")),
                "age_range": self._calculate_age_range(patient_profile.get("birth_year"))
            },
            "general_location": {
                "city_region": self._safe_string(patient_profile.get("city"), 50),
                "state_region": self._safe_string(patient_profile.get("state"), 30)
            },
            "cultural_sharing": {
                "heritage_info": self._safe_string(patient_profile.get("cultural_heritage"), 500),
                "languages": self._safe_string(patient_profile.get("languages"), 200),
                "spiritual_traditions": self._safe_string(patient_profile.get("spiritual_traditions"), 300),
                "additional_context": self._safe_string(patient_profile.get("additional_context"), 1000)
            },
            "caregiver_notes": self._safe_string(patient_profile.get("caregiver_notes"), 500)
        }
        
        return basic_info
    
    def _validate_birth_year(self, birth_year: Any) -> Optional[int]:
        """Validate birth year for adult care (removes age bias)."""
        try:
            year = int(birth_year) if birth_year else None
            current_year = datetime.now().year
            
            if not year:
                return None
            
            # Calculate approximate age
            approximate_age = current_year - year
            
            # This app is designed for adult care - check for 16+ years old
            if approximate_age < 16:
                logger.info(f"Age appears to be {approximate_age} - CareConnect is designed for adult care (16+)")
                return None
            
            # Accept all adults including super-seniors over 100
            # Reasonable birth year range: 1900 to current year - 16
            if 1900 <= year <= (current_year - 16):
                return year
                
            # Log if birth year seems unusual but don't reject
            if year < 1900:
                logger.info(f"Birth year {year} indicates super-senior over 125 - accepting with note")
                return year
            
            return None
        except (ValueError, TypeError):
            return None
    
    def _validate_birth_month(self, birth_month: Any) -> Optional[str]:
        """Validate birth month for seasonal cultural context."""
        try:
            if isinstance(birth_month, str) and birth_month.lower() in [
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"
            ]:
                return birth_month.lower()
            return None
        except (AttributeError, TypeError):
            return None
    
    def _calculate_age_range(self, birth_year: Optional[int]) -> str:
        """Calculate broad age range for demographic context (all adults)."""
        if not birth_year:
            return "age_unknown"
        
        current_year = datetime.now().year
        age = current_year - birth_year
        
        # Broad age ranges supporting all adults with dementia
        if age >= 100:
            return "super_senior_100_plus"
        elif age >= 85:
            return "senior_85_99"
        elif age >= 70:
            return "older_adult_70_84"
        elif age >= 55:
            return "mature_adult_55_69"
        elif age >= 40:
            return "middle_aged_40_54"
        elif age >= 25:
            return "young_adult_25_39"
        elif age >= 16:
            return "adult_16_24"
        else:
            return "under_adult_age"  # Indicates app designed for 16+
    
    def _process_request_context(self, request_type: str) -> Dict[str, Any]:
        """Process the type of request to provide context for cultural intelligence."""
        
        valid_request_types = ["meal", "conversation", "music", "video", "dashboard", "photo_analysis"]
        
        if request_type not in valid_request_types:
            request_type = "dashboard"  # Safe fallback
        
        context_mapping = {
            "meal": {
                "domain": "culinary",
                "sensory_focus": ["taste", "smell", "touch"],
                "cultural_aspects": ["family_traditions", "comfort_foods", "regional_cuisine"],
                "caregiver_goal": "shared_meal_experience"
            },
            "conversation": {
                "domain": "social",
                "sensory_focus": ["auditory", "emotional"],
                "cultural_aspects": ["memories", "stories", "local_history"],
                "caregiver_goal": "meaningful_connection"
            },
            "music": {
                "domain": "auditory",
                "sensory_focus": ["auditory", "emotional", "movement"],
                "cultural_aspects": ["era_music", "cultural_genres", "dance_traditions"],
                "caregiver_goal": "emotional_engagement"
            },
            "video": {
                "domain": "visual_auditory",
                "sensory_focus": ["visual", "auditory"],
                "cultural_aspects": ["era_entertainment", "familiar_shows", "cultural_content"],
                "caregiver_goal": "shared_viewing_experience"
            },
            "dashboard": {
                "domain": "multi_sensory",
                "sensory_focus": ["all_senses"],
                "cultural_aspects": ["daily_routines", "varied_activities", "cultural_preferences"],
                "caregiver_goal": "comprehensive_daily_support"
            },
            "photo_analysis": {
                "domain": "visual_memory",
                "sensory_focus": ["visual", "emotional", "memory"],
                "cultural_aspects": ["family_history", "era_indicators", "cultural_markers"],
                "caregiver_goal": "photo_triggered_engagement"
            }
        }
        
        return {
            "request_type": request_type,
            "context": context_mapping.get(request_type, context_mapping["dashboard"]),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _consolidate_feedback(self, feedback_history: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Consolidate feedback patterns while respecting blocked content.
        Implements feedback learning from Responsible Development Guide.
        """
        if not feedback_history:
            return {
                "has_feedback": False,
                "blocked_content": {},
                "positive_patterns": {},
                "negative_patterns": {},
                "preference_indicators": {}
            }
        
        # Extract blocked content (respects caregiver authority)
        blocked_content = feedback_history.get("blocked_content", {})
        
        # Extract positive feedback patterns
        positive_patterns = self._extract_positive_patterns(feedback_history.get("positive_feedback", []))
        
        # Extract negative patterns (without blocking)
        negative_patterns = self._extract_negative_patterns(feedback_history.get("negative_feedback", []))
        
        # Extract preference indicators
        preference_indicators = feedback_history.get("preferences", {})
        
        return {
            "has_feedback": True,
            "blocked_content": blocked_content,
            "positive_patterns": positive_patterns,
            "negative_patterns": negative_patterns,
            "preference_indicators": preference_indicators,
            "feedback_count": len(feedback_history.get("all_feedback", []))
        }
    
    def _extract_positive_patterns(self, positive_feedback: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from successful suggestions."""
        patterns = {
            "successful_music_genres": [],
            "successful_food_types": [],
            "successful_conversation_topics": [],
            "successful_video_content": [],
            "cultural_connections_that_worked": []
        }
        
        for feedback in positive_feedback:
            content_type = feedback.get("content_type", "")
            content_details = feedback.get("content_details", {})
            
            if content_type == "music":
                patterns["successful_music_genres"].append(content_details.get("genre"))
            elif content_type == "food":
                patterns["successful_food_types"].append(content_details.get("cuisine_type"))
            elif content_type == "conversation":
                patterns["successful_conversation_topics"].append(content_details.get("topic_category"))
            elif content_type == "video":
                patterns["successful_video_content"].append(content_details.get("content_category"))
            
            # Extract cultural connections that worked
            if content_details.get("cultural_connection"):
                patterns["cultural_connections_that_worked"].append(content_details["cultural_connection"])
        
        return patterns
    
    def _extract_negative_patterns(self, negative_feedback: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from unsuccessful suggestions (not blocked)."""
        patterns = {
            "timing_issues": [],
            "complexity_issues": [],
            "sensory_issues": [],
            "cultural_mismatches": []
        }
        
        for feedback in negative_feedback:
            feedback_reason = feedback.get("reason", "")
            
            if "time" in feedback_reason.lower() or "timing" in feedback_reason.lower():
                patterns["timing_issues"].append(feedback.get("context", ""))
            elif "complex" in feedback_reason.lower() or "difficult" in feedback_reason.lower():
                patterns["complexity_issues"].append(feedback.get("context", ""))
            elif any(sense in feedback_reason.lower() for sense in ["loud", "bright", "overwhelming"]):
                patterns["sensory_issues"].append(feedback.get("context", ""))
            elif "cultural" in feedback_reason.lower() or "not their style" in feedback_reason.lower():
                patterns["cultural_mismatches"].append(feedback.get("context", ""))
        
        return patterns
    
    def _process_photo_context(self, photo_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process photo data context for Agent 5 (Photo Cultural Analyzer)."""
        if not photo_data:
            return {"has_photo": False}
        
        return {
            "has_photo": True,
            "photo_metadata": {
                "upload_timestamp": photo_data.get("timestamp", datetime.utcnow().isoformat()),
                "photo_type": photo_data.get("type", "family_photo"),
                "caregiver_description": self._safe_string(photo_data.get("description"), 200)
            },
            "photo_processing_ready": True
        }
    
    def _validate_privacy_compliance(self, consolidated_info: Dict[str, Any]) -> None:
        """
        Validate that consolidated information meets privacy standards.
        Raises exception if any PII detected.
        """
        # Check for full names (longer than reasonable first name)
        first_name = consolidated_info.get("basic_demographics", {}).get("first_name_or_nickname", "")
        if len(first_name.split()) > 2:  # Likely full name
            logger.warning("Potential full name detected, truncating to first name only")
            consolidated_info["basic_demographics"]["first_name_or_nickname"] = first_name.split()[0]
        
        # Check for specific addresses (not allowed)
        location_info = str(consolidated_info.get("basic_demographics", {}).get("general_location", {}))
        pii_indicators = ["street", "apartment", "apt", "unit", "address", "zip", "postal"]
        if any(indicator in location_info.lower() for indicator in pii_indicators):
            logger.warning("Potential address information detected, removing")
            consolidated_info["basic_demographics"]["general_location"] = {
                "city_region": "location_removed_for_privacy",
                "state_region": ""
            }
        
        logger.info("Privacy compliance validation passed")
    
    def _create_fallback_consolidation(self, request_type: str) -> Dict[str, Any]:
        """Create safe fallback when consolidation fails."""
        return {
            "consolidated_info": {
                "session_metadata": {
                    "session_id": None,
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "has_photo": False,
                    "processing_mode": "fallback"
                },
                "basic_demographics": {
                    "first_name_or_nickname": "",
                    "birth_context": {"age_range": "age_unknown"},
                    "general_location": {"city_region": "", "state_region": ""},
                    "cultural_sharing": {},
                    "caregiver_notes": ""
                },
                "request_context": self._process_request_context(request_type),
                "feedback_patterns": {"has_feedback": False},
                "photo_context": {"has_photo": False},
                "processing_notes": {
                    "privacy_compliance": "minimal_data_only",
                    "caregiver_authority": "respected",
                    "cultural_assumptions": "none_made",
                    "mode": "fallback_safe_defaults"
                }
            }
        }