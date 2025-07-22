"""
Agent 5: Photo Cultural Analyzer
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
        self.vision_ai_tool = vision_ai_tool
    
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
            
            # Perform vision AI analysis
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
    
    def _create_empty_photo_analysis(self) -> Dict[str, Any]:
        """Create empty analysis when no photo is present."""
        
        return {
            "photo_analysis": {
                "analysis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "photo_analyzed": False,
                    "reason": "no_photo_data_provided"
                },
                "vision_analysis": {"available": False},
                "cultural_indicators": {"extracted": False},
                "era_analysis": {"available": False},
                "conversation_suggestions": [],
                "memory_triggers": [],
                "integration_suggestions": [],
                "caregiver_guidance": {
                    "photo_opportunity": "Consider adding family photos for enhanced cultural recommendations"
                }
            }
        }
    
    async def _analyze_photo_with_vision_ai(self, photo_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Perform Vision AI analysis on the photo."""
        
        try:
            logger.info("Starting Vision AI photo analysis")
            
            # Extract photo data for analysis
            photo_type = photo_metadata.get("photo_type", "family_photo")
            caregiver_description = photo_metadata.get("caregiver_description", "")
            
            # Perform comprehensive vision analysis
            vision_results = await self.vision_ai_tool.analyze_photo({
                "photo_type": photo_type,
                "caregiver_context": caregiver_description,
                "analysis_focus": [
                    "objects_and_items",
                    "people_and_clothing",
                    "setting_and_environment", 
                    "era_indicators",
                    "cultural_elements",
                    "emotional_context"
                ]
            })
            
            if not vision_results or not vision_results.get("success"):
                logger.warning("Vision AI analysis failed or returned no results")
                return {"available": False, "error": "vision_ai_analysis_failed"}
            
            # Process vision AI results
            processed_results = {
                "available": True,
                "timestamp": datetime.utcnow().isoformat(),
                "photo_type": photo_type,
                "caregiver_description": caregiver_description,
                "detected_elements": {
                    "objects": vision_results.get("objects", []),
                    "people": vision_results.get("people", []),
                    "settings": vision_results.get("settings", []),
                    "clothing_styles": vision_results.get("clothing", []),
                    "activities": vision_results.get("activities", []),
                    "emotions": vision_results.get("emotions", [])
                },
                "technical_indicators": {
                    "photo_quality": vision_results.get("photo_quality", "unknown"),
                    "color_vs_bw": vision_results.get("color_type", "unknown"),
                    "composition_style": vision_results.get("composition", "unknown")
                },
                "confidence_scores": vision_results.get("confidence", {}),
                "raw_vision_data": vision_results  # For debugging if needed
            }
            
            logger.info("Vision AI analysis completed successfully")
            return processed_results
            
        except Exception as e:
            logger.error(f"Vision AI analysis error: {str(e)}")
            return {
                "available": False,
                "error": str(e),
                "fallback_used": True
            }
    
    def _extract_cultural_indicators(self, vision_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Extract cultural indicators from vision analysis WITHOUT assumptions."""
        
        if not vision_analysis.get("available"):
            return {"extracted": False, "reason": "no_vision_analysis"}
        
        detected_elements = vision_analysis.get("detected_elements", {})
        
        # Extract factual cultural elements (no assumptions about meaning)
        cultural_indicators = {
            "extracted": True,
            "approach": "factual_observation_only",
            "visible_elements": {
                "clothing_styles": self._analyze_clothing_styles(detected_elements.get("clothing_styles", [])),
                "objects_and_items": self._analyze_cultural_objects(detected_elements.get("objects", [])),
                "setting_context": self._analyze_setting_context(detected_elements.get("settings", [])),
                "activities_observed": self._analyze_activities(detected_elements.get("activities", [])),
                "people_context": self._analyze_people_context(detected_elements.get("people", []))
            },
            "potential_conversation_topics": self._identify_conversation_opportunities(detected_elements),
            "memory_trigger_possibilities": self._identify_memory_triggers(detected_elements),
            "bias_prevention_note": "All observations are factual - no cultural assumptions made"
        }
        
        return cultural_indicators
    
    def _analyze_clothing_styles(self, clothing_styles: List[str]) -> Dict[str, Any]:
        """Analyze clothing styles for era indicators (factual only)."""
        
        if not clothing_styles:
            return {"available": False}
        
        # Factual era mapping based on clothing styles (no cultural assumptions)
        era_clothing_indicators = {
            "formal_wear": ["suit", "dress", "tie", "formal", "wedding", "celebration"],
            "casual_styles": ["casual", "everyday", "informal", "relaxed"],
            "vintage_indicators": ["vintage", "period", "historical", "retro"],
            "modern_indicators": ["contemporary", "current", "recent", "modern"]
        }
        
        identified_categories = []
        for category, indicators in era_clothing_indicators.items():
            if any(indicator in " ".join(clothing_styles).lower() for indicator in indicators):
                identified_categories.append(category)
        
        return {
            "available": True,
            "detected_styles": clothing_styles,
            "era_categories": identified_categories,
            "conversation_potential": "Ask about clothing memories from that era",
            "approach": "factual_style_analysis_no_cultural_assumptions"
        }
    
    def _analyze_cultural_objects(self, objects: List[str]) -> Dict[str, Any]:
        """Analyze objects for cultural conversation opportunities (no assumptions)."""
        
        if not objects:
            return {"available": False}
        
        # Categorize objects by conversation potential (not cultural assumptions)
        object_categories = {
            "household_items": ["furniture", "kitchen", "home", "domestic"],
            "celebration_items": ["cake", "flowers", "gifts", "decorations"],
            "personal_items": ["jewelry", "accessories", "books", "photographs"],
            "technology_items": ["camera", "radio", "television", "phone"],
            "transportation": ["car", "vehicle", "bicycle", "travel"]
        }
        
        identified_objects = {}
        for category, keywords in object_categories.items():
            category_objects = [obj for obj in objects if any(keyword in obj.lower() for keyword in keywords)]
            if category_objects:
                identified_objects[category] = category_objects
        
        return {
            "available": True,
            "detected_objects": objects,
            "conversation_categories": identified_objects,
            "memory_trigger_potential": "Objects may trigger memories of similar items",
            "approach": "object_based_conversation_starters_no_cultural_assumptions"
        }
    
    def _analyze_setting_context(self, settings: List[str]) -> Dict[str, Any]:
        """Analyze setting context for conversation opportunities."""
        
        if not settings:
            return {"available": False}
        
        # Setting-based conversation opportunities
        setting_categories = {
            "indoor_settings": ["home", "house", "room", "indoor", "interior"],
            "outdoor_settings": ["garden", "park", "outdoor", "nature", "yard"],
            "event_settings": ["celebration", "party", "gathering", "event", "ceremony"],
            "public_places": ["restaurant", "church", "building", "street", "community"]
        }
        
        identified_settings = {}
        for category, keywords in setting_categories.items():
            category_settings = [setting for setting in settings if any(keyword in setting.lower() for keyword in keywords)]
            if category_settings:
                identified_settings[category] = category_settings
        
        return {
            "available": True,
            "detected_settings": settings,
            "setting_categories": identified_settings,
            "conversation_starters": self._generate_setting_conversation_starters(identified_settings),
            "approach": "setting_based_memory_exploration"
        }
    
    def _generate_setting_conversation_starters(self, identified_settings: Dict[str, List[str]]) -> List[str]:
        """Generate conversation starters based on identified settings."""
        
        conversation_starters = []
        
        for category, settings in identified_settings.items():
            if category == "indoor_settings":
                conversation_starters.append("Tell me about your home during this time period")
                conversation_starters.append("What was your favorite room in the house?")
            elif category == "outdoor_settings":
                conversation_starters.append("Do you remember spending time outside like this?")
                conversation_starters.append("What outdoor activities did you enjoy?")
            elif category == "event_settings":
                conversation_starters.append("What special occasions did your family celebrate?")
                conversation_starters.append("Tell me about family gatherings you remember")
            elif category == "public_places":
                conversation_starters.append("What places in your community were important to you?")
                conversation_starters.append("Where did your family like to go together?")
        
        return conversation_starters
    
    def _analyze_activities(self, activities: List[str]) -> Dict[str, Any]:
        """Analyze activities for memory trigger opportunities."""
        
        if not activities:
            return {"available": False}
        
        # Activity-based memory triggers
        activity_memory_connections = {
            "social_activities": ["talking", "gathering", "celebrating", "visiting"],
            "family_activities": ["cooking", "eating", "playing", "caring"],
            "work_activities": ["working", "building", "creating", "helping"],
            "leisure_activities": ["reading", "listening", "watching", "relaxing"]
        }
        
        identified_activities = {}
        for category, keywords in activity_memory_connections.items():
            category_activities = [activity for activity in activities if any(keyword in activity.lower() for keyword in keywords)]
            if category_activities:
                identified_activities[category] = category_activities
        
        return {
            "available": True,
            "detected_activities": activities,
            "activity_categories": identified_activities,
            "memory_trigger_questions": self._generate_activity_memory_questions(identified_activities),
            "approach": "activity_based_memory_exploration"
        }
    
    def _generate_activity_memory_questions(self, identified_activities: Dict[str, List[str]]) -> List[str]:
        """Generate memory trigger questions based on activities."""
        
        memory_questions = []
        
        for category, activities in identified_activities.items():
            if category == "social_activities":
                memory_questions.append("Who did you like to spend time with?")
                memory_questions.append("What social activities did you enjoy most?")
            elif category == "family_activities":
                memory_questions.append("What family activities were special to you?")
                memory_questions.append("How did your family spend time together?")
            elif category == "work_activities":
                memory_questions.append("What kind of work did you do?")
                memory_questions.append("Tell me about your working years")
            elif category == "leisure_activities":
                memory_questions.append("What did you like to do in your free time?")
                memory_questions.append("What hobbies or interests did you have?")
        
        return memory_questions
    
    def _analyze_people_context(self, people: List[str]) -> Dict[str, Any]:
        """Analyze people context for relationship conversations."""
        
        if not people:
            return {"available": False}
        
        # People-based conversation opportunities
        people_categories = {
            "family_indicators": ["family", "relatives", "children", "parents", "siblings"],
            "age_groups": ["children", "adults", "elderly", "young", "older"],
            "group_dynamics": ["couple", "group", "individual", "pair", "gathering"]
        }
        
        identified_people_context = {}
        for category, keywords in people_categories.items():
            people_matches = [person for person in people if any(keyword in person.lower() for keyword in keywords)]
            if people_matches:
                identified_people_context[category] = people_matches
        
        return {
            "available": True,
            "detected_people": people,
            "people_categories": identified_people_context,
            "relationship_conversation_starters": self._generate_relationship_conversations(identified_people_context),
            "approach": "relationship_based_memory_exploration"
        }
    
    def _generate_relationship_conversations(self, people_context: Dict[str, List[str]]) -> List[str]:
        """Generate relationship-based conversation starters."""
        
        conversations = []
        
        for category, people_data in people_context.items():
            if category == "family_indicators":
                conversations.append("Tell me about your family")
                conversations.append("Who was in this photo with you?")
            elif category == "age_groups":
                conversations.append("What do you remember about people in your life?")
                conversations.append("Who were the important people in your community?")
            elif category == "group_dynamics":
                conversations.append("What gatherings did you enjoy?")
                conversations.append("Tell me about times when people came together")
        
        return conversations
    
    def _identify_conversation_opportunities(self, detected_elements: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify conversation opportunities from all detected elements."""
        
        opportunities = []
        
        # Create conversation opportunities based on what's actually visible
        for element_type, elements in detected_elements.items():
            if elements:
                opportunities.append({
                    "element_type": element_type,
                    "conversation_starter": f"I see {element_type} in this photo - tell me about {element_type} from your life",
                    "follow_up": f"What memories do you have related to {element_type}?",
                    "approach": "photo_element_based_conversation"
                })
        
        return opportunities
    
    def _identify_memory_triggers(self, detected_elements: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify memory trigger possibilities from detected elements."""
        
        memory_triggers = []
        
        # Generate memory triggers based on actual photo content
        if detected_elements.get("objects"):
            memory_triggers.append({
                "trigger_type": "object_memories",
                "description": "Use visible objects to trigger memories of similar items",
                "implementation": "Point to objects in photo and ask about similar things in their life",
                "caregiver_guidance": "Let them guide the conversation based on what interests them"
            })
        
        if detected_elements.get("people"):
            memory_triggers.append({
                "trigger_type": "relationship_memories",
                "description": "Use people in photo to discuss relationships and social connections",
                "implementation": "Ask about relationships and people who were important to them",
                "caregiver_guidance": "Be sensitive to emotional responses about people from the past"
            })
        
        if detected_elements.get("settings"):
            memory_triggers.append({
                "trigger_type": "place_memories",
                "description": "Use photo settings to explore memories of places",
                "implementation": "Discuss places that were meaningful in their life",
                "caregiver_guidance": "Encourage storytelling about favorite places and locations"
            })
        
        return memory_triggers
    
    def _analyze_era_indicators(self, 
                               vision_analysis: Dict[str, Any],
                               cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze era indicators from photo to enhance cultural profile."""
        
        if not vision_analysis.get("available"):
            return {"available": False}
        
        # Extract technical era indicators
        technical_indicators = vision_analysis.get("technical_indicators", {})
        detected_elements = vision_analysis.get("detected_elements", {})
        
        # Analyze photo quality and style for era context
        era_context = {
            "available": True,
            "photo_era_indicators": {
                "photo_quality": technical_indicators.get("photo_quality", "unknown"),
                "color_type": technical_indicators.get("color_vs_bw", "unknown"),
                "composition_style": technical_indicators.get("composition_style", "unknown")
            },
            "content_era_indicators": {
                "clothing_era": self._estimate_clothing_era(detected_elements.get("clothing_styles", [])),
                "object_era": self._estimate_object_era(detected_elements.get("objects", [])),
                "setting_era": self._estimate_setting_era(detected_elements.get("settings", []))
            },
            "era_consistency_check": self._check_era_consistency_with_profile(cultural_profile),
            "conversation_enhancement": self._generate_era_conversation_enhancements(),
            "approach": "factual_era_analysis_no_assumptions"
        }
        
        return era_context
    
    def _estimate_clothing_era(self, clothing_styles: List[str]) -> Dict[str, Any]:
        """Estimate era from clothing styles (factual indicators only)."""
        
        if not clothing_styles:
            return {"available": False}
        
        # Factual clothing era indicators (not assumptions)
        era_indicators = {
            "formal_traditional": ["suit", "formal dress", "hat", "gloves"],
            "casual_modern": ["casual", "informal", "contemporary"],
            "vintage_style": ["vintage", "period", "classic", "traditional"]
        }
        
        detected_eras = []
        for era, indicators in era_indicators.items():
            if any(indicator in " ".join(clothing_styles).lower() for indicator in indicators):
                detected_eras.append(era)
        
        return {
            "available": True,
            "detected_clothing_eras": detected_eras,
            "clothing_styles": clothing_styles,
            "conversation_potential": "Discuss clothing and fashion from that time period"
        }
    
    def _estimate_object_era(self, objects: List[str]) -> Dict[str, Any]:
        """Estimate era from objects (factual indicators only)."""
        
        if not objects:
            return {"available": False}
        
        # Technology and object era indicators
        technology_eras = {
            "pre_digital": ["radio", "record player", "film camera", "typewriter"],
            "early_digital": ["cassette", "vhs", "early computer", "digital camera"],
            "modern_tech": ["smartphone", "laptop", "tablet", "digital device"]
        }
        
        detected_tech_eras = []
        for era, tech_items in technology_eras.items():
            if any(item in " ".join(objects).lower() for item in tech_items):
                detected_tech_eras.append(era)
        
        return {
            "available": True,
            "detected_object_eras": detected_tech_eras,
            "era_objects": objects,
            "conversation_potential": "Discuss technology and objects from that era"
        }
    
    def _estimate_setting_era(self, settings: List[str]) -> Dict[str, Any]:
        """Estimate era from settings (factual indicators only)."""
        
        if not settings:
            return {"available": False}
        
        # Setting era indicators
        setting_eras = {
            "traditional_settings": ["formal dining", "traditional home", "classic interior"],
            "modern_settings": ["contemporary", "modern", "updated", "current"],
            "vintage_settings": ["vintage", "period", "historical", "retro"]
        }
        
        detected_setting_eras = []
        for era, setting_indicators in setting_eras.items():
            if any(indicator in " ".join(settings).lower() for indicator in setting_indicators):
                detected_setting_eras.append(era)
        
        return {
            "available": True,
            "detected_setting_eras": detected_setting_eras,
            "era_settings": settings,
            "conversation_potential": "Discuss homes and places from that time period"
        }
    
    def _check_era_consistency_with_profile(self, cultural_profile: Dict[str, Any]) -> Dict[str, str]:
        """Check if photo era indicators are consistent with cultural profile."""
        
        era_context = cultural_profile.get("era_context", {})
        profile_birth_year = era_context.get("birth_year")
        profile_decades = era_context.get("decades_lived", [])
        
        consistency_check = {
            "profile_era_available": bool(profile_birth_year),
            "photo_era_consistency": "requires_analysis",
            "enhancement_opportunity": "photo_provides_additional_era_context"
        }
        
        if profile_birth_year:
            consistency_check["profile_birth_year"] = profile_birth_year
            consistency_check["profile_decades"] = profile_decades
            consistency_check["integration_note"] = "Photo era indicators can enhance existing profile context"
        
        return consistency_check
    
    def _generate_era_conversation_enhancements(self) -> List[Dict[str, str]]:
        """Generate era-based conversation enhancements from photo."""
        
        return [
            {
                "conversation_type": "photo_era_exploration",
                "starter": "This photo looks like it was taken during [era] - what do you remember about that time?",
                "approach": "Use photo as window into time period",
                "caregiver_guidance": "Let the photo guide the conversation about that era"
            },
            {
                "conversation_type": "era_comparison",
                "starter": "How were things different during the time of this photo?",
                "approach": "Compare photo era to other time periods they lived through",
                "caregiver_guidance": "Encourage comparisons between different decades they experienced"
            },
            {
                "conversation_type": "photo_context_exploration",
                "starter": "Tell me about what was happening in your life when this photo was taken",
                "approach": "Use photo as anchor for personal timeline exploration",
                "caregiver_guidance": "Help them place the photo in the context of their life story"
            }
        ]
    
    def _generate_photo_conversation_suggestions(self, 
                                               vision_analysis: Dict[str, Any],
                                               cultural_indicators: Dict[str, Any],
                                               era_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate photo-specific conversation suggestions."""
        
        if not vision_analysis.get("available"):
            return []
        
        conversation_suggestions = []
        
        # Generate conversations based on what's actually visible
        detected_elements = vision_analysis.get("detected_elements", {})
        
        # Object-based conversations
        if detected_elements.get("objects"):
            conversation_suggestions.append({
                "conversation_type": "object_exploration",
                "starter": "I can see [specific objects] in this photo",
                "questions": [
                    "Do you remember having similar objects?",
                    "What do these objects remind you of?",
                    "Tell me about [specific object] from your life"
                ],
                "caregiver_implementation": {
                    "approach": "Point to specific objects in the photo",
                    "guidance": "Let them guide which objects interest them most",
                    "follow_up": "Ask for stories about similar objects from their life"
                }
            })
        
        # People-based conversations
        if detected_elements.get("people"):
            conversation_suggestions.append({
                "conversation_type": "relationship_exploration",
                "starter": "I can see people in this photo",
                "questions": [
                    "Who are the people in this photo?",
                    "What was happening when this was taken?",
                    "Tell me about the relationships between these people"
                ],
                "caregiver_implementation": {
                    "approach": "Ask gently about relationships and connections",
                    "sensitivity": "Be prepared for emotional responses",
                    "validation": "All memories and relationships are valuable"
                }
            })
        
        # Setting-based conversations
        if detected_elements.get("settings"):
            conversation_suggestions.append({
                "conversation_type": "place_exploration",
                "starter": "This photo was taken in [setting description]",
                "questions": [
                    "Where was this photo taken?",
                    "What do you remember about this place?",
                    "What other places were important to you?"
                ],
                "caregiver_implementation": {
                    "approach": "Use the photo setting as starting point for place memories",
                    "expansion": "Encourage stories about other meaningful places",
                    "connection": "Connect to current places they find meaningful"
                }
            })
        
        # Activity-based conversations
        if detected_elements.get("activities"):
            conversation_suggestions.append({
                "conversation_type": "activity_exploration",
                "starter": "It looks like [activity] was happening in this photo",
                "questions": [
                    "What was the occasion for this photo?",
                    "What activities did you enjoy doing?",
                    "Tell me about similar celebrations or gatherings"
                ],
                "caregiver_implementation": {
                    "approach": "Use visible activities to explore life experiences",
                    "encouragement": "Celebrate all activities and experiences they share",
                    "connection": "Link to current activities they might enjoy"
                }
            })
        
        return conversation_suggestions
    
    def _generate_photo_memory_triggers(self, 
                                       vision_analysis: Dict[str, Any],
                                       cultural_indicators: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate memory trigger activities based on photo analysis."""
        
        if not vision_analysis.get("available"):
            return []
        
        memory_triggers = []
        
        detected_elements = vision_analysis.get("detected_elements", {})
        
        # Create memory triggers based on actual photo content
        memory_triggers.append({
            "trigger_type": "photo_storytelling",
            "activity": "Tell the story of this photo",
            "implementation": {
                "setup": "Display the photo where they can see it clearly",
                "approach": "Ask them to tell you everything they remember about this photo",
                "patience": "Give them time to process and remember",
                "encouragement": "Celebrate any details they share"
            },
            "caregiver_guidance": {
                "emotional_support": "Be prepared for emotional responses to memories",
                "validation": "All memories are valuable, even if details vary",
                "documentation": "Consider recording their stories about the photo"
            }
        })
        
        if detected_elements.get("objects"):
            memory_triggers.append({
                "trigger_type": "object_memory_exploration",
                "activity": "Explore memories triggered by objects in the photo",
                "implementation": {
                    "focus": "Point to specific objects and ask about memories",
                    "examples": "Ask about similar objects from their life",
                    "expansion": "Use objects as starting points for broader life stories"
                },
                "caregiver_guidance": {
                    "specificity": "Be specific about which objects you're discussing",
                    "patience": "Allow time for memories to surface",
                    "follow_through": "Consider finding similar objects for tactile exploration"
                }
            })
        
        if detected_elements.get("people"):
            memory_triggers.append({
                "trigger_type": "relationship_memory_exploration",
                "activity": "Explore relationship memories from the photo",
                "implementation": {
                    "identification": "Ask about people in the photo if they're comfortable sharing",
                    "relationships": "Discuss relationships and connections",
                    "expansion": "Talk about other important people in their life"
                },
                "caregiver_guidance": {
                    "sensitivity": "Be gentle with questions about people who may no longer be alive",
                    "celebration": "Celebrate all relationships and connections they share",
                    "present_connection": "Connect past relationships to current meaningful connections"
                }
            })
        
        return memory_triggers
    
    def _integrate_with_existing_recommendations(self, 
                                               vision_analysis: Dict[str, Any],
                                               qloo_intelligence: Dict[str, Any],
                                               sensory_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Integrate photo insights with existing recommendations."""
        
        if not vision_analysis.get("available"):
            return []
        
        integration_suggestions = []
        
        # Enhance musical experiences with photo context
        sensory_content_data = sensory_content.get("sensory_content", {})
        auditory_content = sensory_content_data.get("auditory", {})
        
        if auditory_content.get("available"):
            integration_suggestions.append({
                "integration_type": "photo_enhanced_music",
                "description": "Combine photo viewing with musical experiences",
                "implementation": {
                    "setup": "Display the photo while playing culturally relevant music",
                    "interaction": "Ask about music from the time period of the photo",
                    "enhancement": "Use photo era to guide music selection"
                },
                "caregiver_guidance": {
                    "timing": "Introduce music after photo conversation is established",
                    "observation": "Watch for positive responses to the combined experience",
                    "flexibility": "Adjust music based on photo-triggered memories"
                }
            })
        
        # Enhance cooking experiences with photo context
        gustatory_content = sensory_content_data.get("gustatory", {})
        if gustatory_content.get("available"):
            integration_suggestions.append({
                "integration_type": "photo_enhanced_cooking",
                "description": "Use photo context to enhance cooking experiences",
                "implementation": {
                    "recipe_selection": "Choose recipes that connect to photo era or setting",
                    "storytelling": "Share photo stories while cooking together",
                    "memory_connection": "Use cooking to explore food memories from photo era"
                },
                "caregiver_guidance": {
                    "cultural_connection": "Connect cooking to stories from the photo",
                    "sensory_enhancement": "Use cooking smells to enhance photo memories",
                    "shared_experience": "Create new memories while honoring past ones"
                }
            })
        
        # Enhance conversation experiences
        integration_suggestions.append({
            "integration_type": "photo_enhanced_conversation",
            "description": "Use photo as anchor for broader cultural conversations",
            "implementation": {
                "starting_point": "Begin conversations with photo observations",
                "expansion": "Use photo elements to explore broader life stories",
                "connection": "Connect photo memories to current experiences"
            },
            "caregiver_guidance": {
                "patient_approach": "Let photo guide the pace and direction of conversation",
                "validation": "Celebrate all memories and stories that emerge",
                "documentation": "Consider documenting stories for family preservation"
            }
        })
        
        return integration_suggestions
    
    def _generate_photo_caregiver_guidance(self, vision_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive caregiver guidance for photo-based activities."""
        
        return {
            "photo_preparation": {
                "display": "Ensure photo is clearly visible and well-lit",
                "comfort": "Create comfortable seating and calm environment",
                "timing": "Choose times when they are alert and relaxed",
                "backup_plan": "Have other photos available if this one doesn't resonate"
            },
            "conversation_approach": {
                "starting": "Begin with simple observations about what you see in the photo",
                "questions": "Ask open-ended questions rather than yes/no questions",
                "patience": "Allow plenty of time for memories to surface",
                "validation": "Accept all responses and memories as valuable"
            },
            "emotional_considerations": {
                "sensitivity": "Be prepared for emotional responses to photo memories",
                "support": "Provide comfort if memories bring up sadness or loss",
                "celebration": "Celebrate positive memories and connections",
                "presence": "Your patient, caring presence is the most important element"
            },
            "practical_tips": {
                "photo_quality": "Ensure photo is clear enough for them to see details",
                "duration": "Keep sessions to 15-30 minutes unless they want to continue",
                "documentation": "Consider recording their stories about the photo",
                "follow_up": "Use successful photo sessions to guide future activities"
            },
            "safety_and_comfort": {
                "physical_comfort": "Ensure they can see the photo without strain",
                "emotional_safety": "Stop if the photo causes distress",
                "autonomy": "Let them guide how much they want to share",
                "respect": "Honor their memories and experiences"
            }
        }
    
    def _validate_photo_analysis_bias_compliance(self, photo_analysis: Dict[str, Any]) -> None:
        """Validate that photo analysis doesn't introduce cultural bias."""
        
        # Check for cultural stereotyping in analysis
        bias_indicators = [
            "typical", "traditional", "authentic", "cultural stereotype",
            "must be", "obviously", "clearly cultural"
        ]
        
        analysis_text = str(photo_analysis).lower()
        
        detected_bias = []
        for indicator in bias_indicators:
            if indicator in analysis_text:
                detected_bias.append(indicator)
        
        if detected_bias:
            logger.warning(f"Potential cultural bias detected in photo analysis: {detected_bias}")
        
        # Verify factual approach
        factual_indicators = [
            "factual", "observed", "visible", "detected", "appears",
            "no_assumptions", "individual", "caregiver_guided"
        ]
        
        factual_count = sum(1 for indicator in factual_indicators if indicator in analysis_text)
        
        if factual_count < 3:
            logger.warning("Insufficient factual language in photo analysis")
        
        # Check conversation suggestions for bias
        conversation_suggestions = photo_analysis.get("conversation_suggestions", [])
        for suggestion in conversation_suggestions:
            suggestion_text = str(suggestion).lower()
            if any(bias in suggestion_text for bias in bias_indicators):
                logger.warning(f"Potential bias in conversation suggestion: {suggestion.get('conversation_type', 'unknown')}")
        
        logger.info("Photo analysis bias compliance validation completed")
    
    def _create_fallback_photo_analysis(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback photo analysis when processing fails."""
        
        return {
            "photo_analysis": {
                "analysis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "photo_analyzed": False,
                    "mode": "fallback_safe_defaults",
                    "reason": "photo_analysis_failed"
                },
                "vision_analysis": {"available": False, "error": "analysis_failed"},
                "cultural_indicators": {"extracted": False},
                "era_analysis": {"available": False},
                "conversation_suggestions": [
                    {
                        "conversation_type": "general_photo_exploration",
                        "starter": "Tell me about this photo",
                        "questions": ["What do you see in this photo?", "What does this photo remind you of?"],
                        "caregiver_implementation": {
                            "approach": "Use general photo conversation techniques",
                            "guidance": "Let them guide the conversation about what they see"
                        }
                    }
                ],
                "memory_triggers": [
                    {
                        "trigger_type": "basic_photo_storytelling",
                        "activity": "Ask them to tell you about the photo",
                        "implementation": {
                            "approach": "Simple, open-ended questions about the photo",
                            "patience": "Allow time for them to process and respond"
                        }
                    }
                ],
                "integration_suggestions": [],
                "caregiver_guidance": {
                    "fallback_approach": "Use basic photo conversation techniques",
                    "flexibility": "Adapt based on their response to the photo"
                }
            }
        }