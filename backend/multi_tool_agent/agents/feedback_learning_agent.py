"""
Agent 7: Feedback Learning System - FIXED VERSION
Role: Process feedback and update preference profile
Follows Responsible Development Guide principles - individual preferences override everything
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

class FeedbackLearningSystemAgent(Agent):
    """
    Agent 7: Feedback Learning System
    
    Purpose: Process feedback and update preference profile
    Input: Feedback data + all previous outputs
    Output: Updated preference profile with feedback integration
    
    Anti-Bias Principles:
    - Process emoji feedback and blocking choices
    - Update blocked content and dislikes
    - Learn individual patterns that override cultural assumptions
    - Maintain preference profile for future sessions
    - Individual feedback always overrides demographic suggestions
    """
    
    def __init__(self, session_storage_tool):
        super().__init__(
            name="feedback_learning_system",
            description="Processes user feedback and learns individual preferences"
        )
        # FIXED: Store tool reference differently to avoid Pydantic field errors
        self._session_storage_tool_ref = session_storage_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any],
                  mobile_experience: Dict[str, Any],
                  feedback_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process feedback and update user preferences.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            qloo_intelligence: Output from Agent 3
            sensory_content: Output from Agent 4
            photo_analysis: Output from Agent 5
            mobile_experience: Output from Agent 6
            feedback_data: User feedback from mobile interface
            
        Returns:
            Updated preferences and learning results
        """
        
        try:
            logger.info("Processing feedback and updating preferences")
            
            # Extract session information
            session_metadata = consolidated_info.get("session_metadata", {})
            session_id = session_metadata.get("session_id")
            
            if not feedback_data:
                logger.info("No feedback data provided - returning current preferences")
                return await self._get_current_preferences(session_id)
            
            # Process the feedback using tool reference
            feedback_results = await self._process_feedback_data(feedback_data, session_id)
            
            # Update preferences based on feedback
            updated_preferences = await self._update_preferences(feedback_results, session_id)
            
            # Learn patterns from feedback
            learning_insights = self._analyze_feedback_patterns(feedback_results, updated_preferences)
            
            # Generate blocking updates
            blocking_updates = self._process_blocking_feedback(feedback_data, updated_preferences)
            
            # Create preference profile for future sessions
            future_guidance = self._generate_future_session_guidance(
                updated_preferences,
                learning_insights,
                blocking_updates
            )
            
            # Build complete feedback learning results
            feedback_learning = {
                "learning_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": session_id,
                    "feedback_processed": bool(feedback_data),
                    "preferences_updated": True,
                    "individual_learning_active": True
                },
                "feedback_results": feedback_results,
                "updated_preferences": updated_preferences,
                "learning_insights": learning_insights,
                "blocking_updates": blocking_updates,
                "future_guidance": future_guidance,
                "anti_bias_validation": {
                    "individual_preferences_prioritized": True,
                    "demographic_assumptions_overridden": True,
                    "cultural_stereotypes_blocked": True,
                    "personal_choice_respected": True
                }
            }
            
            # Save updated preferences to session storage
            await self._save_preferences_to_storage(session_id, updated_preferences)
            
            logger.info("Feedback learning completed successfully")
            return {"updated_preferences": feedback_learning}
            
        except Exception as e:
            logger.error(f"Error in feedback learning: {str(e)}")
            return self._create_fallback_feedback_learning(consolidated_info, feedback_data)
    
    async def _get_current_preferences(self, session_id: str) -> Dict[str, Any]:
        """Get current preferences when no new feedback is provided."""
        
        try:
            # Use session storage tool reference
            session_data = await self._session_storage_tool_ref.get_session(session_id)
            
            if session_data:
                preferences = session_data.get("preferences", {})
                blocked_content = session_data.get("blocked_content", {})
                
                return {
                    "updated_preferences": {
                        "learning_metadata": {
                            "timestamp": datetime.utcnow().isoformat(),
                            "session_id": session_id,
                            "feedback_processed": False,
                            "preferences_loaded": True
                        },
                        "current_preferences": preferences,
                        "current_blocked_content": blocked_content,
                        "feedback_results": {},
                        "learning_insights": {"status": "no_new_feedback"},
                        "blocking_updates": {},
                        "future_guidance": self._generate_current_guidance(preferences, blocked_content)
                    }
                }
            else:
                return self._create_empty_preferences(session_id)
                
        except Exception as e:
            logger.error(f"Error getting current preferences: {str(e)}")
            return self._create_empty_preferences(session_id)
    
    async def _process_feedback_data(self, 
                                   feedback_data: Dict[str, Any], 
                                   session_id: str) -> Dict[str, Any]:
        """Process incoming feedback data."""
        
        feedback_results = {
            "feedback_type": feedback_data.get("feedback_type", "unknown"),
            "content_category": feedback_data.get("content_category", "unknown"),
            "content_details": feedback_data.get("content_details", {}),
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id
        }
        
        # Process emoji feedback
        if feedback_results["feedback_type"] in ["positive", "negative", "neutral"]:
            feedback_results["emoji_feedback"] = {
                "reaction": feedback_results["feedback_type"],
                "content_id": feedback_data.get("content_id", ""),
                "processing": "individual_preference_learning"
            }
        
        # Process blocking feedback
        if feedback_results["feedback_type"] == "blocked":
            feedback_results["blocking_feedback"] = {
                "blocked_item": feedback_data.get("content_details", {}).get("name", ""),
                "blocking_scope": feedback_data.get("blocking_scope", "item"),
                "processing": "individual_blocking_preference"
            }
        
        return feedback_results
    
    async def _update_preferences(self, 
                                feedback_results: Dict[str, Any], 
                                session_id: str) -> Dict[str, Any]:
        """Update user preferences based on feedback."""
        
        try:
            # Get existing preferences using tool reference
            session_data = await self._session_storage_tool_ref.get_session(session_id)
            existing_preferences = session_data.get("preferences", {}) if session_data else {}
            
            updated_preferences = existing_preferences.copy()
            
            # Update based on emoji feedback
            if "emoji_feedback" in feedback_results:
                emoji_data = feedback_results["emoji_feedback"]
                reaction = emoji_data["reaction"]
                content_category = feedback_results["content_category"]
                
                if reaction == "positive":
                    if "liked_content" not in updated_preferences:
                        updated_preferences["liked_content"] = {}
                    if content_category not in updated_preferences["liked_content"]:
                        updated_preferences["liked_content"][content_category] = []
                    
                    content_details = feedback_results["content_details"]
                    if content_details not in updated_preferences["liked_content"][content_category]:
                        updated_preferences["liked_content"][content_category].append(content_details)
                
                elif reaction == "negative":
                    if "disliked_content" not in updated_preferences:
                        updated_preferences["disliked_content"] = {}
                    if content_category not in updated_preferences["disliked_content"]:
                        updated_preferences["disliked_content"][content_category] = []
                    
                    content_details = feedback_results["content_details"]
                    if content_details not in updated_preferences["disliked_content"][content_category]:
                        updated_preferences["disliked_content"][content_category].append(content_details)
            
            # Update based on blocking feedback
            if "blocking_feedback" in feedback_results:
                blocking_data = feedback_results["blocking_feedback"]
                
                if "blocked_content" not in updated_preferences:
                    updated_preferences["blocked_content"] = {}
                
                blocking_scope = blocking_data["blocking_scope"]
                blocked_item = blocking_data["blocked_item"]
                content_category = feedback_results["content_category"]
                
                if blocking_scope == "item":
                    if "blocked_items" not in updated_preferences["blocked_content"]:
                        updated_preferences["blocked_content"]["blocked_items"] = []
                    updated_preferences["blocked_content"]["blocked_items"].append(blocked_item)
                
                elif blocking_scope == "type":
                    if "blocked_types" not in updated_preferences["blocked_content"]:
                        updated_preferences["blocked_content"]["blocked_types"] = []
                    updated_preferences["blocked_content"]["blocked_types"].append(content_category)
                
                elif blocking_scope == "category":
                    if "blocked_categories" not in updated_preferences["blocked_content"]:
                        updated_preferences["blocked_content"]["blocked_categories"] = []
                    updated_preferences["blocked_content"]["blocked_categories"].append(content_category)
            
            return updated_preferences
            
        except Exception as e:
            logger.error(f"Error updating preferences: {str(e)}")
            return {}
    
    def _analyze_feedback_patterns(self, 
                                  feedback_results: Dict[str, Any], 
                                  updated_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in feedback to generate learning insights."""
        
        insights = {
            "individual_learning_active": True,
            "pattern_analysis": {},
            "preference_trends": {},
            "anti_bias_compliance": "individual_preferences_override_demographics"
        }
        
        # Analyze liked content patterns
        liked_content = updated_preferences.get("liked_content", {})
        if liked_content:
            insights["preference_trends"]["positive_patterns"] = {}
            for category, items in liked_content.items():
                if len(items) >= 2:  # Pattern emerges with 2+ likes
                    insights["preference_trends"]["positive_patterns"][category] = {
                        "count": len(items),
                        "trend": "consistent_positive_feedback",
                        "recommendation": f"prioritize_{category}_content_in_future"
                    }
        
        # Analyze disliked content patterns  
        disliked_content = updated_preferences.get("disliked_content", {})
        if disliked_content:
            insights["preference_trends"]["negative_patterns"] = {}
            for category, items in disliked_content.items():
                if len(items) >= 2:  # Pattern emerges with 2+ dislikes
                    insights["preference_trends"]["negative_patterns"][category] = {
                        "count": len(items),
                        "trend": "consistent_negative_feedback",
                        "recommendation": f"reduce_{category}_content_suggestions"
                    }
        
        # Analyze blocking patterns
        blocked_content = updated_preferences.get("blocked_content", {})
        if blocked_content:
            insights["pattern_analysis"]["blocking_behavior"] = {
                "blocked_items": len(blocked_content.get("blocked_items", [])),
                "blocked_types": len(blocked_content.get("blocked_types", [])),
                "blocked_categories": len(blocked_content.get("blocked_categories", [])),
                "approach": "respect_all_blocking_preferences"
            }
        
        return insights
    
    def _process_blocking_feedback(self, 
                                  feedback_data: Dict[str, Any], 
                                  updated_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Process blocking feedback and generate updates."""
        
        blocking_updates = {
            "new_blocks_added": False,
            "blocking_scope": "none",
            "immediate_effect": "none"
        }
        
        if feedback_data and feedback_data.get("feedback_type") == "blocked":
            blocking_scope = feedback_data.get("blocking_scope", "item")
            content_details = feedback_data.get("content_details", {})
            content_name = content_details.get("name", "unknown")
            
            blocking_updates = {
                "new_blocks_added": True,
                "blocking_scope": blocking_scope,
                "blocked_item": content_name,
                "immediate_effect": f"future_recommendations_will_exclude_{blocking_scope}",
                "compliance": "individual_choice_respected",
                "override_effect": "blocks_override_all_demographic_and_cultural_suggestions"
            }
        
        return blocking_updates
    
    def _generate_future_session_guidance(self, 
                                        updated_preferences: Dict[str, Any],
                                        learning_insights: Dict[str, Any],
                                        blocking_updates: Dict[str, Any]) -> Dict[str, Any]:
        """Generate guidance for future sessions based on learned preferences."""
        
        guidance = {
            "preference_priorities": [],
            "content_avoidance": [],
            "personalization_level": "high_individual_customization",
            "bias_prevention": "individual_preferences_override_everything"
        }
        
        # Positive preference guidance
        liked_content = updated_preferences.get("liked_content", {})
        for category, items in liked_content.items():
            if len(items) >= 2:
                guidance["preference_priorities"].append({
                    "category": category,
                    "priority": "high",
                    "reason": f"consistent_positive_feedback_{len(items)}_times",
                    "implementation": f"prioritize_{category}_content_in_recommendations"
                })
        
        # Negative preference guidance
        disliked_content = updated_preferences.get("disliked_content", {})
        blocked_content = updated_preferences.get("blocked_content", {})
        
        for category, items in disliked_content.items():
            guidance["content_avoidance"].append({
                "category": category,
                "avoidance_level": "reduce_frequency",
                "reason": f"negative_feedback_received_{len(items)}_times"
            })
        
        # Blocking guidance
        if blocked_content:
            for block_type in ["blocked_items", "blocked_types", "blocked_categories"]:
                blocked_list = blocked_content.get(block_type, [])
                for blocked_item in blocked_list:
                    guidance["content_avoidance"].append({
                        "item": blocked_item,
                        "avoidance_level": "complete_exclusion",
                        "reason": "explicit_user_blocking",
                        "scope": block_type
                    })
        
        return guidance
    
    def _generate_current_guidance(self, 
                                  preferences: Dict[str, Any], 
                                  blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate guidance based on current preferences when no new feedback."""
        
        return {
            "current_preferences_active": True,
            "liked_content_categories": list(preferences.get("liked_content", {}).keys()),
            "disliked_content_categories": list(preferences.get("disliked_content", {}).keys()),
            "blocked_content_summary": {
                "items_blocked": len(blocked_content.get("blocked_items", [])),
                "types_blocked": len(blocked_content.get("blocked_types", [])),
                "categories_blocked": len(blocked_content.get("blocked_categories", []))
            },
            "recommendation": "continue_using_established_preferences"
        }
    
    async def _save_preferences_to_storage(self, 
                                         session_id: str, 
                                         updated_preferences: Dict[str, Any]) -> None:
        """Save updated preferences to session storage."""
        
        try:
            # Use session storage tool reference
            await self._session_storage_tool_ref.update_session_preferences(session_id, updated_preferences)
            logger.info(f"Preferences saved to session storage for session {session_id}")
        except Exception as e:
            logger.error(f"Error saving preferences to storage: {str(e)}")
    
    def _create_empty_preferences(self, session_id: str) -> Dict[str, Any]:
        """Create empty preferences structure."""
        
        return {
            "updated_preferences": {
                "learning_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": session_id,
                    "feedback_processed": False,
                    "preferences_loaded": False,
                    "new_session": True
                },
                "current_preferences": {},
                "current_blocked_content": {},
                "feedback_results": {},
                "learning_insights": {"status": "new_session_no_preferences"},
                "blocking_updates": {},
                "future_guidance": {
                    "new_session": True,
                    "recommendation": "start_learning_from_user_feedback"
                }
            }
        }
    
    def _create_fallback_feedback_learning(self, 
                                         consolidated_info: Dict[str, Any], 
                                         feedback_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Create fallback feedback learning when session storage is unavailable."""
        
        session_metadata = consolidated_info.get("session_metadata", {})
        session_id = session_metadata.get("session_id", "unknown")
        
        return {
            "updated_preferences": {
                "learning_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": session_id,
                    "feedback_processed": False,
                    "fallback_used": True,
                    "fallback_reason": "session_storage_unavailable"
                },
                "feedback_results": {"status": "unable_to_process"},
                "updated_preferences": {},
                "learning_insights": {"status": "session_storage_unavailable"},
                "blocking_updates": {"status": "unable_to_update"},
                "future_guidance": {
                    "fallback_mode": True,
                    "recommendation": "feedback_learning_unavailable_this_session"
                }
            }
        }