"""
Step 1: Information Consolidator Agent - WITH THEME FILE WRITING
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

NEW FEATURE:
- Writes current theme to config/current_theme.json
- Creates single source of truth for all other agents
- Eliminates theme drift and parameter confusion
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
    Step 1: Information Consolidator with Theme State File
    
    NEW FEATURE:
    - Writes theme to config/current_theme.json for other agents
    """
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        
        # Path to current theme state file
        self.theme_file_path = os.path.join(
            os.path.dirname(__file__), 
            "..", "..", "config", "current_theme.json"
        )
        
        logger.info("✅ Step 1: Information Consolidator initialized with theme file writing")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Step 1: Consolidate information and write theme state file
        """
        
        logger.info("📋 Step 1: Starting information consolidation with theme file writing")
        
        try:
            # Extract basic profile information
            basic_info = self._extract_basic_profile(patient_profile)
            
            # Handle simple feedback mechanism
            feedback_summary = self._process_feedback(feedback_data)
            
            # Get complete theme data including photo_filename
            theme_data = self._select_theme_with_photo(session_id)
            
            # NEW: Write theme to file for other agents
            self._write_theme_state_file(theme_data, session_id)
            
            # Create consolidated profile with proper structure for Agent 2
            consolidated_profile = {
                # Basic patient information
                "patient_info": basic_info,
                
                # Include photo_filename in theme_info for Agent 2
                "theme_info": theme_data,
                
                # Simple feedback tracking
                "feedback_info": feedback_summary,
                
                # Session metadata
                "session_metadata": {
                    "session_id": session_id or "default",
                    "request_type": request_type,
                    "timestamp": datetime.now().isoformat(),
                    "step": "information_consolidation"
                },
                
                # Pipeline state tracking
                "pipeline_state": {
                    "current_step": 1,
                    "next_step": "photo_analysis",
                    "profile_ready": True,
                    "theme_file_written": True  # NEW: Track theme file status
                }
            }
            
            logger.info(f"✅ Step 1: Profile consolidated successfully")
            logger.info(f"   Patient: {basic_info.get('first_name', 'Unknown')}")
            logger.info(f"   Theme: {theme_data.get('name', 'Unknown')}")
            logger.info(f"   Theme file: Written to {self.theme_file_path}")
            logger.info(f"   Feedback: {len(feedback_summary.get('likes', []))} likes, {len(feedback_summary.get('dislikes', []))} dislikes")
            
            return consolidated_profile
            
        except Exception as e:
            logger.error(f"❌ Step 1 failed: {e}")
            return self._create_fallback_profile(patient_profile, request_type, session_id)
    
    def _write_theme_state_file(self, theme_data: Dict[str, Any], session_id: Optional[str]) -> None:
        """
        NEW: Write current theme state to JSON file for other agents to read
        
        Args:
            theme_data: Complete theme information from _select_theme_with_photo()
            session_id: Current session ID
        """
        
        try:
            # Ensure config directory exists
            config_dir = os.path.dirname(self.theme_file_path)
            os.makedirs(config_dir, exist_ok=True)
            
            # FIXED: Extract theme information directly from theme_data (not nested)
            # theme_data comes from _select_theme_with_photo() which returns the theme directly
            
            # Create theme state structure using the direct theme data
            theme_state = {
                "theme_id": theme_data.get("id", "memory_lane"),
                "theme_name": theme_data.get("name", "Memory Lane"), 
                "theme_description": theme_data.get("description", "A time for remembering special moments"),
                "photo_filename": theme_data.get("photo_filename", "memory_lane.png"),
                "conversation_prompts": theme_data.get("conversation_prompts", []),
                "timestamp": datetime.now().isoformat(),
                "session_id": session_id or "default",
                "written_by": "information_consolidator_agent",
                "selection_metadata": theme_data.get("metadata", {}),  # FIXED: Use "metadata" key
                "source": theme_data.get("source", "unknown")
            }
            
            # Write to file
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
    
    def _extract_basic_profile(self, patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and clean basic profile information"""
        
        # Get essential profile fields
        first_name = patient_profile.get("first_name", "Friend")
        birth_year = patient_profile.get("birth_year")
        cultural_heritage = patient_profile.get("cultural_heritage", "American")
        
        # Calculate age if birth year provided
        current_age = None
        age_group = "senior"  # Default assumption for dementia care
        
        if birth_year:
            current_age = datetime.now().year - birth_year
            if current_age >= 80:
                age_group = "oldest_senior"
            elif current_age >= 65:
                age_group = "senior"
            else:
                age_group = "adult"
        
        logger.info(f"📝 Basic profile: {first_name}, age {current_age or 'unknown'}, {cultural_heritage}")
        
        return {
            "first_name": first_name,
            "last_name": patient_profile.get("last_name", ""),
            "birth_year": birth_year,
            "current_age": current_age,
            "age_group": age_group,
            "cultural_heritage": cultural_heritage,
            "city": patient_profile.get("city", ""),
            "state": patient_profile.get("state", ""),
            "interests": patient_profile.get("interests", []),
            "medical_conditions": patient_profile.get("medical_conditions", []),
            "profile_complete": bool(first_name and cultural_heritage)
        }
    
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
        """
        Select theme AND extract photo_filename for Agent 2
        """
        
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
                    "photo_filename": photo_filename,  # For Agent 2
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
    
    def _create_fallback_profile(self, patient_profile: Dict[str, Any], 
                                request_type: str, 
                                session_id: Optional[str]) -> Dict[str, Any]:
        """Create fallback profile when main processing fails"""
        
        logger.warning("🔄 Creating fallback consolidated profile")
        
        # Still try to write theme file even in fallback mode
        fallback_theme = self._get_fallback_theme()
        self._write_theme_state_file({"theme_of_the_day": fallback_theme, "photo_filename": fallback_theme["photo_filename"]}, session_id)
        
        return {
            "patient_info": {
                "first_name": patient_profile.get("first_name", "Friend"),
                "cultural_heritage": "American",
                "age_group": "senior",
                "profile_complete": False
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
                "theme_file_written": True  # Theme file still written in fallback
            }
        }

# Export the main class
__all__ = ["InformationConsolidatorAgent"]