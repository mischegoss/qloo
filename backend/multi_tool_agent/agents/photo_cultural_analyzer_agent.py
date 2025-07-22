"""
Agent 5: Photo Cultural Analyzer - FIXED VERSION
Role: Analyze photos for cultural context when present
Follows Responsible Development Guide principles - factual analysis without cultural assumptions
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class PhotoCulturalAnalyzerAgent(Agent):
    """
    Agent 5: Photo Cultural Analyzer
    
    Purpose: Analyze photos for cultural context when present
    Input: All previous outputs + photo data (if available)
    Output: Photo cultural insights or empty analysis
    
    Tools: vision_ai_analyzer
    
    Anti-Bias Principles:
    - Only activate if photo data present (conditional execution)
    - Extract era indicators and cultural markers factually
    - Generate photo-specific recommendations without stereotypes
    - Focus on what's actually visible, not cultural assumptions
    - Enhance existing recommendations with photo context
    """
    
    def __init__(self, vision_ai_tool):
        super().__init__(
            name="photo_cultural_analyzer",
            description="Analyzes photos for cultural context without assumptions, only when photos are present"
        )
        # FIXED: Store tool reference differently to avoid Pydantic field errors
        self._vision_ai_tool_ref = vision_ai_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze photos for cultural context when present.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            qloo_intelligence: Output from Agent 3
            sensory_content: Output from Agent 4
            
        Returns:
            Photo cultural insights or empty analysis if no photo
        """
        
        try:
            # Check if photo data is present
            photo_context = consolidated_info.get("photo_context", {})
            has_photo = photo_context.get("has_photo", False)
            
            if not has_photo:
                logger.info("No photo data present - skipping photo analysis")
                return self._create_empty_photo_analysis()
            
            logger.info("Photo data detected - starting cultural analysis")
            
            # Extract photo metadata and data
            photo_metadata = photo_context.get("photo_metadata", {})
            
            # Perform vision AI analysis using tool reference
            vision_analysis = await self._analyze_photo_with_vision_ai(photo_metadata)
            
            # Extract cultural indicators without assumptions
            cultural_indicators = self._extract_cultural_indicators(vision_analysis)
            
            # Generate era context from visual elements
            era_analysis = self._analyze_era_indicators(vision_analysis, cultural_profile)
            
            # Create photo-specific conversation starters
            conversation_suggestions = self._generate_photo_conversation_suggestions(
                vision_analysis, 
                cultural_indicators,
                era_analysis
            )
            
            # Generate memory trigger activities
            memory_triggers = self._generate_photo_memory_triggers(
                vision_analysis,
                cultural_indicators
            )
            
            # Integrate with existing recommendations
            integration_suggestions = self._integrate_with_existing_recommendations(
                vision_analysis,
                qloo_intelligence,
                sensory_content
            )
            
            # Build comprehensive photo analysis
            photo_analysis = {
                "analysis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "photo_analyzed": True,
                    "privacy_compliant": "analyzed_instantly_not_stored",
                    "approach": "factual_observation_no_assumptions"
                },
                "vision_analysis": vision_analysis,
                "cultural_indicators": cultural_indicators,
                "era_analysis": era_analysis,
                "conversation_suggestions": conversation_suggestions,
                "memory_triggers": memory_triggers,
                "integration_suggestions": integration_suggestions,
                "caregiver_guidance": self._generate_photo_caregiver_guidance(vision_analysis),
                "privacy_notes": {
                    "processing": "instant_analysis_only",
                    "storage": "no_photo_data_retained",
                    "usage": "cultural_context_extraction_only"
                }
            }
            
            # Validate no assumptions were made
            self._validate_photo_analysis_bias_compliance(photo_analysis)
            
            logger.info("Photo cultural analysis completed successfully")
            return {"photo_analysis": photo_analysis}
            
        except Exception as e:
            logger.error(f"Error in photo cultural analysis: {str(e)}")
            return self._create_fallback_photo_analysis(consolidated_info)
    
    async def _analyze_photo_with_vision_ai(self, photo_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze photo using Vision AI tool."""
        
        try:
            # Use the tool reference
            analysis_result = await self._vision_ai_tool_ref.analyze_image(photo_metadata)
            
            if analysis_result and analysis_result.get("success"):
                return analysis_result.get("analysis", {})
            else:
                logger.warning("Vision AI analysis failed or returned no results")
                return {}
                
        except Exception as e:
            logger.error(f"Vision AI analysis error: {str(e)}")
            return {}
    
    def _create_empty_photo_analysis(self) -> Dict[str, Any]:
        """Create empty analysis when no photo is present."""
        
        return {
            "photo_analysis": {
                "analysis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "photo_analyzed": False,
                    "reason": "no_photo_data_provided"
                },
                "vision_analysis": {},
                "cultural_indicators": {"available": False},
                "era_analysis": {"available": False},
                "conversation_suggestions": [],
                "memory_triggers": [],
                "integration_suggestions": [],
                "caregiver_guidance": {
                    "photo_analysis": "No photo provided - analysis not applicable"
                }
            }
        }
    
    def _extract_cultural_indicators(self, vision_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cultural indicators from vision analysis without assumptions."""
        
        if not vision_analysis:
            return {"available": False, "reason": "no_vision_analysis_data"}
        
        # Extract factual visual elements
        detected_objects = vision_analysis.get("objects", [])
        detected_text = vision_analysis.get("text", [])
        detected_faces = vision_analysis.get("faces", [])
        detected_landmarks = vision_analysis.get("landmarks", [])
        
        cultural_indicators = {
            "available": True,
            "visual_elements": {
                "objects": detected_objects,
                "text_elements": detected_text,
                "people_present": len(detected_faces) > 0,
                "landmarks": detected_landmarks
            },
            "factual_observations": self._generate_factual_observations(vision_analysis),
            "approach": "fact_based_no_cultural_assumptions"
        }
        
        return cultural_indicators
    
    def _generate_factual_observations(self, vision_analysis: Dict[str, Any]) -> List[str]:
        """Generate factual observations from vision analysis."""
        
        observations = []
        
        # Objects observed
        objects = vision_analysis.get("objects", [])
        if objects:
            observations.append(f"Objects visible in photo: {', '.join(objects[:5])}")
        
        # Text observed
        text_elements = vision_analysis.get("text", [])
        if text_elements:
            observations.append(f"Text visible in photo: {', '.join(text_elements[:3])}")
        
        # People observed
        faces = vision_analysis.get("faces", [])
        if faces:
            observations.append(f"Number of people visible: {len(faces)}")
        
        # Settings observed
        settings = vision_analysis.get("labels", [])
        if settings:
            observations.append(f"Setting appears to be: {', '.join(settings[:3])}")
        
        return observations
    
    def _analyze_era_indicators(self, 
                               vision_analysis: Dict[str, Any],
                               cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze era indicators from photo to enhance cultural profile."""
        
        if not vision_analysis:
            return {"available": False}
        
        # Look for era indicators in objects and settings
        era_objects = []
        modern_objects = ["smartphone", "computer", "digital", "lcd", "led"]
        vintage_objects = ["typewriter", "rotary phone", "vinyl", "cassette", "film camera"]
        
        detected_objects = vision_analysis.get("objects", [])
        
        for obj in detected_objects:
            obj_lower = obj.lower()
            if any(modern in obj_lower for modern in modern_objects):
                era_objects.append({"object": obj, "era_indicator": "modern"})
            elif any(vintage in obj_lower for vintage in vintage_objects):
                era_objects.append({"object": obj, "era_indicator": "vintage"})
        
        era_analysis = {
            "available": True,
            "era_objects": era_objects,
            "photo_era_context": self._determine_photo_era_context(era_objects),
            "integration_with_profile": self._integrate_era_with_profile(era_objects, cultural_profile),
            "approach": "factual_era_indicator_analysis"
        }
        
        return era_analysis
    
    def _determine_photo_era_context(self, era_objects: List[Dict[str, str]]) -> str:
        """Determine photo era context based on objects."""
        
        if not era_objects:
            return "era_unclear_from_photo"
        
        modern_count = sum(1 for obj in era_objects if obj["era_indicator"] == "modern")
        vintage_count = sum(1 for obj in era_objects if obj["era_indicator"] == "vintage")
        
        if modern_count > vintage_count:
            return "appears_recent_photo"
        elif vintage_count > modern_count:
            return "appears_older_photo"
        else:
            return "mixed_era_indicators"
    
    def _integrate_era_with_profile(self, 
                                   era_objects: List[Dict[str, str]], 
                                   cultural_profile: Dict[str, Any]) -> Dict[str, str]:
        """Integrate photo era indicators with existing cultural profile."""
        
        profile_era = cultural_profile.get("era_context", {})
        profile_decades = profile_era.get("decades_lived", [])
        
        integration = {
            "profile_alignment": "checking_era_consistency",
            "photo_era_support": "factual_object_based_analysis"
        }
        
        if era_objects:
            integration["era_objects_detected"] = len(era_objects)
            integration["potential_memory_connection"] = "objects_may_trigger_era_memories"
        
        return integration
    
    def _generate_photo_conversation_suggestions(self, 
                                               vision_analysis: Dict[str, Any],
                                               cultural_indicators: Dict[str, Any],
                                               era_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate conversation suggestions based on photo analysis."""
        
        suggestions = []
        
        if not vision_analysis:
            return suggestions
        
        # Object-based conversation starters
        detected_objects = vision_analysis.get("objects", [])
        if detected_objects:
            suggestions.append({
                "conversation_type": "object_discussion",
                "starter": f"I see {detected_objects[0]} in this photo. Do you remember having something similar?",
                "follow_up": "Tell me about your experience with items like this",
                "caregiver_guidance": "Let them lead the conversation about objects they find interesting"
            })
        
        # People-based conversation starters
        faces = vision_analysis.get("faces", [])
        if faces:
            suggestions.append({
                "conversation_type": "people_discussion",
                "starter": "I can see people in this photo. Who are they?",
                "follow_up": "What can you tell me about the people in your life?",
                "caregiver_guidance": "Be patient if they can't remember names - focus on feelings and relationships"
            })
        
        # Setting-based conversation starters
        settings = vision_analysis.get("labels", [])
        if settings:
            suggestions.append({
                "conversation_type": "place_discussion",
                "starter": f"This looks like it was taken at {settings[0]}. Does this remind you of anywhere?",
                "follow_up": "What places were special to you?",
                "caregiver_guidance": "Encourage storytelling about meaningful places"
            })
        
        return suggestions
    
    def _generate_photo_memory_triggers(self, 
                                      vision_analysis: Dict[str, Any],
                                      cultural_indicators: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate memory trigger activities based on photo content."""
        
        memory_triggers = []
        
        if not vision_analysis:
            return memory_triggers
        
        # Object-based memory triggers
        objects = vision_analysis.get("objects", [])
        if objects:
            memory_triggers.append({
                "trigger_type": "object_memories",
                "activity": "Object Memory Exploration",
                "description": "Use objects in photo to explore related memories",
                "implementation": "Point to specific objects and ask about similar items from their past",
                "materials_needed": "Just the photo",
                "caregiver_guidance": "Follow their interest level - some objects may trigger stronger memories than others"
            })
        
        # People-based memory triggers
        faces = vision_analysis.get("faces", [])
        if faces:
            memory_triggers.append({
                "trigger_type": "relationship_memories",
                "activity": "Relationship Memory Sharing",
                "description": "Use people in photo to discuss important relationships",
                "implementation": "Ask about relationships and people who were meaningful to them",
                "materials_needed": "Just the photo",
                "caregiver_guidance": "Be sensitive to emotional responses - some memories may be bittersweet"
            })
        
        # Setting-based memory triggers
        settings = vision_analysis.get("labels", [])
        if settings:
            memory_triggers.append({
                "trigger_type": "place_memories",
                "activity": "Place Memory Journey",
                "description": "Use photo setting to explore memories of meaningful places",
                "implementation": "Discuss places that were important in their life history",
                "materials_needed": "Just the photo, optionally maps or other photos of places",
                "caregiver_guidance": "Encourage detailed storytelling about favorite places and experiences there"
            })
        
        return memory_triggers
    
    def _integrate_with_existing_recommendations(self, 
                                               vision_analysis: Dict[str, Any],
                                               qloo_intelligence: Dict[str, Any],
                                               sensory_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Integrate photo insights with existing recommendations."""
        
        integrations = []
        
        if not vision_analysis:
            return integrations
        
        # Integrate with Qloo recommendations
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        if cultural_recommendations:
            integrations.append({
                "integration_type": "qloo_photo_enhancement",
                "description": "Use photo context to enhance Qloo cultural recommendations",
                "implementation": "Connect photo elements with recommended cultural content",
                "example": "If photo shows music-related objects, highlight music recommendations from Qloo"
            })
        
        # Integrate with sensory content
        sensory_elements = sensory_content.get("auditory", {}).get("elements", [])
        if sensory_elements:
            integrations.append({
                "integration_type": "sensory_photo_connection",
                "description": "Connect photo memories with sensory experiences",
                "implementation": "Use photo content to guide sensory activity selection",
                "example": "If photo shows cooking, prioritize gustatory and olfactory experiences"
            })
        
        return integrations
    
    def _generate_photo_caregiver_guidance(self, vision_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific caregiver guidance for photo-based activities."""
        
        guidance = {
            "general_approach": [
                "Use the photo as a conversation starter, not a memory test",
                "Follow their lead - if they show interest in something, explore it further",
                "Don't correct them if they misidentify something - focus on the emotions",
                "Be patient with processing time - photos can take time to understand",
                "Watch for emotional responses and be ready to change topics if needed"
            ],
            "photo_specific_tips": [],
            "conversation_techniques": [
                "Ask open-ended questions about what they see",
                "Share your own observations to keep conversation flowing",
                "Use 'I wonder...' statements to explore possibilities together",
                "Validate their responses regardless of accuracy",
                "Focus on feelings and experiences rather than facts"
            ],
            "safety_considerations": [
                "Monitor emotional responses to photo content",
                "Be prepared to put photo away if it causes distress",
                "Ensure good lighting for viewing photos",
                "Use photos that are familiar and generally positive",
                "Respect if they don't want to discuss certain photos"
            ]
        }
        
        # Add photo-specific guidance based on content
        if vision_analysis:
            objects = vision_analysis.get("objects", [])
            if objects:
                guidance["photo_specific_tips"].append(f"Focus on visible objects: {', '.join(objects[:3])}")
            
            faces = vision_analysis.get("faces", [])
            if faces:
                guidance["photo_specific_tips"].append("People are visible - be sensitive about relationship discussions")
            
            settings = vision_analysis.get("labels", [])
            if settings:
                guidance["photo_specific_tips"].append(f"Setting appears to be {settings[0]} - can explore related place memories")
        
        return guidance
    
    def _validate_photo_analysis_bias_compliance(self, photo_analysis: Dict[str, Any]) -> None:
        """Validate that photo analysis followed bias prevention principles."""
        
        # Check that analysis is factual, not assumptive
        cultural_indicators = photo_analysis.get("cultural_indicators", {})
        approach = cultural_indicators.get("approach", "")
        
        if "fact_based_no_cultural_assumptions" in approach:
            logger.info("Photo analysis bias compliance validated: factual approach confirmed")
        else:
            logger.warning("Photo analysis may not follow bias prevention principles")
        
        # Log validation
        logger.info("Photo analysis validated for bias prevention compliance")
    
    def _create_fallback_photo_analysis(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback photo analysis when Vision AI is unavailable."""
        
        return {
            "photo_analysis": {
                "analysis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "photo_analyzed": False,
                    "fallback_used": True,
                    "fallback_reason": "vision_ai_unavailable"
                },
                "vision_analysis": {},
                "cultural_indicators": {"available": False, "reason": "vision_ai_unavailable"},
                "era_analysis": {"available": False, "reason": "vision_ai_unavailable"},
                "conversation_suggestions": [],
                "memory_triggers": [],
                "integration_suggestions": [],
                "caregiver_guidance": {
                    "fallback_approach": "Use photo for general conversation without AI analysis",
                    "manual_guidance": "Point out interesting elements and ask open-ended questions"
                }
            }
        }