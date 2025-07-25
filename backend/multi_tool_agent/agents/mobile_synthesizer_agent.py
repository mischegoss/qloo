"""
Enhanced Mobile Synthesizer Agent - Local Memory Card Added
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

ENHANCED: Now includes Local Memory card with Places + Vision Analysis
- Processes place photo analysis from Agent 5
- Creates theme-aware conversation starters about local places
- Handles rural area fallbacks gracefully
- Maintains all existing functionality (Music, TV, Recipe)
- Clean 4-card dashboard: Music | TV | Recipe | Local Memory
"""

import logging
import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class MobileSynthesizerAgent:
    """
    Agent 6: Enhanced Mobile Synthesizer with Local Memory Card
    
    ENHANCED FUNCTIONALITY:
    - Processes place photo analysis from Agent 5
    - Creates Local Memory card with theme-aware conversation starters
    - Handles rural area fallbacks with hometown conversations
    - Maintains existing music, TV, and recipe card functionality
    - Clean 4-card dashboard layout
    """
    
    def __init__(self):
        # Load fallback data for robust operation
        self.fallback_data = self._load_fallback_data()
        logger.info("✅ Mobile Synthesizer initialized with LOCAL MEMORY card support")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced synthesis with Local Memory card
        
        Args:
            consolidated_info: Patient info and daily theme
            cultural_profile: Cultural profile data
            qloo_intelligence: Qloo API results
            sensory_content: Music, TV, recipe content
            photo_analysis: NEW - Place photo analysis from Agent 5
            
        Returns:
            Complete dashboard with 4 cards including Local Memory
        """
        
        logger.info("📱 Agent 6: Starting enhanced mobile synthesis with Local Memory card")
        
        try:
            # Extract theme and location information
            current_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
            location_info = consolidated_info.get("location_info", {})
            
            logger.info(f"🎯 Synthesizing for theme: {current_theme.get('name', 'Unknown')}")
            logger.info(f"🏠 Location context: {location_info.get('primary_location', 'Unknown')}")
            
            # Synthesize dashboard content with all 4 cards
            dashboard_result = await self._synthesize_dashboard_content(
                qloo_intelligence=qloo_intelligence,
                sensory_content=sensory_content,
                photo_analysis=photo_analysis,  # NEW - Place analysis
                current_theme=current_theme,
                location_info=location_info
            )
            
            logger.info("✅ Agent 6: Enhanced mobile synthesis completed successfully")
            return dashboard_result
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            return self._generate_fallback_dashboard(current_theme, location_info)
    
    async def _synthesize_dashboard_content(self,
                                            qloo_intelligence: Dict[str, Any],
                                            sensory_content: Dict[str, Any],
                                            photo_analysis: Dict[str, Any],
                                            current_theme: Dict[str, Any],
                                            location_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize complete dashboard with all 4 cards including Local Memory
        """
        
        logger.info("🎨 Synthesizing complete 4-card dashboard")
        
        try:
            # Process all content types
            selected_content = {
                "music": self._select_music_content(sensory_content, current_theme),
                "tv_show": self._select_tv_content(qloo_intelligence, current_theme),
                "recipe": self._select_recipe_content(sensory_content, current_theme),
                "local_memory": await self._select_places_content(photo_analysis, current_theme, location_info)  # NEW
            }
            
            # Get theme information
            theme_name = current_theme.get("name", "Memory Lane")
            theme_description = current_theme.get("description", "Exploring memories and experiences")
            
            # Build complete dashboard structure
            dashboard_result = {
                "success": True,
                "dashboard_type": "enhanced_with_local_memory",
                "theme": {
                    "name": theme_name,
                    "description": theme_description,
                    "id": current_theme.get("id", "general")
                },
                "cards": {
                    "music": {
                        "title": "🎵 Music",
                        "type": "music",
                        "content": selected_content["music"],
                        "interaction_type": "audio_playback"
                    },
                    "tv_show": {
                        "title": "📺 TV Show",
                        "type": "tv_show", 
                        "content": selected_content["tv_show"],
                        "interaction_type": "video_content"
                    },
                    "recipe": {
                        "title": "🍽️ Recipe",
                        "type": "recipe",
                        "content": selected_content["recipe"],
                        "interaction_type": "cooking_activity"
                    },
                    "local_memory": {  # NEW CARD
                        "title": "📍 Local Memory",
                        "type": "local_memory",
                        "content": selected_content["local_memory"],
                        "interaction_type": "conversation_starter"
                    }
                },
                "metadata": {
                    "generation_timestamp": datetime.now().isoformat(),
                    "theme_applied": theme_name,
                    "cards_generated": 4,
                    "local_memory_enabled": True,
                    "synthesis_agent": "mobile_synthesizer_enhanced"
                }
            }
            
            logger.info(f"✅ Enhanced dashboard synthesized successfully for theme: {theme_name}")
            logger.info(f"🎵 Music: {selected_content['music'].get('artist', 'Unknown')} - {selected_content['music'].get('song', 'Unknown')}")
            logger.info(f"📺 TV Show: {selected_content['tv_show'].get('name', 'Unknown')}")
            logger.info(f"🍽️ Recipe: {selected_content['recipe'].get('name', 'Unknown')}")
            logger.info(f"📍 Local Memory: {selected_content['local_memory'].get('place_name', 'Unknown')}")
            
            return dashboard_result
            
        except Exception as e:
            logger.error(f"❌ Error synthesizing enhanced dashboard content: {e}")
            return self._generate_fallback_dashboard(current_theme, location_info)
    
    async def _select_places_content(self, photo_analysis: Dict[str, Any], 
                                     current_theme: Dict[str, Any],
                                     location_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        NEW: Select and process place content for Local Memory card
        
        Args:
            photo_analysis: Place photo analysis from Agent 5
            current_theme: Current daily theme
            location_info: Location information from Agent 1
            
        Returns:
            Local Memory card content
        """
        
        logger.info("📍 Selecting place content for Local Memory card")
        
        # Get place analysis data
        place_analysis = photo_analysis.get("place_photo_analysis", {})
        
        if place_analysis.get("available") and not place_analysis.get("rural_fallback"):
            # SUCCESS CASE: Place found and analyzed
            return self._create_place_memory_card(place_analysis, current_theme, location_info)
        else:
            # FALLBACK CASE: Rural area or no places found
            return self._create_hometown_memory_card(place_analysis, current_theme, location_info)
    
    def _create_place_memory_card(self, place_analysis: Dict[str, Any],
                                  current_theme: Dict[str, Any],
                                  location_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Local Memory card from successful place analysis
        """
        
        place_data = place_analysis.get("place_data", {})
        vision_analysis = place_analysis.get("vision_analysis", {})
        theme_relevance = place_analysis.get("theme_relevance", {})
        
        place_name = place_data.get("name", "Local Place")
        photo_url = place_analysis.get("photo_url", "")
        
        logger.info(f"🏢 Creating place memory card for: {place_name}")
        
        # Create theme-aware conversation starter
        conversation_starter = self._create_place_conversation_starter(
            place_data, vision_analysis, theme_relevance, location_info
        )
        
        # Create context information
        context_info = self._create_place_context(place_data, vision_analysis)
        
        return {
            "place_name": place_name,
            "photo_url": photo_url,
            "conversation_starter": conversation_starter,
            "context_info": context_info,
            "location_type": location_info.get("location_type", "location"),
            "primary_location": location_info.get("primary_location", "your area"),
            "theme_connection": theme_relevance.get("relevance_explanation", ""),
            "visual_details": {
                "architectural_features": vision_analysis.get("architectural_details", ""),
                "atmosphere": vision_analysis.get("atmosphere_description", ""),
                "key_elements": [label.get("description", "") for label in vision_analysis.get("labels", [])[:3]]
            },
            "source": "qloo_place_analysis",
            "interaction_suggestions": [
                "Ask about similar places they remember",
                "Discuss the neighborhood in their youth",
                f"Talk about {current_theme.get('name', 'activities')} in this area"
            ]
        }
    
    def _create_hometown_memory_card(self, place_analysis: Dict[str, Any],
                                     current_theme: Dict[str, Any],
                                     location_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create Local Memory card for rural areas or when no places found
        """
        
        primary_location = location_info.get("primary_location", "your hometown")
        location_type = location_info.get("location_type", "hometown")
        
        logger.info(f"🏡 Creating hometown memory card for: {primary_location}")
        
        # Create rural/hometown conversation starter
        conversation_starter = self._create_hometown_conversation_starter(
            current_theme, location_info
        )
        
        # Create context for smaller communities
        context_info = self._create_hometown_context(location_info, current_theme)
        
        return {
            "place_name": f"Your {location_type}: {primary_location}",
            "photo_url": "",  # No specific place photo
            "conversation_starter": conversation_starter,
            "context_info": context_info,
            "location_type": location_type,
            "primary_location": primary_location,
            "theme_connection": f"Exploring {current_theme.get('name', 'memories')} from your community",
            "rural_context": {
                "community_focus": True,
                "rural_themes": self._get_rural_themes(current_theme),
                "hometown_emphasis": location_type == "hometown"
            },
            "source": "hometown_conversation",
            "interaction_suggestions": [
                f"Share memories about {current_theme.get('name', 'life')} in {primary_location}",
                "Describe the community atmosphere",
                "Talk about local traditions and gatherings"
            ]
        }
    
    def _create_place_conversation_starter(self, place_data: Dict[str, Any],
                                           vision_analysis: Dict[str, Any],
                                           theme_relevance: Dict[str, Any],
                                           location_info: Dict[str, Any]) -> str:
        """
        Create theme-aware conversation starter using place and vision analysis
        """
        
        place_name = place_data.get("name", "this place")
        location_type = location_info.get("location_type", "area")
        primary_location = location_info.get("primary_location", "your neighborhood")
        
        # Get visual context
        architectural_details = vision_analysis.get("architectural_details", "")
        atmosphere_description = vision_analysis.get("atmosphere_description", "")
        
        # Build conversation starter with theme integration
        theme_id = theme_relevance.get("theme_id", "general")
        
        conversation_templates = {
            "school": f"I found {place_name} in your {location_type}. {architectural_details} {atmosphere_description} Did you ever visit buildings like this during your school days? What do you remember about the schools or libraries in {primary_location}?",
            
            "birthday": f"Here's {place_name} from your {location_type}. {atmosphere_description} {architectural_details} Did your family ever celebrate special occasions like birthdays at places like this? How did people in {primary_location} celebrate special days?",
            
            "music": f"I found {place_name} in your {location_type}. {architectural_details} {atmosphere_description} Did you ever attend music performances or cultural events at venues like this? What kind of music did people enjoy in {primary_location}?",
            
            "food": f"Here's {place_name} from your {location_type}. {atmosphere_description} Did you ever dine at places like this? What were the popular restaurants or food spots in {primary_location} when you were younger?",
            
            "travel": f"I found {place_name}, a notable place in your {location_type}. {architectural_details} {atmosphere_description} Did you ever visit landmarks like this on special trips? What places did people from {primary_location} like to visit?",
            
            "weather": f"Here's {place_name} in your {location_type}. {atmosphere_description} Did you enjoy spending time at outdoor places like this in different seasons? How did the weather affect community activities in {primary_location}?",
            
            "holidays": f"I found {place_name} in your {location_type}. {architectural_details} {atmosphere_description} Did your community gather at places like this for holidays and celebrations? What holiday traditions were special in {primary_location}?",
            
            "pets": f"Here's {place_name} from your {location_type}. {atmosphere_description} Did families with pets enjoy spending time at community places like this? What outdoor spaces did people and their pets enjoy in {primary_location}?"
        }
        
        # Get theme-specific conversation or use general template
        conversation = conversation_templates.get(
            theme_id,
            f"I found {place_name} in your {location_type}. {architectural_details} {atmosphere_description} This place represents an important part of your community's heritage. What memories do you have of places like this in {primary_location}?"
        )
        
        return conversation.strip()
    
    def _create_hometown_conversation_starter(self, current_theme: Dict[str, Any],
                                              location_info: Dict[str, Any]) -> str:
        """
        Create conversation starter for rural areas/hometown focus
        """
        
        theme_id = current_theme.get("id", "general")
        theme_name = current_theme.get("name", "memories")
        primary_location = location_info.get("primary_location", "your hometown")
        location_type = location_info.get("location_type", "hometown")
        
        # Rural/hometown conversation templates
        hometown_templates = {
            "school": f"Tell me about going to school in {primary_location}. Did you walk to school? What was the schoolhouse or school building like? How did children in your community get to school?",
            
            "birthday": f"How did families celebrate birthdays in {primary_location}? What made birthdays special in your community? Did neighbors join in celebrations?",
            
            "music": f"What kind of music did people listen to in {primary_location}? Were there local musicians or community gatherings with music? Did families have musical traditions?",
            
            "food": f"What foods were popular in {primary_location} when you were growing up? Did your community have special local dishes or food traditions? What did families cook for special occasions?",
            
            "travel": f"Where did people from {primary_location} like to go for special trips or outings? What were considered the 'big' destinations from your community? How did families travel in those days?",
            
            "weather": f"How did different seasons affect life in {primary_location}? What did people do during harsh weather? How did your community adapt to seasonal changes?",
            
            "holidays": f"What holiday traditions were special in {primary_location}? How did your community celebrate together? What made holidays memorable in your {location_type}?",
            
            "pets": f"Tell me about pets and animals in {primary_location}. Did most families have pets? What role did animals play in your community life?"
        }
        
        # Get theme-specific hometown conversation
        conversation = hometown_templates.get(
            theme_id,
            f"Tell me about {theme_name.lower()} in {primary_location}. What was special about your {location_type}? How did the community experience {theme_name.lower()} together?"
        )
        
        return conversation
    
    def _create_place_context(self, place_data: Dict[str, Any],
                              vision_analysis: Dict[str, Any]) -> str:
        """Create rich context information for places"""
        
        description = place_data.get("description", "")
        address = place_data.get("address", "")
        neighborhood = place_data.get("neighborhood", "")
        
        # Combine available context
        context_parts = []
        
        if description:
            context_parts.append(description)
        
        if neighborhood:
            context_parts.append(f"Located in the {neighborhood} area")
            
        if address:
            context_parts.append(f"Address: {address}")
        
        return " • ".join(context_parts) if context_parts else "A notable place in your community with historical significance."
    
    def _create_hometown_context(self, location_info: Dict[str, Any],
                                 current_theme: Dict[str, Any]) -> str:
        """Create context information for hometown/rural areas"""
        
        primary_location = location_info.get("primary_location", "your area")
        location_type = location_info.get("location_type", "location")
        rural_indicators = location_info.get("rural_indicators", {})
        
        if rural_indicators.get("likely_rural"):
            return f"Focusing on {current_theme.get('name', 'memories')} from your {location_type} in {primary_location}. Small communities often have unique traditions and close-knit experiences that create lasting memories."
        else:
            return f"Exploring {current_theme.get('name', 'memories')} from your time in {primary_location}. Every community has its own character and special places that hold meaningful memories."
    
    def _get_rural_themes(self, current_theme: Dict[str, Any]) -> List[str]:
        """Get rural-appropriate themes for hometown conversations"""
        
        theme_id = current_theme.get("id", "general")
        
        rural_theme_suggestions = {
            "school": ["one-room schoolhouse", "walking to school", "school community events"],
            "birthday": ["family celebrations", "neighbor gatherings", "homemade traditions"],  
            "music": ["local musicians", "community singing", "radio programs"],
            "food": ["home cooking", "local ingredients", "community meals"],
            "travel": ["trips to town", "visiting relatives", "county fair"],
            "weather": ["seasonal work", "weather preparations", "community cooperation"],
            "holidays": ["church gatherings", "community celebrations", "family traditions"],
            "pets": ["farm animals", "working dogs", "outdoor cats"]
        }
        
        return rural_theme_suggestions.get(theme_id, ["community life", "family traditions", "simple pleasures"])
    
    # ===== EXISTING METHODS (UNCHANGED) =====
    
    def _select_music_content(self, audio_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select music content from sensory content results (unchanged)"""
        logger.info("🎵 Extracting music content from sensory results")
        
        try:
            # Extract from sensory content structure
            content_by_sense = audio_content.get("sensory_content", {}).get("content_by_sense", {})
            auditory_content = content_by_sense.get("auditory", {})
            
            # Try primary song first
            if auditory_content.get("primary_song"):
                primary_song = auditory_content["primary_song"]
                logger.info(f"✅ Found primary song: {primary_song.get('artist', 'Unknown')} - {primary_song.get('song', 'Unknown')}")
                
                return {
                    "artist": primary_song.get("artist", "Unknown Artist"),
                    "song": primary_song.get("song", primary_song.get("title", "Unknown Song")),
                    "youtube_url": primary_song.get("youtube_url", ""),
                    "year": primary_song.get("year"),
                    "genre": primary_song.get("genre"),
                    "source": "sensory_primary"
                }
            
            # Fallback to auditory elements
            elif auditory_content.get("elements") and len(auditory_content["elements"]) > 0:
                first_song = auditory_content["elements"][0]
                logger.info(f"✅ Found song via auditory elements: {first_song.get('artist', 'Unknown')}")
                
                return {
                    "artist": first_song.get("artist", "Unknown Artist"),
                    "song": first_song.get("song", first_song.get("title", "Unknown Song")),
                    "youtube_url": first_song.get("youtube_url", ""),
                    "year": first_song.get("year"),
                    "genre": first_song.get("genre"),
                    "source": "sensory_elements"
                }
        
        except Exception as e:
            logger.warning(f"Error selecting music content: {e}")
        
        # Fallback
        logger.info("🔄 Using fallback music content")
        fallback_music = self.fallback_data.get("music", [{}])[0]
        return {
            "artist": fallback_music.get("artist", "Classic Artist"),
            "song": fallback_music.get("song", "Timeless Song"),
            "youtube_url": fallback_music.get("youtube_url", ""),
            "genre": fallback_music.get("genre"),
            "year": fallback_music.get("year"),
            "source": "fallback"
        }
    
    def _select_tv_content(self, qloo_intelligence: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select TV content from Qloo intelligence (unchanged)"""
        logger.info("📺 Extracting TV content from Qloo results")
        
        try:
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            tv_shows_data = cultural_recommendations.get("tv_shows", {})
            tv_shows = tv_shows_data.get("entities", []) if isinstance(tv_shows_data, dict) else []
            
            if tv_shows and len(tv_shows) > 0:
                selected_show = tv_shows[0]
                show_name = selected_show.get("name", "Classic Television")
                logger.info(f"✅ Selected TV show from Qloo: {show_name}")
                
                return {
                    "name": show_name,
                    "youtube_url": selected_show.get("embeddable_url", ""),
                    "genre": selected_show.get("properties", {}).get("genre"),
                    "year": selected_show.get("properties", {}).get("year"),
                    "description": selected_show.get("properties", {}).get("description"),
                    "source": "qloo_intelligence"
                }
        except Exception as e:
            logger.warning(f"Error selecting TV content from Qloo: {e}")
        
        # Fallback
        logger.info("🔄 Using fallback TV content")
        fallback_tv = self.fallback_data.get("tv_shows", [{}])[0]
        return {
            "name": fallback_tv.get("name", "Classic Television"),
            "youtube_url": fallback_tv.get("youtube_url", ""),
            "genre": fallback_tv.get("genre"),
            "year": fallback_tv.get("year"),
            "description": fallback_tv.get("description"),
            "source": "fallback"
        }
    
    def _select_recipe_content(self, sensory_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select recipe content from sensory content (unchanged)"""
        logger.info("🍽️ Extracting recipe content from sensory results")
        
        try:
            content_by_sense = sensory_content.get("sensory_content", {}).get("content_by_sense", {})
            gustatory_content = content_by_sense.get("gustatory", {})
            
            # Try primary recipe first
            if gustatory_content.get("primary_recipe"):
                recipe_data = gustatory_content["primary_recipe"]
                logger.info(f"✅ Found primary recipe: {recipe_data.get('name', 'Unknown')}")
                
                return {
                    "name": recipe_data.get("name", "Comfort Recipe"),
                    "ingredients": recipe_data.get("ingredients", []),
                    "instructions": recipe_data.get("instructions", []),
                    "prep_time": recipe_data.get("prep_time", "30 minutes"),
                    "difficulty": recipe_data.get("difficulty", "Easy"),
                    "cultural_context": recipe_data.get("cultural_context", ""),
                    "source": "sensory_primary"
                }
            
            # Fallback to gustatory elements
            elif gustatory_content.get("elements") and len(gustatory_content["elements"]) > 0:
                recipe_data = gustatory_content["elements"][0]
                logger.info(f"✅ Found recipe via gustatory elements: {recipe_data.get('name', 'Unknown')}")
                
                return {
                    "name": recipe_data.get("name", "Comfort Recipe"),
                    "ingredients": recipe_data.get("ingredients", []),
                    "instructions": recipe_data.get("instructions", []),
                    "prep_time": recipe_data.get("prep_time", "30 minutes"),
                    "difficulty": recipe_data.get("difficulty", "Easy"),
                    "cultural_context": recipe_data.get("cultural_context", ""),
                    "source": "sensory_elements"
                }
        
        except Exception as e:
            logger.warning(f"Error selecting recipe content: {e}")
        
        # Fallback
        logger.info("🔄 Using fallback recipe content")
        fallback_recipe = self.fallback_data.get("recipes", [{}])[0]
        return {
            "name": fallback_recipe.get("name", "Comfort Food Recipe"),
            "ingredients": fallback_recipe.get("ingredients", ["Simple ingredients"]),
            "instructions": fallback_recipe.get("instructions", ["Follow traditional methods"]),
            "prep_time": fallback_recipe.get("prep_time", "30 minutes"),
            "difficulty": fallback_recipe.get("difficulty", "Easy"),
            "cultural_context": fallback_recipe.get("cultural_context", "A traditional comfort food"),
            "source": "fallback"
        }
    
    def _load_fallback_data(self) -> Dict[str, Any]:
        """Load fallback data for robust operation (unchanged)"""
        return {
            "music": [
                {
                    "artist": "Frank Sinatra",
                    "song": "My Way",
                    "genre": "Traditional Pop",
                    "year": 1969,
                    "youtube_url": ""
                }
            ],
            "tv_shows": [
                {
                    "name": "The Ed Sullivan Show",
                    "genre": "Variety",
                    "year": 1960,
                    "description": "Classic variety show featuring music and entertainment",
                    "youtube_url": ""
                }
            ],
            "recipes": [
                {
                    "name": "Sunday Gravy",
                    "ingredients": ["Tomatoes", "Garlic", "Olive oil", "Herbs"],
                    "instructions": ["Simmer ingredients slowly", "Season to taste"],
                    "prep_time": "2 hours",
                    "difficulty": "Medium",
                    "cultural_context": "Traditional Italian-American family recipe"
                }
            ]
        }
    
    def _generate_fallback_dashboard(self, current_theme: Dict[str, Any], 
                                     location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback dashboard when main synthesis fails"""
        
        logger.warning("⚠️ Generating fallback dashboard")
        
        theme_name = current_theme.get("name", "Memory Lane")
        primary_location = location_info.get("primary_location", "your area")
        
        return {
            "success": True,
            "dashboard_type": "fallback_with_local_memory",
            "theme": {
                "name": theme_name,
                "description": "Exploring memories and experiences",
                "id": current_theme.get("id", "general")
            },
            "cards": {
                "music": {
                    "title": "🎵 Music",
                    "type": "music",
                    "content": self.fallback_data["music"][0],
                    "interaction_type": "audio_playback"
                },
                "tv_show": {
                    "title": "📺 TV Show",
                    "type": "tv_show",
                    "content": self.fallback_data["tv_shows"][0],
                    "interaction_type": "video_content"
                },
                "recipe": {
                    "title": "🍽️ Recipe",
                    "type": "recipe",
                    "content": self.fallback_data["recipes"][0],
                    "interaction_type": "cooking_activity"
                },
                "local_memory": {
                    "title": "📍 Local Memory",
                    "type": "local_memory",
                    "content": {
                        "place_name": f"Your Community: {primary_location}",
                        "photo_url": "",
                        "conversation_starter": f"Tell me about growing up in {primary_location}. What made your community special?",
                        "context_info": "Every community has its own unique character and memories.",
                        "source": "fallback_hometown"
                    },
                    "interaction_type": "conversation_starter"
                }
            },
            "metadata": {
                "generation_timestamp": datetime.now().isoformat(),
                "theme_applied": theme_name,
                "cards_generated": 4,
                "fallback_used": True,
                "local_memory_enabled": True
            }
        }

# Export the main class
__all__ = ["MobileSynthesizerAgent"]