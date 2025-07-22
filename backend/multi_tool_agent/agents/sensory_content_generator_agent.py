"""
Agent 4: Sensory Content Generator - FIXED VERSION
Role: Create connected multi-sensory experiences
Fixes: Tool references, error handling, content population
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent(Agent):
    """
    Agent 4: Sensory Content Generator - FIXED
    
    FIXED ISSUES:
    - Correct tool reference handling
    - Better error handling for empty API responses  
    - Proper content structure for Agent 6 consumption
    - Fallback content when APIs fail
    - Content arrays properly populated
    """
    
    def __init__(self, youtube_tool, gemini_tool):
        super().__init__(
            name="sensory_content_generator",
            description="Creates practical multi-sensory experiences with proper error handling"
        )
        # FIXED: Store tool references correctly
        self._youtube_tool = youtube_tool
        self._gemini_tool = gemini_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Generate connected sensory content across all 5 senses."""
        
        try:
            logger.info("Starting sensory content generation with improved error handling")
            
            # Extract context information
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            
            # Extract cultural elements
            cultural_elements = cultural_profile.get("cultural_elements", {})
            
            # Extract Qloo recommendations with better validation
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            logger.info(f"Processing {len(cultural_recommendations)} Qloo recommendation types")
            
            # Build sensory strategy
            sensory_strategy = self._build_sensory_strategy(
                request_context,
                cultural_elements,
                cultural_recommendations,
                blocked_content
            )
            
            # Generate content for each sense with better error handling
            logger.info("Generating multi-sensory content with validation")
            
            # 1. Auditory content (music, sounds)
            auditory_content = await self._generate_auditory_content_fixed(
                sensory_strategy, 
                cultural_recommendations, 
                blocked_content
            )
            
            # 2. Gustatory content (taste experiences)
            gustatory_content = await self._generate_gustatory_content_fixed(
                sensory_strategy,
                cultural_elements,
                blocked_content
            )
            
            # 3. Olfactory content (smell experiences)
            olfactory_content = self._generate_olfactory_content_fixed(
                sensory_strategy,
                gustatory_content
            )
            
            # 4. Visual content (videos, activities)
            visual_content = await self._generate_visual_content_fixed(
                sensory_strategy,
                cultural_recommendations,
                blocked_content
            )
            
            # 5. Tactile content (touch experiences)
            tactile_content = self._generate_tactile_content_fixed(
                sensory_strategy,
                cultural_elements
            )
            
            # Create connected sensory experiences
            cross_sensory_experiences = self._create_cross_sensory_experiences(
                auditory_content,
                gustatory_content,
                olfactory_content,
                visual_content,
                tactile_content,
                sensory_strategy
            )
            
            # Build complete sensory content package
            sensory_content = {
                "generation_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_context.get("request_type", "dashboard"),
                    "sensory_strategy": sensory_strategy["approach"],
                    "senses_activated": self._get_activated_senses([auditory_content, gustatory_content, olfactory_content, visual_content, tactile_content]),
                    "cultural_elements_integrated": len(cultural_elements),
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "auditory": auditory_content,
                "gustatory": gustatory_content,
                "olfactory": olfactory_content,
                "visual": visual_content,
                "tactile": tactile_content,
                "cross_sensory_experiences": cross_sensory_experiences,
                "implementation_guidance": self._generate_implementation_guidance(cross_sensory_experiences),
                "content_summary": self._generate_content_summary([auditory_content, gustatory_content, olfactory_content, visual_content, tactile_content])
            }
            
            logger.info(f"Sensory content generation completed: {len(cross_sensory_experiences)} connected experiences")
            return {"sensory_content": sensory_content}
            
        except Exception as e:
            logger.error(f"Error in sensory content generation: {str(e)}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    def _build_sensory_strategy(self, 
                               request_context: Dict[str, Any],
                               cultural_elements: Dict[str, Any],
                               cultural_recommendations: Dict[str, Any],
                               blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build strategy for sensory content generation."""
        
        request_type = request_context.get("request_type", "dashboard")
        
        # Determine sensory focus based on request type
        sensory_focus = self._determine_sensory_focus(request_type)
        
        # Extract cultural themes without stereotypes
        cultural_themes = self._extract_cultural_themes(cultural_elements, cultural_recommendations)
        
        # Build strategy
        strategy = {
            "approach": "multi_sensory_integration_with_fallbacks",
            "request_type": request_type,
            "sensory_focus": sensory_focus,
            "cultural_themes": cultural_themes,
            "blocked_content": blocked_content,
            "generation_priorities": self._set_generation_priorities(request_type),
            "has_qloo_data": len(cultural_recommendations) > 0,
            "has_cultural_elements": len(cultural_elements) > 0
        }
        
        return strategy
    
    def _determine_sensory_focus(self, request_type: str) -> List[str]:
        """Determine which senses to prioritize based on request type."""
        
        if request_type == "meal":
            return ["gustatory", "olfactory", "tactile", "visual", "auditory"]
        elif request_type == "music":
            return ["auditory", "tactile", "visual", "olfactory", "gustatory"]
        elif request_type == "conversation":
            return ["auditory", "visual", "tactile", "olfactory", "gustatory"]
        else:  # dashboard or general
            return ["auditory", "visual", "gustatory", "olfactory", "tactile"]
    
    def _extract_cultural_themes(self, 
                                cultural_elements: Dict[str, Any],
                                cultural_recommendations: Dict[str, Any]) -> List[str]:
        """Extract cultural themes without stereotypical assumptions."""
        
        themes = []
        
        # Extract from user-provided elements (most important)
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        tradition_keywords = cultural_elements.get("tradition_elements", {}).get("tradition_keywords", [])
        
        themes.extend(heritage_keywords[:3])  # Limit to avoid overwhelming
        themes.extend(tradition_keywords[:3])
        
        # Extract from Qloo recommendations (supplementary)
        for entity_type, recommendations in cultural_recommendations.items():
            if recommendations.get("available") and recommendations.get("entities"):
                entities = recommendations.get("entities", [])
                for entity in entities[:2]:  # Limit per type
                    entity_name = entity.get("name", "")
                    if entity_name and entity_name not in themes:
                        themes.append(entity_name)
        
        return themes[:8]  # Maximum 8 themes to keep focused
    
    def _set_generation_priorities(self, request_type: str) -> Dict[str, int]:
        """Set priorities for content generation based on request type."""
        
        base_priorities = {
            "auditory": 3,
            "gustatory": 3,
            "olfactory": 2,
            "visual": 3,
            "tactile": 2
        }
        
        if request_type == "meal":
            base_priorities.update({"gustatory": 5, "olfactory": 4, "tactile": 3})
        elif request_type == "music":
            base_priorities.update({"auditory": 5, "tactile": 3})
        elif request_type == "conversation":
            base_priorities.update({"auditory": 4, "visual": 4})
        
        return base_priorities
    
    async def _generate_auditory_content_fixed(self, 
                                             sensory_strategy: Dict[str, Any],
                                             cultural_recommendations: Dict[str, Any],
                                             blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Generate auditory content with proper error handling."""
        
        auditory_content = {
            "available": True,
            "content_type": "auditory",
            "elements": []
        }
        
        # Check if audio content is blocked
        if self._is_content_blocked("audio", blocked_content):
            auditory_content["available"] = False
            auditory_content["blocked_reason"] = "user_feedback"
            return auditory_content
        
        # FIXED: Better processing of Qloo music recommendations
        music_entities = []
        for entity_type in ["urn:entity:artist"]:  # Only use supported types
            if entity_type in cultural_recommendations:
                recommendation = cultural_recommendations[entity_type]
                if recommendation.get("available") and recommendation.get("entities"):
                    music_entities.extend(recommendation.get("entities", []))
        
        # Generate YouTube music content with better error handling
        if music_entities:
            try:
                youtube_music = await self._generate_youtube_music_content_fixed(music_entities[:3])
                if youtube_music:  # Only add if we got results
                    auditory_content["elements"].extend(youtube_music)
                    logger.info(f"Generated {len(youtube_music)} YouTube music elements")
            except Exception as e:
                logger.warning(f"YouTube music generation failed: {str(e)}")
        
        # ALWAYS generate ambient sound suggestions as fallback
        ambient_sounds = self._generate_ambient_sound_suggestions_fixed(sensory_strategy)
        auditory_content["elements"].extend(ambient_sounds)
        
        # Generate conversation starters (auditory experience)
        conversation_starters = self._generate_conversation_starters(sensory_strategy)
        auditory_content["elements"].extend(conversation_starters)
        
        logger.info(f"Generated {len(auditory_content['elements'])} auditory elements total")
        return auditory_content
    
    async def _generate_youtube_music_content_fixed(self, music_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """FIXED: Generate YouTube music content with proper error handling."""
        
        youtube_content = []
        
        for entity in music_entities:
            artist_name = entity.get("name", "")
            if not artist_name:
                continue
            
            try:
                # FIXED: Use correct tool reference
                search_results = await self._youtube_tool.search_music(
                    query=f"{artist_name} best songs classic hits",
                    max_results=2
                )
                
                if search_results and search_results.get("items"):
                    for video in search_results["items"]:
                        video_snippet = video.get("snippet", {})
                        video_id_obj = video.get("id", {})
                        video_id = video_id_obj.get("videoId", "") if isinstance(video_id_obj, dict) else ""
                        
                        if video_id:  # Only add if we have a valid video ID
                            youtube_content.append({
                                "content_subtype": "youtube_music",
                                "activity": f"Listen to {artist_name} music",
                                "title": video_snippet.get("title", f"{artist_name} - Classic Song"),
                                "video_id": video_id,
                                "artist": artist_name,
                                "cultural_connection": entity.get("cultural_context", {}),
                                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                                "caregiver_guidance": {
                                    "implementation": f"Play {artist_name} music during activities",
                                    "engagement": "Ask about memories associated with this music",
                                    "volume": "Keep at comfortable level, adjust as needed",
                                    "duration": "Start with 3-5 minutes, extend if they enjoy it"
                                },
                                "accessibility": {
                                    "volume_control": "Adjustable",
                                    "subtitle_options": "Available on YouTube",
                                    "visual_component": "Can watch or just listen"
                                }
                            })
                else:
                    logger.warning(f"No YouTube results for {artist_name}")
                
                await asyncio.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"YouTube music search failed for {artist_name}: {str(e)}")
        
        return youtube_content
    
    def _generate_ambient_sound_suggestions_fixed(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FIXED: Generate ambient sound suggestions that always work."""
        
        ambient_sounds = [
            {
                "content_subtype": "ambient_sound",
                "activity": "Nature sounds listening",
                "name": "Nature Sounds",
                "description": "Gentle rain, ocean waves, or forest sounds",
                "cultural_connection": "universal_nature_connection",
                "implementation": {
                    "setup": "Use smartphone, tablet, or smart speaker",
                    "method": "Search for 'rain sounds' or 'ocean waves' on YouTube/Spotify",
                    "duration": "Can play continuously in background"
                },
                "caregiver_guidance": {
                    "implementation": "Play softly in background during activities",
                    "engagement": "Ask about favorite outdoor places or weather memories",
                    "volume": "Very low volume, barely audible",
                    "customization": "Try different nature sounds to find preferences"
                }
            },
            {
                "content_subtype": "ambient_sound",
                "activity": "Soft instrumental music",
                "name": "Gentle Instrumental Music",
                "description": "Piano, acoustic guitar, or string instruments",
                "cultural_connection": "universal_music_appreciation",
                "implementation": {
                    "setup": "Use any music streaming service or radio",
                    "method": "Search for 'gentle piano music' or 'relaxing instrumental'",
                    "duration": "30 minutes to several hours"
                },
                "caregiver_guidance": {
                    "implementation": "Use during quiet activities or conversation",
                    "engagement": "Notice if it helps with relaxation or mood",
                    "volume": "Background level only",
                    "customization": "Switch between piano, guitar, or classical based on response"
                }
            }
        ]
        
        return ambient_sounds
    
    def _generate_conversation_starters(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate conversation starter activities."""
        
        cultural_themes = sensory_strategy.get("cultural_themes", [])
        
        conversation_starters = [
            {
                "content_subtype": "conversation_starter",
                "activity": "Memory sharing conversation",
                "topic": "Favorite music and songs",
                "description": "Talk about music that was meaningful to them",
                "conversation_guide": {
                    "opening": "What was your favorite song when you were younger?",
                    "follow_up_questions": [
                        "Do you remember where you first heard it?",
                        "Did you dance to any special songs?",
                        "What music did your family enjoy together?"
                    ]
                },
                "caregiver_guidance": {
                    "implementation": "Ask open-ended questions about music memories",
                    "engagement": "Share your own music memories too",
                    "pacing": "Give them time to remember, don't rush",
                    "response": "Accept all answers, focus on emotions rather than facts"
                }
            }
        ]
        
        # Add theme-specific conversation starters
        if cultural_themes:
            for theme in cultural_themes[:2]:
                conversation_starters.append({
                    "content_subtype": "era_conversation",
                    "activity": f"Conversation about {theme}",
                    "topic": f"Memories related to {theme}",
                    "description": f"Explore memories and experiences related to {theme}",
                    "conversation_guide": {
                        "opening": f"Tell me about {theme} - what does that remind you of?",
                        "follow_up_questions": [
                            f"What do you remember about {theme}?",
                            f"Did {theme} play a role in your family?",
                            f"What feelings does {theme} bring up for you?"
                        ]
                    },
                    "caregiver_guidance": {
                        "implementation": f"Use {theme} as a conversation starting point",
                        "engagement": "Follow their lead on what aspects interest them",
                        "customization": "Adapt questions based on their responses",
                        "safety": "Change topics if it causes distress"
                    }
                })
        
        return conversation_starters
    
    async def _generate_gustatory_content_fixed(self, 
                                              sensory_strategy: Dict[str, Any],
                                              cultural_elements: Dict[str, Any],
                                              blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Generate gustatory content with proper error handling."""
        
        gustatory_content = {
            "available": True,
            "content_type": "gustatory",
            "elements": []
        }
        
        # Check if food content is blocked
        if self._is_content_blocked("food", blocked_content):
            gustatory_content["available"] = False
            gustatory_content["blocked_reason"] = "user_feedback"
            return gustatory_content
        
        # Generate recipes using Gemini with better error handling
        try:
            recipes = await self._generate_cultural_recipes_fixed(sensory_strategy, cultural_elements)
            if recipes:  # Only add if we got results
                gustatory_content["elements"].extend(recipes)
                logger.info(f"Generated {len(recipes)} recipe elements")
        except Exception as e:
            logger.warning(f"Recipe generation failed: {str(e)}")
        
        # ALWAYS generate simple snack suggestions as fallback
        snack_suggestions = self._generate_snack_suggestions_fixed(sensory_strategy)
        gustatory_content["elements"].extend(snack_suggestions)
        
        logger.info(f"Generated {len(gustatory_content['elements'])} gustatory elements total")
        return gustatory_content
    
    async def _generate_cultural_recipes_fixed(self, 
                                             sensory_strategy: Dict[str, Any],
                                             cultural_elements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FIXED: Generate culturally-informed recipes with better error handling."""
        
        cultural_themes = sensory_strategy.get("cultural_themes", [])
        recipes = []
        
        # Use cultural themes if available, otherwise use comfort food
        themes_to_use = cultural_themes[:2] if cultural_themes else ["comfort food", "family meal"]
        
        for theme in themes_to_use:
            try:
                recipe_prompt = f"""
                Generate a simple, accessible recipe that could connect to {theme} cultural elements,
                but avoid stereotypical assumptions. Focus on:
                
                1. Simple ingredients that are easy to find
                2. Clear, step-by-step instructions suitable for dementia care
                3. Opportunities for caregiver-patient interaction during cooking
                4. Sensory engagement (smells, textures, tastes)
                5. Safety considerations and adaptations
                6. Memory-triggering potential through familiar flavors or cooking activities
                
                The recipe should be:
                - Easy to moderate difficulty
                - 30-45 minutes total time
                - Adaptable for different dietary needs
                - Safe for people with dementia
                - Focused on the cooking experience, not just the end result
                """
                
                # FIXED: Use correct tool reference
                recipe_data = await self._gemini_tool.generate_recipe(recipe_prompt)
                
                if recipe_data and recipe_data.get("name"):
                    # FIXED: Add proper activity structure
                    recipe_element = {
                        "content_subtype": "heritage_inspired_recipe",
                        "activity": f"Cooking together: {recipe_data.get('name', 'Recipe')}",
                        "recipe_data": recipe_data,
                        "cultural_theme": theme,
                        "implementation": {
                            "setup": "Gather all ingredients and cooking tools together",
                            "method": "Cook together, involving them in safe steps",
                            "duration": recipe_data.get("total_time", "30-45 minutes")
                        },
                        "caregiver_guidance": {
                            "preparation": "Read through recipe together first",
                            "engagement": "Let them help with safe tasks like stirring or measuring",
                            "safety": "Supervise all knife and heat use",
                            "customization": "Adapt recipe based on dietary needs and abilities"
                        },
                        "sensory_benefits": {
                            "smell": "Cooking aromas throughout preparation",
                            "touch": "Feeling ingredients and textures",
                            "taste": "Sampling during cooking process",
                            "sight": "Watching food transform during cooking",
                            "sound": "Kitchen sounds and conversation"
                        }
                    }
                    recipes.append(recipe_element)
                    logger.info(f"Generated recipe: {recipe_data.get('name')}")
                else:
                    logger.warning(f"Recipe generation returned empty data for theme {theme}")
                
                await asyncio.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Recipe generation failed for theme {theme}: {str(e)}")
        
        return recipes
    
    def _generate_snack_suggestions_fixed(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FIXED: Generate simple snack suggestions that always work."""
        
        snacks = [
            {
                "content_subtype": "universal_comfort_recipe",
                "activity": "Making a fruit and cheese plate together",
                "name": "Fruit and Cheese Plate",
                "description": "Simple combination of soft fruits and mild cheese",
                "ingredients": [
                    {"item": "soft fruits", "examples": "bananas, grapes, berries"},
                    {"item": "mild cheese", "examples": "cheddar, swiss, or their favorite"},
                    {"item": "crackers", "examples": "simple crackers or bread"}
                ],
                "implementation": {
                    "setup": "Wash fruits, cut cheese into small cubes",
                    "method": "Arrange together on a plate",
                    "duration": "10-15 minutes preparation"
                },
                "caregiver_guidance": {
                    "preparation": "Let them help wash fruits and arrange the plate",
                    "engagement": "Talk about favorite fruits or cheese preferences",
                    "safety": "Cut into appropriate sizes, check for dietary restrictions",
                    "customization": "Use their favorite fruits and cheese varieties"
                },
                "sensory_benefits": {
                    "taste": "Multiple familiar flavors",
                    "touch": "Different textures to explore",
                    "smell": "Natural fruit and cheese aromas",
                    "sight": "Colorful, appealing presentation"
                }
            },
            {
                "content_subtype": "warm_beverage_experience",
                "activity": "Making warm tea or hot chocolate together",
                "name": "Warm Beverage Time",
                "description": "Comforting warm beverage preparation and sharing",
                "ingredients": [
                    {"item": "tea bags or hot chocolate mix", "examples": "chamomile, earl grey, or hot chocolate"},
                    {"item": "warm milk or water"},
                    {"item": "optional additions", "examples": "honey, cinnamon, or marshmallows"}
                ],
                "implementation": {
                    "setup": "Heat liquid, prepare cups and additions",
                    "method": "Steep tea or mix chocolate together",
                    "duration": "10-15 minutes including drinking time"
                },
                "caregiver_guidance": {
                    "preparation": "Let them choose the beverage and help prepare",
                    "engagement": "Share stories about favorite drinks or tea time memories",
                    "safety": "Check temperature carefully, use cups with handles",
                    "customization": "Adjust sweetness and temperature to preference"
                },
                "sensory_benefits": {
                    "smell": "Steam and beverage aromas",
                    "taste": "Warm, comforting flavors",
                    "touch": "Warmth of the cup",
                    "sight": "Steam rising from the cup"
                }
            }
        ]
        
        return snacks
    
    def _generate_olfactory_content_fixed(self, 
                                        sensory_strategy: Dict[str, Any],
                                        gustatory_content: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Generate olfactory content with better structure."""
        
        olfactory_content = {
            "available": True,
            "content_type": "olfactory",
            "elements": []
        }
        
        # Extract cooking aromas from gustatory content
        cooking_aromas = []
        for element in gustatory_content.get("elements", []):
            if element.get("content_subtype") in ["heritage_inspired_recipe", "universal_comfort_recipe"]:
                recipe_name = element.get("name", element.get("activity", "Recipe"))
                cooking_aromas.append({
                    "content_subtype": "cooking_aroma",
                    "activity": f"Enjoying cooking aromas from {recipe_name}",
                    "name": f"Cooking aromas from {recipe_name}",
                    "description": f"The smells that come from preparing {recipe_name}",
                    "source": "recipe_preparation",
                    "implementation": {
                        "setup": "Cook together and focus on smells",
                        "method": "Point out different aromas as they develop",
                        "duration": "Throughout cooking process"
                    },
                    "caregiver_guidance": {
                        "implementation": "Point out different smells during cooking",
                        "engagement": "Ask what the smells remind them of",
                        "safety": "Ensure good ventilation during cooking",
                        "customization": "Focus on scents they respond positively to"
                    }
                })
        
        olfactory_content["elements"].extend(cooking_aromas)
        
        # Add general pleasant scents that are always available
        general_scents = [
            {
                "content_subtype": "cultural_scent",
                "activity": "Fresh flower appreciation",
                "name": "Fresh Flowers",
                "description": "Mild floral scents from fresh flowers",
                "source": "fresh_flowers",
                "implementation": {
                    "setup": "Place fresh flowers in room (check for allergies first)",
                    "method": "Enjoy natural flower scents",
                    "duration": "Ongoing - flowers last several days"
                },
                "caregiver_guidance": {
                    "implementation": "Place fresh flowers in room if no allergies",
                    "engagement": "Ask about favorite flowers or garden memories",
                    "safety": "Check for allergies, avoid strong scents",
                    "customization": "Use flowers they recognize or have mentioned"
                }
            },
            {
                "content_subtype": "spice_exploration",
                "activity": "Gentle spice and herb exploration",
                "name": "Vanilla or Cinnamon Scents",
                "description": "Gentle, familiar baking scents",
                "source": "baking_spices",
                "implementation": {
                    "setup": "Have mild spices available (cinnamon, vanilla)",
                    "method": "Let them smell spices or add to drinks/cooking",
                    "duration": "A few minutes at a time"
                },
                "caregiver_guidance": {
                    "implementation": "Use during baking activities or add to drinks",
                    "engagement": "Talk about baking memories or favorite scents",
                    "safety": "Use sparingly, avoid overwhelming scents",
                    "customization": "Use only scents they find pleasant"
                }
            }
        ]
        
        olfactory_content["elements"].extend(general_scents)
        
        logger.info(f"Generated {len(olfactory_content['elements'])} olfactory elements")
        return olfactory_content
    
    async def _generate_visual_content_fixed(self, 
                                           sensory_strategy: Dict[str, Any],
                                           cultural_recommendations: Dict[str, Any],
                                           blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Generate visual content with proper error handling."""
        
        visual_content = {
            "available": True,
            "content_type": "visual",
            "elements": []
        }
        
        # Check for video recommendations from Qloo
        video_entities = []
        for entity_type in ["urn:entity:movie", "urn:entity:tv_show"]:
            if entity_type in cultural_recommendations:
                recommendation = cultural_recommendations[entity_type]
                if recommendation.get("available") and recommendation.get("entities"):
                    video_entities.extend(recommendation.get("entities", []))
        
        # Generate YouTube video content if not blocked
        if video_entities and not self._is_content_blocked("video", blocked_content):
            try:
                youtube_videos = await self._generate_youtube_video_content_fixed(video_entities[:3])
                if youtube_videos:
                    visual_content["elements"].extend(youtube_videos)
                    logger.info(f"Generated {len(youtube_videos)} YouTube video elements")
            except Exception as e:
                logger.warning(f"YouTube video generation failed: {str(e)}")
        
        # ALWAYS generate visual activities as fallback
        visual_activities = self._generate_visual_activities_fixed(sensory_strategy)
        visual_content["elements"].extend(visual_activities)
        
        # Generate photo viewing suggestions
        photo_suggestions = self._generate_photo_viewing_suggestions_fixed(sensory_strategy)
        visual_content["elements"].extend(photo_suggestions)
        
        logger.info(f"Generated {len(visual_content['elements'])} visual elements total")
        return visual_content
    
    async def _generate_youtube_video_content_fixed(self, video_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """FIXED: Generate YouTube video content with proper error handling."""
        
        youtube_content = []
        
        for entity in video_entities:
            content_name = entity.get("name", "")
            if not content_name:
                continue
            
            try:
                # FIXED: Use correct tool reference
                search_results = await self._youtube_tool.search_videos(
                    query=f"{content_name} classic scenes highlights",
                    max_results=2
                )
                
                if search_results and search_results.get("items"):
                    for video in search_results["items"]:
                        video_snippet = video.get("snippet", {})
                        video_id_obj = video.get("id", {})
                        video_id = video_id_obj.get("videoId", "") if isinstance(video_id_obj, dict) else ""
                        
                        if video_id:  # Only add if we have a valid video ID
                            youtube_content.append({
                                "content_subtype": "youtube_video",
                                "activity": f"Watching {content_name} together",
                                "title": video_snippet.get("title", f"{content_name} - Classic Content"),
                                "video_id": video_id,
                                "original_content": content_name,
                                "cultural_connection": entity.get("cultural_context", {}),
                                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                                "implementation": {
                                    "setup": "Comfortable seating with good view of screen",
                                    "method": "Watch together, pause for comments",
                                    "duration": "Start with 5-15 minutes, extend if engaged"
                                },
                                "caregiver_guidance": {
                                    "implementation": f"Watch {content_name} content together",
                                    "engagement": "Comment on scenes, ask about memories",
                                    "attention": "Watch for attention span, pause if needed",
                                    "customization": "Adjust volume and lighting for comfort"
                                },
                                "viewing_notes": {
                                    "duration": "Start with short clips (5-15 minutes)",
                                    "interaction": "Encourage comments and reactions",
                                    "comfort": "Ensure comfortable seating and lighting"
                                }
                            })
                else:
                    logger.warning(f"No YouTube results for {content_name}")
                
                await asyncio.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"YouTube video search failed for {content_name}: {str(e)}")
        
        return youtube_content
    
    def _generate_visual_activities_fixed(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FIXED: Generate visual activities that always work."""
        
        activities = [
            {
                "content_subtype": "photo_viewing",
                "activity": "Family photo album review",
                "name": "Photo Album Time",
                "description": "Look through family photos or cultural images together",
                "materials": "Photo albums, printed photos, or tablet with photos",
                "implementation": {
                    "setup": "Comfortable seating with good lighting",
                    "method": "Go through photos slowly together",
                    "duration": "15-30 minutes or as long as they're interested"
                },
                "caregiver_guidance": {
                    "engagement": "Ask open-ended questions about photos",
                    "pacing": "Go slowly, don't rush through images",
                    "response": "Follow their lead on which photos interest them",
                    "safety": "Choose photos that usually bring positive reactions"
                }
            },
            {
                "content_subtype": "nature_observation",
                "activity": "Nature viewing and observation",
                "name": "Window Nature Watching",
                "description": "Look out windows at nature or view nature content",
                "materials": "Window view, nature magazines, or nature videos/photos",
                "implementation": {
                    "setup": "Sit by window or set up nature viewing materials",
                    "method": "Point out interesting things in nature",
                    "duration": "10-20 minutes of focused observation"
                },
                "caregiver_guidance": {
                    "engagement": "Talk about animals, plants, weather, or seasons",
                    "interaction": "Ask about favorite outdoor places or nature memories",
                    "comfort": "Ensure good lighting and comfortable seating",
                    "customization": "Focus on nature elements they show interest in"
                }
            }
        ]
        
        return activities
    
    def _generate_photo_viewing_suggestions_fixed(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FIXED: Generate photo viewing suggestions."""
        
        suggestions = [
            {
                "content_subtype": "family_photo_time",
                "activity": "Dedicated family photo viewing",
                "name": "Family Memory Time",
                "description": "Focused time for looking at meaningful family photos",
                "implementation": {
                    "setup": "Comfortable seating with good lighting and photo materials",
                    "method": "Look at photos together, let them guide the conversation",
                    "duration": "15-30 minutes or based on their engagement"
                },
                "caregiver_guidance": {
                    "preparation": "Choose photos that usually bring positive reactions",
                    "interaction": "Ask who people are, when photos were taken, what was happening",
                    "flexibility": "Be ready to change photos if reaction is negative",
                    "focus": "Focus on emotions and feelings rather than facts"
                }
            }
        ]
        
        return suggestions
    
    def _generate_tactile_content_fixed(self, 
                                      sensory_strategy: Dict[str, Any],
                                      cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Generate tactile content that always works."""
        
        tactile_content = {
            "available": True,
            "content_type": "tactile",
            "elements": []
        }
        
        # Generate tactile activities that are always available
        tactile_activities = [
            {
                "content_subtype": "texture_exploration",
                "activity": "Safe texture exploration",
                "name": "Texture Discovery",
                "description": "Feel different safe and pleasant textures",
                "materials": "Soft fabrics, smooth stones, textured papers, safe household items",
                "implementation": {
                    "setup": "Gather various safe textures in a basket or tray",
                    "method": "Let them touch and explore different materials",
                    "duration": "10-15 minutes or as long as they're interested"
                },
                "caregiver_guidance": {
                    "safety": "Ensure all materials are safe, clean, and appropriate size",
                    "engagement": "Ask how textures feel - soft, smooth, rough, warm",
                    "response": "Remove any textures they don't like immediately",
                    "customization": "Use textures that remind them of meaningful objects"
                }
            },
            {
                "content_subtype": "gentle_touch",
                "activity": "Gentle hand or shoulder massage",
                "name": "Gentle Touch Time",
                "description": "Comforting gentle massage with permission",
                "materials": "Gentle lotion or oil (if no allergies), soft towels",
                "implementation": {
                    "setup": "Comfortable seating, gentle lotion if appropriate",
                    "method": "Offer gentle hand or shoulder massage with permission",
                    "duration": "5-15 minutes based on their comfort"
                },
                "caregiver_guidance": {
                    "consent": "Always ask permission before any touching",
                    "gentleness": "Use very gentle pressure, follow their comfort level",
                    "observation": "Watch for comfort level and adjust immediately",
                    "safety": "Stop immediately if they show any discomfort"
                }
            }
        ]
        
        tactile_content["elements"].extend(tactile_activities)
        
        logger.info(f"Generated {len(tactile_content['elements'])} tactile elements")
        return tactile_content
    
    def _create_cross_sensory_experiences(self, 
                                        auditory_content: Dict[str, Any],
                                        gustatory_content: Dict[str, Any],
                                        olfactory_content: Dict[str, Any],
                                        visual_content: Dict[str, Any],
                                        tactile_content: Dict[str, Any],
                                        sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """FIXED: Create meaningful cross-sensory experiences."""
        
        cross_sensory_experiences = []
        
        # Create cooking experience (combines multiple senses)
        recipes = [e for e in gustatory_content.get("elements", []) if "recipe" in e.get("content_subtype", "")]
        for recipe in recipes[:1]:  # One main cooking experience
            experience = {
                "experience_name": f"Complete cooking experience: {recipe.get('name', 'Recipe')}",
                "experience_type": "cooking_multi_sensory",
                "primary_senses": ["gustatory", "olfactory", "tactile", "visual", "auditory"],
                "sensory_elements": {
                    "gustatory": recipe.get("name", "Cooking recipe"),
                    "olfactory": f"Cooking aromas from {recipe.get('name', 'recipe')}",
                    "tactile": "Feeling ingredients and cooking utensils",
                    "visual": "Watching food preparation and cooking",
                    "auditory": "Kitchen sounds and conversation"
                },
                "implementation_guide": {
                    "setup": "Prepare all ingredients and cooking space together",
                    "process": "Involve them in safe cooking steps throughout",
                    "sensory_focus": "Point out smells, textures, colors, and sounds",
                    "completion": "Enjoy the meal together with continued conversation"
                },
                "caregiver_guidance": {
                    "preparation": "Have all materials ready before starting",
                    "engagement": "Engage all senses throughout the cooking process",
                    "safety": "Supervise all cooking steps, adapt based on abilities",
                    "customization": "Focus on senses they respond to most positively"
                }
            }
            cross_sensory_experiences.append(experience)
        
        # Create music and movement experience
        music_content = [e for e in auditory_content.get("elements", []) if e.get("content_subtype") == "youtube_music"]
        if music_content:
            experience = {
                "experience_name": "Music listening with gentle movement",
                "experience_type": "music_multi_sensory",
                "primary_senses": ["auditory", "tactile", "visual"],
                "sensory_elements": {
                    "auditory": "Music playing",
                    "tactile": "Gentle swaying or hand movements",
                    "visual": "Watching each other, observing responses"
                },
                "implementation_guide": {
                    "setup": "Comfortable seating with space for gentle movement",
                    "process": "Start music and encourage gentle movement or swaying",
                    "sensory_focus": "Feel the rhythm, watch for responses, listen together",
                    "adaptation": "Adjust volume and movement to their comfort level"
                },
                "caregiver_guidance": {
                    "preparation": "Choose music they've responded positively to",
                    "engagement": "Move together, follow their lead and comfort level",
                    "safety": "Ensure safe space for any movement",
                    "customization": "Adapt based on their mobility and preferences"
                }
            }
            cross_sensory_experiences.append(experience)
        
        # Create photo viewing with conversation experience
        photo_activities = [e for e in visual_content.get("elements", []) if "photo" in e.get("content_subtype", "")]
        if photo_activities:
            experience = {
                "experience_name": "Photo memories with conversation",
                "experience_type": "memory_multi_sensory",
                "primary_senses": ["visual", "auditory", "tactile"],
                "sensory_elements": {
                    "visual": "Looking at meaningful photos",
                    "auditory": "Conversation and memory sharing",
                    "tactile": "Holding photos or photo albums"
                },
                "implementation_guide": {
                    "setup": "Comfortable seating with good lighting and photo materials",
                    "process": "Look at photos together while encouraging conversation",
                    "sensory_focus": "See the images, hear the stories, feel the photos",
                    "connection": "Connect visual memories with verbal sharing"
                },
                "caregiver_guidance": {
                    "preparation": "Select photos that typically bring positive responses",
                    "engagement": "Ask open-ended questions, share your own observations",
                    "flexibility": "Be ready to change photos if they cause distress",
                    "focus": "Focus on emotions and feelings rather than facts"
                }
            }
            cross_sensory_experiences.append(experience)
        
        logger.info(f"Created {len(cross_sensory_experiences)} cross-sensory experiences")
        return cross_sensory_experiences
    
    def _generate_implementation_guidance(self, cross_sensory_experiences: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive implementation guidance for caregivers."""
        
        guidance = {
            "general_principles": [
                "Follow the person's lead and preferences at all times",
                "Start with one sense and gradually add others if they're comfortable",
                "Watch for signs of overwhelm and adjust or stop immediately",
                "Focus on the experience and connection, not achieving perfect outcomes",
                "Be flexible and ready to change activities based on their responses"
            ],
            "setup_preparation": [
                "Choose a quiet, comfortable environment free from distractions",
                "Ensure good lighting for visual activities",
                "Have all materials ready before starting any activity",
                "Check for any allergies or sensitivities before using scents or foods",
                "Make sure the person is comfortable, fed, and has used the bathroom"
            ],
            "engagement_strategies": [
                "Use open-ended questions that don't require specific memory recall",
                "Share your own reactions and experiences to model engagement",
                "Allow for comfortable silence and processing time",
                "Encourage participation but never force or pressure",
                "Celebrate any level of engagement, no matter how small"
            ],
            "safety_first": [
                "Check for allergies before using any scents, foods, or materials",
                "Ensure all materials are safe, clean, and appropriate size",
                "Monitor continuously for signs of distress, confusion, or discomfort",
                "Have a plan for ending activities quickly if needed",
                "Keep emergency contacts and important information readily available"
            ],
            "adaptation_guidelines": [
                "Simplify activities if they seem too complex or overwhelming",
                "Increase or decrease sensory stimulation based on their responses",
                "Modify activities for any physical limitations or preferences",
                "Change activities immediately if attention wanes or distress occurs",
                "Always respect 'no' responses and offer gentle alternatives"
            ],
            "success_indicators": [
                "Any positive facial expressions, smiles, or laughter",
                "Sustained attention or interest in the activity",
                "Verbal responses, questions, or comments",
                "Physical engagement like reaching, touching, or moving",
                "Relaxed body language and comfortable participation"
            ]
        }
        
        return guidance
    
    def _generate_content_summary(self, all_sensory_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of all generated content for reporting."""
        
        summary = {
            "total_elements_generated": 0,
            "elements_by_sense": {},
            "content_types_created": [],
            "cross_sensory_potential": 0
        }
        
        sense_names = ["auditory", "gustatory", "olfactory", "visual", "tactile"]
        
        for i, sense_content in enumerate(all_sensory_content):
            sense_name = sense_names[i] if i < len(sense_names) else f"sense_{i}"
            element_count = len(sense_content.get("elements", []))
            
            summary["total_elements_generated"] += element_count
            summary["elements_by_sense"][sense_name] = element_count
            
            # Collect content types
            for element in sense_content.get("elements", []):
                content_type = element.get("content_subtype", "unknown")
                if content_type not in summary["content_types_created"]:
                    summary["content_types_created"].append(content_type)
        
        return summary
    
    def _get_activated_senses(self, all_sensory_content: List[Dict[str, Any]]) -> List[str]:
        """Get list of senses that have generated content."""
        
        activated_senses = []
        sense_names = ["auditory", "gustatory", "olfactory", "visual", "tactile"]
        
        for i, sense_content in enumerate(all_sensory_content):
            if sense_content.get("available") and sense_content.get("elements"):
                sense_name = sense_names[i] if i < len(sense_names) else f"sense_{i}"
                activated_senses.append(sense_name)
        
        return activated_senses
    
    def _is_content_blocked(self, content_type: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if a content type is blocked by user feedback."""
        
        blocked_types = blocked_content.get("blocked_content_types", [])
        return content_type in blocked_types
    
    def _create_fallback_sensory_content(self, 
                                       consolidated_info: Dict[str, Any],
                                       cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Create comprehensive fallback sensory content when APIs fail."""
        
        request_type = consolidated_info.get("request_context", {}).get("request_type", "dashboard")
        
        # Create basic sensory content that always works
        fallback_auditory = {
            "available": True,
            "content_type": "auditory",
            "elements": [
                {
                    "content_subtype": "conversation_starter",
                    "activity": "Music memory conversation",
                    "description": "Talk about favorite songs and music memories",
                    "caregiver_guidance": {
                        "implementation": "Ask about music they enjoyed when younger",
                        "engagement": "Share your own music memories too"
                    }
                }
            ]
        }
        
        fallback_gustatory = {
            "available": True,
            "content_type": "gustatory",
            "elements": [
                {
                    "content_subtype": "universal_comfort_recipe",
                    "activity": "Simple snack preparation",
                    "name": "Tea and Cookies",
                    "description": "Make warm tea and enjoy simple cookies together",
                    "caregiver_guidance": {
                        "implementation": "Prepare warm beverage and snack together",
                        "engagement": "Talk about favorite treats and beverages"
                    }
                }
            ]
        }
        
        fallback_visual = {
            "available": True,
            "content_type": "visual",
            "elements": [
                {
                    "content_subtype": "photo_viewing",
                    "activity": "Family photo time",
                    "description": "Look at family photos together",
                    "caregiver_guidance": {
                        "implementation": "Go through photos slowly together",
                        "engagement": "Ask open-ended questions about the photos"
                    }
                }
            ]
        }
        
        return {
            "sensory_content": {
                "generation_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "fallback_used": True,
                    "fallback_reason": "api_unavailable_or_error",
                    "request_type": request_type
                },
                "auditory": fallback_auditory,
                "gustatory": fallback_gustatory,
                "olfactory": {"available": True, "content_type": "olfactory", "elements": []},
                "visual": fallback_visual,
                "tactile": {"available": True, "content_type": "tactile", "elements": []},
                "cross_sensory_experiences": [
                    {
                        "experience_name": "Simple shared activities",
                        "experience_type": "basic_multi_sensory",
                        "primary_senses": ["auditory", "visual", "gustatory"],
                        "implementation_guide": {
                            "approach": "Combine conversation, photos, and simple snacks",
                            "guidance": "Focus on being together and sharing simple moments"
                        }
                    }
                ],
                "implementation_guidance": self._generate_implementation_guidance([]),
                "content_summary": {
                    "total_elements_generated": 3,
                    "fallback_mode": True,
                    "note": "Basic activities that always work when technology fails"
                }
            }
        }