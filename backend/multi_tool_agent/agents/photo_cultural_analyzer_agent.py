"""
Updated Photo Cultural Analyzer Agent
File: backend/multi_tool_agent/agents/photo_cultural_analyzer_agent.py

Now handles photo selection with stored analysis and generates fresh conversation starters.
"""

import logging
import random
from typing import Dict, Any, Optional, List

# Configure logger
logger = logging.getLogger(__name__)

class PhotoCulturalAnalyzerAgent:
    """
    Agent 5: Photo Cultural Analyzer Agent
    
    UPDATED FUNCTIONALITY:
    - Uses pre-processed photo analysis from storage
    - Selects photo of the day with rotation
    - Generates fresh conversation starters aligned with cultural context
    - Integrates stored vision data with current pipeline context
    """
    
    def __init__(self, vision_ai_tool: Optional[Any] = None):
        self.vision_ai_tool = vision_ai_tool
        logger.info("📷 Photo Cultural Analyzer Agent initialized for photo selection")
    
    async def run(self, 
                 consolidated_info: Dict[str, Any],
                 cultural_profile: Dict[str, Any],
                 qloo_intelligence: Dict[str, Any],
                 sensory_content: Dict[str, Any],
                 photo_of_the_day: Optional[str] = None,
                 stored_photo_analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process selected photo with stored analysis and generate culturally-aligned conversation.
        
        NEW APPROACH:
        1. Use stored vision analysis (no real-time processing)
        2. Generate fresh conversation starters using cultural context
        3. Create memory triggers aligned with patient's heritage
        """
        
        try:
            logger.info("🔍 Starting photo cultural analysis with stored data")
            
            # Validate inputs
            if not photo_of_the_day or not stored_photo_analysis:
                return {
                    "photo_analysis": {
                        "status": "skipped",
                        "reason": "no_photo_or_analysis_available"
                    }
                }
            
            # Extract stored vision analysis
            vision_analysis = stored_photo_analysis.get("vision_analysis", {})
            if not vision_analysis:
                logger.warning("No vision analysis found in stored data")
                return {
                    "photo_analysis": {
                        "status": "failed",
                        "reason": "missing_vision_analysis"
                    }
                }
            
            logger.info(f"📷 Processing photo: {photo_of_the_day}")
            logger.info(f"🔍 Vision data: {len(vision_analysis.get('objects', []))} objects, {len(vision_analysis.get('labels', []))} labels")
            
            # Generate cultural context integration
            cultural_integration = self._integrate_cultural_context(
                vision_analysis=vision_analysis,
                cultural_profile=cultural_profile,
                consolidated_info=consolidated_info
            )
            
            # Generate fresh conversation starters (aligned with current cultural context)
            conversation_starters = self._generate_dynamic_conversation_starters(
                vision_analysis=vision_analysis,
                cultural_profile=cultural_profile,
                qloo_intelligence=qloo_intelligence,
                cultural_integration=cultural_integration
            )
            
            # Generate memory triggers
            memory_triggers = self._generate_memory_triggers(
                vision_analysis=vision_analysis,
                cultural_profile=cultural_profile,
                cultural_integration=cultural_integration
            )
            
            # Create era analysis based on cultural profile
            era_analysis = self._analyze_era_context(
                vision_analysis=vision_analysis,
                cultural_profile=cultural_profile
            )
            
            # Compile final photo analysis
            photo_analysis_result = {
                "status": "success",
                "photo_path": photo_of_the_day,
                "analysis_source": "stored_vision_with_dynamic_conversation",
                "vision_analysis": vision_analysis,
                "cultural_integration": cultural_integration,
                "conversation_starters": conversation_starters,
                "memory_triggers": memory_triggers,
                "era_analysis": era_analysis,
                "processing_metadata": {
                    "agent": "photo_cultural_analyzer",
                    "analysis_type": "stored_with_fresh_conversation",
                    "cultural_alignment": True,
                    "conversation_count": len(conversation_starters),
                    "memory_trigger_count": len(memory_triggers)
                }
            }
            
            logger.info(f"✅ Photo analysis completed: {len(conversation_starters)} conversation starters generated")
            
            return {
                "photo_analysis": photo_analysis_result
            }
            
        except Exception as e:
            logger.error(f"❌ Photo cultural analysis failed: {e}")
            return {
                "photo_analysis": {
                    "status": "error",
                    "error": str(e),
                    "photo_path": photo_of_the_day
                }
            }
    
    def _integrate_cultural_context(self, 
                                  vision_analysis: Dict[str, Any],
                                  cultural_profile: Dict[str, Any],
                                  consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Integrate photo content with patient's cultural background."""
        
        integration = {
            "cultural_alignment_detected": False,
            "heritage_connections": [],
            "era_consistency": False,
            "family_context_likely": False
        }
        
        # Extract cultural elements
        heritage = cultural_profile.get("cultural_elements", {}).get("heritage", "")
        era_context = cultural_profile.get("era_context", {})
        
        # Analyze objects for cultural relevance
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        all_content = objects + labels
        
        # Check for heritage-specific items
        heritage_keywords = {
            "Italian": ["pasta", "wine", "church", "family", "cooking", "kitchen"],
            "Irish": ["music", "pub", "green", "family", "celebration"],
            "Mexican": ["family", "celebration", "food", "church", "colorful"],
            "Jewish": ["family", "celebration", "religious", "ceremony", "gathering"],
            "Chinese": ["family", "food", "red", "celebration", "gathering"],
            "German": ["beer", "family", "celebration", "outdoor", "gathering"]
        }
        
        for heritage_type, keywords in heritage_keywords.items():
            if heritage_type.lower() in heritage.lower():
                for keyword in keywords:
                    if any(keyword in item.lower() for item in all_content):
                        integration["heritage_connections"].append({
                            "heritage": heritage_type,
                            "keyword": keyword,
                            "connection_strength": "strong"
                        })
                        integration["cultural_alignment_detected"] = True
        
        # Check for family/gathering context
        family_indicators = ["people", "family", "gathering", "celebration", "home", "kitchen"]
        if any(indicator in item.lower() for item in all_content for indicator in family_indicators):
            integration["family_context_likely"] = True
        
        # Era consistency check
        birth_year = consolidated_info.get("patient_profile", {}).get("birth_year")
        if birth_year and era_context:
            photo_era_indicators = ["vintage", "old", "black and white", "sepia", "formal"]
            if any(indicator in item.lower() for item in all_content for indicator in photo_era_indicators):
                integration["era_consistency"] = True
        
        return integration
    
    def _generate_dynamic_conversation_starters(self, 
                                              vision_analysis: Dict[str, Any],
                                              cultural_profile: Dict[str, Any],
                                              qloo_intelligence: Dict[str, Any],
                                              cultural_integration: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate fresh conversation starters aligned with cultural context."""
        
        starters = []
        heritage = cultural_profile.get("cultural_elements", {}).get("heritage", "")
        first_name = cultural_profile.get("cultural_elements", {}).get("patient_name", "")
        
        # Extract photo content
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        people = vision_analysis.get("people", [])
        activities = vision_analysis.get("activities", [])
        settings = vision_analysis.get("settings", [])
        
        # Generate culturally-informed conversation starters
        
        # Object-based starters with cultural context
        if objects:
            primary_object = objects[0]
            if cultural_integration.get("heritage_connections"):
                heritage_connection = cultural_integration["heritage_connections"][0]
                starters.append({
                    "type": "cultural_object_discussion",
                    "starter": f"I notice {primary_object} in this photo. In {heritage} families, this often brings back special memories. What does this remind you of?",
                    "follow_up": f"Did your family have traditions around {primary_object}?",
                    "cultural_context": heritage_connection["heritage"],
                    "caregiver_guidance": "Encourage storytelling about family traditions and cultural memories"
                })
            else:
                starters.append({
                    "type": "object_memory_discussion",
                    "starter": f"I see {primary_object} in this photo. Does this bring back any memories for you?",
                    "follow_up": "Tell me about times when this was important in your life",
                    "caregiver_guidance": "Let them lead the conversation about personal connections"
                })
        
        # People and family context
        if people and cultural_integration.get("family_context_likely"):
            starters.append({
                "type": "family_cultural_discussion",
                "starter": f"This looks like a wonderful family moment. {heritage} families often have such rich traditions. Who are the important people in this photo?",
                "follow_up": "What family traditions were most meaningful to you?",
                "cultural_context": heritage,
                "caregiver_guidance": "Focus on relationships and feelings rather than specific names if memory is unclear"
            })
        elif people:
            starters.append({
                "type": "people_discussion",
                "starter": "I can see there are people in this photo who were important to you. Tell me about them.",
                "follow_up": "What made your relationships with these people special?",
                "caregiver_guidance": "Be patient if names aren't remembered - focus on emotions and relationships"
            })
        
        # Activity and celebration context
        if activities:
            primary_activity = activities[0]
            if "celebration" in primary_activity.lower() or "ceremony" in primary_activity.lower():
                starters.append({
                    "type": "celebration_cultural_discussion",
                    "starter": f"This looks like a special {primary_activity}. What celebrations were most important in your family?",
                    "follow_up": f"How did your family celebrate special occasions?",
                    "cultural_context": heritage,
                    "caregiver_guidance": "Encourage sharing about meaningful celebrations and traditions"
                })
        
        # Setting-based discussions
        if settings:
            primary_setting = settings[0]
            if "home" in primary_setting.lower() or "kitchen" in primary_setting.lower():
                starters.append({
                    "type": "home_cultural_discussion",
                    "starter": f"This {primary_setting} looks like it held many memories. What was your favorite room in your family home?",
                    "follow_up": "What activities did your family enjoy doing at home?",
                    "cultural_context": heritage,
                    "caregiver_guidance": "Home environments often trigger rich sensory memories"
                })
        
        # Qloo-informed cultural discussions
        qloo_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        if qloo_recommendations and heritage:
            starters.append({
                "type": "qloo_cultural_connection",
                "starter": f"Looking at this photo reminds me that {heritage} culture has such rich traditions. What aspects of your heritage were most important to your family?",
                "follow_up": "Are there traditions you'd like to share or continue?",
                "cultural_context": heritage,
                "caregiver_guidance": "Connect photo memories to broader cultural identity and pride"
            })
        
        # Ensure variety with randomization
        if len(starters) > 3:
            selected_starters = random.sample(starters, 3)
        else:
            selected_starters = starters
        
        # Add general fallback if no specific starters generated
        if not selected_starters:
            selected_starters.append({
                "type": "general_photo_discussion",
                "starter": "This is a beautiful photo. What story does it tell?",
                "follow_up": "What emotions does this photo bring up for you?",
                "caregiver_guidance": "Allow open-ended storytelling and follow their emotional lead"
            })
        
        return selected_starters
    
    def _generate_memory_triggers(self, 
                                vision_analysis: Dict[str, Any],
                                cultural_profile: Dict[str, Any],
                                cultural_integration: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate memory trigger activities based on photo content and cultural context."""
        
        triggers = []
        heritage = cultural_profile.get("cultural_elements", {}).get("heritage", "")
        
        # Extract photo elements
        objects = vision_analysis.get("objects", [])
        labels = vision_analysis.get("labels", [])
        activities = vision_analysis.get("activities", [])
        
        # Cultural heritage-based triggers
        if cultural_integration.get("heritage_connections"):
            heritage_type = cultural_integration["heritage_connections"][0]["heritage"]
            
            cultural_activities = {
                "Italian": ["cooking traditional recipes", "sharing family stories", "listening to Italian music"],
                "Irish": ["listening to traditional music", "sharing folklore", "discussing family heritage"],
                "Mexican": ["exploring traditional crafts", "discussing family celebrations", "sharing cultural recipes"],
                "Jewish": ["discussing family traditions", "sharing holiday memories", "exploring cultural music"],
                "Chinese": ["discussing family values", "exploring traditional arts", "sharing cultural stories"],
                "German": ["discussing family history", "exploring traditional music", "sharing cultural memories"]
            }
            
            if heritage_type in cultural_activities:
                for activity in cultural_activities[heritage_type]:
                    triggers.append({
                        "type": "cultural_heritage_activity",
                        "activity": activity,
                        "cultural_context": heritage_type,
                        "connection_to_photo": "Heritage alignment with photo content"
                    })
        
        # Object-based memory triggers
        if "food" in objects or "cooking" in labels:
            triggers.append({
                "type": "sensory_memory_trigger",
                "activity": "cooking together or discussing favorite family recipes",
                "sensory_focus": "taste and smell memories",
                "connection_to_photo": "Food-related objects detected"
            })
        
        if "music" in objects or "musical" in labels:
            triggers.append({
                "type": "auditory_memory_trigger", 
                "activity": "listening to music from their era or cultural background",
                "sensory_focus": "auditory memories and emotional connections",
                "connection_to_photo": "Musical elements detected"
            })
        
        # Family and social triggers
        if cultural_integration.get("family_context_likely"):
            triggers.append({
                "type": "social_memory_trigger",
                "activity": "sharing stories about family gatherings and traditions",
                "social_focus": "family relationships and shared experiences",
                "connection_to_photo": "Family context detected in photo"
            })
        
        # Ensure at least one trigger
        if not triggers:
            triggers.append({
                "type": "general_reminiscence",
                "activity": "discussing the time period when this photo was taken",
                "focus": "historical and personal context",
                "connection_to_photo": "General photo memory exploration"
            })
        
        return triggers[:3]  # Limit to 3 most relevant triggers
    
    def _analyze_era_context(self, 
                           vision_analysis: Dict[str, Any],
                           cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze photo era context for temporal memory connections."""
        
        era_analysis = {
            "has_era_context": False,
            "estimated_decade": None,
            "era_indicators": [],
            "generation_context": None
        }
        
        # Extract patient's era information
        era_context = cultural_profile.get("era_context", {})
        if era_context:
            era_analysis["has_era_context"] = True
            era_analysis["generation_context"] = era_context.get("generation_context")
            
            # Look for visual era indicators in photo
            labels = vision_analysis.get("labels", [])
            objects = vision_analysis.get("objects", [])
            all_content = labels + objects
            
            era_indicators = []
            for item in all_content:
                if any(indicator in item.lower() for indicator in ["vintage", "old", "classic", "retro", "traditional"]):
                    era_indicators.append(item)
            
            era_analysis["era_indicators"] = era_indicators
            
            # Estimate decade based on patient's formative years
            formative_decades = era_context.get("formative_decades", [])
            if formative_decades:
                # Assume photo is from patient's young adult years
                era_analysis["estimated_decade"] = formative_decades[1] if len(formative_decades) > 1 else formative_decades[0]
        
        return era_analysis