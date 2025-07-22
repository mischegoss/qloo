"""
Agent 6: Mobile Synthesizer
Role: Package all content for mobile caregiver experience
Follows Responsible Development Guide principles - caregiver authority and individual focus
"""

from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class MobileSynthesizerAgent(Agent):
    """
    Agent 6: Mobile Synthesizer
    
    Purpose: Package all content for mobile caregiver experience
    Input: All previous agent outputs
    Output: Complete mobile experience with caregiver instructions
    
    Anti-Bias Principles:
    - Structure for specific page type (dashboard, recipe, music, conversation)
    - Add caregiver guidance and cultural context explanations
    - Include feedback collection points
    - Maintain caregiver authority throughout interface
    - Present cultural intelligence as suggestions, not directions
    - Individual preferences override all recommendations
    """
    
    def __init__(self):
        super().__init__(
            name="mobile_synthesizer",
            description="Synthesizes all content into mobile-optimized caregiver experience"
        )
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize all content into mobile caregiver experience.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            qloo_intelligence: Output from Agent 3  
            sensory_content: Output from Agent 4
            photo_analysis: Output from Agent 5
            
        Returns:
            Complete mobile experience package
        """
        
        try:
            logger.info("Synthesizing content for mobile caregiver experience")
            
            # Extract request context and metadata
            request_context = consolidated_info.get("request_context", {})
            request_type = request_context.get("request_type", "dashboard")
            session_metadata = consolidated_info.get("session_metadata", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            
            # Determine mobile page structure based on request type
            page_structure = self._determine_page_structure(request_type)
            
            # Synthesize content for mobile presentation
            mobile_content = self._synthesize_mobile_content(
                request_type,
                cultural_profile,
                qloo_intelligence,
                sensory_content,
                photo_analysis
            )
            
            # Generate caregiver implementation guide
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
            feedback_collection = self._structure_feedback_collection(request_type, mobile_content)
            
            # Generate mobile accessibility features
            accessibility_features = self._generate_accessibility_features(mobile_content)
            
            # Create emergency and fallback options
            emergency_options = self._create_emergency_fallback_options(request_type)
            
            # Build complete mobile experience
            mobile_experience = {
                "synthesis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "page_structure": page_structure["structure_type"],
                    "content_sources": self._document_content_sources(qloo_intelligence, sensory_content, photo_analysis),
                    "caregiver_authority": "maintained_throughout",
                    "individual_focus": "prioritized",
                    "cultural_approach": "enhancement_not_direction"
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
            
            # Validate mobile experience quality
            self._validate_mobile_experience_quality(mobile_experience)
            
            # Validate caregiver authority maintenance
            self._validate_caregiver_authority_compliance(mobile_experience)
            
            logger.info("Mobile caregiver experience synthesized successfully")
            return {"mobile_experience": mobile_experience}
            
        except Exception as e:
            logger.error(f"Error synthesizing mobile experience: {str(e)}")
            return self._create_fallback_mobile_experience(consolidated_info)
    
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
    
    def _synthesize_mobile_content(self, 
                                  request_type: str,
                                  cultural_profile: Dict[str, Any],
                                  qloo_intelligence: Dict[str, Any],
                                  sensory_content: Dict[str, Any],
                                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all content for mobile presentation."""
        
        # Extract key content from each agent
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        sensory_content_data = sensory_content.get("sensory_content", {})
        cross_sensory_experiences = sensory_content.get("cross_sensory_experiences", [])
        photo_suggestions = photo_analysis.get("conversation_suggestions", [])
        
        # Create unified content structure
        mobile_content = {
            "content_synthesis_approach": "individual_first_cultural_enhancement",
            "primary_content": self._structure_primary_content(
                request_type, 
                cultural_recommendations,
                sensory_content_data,
                cross_sensory_experiences
            ),
            "enhancement_content": self._structure_enhancement_content(
                cultural_profile,
                photo_suggestions,
                qloo_intelligence
            ),
            "caregiver_implementation": self._structure_implementation_content(
                sensory_content_data,
                cross_sensory_experiences
            ),
            "cultural_intelligence_insights": self._structure_cultural_insights(
                qloo_intelligence,
                cultural_profile,
                photo_analysis
            ),
            "individual_customization_options": self._structure_customization_options(request_type),
            "anti_bias_safeguards": {
                "individual_preferences_override": "all_suggestions_are_starting_points",
                "caregiver_authority": "caregiver_makes_all_decisions",
                "cultural_approach": "enhancement_not_prescription",
                "adaptation_required": "customize_based_on_individual_response"
            }
        }
        
        return mobile_content
    
    def _structure_primary_content(self, 
                                  request_type: str,
                                  cultural_recommendations: Dict[str, Any],
                                  sensory_content_data: Dict[str, Any],
                                  cross_sensory_experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Structure primary content based on request type."""
        
        if request_type == "dashboard":
            return self._create_dashboard_primary_content(
                cultural_recommendations, 
                sensory_content_data,
                cross_sensory_experiences
            )
        elif request_type == "meal":
            return self._create_meal_primary_content(sensory_content_data)
        elif request_type == "conversation":
            return self._create_conversation_primary_content(sensory_content_data)
        elif request_type == "music":
            return self._create_music_primary_content(sensory_content_data)
        elif request_type == "video":
            return self._create_video_primary_content(sensory_content_data)
        else:
            return self._create_general_primary_content(sensory_content_data)
    
    def _create_dashboard_primary_content(self, 
                                         cultural_recommendations: Dict[str, Any],
                                         sensory_content_data: Dict[str, Any],
                                         cross_sensory_experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create dashboard-specific primary content."""
        
        dashboard_content = {
            "content_type": "comprehensive_dashboard",
            "today_highlights": [],
            "quick_activities": [],
            "multi_sensory_experiences": cross_sensory_experiences,
            "cultural_discoveries": []
        }
        
        # Extract highlights from each sensory domain
        for sense, content in sensory_content_data.items():
            if content.get("available") and content.get("elements"):
                # Take top 2 elements from each sense for dashboard
                top_elements = content["elements"][:2]
                for element in top_elements:
                    dashboard_content["today_highlights"].append({
                        "sensory_domain": sense,
                        "activity": element.get("content_subtype", f"{sense}_activity"),
                        "title": element.get("activity", element.get("title", f"{sense.capitalize()} Experience")),
                        "quick_description": self._create_quick_description(element, sense),
                        "implementation_time": self._estimate_implementation_time(element),
                        "caregiver_preparation": self._extract_preparation_steps(element),
                        "individual_customization": "Adapt based on their response and preferences"
                    })
        
        # Create quick activities (5-15 minute activities)
        dashboard_content["quick_activities"] = self._extract_quick_activities(sensory_content_data)
        
        # Extract cultural discoveries from Qloo recommendations
        for entity_type, recommendations in cultural_recommendations.items():
            if recommendations.get("available") and recommendations.get("entities"):
                entity = recommendations["entities"][0]  # Top recommendation
                dashboard_content["cultural_discoveries"].append({
                    "discovery_type": recommendations.get("entity_type_category", "cultural"),
                    "title": entity.get("name", "Cultural Discovery"),
                    "why_suggested": "Based on cultural intelligence and individual context",
                    "how_to_explore": entity.get("caregiver_guidance", {}).get("implementation", "Explore together"),
                    "cultural_connection": entity.get("cultural_context", {}).get("why_suggested", "Cultural exploration"),
                    "individual_note": "Use this as a starting point - customize based on their interests"
                })
        
        return dashboard_content
    
    def _create_meal_primary_content(self, sensory_content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create meal-specific primary content."""
        
        gustatory_content = sensory_content_data.get("gustatory", {})
        
        if not gustatory_content.get("available"):
            return {
                "content_type": "meal_experience",
                "available": False,
                "reason": "No meal content available",
                "alternative": "Consider simple food memory conversations"
            }
        
        # Extract recipe content
        recipes = [elem for elem in gustatory_content.get("elements", []) 
                  if elem.get("content_subtype") in ["heritage_inspired_recipe", "era_comfort_food", "universal_comfort_recipe"]]
        
        meal_content = {
            "content_type": "meal_experience",
            "available": True,
            "featured_recipe": recipes[0] if recipes else None,
            "alternative_recipes": recipes[1:3] if len(recipes) > 1 else [],
            "cooking_together_guide": self._create_cooking_together_guide(recipes[0] if recipes else None),
            "sensory_engagement": self._extract_cooking_sensory_elements(gustatory_content),
            "memory_conversation_starters": self._extract_food_memory_conversations(gustatory_content),
            "safety_considerations": self._extract_cooking_safety_considerations(gustatory_content)
        }
        
        return meal_content
    
    def _create_conversation_primary_content(self, sensory_content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create conversation-specific primary content."""
        
        auditory_content = sensory_content_data.get("auditory", {})
        
        conversation_content = {
            "content_type": "conversation_experience",
            "conversation_starters": [],
            "follow_up_questions": [],
            "memory_exploration_topics": [],
            "cultural_conversation_enhancements": []
        }
        
        # Extract conversation elements
        if auditory_content.get("available"):
            conversation_elements = [elem for elem in auditory_content.get("elements", [])
                                   if elem.get("content_subtype") in ["conversation_starter", "era_conversation"]]
            
            for element in conversation_elements:
                conversation_content["conversation_starters"].append({
                    "topic": element.get("topic", "General conversation"),
                    "opening": element.get("conversation_guide", {}).get("opening", "Let's talk about..."),
                    "follow_ups": element.get("conversation_guide", {}).get("follow_up_questions", []),
                    "caregiver_guidance": element.get("caregiver_guidance", {}),
                    "cultural_connection": element.get("cultural_connection", ""),
                    "individual_adaptation": "Customize based on their interests and comfort level"
                })
        
        return conversation_content
    
    def _create_music_primary_content(self, sensory_content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create music-specific primary content."""
        
        auditory_content = sensory_content_data.get("auditory", {})
        
        music_content = {
            "content_type": "music_experience",
            "music_selections": [],
            "engagement_activities": [],
            "cultural_connections": [],
            "multi_sensory_enhancements": []
        }
        
        # Extract music elements
        if auditory_content.get("available"):
            music_elements = [elem for elem in auditory_content.get("elements", [])
                            if elem.get("content_subtype") == "youtube_music"]
            
            for element in music_elements:
                music_content["music_selections"].append({
                    "title": element.get("title", "Music Selection"),
                    "artist": element.get("artist", "Unknown Artist"),
                    "youtube_url": element.get("youtube_url", ""),
                    "cultural_connection": element.get("cultural_connection", {}),
                    "engagement_guide": element.get("caregiver_guidance", {}),
                    "accessibility_notes": element.get("accessibility", {}),
                    "individual_customization": "Adjust volume, duration, and interaction based on their response"
                })
        
        return music_content
    
    def _create_video_primary_content(self, sensory_content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create video-specific primary content."""
        
        visual_content = sensory_content_data.get("visual", {})
        
        video_content = {
            "content_type": "video_experience",
            "video_selections": [],
            "viewing_guidance": [],
            "discussion_prompts": []
        }
        
        # Extract video elements
        if visual_content.get("available"):
            video_elements = [elem for elem in visual_content.get("elements", [])
                            if elem.get("content_subtype") == "youtube_video"]
            
            for element in video_elements:
                video_content["video_selections"].append({
                    "title": element.get("title", "Video Selection"),
                    "content_source": element.get("original_content", "Unknown"),
                    "youtube_url": element.get("youtube_url", ""),
                    "viewing_notes": element.get("viewing_notes", {}),
                    "engagement_guidance": element.get("caregiver_guidance", {}),
                    "individual_adaptation": "Adjust viewing duration and interaction based on attention and interest"
                })
        
        return video_content
    
    def _create_general_primary_content(self, sensory_content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create general primary content for other request types."""
        
        return {
            "content_type": "general_experience",
            "available_activities": self._extract_all_activities(sensory_content_data),
            "implementation_guidance": "Choose activities based on current mood and energy level",
            "individual_focus": "Customize all activities based on their preferences and responses"
        }
    
    def _structure_enhancement_content(self, 
                                     cultural_profile: Dict[str, Any],
                                     photo_suggestions: List[Dict[str, Any]],
                                     qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Structure enhancement content from cultural intelligence."""
        
        enhancement_content = {
            "cultural_intelligence_enhancements": [],
            "photo_memory_enhancements": photo_suggestions,
            "cross_domain_connections": qloo_intelligence.get("cross_domain_connections", {}),
            "era_context_enhancements": self._extract_era_enhancements(cultural_profile),
            "individual_customization_suggestions": self._extract_customization_suggestions(cultural_profile)
        }
        
        # Extract Qloo-powered enhancements
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        for entity_type, recommendations in cultural_recommendations.items():
            if recommendations.get("available"):
                for entity in recommendations.get("entities", [])[:2]:  # Top 2 per domain
                    enhancement_content["cultural_intelligence_enhancements"].append({
                        "enhancement_type": recommendations.get("entity_type_category", "cultural"),
                        "suggestion": entity.get("name", "Cultural Enhancement"),
                        "cultural_context": entity.get("cultural_context", {}),
                        "implementation_guidance": entity.get("caregiver_guidance", {}),
                        "cross_domain_potential": entity.get("cross_domain_potential", []),
                        "individual_note": "Use as starting point - adapt based on their actual interests and responses"
                    })
        
        return enhancement_content
    
    def _structure_implementation_content(self, 
                                        sensory_content_data: Dict[str, Any],
                                        cross_sensory_experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Structure implementation guidance for caregivers."""
        
        implementation_content = {
            "getting_started_guide": {
                "step_1": "Choose one activity that matches their current mood and energy",
                "step_2": "Prepare any materials needed in advance", 
                "step_3": "Create a comfortable, distraction-free environment",
                "step_4": "Start with simple engagement and build based on response",
                "step_5": "Watch for positive responses and adapt accordingly"
            },
            "sensory_implementation_guides": {},
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
        
        # Create implementation guides for each sensory domain
        for sense, content in sensory_content_data.items():
            if content.get("available"):
                implementation_content["sensory_implementation_guides"][sense] = {
                    "preparation": self._extract_preparation_requirements(content),
                    "implementation_steps": self._extract_implementation_steps(content),
                    "safety_considerations": self._extract_safety_considerations(content),
                    "customization_options": self._extract_customization_options(content)
                }
        
        # Add multi-sensory implementation guidance
        for experience in cross_sensory_experiences:
            implementation_content["multi_sensory_implementation"].append({
                "experience_name": experience.get("experience_name", "Multi-sensory Experience"),
                "preparation": experience.get("implementation_guide", {}),
                "caregiver_guidance": experience.get("caregiver_guidance", {}),
                "individual_adaptation": "Modify based on their response to each sensory element"
            })
        
        return implementation_content
    
    def _structure_cultural_insights(self, 
                                   qloo_intelligence: Dict[str, Any],
                                   cultural_profile: Dict[str, Any],
                                   photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Structure cultural intelligence insights for caregiver understanding."""
        
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
        
        # Document data sources
        qloo_meta = qloo_intelligence.get("qloo_metadata", {})
        if qloo_meta.get("api_calls_made", 0) > 0:
            cultural_insights["why_these_suggestions"]["data_sources"].append("Qloo cultural intelligence API")
        
        photo_meta = photo_analysis.get("analysis_metadata", {})
        if photo_meta.get("photo_analyzed", False):
            cultural_insights["why_these_suggestions"]["data_sources"].append("Photo cultural analysis")
        
        cultural_insights["why_these_suggestions"]["data_sources"].append("Individual heritage sharing")
        cultural_insights["why_these_suggestions"]["data_sources"].append("Era and demographic context")
        
        # Explain cultural connections without assumptions
        thematic_intelligence = qloo_intelligence.get("thematic_intelligence", {})
        common_themes = thematic_intelligence.get("common_themes", [])
        
        for theme in common_themes:
            cultural_insights["cultural_connections_explained"].append({
                "theme": theme,
                "explanation": f"This theme emerged from cross-domain cultural intelligence analysis",
                "how_to_use": "Use as starting point for exploration - customize based on their individual interests",
                "individual_note": "Their personal preferences may differ from these cultural patterns"
            })
        
        # Add era context insights
        era_context = cultural_profile.get("era_context", {})
        if era_context.get("has_era_context"):
            cultural_insights["era_context_insights"] = {
                "birth_year": era_context.get("birth_year"),
                "decades_lived": era_context.get("decades_lived", []),
                "cultural_eras": era_context.get("cultural_eras", {}),
                "usage_note": "Era context provides factual background - individual experiences within eras vary greatly",
                "customization": "Use era information to start conversations, but focus on their specific memories and experiences"
            }
        
        # Add photo insights if available
        if photo_analysis.get("analysis_metadata", {}).get("photo_analyzed"):
            cultural_insights["photo_cultural_insights"] = {
                "photo_elements": photo_analysis.get("cultural_indicators", {}),
                "conversation_opportunities": photo_analysis.get("conversation_suggestions", []),
                "usage_note": "Photo analysis provides conversation starters based on what's visible",
                "individual_focus": "Let them guide what aspects of the photo interest them most"
            }
        
        return cultural_insights
    
    def _structure_customization_options(self, request_type: str) -> Dict[str, Any]:
        """Structure individual customization options."""
        
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
        
        # Add request-type specific customizations
        if request_type == "meal":
            base_customization["cooking_customization"] = {
                "participation_level": "From watching to full participation based on ability",
                "dietary_preferences": "Adapt recipes for dietary restrictions and preferences",
                "cooking_complexity": "Simplify steps based on current abilities"
            }
        elif request_type == "music":
            base_customization["music_customization"] = {
                "music_selection": "Focus on music that generates positive responses",
                "volume_control": "Adjust for hearing ability and sensitivity",
                "interaction_level": "From passive listening to active participation"
            }
        elif request_type == "conversation":
            base_customization["conversation_customization"] = {
                "topic_depth": "Adjust from simple to complex based on cognitive abilities",
                "emotional_sensitivity": "Avoid topics that cause distress",
                "memory_support": "Provide gentle prompts without pressure to remember"
            }
        
        return base_customization
    
    def _generate_comprehensive_caregiver_guide(self, 
                                               mobile_content: Dict[str, Any],
                                               request_type: str,
                                               feedback_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive caregiver implementation guide."""
        
        caregiver_guide = {
            "caregiver_authority_note": {
                "primary_principle": "You know them best - use these suggestions as starting points only",
                "decision_making": "You make all decisions about what to try and when to stop",
                "adaptation": "Modify anything based on their individual needs and responses",
                "safety": "Stop any activity immediately if it causes distress or discomfort"
            },
            "before_you_start": {
                "preparation_checklist": self._create_preparation_checklist(mobile_content, request_type),
                "environment_setup": self._create_environment_setup_guide(request_type),
                "timing_considerations": self._create_timing_considerations(),
                "backup_plans": self._create_backup_plans(request_type)
            },
            "during_activities": {
                "observation_guide": self._create_observation_guide(),
                "adaptation_strategies": self._create_adaptation_strategies(),
                "communication_tips": self._create_communication_tips(),
                "safety_monitoring": self._create_safety_monitoring_guide()
            },
            "after_activities": {
                "response_assessment": self._create_response_assessment_guide(),
                "feedback_collection": self._create_feedback_collection_guide(),
                "future_planning": self._create_future_planning_guide(),
                "documentation_suggestions": self._create_documentation_suggestions()
            },
            "troubleshooting": {
                "common_challenges": self._create_troubleshooting_guide(),
                "emergency_responses": self._create_emergency_response_guide(),
                "when_to_seek_help": self._create_help_seeking_guide()
            },
            "individual_focus_reminders": {
                "remember": [
                    "Their individual preferences override all cultural suggestions",
                    "What works today may be different tomorrow - stay flexible",
                    "Positive responses indicate success, regardless of the activity",
                    "Your caring presence is more important than perfect execution",
                    "Every person with dementia is unique - these are just starting points"
                ]
            }
        }
        
        return caregiver_guide
    
    def _structure_feedback_collection(self, request_type: str, mobile_content: Dict[str, Any]) -> Dict[str, Any]:
        """Structure feedback collection points throughout the experience."""
        
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
        
        # Create feedback collection points based on content
        primary_content = mobile_content.get("primary_content", {})
        
        if request_type == "dashboard":
            highlights = primary_content.get("today_highlights", [])
            for highlight in highlights:
                feedback_collection["collection_points"].append({
                    "content_type": highlight.get("sensory_domain"),
                    "content_title": highlight.get("title"),
                    "feedback_question": f"How did the {highlight.get('sensory_domain')} activity work?",
                    "blocking_options": [
                        f"Just this specific {highlight.get('sensory_domain')} activity",
                        f"All {highlight.get('sensory_domain')} activities", 
                        f"This type of activity",
                        "No blocking - just note it didn't work"
                    ]
                })
        
        elif request_type == "meal":
            feedback_collection["collection_points"].append({
                "content_type": "cooking_experience",
                "content_title": "Cooking Together",
                "feedback_question": "How did the cooking experience work?",
                "blocking_options": [
                    "Just this specific recipe",
                    "This type of cooking activity",
                    "All cooking activities",
                    "No blocking - just note it didn't work"
                ]
            })
        
        elif request_type == "music":
            music_selections = primary_content.get("music_selections", [])
            for music in music_selections:
                feedback_collection["collection_points"].append({
                    "content_type": "music",
                    "content_title": music.get("title"),
                    "feedback_question": f"How did {music.get('artist')} music work?",
                    "blocking_options": [
                        f"Just this specific song",
                        f"Music by {music.get('artist')}",
                        "This type of music",
                        "All music activities"
                    ]
                })
        
        # Add general activity feedback
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
        
        return feedback_collection
    
    def _generate_accessibility_features(self, mobile_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mobile accessibility features."""
        
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
        """Create emergency and fallback options for difficult situations."""
        
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
    
    def _document_content_sources(self, 
                                 qloo_intelligence: Dict[str, Any],
                                 sensory_content: Dict[str, Any],
                                 photo_analysis: Dict[str, Any]) -> List[str]:
        """Document what content sources were used."""
        
        sources = ["Individual heritage sharing", "Caregiver input"]
        
        # Check Qloo usage
        qloo_meta = qloo_intelligence.get("qloo_metadata", {})
        if qloo_meta.get("api_calls_made", 0) > 0:
            sources.append("Qloo cultural intelligence API")
        
        # Check photo analysis
        photo_meta = photo_analysis.get("analysis_metadata", {})
        if photo_meta.get("photo_analyzed", False):
            sources.append("Photo cultural analysis")
        
        # Check sensory content generation
        sensory_meta = sensory_content.get("generation_metadata", {})
        if sensory_meta.get("senses_activated"):
            sources.extend([f"{sense.capitalize()} content generation" for sense in sensory_meta["senses_activated"]])
        
        return sources
    
    def _validate_mobile_experience_quality(self, mobile_experience: Dict[str, Any]) -> None:
        """Validate the quality of the mobile experience."""
        
        # Check for required components
        required_components = [
            "page_structure", "mobile_content", "caregiver_guide", 
            "feedback_collection", "accessibility_features"
        ]
        
        missing_components = []
        for component in required_components:
            if component not in mobile_experience:
                missing_components.append(component)
        
        if missing_components:
            logger.warning(f"Missing mobile experience components: {missing_components}")
        
        # Check caregiver guidance quality
        caregiver_guide = mobile_experience.get("caregiver_guide", {})
        if not caregiver_guide.get("caregiver_authority_note"):
            logger.warning("Caregiver authority note missing from mobile experience")
        
        # Check feedback collection
        feedback_collection = mobile_experience.get("feedback_collection", {})
        if not feedback_collection.get("collection_points"):
            logger.warning("No feedback collection points defined")
        
        logger.info("Mobile experience quality validation completed")
    
    def _validate_caregiver_authority_compliance(self, mobile_experience: Dict[str, Any]) -> None:
        """Validate that caregiver authority is maintained throughout."""
        
        # Check for authority indicators
        authority_indicators = [
            "caregiver", "you know them best", "individual", "customize",
            "adapt", "modify", "starting point", "suggestion"
        ]
        
        experience_text = str(mobile_experience).lower()
        authority_count = sum(1 for indicator in authority_indicators if indicator in experience_text)
        
        if authority_count < 10:
            logger.warning("Insufficient caregiver authority language in mobile experience")
        
        # Check for directive language (should be minimal)
        directive_indicators = [
            "must", "should", "will", "always", "never", "required"
        ]
        
        directive_count = sum(1 for indicator in directive_indicators if indicator in experience_text)
        
        if directive_count > 5:
            logger.warning("Too much directive language in mobile experience")
        
        # Check caregiver authority note
        caregiver_guide = mobile_experience.get("caregiver_guide", {})
        authority_note = caregiver_guide.get("caregiver_authority_note", {})
        
        if not authority_note.get("primary_principle"):
            logger.warning("Primary caregiver authority principle missing")
        
        logger.info("Caregiver authority compliance validation completed")
    
    def _create_fallback_mobile_experience(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback mobile experience when synthesis fails."""
        
        request_type = consolidated_info.get("request_context", {}).get("request_type", "dashboard")
        
        return {
            "mobile_experience": {
                "synthesis_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_type,
                    "mode": "fallback_safe_defaults",
                    "caregiver_authority": "maintained"
                },
                "page_structure": self._determine_page_structure(request_type),
                "mobile_content": {
                    "content_synthesis_approach": "safe_fallback_individual_focus",
                    "primary_content": {
                        "content_type": "fallback_activities",
                        "simple_activities": [
                            "Look at family photos together",
                            "Listen to familiar, gentle music",
                            "Have a simple conversation about today",
                            "Enjoy a comfortable snack together"
                        ]
                    }
                },
                "caregiver_guide": {
                    "caregiver_authority_note": {
                        "primary_principle": "You know them best - use your judgment about what will work",
                        "fallback_approach": "Start with simple, familiar activities"
                    },
                    "basic_guidance": {
                        "approach": "Keep it simple and follow their lead",
                        "observation": "Watch for positive responses and adapt",
                        "safety": "Stop any activity if it causes discomfort"
                    }
                },
                "feedback_collection": {
                    "simple_feedback": "Note what works and what doesn't for future reference"
                },
                "accessibility_features": self._generate_accessibility_features({}),
                "emergency_options": self._create_emergency_fallback_options(request_type)
            }
        }
    
    # Helper methods for content extraction and creation
    def _create_quick_description(self, element: Dict[str, Any], sense: str) -> str:
        """Create quick description for dashboard items."""
        
        descriptions = {
            "auditory": "Music and conversation activities",
            "visual": "Photos and visual activities", 
            "gustatory": "Cooking and food experiences",
            "olfactory": "Scent and aroma activities",
            "tactile": "Touch and texture activities"
        }
        
        return element.get("description", descriptions.get(sense, f"{sense.capitalize()} experience"))
    
    def _estimate_implementation_time(self, element: Dict[str, Any]) -> str:
        """Estimate implementation time for activities."""
        
        # Default time estimates
        time_mapping = {
            "youtube_music": "5-15 minutes",
            "youtube_video": "5-20 minutes",
            "heritage_inspired_recipe": "30-60 minutes",
            "conversation_starter": "10-30 minutes",
            "cultural_scent": "5-10 minutes",
            "tactile_exploration": "10-20 minutes"
        }
        
        content_subtype = element.get("content_subtype", "")
        return time_mapping.get(content_subtype, "10-20 minutes")
    
    def _extract_preparation_steps(self, element: Dict[str, Any]) -> List[str]:
        """Extract preparation steps from element."""
        
        implementation = element.get("implementation", {})
        caregiver_guidance = element.get("caregiver_guidance", {})
        
        preparation_steps = []
        
        if implementation.get("setup"):
            preparation_steps.append(implementation["setup"])
        if implementation.get("method"):
            preparation_steps.append(f"Method: {implementation['method']}")
        if caregiver_guidance.get("preparation"):
            preparation_steps.append(caregiver_guidance["preparation"])
        
        return preparation_steps if preparation_steps else ["Minimal preparation needed"]
    
    def _extract_quick_activities(self, sensory_content_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract quick 5-15 minute activities."""
        
        quick_activities = []
        
        for sense, content in sensory_content_data.items():
            if content.get("available") and content.get("elements"):
                for element in content["elements"][:1]:  # One per sense for quick activities
                    if element.get("content_subtype") in ["ambient_sound", "cultural_scent", "texture_exploration", "spice_exploration"]:
                        quick_activities.append({
                            "title": element.get("activity", f"{sense.capitalize()} Activity"),
                            "duration": "5-15 minutes",
                            "preparation": "Minimal setup required",
                            "description": f"Quick {sense} experience"
                        })
        
        return quick_activities
    
    # Additional helper methods would continue here for extracting and organizing content...
    # (Implementation details for remaining helper methods would follow similar patterns)
    
    def _create_preparation_checklist(self, mobile_content: Dict[str, Any], request_type: str) -> List[str]:
        """Create preparation checklist for caregivers."""
        
        base_checklist = [
            "Choose a time when they're alert and comfortable",
            "Create a quiet, distraction-free environment",
            "Have backup activities ready if needed",
            "Ensure you have uninterrupted time together"
        ]
        
        if request_type == "meal":
            base_checklist.extend([
                "Gather all ingredients and cooking tools",
                "Check for dietary restrictions or allergies",
                "Ensure kitchen safety (supervise sharp objects and heat)"
            ])
        elif request_type == "music":
            base_checklist.extend([
                "Test audio equipment and volume levels",
                "Have comfortable seating arranged",
                "Prepare alternative music if needed"
            ])
        
        return base_checklist
    
    def _create_environment_setup_guide(self, request_type: str) -> Dict[str, str]:
        """Create environment setup guide."""
        
        return {
            "lighting": "Comfortable, not too bright or dim",
            "noise_level": "Quiet background, minimal distractions",
            "seating": "Comfortable chairs with good support",
            "temperature": "Comfortable room temperature",
            "safety": "Clear pathways, remove tripping hazards",
            "materials": "Have all needed items within easy reach"
        }
    
    def _create_timing_considerations(self) -> Dict[str, str]:
        """Create timing considerations guide."""
        
        return {
            "best_times": "When they're most alert (often mornings)",
            "avoid_times": "When tired, hungry, or usually nap",
            "duration": "Start with 15-30 minutes, extend if engaged",
            "frequency": "Can be daily or several times per week",
            "flexibility": "Stop anytime if they're not enjoying it"
        }
    
    def _create_backup_plans(self, request_type: str) -> List[str]:
        """Create backup plans for when activities don't work."""
        
        return [
            "Have simpler versions of activities ready",
            "Keep familiar comfort activities available",
            "Be prepared to switch to quiet time together",
            "Have emergency contact information accessible"
        ]
    
    def _create_observation_guide(self) -> Dict[str, List[str]]:
        """Create observation guide for caregivers."""
        
        return {
            "positive_responses": [
                "Smiling, laughing, or positive facial expressions",
                "Leaning in or moving closer to activity",
                "Asking questions or making comments",
                "Wanting to touch or participate more",
                "Relaxed body language"
            ],
            "neutral_responses": [
                "Quiet attention without strong reaction",
                "Following along but not actively engaging",
                "Answering questions when asked but not initiating"
            ],
            "negative_responses": [
                "Turning away or backing away",
                "Expressions of confusion or distress",
                "Agitation or restlessness",
                "Asking to stop or do something else",
                "Any signs of physical discomfort"
            ]
        }
    
    def _create_adaptation_strategies(self) -> Dict[str, List[str]]:
        """Create adaptation strategies."""
        
        return {
            "if_overwhelmed": [
                "Reduce sensory input (lower volume, dimmer lights)",
                "Simplify the activity to fewer elements",
                "Take breaks or pause the activity",
                "Move to a quieter environment"
            ],
            "if_not_engaged": [
                "Try a different approach or element",
                "Ask what they prefer or would like to do",
                "Switch to a more familiar activity",
                "Give them more time to process"
            ],
            "if_agitated": [
                "Stop the current activity immediately",
                "Switch to calming activities (gentle music, soft textures)",
                "Use familiar, comforting words and actions",
                "Consider if they have basic needs (hungry, tired, need bathroom)"
            ]
        }
    
    def _create_communication_tips(self) -> Dict[str, List[str]]:
        """Create communication tips."""
        
        return {
            "verbal_communication": [
                "Speak slowly and clearly",
                "Use simple, familiar words",
                "Ask one question at a time",
                "Give them time to process and respond"
            ],
            "non_verbal_communication": [
                "Maintain gentle eye contact",
                "Use warm, encouraging facial expressions",
                "Keep body language open and relaxed",
                "Respect their personal space"
            ],
            "validation_techniques": [
                "Accept all responses as valuable",
                "Don't correct or argue with their reality",
                "Focus on emotions rather than facts",
                "Celebrate any engagement or participation"
            ]
        }
    
    def _create_safety_monitoring_guide(self) -> Dict[str, List[str]]:
        """Create safety monitoring guide."""
        
        return {
            "physical_safety": [
                "Watch for signs of fatigue or discomfort",
                "Ensure they can see and hear clearly",
                "Monitor for any allergic reactions",
                "Keep pathways clear and safe"
            ],
            "emotional_safety": [
                "Watch for signs of distress or anxiety",
                "Be prepared to stop activities that upset them",
                "Provide comfort and reassurance as needed",
                "Respect their choices and preferences"
            ],
            "cognitive_safety": [
                "Don't pressure them to remember specific details",
                "Avoid correcting their memories or stories",
                "Provide gentle guidance without frustration",
                "Accept their current abilities and limitations"
            ]
        }
    
    def _create_response_assessment_guide(self) -> Dict[str, str]:
        """Create response assessment guide."""
        
        return {
            "successful_session": "Any positive engagement, smiles, or participation",
            "partially_successful": "Some positive moments, even if brief",
            "neutral_session": "No negative reactions, some attention or cooperation",
            "unsuccessful_session": "Negative reactions, distress, or request to stop",
            "learning_from_all": "Every session provides information about their preferences"
        }
    
    def _create_feedback_collection_guide(self) -> Dict[str, str]:
        """Create feedback collection guide."""
        
        return {
            "immediate_feedback": "Note their immediate responses during activities",
            "overall_session": "Assess how the entire session went",
            "what_worked": "Document specific elements that generated positive responses",
            "what_to_avoid": "Note anything that caused negative reactions",
            "future_modifications": "Ideas for how to improve next time"
        }
    
    def _create_future_planning_guide(self) -> Dict[str, str]:
        """Create future planning guide."""
        
        return {
            "successful_elements": "Plan to repeat activities that worked well",
            "modifications": "Adjust activities based on today's responses",
            "new_explorations": "Try variations of successful activities",
            "timing_adjustments": "Consider different times of day if needed",
            "gradual_progression": "Slowly build on successful experiences"
        }
    
    def _create_documentation_suggestions(self) -> List[str]:
        """Create documentation suggestions."""
        
        return [
            "Keep simple notes about what activities work best",
            "Note optimal times of day for different activities",
            "Record favorite music, foods, or conversation topics",
            "Document any activities or topics to avoid",
            "Track changes in preferences over time"
        ]
    
    def _create_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Create troubleshooting guide."""
        
        return {
            "activity_rejection": [
                "Try the same activity at a different time",
                "Modify the activity to be simpler or shorter",
                "Offer choices between two activities",
                "Respect their 'no' and try something else"
            ],
            "confusion_or_agitation": [
                "Lower your voice and speak more slowly",
                "Remove distracting elements from environment",
                "Offer simple, familiar comfort activities",
                "Consider if they have unmet basic needs"
            ],
            "lack_of_response": [
                "Give more time for processing",
                "Try a different sensory approach",
                "Check if they can see/hear clearly",
                "Consider if they're tired or not feeling well"
            ]
        }
    
    def _create_emergency_response_guide(self) -> Dict[str, List[str]]:
        """Create emergency response guide."""
        
        return {
            "if_they_become_distressed": [
                "Stop the current activity immediately",
                "Speak in calm, reassuring tones",
                "Offer comfort items or familiar objects",
                "Consider calling family member or healthcare provider"
            ],
            "if_they_seem_unwell": [
                "Check for basic needs (hunger, thirst, bathroom)",
                "Look for signs of pain or discomfort",
                "Take vital signs if possible",
                "Contact healthcare provider if concerned"
            ],
            "if_you_feel_overwhelmed": [
                "Take a break if possible",
                "Call family member or friend for support",
                "Remember that challenging moments are normal",
                "Seek professional help if needed"
            ]
        }
    
    def _create_help_seeking_guide(self) -> Dict[str, str]:
        """Create help seeking guide."""
        
        return {
            "when_to_call_doctor": "Any concerning changes in behavior, appetite, or health",
            "when_to_seek_family_support": "When you need a break or additional help",
            "when_to_contact_emergency_services": "Any serious health or safety concerns",
            "ongoing_support_resources": "Support groups, respite care, counseling services",
            "remember": "Asking for help is a sign of good caregiving, not weakness"
        }
    
    def _extract_era_enhancements(self, cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Extract era-based enhancements."""
        
        era_context = cultural_profile.get("era_context", {})
        
        if not era_context.get("has_era_context"):
            return {"available": False}
        
        return {
            "available": True,
            "birth_decade": era_context.get("birth_year", 0) // 10 * 10 if era_context.get("birth_year") else None,
            "formative_decades": era_context.get("decades_lived", [])[-3:],  # Recent decades
            "cultural_eras": era_context.get("cultural_eras", {}),
            "usage_note": "Use era context as conversation starters, not assumptions about preferences"
        }
    
    def _extract_customization_suggestions(self, cultural_profile: Dict[str, Any]) -> List[str]:
        """Extract customization suggestions from cultural profile."""
        
        cultural_elements = cultural_profile.get("cultural_elements", {})
        
        suggestions = [
            "Adapt all activities based on their individual responses",
            "Use cultural elements as starting points for exploration",
            "Focus on what generates positive reactions"
        ]
        
        if cultural_elements.get("has_cultural_info"):
            suggestions.append("Use their heritage sharing for conversation topics")
            
        if cultural_elements.get("language_elements", {}).get("multilingual"):
            suggestions.append("Consider incorporating their languages if they respond positively")
        
        return suggestions
    
    def _extract_all_activities(self, sensory_content_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract all available activities from sensory content."""
        
        activities = []
        
        for sense, content in sensory_content_data.items():
            if content.get("available") and content.get("elements"):
                for element in content["elements"]:
                    activities.append({
                        "sensory_domain": sense,
                        "activity_type": element.get("content_subtype", f"{sense}_activity"),
                        "title": element.get("activity", element.get("title", f"{sense.capitalize()} Activity")),
                        "implementation": element.get("implementation", {}).get("approach", "Follow individual guidance"),
                        "duration": self._estimate_implementation_time(element)
                    })
        
        return activities
    
    def _create_cooking_together_guide(self, recipe: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Create cooking together guide from recipe."""
        
        if not recipe:
            return {"available": False, "note": "No recipe available"}
        
        return {
            "available": True,
            "recipe_name": recipe.get("recipe_data", {}).get("name", "Comfort Food Recipe"),
            "preparation_steps": "Prepare ingredients and workspace together",
            "cooking_engagement": "Involve them in simple, safe tasks",
            "sensory_focus": "Emphasize smells, textures, and tastes",
            "safety_considerations": recipe.get("safety_considerations", {}),
            "adaptation_notes": recipe.get("caregiver_guidance", {}).get("customization", "Adapt based on abilities")
        }
    
    def _extract_cooking_sensory_elements(self, gustatory_content: Dict[str, Any]) -> List[str]:
        """Extract sensory elements from cooking content."""
        
        sensory_elements = [
            "Enjoy cooking aromas together",
            "Touch and feel ingredients", 
            "Taste small samples during cooking",
            "Listen to cooking sounds (sizzling, bubbling)",
            "Appreciate visual presentation of food"
        ]
        
        return sensory_elements
    
    def _extract_food_memory_conversations(self, gustatory_content: Dict[str, Any]) -> List[str]:
        """Extract food memory conversation starters."""
        
        conversations = [
            "What was your favorite family recipe?",
            "Who did the cooking in your family?",
            "What foods remind you of special occasions?",
            "Tell me about meals you enjoyed growing up",
            "What was your favorite restaurant or special meal?"
        ]
        
        return conversations
    
    def _extract_cooking_safety_considerations(self, gustatory_content: Dict[str, Any]) -> List[str]:
        """Extract cooking safety considerations."""
        
        safety_considerations = [
            "Supervise all knife and heat use",
            "Check for food allergies and dietary restrictions",
            "Ensure safe kitchen environment",
            "Break cooking into simple, manageable steps",
            "Be prepared to simplify or modify recipe"
        ]
        
        return safety_considerations
    
    def _extract_preparation_requirements(self, content: Dict[str, Any]) -> List[str]:
        """Extract preparation requirements from content."""
        
        requirements = ["Minimal preparation needed"]
        
        elements = content.get("elements", [])
        for element in elements:
            implementation = element.get("implementation", {})
            if implementation.get("setup"):
                requirements.append(implementation["setup"])
        
        return requirements
    
    def _extract_implementation_steps(self, content: Dict[str, Any]) -> List[str]:
        """Extract implementation steps from content."""
        
        steps = ["Follow individual guidance and preferences"]
        
        elements = content.get("elements", [])
        for element in elements:
            caregiver_guidance = element.get("caregiver_guidance", {})
            if caregiver_guidance.get("implementation"):
                steps.append(caregiver_guidance["implementation"])
        
        return steps
    
    def _extract_safety_considerations(self, content: Dict[str, Any]) -> List[str]:
        """Extract safety considerations from content."""
        
        safety = ["Monitor for comfort and positive response"]
        
        elements = content.get("elements", [])
        for element in elements:
            safety_info = element.get("safety_considerations", {})
            caregiver_guidance = element.get("caregiver_guidance", {})
            
            if safety_info:
                safety.extend(safety_info.values() if isinstance(safety_info, dict) else [str(safety_info)])
            
            if caregiver_guidance.get("safety"):
                safety.append(caregiver_guidance["safety"])
        
        return safety
    
    def _extract_customization_options(self, content: Dict[str, Any]) -> List[str]:
        """Extract customization options from content."""
        
        options = ["Adapt based on individual response and preferences"]
        
        elements = content.get("elements", [])
        for element in elements:
            if element.get("individual_customization"):
                options.append(element["individual_customization"])
            
            caregiver_guidance = element.get("caregiver_guidance", {})
            if caregiver_guidance.get("customization"):
                options.append(caregiver_guidance["customization"])
        
        return options