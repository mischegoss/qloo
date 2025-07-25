"""
Mobile Synthesizer Agent - FIXED: Correct Qloo Data Structure Extraction
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

CRITICAL FIX:
- Updated data extraction paths to match improved Qloo tools structure
- Fixed: artists = cultural_recommendations.get("artists", {}).get("entities", [])
- Fixed: tv_shows = cultural_recommendations.get("tv_shows", {}).get("entities", [])
- Now correctly extracts from nested "entities" arrays instead of expecting flat lists
"""

import logging
import json
import os
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger FIRST
logger = logging.getLogger(__name__)

# Import theme manager for theme-aware functionality
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Mobile Synthesizer: theme_manager imported successfully")
except ImportError as e:
    logger.error(f"❌ Mobile Synthesizer: Failed to import theme_manager: {e}")
    theme_manager = None
except Exception as e:
    logger.error(f"❌ Mobile Synthesizer: Error with theme_manager: {e}")
    theme_manager = None

class MobileSynthesizerAgent:
    """
    Agent 6: Mobile Synthesizer with FIXED Qloo Data Structure Extraction
    
    CRITICAL FIX:
    - Corrected data extraction paths for improved Qloo tools structure
    - Now properly finds artists and TV shows from nested "entities" arrays
    - Should eliminate fallback to hardcoded content when Qloo data is available
    """
    
    def __init__(self):
        self.fallback_data = self._load_fallback_content()
        logger.info("Mobile Synthesizer initialized with FIXED Qloo data structure extraction")
    
    async def run(self, audio_content: Dict[str, Any], 
                  visual_content: Dict[str, Any], 
                  sensory_content: Dict[str, Any],
                  daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for the Mobile Synthesizer Agent
        """
        logger.info("🚀 Mobile Synthesizer Agent starting with FIXED data structure extraction")
        return self.synthesize_dashboard_content(audio_content, visual_content, sensory_content, daily_theme)
    
    def _load_fallback_content(self) -> Dict[str, Any]:
        """Load fallback content from JSON file."""
        try:
            fallback_path = os.path.join(os.path.dirname(__file__), "../../data/fallback_content.json")
            with open(fallback_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load fallback content: {e}")
            return self._get_hardcoded_fallbacks()
    
    def _get_hardcoded_fallbacks(self) -> Dict[str, Any]:
        """Hardcoded fallbacks if JSON file unavailable."""
        return {
            "music": [{"artist": "Frank Sinatra", "song": "My Way", "youtube_url": ""}],
            "tv_shows": [{"name": "I Love Lucy", "genre": "Comedy", "youtube_url": ""}],
            "recipes": [{
                "name": "Simple Comfort Food",
                "ingredients": ["Basic ingredients"],
                "instructions": ["Simple preparation"],
                "notes": {"text": "A comforting choice", "theme": "food"},
                "conversation_starters": ["What comfort foods do you remember?"]
            }]
        }
    
    def synthesize_dashboard_content(self, audio_content: Dict[str, Any], 
                                   visual_content: Dict[str, Any], 
                                   sensory_content: Dict[str, Any],
                                   daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize content for mobile dashboard with FIXED Qloo data extraction
        """
        
        current_theme = daily_theme.get("theme_of_the_day", {})
        theme_name = current_theme.get("name", "Unknown")
        
        logger.info(f"🎯 Synthesizing dashboard content for theme: {theme_name}")
        
        try:
            # FIXED: Select content with correct Qloo data paths
            selected_content = {
                "music": self._select_music_content(audio_content, current_theme),
                "tv_show": self._select_tv_content(visual_content, current_theme),
                "recipe": self._select_recipe_content(sensory_content, current_theme),
                "theme_info": {
                    "name": theme_name,
                    "description": current_theme.get("description", ""),
                    "id": current_theme.get("id", "")
                }
            }
            
            # Generate theme-aware conversation starters
            conversation_starters = self._generate_conversation_starters(selected_content, current_theme)
            
            # Create clean dashboard response
            dashboard_result = {
                "status": "success",
                "dashboard_content": {
                    "theme_of_the_day": {
                        "name": theme_name,
                        "description": current_theme.get("description", "Today's theme for memory sharing"),
                        "id": current_theme.get("id", "")
                    },
                    "selected_content": selected_content,
                    "conversation_starters": conversation_starters,
                    "generation_metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "theme_selection_quality": self._assess_content_quality(selected_content),
                        "agent": "MobileSynthesizer",
                        "version": "fixed_qloo_data_structure"
                    }
                }
            }
            
            logger.info(f"✅ Dashboard content synthesized successfully for theme: {theme_name}")
            logger.info(f"🎵 Selected music: {selected_content['music'].get('artist', 'Unknown')} - {selected_content['music'].get('song', 'Unknown')}")
            logger.info(f"📺 Selected TV show: {selected_content['tv_show'].get('name', 'Unknown')}")
            logger.info(f"🍽️ Selected recipe: {selected_content['recipe'].get('name', 'Unknown')}")
            
            return dashboard_result
            
        except Exception as e:
            logger.error(f"❌ Error synthesizing dashboard content: {e}")
            return self._generate_fallback_dashboard(current_theme)
    
    def _select_music_content(self, audio_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Select music content from correct Qloo data structure"""
        logger.info("🎵 Extracting music content from Qloo results")
        
        try:
            # FIXED: Extract from correct Qloo data structure
            qloo_intelligence = audio_content.get("qloo_intelligence", {})
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # CRITICAL FIX: Extract from nested "entities" array
            artists_data = cultural_recommendations.get("artists", {})
            artists = artists_data.get("entities", []) if isinstance(artists_data, dict) else []
            
            logger.info(f"🔍 Found {len(artists)} artists from Qloo")
            
            if artists and len(artists) > 0:
                selected_artist = artists[0]
                artist_name = selected_artist.get("name", "Unknown Artist")
                logger.info(f"✅ Selected artist from Qloo: {artist_name}")
                
                # Map embeddable_url to youtube_url for frontend
                youtube_url = selected_artist.get("embeddable_url", "")
                
                return {
                    "artist": artist_name,
                    "song": selected_artist.get("title", selected_artist.get("name", "Unknown Song")),
                    "youtube_url": youtube_url,
                    "year": selected_artist.get("properties", {}).get("year"),
                    "genre": selected_artist.get("properties", {}).get("genre"),
                    "source": "qloo_intelligence"
                }
        except Exception as e:
            logger.warning(f"Error selecting music content from Qloo: {e}")
        
        # Fallback
        logger.info("🔄 Using fallback music content")
        fallback_music = self.fallback_data.get("music", [{}])[0]
        return {
            "artist": fallback_music.get("artist", "Classic Artist"),
            "song": fallback_music.get("song", "Timeless Song"),
            "youtube_url": fallback_music.get("youtube_url", ""),
            "year": fallback_music.get("year"),
            "genre": fallback_music.get("genre"),
            "source": "fallback"
        }
    
    def _select_tv_content(self, visual_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """FIXED: Select TV content from correct Qloo data structure"""
        logger.info("📺 Extracting TV content from Qloo results")
        
        try:
            # FIXED: Extract from correct Qloo data structure
            qloo_intelligence = visual_content.get("qloo_intelligence", {})
            cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # CRITICAL FIX: Extract from nested "entities" array
            tv_shows_data = cultural_recommendations.get("tv_shows", {})
            tv_shows = tv_shows_data.get("entities", []) if isinstance(tv_shows_data, dict) else []
            
            logger.info(f"🔍 Found {len(tv_shows)} TV shows from Qloo")
            
            if tv_shows and len(tv_shows) > 0:
                selected_show = tv_shows[0]
                show_name = selected_show.get("name", "Unknown Show")
                logger.info(f"✅ Selected TV show from Qloo: {show_name}")
                
                # Map embeddable_url to youtube_url for frontend
                youtube_url = selected_show.get("embeddable_url", "")
                
                return {
                    "name": show_name,
                    "youtube_url": youtube_url,
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
    
    def _select_recipe_content(self, sensory_content: Dict[str, Any], 
                             current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select recipe content with improved data structure navigation
        """
        
        logger.info(f"🔍 Selecting recipe content for theme: {current_theme.get('name', 'Unknown')}")
        
        # IMPROVED: More robust recipe data extraction with better error handling
        recipe_data = None
        selection_method = "unknown"
        
        try:
            # Path 1: Enhanced gustatory content structure (expected from Agent 4)
            gustatory_content = sensory_content.get("content_by_sense", {}).get("gustatory", {})
            
            # Try primary recipe first (new enhanced structure)
            if gustatory_content.get("primary_recipe"):
                recipe_data = gustatory_content["primary_recipe"]
                selection_method = "primary_recipe"
                logger.info(f"✅ Found recipe via primary_recipe: {recipe_data.get('name', 'Unknown')}")
            
            # Fallback to elements array
            elif gustatory_content.get("elements") and len(gustatory_content["elements"]) > 0:
                recipe_data = gustatory_content["elements"][0]
                selection_method = "gustatory_elements"
                logger.info(f"✅ Found recipe via gustatory elements: {recipe_data.get('name', 'Unknown')}")
            
            # Path 2: Direct sensory content structure (older format)
            elif sensory_content.get("primary_recipe"):
                recipe_data = sensory_content["primary_recipe"]
                selection_method = "direct_primary_recipe"
                logger.info(f"✅ Found recipe via direct primary_recipe: {recipe_data.get('name', 'Unknown')}")
            
            # Path 3: Sensory elements fallback
            elif sensory_content.get("sensory_elements"):
                sensory_elements = sensory_content["sensory_elements"]
                for element in sensory_elements:
                    if element.get("sense") == "gustatory" and element.get("item"):
                        recipe_data = element["item"]
                        selection_method = "sensory_elements"
                        logger.info(f"✅ Found recipe via sensory elements: {recipe_data.get('name', 'Unknown')}")
                        break
            
            if recipe_data:
                logger.info(f"🍽️ Recipe selection complete: '{recipe_data.get('name', 'Unknown')}' (method: {selection_method})")
                
                return {
                    "name": recipe_data.get("name", "Unknown Recipe"),
                    "ingredients": recipe_data.get("ingredients", []),
                    "instructions": recipe_data.get("instructions", []),
                    "notes": recipe_data.get("notes", {}),
                    "conversation_starters": recipe_data.get("conversation_starters", []),
                    "theme_connection": recipe_data.get("theme_connection", ""),
                    "source": "sensory_content",
                    "selection_method": selection_method
                }
                
        except Exception as e:
            logger.warning(f"Error selecting recipe content: {e}")
        
        # Final fallback
        logger.info("🔄 Using fallback recipe content")
        fallback_recipe = self.fallback_data.get("recipes", [{}])[0]
        return {
            "name": fallback_recipe.get("name", "Simple Comfort Food"),
            "ingredients": fallback_recipe.get("ingredients", ["Basic ingredients"]),
            "instructions": fallback_recipe.get("instructions", ["Simple preparation"]),
            "notes": fallback_recipe.get("notes", {"text": "A comforting choice"}),
            "conversation_starters": fallback_recipe.get("conversation_starters", ["What comfort foods do you remember?"]),
            "source": "fallback"
        }
    
    def _generate_conversation_starters(self, selected_content: Dict[str, Any], current_theme: Dict[str, Any]) -> List[str]:
        """Generate theme-aware conversation starters"""
        
        theme_name = current_theme.get("name", "memories")
        
        # Base conversation starters from content
        starters = []
        
        # Music-based starters
        music = selected_content.get("music", {})
        if music.get("artist"):
            starters.append(f"Do you remember listening to {music['artist']}?")
            starters.append(f"What kind of music did you enjoy when you were younger?")
        
        # TV-based starters
        tv_show = selected_content.get("tv_show", {})
        if tv_show.get("name"):
            starters.append(f"Did you ever watch {tv_show['name']}?")
            starters.append("What were your favorite TV programs?")
        
        # Recipe-based starters
        recipe = selected_content.get("recipe", {})
        if recipe.get("name"):
            starters.append(f"Have you ever made {recipe['name']}?")
        
        # Theme-specific starters
        theme_starters = {
            "Travel": [
                "What's the most memorable place you've visited?",
                "Tell me about a special trip you took."
            ],
            "Holidays": [
                "What holiday traditions did your family have?",
                "What's your favorite holiday memory?"
            ],
            "Music": [
                "What songs remind you of special times?",
                "Did you have a favorite singer or band?"
            ],
            "Food": [
                "What was your mother's best dish?",
                "What foods remind you of home?"
            ]
        }
        
        starters.extend(theme_starters.get(theme_name, [f"Tell me about your memories of {theme_name.lower()}."]))
        
        # Return up to 5 unique starters
        return list(set(starters))[:5]
    
    def _assess_content_quality(self, selected_content: Dict[str, Any]) -> str:
        """Assess the quality of selected content"""
        
        quality_scores = []
        
        # Check music source
        if selected_content.get("music", {}).get("source") == "qloo_intelligence":
            quality_scores.append("music_from_qloo")
        
        # Check TV source
        if selected_content.get("tv_show", {}).get("source") == "qloo_intelligence":
            quality_scores.append("tv_from_qloo")
        
        # Check recipe source
        if selected_content.get("recipe", {}).get("source") == "sensory_content":
            quality_scores.append("recipe_from_sensory")
        
        if len(quality_scores) >= 2:
            return "high_quality"
        elif len(quality_scores) == 1:
            return "medium_quality"
        else:
            return "fallback_content"
    
    def _generate_fallback_dashboard(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback dashboard when synthesis fails"""
        
        logger.warning("🔄 Generating fallback dashboard content")
        
        fallback_content = {
            "music": self.fallback_data.get("music", [{}])[0],
            "tv_show": self.fallback_data.get("tv_shows", [{}])[0],
            "recipe": self.fallback_data.get("recipes", [{}])[0],
            "theme_info": current_theme
        }
        
        return {
            "status": "success",
            "dashboard_content": {
                "theme_of_the_day": current_theme,
                "selected_content": fallback_content,
                "conversation_starters": [
                    "Tell me about your day.",
                    "What are you thinking about?",
                    "Would you like to share a memory?"
                ],
                "generation_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "theme_selection_quality": "fallback_only",
                    "agent": "MobileSynthesizer",
                    "version": "fixed_qloo_data_structure_fallback"
                }
            }
        }

# Export the main class
__all__ = ["MobileSynthesizerAgent"]