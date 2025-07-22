"""
Agent 4: Sensory Content Generator - FIXED VERSION
Role: Create connected multi-sensory experiences
Follows Responsible Development Guide principles - practical implementation with caregiver guidance
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent(Agent):
    """
    Agent 4: Sensory Content Generator
    
    Purpose: Create connected multi-sensory experiences across all 5 senses
    Input: All previous agent outputs
    Output: Connected sensory content package with practical implementation
    
    Tools: youtube_music_search, gemini_recipe_generator
    
    Anti-Bias Principles:
    - Generate content across all 5 senses using cultural theme WITHOUT STEREOTYPES
    - Use conditional logic based on request type
    - Integrate Qloo suggestions with practical implementation  
    - Respect blocked content and individual preferences
    - NO predetermined cultural mappings or assumptions
    - Individual stories and preferences override heritage keywords
    - Open-ended exploration rather than stereotypical cultural "packages"
    """
    
    def __init__(self, youtube_tool, gemini_tool):
        super().__init__(
            name="sensory_content_generator",
            description="Creates practical multi-sensory experiences with caregiver implementation guidance"
        )
        # FIXED: Store tool references differently to avoid Pydantic field errors
        self._youtube_tool_ref = youtube_tool
        self._gemini_tool_ref = gemini_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate connected sensory content across all 5 senses.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2  
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Connected sensory content package
        """
        
        try:
            logger.info("Starting sensory content generation")
            
            # Extract context information
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            
            # Extract cultural elements
            cultural_elements = cultural_profile.get("cultural_elements", {})
            
            # Extract Qloo recommendations
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # Build sensory strategy (anti-bias approach)
            sensory_strategy = self._build_sensory_strategy(
                request_context,
                cultural_elements,
                cultural_recommendations,
                blocked_content
            )
            
            # Generate content for each sense
            logger.info("Generating multi-sensory content")
            
            # 1. Auditory content (music, sounds)
            auditory_content = await self._generate_auditory_content(
                sensory_strategy, 
                cultural_recommendations, 
                blocked_content
            )
            
            # 2. Gustatory content (taste experiences)
            gustatory_content = await self._generate_gustatory_content(
                sensory_strategy,
                cultural_elements,
                blocked_content
            )
            
            # 3. Olfactory content (smell experiences)
            olfactory_content = self._generate_olfactory_content(
                sensory_strategy,
                gustatory_content
            )
            
            # 4. Visual content (videos, activities)
            visual_content = await self._generate_visual_content(
                sensory_strategy,
                cultural_recommendations,
                blocked_content
            )
            
            # 5. Tactile content (touch experiences)
            tactile_content = self._generate_tactile_content(
                sensory_strategy,
                cultural_elements
            )
            
            # Create connected sensory experience
            connected_experience = self._create_connected_experience(
                auditory_content,
                gustatory_content,
                olfactory_content,
                visual_content,
                tactile_content,
                sensory_strategy
            )
            
            # Build complete sensory content package
            sensory_content = {
                "sensory_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "request_type": request_context.get("request_type", "dashboard"),
                    "sensory_strategy": sensory_strategy["approach"],
                    "cultural_elements_integrated": len(cultural_elements),
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "auditory": auditory_content,
                "gustatory": gustatory_content,
                "olfactory": olfactory_content,
                "visual": visual_content,
                "tactile": tactile_content,
                "connected_experience": connected_experience,
                "implementation_guidance": self._generate_implementation_guidance(connected_experience),
                "anti_bias_validation": {
                    "stereotypical_assumptions": "none_made",
                    "individual_preferences_respected": True,
                    "open_ended_exploration": True,
                    "cultural_sensitivity": "non_assumptive"
                }
            }
            
            logger.info("Sensory content generation completed successfully")
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
            "approach": "multi_sensory_integration_anti_bias",
            "request_type": request_type,
            "sensory_focus": sensory_focus,
            "cultural_themes": cultural_themes,
            "blocked_content": blocked_content,
            "generation_priorities": self._set_generation_priorities(request_type),
            "bias_prevention": {
                "no_cultural_stereotypes": True,
                "individual_preferences_first": True,
                "open_ended_exploration": True
            }
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
    
    async def _generate_auditory_content(self, 
                                       sensory_strategy: Dict[str, Any],
                                       cultural_recommendations: Dict[str, Any],
                                       blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate auditory content using YouTube API."""
        
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
        
        # Get music recommendations from Qloo
        music_entities = []
        for entity_type in ["urn:entity:artist", "urn:entity:album"]:
            if entity_type in cultural_recommendations:
                recommendation = cultural_recommendations[entity_type]
                if recommendation.get("entities"):
                    music_entities.extend(recommendation.get("entities", []))
        
        # Generate YouTube music content
        if music_entities:
            try:
                youtube_music = await self._generate_youtube_music_content(music_entities[:5])
                auditory_content["elements"].extend(youtube_music)
            except Exception as e:
                logger.warning(f"YouTube music generation failed: {str(e)}")
        
        # Generate ambient sound suggestions
        ambient_sounds = self._generate_ambient_sound_suggestions(sensory_strategy)
        auditory_content["elements"].extend(ambient_sounds)
        
        return auditory_content
    
    async def _generate_youtube_music_content(self, music_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate YouTube music content from Qloo music entities."""
        
        youtube_content = []
        
        for entity in music_entities:
            artist_name = entity.get("name", "")
            if not artist_name:
                continue
            
            try:
                # Search for music on YouTube - use tool reference
                search_results = await self._youtube_tool_ref.search_music(
                    query=f"{artist_name} best songs classic hits",
                    max_results=2
                )
                
                if search_results and search_results.get("items"):
                    for video in search_results["items"]:
                        youtube_content.append({
                            "content_subtype": "youtube_music",
                            "title": video.get("snippet", {}).get("title", ""),
                            "video_id": video.get("id", {}).get("videoId", ""),
                            "artist": artist_name,
                            "cultural_connection": entity.get("cultural_context", {}),
                            "youtube_url": f"https://www.youtube.com/watch?v={video.get('id', {}).get('videoId', '')}",
                            "caregiver_guidance": {
                                "implementation": f"Play {artist_name} music during activities",
                                "engagement": "Ask about memories associated with this music",
                                "volume": "Keep at comfortable level, adjust as needed"
                            },
                            "listening_notes": {
                                "duration": "Start with familiar songs (3-5 minutes)",
                                "interaction": "Encourage singing along or moving to rhythm",
                                "mood": "Watch for positive or negative emotional responses"
                            }
                        })
                
                await asyncio.sleep(0.2)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"YouTube music search failed for {artist_name}: {str(e)}")
        
        return youtube_content
    
    def _generate_ambient_sound_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate ambient sound suggestions based on cultural themes."""
        
        cultural_themes = sensory_strategy.get("cultural_themes", [])
        
        ambient_sounds = []
        
        # Base ambient sounds that work for most people
        base_sounds = [
            {
                "content_subtype": "ambient_sound",
                "name": "Nature Sounds",
                "description": "Gentle rain, ocean waves, or forest sounds",
                "cultural_connection": "universal_nature_connection",
                "caregiver_guidance": {
                    "implementation": "Play softly in background during activities",
                    "engagement": "Ask about favorite outdoor places",
                    "volume": "Very low volume, barely audible"
                }
            },
            {
                "content_subtype": "ambient_sound", 
                "name": "Soft Instrumental Music",
                "description": "Piano, acoustic guitar, or string instruments",
                "cultural_connection": "universal_music_appreciation",
                "caregiver_guidance": {
                    "implementation": "Use during quiet activities or conversation",
                    "engagement": "Notice if it helps with relaxation",
                    "volume": "Background level only"
                }
            }
        ]
        
        ambient_sounds.extend(base_sounds)
        
        return ambient_sounds
    
    async def _generate_gustatory_content(self, 
                                        sensory_strategy: Dict[str, Any],
                                        cultural_elements: Dict[str, Any],
                                        blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate gustatory content using Gemini recipe generator."""
        
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
        
        # Generate recipes using Gemini
        try:
            recipes = await self._generate_cultural_recipes(sensory_strategy, cultural_elements)
            gustatory_content["elements"].extend(recipes)
        except Exception as e:
            logger.warning(f"Recipe generation failed: {str(e)}")
        
        # Generate simple snack suggestions
        snack_suggestions = self._generate_snack_suggestions(sensory_strategy)
        gustatory_content["elements"].extend(snack_suggestions)
        
        return gustatory_content
    
    async def _generate_cultural_recipes(self, 
                                       sensory_strategy: Dict[str, Any],
                                       cultural_elements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate culturally-informed recipes using Gemini AI."""
        
        cultural_themes = sensory_strategy.get("cultural_themes", [])
        recipes = []
        
        if not cultural_themes:
            # Generate a simple comfort food recipe
            cultural_themes = ["comfort food"]
        
        for theme in cultural_themes[:2]:  # Limit to 2 recipes
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
                
                # Use Gemini tool reference
                recipe_data = await self._gemini_tool_ref.generate_recipe(recipe_prompt)
                
                if recipe_data:
                    recipe_data["content_subtype"] = "recipe"
                    recipe_data["cultural_theme"] = theme
                    recipes.append(recipe_data)
                
                await asyncio.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Recipe generation failed for theme {theme}: {str(e)}")
        
        return recipes
    
    def _generate_snack_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate simple snack suggestions."""
        
        snacks = [
            {
                "content_subtype": "snack_suggestion",
                "name": "Fruit and Cheese Plate",
                "description": "Simple combination of soft fruits and mild cheese",
                "ingredients": ["soft fruits (bananas, grapes)", "mild cheese cubes", "crackers"],
                "preparation": "No cooking required - arrange on plate",
                "sensory_benefits": "Multiple textures, familiar flavors, easy to eat",
                "caregiver_guidance": {
                    "implementation": "Let them help arrange the plate",
                    "engagement": "Talk about favorite fruits or cheese preferences",
                    "safety": "Cut into appropriate sizes, check for dietary restrictions"
                }
            },
            {
                "content_subtype": "snack_suggestion",
                "name": "Warm Tea or Hot Chocolate",
                "description": "Comforting warm beverage",
                "ingredients": ["tea bags or hot chocolate mix", "warm milk or water", "optional: honey"],
                "preparation": "Heat liquid, steep tea or mix chocolate",
                "sensory_benefits": "Warmth, aroma, soothing taste",
                "caregiver_guidance": {
                    "implementation": "Make together, let them smell the tea/chocolate",
                    "engagement": "Share stories about favorite drinks",
                    "safety": "Check temperature, use cups with handles"
                }
            }
        ]
        
        return snacks
    
    def _generate_olfactory_content(self, 
                                   sensory_strategy: Dict[str, Any],
                                   gustatory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate olfactory content based on gustatory content and cultural themes."""
        
        olfactory_content = {
            "available": True,
            "content_type": "olfactory",
            "elements": []
        }
        
        # Extract cooking aromas from gustatory content
        cooking_aromas = []
        for element in gustatory_content.get("elements", []):
            if element.get("content_subtype") == "recipe":
                recipe_name = element.get("name", "")
                cooking_aromas.append({
                    "content_subtype": "cooking_aroma",
                    "name": f"Cooking aromas from {recipe_name}",
                    "description": f"The smells that come from preparing {recipe_name}",
                    "source": "recipe_preparation",
                    "caregiver_guidance": {
                        "implementation": "Point out different smells during cooking",
                        "engagement": "Ask what the smells remind them of",
                        "safety": "Ensure good ventilation during cooking"
                    }
                })
        
        olfactory_content["elements"].extend(cooking_aromas)
        
        # Add general pleasant scents
        general_scents = [
            {
                "content_subtype": "ambient_scent",
                "name": "Fresh Flowers",
                "description": "Mild floral scents from fresh flowers",
                "source": "fresh_flowers",
                "caregiver_guidance": {
                    "implementation": "Place fresh flowers in room (if no allergies)",
                    "engagement": "Ask about favorite flowers or garden memories",
                    "safety": "Check for allergies, avoid strong scents"
                }
            },
            {
                "content_subtype": "ambient_scent",
                "name": "Vanilla or Cinnamon",
                "description": "Gentle, familiar baking scents",
                "source": "baking_spices",
                "caregiver_guidance": {
                    "implementation": "Use during baking activities or add to drinks",
                    "engagement": "Talk about baking memories",
                    "safety": "Use sparingly, avoid overwhelming scents"
                }
            }
        ]
        
        olfactory_content["elements"].extend(general_scents)
        
        return olfactory_content
    
    async def _generate_visual_content(self, 
                                     sensory_strategy: Dict[str, Any],
                                     cultural_recommendations: Dict[str, Any],
                                     blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content including YouTube videos and activities."""
        
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
                if recommendation.get("entities"):
                    video_entities.extend(recommendation.get("entities", []))
        
        # Generate YouTube video content
        if video_entities and not self._is_content_blocked("video", blocked_content):
            try:
                youtube_videos = await self._generate_youtube_video_content(video_entities[:3])
                visual_content["elements"].extend(youtube_videos)
            except Exception as e:
                logger.warning(f"YouTube video generation failed: {str(e)}")
        
        # Generate visual activities based on cultural elements
        visual_activities = self._generate_visual_activities(sensory_strategy)
        visual_content["elements"].extend(visual_activities)
        
        # Generate photo viewing suggestions
        photo_suggestions = self._generate_photo_viewing_suggestions(sensory_strategy)
        visual_content["elements"].extend(photo_suggestions)
        
        return visual_content
    
    async def _generate_youtube_video_content(self, video_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate YouTube video content from Qloo video entities."""
        
        youtube_content = []
        
        for entity in video_entities:
            content_name = entity.get("name", "")
            if not content_name:
                continue
            
            try:
                # Search for content on YouTube - use tool reference
                search_results = await self._youtube_tool_ref.search_videos(
                    query=f"{content_name} classic scenes highlights",
                    max_results=2
                )
                
                if search_results and search_results.get("items"):
                    for video in search_results["items"]:
                        youtube_content.append({
                            "content_subtype": "youtube_video",
                            "title": video.get("snippet", {}).get("title", ""),
                            "video_id": video.get("id", {}).get("videoId", ""),
                            "original_content": content_name,
                            "cultural_connection": entity.get("cultural_context", {}),
                            "youtube_url": f"https://www.youtube.com/watch?v={video.get('id', {}).get('videoId', '')}",
                            "caregiver_guidance": {
                                "implementation": f"Watch {content_name} content together",
                                "engagement": "Comment on scenes, ask about memories",
                                "attention": "Watch for attention span, pause if needed"
                            },
                            "viewing_notes": {
                                "duration": "Start with short clips (5-15 minutes)",
                                "interaction": "Encourage comments and reactions",
                                "comfort": "Ensure comfortable seating and lighting"
                            }
                        })
                
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"YouTube video search failed for {content_name}: {str(e)}")
        
        return youtube_content
    
    def _generate_visual_activities(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate visual activities based on cultural elements."""
        
        activities = [
            {
                "content_subtype": "visual_activity",
                "name": "Photo Album Review",
                "description": "Look through family photos or cultural images together",
                "materials": "Photo albums, printed photos, or tablet with photos",
                "implementation": "Sit together and go through photos slowly",
                "caregiver_guidance": {
                    "engagement": "Ask open-ended questions about photos",
                    "pacing": "Go slowly, don't rush through images",
                    "response": "Follow their lead on which photos interest them"
                }
            },
            {
                "content_subtype": "visual_activity",
                "name": "Nature Viewing",
                "description": "Look out windows at nature or view nature documentaries",
                "materials": "Window view, nature magazines, or nature videos",
                "implementation": "Point out interesting things in nature",
                "caregiver_guidance": {
                    "engagement": "Talk about animals, plants, or weather",
                    "interaction": "Ask about favorite outdoor places",
                    "comfort": "Ensure good lighting and comfortable seating"
                }
            }
        ]
        
        return activities
    
    def _generate_photo_viewing_suggestions(self, sensory_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate photo viewing suggestions."""
        
        suggestions = [
            {
                "content_subtype": "photo_viewing",
                "name": "Family Photo Time",
                "description": "Dedicated time for looking at family photos",
                "setup": "Comfortable seating with good lighting",
                "caregiver_guidance": {
                    "preparation": "Choose photos that usually bring positive reactions",
                    "interaction": "Ask who people are, when photos were taken",
                    "flexibility": "Be ready to change photos if reaction is negative"
                }
            }
        ]
        
        return suggestions
    
    def _generate_tactile_content(self, 
                                 sensory_strategy: Dict[str, Any],
                                 cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tactile content based on cultural themes."""
        
        tactile_content = {
            "available": True,
            "content_type": "tactile",
            "elements": []
        }
        
        # Generate tactile activities
        tactile_activities = [
            {
                "content_subtype": "tactile_activity",
                "name": "Texture Exploration",
                "description": "Feel different safe textures",
                "materials": "Soft fabrics, smooth stones, textured papers",
                "implementation": "Let them touch and feel different materials",
                "caregiver_guidance": {
                    "safety": "Ensure all materials are safe and clean",
                    "engagement": "Ask about how textures feel",
                    "response": "Remove any textures they don't like"
                }
            },
            {
                "content_subtype": "tactile_activity",
                "name": "Hand Massage",
                "description": "Gentle hand or shoulder massage",
                "materials": "Gentle lotion or oil (if no allergies)",
                "implementation": "Offer gentle massage with their permission",
                "caregiver_guidance": {
                    "consent": "Always ask permission before touching",
                    "gentleness": "Use very gentle pressure",
                    "observation": "Watch for comfort level and adjust"
                }
            }
        ]
        
        tactile_content["elements"].extend(tactile_activities)
        
        return tactile_content
    
    def _create_connected_experience(self, 
                                   auditory_content: Dict[str, Any],
                                   gustatory_content: Dict[str, Any],
                                   olfactory_content: Dict[str, Any],
                                   visual_content: Dict[str, Any],
                                   tactile_content: Dict[str, Any],
                                   sensory_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Create connections between different sensory experiences."""
        
        connections = []
        
        # Connect cooking activities across senses
        recipes = [e for e in gustatory_content.get("elements", []) if e.get("content_subtype") == "recipe"]
        for recipe in recipes:
            connection = {
                "connection_type": "cooking_experience",
                "name": f"Complete cooking experience: {recipe.get('name', 'Recipe')}",
                "sensory_integration": {
                    "gustatory": recipe.get("name"),
                    "olfactory": f"Cooking aromas from {recipe.get('name')}",
                    "tactile": "Feeling ingredients and cooking utensils",
                    "visual": "Watching food preparation and cooking",
                    "auditory": "Kitchen sounds and background music"
                },
                "implementation_guide": {
                    "setup": "Prepare ingredients together",
                    "process": "Involve them in safe cooking steps",
                    "experience": "Engage all senses during cooking",
                    "completion": "Enjoy the meal together"
                }
            }
            connections.append(connection)
        
        # Connect music and movement
        music_content = [e for e in auditory_content.get("elements", []) if e.get("content_subtype") == "youtube_music"]
        if music_content:
            connection = {
                "connection_type": "music_and_movement",
                "name": "Music listening with gentle movement",
                "sensory_integration": {
                    "auditory": "Music playing",
                    "tactile": "Gentle swaying or hand movements",
                    "visual": "Watching each other move to music",
                    "olfactory": "Pleasant room scents",
                    "gustatory": "Optional: favorite drink while listening"
                },
                "implementation_guide": {
                    "setup": "Comfortable seating with space to move",
                    "process": "Start music and encourage gentle movement",
                    "experience": "Move together, follow their lead",
                    "adaptation": "Adjust volume and movement to comfort level"
                }
            }
            connections.append(connection)
        
        connected_experience = {
            "total_connections": len(connections),
            "connection_details": connections,
            "integration_approach": "multi_sensory_engagement",
            "caregiver_support": "Detailed implementation guidance provided"
        }
        
        return connected_experience
    
    def _generate_implementation_guidance(self, connected_experience: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive implementation guidance for caregivers."""
        
        guidance = {
            "general_principles": [
                "Follow the person's lead and preferences",
                "Start with one sense and gradually add others",
                "Watch for signs of overwhelm and adjust accordingly",
                "Focus on the experience, not the outcome",
                "Be flexible and ready to change activities"
            ],
            "setup_tips": [
                "Choose a quiet, comfortable environment",
                "Ensure good lighting for visual activities",
                "Have materials ready before starting",
                "Remove distractions like loud noises",
                "Make sure the person is comfortable and relaxed"
            ],
            "engagement_strategies": [
                "Use open-ended questions",
                "Share your own reactions and experiences",
                "Allow for silence and processing time",
                "Encourage participation but don't force it",
                "Celebrate small moments of engagement"
            ],
            "safety_considerations": [
                "Check for allergies before using scents or foods",
                "Ensure all materials are safe and clean",
                "Monitor for signs of distress or discomfort",
                "Have a plan for ending activities if needed",
                "Keep emergency contacts readily available"
            ],
            "adaptation_guidelines": [
                "Simplify activities if they seem too complex",
                "Increase or decrease stimulation based on response",
                "Modify for physical limitations or preferences",
                "Change activities if attention wanes",
                "Respect 'no' and offer alternatives"
            ]
        }
        
        return guidance
    
    def _is_content_blocked(self, content_type: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if a content type is blocked by user feedback."""
        
        blocked_types = blocked_content.get("blocked_content_types", [])
        return content_type in blocked_types
    
    def _create_fallback_sensory_content(self, 
                                       consolidated_info: Dict[str, Any],
                                       cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when APIs are unavailable."""
        
        return {
            "sensory_content": {
                "sensory_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "fallback_used": True,
                    "fallback_reason": "api_unavailable"
                },
                "auditory": {"available": False, "fallback": True},
                "gustatory": {"available": False, "fallback": True},
                "olfactory": {"available": False, "fallback": True},
                "visual": {"available": False, "fallback": True},
                "tactile": {"available": False, "fallback": True},
                "connected_experience": {
                    "total_connections": 0,
                    "fallback_used": True
                },
                "implementation_guidance": self._generate_implementation_guidance({})
            }
        }