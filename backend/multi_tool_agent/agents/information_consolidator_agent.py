"""
Information Consolidator Agent - Enhanced with Daily Theme Selection
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

Agent 1: Consolidates all input information and adds daily theme selection
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Configure logger FIRST
logger = logging.getLogger(__name__)

# Import theme manager with error handling (FIXED import path)
try:
    # Try direct import path first (working path)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Successfully imported theme_manager")
    
    # Debug theme manager status
    debug_status = theme_manager.debug_theme_status()
    logger.info(f"🔍 Theme manager debug: {debug_status}")
    
except ImportError as e:
    logger.error(f"❌ Failed to import theme_manager: {e}")
    theme_manager = None
except Exception as e:
    logger.error(f"❌ Error with theme_manager: {e}")
    theme_manager = None

class InformationConsolidatorAgent:
    """
    Agent 1: Information Consolidator with Daily Theme Selection
    
    Consolidates patient profile, request type, and session info.
    NEW: Adds daily theme selection for enhanced content curation.
    """
    
    def __init__(self):
        logger.info("Information Consolidator initialized with theme support")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None,
                  photo_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Consolidate all input information and select daily theme.
        
        Args:
            patient_profile: Patient information including demographics and preferences
            request_type: Type of request (dashboard, recipe, music, etc.)
            session_id: Session identifier for tracking
            feedback_data: Previous feedback for learning (optional)
            photo_data: Photo information if available
            
        Returns:
            Consolidated information with daily theme selection
        """
        
        try:
            logger.info("🔄 Agent 1: Starting information consolidation with theme selection")
            
            # Generate session ID if not provided
            if not session_id:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                patient_name = patient_profile.get("first_name", "unknown")
                birth_year = patient_profile.get("birth_year", "unknown")
                session_id = f"session_{patient_name}_{birth_year}_{timestamp}"
            
            # Extract patient demographics
            demographics = self._extract_demographics(patient_profile)
            
            # Extract cultural heritage information
            heritage_info = self._extract_heritage_info(patient_profile)
            
            # Extract preferences and blocked content
            preferences_info = self._extract_preferences_info(patient_profile, feedback_data)
            
            # NEW: Select daily theme (additive - doesn't change existing logic)
            if theme_manager:
                try:
                    theme_selection = theme_manager.get_daily_theme(session_id)
                    daily_theme = theme_selection["theme_of_the_day"]
                    logger.info(f"📅 Daily theme selected: {daily_theme['name']} - {daily_theme['description']}")
                except Exception as e:
                    logger.error(f"❌ Error selecting daily theme: {e}")
                    # Fallback theme
                    daily_theme = {
                        "id": "general",
                        "name": "General",
                        "description": "General daily activities",
                        "conversation_prompts": ["Tell me about something that makes you happy"],
                        "recipe_keywords": ["comfort"],
                        "content_preferences": {"qloo_priority": "places", "sensory_focus": "visual"}
                    }
                    theme_selection = {
                        "theme_of_the_day": daily_theme,
                        "selection_metadata": {
                            "date": datetime.now().date().isoformat(),
                            "fallback_used": True,
                            "error": str(e)
                        }
                    }
            else:
                logger.warning("⚠️ theme_manager not available - using fallback theme")
                # Fallback theme when theme_manager import failed
                daily_theme = {
                    "id": "general", 
                    "name": "General",
                    "description": "General daily activities",
                    "conversation_prompts": ["Tell me about something that makes you happy"],
                    "recipe_keywords": ["comfort"],
                    "content_preferences": {"qloo_priority": "places", "sensory_focus": "visual"}
                }
                theme_selection = {
                    "theme_of_the_day": daily_theme,
                    "selection_metadata": {
                        "date": datetime.now().date().isoformat(),
                        "fallback_used": True,
                        "fallback_reason": "theme_manager_import_failed"
                    }
                }
            
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
                # NEW: Theme information (additive)
                "daily_theme": {
                    "theme": daily_theme,
                    "selection_metadata": theme_selection["selection_metadata"],
                    "application_note": "Theme enhances content selection but doesn't override individual preferences"
                },
                "feedback_history": feedback_data or {},
                "photo_context": photo_data or {},
                "processing_metadata": {
                    "consolidation_timestamp": datetime.now().isoformat(),
                    "data_sources": ["patient_profile", "session_data", "daily_theme"],
                    "theme_enabled": theme_manager is not None,
                    "agent_version": "1.1_with_themes"
                }
            }
            
            logger.info("✅ Agent 1 completed: Information consolidated with daily theme")
            logger.info(f"   Patient: {demographics.get('first_name')} (Age {demographics.get('age')})")
            logger.info(f"   Heritage: {heritage_info.get('primary_heritage', 'Not specified')}")
            logger.info(f"   Daily Theme: {daily_theme['name']}")
            
            # DEBUG: Log the structure being returned
            logger.info(f"🔍 DEBUG Agent 1 RETURN: daily_theme structure in consolidated_info: {consolidated_info['daily_theme']}")
            
            # IMPORTANT: Return wrapped in the expected format for sequential agent
            return {"consolidated_info": consolidated_info}
            
        except Exception as e:
            logger.error(f"❌ Agent 1 failed: {e}")
            return self._create_fallback_consolidated_info(patient_profile, request_type, session_id)
    
    def _extract_demographics(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and calculate demographic information."""
        
        current_year = datetime.now().year
        birth_year = patient_profile.get("birth_year")
        age = current_year - birth_year if birth_year else None
        
        # Determine age demographic for Qloo API
        age_demographic = "55_and_older"  # Default for dementia care
        if age:
            if age >= 80:
                age_demographic = "55_and_older"  # Qloo's oldest category
            elif age >= 65:
                age_demographic = "55_and_older"
            else:
                age_demographic = "35_to_54"
        
        return {
            "first_name": patient_profile.get("first_name", ""),
            "birth_year": birth_year,
            "birth_month": patient_profile.get("birth_month"),
            "age": age,
            "age_demographic": age_demographic,
            "location": {
                "city": patient_profile.get("city", ""),
                "region": patient_profile.get("region", ""),
                "country": patient_profile.get("country", "")
            }
        }
    
    def _extract_heritage_info(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cultural heritage information for cultural intelligence."""
        
        return {
            "primary_heritage": patient_profile.get("heritage", ""),
            "languages": patient_profile.get("languages", ""),
            "spiritual_traditions": patient_profile.get("spiritual_traditions", ""),
            "cultural_context": patient_profile.get("additional_context", ""),
            "heritage_specified": bool(patient_profile.get("heritage"))
        }
    
    def _extract_preferences_info(self, 
                                patient_profile: Dict[str, Any],
                                feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract preferences and blocked content from profile and feedback."""
        
        # Extract explicit preferences from profile
        explicit_preferences = {
            "tags": patient_profile.get("tags", []),
            "interests": patient_profile.get("interests", []),
            "photo_library": patient_profile.get("photo_library", [])
        }
        
        # Extract learned preferences from feedback
        learned_preferences = {}
        blocked_content = []
        
        if feedback_data:
            learned_preferences = feedback_data.get("learned_preferences", {})
            blocked_content = feedback_data.get("blocked_content", [])
        
        return {
            "explicit_preferences": explicit_preferences,
            "learned_preferences": learned_preferences,
            "blocked_content": blocked_content,
            "caregiver_notes": patient_profile.get("caregiver_notes", ""),
            "preferences_available": bool(explicit_preferences["tags"] or learned_preferences)
        }
    
    def _create_fallback_consolidated_info(self, 
                                         patient_profile: Dict[str, Any],
                                         request_type: str,
                                         session_id: Optional[str]) -> Dict[str, Any]:
        """Create fallback consolidated info if main processing fails."""
        
        logger.warning("Creating fallback consolidated information")
        
        # Get fallback theme
        fallback_theme = {
            "id": "general",
            "name": "General",
            "description": "General daily activities",
            "conversation_prompts": ["Tell me about something that makes you happy"],
            "recipe_keywords": ["comfort"],
            "content_preferences": {"qloo_priority": "places", "sensory_focus": "visual"}
        }
        
        fallback_theme_selection = {
            "theme_of_the_day": fallback_theme,
            "selection_metadata": {
                "date": datetime.now().date().isoformat(),
                "fallback_used": True,
                "fallback_reason": "main_processing_failed"
            }
        }
        
        return {
            "consolidated_info": {
                "patient_profile": patient_profile,
                "session_metadata": {
                    "session_id": session_id or "fallback_session",
                    "request_type": request_type,
                    "timestamp": datetime.now().isoformat(),
                    "processing_agent": "information_consolidator_fallback"
                },
                "demographics": {
                    "first_name": patient_profile.get("first_name", ""),
                    "age_demographic": "55_and_older",
                    "age": None
                },
                "heritage_info": {
                    "primary_heritage": patient_profile.get("heritage", ""),
                    "heritage_specified": False
                },
                "preferences_info": {
                    "explicit_preferences": {"tags": []},
                    "learned_preferences": {},
                    "blocked_content": [],
                    "preferences_available": False
                },
                "daily_theme": {
                    "theme": fallback_theme,
                    "selection_metadata": fallback_theme_selection["selection_metadata"],
                    "application_note": "Fallback theme selection"
                },
                "feedback_history": {},
                "photo_context": {},
                "processing_metadata": {
                    "consolidation_timestamp": datetime.now().isoformat(),
                    "data_sources": ["patient_profile_fallback", "daily_theme_fallback"],
                    "theme_enabled": False,
                    "agent_version": "1.1_fallback",
                    "fallback_reason": "main_processing_failed"
                }
            }
        }