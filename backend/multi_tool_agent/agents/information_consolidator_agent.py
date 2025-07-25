"""
Enhanced Information Consolidator Agent - THEME METHOD CALL FIXED
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

CRITICAL FIX:
- Fixed theme_manager.get_todays_theme() → theme_manager.get_daily_theme()
- Now correctly calls the existing method in ThemeManager
- Maintains all existing location prioritization functionality
- Supports rural area identification and theme image support
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
    Agent 1: Enhanced Information Consolidator with FIXED Theme Method Call
    
    CRITICAL FIX:
    - Fixed method call from get_todays_theme() to get_daily_theme()
    - Now properly integrates with ThemeManager
    - Maintains location prioritization and rural area support
    - Full theme image and metadata support
    """
    
    def __init__(self):
        logger.info("✅ Information Consolidator initialized with LOCATION PRIORITIZATION")
    
    async def run(self, 
                  patient_profile: Dict[str, Any], 
                  request_type: str, 
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Enhanced consolidation with location prioritization and FIXED theme integration
        
        Args:
            patient_profile: Patient profile data
            request_type: Type of request (dashboard, etc.)
            session_id: Session identifier
            feedback_data: Feedback history (optional)
            
        Returns:
            Consolidated information with prioritized location data and proper theme
        """
        
        logger.info("📋 Agent 1: Starting enhanced information consolidation with location prioritization")
        
        try:
            # Core consolidation
            demographics = self._extract_demographics(patient_profile)
            heritage_info = self._extract_heritage_info(patient_profile)
            preferences_info = self._extract_preferences_info(feedback_data)
            
            # ENHANCED: Location prioritization
            location_info = self._extract_location_info(patient_profile)
            
            # FIXED: Theme selection with proper method call
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
                "daily_theme": daily_theme,  # FIXED: Now properly selected
                "feedback_history": self._extract_feedback_history(feedback_data),
                "processing_metadata": {
                    "theme_manager_available": theme_manager is not None,
                    "location_prioritization": "hometown_preferred",
                    "rural_area_support": True,
                    "consolidated_successfully": True,
                    "theme_method_fixed": True  # NEW: Indicates the fix is applied
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
                "hometown_preferred": bool(hometown),
                "priority_used": location_type,
                "rural_area_detected": rural_indicators.get("likely_rural", False)
            }
        }
        
        logger.info(f"🏠 Location prioritization: {primary_location} ({location_type})")
        if rural_indicators.get("likely_rural"):
            logger.info(f"🌾 Rural area detected: {rural_indicators.get('reason', 'unknown')}")
        
        return location_info
    
    def _detect_rural_area(self, location: str) -> Dict[str, Any]:
        """Detect if location might be a rural area using simple heuristics"""
        
        if not location:
            return {"likely_rural": False, "reason": "no_location_data"}
        
        location_lower = location.lower()
        
        # Rural indicators (simple heuristics)
        rural_keywords = [
            "county", "township", "village", "hamlet", "farm", "ranch", 
            "rural", "countryside", "valley", "creek", "mountain", "hill",
            "road", "route", "highway", "mile", "acres"
        ]
        
        # Urban indicators (counterbalances)
        urban_keywords = [
            "city", "downtown", "metro", "district", "avenue", "boulevard",
            "plaza", "center", "square", "street", "st.", "ave.", "blvd."
        ]
        
        rural_score = sum(1 for keyword in rural_keywords if keyword in location_lower)
        urban_score = sum(1 for keyword in urban_keywords if keyword in location_lower)
        
        # Simple scoring logic
        if rural_score > urban_score and rural_score >= 1:
            return {
                "likely_rural": True,
                "reason": f"rural_keywords_found",
                "rural_score": rural_score,
                "urban_score": urban_score
            }
        else:
            return {
                "likely_rural": False,
                "reason": "urban_or_unclear",
                "rural_score": rural_score,
                "urban_score": urban_score
            }
    
    def _extract_demographics(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract demographic information (unchanged)"""
        birth_year = patient_profile.get("birth_year")
        birth_month = patient_profile.get("birth_month")
        
        # Calculate age range
        current_year = datetime.now().year
        age = current_year - birth_year if birth_year else None
        
        # Determine age range for filtering
        if age:
            if age >= 55:
                age_range = "55_and_older"
            elif age >= 36:
                age_range = "36_to_55"
            else:
                age_range = "18_to_35"
        else:
            age_range = "55_and_older"  # Default assumption
        
        return {
            "first_name": patient_profile.get("first_name", "Friend"),
            "birth_year": birth_year,
            "birth_month": birth_month,
            "calculated_age": age,
            "age_range": age_range,
            "demographics_available": bool(birth_year)
        }
    
    def _extract_heritage_info(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract heritage information (unchanged)"""
        heritage_raw = patient_profile.get("heritage", "").strip()
        
        if not heritage_raw:
            return {
                "cultural_heritage": "American",
                "heritage_tags": ["american"],
                "heritage_available": False
            }
        
        # Clean and split heritage information
        heritage_parts = [part.strip() for part in heritage_raw.replace(",", " ").split()]
        heritage_parts = [part for part in heritage_parts if len(part.strip()) > 2]
        
        # Extract main heritage
        cultural_heritage = heritage_parts[0] if heritage_parts else "American"
        additional_context = " ".join(heritage_parts[1:]) if len(heritage_parts) > 1 else ""
        
        # Create heritage tags for API calls
        heritage_tags = [part.lower().replace("-", "_") for part in heritage_parts if len(part.strip()) > 2]
        
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
        """FIXED: Select daily theme with proper method call"""
        try:
            if theme_manager:
                # CRITICAL FIX: Changed from get_todays_theme() to get_daily_theme()
                daily_theme_data = theme_manager.get_daily_theme()
                theme_of_the_day = daily_theme_data.get("theme_of_the_day", {})
                theme_image = daily_theme_data.get("theme_image", {})
                
                logger.info(f"✅ FIXED: Daily theme selected successfully: {theme_of_the_day.get('name', 'Unknown')}")
                
                return {
                    "theme": theme_of_the_day,
                    "theme_image": theme_image,
                    "selection_metadata": {
                        "date": datetime.now().date().isoformat(),
                        "theme_manager_used": True,
                        "image_available": bool(theme_image.get("filename")),
                        "method_call_fixed": True,  # NEW: Indicates fix was applied
                        "correct_method_used": "get_daily_theme"
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
        """Create fallback theme image structure"""
        return {
            "filename": f"{theme['id']}_fallback.jpg",
            "backend_path": f"/static/themes/{theme['id']}_fallback.jpg",
            "frontend_path": f"images/{theme['id']}_fallback.jpg",
            "theme_id": theme['id'],
            "theme_name": theme['name'],
            "exists": False,
            "is_fallback": True
        }
    
    def _create_emergency_theme(self) -> Dict[str, Any]:
        """Create emergency theme when all else fails"""
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
            "location_info": fallback_location,
            "daily_theme": fallback_theme,
            "feedback_history": {},
            "processing_metadata": {
                "fallback_used": True,
                "fallback_reason": "main_processing_failed",
                "theme_method_available": theme_manager is not None
            }
        }

# Export the main class
__all__ = ["InformationConsolidatorAgent"]