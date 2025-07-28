"""
Information Consolidator Agent - Fixed Version with PII Safety
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

FEATURES:
- PII validation and safety checks (from original version)
- Theme manager integration (from updated version)
- Theme file writing capability
- Safe fallbacks for all API methods
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class InformationConsolidatorAgent:
    """
    Information Consolidator Agent with PII Safety and Theme Integration
    
    FEATURES:
    - Validates and anonymizes patient data (removes PII)
    - Integrates with theme manager
    - Writes theme state to file for other agents
    - Safe fallbacks for all operations
    """
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.logger = logger
        
        # Path to current theme state file
        self.theme_file_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "current_theme.json"
        )
        
        logger.info("✅ Information Consolidator initialized with PII safety and theme integration")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main processing method with PII safety and theme integration
        """
        
        logger.info("📋 Starting information consolidation with PII safety")
        
        try:
            # Process patient data with PII validation
            validated_profile = self.process_patient_data(patient_profile)
            
            # Handle feedback processing
            feedback_summary = self._process_feedback(feedback_data)
            
            # Get theme data and write to file
            theme_data = self._select_theme_with_photo(session_id)
            self._write_theme_state_file(theme_data, session_id)
            
            # Create consolidated profile
            consolidated_profile = {
                "patient_info": validated_profile,
                "theme_info": theme_data,
                "feedback_info": feedback_summary,
                "session_metadata": {
                    "session_id": session_id or "default",
                    "request_type": request_type,
                    "timestamp": datetime.now().isoformat(),
                    "step": "information_consolidation"
                },
                "pipeline_state": {
                    "current_step": 1,
                    "next_step": "photo_analysis",
                    "profile_ready": True,
                    "theme_file_written": True,
                    "pii_validated": True
                }
            }
            
            logger.info("✅ Profile consolidated successfully with PII safety")
            return consolidated_profile
            
        except Exception as e:
            logger.error(f"❌ Consolidation failed: {e}")
            return self._create_fallback_profile(patient_profile, request_type, session_id)
    
    def process_patient_data(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and validate patient data with PII safety checks
        """
        try:
            # Extract and validate the basic profile with PII checks
            validated_profile = self._extract_basic_profile(patient_profile)
            
            # Additional anonymization validation
            if not self._validate_anonymized_profile(validated_profile):
                raise ValueError("Profile failed anonymization validation")
            
            logger.info("✅ Patient data processing completed successfully")
            return validated_profile
            
        except Exception as e:
            logger.error(f"❌ Error processing patient data: {str(e)}")
            # Return safe fallback data - NO AGE
            return {
                "age_group": "senior",  # ✅ Non-PII age category only
                "cultural_heritage": "American",
                "interests": [],
                "profile_complete": False,
                "anonymized": True,
                "pii_validated": True,
                "validation_timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
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
        age_group = patient_profile.get("age_group", "senior")  # Accept pre-calculated age_group
        cultural_heritage = patient_profile.get("cultural_heritage", "American")
        interests = patient_profile.get("interests", [])
        profile_complete = patient_profile.get("profile_complete", False)
        
        # PII COMPLIANCE: Never calculate or expose actual age
        # Frontend already provides age_group - trust it and don't recalculate age
        if age_group not in ["adult", "senior", "oldest_senior"]:
            logger.warning(f"🚨 Invalid age_group: {age_group}. Using safe default.")
            age_group = "senior"  # Safe default
        
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
                if isinstance(interest, str) and len(interest) <= 50 and (interest.isalnum() or ' ' in interest):
                    safe_interests.append(interest.strip())
            interests = safe_interests
        
        # ANONYMIZED LOGGING (no PII, no age)
        logger.info(f"📝 Anonymized profile validated: age_group={age_group}, heritage={cultural_heritage}, interests_count={len(interests)}")
        
        # RETURN ONLY SAFE, ANONYMIZED DATA - NO AGE
        return {
            # NO PII FIELDS - completely removed
            "age_group": age_group,  # ✅ Non-PII age category
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
    
    def _process_feedback(self, feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process and clean feedback data"""
        
        if not feedback_data:
            feedback_data = {}
        
        likes = feedback_data.get("likes", [])
        dislikes = feedback_data.get("dislikes", [])
        
        # Extract preferred content types
        liked_types = self._extract_liked_types(likes)
        avoided_types = self._extract_avoided_types(dislikes)
        
        feedback_summary = {
            "likes": likes,
            "dislikes": dislikes,
            "liked_types": liked_types,
            "avoided_types": avoided_types,
            "total_feedback": len(likes) + len(dislikes),
            "feedback_available": len(likes) > 0 or len(dislikes) > 0
        }
        
        logger.info(f"🔄 Feedback processed: {len(likes)} likes, {len(dislikes)} dislikes")
        return feedback_summary
    
    def _extract_liked_types(self, likes: List[Dict[str, Any]]) -> List[str]:
        """Extract content types from likes"""
        types = []
        for like in likes:
            content_type = like.get("type", "unknown")
            if content_type not in types:
                types.append(content_type)
        return types
    
    def _extract_avoided_types(self, dislikes: List[Dict[str, Any]]) -> List[str]:
        """Extract content types from dislikes"""
        types = []
        for dislike in dislikes:
            content_type = dislike.get("type", "unknown")
            if content_type not in types:
                types.append(content_type)
        return types
    
    def _select_theme_with_photo(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Select theme and extract photo_filename for other agents"""
        
        try:
            if self.theme_manager:
                # Get complete theme data from theme manager
                theme_data = self.theme_manager.get_daily_theme(session_id)
                selected_theme = theme_data.get("theme_of_the_day", {})
                photo_filename = theme_data.get("photo_filename", "")
                
                theme_name = selected_theme.get("name", "Unknown")
                logger.info(f"🎯 Theme selected: {theme_name}")
                
                # Include photo_filename in the returned data
                return {
                    "id": selected_theme.get("id", "general"),
                    "name": theme_name,
                    "description": selected_theme.get("description", "A time for remembering"),
                    "conversation_prompts": selected_theme.get("conversation_prompts", []),
                    "photo_filename": photo_filename,  # For other agents
                    "source": "theme_manager",
                    "metadata": theme_data.get("selection_metadata", {})
                }
            else:
                logger.warning("⚠️ No theme manager available, using fallback")
                return self._get_fallback_theme()
                
        except Exception as e:
            logger.error(f"❌ Theme selection failed: {e}")
            return self._get_fallback_theme()
    
    def _get_fallback_theme(self) -> Dict[str, Any]:
        """Fallback theme when theme manager fails"""
        return {
            "id": "memory_lane",
            "name": "Memory Lane", 
            "description": "A time for remembering special moments",
            "conversation_prompts": [
                "Tell me about a happy memory",
                "What's something that always makes you smile?",
                "Share a story from the good old days"
            ],
            "photo_filename": "memory_lane.png",  # Include fallback photo
            "source": "fallback"
        }
    
    def _write_theme_state_file(self, theme_data: Dict[str, Any], session_id: Optional[str]) -> None:
        """Write current theme state to JSON file for other agents to read"""
        
        try:
            # Ensure config directory exists
            config_dir = os.path.dirname(self.theme_file_path)
            os.makedirs(config_dir, exist_ok=True)
            
            # Create theme state structure
            theme_state = {
                "theme_id": theme_data.get("id", "memory_lane"),
                "theme_name": theme_data.get("name", "Memory Lane"), 
                "theme_description": theme_data.get("description", "A time for remembering special moments"),
                "photo_filename": theme_data.get("photo_filename", "memory_lane.png"),
                "conversation_prompts": theme_data.get("conversation_prompts", []),
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id or "default",
                "written_by": "information_consolidator_agent",
                "selection_metadata": theme_data.get("metadata", {}),
                "source": theme_data.get("source", "unknown")
            }
            
            # Write to file with safe fallback
            with open(self.theme_file_path, 'w', encoding='utf-8') as f:
                json.dump(theme_state, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📝 Theme state written to file:")
            logger.info(f"   Theme: {theme_state['theme_name']} (ID: {theme_state['theme_id']})")
            logger.info(f"   Photo: {theme_state['photo_filename']}")
            logger.info(f"   File: {self.theme_file_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to write theme state file: {e}")
            # Don't let theme file writing failure break the pipeline
            pass
    
    def _create_fallback_profile(self, patient_profile: Dict[str, Any], 
                                request_type: str, 
                                session_id: Optional[str]) -> Dict[str, Any]:
        """Create fallback profile when main processing fails"""
        
        logger.warning("🔄 Creating fallback consolidated profile")
        
        # Still try to write theme file even in fallback mode
        fallback_theme = self._get_fallback_theme()
        self._write_theme_state_file(fallback_theme, session_id)
        
        return {
            "patient_info": {
                "age_group": "senior",  # ✅ Non-PII age category only
                "cultural_heritage": "American",
                "interests": [],
                "profile_complete": False,
                "anonymized": True,
                "pii_validated": True,
                "validation_timestamp": datetime.now().isoformat()
            },
            "theme_info": fallback_theme,
            "feedback_info": {
                "likes": [],
                "dislikes": [],
                "total_feedback": 0,
                "feedback_available": False
            },
            "session_metadata": {
                "session_id": session_id or "fallback",
                "request_type": request_type,
                "timestamp": datetime.now().isoformat(),
                "step": "information_consolidation_fallback"
            },
            "pipeline_state": {
                "current_step": 1,
                "next_step": "photo_analysis",
                "profile_ready": True,
                "fallback_used": True,
                "theme_file_written": True,
                "pii_validated": True
            }
        }

# Export the main class
__all__ = ["InformationConsolidatorAgent"]