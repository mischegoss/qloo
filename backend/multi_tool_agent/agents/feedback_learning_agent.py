"""
Agent 7: Feedback Learning System
Role: Process feedback and update preference profile
Follows Responsible Development Guide principles - individual preferences override everything
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from google.adk.agents import Agent

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
        self.session_storage_tool = session_storage_tool
    
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
            
            # Process the feedback
            feedback_results = await self._process_feedback(feedback_data, session_id)
            
            # Update preference patterns
            preference_updates = await self._update_preference_patterns(
                feedback_data,
                cultural_profile,
                qloo_intelligence,
                sensory_content,
                session_id
            )
            
            # Learn from mobile experience effectiveness
            mobile_learning = await self._learn_from_mobile_experience(
                mobile_experience,
                feedback_data,
                session_id
            )
            
            # Build updated preference profile
            updated_preferences = {
                "learning_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "session_id": session_id,
                    "feedback_processed": True,
                    "learning_approach": "individual_preferences_override_demographics"
                },
                "feedback_results": feedback_results,
                "preference_updates": preference_updates,
                "mobile_learning": mobile_learning,
                "individual_priority_maintained": True,
                "cultural_assumptions_overridden": self._check_cultural_overrides(
                    feedback_data, cultural_profile
                )
            }
            
            logger.info("Feedback learning completed successfully")
            return {"updated_preferences": updated_preferences}
            
        except Exception as e:
            logger.error(f"Error in feedback learning: {str(e)}")
            return self._create_fallback_preferences(consolidated_info)
    
    async def _process_feedback(self, 
                               feedback_data: Dict[str, Any], 
                               session_id: Optional[str]) -> Dict[str, Any]:
        """Process the raw feedback data into structured preferences."""
        
        feedback_type = feedback_data.get("feedback_type", "unknown")
        content_category = feedback_data.get("content_category", "general")
        content_details = feedback_data.get("content_details", {})
        blocking_scope = feedback_data.get("blocking_scope")
        
        feedback_results = {
            "feedback_type": feedback_type,
            "content_category": content_category,
            "processing_successful": True,
            "actions_taken": []
        }
        
        if not session_id:
            # Create new session if none exists
            patient_id = content_details.get("patient_id", "unknown_patient")
            session_id = await self.session_storage_tool.create_session(patient_id)
            feedback_results["actions_taken"].append("created_new_session")
        
        # Process based on feedback type
        if feedback_type == "positive":
            success = await self.session_storage_tool.add_preference(
                session_id=session_id,
                category=content_category,
                item_name=content_details.get("content_name", "unknown"),
                preference_type="positive",
                context=content_details,
                feedback_source="emoji_feedback"
            )
            if success:
                feedback_results["actions_taken"].append("added_positive_preference")
        
        elif feedback_type == "negative":
            success = await self.session_storage_tool.add_preference(
                session_id=session_id,
                category=content_category,
                item_name=content_details.get("content_name", "unknown"),
                preference_type="negative",
                context=content_details,
                feedback_source="emoji_feedback"
            )
            if success:
                feedback_results["actions_taken"].append("added_negative_preference")
        
        elif feedback_type == "blocked":
            # Handle blocking based on scope
            content_name = content_details.get("content_name", "unknown")
            
            if blocking_scope == "item":
                success = await self.session_storage_tool.add_blocked_content(
                    session_id=session_id,
                    block_type="specific_item",
                    content_identifier=content_name,
                    context=content_details
                )
            elif blocking_scope == "type":
                content_type = content_details.get("content_type", content_category)
                success = await self.session_storage_tool.add_blocked_content(
                    session_id=session_id,
                    block_type="type",
                    content_identifier=content_type,
                    context=content_details
                )
            elif blocking_scope == "category":
                success = await self.session_storage_tool.add_blocked_content(
                    session_id=session_id,
                    block_type="category",
                    content_identifier=content_category,
                    context=content_details
                )
            else:
                # Default to specific item blocking
                success = await self.session_storage_tool.add_blocked_content(
                    session_id=session_id,
                    block_type="specific_item",
                    content_identifier=content_name,
                    context=content_details
                )
            
            if success:
                feedback_results["actions_taken"].append(f"blocked_{blocking_scope or 'item'}")
        
        return feedback_results
    
    async def _update_preference_patterns(self, 
                                         feedback_data: Dict[str, Any],
                                         cultural_profile: Dict[str, Any],
                                         qloo_intelligence: Dict[str, Any],
                                         sensory_content: Dict[str, Any],
                                         session_id: Optional[str]) -> Dict[str, Any]:
        """Update preference patterns based on feedback."""
        
        if not session_id:
            return {"patterns_updated": False, "reason": "no_session_id"}
        
        # Get current positive patterns
        positive_patterns = await self.session_storage_tool.get_positive_patterns(session_id)
        
        # Analyze feedback in context of cultural intelligence
        pattern_analysis = self._analyze_feedback_patterns(
            feedback_data,
            cultural_profile,
            qloo_intelligence
        )
        
        # Check if feedback overrides cultural suggestions
        cultural_overrides = self._identify_cultural_overrides(
            feedback_data,
            cultural_profile,
            qloo_intelligence
        )
        
        return {
            "patterns_updated": True,
            "current_positive_patterns": positive_patterns,
            "pattern_analysis": pattern_analysis,
            "cultural_overrides": cultural_overrides,
            "individual_learning": "preferences_override_demographics"
        }
    
    def _analyze_feedback_patterns(self, 
                                  feedback_data: Dict[str, Any],
                                  cultural_profile: Dict[str, Any],
                                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feedback in context of cultural suggestions."""
        
        content_details = feedback_data.get("content_details", {})
        feedback_type = feedback_data.get("feedback_type")
        
        # Check if this feedback relates to cultural intelligence suggestions
        cultural_connection = content_details.get("cultural_connection")
        qloo_source = content_details.get("qloo_generated", False)
        
        analysis = {
            "feedback_source": "cultural_intelligence" if qloo_source else "other",
            "cultural_accuracy": None,
            "pattern_insights": []
        }
        
        if cultural_connection and qloo_source:
            if feedback_type == "positive":
                analysis["cultural_accuracy"] = "cultural_suggestion_successful"
                analysis["pattern_insights"].append(
                    f"Cultural connection '{cultural_connection}' resonated positively"
                )
            elif feedback_type in ["negative", "blocked"]:
                analysis["cultural_accuracy"] = "cultural_assumption_incorrect"
                analysis["pattern_insights"].append(
                    f"Cultural connection '{cultural_connection}' was rejected - individual preferences override"
                )
        
        return analysis
    
    def _identify_cultural_overrides(self, 
                                   feedback_data: Dict[str, Any],
                                   cultural_profile: Dict[str, Any],
                                   qloo_intelligence: Dict[str, Any]) -> List[str]:
        """Identify when individual feedback overrides cultural assumptions."""
        
        overrides = []
        
        feedback_type = feedback_data.get("feedback_type")
        content_details = feedback_data.get("content_details", {})
        cultural_connection = content_details.get("cultural_connection")
        
        if feedback_type in ["negative", "blocked"] and cultural_connection:
            # Individual rejected a cultural suggestion
            overrides.append(f"Individual rejected cultural suggestion: {cultural_connection}")
            
            # Check what cultural elements were assumed
            heritage_keywords = cultural_profile.get("cultural_elements", {}).get(
                "heritage_elements", {}).get("heritage_keywords", [])
            
            for keyword in heritage_keywords:
                if keyword.lower() in str(cultural_connection).lower():
                    overrides.append(f"Heritage keyword '{keyword}' assumption overridden by individual feedback")
        
        return overrides
    
    async def _learn_from_mobile_experience(self, 
                                           mobile_experience: Dict[str, Any],
                                           feedback_data: Dict[str, Any],
                                           session_id: Optional[str]) -> Dict[str, Any]:
        """Learn from mobile experience effectiveness."""
        
        mobile_learning = {
            "mobile_effectiveness": {},
            "ui_preferences": {},
            "content_preferences": {},
            "caregiver_usage_patterns": {}
        }
        
        # Analyze feedback in context of mobile content structure
        mobile_content = mobile_experience.get("mobile_content", {})
        page_structure = mobile_experience.get("page_structure", {})
        
        feedback_category = feedback_data.get("content_category")
        feedback_type = feedback_data.get("feedback_type")
        
        # Learn about content type effectiveness
        if feedback_category and feedback_type:
            mobile_learning["content_preferences"][feedback_category] = feedback_type
        
        # Learn about page structure effectiveness
        structure_type = page_structure.get("structure_type", "unknown")
        mobile_learning["ui_preferences"]["last_structure_used"] = structure_type
        
        # Note: In a full implementation, we'd track more detailed mobile interaction patterns
        
        return mobile_learning
    
    def _check_cultural_overrides(self, 
                                 feedback_data: Dict[str, Any],
                                 cultural_profile: Dict[str, Any]) -> Dict[str, bool]:
        """Check what cultural assumptions were overridden by individual feedback."""
        
        overrides = {
            "heritage_assumptions_overridden": False,
            "era_assumptions_overridden": False,
            "demographic_assumptions_overridden": False,
            "individual_preferences_prioritized": True
        }
        
        feedback_type = feedback_data.get("feedback_type")
        content_details = feedback_data.get("content_details", {})
        
        if feedback_type in ["negative", "blocked"]:
            # Check if rejected content was based on cultural assumptions
            cultural_connection = content_details.get("cultural_connection", "")
            
            # Check heritage overrides
            heritage_keywords = cultural_profile.get("cultural_elements", {}).get(
                "heritage_elements", {}).get("heritage_keywords", [])
            for keyword in heritage_keywords:
                if keyword.lower() in cultural_connection.lower():
                    overrides["heritage_assumptions_overridden"] = True
                    break
            
            # Check era overrides
            if any(decade in cultural_connection.lower() for decade in ["1940s", "1950s", "1960s", "1970s"]):
                overrides["era_assumptions_overridden"] = True
            
            # Check demographic overrides
            if "age" in cultural_connection.lower() or "demographic" in cultural_connection.lower():
                overrides["demographic_assumptions_overridden"] = True
        
        return overrides
    
    async def _get_current_preferences(self, session_id: Optional[str]) -> Dict[str, Any]:
        """Get current preferences when no new feedback is provided."""
        
        if not session_id:
            return {
                "updated_preferences": {
                    "learning_metadata": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "session_id": None,
                        "feedback_processed": False,
                        "reason": "no_session_id"
                    }
                }
            }
        
        # Get current session data
        session_data = await self.session_storage_tool.get_session(session_id)
        
        if session_data:
            blocked_content = await self.session_storage_tool.get_blocked_content(session_id)
            positive_patterns = await self.session_storage_tool.get_positive_patterns(session_id)
            
            return {
                "updated_preferences": {
                    "learning_metadata": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "session_id": session_id,
                        "feedback_processed": False,
                        "current_preferences_retrieved": True
                    },
                    "current_blocked_content": blocked_content,
                    "current_positive_patterns": positive_patterns,
                    "individual_priority_maintained": True
                }
            }
        else:
            return {
                "updated_preferences": {
                    "learning_metadata": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "session_id": session_id,
                        "feedback_processed": False,
                        "reason": "session_not_found"
                    }
                }
            }
    
    def _create_fallback_preferences(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback preferences when feedback processing fails."""
        
        return {
            "updated_preferences": {
                "learning_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "feedback_processed": False,
                    "mode": "fallback_safe_defaults",
                    "individual_priority_maintained": True
                },
                "fallback_approach": {
                    "principle": "individual_preferences_always_override_demographics",
                    "safety": "no_assumptions_made_about_preferences",
                    "learning": "will_learn_from_individual_feedback_when_available"
                }
            }
        }