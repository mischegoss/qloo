"""
Step 1: Simplified Information Consolidator Agent
File: backend/multi_tool_agent/agents/information_consolidator_agent.py

SIMPLIFIED PIPELINE APPROACH:
- Get basic profile information from UI
- Handle simple feedback (likes/dislikes)
- Pick theme from 10 themes in JSON
- Create clean consolidated profile for next step
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class InformationConsolidatorAgent:
    """
    Step 1: Simplified Information Consolidator
    
    PURPOSE:
    - Consolidate basic profile information
    - Handle simple feedback mechanism  
    - Select daily theme from themes.json
    - Create clean profile structure for pipeline
    """
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        logger.info("✅ Step 1: Information Consolidator initialized (simplified pipeline)")
    
    async def run(self, 
                  patient_profile: Dict[str, Any],
                  request_type: str = "dashboard",
                  session_id: Optional[str] = None,
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Step 1: Consolidate information for simplified pipeline
        
        Args:
            patient_profile: Basic profile from UI
            request_type: Type of request 
            session_id: Session identifier
            feedback_data: Simple likes/dislikes feedback
            
        Returns:
            Clean consolidated profile for Step 2
        """
        
        logger.info("📋 Step 1: Starting information consolidation")
        
        try:
            # Extract basic profile information
            basic_info = self._extract_basic_profile(patient_profile)
            
            # Handle simple feedback mechanism
            feedback_summary = self._process_feedback(feedback_data)
            
            # Select theme for the session
            selected_theme = self._select_theme(session_id)
            
            # Create consolidated profile
            consolidated_profile = {
                # Basic patient information
                "patient_info": basic_info,
                
                # Theme for this session
                "selected_theme": selected_theme,
                
                # Simple feedback tracking
                "feedback": feedback_summary,
                
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
                    "profile_ready": True
                }
            }
            
            logger.info(f"✅ Step 1: Profile consolidated successfully")
            logger.info(f"   Patient: {basic_info.get('first_name', 'Unknown')}")
            logger.info(f"   Theme: {selected_theme.get('name', 'Unknown')}")
            logger.info(f"   Feedback: {len(feedback_summary.get('likes', []))} likes, {len(feedback_summary.get('dislikes', []))} dislikes")
            
            return consolidated_profile
            
        except Exception as e:
            logger.error(f"❌ Step 1 failed: {e}")
            return self._create_fallback_profile(patient_profile, request_type, session_id)
    
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
        
        basic_info = {
            "first_name": first_name,
            "birth_year": birth_year,
            "current_age": current_age,
            "age_group": age_group,
            "cultural_heritage": cultural_heritage,
            
            # Additional context
            "location": patient_profile.get("city", "") + ", " + patient_profile.get("state", ""),
            "additional_context": patient_profile.get("additional_context", ""),
            
            # Profile completeness
            "profile_complete": bool(first_name and birth_year and cultural_heritage)
        }
        
        logger.info(f"📝 Basic profile: {first_name}, age {current_age}, {cultural_heritage}")
        return basic_info
    
    def _process_feedback(self, feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Process simple feedback mechanism (likes/dislikes)"""
        
        if not feedback_data:
            return {
                "likes": [],
                "dislikes": [],
                "total_feedback": 0,
                "feedback_available": False
            }
        
        # Extract likes and dislikes
        likes = feedback_data.get("likes", [])
        dislikes = feedback_data.get("dislikes", [])
        
        # Ensure they're lists
        if not isinstance(likes, list):
            likes = []
        if not isinstance(dislikes, list):
            dislikes = []
        
        feedback_summary = {
            "likes": likes,
            "dislikes": dislikes,
            "total_feedback": len(likes) + len(dislikes),
            "feedback_available": len(likes) + len(dislikes) > 0,
            
            # Simple feedback insights
            "preferred_types": self._extract_preferred_types(likes),
            "avoided_types": self._extract_avoided_types(dislikes)
        }
        
        logger.info(f"🔄 Feedback processed: {len(likes)} likes, {len(dislikes)} dislikes")
        return feedback_summary
    
    def _extract_preferred_types(self, likes: List[Dict[str, Any]]) -> List[str]:
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
    
    def _select_theme(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Select theme using theme manager"""
        
        try:
            if self.theme_manager:
                # Use theme manager to get daily theme
                theme_data = self.theme_manager.get_daily_theme(session_id)
                selected_theme = theme_data.get("theme_of_the_day", {})
                
                logger.info(f"🎯 Theme selected: {selected_theme.get('name', 'Unknown')}")
                
                return {
                    "id": selected_theme.get("id", "general"),
                    "name": selected_theme.get("name", "Memory Lane"),
                    "description": selected_theme.get("description", "A time for remembering"),
                    "conversation_prompts": selected_theme.get("conversation_prompts", []),
                    "source": "theme_manager"
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
            "source": "fallback"
        }
    
    def _create_fallback_profile(self, patient_profile: Dict[str, Any], 
                                request_type: str, 
                                session_id: Optional[str]) -> Dict[str, Any]:
        """Create fallback profile when main processing fails"""
        
        logger.warning("🔄 Creating fallback consolidated profile")
        
        return {
            "patient_info": {
                "first_name": patient_profile.get("first_name", "Friend"),
                "cultural_heritage": "American",
                "age_group": "senior",
                "profile_complete": False
            },
            "selected_theme": self._get_fallback_theme(),
            "feedback": {
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
                "fallback_used": True
            }
        }

# Export the main class
__all__ = ["InformationConsolidatorAgent"]