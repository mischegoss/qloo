"""
Enhanced Mobile Synthesizer Agent - FIXED DATA UNWRAPPING
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

CRITICAL FIX:
- Added data unwrapping for double-wrapped qloo_intelligence structure
- Agent 3 output was being wrapped in extra layer: {"qloo_intelligence": {...}}
- Now correctly unwraps to access cultural_recommendations data
- Maintains all existing functionality and debugging
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
    Agent 6: Enhanced Mobile Synthesizer with CRITICAL DATA UNWRAPPING FIX
    
    CRITICAL FIX:
    - Unwraps double-wrapped qloo_intelligence data structure
    - Now correctly accesses 19 artists and 5 TV shows from Agent 3
    - Maintains comprehensive debugging and error handling
    - Full 4-card dashboard functionality restored
    """
    
    def __init__(self):
        # Load fallback data for robust operation
        self.fallback_data = self._load_fallback_data()
        logger.info("✅ Mobile Synthesizer initialized with LOCAL MEMORY card support")
    
    def _load_fallback_data(self) -> Dict[str, Any]:
        """Load fallback data for when API calls fail."""
        try:
            fallback_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "fallback_content.json"
)
            
            if os.path.exists(fallback_path):
                with open(fallback_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Fallback file not found at {fallback_path}, using defaults")
                
        except Exception as e:
            logger.warning(f"Error loading fallback data: {e}")
        
        # Default fallback data
        return {
            "music": [{
                "artist": "Frank Sinatra",
                "song": "My Way",
                "youtube_url": "",
                "genre": "Traditional Pop",
                "year": "1969"
            }],
            "tv_shows": [{
                "name": "The Ed Sullivan Show",
                "youtube_url": "",
                "genre": "Variety Show",
                "year": "1948",
                "description": "Classic variety entertainment show"
            }],
            "places": [{
                "name": "Your hometown",
                "description": "A place filled with memories and familiar faces"
            }]
        }
    
    def _unwrap_qloo_intelligence(self, qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        CRITICAL FIX: Unwrap the qloo_intelligence data structure if it's double-wrapped.
        
        Expected structure from Agent 3:
        {
            "success": True,
            "cultural_recommendations": {...}
        }
        
        But we receive:
        {
            "qloo_intelligence": {
                "success": True, 
                "cultural_recommendations": {...}
            }
        }
        """
        
        # Check if we have the double-wrapped structure
        if "qloo_intelligence" in qloo_intelligence and len(qloo_intelligence.keys()) == 1:
            logger.info("🔧 CRITICAL FIX: Unwrapping double-wrapped qloo_intelligence structure")
            unwrapped = qloo_intelligence["qloo_intelligence"]
            logger.info(f"🔧 Unwrapped keys: {list(unwrapped.keys())}")
            return unwrapped
        
        # Return as-is if already properly structured
        logger.info("🔧 Data structure already properly formatted")
        return qloo_intelligence
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhanced synthesis with CRITICAL DATA UNWRAPPING FIX
        """
        
        logger.info("📱 Agent 6: Starting enhanced mobile synthesis with Local Memory card")
        
        # COMPREHENSIVE INPUT DEBUGGING
        logger.info("🔍 DEBUGGING AGENT 6 INPUTS:")
        logger.info(f"🔍 qloo_intelligence keys: {list(qloo_intelligence.keys())}")
        logger.info(f"🔍 qloo_intelligence type: {type(qloo_intelligence)}")
        
        # Test the unwrapping
        unwrapped_data = self._unwrap_qloo_intelligence(qloo_intelligence)
        logger.info(f"🔍 After unwrapping - keys: {list(unwrapped_data.keys())}")
        logger.info(f"🔍 After unwrapping - success: {unwrapped_data.get('success', 'NOT_FOUND')}")
        
        if "cultural_recommendations" in unwrapped_data:
            cultural_recs = unwrapped_data["cultural_recommendations"]
            logger.info(f"🔍 FOUND cultural_recommendations with keys: {list(cultural_recs.keys())}")
            
            for key, value in cultural_recs.items():
                if isinstance(value, dict):
                    logger.info(f"🔍   - {key}: available={value.get('available')}, entity_count={value.get('entity_count')}")
        else:
            logger.warning("🔍 ⚠️ STILL NO cultural_recommendations found after unwrapping!")
        
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
                photo_analysis=photo_analysis,
                current_theme=current_theme,
                location_info=location_info
            )
            
            logger.info("✅ Agent 6: Enhanced mobile synthesis completed successfully")
            return dashboard_result
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            logger.error(f"❌ Exception details: {str(e)}")
            return self._generate_fallback_dashboard(current_theme, location_info)
    
    async def _synthesize_dashboard_content(self,
                                            qloo_intelligence: Dict[str, Any],
                                            sensory_content: Dict[str, Any],
                                            photo_analysis: Dict[str, Any],
                                            current_theme: Dict[str, Any],
                                            location_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize complete dashboard with FIXED data unwrapping
        """
        
        logger.info("🎨 Synthesizing complete 4-card dashboard")
        
        try:
            # Process all content types with FIXED data unwrapping
            logger.info("🔍 Starting content selection with FIXED unwrapping...")
            
            selected_content = {
                "music": self._select_music_content(qloo_intelligence, current_theme),
                "tv_show": self._select_tv_content(qloo_intelligence, current_theme),
                "recipe": self._select_recipe_content(sensory_content, current_theme),
                "local_memory": await self._select_places_content(photo_analysis, current_theme, location_info)
            }
            
            # Get theme information
            theme_name = current_theme.get("name", "Unknown")
            theme_description = current_theme.get("description", "A special theme for today")
            
            # Log selected content for verification
            logger.info("🔍 FINAL SELECTED CONTENT (AFTER FIX):")
            logger.info(f"🎵 Music: {selected_content['music']['artist']} - {selected_content['music']['song']} (source: {selected_content['music']['source']})")
            logger.info(f"📺 TV Show: {selected_content['tv_show']['name']} (source: {selected_content['tv_show']['source']})")
            logger.info(f"🍽️ Recipe: {selected_content['recipe']['name']} (source: {selected_content['recipe']['source']})")
            logger.info(f"📍 Local Memory: {selected_content['local_memory']['title']} (source: {selected_content['local_memory']['source']})")
            
            # Generate conversation starter
            conversation_starter = self._generate_conversation_starter(current_theme, selected_content, location_info)
            
            # Create final dashboard structure
            dashboard_content = {
                "music": selected_content["music"],
                "tv_show": selected_content["tv_show"],
                "recipe": selected_content["recipe"],
                "local_memory": selected_content["local_memory"],
                "conversation_starter": conversation_starter
            }
            
            # Create metadata
            dashboard_metadata = {
                "theme": {
                    "name": theme_name,
                    "description": theme_description,
                    "conversation_prompts": current_theme.get("conversation_prompts", [])
                },
                "content_sources": {
                    "music": selected_content["music"]["source"],
                    "tv_show": selected_content["tv_show"]["source"],
                    "recipe": selected_content["recipe"]["source"],
                    "local_memory": selected_content["local_memory"]["source"]
                },
                "content_quality": self._assess_content_quality(selected_content),
                "fallbacks_used": [k for k, v in selected_content.items() if v.get("source") == "fallback"]
            }
            
            logger.info("✅ Enhanced dashboard synthesized successfully for theme: {}".format(theme_name))
            logger.info(f"🔍 Content quality assessment: {dashboard_metadata['content_quality']}")
            logger.info(f"🔍 Fallbacks used: {dashboard_metadata['fallbacks_used']}")
            
            return {
                "success": True,
                "dashboard_content": dashboard_content,
                "dashboard_metadata": dashboard_metadata,
                "synthesis_approach": "enhanced_local_memory_with_critical_data_unwrapping_fix"
            }
            
        except Exception as e:
            logger.error(f"❌ Dashboard synthesis failed: {e}")
            logger.error(f"❌ Exception details: {str(e)}")
            return self._generate_fallback_dashboard(current_theme, location_info)
    
    def _select_music_content(self, qloo_intelligence: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select music content from Qloo intelligence (FIXED with unwrapping)"""
        logger.info("🎵 Extracting music content from Qloo results")
        
        # CRITICAL FIX: Unwrap the data structure
        unwrapped_data = self._unwrap_qloo_intelligence(qloo_intelligence)
        
        # COMPREHENSIVE DEBUGGING
        logger.info("🔍 MUSIC SELECTION DEBUGGING (AFTER UNWRAPPING):")
        logger.info(f"🔍 Unwrapped data keys: {list(unwrapped_data.keys())}")
        logger.info(f"🔍 Unwrapped data success: {unwrapped_data.get('success', 'NOT_FOUND')}")
        
        cultural_recommendations = unwrapped_data.get("cultural_recommendations", {})
        logger.info(f"🔍 cultural_recommendations keys: {list(cultural_recommendations.keys())}")
        
        try:
            artists_data = cultural_recommendations.get("artists", {})
            logger.info(f"🔍 artists_data type: {type(artists_data)}")
            logger.info(f"🔍 artists_data available: {artists_data.get('available', 'NOT_FOUND')}")
            logger.info(f"🔍 artists_data entity_count: {artists_data.get('entity_count', 'NOT_FOUND')}")
            
            entities = artists_data.get("entities", [])
            logger.info(f"🔍 Found {len(entities)} artists in Qloo results")
            
            if entities and len(entities) > 0:
                selected_artist = entities[0]
                artist_name = selected_artist.get("name", "Unknown Artist")
                logger.info(f"✅ FIXED - Selected artist from Qloo: {artist_name}")
                
                # Create a representative song title
                song_title = "Greatest Hits"
                if selected_artist.get("music_genre") == "classical":
                    song_title = "Timeless Classics"
                elif selected_artist.get("music_genre") == "jazz":
                    song_title = "Jazz Standards"
                
                return {
                    "artist": artist_name,
                    "song": song_title,
                    "youtube_url": "",
                    "year": selected_artist.get("properties", {}).get("year"),
                    "genre": selected_artist.get("music_genre", selected_artist.get("properties", {}).get("genre")),
                    "source": "qloo_intelligence"
                }
            else:
                logger.warning(f"⚠️ No artists found in entities list (length: {len(entities)})")
                    
        except Exception as e:
            logger.error(f"❌ Error selecting music content: {e}")
        
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
        """Select TV content from Qloo intelligence (FIXED with unwrapping)"""
        logger.info("📺 Extracting TV content from Qloo results")
        
        # CRITICAL FIX: Unwrap the data structure
        unwrapped_data = self._unwrap_qloo_intelligence(qloo_intelligence)
        
        logger.info("🔍 TV SELECTION DEBUGGING (AFTER UNWRAPPING):")
        
        try:
            cultural_recommendations = unwrapped_data.get("cultural_recommendations", {})
            logger.info(f"🔍 Cultural recommendations keys: {list(cultural_recommendations.keys())}")
            
            tv_shows_data = cultural_recommendations.get("tv_shows", {})
            logger.info(f"🔍 TV shows data available: {tv_shows_data.get('available', 'NOT_FOUND')}")
            logger.info(f"🔍 TV shows entity_count: {tv_shows_data.get('entity_count', 'NOT_FOUND')}")
            
            tv_shows = tv_shows_data.get("entities", [])
            logger.info(f"🔍 Found {len(tv_shows)} TV shows")
            
            if tv_shows and len(tv_shows) > 0:
                selected_show = tv_shows[0]
                show_name = selected_show.get("name", "Classic Television")
                logger.info(f"✅ FIXED - Selected TV show from Qloo: {show_name}")
                
                return {
                    "name": show_name,
                    "youtube_url": selected_show.get("embeddable_url", ""),
                    "genre": selected_show.get("properties", {}).get("genre"),
                    "year": selected_show.get("properties", {}).get("year"),
                    "description": selected_show.get("properties", {}).get("description"),
                    "source": "qloo_intelligence"
                }
            else:
                logger.warning(f"⚠️ No TV shows found in entities list (length: {len(tv_shows)})")
                
        except Exception as e:
            logger.error(f"❌ Error selecting TV content: {e}")
        
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
                recipe_element = gustatory_content["elements"][0]
                logger.info(f"✅ Found recipe via gustatory elements: {recipe_element.get('name', 'Unknown')}")
                
                return {
                    "name": recipe_element.get("name", "Comfort Recipe"),
                    "ingredients": recipe_element.get("ingredients", []),
                    "instructions": recipe_element.get("instructions", []),
                    "prep_time": recipe_element.get("prep_time", "30 minutes"),
                    "difficulty": recipe_element.get("difficulty", "Easy"),
                    "cultural_context": recipe_element.get("cultural_context", ""),
                    "source": "sensory_elements"
                }
                
        except Exception as e:
            logger.warning(f"Error selecting recipe content: {e}")
        
        # Fallback
        logger.info("🔄 Using fallback recipe content")
        return {
            "name": "Warm Apple Slices",
            "ingredients": ["2 apples", "1 tsp cinnamon", "1 tbsp butter"],
            "instructions": ["Slice apples", "Heat butter in pan", "Add apples and cinnamon", "Cook until tender"],
            "prep_time": "10 minutes",
            "difficulty": "Easy",
            "cultural_context": "A simple, comforting treat that brings back memories",
            "source": "fallback"
        }
    
    async def _select_places_content(self, photo_analysis: Dict[str, Any], current_theme: Dict[str, Any], location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Select place content for Local Memory card (unchanged)"""
        logger.info("📍 Selecting place content for Local Memory card")
        
        try:
            # Try to use photo analysis first
            if photo_analysis.get("success") and photo_analysis.get("places_analysis"):
                places_data = photo_analysis["places_analysis"]
                if places_data.get("local_spots") and len(places_data["local_spots"]) > 0:
                    selected_place = places_data["local_spots"][0]
                    logger.info(f"✅ Selected place from photo analysis: {selected_place.get('name', 'Local spot')}")
                    
                    return {
                        "title": f"Remember: {selected_place.get('name', 'This special place')}",
                        "description": selected_place.get("description", "A meaningful place with memories"),
                        "conversation_starters": selected_place.get("conversation_starters", [
                            "Tell me about times you visited places like this",
                            "What does this place remind you of?"
                        ]),
                        "source": "photo_analysis"
                    }
            
            # Fallback to hometown memory
            primary_location = location_info.get("primary_location", "your hometown")
            location_type = location_info.get("location_type", "legacy_location")
            
            logger.info(f"🏡 Creating hometown memory card for: {primary_location}")
            
            # Create themed conversation starters based on current theme
            theme_name = current_theme.get("name", "").lower()
            if "family" in theme_name:
                conversation_starters = [
                    f"Tell me about your family life in {primary_location}",
                    "What family traditions did you have growing up?",
                    "Who were your neighbors when you lived there?"
                ]
            elif "memory" in theme_name or "lane" in theme_name:
                conversation_starters = [
                    f"What do you remember most about {primary_location}?",
                    "Tell me about the best times you had there",
                    "What made that place special to you?"
                ]
            else:
                conversation_starters = [
                    f"Tell me about life in {primary_location}",
                    "What was your favorite spot there?",
                    "What do you miss most about that time?"
                ]
            
            return {
                "title": f"Your {location_type.replace('_', ' ')}: {primary_location}",
                "description": f"Memories and moments from {primary_location}",
                "conversation_starters": conversation_starters,
                "source": "hometown_memory"
            }
            
        except Exception as e:
            logger.warning(f"Error selecting places content: {e}")
            
            # Final fallback
            return {
                "title": "A Special Place",
                "description": "Every place holds memories and stories",
                "conversation_starters": [
                    "Tell me about a place that was special to you",
                    "What made that place memorable?",
                    "Who did you share that place with?"
                ],
                "source": "fallback"
            }
    
    def _generate_conversation_starter(self, current_theme: Dict[str, Any], selected_content: Dict[str, Any], location_info: Dict[str, Any]) -> str:
        """Generate a theme-appropriate conversation starter."""
        
        theme_name = current_theme.get("name", "").lower()
        
        # Theme-based conversation starters
        if "family" in theme_name:
            starters = [
                "Tell me about a favorite family memory",
                "What family traditions were most important to you?",
                "Who in your family made you laugh the most?"
            ]
        elif "memory" in theme_name or "lane" in theme_name:
            starters = [
                "Tell me about something that always makes you smile",
                "What's a memory you love to think about?",
                "Share a story from the good old days"
            ]
        elif "music" in theme_name or selected_content.get("music", {}).get("source") == "qloo_intelligence":
            artist = selected_content.get("music", {}).get("artist", "music")
            starters = [
                f"Did you ever listen to {artist}?",
                "What music did you love when you were young?",
                "Tell me about a song that brings back memories"
            ]
        else:
            # General conversation starters
            starters = [
                "What's something that made today special?",
                "Tell me about something you enjoyed doing",
                "What's a happy memory you'd like to share?"
            ]
        
        return random.choice(starters)
    
    def _assess_content_quality(self, selected_content: Dict[str, Any]) -> str:
        """Assess overall content quality based on sources."""
        
        sources = [content.get("source", "unknown") for content in selected_content.values()]
        fallback_count = sources.count("fallback")
        
        if fallback_count == 0:
            return "high"
        elif fallback_count <= 2:
            return "mixed"
        else:
            return "low"
    
    def _generate_fallback_dashboard(self, current_theme: Dict[str, Any], location_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete fallback dashboard when synthesis fails."""
        
        logger.info("🔄 Generating complete fallback dashboard")
        
        fallback_content = {
            "music": {
                "artist": "Frank Sinatra",
                "song": "My Way", 
                "youtube_url": "",
                "genre": "Traditional Pop",
                "year": "1969",
                "source": "fallback"
            },
            "tv_show": {
                "name": "The Ed Sullivan Show",
                "youtube_url": "",
                "genre": "Variety Show", 
                "year": "1948",
                "description": "Classic variety entertainment show",
                "source": "fallback"
            },
            "recipe": {
                "name": "Warm Apple Slices",
                "ingredients": ["2 apples", "1 tsp cinnamon", "1 tbsp butter"],
                "instructions": ["Slice apples", "Heat butter in pan", "Add apples and cinnamon", "Cook until tender"],
                "prep_time": "10 minutes",
                "difficulty": "Easy",
                "cultural_context": "A simple, comforting treat",
                "source": "fallback"
            },
            "local_memory": {
                "title": "Your hometown",
                "description": "A place filled with memories and familiar faces",
                "conversation_starters": [
                    "Tell me about your hometown",
                    "What do you remember most about growing up?",
                    "Who were the special people in your life?"
                ],
                "source": "fallback"
            },
            "conversation_starter": "Tell me about something that always makes you smile"
        }
        
        dashboard_metadata = {
            "theme": {
                "name": current_theme.get("name", "Memory Lane"),
                "description": current_theme.get("description", "A time for remembering"),
                "conversation_prompts": []
            },
            "content_sources": {
                "music": "fallback", 
                "tv_show": "fallback",
                "recipe": "fallback",
                "local_memory": "fallback"
            },
            "content_quality": "low",
            "fallbacks_used": ["music", "tv_show", "recipe", "local_memory"]
        }
        
        return {
            "success": True,
            "dashboard_content": fallback_content,
            "dashboard_metadata": dashboard_metadata,
            "synthesis_approach": "complete_fallback"
        }

# Export the main class
__all__ = ["MobileSynthesizerAgent"]