"""
Enhanced Information Consolidator Agent - Location Prioritization Added
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

ENHANCED: Now prioritizes hometown over location for Places analysis
- Extracts and prioritizes hometown > location > city/state
- Creates location_info structure for downstream agents
- Maintains all existing functionality
- Supports rural area identification
"""

import logging
import json
import os
from datetime import datetime, date
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Import theme manager for enhanced theme-aware functionality
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Information Consolidator: theme_manager imported successfully")
except ImportError as e:
    logger.error(f"❌ Information Consolidator: Failed to import theme_manager: {e}")
    theme_manager = None

class InformationConsolidatorAgent:
    """
    Agent 1: Enhanced Information Consolidator with Location Prioritization
    
    ENHANCED FUNCTIONALITY:
    - Prioritizes hometown over location for place-based conversations
    - Creates structured location_info for downstream agents
    - Maintains backward compatibility with existing profiles
    - Supports rural area detection and handling
    """
    
    def __init__(self):
        logger.info("✅ Information Consolidator initialized with LOCATION PRIORITIZATION")
    
    async def run(self, 
                  patient_profile: Dict[str, Any], 
                  request_type: str, 
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Enhanced consolidation with location prioritization
        
        Args:
            patient_profile: Patient profile data
            request_type: Type of request (dashboard, etc.)
            session_id: Session identifier
            feedback_data: Feedback history (optional)
            
        Returns:
            Consolidated information with prioritized location data
        """
        
        logger.info("📋 Agent 1: Starting enhanced information consolidation with location prioritization")
        
        try:
            # Core consolidation
            demographics = self._extract_demographics(patient_profile)
            heritage_info = self._extract_heritage_info(patient_profile)
            preferences_info = self._extract_preferences_info(feedback_data)
            
            # ENHANCED: Location prioritization
            location_info = self._extract_location_info(patient_profile)
            
            # Theme selection with enhanced metadata
            daily_theme = self._select_daily_theme()
            
            # Build consolidated information structure
            consolidated_info = {
                "patient_profile": patient_profile,
                "session_metadata": {
                    "session_id": session_id,
                    "request_type": request_type,
                    "timestamp": datetime.now().isoformat(),
                    "processing_agent": "information_consolidator"
                },
                "demographics": demographics,
                "heritage_info": heritage_info,
                "preferences_info": preferences_info,
                "location_info": location_info,  # ENHANCED: New location prioritization
                "daily_theme": daily_theme,
                "feedback_history": self._extract_feedback_history(feedback_data),
                "processing_metadata": {
                    "theme_manager_available": theme_manager is not None,
                    "location_prioritization": "hometown_preferred",
                    "rural_area_support": True,
                    "consolidated_successfully": True
                }
            }
            
            logger.info(f"✅ Agent 1: Information consolidated successfully")
            logger.info(f"👤 Patient: {demographics.get('first_name', 'Unknown')}")
            logger.info(f"🏠 Primary location: {location_info.get('primary_location', 'Unknown')} ({location_info.get('location_type', 'unknown')})")
            logger.info(f"🎯 Daily theme: {daily_theme.get('theme', {}).get('name', 'Unknown')}")
            
            return consolidated_info
            
        except Exception as e:
            logger.error(f"❌ Agent 1 failed: {e}")
            return self._create_fallback_consolidated_info(patient_profile, request_type, session_id)
    
    def _extract_location_info(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCED: Extract and prioritize location information
        
        Priority order:
        1. hometown (NEW - preferred for place-based conversations)
        2. location (current location)
        3. city + state (legacy support)
        
        Args:
            patient_profile: Patient profile data
            
        Returns:
            Structured location information with prioritization
        """
        
        # Extract all location fields
        hometown = patient_profile.get("hometown", "").strip()
        location = patient_profile.get("location", "").strip()
        city = patient_profile.get("city", "").strip()
        state = patient_profile.get("state", "").strip()
        
        # Build legacy location from city/state if needed
        legacy_location = f"{city}, {state}".strip(", ") if city or state else ""
        
        # Prioritize hometown > location > legacy_location
        primary_location = hometown or location or legacy_location
        
        # Determine location type for conversation context
        if hometown:
            location_type = "hometown"
        elif location:
            location_type = "current_location"
        elif legacy_location:
            location_type = "legacy_location"
        else:
            location_type = "unknown"
        
        # Detect potential rural areas (simple heuristics)
        rural_indicators = self._detect_rural_area(primary_location)
        
        location_info = {
            "primary_location": primary_location,
            "location_type": location_type,
            "hometown": hometown,
            "current_location": location,
            "city": city,
            "state": state,
            "legacy_location": legacy_location,
            "location_available": bool(primary_location),
            "rural_indicators": rural_indicators,
            "location_prioritization": {
                "hometown_available": bool(hometown),
                "current_location_available": bool(location),
                "legacy_data_available": bool(legacy_location),
                "priority_used": location_type
            }
        }
        
        logger.info(f"🏠 Location prioritization: {primary_location} ({location_type})")
        if rural_indicators["likely_rural"]:
            logger.info(f"🏡 Rural area detected: {rural_indicators['reason']}")
        
        return location_info
    
    def _detect_rural_area(self, location: str) -> Dict[str, Any]:
        """
        Simple heuristics to detect potential rural areas
        
        Args:
            location: Primary location string
            
        Returns:
            Rural detection analysis
        """
        
        if not location:
            return {"likely_rural": False, "reason": "no_location"}
        
        location_lower = location.lower()
        
        # Rural indicators
        rural_keywords = [
            "rural", "farm", "county", "township", "village", 
            "hollow", "creek", "ridge", "valley", "mountain",
            "route", "highway", "rd", "road only"
        ]
        
        # Urban indicators (counter-indicators)
        urban_keywords = [
            "new york", "brooklyn", "manhattan", "queens", "bronx",
            "los angeles", "chicago", "houston", "philadelphia",
            "city", "downtown", "metro", "borough"
        ]
        
        # Check for rural indicators
        rural_matches = [keyword for keyword in rural_keywords if keyword in location_lower]
        urban_matches = [keyword for keyword in urban_keywords if keyword in location_lower]
        
        # Simple population-based heuristics (very basic)
        small_town_indicators = [
            len(location.split()) == 1 and len(location) < 15,  # Single short word
            "population" in location_lower,
            any(size in location_lower for size in ["small", "tiny", "little"])
        ]
        
        likely_rural = False
        reason = "urban_area"
        
        if rural_matches and not urban_matches:
            likely_rural = True
            reason = f"rural_keywords: {', '.join(rural_matches)}"
        elif any(small_town_indicators) and not urban_matches:
            likely_rural = True
            reason = "small_town_indicators"
        elif not urban_matches and len(location.split(",")) <= 2:
            # Simple location without major city indicators
            likely_rural = True
            reason = "simple_location_format"
        
        return {
            "likely_rural": likely_rural,
            "reason": reason,
            "rural_keywords_found": rural_matches,
            "urban_keywords_found": urban_matches,
            "location_complexity": len(location.split(","))
        }
    
    def _extract_demographics(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract demographic information (unchanged)"""
        first_name = patient_profile.get("first_name", "")
        birth_year = patient_profile.get("birth_year")
        birth_month = patient_profile.get("birth_month", "")
        
        # Calculate age if birth year available
        age = None
        age_range = "unknown"
        if birth_year:
            try:
                current_year = datetime.now().year
                age = current_year - birth_year
                
                if age >= 55:
                    age_range = "55_and_older"
                elif age >= 36:
                    age_range = "36_to_55"
                else:
                    age_range = "35_and_younger"
            except (ValueError, TypeError):
                logger.warning(f"Invalid birth year: {birth_year}")
        
        return {
            "first_name": first_name,
            "birth_year": birth_year,
            "birth_month": birth_month,
            "age": age,
            "age_range": age_range,
            "demographics_available": bool(first_name or birth_year)
        }
    
    def _extract_heritage_info(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cultural heritage information (unchanged)"""
        cultural_heritage = patient_profile.get("cultural_heritage", "")
        additional_context = patient_profile.get("additional_context", "")
        
        # Parse heritage if available
        heritage_tags = []
        if cultural_heritage:
            # Simple parsing - split on common separators
            heritage_parts = cultural_heritage.replace("-", " ").replace("/", " ").split()
            heritage_tags = [part.strip() for part in heritage_parts if len(part.strip()) > 2]
        
        return {
            "cultural_heritage": cultural_heritage,
            "additional_context": additional_context,
            "heritage_tags": heritage_tags,
            "heritage_available": bool(cultural_heritage)
        }
    
    def _extract_preferences_info(self, feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract preferences from feedback data (unchanged)"""
        if not feedback_data:
            return {
                "explicit_preferences": {"tags": []},
                "learned_preferences": {},
                "blocked_content": [],
                "preferences_available": False
            }
        
        # Extract explicit preferences
        explicit_preferences = {"tags": feedback_data.get("preference_tags", [])}
        
        # Extract blocked content
        blocked_content = feedback_data.get("blocked_items", [])
        
        # Extract learned preferences
        learned_preferences = feedback_data.get("preferences", {})
        
        preferences_available = bool(explicit_preferences["tags"] or learned_preferences or blocked_content)
        
        return {
            "explicit_preferences": explicit_preferences,
            "learned_preferences": learned_preferences,
            "blocked_content": blocked_content,
            "preferences_available": preferences_available
        }
    
    def _extract_feedback_history(self, feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract feedback history for learning (unchanged)"""
        if not feedback_data:
            return {}
        
        return {
            "total_feedback_points": feedback_data.get("feedback_points", 0),
            "recent_blocks": feedback_data.get("blocked_items", []),
            "preference_patterns": feedback_data.get("preferences", {}),
            "feedback_available": True
        }
    
    def _select_daily_theme(self) -> Dict[str, Any]:
        """Select daily theme with enhanced metadata"""
        try:
            if theme_manager:
                # Get today's theme
                daily_theme = theme_manager.get_todays_theme()
                theme_image = theme_manager.get_theme_image(daily_theme)
                
                return {
                    "theme": daily_theme,
                    "theme_image": theme_image,
                    "selection_metadata": {
                        "date": datetime.now().date().isoformat(),
                        "theme_manager_used": True,
                        "image_available": bool(theme_image.get("image_url"))
                    }
                }
            else:
                # Fallback theme
                fallback_theme = {
                    "id": "general",
                    "name": "General",
                    "description": "General daily activities and memories",
                    "conversation_prompts": ["Tell me about something that makes you happy"],
                    "recipe_keywords": ["comfort"],
                    "content_preferences": {"qloo_priority": "places", "sensory_focus": "visual"}
                }
                
                fallback_theme_image = self._create_fallback_theme_image(fallback_theme)
                
                return {
                    "theme": fallback_theme,
                    "theme_image": fallback_theme_image,
                    "selection_metadata": {
                        "date": datetime.now().date().isoformat(),
                        "fallback_used": True,
                        "fallback_reason": "theme_manager_unavailable"
                    }
                }
                
        except Exception as e:
            logger.error(f"❌ Theme selection failed: {e}")
            return self._create_emergency_theme()
    
    def _create_fallback_theme_image(self, theme: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback theme image structure (unchanged)"""
        return {
            "image_url": f"/static/themes/{theme['id']}_fallback.jpg",
            "alt_text": f"{theme['name']} theme image",
            "source": "fallback",
            "theme_id": theme['id']
        }
    
    def _create_emergency_theme(self) -> Dict[str, Any]:
        """Create emergency theme when all else fails (unchanged)"""
        emergency_theme = {
            "id": "emergency",
            "name": "Memory Lane",
            "description": "General memories and conversations",
            "conversation_prompts": ["Tell me about a happy memory"],
            "recipe_keywords": ["comfort", "traditional"],
            "content_preferences": {"qloo_priority": "places", "sensory_focus": "visual"}
        }
        
        return {
            "theme": emergency_theme,
            "theme_image": self._create_fallback_theme_image(emergency_theme),
            "selection_metadata": {
                "date": datetime.now().date().isoformat(),
                "emergency_fallback": True,
                "fallback_reason": "all_theme_systems_failed"
            }
        }
    
    def _create_fallback_consolidated_info(self, patient_profile: Dict[str, Any], 
                                         request_type: str, 
                                         session_id: Optional[str]) -> Dict[str, Any]:
        """Create fallback consolidated information when main processing fails"""
        
        logger.warning("Creating fallback consolidated information")
        
        # Basic fallback data
        fallback_demographics = {
            "first_name": patient_profile.get("first_name", "Friend"),
            "age_range": "55_and_older",
            "demographics_available": False
        }
        
        fallback_location = {
            "primary_location": "your area",
            "location_type": "unknown",
            "location_available": False,
            "rural_indicators": {"likely_rural": False, "reason": "fallback_mode"}
        }
        
        fallback_theme = self._create_emergency_theme()
        
        return {
            "patient_profile": patient_profile,
            "session_metadata": {
                "session_id": session_id,
                "request_type": request_type,
                "timestamp": datetime.now().isoformat(),
                "processing_agent": "information_consolidator_fallback"
            },
            "demographics": fallback_demographics,
            "heritage_info": {"heritage_available": False},
            "preferences_info": {"preferences_available": False},
            "location_info": fallback_location,  # ENHANCED: Fallback location
            "daily_theme": fallback_theme,
            "feedback_history": {},
            "processing_metadata": {
                "fallback_used": True,
                "fallback_reason": "main_processing_failed"
            }
        }

# Export the main class
__all__ = ["InformationConsolidatorAgent"]