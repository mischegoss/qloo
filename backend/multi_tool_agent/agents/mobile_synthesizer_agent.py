"""
Agent 6: Mobile Synthesizer - COMPLETELY FIXED VERSION
Role: Package all content for mobile caregiver experience
Fixes: Proper content population, comprehensive fallback content, robust error handling
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class MobileSynthesizerAgent(Agent):
    """
    Agent 6: Mobile Synthesizer - COMPLETELY FIXED
    
    FIXED ISSUES:
    - Content arrays are now properly populated from all sources
    - Comprehensive fallback content when sources are empty
    - Enhanced content validation and error handling
    - Better integration of all agent outputs
    - Guaranteed non-empty mobile experience
    """
    
    def __init__(self):
        super().__init__(
            name="mobile_synthesizer",
            description="Synthesizes all content into guaranteed non-empty mobile caregiver experience"
        )
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize all content into mobile caregiver experience with guaranteed content.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2  
            qloo_intelligence: Output from Agent 3
            sensory_content: Output from Agent 4
            photo_analysis: Output from Agent 5
            
        Returns:
            Complete mobile experience package with guaranteed content
        """
        
        try:
            logger.info("Starting mobile synthesis with comprehensive content validation")
            
            # Extract request context and metadata
            request_context = consolidated_info.get("request_context", {})
            request_type = request_context.get("request_type", "dashboard")
            session_metadata = consolidated_info.get("session_metadata", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            
            # ENHANCED: Validate all input sources
            source_validation = self._validate_all_sources(
                cultural_profile, qloo_intelligence, sensory_content, photo_analysis
            )
            
            # Determine mobile page structure based on request type
            page_structure = self._determine_page_structure(request_type)
            
            # CRITICAL FIX: Synthesize content with guaranteed population
            mobile_content = self._synthesize_guaranteed_mobile_content(
                request_type,
                cultural_profile,
                qloo_intelligence,
                sensory_content,
                photo_analysis,
                source_validation
            )
            
            # Generate comprehensive caregiver implementation guide
            caregiver_guide = self._generate_comprehensive_caregiver_guide(
                mobile_content,
                request_type,
                feedback_patterns
            )
            
            # Create cultural context explanations
            cultural_context_explanations = self._create_cultural_context_explanations(
                cultural_profile,
                qloo_intelligence,
                photo_analysis
            )
            
            # Structure feedback collection points
            feedback_collection = self._structure_enhanced_feedback_collection(request_type, mobile_content)
            
            # Generate mobile accessibility features
            accessibility_features = self._generate_accessibility_features(mobile_content)
            
            # Create emergency and fallback options
            emergency_options = self._create_emergency_fallback_options(request_type)
            
            # Build complete mobile experience with validation
            mobile_experience = {
                "synthesis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "page_structure": page_structure["structure_type"],
                    "content_sources": self._document_content_sources(qloo_intelligence, sensory_content, photo_analysis),
                    "source_validation": source_validation,
                    "caregiver_authority": "maintained_throughout",
                    "individual_focus": "prioritized",
                    "cultural_approach": "enhancement_not_direction",
                    "guaranteed_content": True
                },
                "page_structure": page_structure,
                "mobile_content": mobile_content,
                "caregiver_guide": caregiver_guide,
                "cultural_context_explanations": cultural_context_explanations,
                "feedback_collection": feedback_collection,
                "accessibility_features": accessibility_features,
                "emergency_options": emergency_options,
                "implementation_priority": {
                    "primary_focus": "individual_response_and_comfort",
                    "secondary_focus": "cultural_enhancement_opportunities",
                    "safety_first": "stop_if_any_negative_response",
                    "flexibility": "adapt_based_on_real_time_feedback"
                }
            }
            
            # CRITICAL: Validate mobile experience has content
            content_validation = self._validate_mobile_content_completeness(mobile_experience)
            
            if not content_validation["has_content"]:
                logger.error("Mobile experience validation failed - creating emergency fallback")
                return self._create_emergency_mobile_experience(consolidated_info)
            
            # Validate caregiver authority maintenance
            self._validate_caregiver_authority_compliance(mobile_experience)
            
            logger.info(f"✅ Mobile synthesis completed successfully with {content_validation['content_count']} content items")
            return {"mobile_experience": mobile_experience}
            
        except Exception as e:
            logger.error(f"Critical error in mobile synthesis: {str(e)}")
            return self._create_emergency_mobile_experience(consolidated_info)
    
    def _validate_all_sources(self, 
                             cultural_profile: Dict[str, Any],
                             qloo_intelligence: Dict[str, Any], 
                             sensory_content: Dict[str, Any],
                             photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all input sources and document what's available."""
        
        validation = {
            "cultural_profile_available": bool(cultural_profile.get("cultural_elements", {}).get("has_cultural_info")),
            "qloo_recommendations_available": False,
            "sensory_content_available": False,
            "photo_analysis_available": bool(photo_analysis.get("analysis_metadata", {}).get("photo_analyzed")),
            "content_sources": []
        }
        
        # Validate Qloo intelligence
        qloo_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        if qloo_recommendations:
            for entity_type, rec_data in qloo_recommendations.items():
                if isinstance(rec_data, dict) and rec_data.get("available") and rec_data.get("entities"):
                    validation["qloo_recommendations_available"] = True
                    validation["content_sources"].append(f"qloo_{entity_type}")
                    break
        
        # Validate sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        if isinstance(sensory_content_data, dict):
            for sense, content in sensory_content_data.items():
                if isinstance(content, dict) and content.get("available") and content.get("elements"):
                    validation["sensory_content_available"] = True
                    validation["content_sources"].append(f"sensory_{sense}")
        
        logger.info(f"Source validation: Cultural={validation['cultural_profile_available']}, "
                   f"Qloo={validation['qloo_recommendations_available']}, "
                   f"Sensory={validation['sensory_content_available']}, "
                   f"Photo={validation['photo_analysis_available']}")
        
        return validation
    
    def _synthesize_guaranteed_mobile_content(self, 
                                            request_type: str,
                                            cultural_profile: Dict[str, Any],
                                            qloo_intelligence: Dict[str, Any],
                                            sensory_content: Dict[str, Any],
                                            photo_analysis: Dict[str, Any],
                                            source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize mobile content with guaranteed non-empty arrays."""
        
        logger.info(f"Synthesizing guaranteed content for {request_type}")
        
        # CRITICAL FIX: Build content with multiple fallback layers
        mobile_content = {
            "content_synthesis_approach": "guaranteed_content_with_multiple_fallbacks",
            "primary_content": {},
            "enhancement_content": {},
            "caregiver_implementation": {},
            "cultural_intelligence_insights": {},
            "individual_customization_options": {},
            "anti_bias_safeguards": {
                "individual_preferences_override": "all_suggestions_are_starting_points",
                "caregiver_authority": "caregiver_makes_all_decisions",
                "cultural_approach": "enhancement_not_prescription",
                "adaptation_required": "customize_based_on_individual_response"
            }
        }
        
        # LAYER 1: Try to build from successful sources
        try:
            mobile_content["primary_content"] = self._build_guaranteed_primary_content(
                request_type, qloo_intelligence, sensory_content, source_validation
            )
        except Exception as e:
            logger.warning(f"Primary content synthesis failed: {e}")
            mobile_content["primary_content"] = self._create_fallback_primary_content(request_type)
        
        # LAYER 2: Enhancement content with fallbacks
        try:
            mobile_content["enhancement_content"] = self._build_guaranteed_enhancement_content(
                cultural_profile, photo_analysis, qloo_intelligence, source_validation
            )
        except Exception as e:
            logger.warning(f"Enhancement content synthesis failed: {e}")
            mobile_content["enhancement_content"] = self._create_fallback_enhancement_content()
        
        # LAYER 3: Implementation guidance
        try:
            mobile_content["caregiver_implementation"] = self._build_implementation_content(
                sensory_content, mobile_content["primary_content"]
            )
        except Exception as e:
            logger.warning(f"Implementation content synthesis failed: {e}")
            mobile_content["caregiver_implementation"] = self._create_fallback_implementation_content()
        
        # LAYER 4: Cultural insights
        mobile_content["cultural_intelligence_insights"] = self._build_cultural_insights(
            qloo_intelligence, cultural_profile, photo_analysis, source_validation
        )
        
        # LAYER 5: Customization options
        mobile_content["individual_customization_options"] = self._build_customization_options(request_type)
        
        # FINAL VALIDATION: Ensure we have content
        if self._is_mobile_content_empty(mobile_content):
            logger.error("All content synthesis failed - using emergency content")
            mobile_content = self._create_emergency_mobile_content(request_type)
        
        return mobile_content
    
    def _build_guaranteed_primary_content(self, 
                                        request_type: str,
                                        qloo_intelligence: Dict[str, Any],
                                        sensory_content: Dict[str, Any],
                                        source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Build primary content with multiple fallback strategies."""
        
        if request_type == "dashboard":
            return self._create_guaranteed_dashboard_content(
                qloo_intelligence, sensory_content, source_validation
            )
        elif request_type == "meal":
            return self._create_guaranteed_meal_content(sensory_content, source_validation)
        elif request_type == "conversation":
            return self._create_guaranteed_conversation_content(sensory_content, qloo_intelligence, source_validation)
        elif request_type == "music":
            return self._create_guaranteed_music_content(sensory_content, qloo_intelligence, source_validation)
        elif request_type == "video":
            return self._create_guaranteed_video_content(sensory_content, qloo_intelligence, source_validation)
        else:
            return self._create_guaranteed_general_content(sensory_content, qloo_intelligence, source_validation)
    
    def _create_guaranteed_dashboard_content(self, 
                                           qloo_intelligence: Dict[str, Any],
                                           sensory_content: Dict[str, Any],
                                           source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create dashboard content with guaranteed population."""
        
        dashboard_content = {
            "content_type": "comprehensive_dashboard",
            "today_highlights": [],
            "quick_activities": [],
            "multi_sensory_experiences": {},
            "cultural_discoveries": []
        }
        
        # STRATEGY 1: Extract from sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        if isinstance(sensory_content_data, dict):
            for sense, content in sensory_content_data.items():
                if isinstance(content, dict) and content.get("available") and content.get("elements"):
                    elements = content.get("elements", [])
                    for element in elements[:2]:  # Top 2 per sense
                        dashboard_content["today_highlights"].append({
                            "sensory_domain": sense,
                            "activity": element.get("content_subtype", f"{sense}_activity"),
                            "title": element.get("activity", element.get("name", f"{sense.capitalize()} Experience")),
                            "quick_description": self._create_quick_description(element, sense),
                            "implementation_time": self._estimate_implementation_time(element),
                            "caregiver_preparation": self._extract_preparation_steps(element),
                            "individual_customization": "Adapt based on their response and preferences"
                        })
        
        # STRATEGY 2: Extract quick activities from sensory content
        dashboard_content["quick_activities"] = self._extract_guaranteed_quick_activities(sensory_content_data)
        
        # STRATEGY 3: Extract cultural discoveries from Qloo
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        if cultural_recommendations:
            for entity_type, recommendations in cultural_recommendations.items():
                if isinstance(recommendations, dict) and recommendations.get("available") and recommendations.get("entities"):
                    entities = recommendations.get("entities", [])
                    for entity in entities[:2]:  # Top 2 per type
                        dashboard_content["cultural_discoveries"].append({
                            "discovery_type": recommendations.get("entity_type_category", "cultural"),
                            "title": entity.get("name", "Cultural Discovery"),
                            "why_suggested": "Based on cultural intelligence and individual context",
                            "how_to_explore": entity.get("caregiver_guidance", {}).get("implementation", "Explore together"),
                            "cultural_connection": entity.get("cultural_context", {}).get("why_suggested", "Cultural exploration"),
                            "individual_note": "Use this as a starting point - customize based on their interests"
                        })
        
        # STRATEGY 4: Multi-sensory experiences
        cross_sensory_experiences = sensory_content.get("cross_sensory_experiences", [])
        if cross_sensory_experiences:
            dashboard_content["multi_sensory_experiences"] = {
                "available": True,
                "experiences": cross_sensory_experiences[:3]  # Top 3
            }
        
        # CRITICAL FALLBACK: Ensure we have content
        total_items = (len(dashboard_content["today_highlights"]) + 
                      len(dashboard_content["quick_activities"]) + 
                      len(dashboard_content["cultural_discoveries"]))
        
        if total_items < 3:
            logger.warning(f"Dashboard content insufficient ({total_items} items) - adding guaranteed fallbacks")
            dashboard_content = self._add_guaranteed_dashboard_fallbacks(dashboard_content)
        
        logger.info(f"Dashboard content created: {len(dashboard_content['today_highlights'])} highlights, "
                   f"{len(dashboard_content['quick_activities'])} quick activities, "
                   f"{len(dashboard_content['cultural_discoveries'])} discoveries")
        
        return dashboard_content
    
    def _add_guaranteed_dashboard_fallbacks(self, dashboard_content: Dict[str, Any]) -> Dict[str, Any]:
        """Add guaranteed fallback content to dashboard."""
        
        # Ensure minimum highlights
        if len(dashboard_content["today_highlights"]) < 2:
            fallback_highlights = [
                {
                    "sensory_domain": "auditory",
                    "activity": "music_conversation",
                    "title": "Music Memory Conversation",
                    "quick_description": "Talk about favorite songs and music memories",
                    "implementation_time": "10-20 minutes",
                    "caregiver_preparation": ["Choose quiet time together", "Think of music topics"],
                    "individual_customization": "Focus on music they've mentioned enjoying"
                },
                {
                    "sensory_domain": "visual",
                    "activity": "photo_viewing",
                    "title": "Family Photo Time",
                    "quick_description": "Look at family photos and share memories",
                    "implementation_time": "15-30 minutes",
                    "caregiver_preparation": ["Gather family photos", "Ensure good lighting"],
                    "individual_customization": "Use photos that usually bring positive reactions"
                }
            ]
            
            needed = 2 - len(dashboard_content["today_highlights"])
            dashboard_content["today_highlights"].extend(fallback_highlights[:needed])
        
        # Ensure minimum quick activities
        if len(dashboard_content["quick_activities"]) < 3:
            fallback_quick = [
                {
                    "title": "Gentle Hand Massage",
                    "duration": "5-10 minutes",
                    "preparation": "Gentle lotion if no allergies",
                    "description": "Comforting tactile experience"
                },
                {
                    "title": "Nature Sounds",
                    "duration": "10+ minutes",
                    "preparation": "Smartphone or music device",
                    "description": "Gentle background sounds"
                },
                {
                    "title": "Simple Conversation",
                    "duration": "5-20 minutes",
                    "preparation": "No special preparation needed",
                    "description": "Talk about their day or feelings"
                }
            ]
            
            needed = 3 - len(dashboard_content["quick_activities"])
            dashboard_content["quick_activities"].extend(fallback_quick[:needed])
        
        # Ensure minimum cultural discoveries
        if len(dashboard_content["cultural_discoveries"]) < 1:
            dashboard_content["cultural_discoveries"].append({
                "discovery_type": "general",
                "title": "Meaningful Conversations",
                "why_suggested": "Human connection is universally important",
                "how_to_explore": "Ask open-ended questions about their experiences and feelings",
                "cultural_connection": "Personal stories and memories",
                "individual_note": "Let them guide the conversation topics"
            })
        
        return dashboard_content
    
    def _extract_guaranteed_quick_activities(self, sensory_content_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract quick activities with guaranteed minimum content."""
        
        quick_activities = []
        
        if isinstance(sensory_content_data, dict):
            for sense, content in sensory_content_data.items():
                if isinstance(content, dict) and content.get("available") and content.get("elements"):
                    elements = content["elements"]
                    for element in elements:
                        # Identify quick activities (5-15 minutes)
                        if element.get("content_subtype") in [
                            "ambient_sound", "cultural_scent", "texture_exploration", 
                            "spice_exploration", "gentle_touch", "photo_viewing"
                        ]:
                            quick_activities.append({
                                "title": element.get("activity", element.get("name", f"{sense.capitalize()} Activity")),
                                "duration": "5-15 minutes",
                                "preparation": element.get("implementation", {}).get("setup", "Minimal setup"),
                                "description": element.get("description", f"Quick {sense} experience")
                            })
                        
                        if len(quick_activities) >= 4:  # Limit to prevent overflow
                            break
        
        # GUARANTEED FALLBACK: Ensure minimum quick activities
        if len(quick_activities) < 2:
            fallback_activities = [
                {
                    "title": "Deep Breathing Together",
                    "duration": "5 minutes",
                    "preparation": "Comfortable seating",
                    "description": "Calming breathing exercise"
                },
                {
                    "title": "Hand Holding",
                    "duration": "5-10 minutes", 
                    "preparation": "None needed",
                    "description": "Simple comforting physical connection"
                }
            ]
            needed = 2 - len(quick_activities)
            quick_activities.extend(fallback_activities[:needed])
        
        return quick_activities
    
    def _create_guaranteed_meal_content(self, 
                                      sensory_content: Dict[str, Any],
                                      source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create meal content with guaranteed recipes."""
        
        meal_content = {
            "content_type": "meal_experience",
            "featured_recipe": None,
            "alternative_recipes": [],
            "cooking_together_guide": {},
            "sensory_engagement": [],
            "memory_conversation_starters": [],
            "safety_considerations": []
        }
        
        # Extract recipes from sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        gustatory_content = sensory_content_data.get("gustatory", {})
        
        if gustatory_content.get("available") and gustatory_content.get("elements"):
            elements = gustatory_content["elements"]
            recipes = [elem for elem in elements if "recipe" in elem.get("content_subtype", "")]
            
            if recipes:
                meal_content["featured_recipe"] = recipes[0]
                meal_content["alternative_recipes"] = recipes[1:3]
                meal_content["cooking_together_guide"] = self._create_cooking_guide(recipes[0])
        
        # GUARANTEED FALLBACK: Create recipe if none found
        if not meal_content["featured_recipe"]:
            logger.warning("No recipes found - creating guaranteed fallback recipe")
            meal_content["featured_recipe"] = self._create_guaranteed_fallback_recipe()
            meal_content["cooking_together_guide"] = self._create_cooking_guide(meal_content["featured_recipe"])
        
        # Add guaranteed sensory engagement
        meal_content["sensory_engagement"] = [
            "Enjoy cooking aromas together",
            "Feel ingredient textures",
            "Taste small samples during cooking",
            "Listen to cooking sounds",
            "Appreciate visual presentation"
        ]
        
        # Add guaranteed conversation starters
        meal_content["memory_conversation_starters"] = [
            "What was your favorite family recipe?",
            "Who did the cooking in your family?",
            "What foods remind you of special occasions?",
            "Tell me about meals you enjoyed growing up"
        ]
        
        # Add guaranteed safety considerations
        meal_content["safety_considerations"] = [
            "Supervise all knife and heat use",
            "Check for food allergies",
            "Ensure safe kitchen environment",
            "Break cooking into simple steps"
        ]
        
        return meal_content
    
    def _create_guaranteed_fallback_recipe(self) -> Dict[str, Any]:
        """Create guaranteed fallback recipe that always works."""
        
        return {
            "content_subtype": "universal_comfort_recipe",
            "activity": "Making tea and simple snacks together",
            "name": "Tea Time with Simple Snacks",
            "description": "Comforting warm beverage with easy snacks",
            "recipe_data": {
                "name": "Tea Time with Simple Snacks",
                "description": "A simple, safe cooking experience focused on connection",
                "prep_time": "5 minutes",
                "cook_time": "5 minutes",
                "total_time": "10 minutes",
                "servings": "2 people",
                "difficulty": "very easy",
                "ingredients": [
                    {"item": "Tea bags or instant tea", "amount": "2", "notes": "Their preferred type"},
                    {"item": "Hot water", "amount": "2 cups", "notes": "Not boiling hot"},
                    {"item": "Simple crackers or cookies", "amount": "A few", "notes": "Their favorites"},
                    {"item": "Honey or sugar", "amount": "Optional", "notes": "If desired"}
                ],
                "instructions": [
                    {"step": 1, "instruction": "Heat water to warm, not boiling", "time": "3 minutes", "notes": "Safety first"},
                    {"step": 2, "instruction": "Prepare tea together", "time": "2 minutes", "notes": "Let them help"},
                    {"step": 3, "instruction": "Arrange snacks on plate", "time": "2 minutes", "notes": "Make it look nice"},
                    {"step": 4, "instruction": "Sit together and enjoy", "time": "10+ minutes", "notes": "Focus on conversation"}
                ]
            },
            "caregiver_guidance": {
                "implementation": "Focus on the shared experience, not perfect execution",
                "engagement": "Talk about favorite beverages and snack memories",
                "customization": "Use their preferred tea and snacks",
                "safety": "Ensure appropriate temperature and check for allergies"
            }
        }
    
    def _create_guaranteed_conversation_content(self, 
                                              sensory_content: Dict[str, Any],
                                              qloo_intelligence: Dict[str, Any],
                                              source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create conversation content with guaranteed topics."""
        
        conversation_content = {
            "content_type": "conversation_experience",
            "conversation_starters": [],
            "follow_up_questions": [],
            "memory_exploration_topics": [],
            "cultural_conversation_enhancements": []
        }
        
        # Extract from sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        auditory_content = sensory_content_data.get("auditory", {})
        
        if auditory_content.get("available") and auditory_content.get("elements"):
            elements = auditory_content["elements"]
            conversation_elements = [elem for elem in elements if "conversation" in elem.get("content_subtype", "")]
            
            for element in conversation_elements[:3]:
                conversation_content["conversation_starters"].append({
                    "topic": element.get("topic", "General conversation"),
                    "opening": element.get("conversation_guide", {}).get("opening", "Let's talk about..."),
                    "follow_ups": element.get("conversation_guide", {}).get("follow_up_questions", []),
                    "caregiver_guidance": element.get("caregiver_guidance", {}),
                    "individual_adaptation": "Customize based on their interests and comfort"
                })
        
        # GUARANTEED FALLBACK: Add universal conversation topics
        if len(conversation_content["conversation_starters"]) < 3:
            guaranteed_starters = [
                {
                    "topic": "Daily experiences and feelings",
                    "opening": "How are you feeling today?",
                    "follow_ups": [
                        "What's something good that happened recently?",
                        "Is there anything on your mind?",
                        "What would make today better?"
                    ],
                    "caregiver_guidance": {
                        "implementation": "Start with simple, present-focused questions",
                        "engagement": "Listen actively and validate their responses",
                        "customization": "Follow their emotional state and interests"
                    },
                    "individual_adaptation": "Adjust depth based on their communication abilities"
                },
                {
                    "topic": "Favorite memories and experiences",
                    "opening": "Tell me about something you enjoyed doing",
                    "follow_ups": [
                        "What did you like most about that?",
                        "Who were you with?",
                        "How did it make you feel?"
                    ],
                    "caregiver_guidance": {
                        "implementation": "Let them choose what memories to share",
                        "engagement": "Show genuine interest in their stories",
                        "customization": "Don't pressure for specific details"
                    },
                    "individual_adaptation": "Focus on emotions rather than facts"
                },
                {
                    "topic": "Family and relationships",
                    "opening": "Tell me about people who are important to you",
                    "follow_ups": [
                        "What do you like about spending time with them?",
                        "What makes them special?",
                        "What's a happy memory you have together?"
                    ],
                    "caregiver_guidance": {
                        "implementation": "Be prepared for emotional responses",
                        "engagement": "Celebrate all relationships they mention",
                        "customization": "Include pets and other meaningful connections"
                    },
                    "individual_adaptation": "Respect if some topics are difficult"
                }
            ]
            
            needed = 3 - len(conversation_content["conversation_starters"])
            conversation_content["conversation_starters"].extend(guaranteed_starters[:needed])
        
        # Add guaranteed memory exploration topics
        conversation_content["memory_exploration_topics"] = [
            "Childhood homes and neighborhoods",
            "School experiences and friends",
            "Work and career memories",
            "Travel and special places",
            "Holidays and celebrations",
            "Hobbies and interests"
        ]
        
        return conversation_content
    
    def _create_guaranteed_music_content(self, 
                                       sensory_content: Dict[str, Any],
                                       qloo_intelligence: Dict[str, Any],
                                       source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create music content with guaranteed selections."""
        
        music_content = {
            "content_type": "music_experience",
            "music_selections": [],
            "engagement_activities": [],
            "cultural_connections": [],
            "multi_sensory_enhancements": []
        }
        
        # Extract from sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        auditory_content = sensory_content_data.get("auditory", {})
        
        if auditory_content.get("available") and auditory_content.get("elements"):
            elements = auditory_content["elements"]
            music_elements = [elem for elem in elements if elem.get("content_subtype") == "youtube_music"]
            
            for element in music_elements:
                music_content["music_selections"].append({
                    "title": element.get("title", "Music Selection"),
                    "artist": element.get("artist", "Various Artists"),
                    "youtube_url": element.get("youtube_url", ""),
                    "cultural_connection": element.get("cultural_connection", {}),
                    "engagement_guide": element.get("caregiver_guidance", {}),
                    "individual_customization": "Adjust based on their musical preferences"
                })
        
        # GUARANTEED FALLBACK: Add universal music suggestions
        if not music_content["music_selections"]:
            music_content["music_selections"] = [
                {
                    "title": "Classic Favorites Playlist",
                    "artist": "Various Classic Artists",
                    "youtube_url": "Search: 'classic music playlist'",
                    "cultural_connection": {"type": "universal_appeal"},
                    "engagement_guide": {
                        "implementation": "Play gentle, familiar music",
                        "engagement": "Ask about their music preferences",
                        "customization": "Adjust volume and song selection"
                    },
                    "individual_customization": "Focus on music that brings positive responses"
                }
            ]
        
        # Add guaranteed engagement activities
        music_content["engagement_activities"] = [
            "Gentle swaying or movement to rhythm",
            "Singing along to familiar songs",
            "Tapping hands or feet to the beat",
            "Sharing memories about favorite songs"
        ]
        
        # Add guaranteed multi-sensory enhancements
        music_content["multi_sensory_enhancements"] = [
            "Combine with gentle movement or dance",
            "Add comfortable seating and lighting",
            "Include visual elements like album covers",
            "Incorporate tactile elements like holding hands"
        ]
        
        return music_content
    
    def _create_guaranteed_video_content(self, 
                                       sensory_content: Dict[str, Any],
                                       qloo_intelligence: Dict[str, Any],
                                       source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create video content with guaranteed selections."""
        
        video_content = {
            "content_type": "video_experience",
            "video_selections": [],
            "viewing_guidance": [],
            "discussion_prompts": []
        }
        
        # Extract from sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        visual_content = sensory_content_data.get("visual", {})
        
        if visual_content.get("available") and visual_content.get("elements"):
            elements = visual_content["elements"]
            video_elements = [elem for elem in elements if elem.get("content_subtype") == "youtube_video"]
            
            for element in video_elements:
                video_content["video_selections"].append({
                    "title": element.get("title", "Video Selection"),
                    "content_source": element.get("original_content", "Various"),
                    "youtube_url": element.get("youtube_url", ""),
                    "viewing_notes": element.get("viewing_notes", {}),
                    "engagement_guidance": element.get("caregiver_guidance", {}),
                    "individual_adaptation": "Adjust based on attention and interest"
                })
        
        # GUARANTEED FALLBACK: Add universal video suggestions
        if not video_content["video_selections"]:
            video_content["video_selections"] = [
                {
                    "title": "Nature and Travel Videos",
                    "content_source": "Various nature content",
                    "youtube_url": "Search: 'peaceful nature videos'",
                    "viewing_notes": {"duration": "Start with 5-15 minutes"},
                    "engagement_guidance": {
                        "implementation": "Watch calming nature content together",
                        "engagement": "Comment on what you see together",
                        "customization": "Choose content they find interesting"
                    },
                    "individual_adaptation": "Focus on content that brings positive reactions"
                }
            ]
        
        # Add guaranteed viewing guidance
        video_content["viewing_guidance"] = [
            "Start with short segments (5-15 minutes)",
            "Ensure comfortable seating and good lighting",
            "Be prepared to pause for comments or questions",
            "Watch for attention span and adjust accordingly"
        ]
        
        # Add guaranteed discussion prompts
        video_content["discussion_prompts"] = [
            "What do you think about what we're watching?",
            "Does this remind you of anything?",
            "What's your favorite part so far?",
            "Would you like to watch something similar?"
        ]
        
        return video_content
    
    def _create_guaranteed_general_content(self, 
                                         sensory_content: Dict[str, Any],
                                         qloo_intelligence: Dict[str, Any],
                                         source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create general content for other request types."""
        
        return {
            "content_type": "general_experience",
            "available_activities": [
                {
                    "activity_type": "conversation",
                    "title": "Meaningful Conversation",
                    "description": "Talk about their day, feelings, or memories",
                    "duration": "10-30 minutes",
                    "implementation": "Ask open-ended questions and listen actively"
                },
                {
                    "activity_type": "comfort",
                    "title": "Comfort Activities",
                    "description": "Gentle hand holding, soft music, or familiar objects",
                    "duration": "5-20 minutes",
                    "implementation": "Focus on what brings them comfort"
                },
                {
                    "activity_type": "sensory",
                    "title": "Simple Sensory Experience",
                    "description": "Gentle textures, pleasant scents, or soothing sounds",
                    "duration": "5-15 minutes",
                    "implementation": "Monitor their responses and adjust accordingly"
                }
            ],
            "implementation_guidance": "Choose activities based on current mood and energy level",
            "individual_focus": "Customize all activities based on their preferences and responses"
        }
    
    def _build_guaranteed_enhancement_content(self, 
                                            cultural_profile: Dict[str, Any],
                                            photo_analysis: Dict[str, Any],
                                            qloo_intelligence: Dict[str, Any],
                                            source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Build enhancement content with guaranteed elements."""
        
        enhancement_content = {
            "cultural_intelligence_enhancements": [],
            "photo_memory_enhancements": [],
            "cross_domain_connections": {},
            "era_context_enhancements": {},
            "individual_customization_suggestions": []
        }
        
        # Extract Qloo enhancements
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        for entity_type, recommendations in cultural_recommendations.items():
            if isinstance(recommendations, dict) and recommendations.get("available") and recommendations.get("entities"):
                entities = recommendations.get("entities", [])
                for entity in entities[:2]:
                    enhancement_content["cultural_intelligence_enhancements"].append({
                        "enhancement_type": recommendations.get("entity_type_category", "cultural"),
                        "suggestion": entity.get("name", "Cultural Enhancement"),
                        "cultural_context": entity.get("cultural_context", {}),
                        "implementation_guidance": entity.get("caregiver_guidance", {}),
                        "individual_note": "Use as starting point - adapt based on their actual interests"
                    })
        
        # Extract photo enhancements
        photo_suggestions = photo_analysis.get("conversation_suggestions", [])
        enhancement_content["photo_memory_enhancements"] = photo_suggestions
        
        # Extract cross-domain connections
        enhancement_content["cross_domain_connections"] = qloo_intelligence.get("cross_domain_connections", {})
        
        # Extract era context
        era_context = cultural_profile.get("era_context", {})
        if era_context.get("has_era_context"):
            enhancement_content["era_context_enhancements"] = {
                "available": True,
                "birth_decade": (era_context.get("birth_year", 0) // 10) * 10 if era_context.get("birth_year") else None,
                "formative_decades": era_context.get("decades_lived", [])[-3:] if era_context.get("decades_lived") else [],
                "cultural_eras": era_context.get("cultural_eras", {}),
                "usage_note": "Use era context as conversation starters, not assumptions about preferences"
            }
        
        # Add guaranteed customization suggestions
        enhancement_content["individual_customization_suggestions"] = [
            "Adapt all activities based on their individual responses",
            "Use cultural elements as starting points for exploration",
            "Focus on what generates positive reactions",
            "Always respect their 'no' and try alternatives",
            "Celebrate any level of engagement or participation"
        ]
        
        return enhancement_content
    
    def _build_implementation_content(self, 
                                    sensory_content: Dict[str, Any],
                                    primary_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build implementation guidance with guaranteed elements."""
        
        return {
            "getting_started_guide": {
                "step_1": "Choose one activity that matches their current mood and energy",
                "step_2": "Prepare any materials needed in advance",
                "step_3": "Create a comfortable, distraction-free environment", 
                "step_4": "Start with simple engagement and build based on response",
                "step_5": "Watch for positive responses and adapt accordingly"
            },
            "sensory_implementation_guides": self._create_guaranteed_sensory_guides(),
            "multi_sensory_implementation": [],
            "troubleshooting_guide": {
                "no_response": "Try a different activity or return to this later",
                "negative_response": "Stop immediately and try something comforting",
                "overwhelm": "Reduce stimulation and focus on one simple element",
                "fatigue": "Shorten the activity and focus on comfort",
                "agitation": "Switch to calming activities like gentle music or soft textures"
            },
            "success_indicators": {
                "positive_signs": [
                    "Facial expressions of interest or pleasure",
                    "Verbal responses or questions",
                    "Physical engagement (reaching, touching, moving)",
                    "Sustained attention to the activity",
                    "Requests to continue or do more"
                ],
                "when_to_continue": "Any positive response indicates success",
                "when_to_adapt": "If response is neutral, try modifications",
                "when_to_stop": "Any negative response or signs of distress"
            }
        }
    
    def _create_guaranteed_sensory_guides(self) -> Dict[str, Dict[str, List[str]]]:
        """Create guaranteed sensory implementation guides."""
        
        return {
            "auditory": {
                "preparation": ["Choose quiet environment", "Test volume levels"],
                "implementation_steps": ["Start with low volume", "Watch for responses"],
                "safety_considerations": ["Monitor for sensitivity", "Be ready to stop"],
                "customization_options": ["Adjust volume", "Change music type", "Add or remove visual elements"]
            },
            "visual": {
                "preparation": ["Ensure good lighting", "Have comfortable seating"],
                "implementation_steps": ["Present visual materials slowly", "Allow processing time"],
                "safety_considerations": ["Check vision abilities", "Avoid overwhelming content"],
                "customization_options": ["Adjust brightness", "Change viewing distance", "Switch content types"]
            },
            "tactile": {
                "preparation": ["Gather safe materials", "Check for allergies or sensitivities"],
                "implementation_steps": ["Introduce textures gently", "Let them guide exploration"],
                "safety_considerations": ["Ensure all materials are safe", "Monitor comfort level"],
                "customization_options": ["Change textures", "Adjust pressure", "Add or remove elements"]
            },
            "gustatory": {
                "preparation": ["Check dietary restrictions", "Prepare safe ingredients"],
                "implementation_steps": ["Start with familiar tastes", "Allow them to lead"],
                "safety_considerations": ["Check for allergies", "Ensure safe temperatures"],
                "customization_options": ["Adjust flavors", "Change textures", "Modify portions"]
            },
            "olfactory": {
                "preparation": ["Choose mild scents", "Ensure good ventilation"],
                "implementation_steps": ["Introduce scents gradually", "Watch for reactions"],
                "safety_considerations": ["Check for allergies", "Avoid strong scents"],
                "customization_options": ["Change intensity", "Switch scents", "Remove if needed"]
            }
        }
    
    def _build_cultural_insights(self, 
                               qloo_intelligence: Dict[str, Any],
                               cultural_profile: Dict[str, Any],
                               photo_analysis: Dict[str, Any],
                               source_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Build cultural insights with guaranteed content."""
        
        cultural_insights = {
            "why_these_suggestions": {
                "approach": "individual_first_cultural_enhancement",
                "data_sources": [],
                "cultural_intelligence_note": "These suggestions use cultural intelligence to enhance possibilities, not prescribe preferences",
                "individual_priority": "Their individual responses and preferences always override these suggestions"
            },
            "cultural_connections_explained": [],
            "era_context_insights": {},
            "photo_cultural_insights": {},
            "customization_guidance": {
                "use_suggestions_as": "starting_points_for_exploration",
                "adapt_based_on": "their_individual_responses_and_preferences",
                "remember": "cultural_background_does_not_determine_individual_preferences",
                "focus_on": "what_they_actually_enjoy_and_respond_to_positively"
            }
        }
        
        # Document available data sources
        if source_validation["qloo_recommendations_available"]:
            cultural_insights["why_these_suggestions"]["data_sources"].append("Qloo cultural intelligence API")
        if source_validation["cultural_profile_available"]:
            cultural_insights["why_these_suggestions"]["data_sources"].append("Individual heritage sharing")
        if source_validation["photo_analysis_available"]:
            cultural_insights["why_these_suggestions"]["data_sources"].append("Photo cultural analysis")
        if source_validation["sensory_content_available"]:
            cultural_insights["why_these_suggestions"]["data_sources"].append("Multi-sensory content generation")
        
        # Always include basic source
        if not cultural_insights["why_these_suggestions"]["data_sources"]:
            cultural_insights["why_these_suggestions"]["data_sources"] = ["Caregiver input and universal human needs"]
        
        # Add era context if available
        era_context = cultural_profile.get("era_context", {})
        if era_context.get("has_era_context"):
            cultural_insights["era_context_insights"] = {
                "birth_year": era_context.get("birth_year"),
                "decades_lived": era_context.get("decades_lived", []),
                "usage_note": "Era context provides factual background - individual experiences vary greatly",
                "customization": "Use era information to start conversations, but focus on their specific memories"
            }
        
        return cultural_insights
    
    def _build_customization_options(self, request_type: str) -> Dict[str, Any]:
        """Build customization options with guaranteed content."""
        
        base_customization = {
            "timing_adjustments": {
                "activity_duration": "Adjust from 5 minutes to 1+ hours based on engagement",
                "time_of_day": "Choose times when they're most alert and comfortable",
                "frequency": "Can be daily, weekly, or as-needed based on enjoyment"
            },
            "intensity_adjustments": {
                "sensory_intensity": "Adjust volume, brightness, scent strength based on sensitivity",
                "complexity": "Simplify or elaborate based on current cognitive abilities",
                "social_interaction": "Adapt from quiet solo activities to more social engagement"
            },
            "content_customization": {
                "topic_selection": "Focus on topics that generate positive responses",
                "difficulty_level": "Adjust complexity based on current abilities and comfort",
                "cultural_elements": "Emphasize cultural elements that resonate with them individually"
            },
            "environment_customization": {
                "physical_setup": "Adjust lighting, seating, noise level for comfort",
                "materials": "Provide familiar or preferred objects and tools",
                "space": "Choose indoor/outdoor settings based on preference"
            }
        }
        
        # Add request-specific customizations
        request_specific = {
            "meal": {
                "cooking_customization": {
                    "participation_level": "From watching to full participation based on ability",
                    "dietary_preferences": "Adapt recipes for dietary restrictions and preferences",
                    "cooking_complexity": "Simplify steps based on current abilities"
                }
            },
            "music": {
                "music_customization": {
                    "music_selection": "Focus on music that generates positive responses",
                    "volume_control": "Adjust for hearing ability and sensitivity", 
                    "interaction_level": "From passive listening to active participation"
                }
            },
            "conversation": {
                "conversation_customization": {
                    "topic_depth": "Adjust from simple to complex based on cognitive abilities",
                    "emotional_sensitivity": "Avoid topics that cause distress",
                    "memory_support": "Provide gentle prompts without pressure to remember"
                }
            }
        }
        
        if request_type in request_specific:
            base_customization.update(request_specific[request_type])
        
        return base_customization
    
    def _is_mobile_content_empty(self, mobile_content: Dict[str, Any]) -> bool:
        """Check if mobile content is essentially empty."""
        
        primary_content = mobile_content.get("primary_content", {})
        
        # Check dashboard content
        if primary_content.get("content_type") == "comprehensive_dashboard":
            highlights = len(primary_content.get("today_highlights", []))
            quick_activities = len(primary_content.get("quick_activities", []))
            discoveries = len(primary_content.get("cultural_discoveries", []))
            
            return highlights + quick_activities + discoveries < 2
        
        # Check other content types
        elif primary_content.get("content_type") in ["meal_experience", "conversation_experience", "music_experience", "video_experience"]:
            # Look for primary arrays in each type
            for key, value in primary_content.items():
                if isinstance(value, list) and len(value) > 0:
                    return False
                elif isinstance(value, dict) and value:
                    return False
            return True
        
        # Default check
        return not primary_content or len(str(primary_content)) < 100
    
    def _create_emergency_mobile_content(self, request_type: str) -> Dict[str, Any]:
        """Create emergency mobile content when all else fails."""
        
        logger.error("Creating emergency mobile content - all normal synthesis failed")
        
        return {
            "content_synthesis_approach": "emergency_fallback_universal_activities",
            "primary_content": {
                "content_type": "emergency_universal_activities",
                "today_highlights": [
                    {
                        "sensory_domain": "emotional",
                        "activity": "human_connection",
                        "title": "Spend Quiet Time Together",
                        "quick_description": "Simply being present with them",
                        "implementation_time": "As long as comfortable",
                        "caregiver_preparation": ["No special preparation needed"],
                        "individual_customization": "Follow their lead and comfort level"
                    },
                    {
                        "sensory_domain": "auditory",
                        "activity": "gentle_conversation",
                        "title": "Gentle Conversation",
                        "quick_description": "Talk about how they're feeling today",
                        "implementation_time": "5-20 minutes",
                        "caregiver_preparation": ["Create quiet, comfortable environment"],
                        "individual_customization": "Let them guide topics and pace"
                    }
                ],
                "quick_activities": [
                    {
                        "title": "Hand Holding",
                        "duration": "5-10 minutes",
                        "preparation": "None needed",
                        "description": "Simple physical comfort and connection"
                    },
                    {
                        "title": "Looking Out the Window Together",
                        "duration": "5-15 minutes",
                        "preparation": "Find comfortable seating by window",
                        "description": "Observe and comment on what you see outside"
                    }
                ],
                "cultural_discoveries": [
                    {
                        "discovery_type": "universal",
                        "title": "The Value of Human Connection",
                        "why_suggested": "Connection is a fundamental human need",
                        "how_to_explore": "Focus on being present and caring",
                        "cultural_connection": "Universal human experience",
                        "individual_note": "Your presence and care are the most important gifts you can offer"
                    }
                ]
            },
            "enhancement_content": {
                "individual_customization_suggestions": [
                    "Focus on comfort and safety above all else",
                    "Your caring presence is more valuable than any activity",
                    "Follow their lead - they will show you what they need",
                    "It's okay if formal activities don't work - being together matters most"
                ]
            },
            "emergency_note": "When technology fails, human compassion always works"
        }
    
    def _validate_mobile_content_completeness(self, mobile_experience: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that mobile experience has sufficient content."""
        
        mobile_content = mobile_experience.get("mobile_content", {})
        primary_content = mobile_content.get("primary_content", {})
        
        content_count = 0
        has_content = False
        
        # Count content items based on type
        if primary_content.get("content_type") == "comprehensive_dashboard":
            highlights = len(primary_content.get("today_highlights", []))
            activities = len(primary_content.get("quick_activities", []))
            discoveries = len(primary_content.get("cultural_discoveries", []))
            content_count = highlights + activities + discoveries
            has_content = content_count >= 2
            
        elif primary_content.get("content_type") in ["meal_experience", "conversation_experience", "music_experience", "video_experience"]:
            # Look for any populated arrays or objects
            for key, value in primary_content.items():
                if isinstance(value, list):
                    content_count += len(value)
                elif isinstance(value, dict) and value:
                    content_count += 1
            has_content = content_count >= 1
            
        elif primary_content.get("content_type") in ["general_experience", "emergency_universal_activities"]:
            activities = primary_content.get("available_activities", primary_content.get("today_highlights", []))
            content_count = len(activities) if isinstance(activities, list) else 1
            has_content = content_count >= 1
        
        return {
            "has_content": has_content,
            "content_count": content_count,
            "content_type": primary_content.get("content_type", "unknown")
        }
    
    # Helper methods for content creation
    def _create_quick_description(self, element: Dict[str, Any], sense: str) -> str:
        """Create quick description for dashboard items."""
        
        description = element.get("description", "")
        if description:
            return description
        
        activity = element.get("activity", element.get("name", ""))
        if activity:
            return f"{sense.capitalize()} activity: {activity}"
        
        return f"{sense.capitalize()} experience for comfort and engagement"
    
    def _estimate_implementation_time(self, element: Dict[str, Any]) -> str:
        """Estimate implementation time for activities."""
        
        # Check if duration is specified
        duration = element.get("duration", element.get("implementation", {}).get("duration", ""))
        if duration:
            return duration
        
        # Time estimates based on activity type
        time_mapping = {
            "youtube_music": "5-15 minutes",
            "youtube_video": "5-20 minutes",
            "heritage_inspired_recipe": "30-60 minutes",
            "recipe": "30-60 minutes",
            "conversation_starter": "10-30 minutes",
            "cultural_scent": "5-10 minutes",
            "texture_exploration": "10-20 minutes",
            "photo_viewing": "15-30 minutes",
            "ambient_sound": "10+ minutes"
        }
        
        content_subtype = element.get("content_subtype", "")
        return time_mapping.get(content_subtype, "10-20 minutes")
    
    def _extract_preparation_steps(self, element: Dict[str, Any]) -> List[str]:
        """Extract preparation steps from element."""
        
        preparation_steps = []
        
        # Check implementation guidance
        implementation = element.get("implementation", {})
        if implementation.get("setup"):
            preparation_steps.append(implementation["setup"])
        
        # Check caregiver guidance
        caregiver_guidance = element.get("caregiver_guidance", {})
        if caregiver_guidance.get("preparation"):
            preparation_steps.append(caregiver_guidance["preparation"])
        
        # Default preparation if none specified
        if not preparation_steps:
            preparation_steps = ["Minimal preparation needed", "Create comfortable environment"]
        
        return preparation_steps
    
    def _create_cooking_guide(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Create cooking together guide from recipe."""
        
        if not recipe:
            return {
                "available": False,
                "note": "No recipe available for cooking guide"
            }
        
        recipe_data = recipe.get("recipe_data", {})
        
        return {
            "available": True,
            "recipe_name": recipe_data.get("name", recipe.get("name", "Cooking Together")),
            "preparation_steps": "Gather ingredients and workspace together",
            "cooking_engagement": "Involve them in simple, safe tasks they can handle",
            "sensory_focus": "Point out smells, textures, colors, and sounds during cooking",
            "safety_considerations": [
                "Supervise all knife and heat use",
                "Check for food allergies",
                "Ensure safe kitchen environment",
                "Break tasks into simple steps"
            ],
            "adaptation_notes": "Adjust participation level based on their current abilities and interest"
        }
    
    def _create_fallback_primary_content(self, request_type: str) -> Dict[str, Any]:
        """Create fallback primary content when normal synthesis fails."""
        
        fallback_content_mapping = {
            "dashboard": lambda: {
                "content_type": "fallback_dashboard",
                "today_highlights": [
                    {
                        "sensory_domain": "emotional",
                        "activity": "quality_time",
                        "title": "Quality Time Together",
                        "quick_description": "Focus on being present and connected",
                        "implementation_time": "As long as feels comfortable",
                        "caregiver_preparation": ["Create peaceful environment"],
                        "individual_customization": "Follow their mood and energy level"
                    }
                ],
                "quick_activities": [
                    {
                        "title": "Simple Conversation",
                        "duration": "5-15 minutes",
                        "preparation": "No special preparation",
                        "description": "Ask how they're feeling today"
                    }
                ],
                "cultural_discoveries": [
                    {
                        "discovery_type": "universal",
                        "title": "Human Connection",
                        "why_suggested": "Being together is always meaningful",
                        "how_to_explore": "Focus on presence and compassion",
                        "individual_note": "Your caring attention is the most important thing"
                    }
                ]
            },
            "meal": lambda: {
                "content_type": "fallback_meal",
                "featured_recipe": self._create_guaranteed_fallback_recipe(),
                "cooking_together_guide": {
                    "available": True,
                    "focus": "Simple shared food experience"
                }
            },
            "conversation": lambda: {
                "content_type": "fallback_conversation",
                "conversation_starters": [
                    {
                        "topic": "Today's feelings",
                        "opening": "How are you feeling right now?",
                        "follow_ups": ["What would make you more comfortable?"],
                        "individual_adaptation": "Follow their emotional state"
                    }
                ]
            }
        }
        
        return fallback_content_mapping.get(request_type, fallback_content_mapping["dashboard"])()
    
    def _create_fallback_enhancement_content(self) -> Dict[str, Any]:
        """Create fallback enhancement content."""
        
        return {
            "cultural_intelligence_enhancements": [],
            "photo_memory_enhancements": [],
            "cross_domain_connections": {},
            "era_context_enhancements": {"available": False},
            "individual_customization_suggestions": [
                "Focus on their comfort and well-being",
                "Use your caring judgment about what they need",
                "Remember that your presence is more important than any activity",
                "Be flexible and ready to adapt to their current state"
            ]
        }
    
    def _create_fallback_implementation_content(self) -> Dict[str, Any]:
        """Create fallback implementation content."""
        
        return {
            "getting_started_guide": {
                "step_1": "Ensure they are comfortable and safe",
                "step_2": "Focus on simple human connection",
                "step_3": "Follow their lead and comfort level",
                "step_4": "Remember that being together is enough"
            },
            "troubleshooting_guide": {
                "general_guidance": "When in doubt, focus on comfort and safety",
                "if_nothing_works": "Sometimes just sitting together is perfect"
            },
            "success_indicators": {
                "any_positive_response": "Any sign of comfort or contentment is success"
            }
        }
    
    def _structure_enhanced_feedback_collection(self, request_type: str, mobile_content: Dict[str, Any]) -> Dict[str, Any]:
        """Structure enhanced feedback collection with guaranteed content."""
        
        feedback_collection = {
            "feedback_approach": "simple_emoji_plus_blocking_options",
            "collection_points": [],
            "feedback_processing": {
                "immediate_response": "Adjust current activity based on feedback",
                "session_learning": "Update preferences for future sessions",
                "blocking_respect": "Never suggest blocked content again",
                "preference_building": "Build individual preference profile over time"
            },
            "emoji_feedback_system": {
                "😊": "This worked well - remember for future",
                "😐": "This was okay - neutral response",
                "😞": "This didn't work - avoid similar content",
                "blocking_follow_up": "After 😞, ask what to block (item, type, or category)"
            }
        }
        
        # Always include overall experience feedback
        feedback_collection["collection_points"].append({
            "content_type": "overall_experience",
            "content_title": "Today's Experience",
            "feedback_question": "How was today's overall experience?",
            "blocking_options": [
                "Specific elements that didn't work",
                "Types of activities to avoid",
                "Time of day adjustments needed",
                "No changes needed"
            ]
        })
        
        # Add content-specific feedback based on what was actually created
        primary_content = mobile_content.get("primary_content", {})
        
        if primary_content.get("content_type") == "comprehensive_dashboard":
            highlights = primary_content.get("today_highlights", [])
            for highlight in highlights[:2]:  # Limit to prevent overwhelming
                feedback_collection["collection_points"].append({
                    "content_type": highlight.get("sensory_domain", "activity"),
                    "content_title": highlight.get("title", "Activity"),
                    "feedback_question": f"How did '{highlight.get('title', 'this activity')}' work?",
                    "blocking_options": [
                        "Just this specific activity",
                        f"All {highlight.get('sensory_domain', 'similar')} activities",
                        "This type of activity",
                        "No blocking - just note it didn't work"
                    ]
                })
        
        return feedback_collection
    
    def _generate_accessibility_features(self, mobile_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive accessibility features."""
        
        return {
            "visual_accessibility": {
                "large_text_options": "All text can be increased for better readability",
                "high_contrast_mode": "Available for users with visual difficulties",
                "image_descriptions": "All images include descriptive text",
                "clear_navigation": "Simple, large buttons with clear labels"
            },
            "auditory_accessibility": {
                "volume_controls": "All audio content has easy volume adjustment",
                "visual_indicators": "Visual cues accompany audio content",
                "subtitle_options": "Text descriptions of audio content available",
                "quiet_mode": "All activities can be done without sound"
            },
            "motor_accessibility": {
                "large_touch_targets": "All buttons and controls are easy to tap",
                "simple_gestures": "Only basic taps required, no complex gestures",
                "voice_control": "Voice commands available for navigation",
                "caregiver_operation": "Caregiver can operate all controls"
            },
            "cognitive_accessibility": {
                "simple_language": "All instructions use clear, simple language",
                "step_by_step": "Complex activities broken into simple steps",
                "visual_cues": "Icons and images support text instructions",
                "no_time_pressure": "All activities can be done at individual pace"
            },
            "caregiver_accessibility": {
                "one_handed_operation": "App can be operated with one hand while assisting",
                "quick_access_help": "Help and safety information always accessible",
                "emergency_contacts": "Quick access to emergency contacts and resources",
                "offline_mode": "Core features work without internet connection"
            }
        }
    
    def _create_emergency_fallback_options(self, request_type: str) -> Dict[str, Any]:
        """Create comprehensive emergency and fallback options."""
        
        return {
            "when_activities_arent_working": {
                "immediate_comfort_options": [
                    "Switch to gentle music or nature sounds",
                    "Offer comfort objects like soft blankets or familiar items",
                    "Move to a quieter, more familiar environment",
                    "Engage in simple, repetitive activities like hand massage"
                ],
                "de_escalation_strategies": [
                    "Lower your voice and speak slowly",
                    "Remove any overstimulating elements",
                    "Offer simple choices between two options",
                    "Use familiar phrases or words that usually comfort them"
                ]
            },
            "safety_protocols": {
                "stop_activity_if": [
                    "Any signs of distress or agitation",
                    "Physical discomfort or pain",
                    "Confusion that increases anxiety",
                    "Any negative emotional response"
                ],
                "emergency_contacts": {
                    "note": "Keep emergency contacts easily accessible",
                    "include": "Doctor, family members, emergency services",
                    "quick_access": "Program into phone for immediate access"
                }
            },
            "backup_activities": {
                "always_available_options": [
                    "Looking at familiar family photos",
                    "Listening to very familiar, gentle music",
                    "Simple hand-holding or gentle touch",
                    "Sitting together in comfortable silence"
                ],
                "minimal_preparation_needed": [
                    "Describing what you see outside the window",
                    "Talking about pets or familiar animals",
                    "Simple counting or naming games",
                    "Gentle singing of familiar songs"
                ]
            },
            "caregiver_self_care": {
                "when_you_feel_overwhelmed": [
                    "It's okay if activities don't work - you're doing your best",
                    "Take breaks when you need them",
                    "Ask for help from family, friends, or support groups",
                    "Remember that your presence and care matter most"
                ],
                "support_resources": {
                    "note": "Caregiving is challenging - seek support when needed",
                    "options": "Support groups, respite care, counseling services",
                    "reminder": "Taking care of yourself helps you care for them better"
                }
            }
        }
    
    def _determine_page_structure(self, request_type: str) -> Dict[str, Any]:
        """Determine appropriate mobile page structure based on request type."""
        
        page_structures = {
            "dashboard": {
                "structure_type": "multi_card_dashboard",
                "layout": "vertical_scrolling_cards",
                "primary_sections": [
                    "daily_highlights",
                    "quick_activities",
                    "suggested_conversations",
                    "sensory_experiences",
                    "photo_memories"
                ],
                "interaction_pattern": "tap_to_expand_details",
                "caregiver_controls": "visible_throughout"
            },
            "meal": {
                "structure_type": "recipe_focused",
                "layout": "step_by_step_guide",
                "primary_sections": [
                    "recipe_overview",
                    "ingredients_list",
                    "step_by_step_instructions",
                    "sensory_engagement_tips",
                    "memory_conversation_starters"
                ],
                "interaction_pattern": "linear_progression_with_flexibility",
                "caregiver_controls": "step_guidance_and_adaptation"
            },
            "conversation": {
                "structure_type": "conversation_guide",
                "layout": "topic_cards_with_expansions",
                "primary_sections": [
                    "conversation_starters",
                    "follow_up_questions",
                    "memory_triggers",
                    "cultural_connections",
                    "photo_integration"
                ],
                "interaction_pattern": "guided_conversation_flow",
                "caregiver_controls": "topic_selection_and_pacing"
            },
            "music": {
                "structure_type": "music_experience",
                "layout": "media_player_with_context",
                "primary_sections": [
                    "music_selections",
                    "cultural_context",
                    "engagement_activities",
                    "memory_connections",
                    "multi_sensory_enhancements"
                ],
                "interaction_pattern": "media_playback_with_interaction",
                "caregiver_controls": "playback_and_activity_guidance"
            },
            "video": {
                "structure_type": "video_experience",
                "layout": "video_player_with_context",
                "primary_sections": [
                    "video_selections",
                    "viewing_guidance",
                    "discussion_prompts",
                    "cultural_connections",
                    "related_activities"
                ],
                "interaction_pattern": "video_viewing_with_engagement",
                "caregiver_controls": "playback_and_discussion_guidance"
            },
            "photo_analysis": {
                "structure_type": "photo_exploration",
                "layout": "photo_centered_with_activities",
                "primary_sections": [
                    "photo_display",
                    "observation_prompts",
                    "conversation_starters",
                    "memory_exploration",
                    "related_activities"
                ],
                "interaction_pattern": "photo_guided_discovery",
                "caregiver_controls": "conversation_pacing_and_support"
            }
        }
        
        return page_structures.get(request_type, page_structures["dashboard"])
    
    def _document_content_sources(self, 
                                 qloo_intelligence: Dict[str, Any],
                                 sensory_content: Dict[str, Any],
                                 photo_analysis: Dict[str, Any]) -> List[str]:
        """Document what content sources were successfully used."""
        
        sources = ["Individual heritage sharing", "Caregiver input"]
        
        # Check Qloo usage
        if qloo_intelligence.get("cultural_recommendations"):
            sources.append("Qloo cultural intelligence API")
        
        # Check photo analysis
        if photo_analysis.get("analysis_metadata", {}).get("photo_analyzed"):
            sources.append("Photo cultural analysis")
        
        # Check sensory content
        sensory_content_data = sensory_content.get("sensory_content", {})
        if isinstance(sensory_content_data, dict):
            for sense, content in sensory_content_data.items():
                if isinstance(content, dict) and content.get("available") and content.get("elements"):
                    sources.append(f"{sense.capitalize()} content generation")
        
        return sources
    
    def _generate_comprehensive_caregiver_guide(self, 
                                               mobile_content: Dict[str, Any],
                                               request_type: str,
                                               feedback_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive caregiver implementation guide with guaranteed content."""
        
        return {
            "caregiver_authority_note": {
                "primary_principle": "You know them best - use these suggestions as starting points only",
                "decision_making": "You make all decisions about what to try and when to stop",
                "adaptation": "Modify anything based on their individual needs and responses",
                "safety": "Stop any activity immediately if it causes distress or discomfort"
            },
            "before_you_start": {
                "preparation_checklist": [
                    "Choose a time when they're alert and comfortable",
                    "Create a quiet, distraction-free environment",
                    "Have backup activities ready if needed",
                    "Ensure you have uninterrupted time together"
                ],
                "environment_setup": {
                    "lighting": "Comfortable, not too bright or dim",
                    "noise_level": "Quiet background, minimal distractions",
                    "seating": "Comfortable chairs with good support",
                    "temperature": "Comfortable room temperature",
                    "safety": "Clear pathways, remove tripping hazards",
                    "materials": "Have all needed items within easy reach"
                },
                "timing_considerations": {
                    "best_times": "When they're most alert (often mornings)",
                    "avoid_times": "When tired, hungry, or usually nap",
                    "duration": "Start with 15-30 minutes, extend if engaged",
                    "flexibility": "Stop anytime if they're not enjoying it"
                }
            },
            "during_activities": {
                "observation_guide": {
                    "positive_responses": [
                        "Smiling, laughing, or positive facial expressions",
                        "Leaning in or moving closer to activity",
                        "Asking questions or making comments",
                        "Relaxed body language"
                    ],
                    "negative_responses": [
                        "Turning away or backing away",
                        "Expressions of confusion or distress",
                        "Agitation or restlessness",
                        "Any signs of physical discomfort"
                    ]
                },
                "adaptation_strategies": {
                    "if_overwhelmed": [
                        "Reduce sensory input (lower volume, dimmer lights)",
                        "Simplify the activity to fewer elements",
                        "Take breaks or pause the activity"
                    ],
                    "if_not_engaged": [
                        "Try a different approach or element",
                        "Ask what they prefer or would like to do",
                        "Switch to a more familiar activity"
                    ]
                }
            },
            "success_reminders": {
                "remember": [
                    "Your caring presence is more important than perfect execution",
                    "Any positive response indicates success",
                    "It's okay if formal activities don't work - being together matters most",
                    "Every person with dementia is unique - these are just starting points"
                ]
            }
        }
    
    def _create_cultural_context_explanations(self, 
                                            cultural_profile: Dict[str, Any],
                                            qloo_intelligence: Dict[str, Any],
                                            photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create cultural context explanations with guaranteed content."""
        
        return {
            "approach_explanation": {
                "title": "How Cultural Intelligence Works",
                "description": "These suggestions use cultural data to enhance possibilities, not to make assumptions about individual preferences",
                "key_principles": [
                    "Cultural background provides starting points, not predetermined preferences",
                    "Individual responses always override cultural suggestions",
                    "Heritage information enhances exploration opportunities",
                    "Era context provides conversation topics, not assumptions about taste"
                ]
            },
            "data_sources_explained": {
                "heritage_sharing": self._explain_heritage_usage(cultural_profile),
                "qloo_intelligence": self._explain_qloo_usage(qloo_intelligence),
                "photo_analysis": self._explain_photo_usage(photo_analysis)
            },
            "how_to_use_suggestions": {
                "starting_points": "Use all suggestions as conversation starters and activity ideas",
                "individual_focus": "Pay attention to their actual responses and preferences",
                "customization": "Modify everything based on what they actually enjoy",
                "flexibility": "Feel free to ignore suggestions that don't seem right for them"
            },
            "bias_prevention_note": {
                "cultural_assumptions": "We never assume someone likes something because of their heritage",
                "individual_priority": "Their personal interests and reactions are most important",
                "caregiver_authority": "You know them best - trust your judgment over any suggestion"
            }
        }
    
    def _explain_heritage_usage(self, cultural_profile: Dict[str, Any]) -> Dict[str, str]:
        """Explain how heritage information is used."""
        
        cultural_elements = cultural_profile.get("cultural_elements", {})
        has_heritage = cultural_elements.get("has_cultural_info", False)
        
        if not has_heritage:
            return {
                "usage": "No specific heritage information provided",
                "approach": "Using general cultural exploration activities"
            }
        
        return {
            "usage": "Heritage information used to find conversation topics and activity ideas",
            "approach": "Broad exploration of cultural themes without assumptions about preferences",
            "note": "Heritage provides starting points - their individual interests matter most"
        }
    
    def _explain_qloo_usage(self, qloo_intelligence: Dict[str, Any]) -> Dict[str, str]:
        """Explain how Qloo cultural intelligence is used."""
        
        qloo_meta = qloo_intelligence.get("qloo_metadata", {})
        api_calls = qloo_meta.get("api_calls_made", 0)
        successful_calls = qloo_meta.get("successful_calls", 0)
        
        if api_calls == 0:
            return {
                "usage": "Qloo cultural intelligence not available for this session",
                "fallback": "Using general activity suggestions instead"
            }
        
        return {
            "usage": f"Qloo made {api_calls} cultural intelligence queries ({successful_calls} successful)",
            "approach": "Cross-domain cultural discovery without stereotypical assumptions",
            "note": "Qloo suggestions are starting points for exploration - customize based on individual response"
        }
    
    def _explain_photo_usage(self, photo_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Explain how photo analysis is used."""
        
        analysis_meta = photo_analysis.get("analysis_metadata", {})
        photo_analyzed = analysis_meta.get("photo_analyzed", False)
        
        if not photo_analyzed:
            return {
                "usage": "No photo analysis performed",
                "note": "Photo-based suggestions not available"
            }
        
        return {
            "usage": "Photo analyzed for visible elements and potential conversation topics",
            "approach": "Factual observation of photo contents, not cultural assumptions",
            "note": "Photo analysis provides conversation starters based on what's actually visible"
        }
    
    def _validate_caregiver_authority_compliance(self, mobile_experience: Dict[str, Any]) -> None:
        """Validate that caregiver authority is maintained throughout."""
        
        # Check for authority indicators in the experience
        experience_text = str(mobile_experience).lower()
        authority_indicators = [
            "caregiver", "you know", "individual", "customize", "adapt", 
            "modify", "starting point", "suggestion", "their response", "follow their lead"
        ]
        
        authority_count = sum(1 for indicator in authority_indicators if indicator in experience_text)
        
        if authority_count < 10:
            logger.warning(f"Insufficient caregiver authority language: {authority_count} indicators found")
        else:
            logger.info(f"✅ Caregiver authority compliance validated: {authority_count} indicators found")
        
        # Check that caregiver authority note exists
        caregiver_guide = mobile_experience.get("caregiver_guide", {})
        authority_note = caregiver_guide.get("caregiver_authority_note", {})
        
        if not authority_note.get("primary_principle"):
            logger.warning("❌ Primary caregiver authority principle missing")
        else:
            logger.info("✅ Caregiver authority principle present")
    
    def _create_emergency_mobile_experience(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create emergency mobile experience when everything fails."""
        
        request_type = consolidated_info.get("request_context", {}).get("request_type", "dashboard")
        
        logger.error("🚨 CREATING EMERGENCY MOBILE EXPERIENCE - All synthesis failed")
        
        return {
            "mobile_experience": {
                "synthesis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "mode": "EMERGENCY_FALLBACK",
                    "caregiver_authority": "maintained",
                    "guaranteed_content": True,
                    "emergency_reason": "complete_synthesis_failure"
                },
                "page_structure": self._determine_page_structure(request_type),
                "mobile_content": self._create_emergency_mobile_content(request_type),
                "caregiver_guide": {
                    "caregiver_authority_note": {
                        "primary_principle": "You know them best - your caring presence is what matters most",
                        "emergency_approach": "When technology fails, human compassion always works",
                        "focus": "Simply being present and caring is enough"
                    },
                    "emergency_guidance": {
                        "remember": [
                            "Your caring presence is more valuable than any technology",
                            "Simple human connection never fails",
                            "Follow your instincts about what they need",
                            "Being together with love and patience is always right"
                        ]
                    }
                },
                "cultural_context_explanations": {
                    "emergency_mode": True,
                    "message": "When systems fail, the most important cultural element is human kindness"
                },
                "feedback_collection": {
                    "simple_feedback": "Note what brings them comfort for future reference"
                },
                "accessibility_features": self._generate_accessibility_features({}),
                "emergency_options": self._create_emergency_fallback_options(request_type)
            }
        }