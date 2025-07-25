"""
Mobile Synthesizer Agent - FIXED Qloo Data Path Mapping + YouTube URL Support
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

CHANGES:
- FIXED: Correct data path mapping from Agent 3 (Qloo) output structure
- Added YouTube URL mapping from embeddable_url to youtube_url
- Enhanced theme-based recipe selection
- Proper run() method for pipeline compatibility
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
    Agent 6: Mobile Synthesizer with FIXED Qloo Data Path Mapping
    
    FIXES:
    - Correct data extraction from Agent 3 (Qloo Cultural Intelligence) output
    - YouTube URL mapping from embeddable_url to youtube_url
    - Enhanced theme-based recipe selection
    - Proper pipeline integration
    """
    
    def __init__(self):
        self.fallback_data = self._load_fallback_content()
        logger.info("Mobile Synthesizer initialized with FIXED Qloo data path mapping")
    
    async def run(self, audio_content: Dict[str, Any], 
                  visual_content: Dict[str, Any], 
                  sensory_content: Dict[str, Any],
                  daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for the Mobile Synthesizer Agent
        """
        logger.info("🚀 Mobile Synthesizer Agent starting with FIXED data path mapping")
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
            "music": [{"artist": "Unknown Artist", "song": "Unforgotten Melody", "youtube_url": ""}],
            "tv_shows": [{"name": "Classic Show", "genre": "Drama", "youtube_url": ""}],
            "recipes": [{
                "name": "Simple Warm Snack",
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
                        "version": "fixed_qloo_mapping"
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
            artists = cultural_recommendations.get("artists", [])
            
            logger.info(f"🔍 Found {len(artists)} artists from Qloo")
            
            if artists and len(artists) > 0:
                selected_artist = artists[0]
                logger.info(f"✅ Selected artist from Qloo: {selected_artist.get('name', 'Unknown')}")
                
                # Map embeddable_url to youtube_url for frontend
                youtube_url = selected_artist.get("embeddable_url", "")
                
                return {
                    "artist": selected_artist.get("name", "Unknown Artist"),
                    "song": selected_artist.get("title", selected_artist.get("name", "Unknown Song")),
                    "youtube_url": youtube_url,
                    "year": selected_artist.get("year"),
                    "genre": selected_artist.get("genre"),
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
            tv_shows = cultural_recommendations.get("tv_shows", [])
            
            logger.info(f"🔍 Found {len(tv_shows)} TV shows from Qloo")
            
            if tv_shows and len(tv_shows) > 0:
                selected_show = tv_shows[0]
                logger.info(f"✅ Selected TV show from Qloo: {selected_show.get('name', 'Unknown')}")
                
                # Map embeddable_url to youtube_url for frontend
                youtube_url = selected_show.get("embeddable_url", "")
                
                return {
                    "name": selected_show.get("name", "Unknown Show"),
                    "youtube_url": youtube_url,
                    "genre": selected_show.get("genre"),
                    "year": selected_show.get("year"),
                    "description": selected_show.get("description"),
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
            
            # Path 2: Direct sensory content fallback
            elif sensory_content.get("gustatory_content"):
                recipe_data = sensory_content["gustatory_content"]
                selection_method = "direct_gustatory"
                logger.info(f"✅ Found recipe via direct gustatory content: {recipe_data.get('name', 'Unknown')}")
            
        except Exception as e:
            logger.warning(f"⚠️ Error in recipe extraction: {e}")
        
        # Use theme-specific fallback if no recipe found
        if not recipe_data:
            logger.warning(f"⚠️ No recipe found in sensory content, using theme-specific fallback")
            recipe_data = self._get_theme_fallback_recipe(current_theme)
            selection_method = "theme_fallback"
        
        # Validate and enrich recipe data
        validated_recipe = self._validate_and_enrich_recipe(recipe_data, current_theme, selection_method)
        
        logger.info(f"🍽️ Recipe selection complete: '{validated_recipe.get('name', 'Unknown')}' (method: {selection_method})")
        return validated_recipe
    
    def _validate_and_enrich_recipe(self, recipe_data: Dict[str, Any], 
                                  current_theme: Dict[str, Any], 
                                  selection_method: str) -> Dict[str, Any]:
        """
        Validate and enrich recipe data with theme context
        """
        
        if not recipe_data:
            logger.warning("⚠️ Empty recipe data provided for validation")
            recipe_data = {}
        
        # Ensure required fields exist with sensible defaults
        validated_recipe = {
            "name": recipe_data.get("name", "Simple Comfort Food"),
            "ingredients": recipe_data.get("ingredients", ["Basic ingredients as needed"]),
            "instructions": recipe_data.get("instructions", ["Prepare with care and love"]),
            "notes": recipe_data.get("notes", {"text": "A nourishing choice", "theme": current_theme.get("id", "food")}),
            "conversation_starters": recipe_data.get("conversation_starters", []),
            "selection_metadata": {
                "method": selection_method,
                "theme_id": current_theme.get("id"),
                "theme_name": current_theme.get("name"),
                "selected_at": datetime.now().isoformat(),
                "quality": self._assess_recipe_quality(recipe_data, current_theme)
            }
        }
        
        # Ensure conversation starters exist
        if not validated_recipe["conversation_starters"]:
            validated_recipe["conversation_starters"] = self._get_default_recipe_starters(current_theme)
        
        return validated_recipe
    
    def _assess_recipe_quality(self, recipe_data: Dict[str, Any], current_theme: Dict[str, Any]) -> str:
        """Assess the quality of recipe selection for theme matching"""
        if not recipe_data:
            return "fallback"
        
        # Check if recipe has explicit theme matching
        if isinstance(recipe_data.get("notes"), dict):
            recipe_theme = recipe_data["notes"].get("theme")
            if recipe_theme == current_theme.get("id"):
                return "exact_theme_match"
        
        # Check if recipe has conversation starters
        if recipe_data.get("conversation_starters"):
            return "good_with_starters"
        
        return "basic"
    
    def _get_theme_fallback_recipe(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Get theme-specific fallback recipe"""
        
        theme_id = current_theme.get("id", "food")
        theme_name = current_theme.get("name", "Food")
        
        # Theme-specific fallback recipes
        theme_fallbacks = {
            "birthday": {
                "name": "Birthday Cookie (soft)",
                "ingredients": ["1 soft cookie", "Optional: small amount of frosting"],
                "instructions": ["If cookie is hard, soften slightly with a damp paper towel", "Enjoy this special treat"],
                "conversation_starters": ["What were your favorite birthday treats?", "Tell me about a memorable birthday"]
            },
            "family": {
                "name": "Family Comfort Toast",
                "ingredients": ["1 slice bread", "Butter or favorite spread"],
                "instructions": ["Toast bread lightly", "Add your favorite spread", "Share memories while eating"],
                "conversation_starters": ["What foods did your family make together?", "What comfort foods remind you of home?"]
            },
            "music": {
                "name": "Music Listening Snack",
                "ingredients": ["Your favorite listening snack", "A comfortable seat"],
                "instructions": ["Prepare your favorite snack", "Find a comfortable spot", "Enjoy music and memories"],
                "conversation_starters": ["What music brings back memories?", "Did you have favorite songs to eat by?"]
            },
            "food": {
                "name": "Simple Comfort Snack",
                "ingredients": ["Your favorite easy-to-eat snack"],
                "instructions": ["Choose something you enjoy", "Take your time and savor it"],
                "conversation_starters": ["What foods bring you comfort?", "What did you like to cook or eat?"]
            }
        }
        
        # Get theme-specific fallback or default
        fallback_recipe = theme_fallbacks.get(theme_id, theme_fallbacks["food"])
        
        # Add theme context
        fallback_recipe["notes"] = {
            "text": f"A comforting choice for {theme_name} theme",
            "theme": theme_id
        }
        
        return fallback_recipe
    
    def _get_default_recipe_starters(self, current_theme: Dict[str, Any]) -> List[str]:
        """Get default conversation starters for recipes"""
        return [
            "What foods bring back good memories?",
            "Do you have a favorite comfort food?",
            "What did you like to cook or eat?"
        ]
    
    def _generate_conversation_starters(self, selected_content: Dict[str, Any], 
                                      current_theme: Dict[str, Any]) -> List[str]:
        """
        Generate conversation starters with improved theme integration
        """
        if not theme_manager:
            # Fallback without theme manager
            return [
                "What brings back good memories for you?",
                "Tell me about something that makes you happy",
                "What was special about your day?"
            ]
        
        try:
            starters = theme_manager.get_theme_conversation_starters(current_theme, selected_content)
            logger.info(f"🗣️ Generated {len(starters)} conversation starters")
            return starters[:5]  # Limit to 5 for mobile UI
        except Exception as e:
            logger.warning(f"Error generating conversation starters: {e}")
            return [
                "What brings back good memories for you?",
                "Tell me about something that makes you happy"
            ]
    
    def _assess_content_quality(self, selected_content: Dict[str, Any]) -> str:
        """Assess overall quality of content selection"""
        quality_factors = []
        
        # Check recipe quality
        recipe_quality = selected_content.get("recipe", {}).get("selection_metadata", {}).get("quality", "unknown")
        quality_factors.append(recipe_quality)
        
        # Check if all content types are present
        if all(key in selected_content for key in ["music", "tv_show", "recipe"]):
            quality_factors.append("complete")
        
        # Check if content is from live Qloo data
        if selected_content.get("music", {}).get("source") == "qloo_intelligence":
            quality_factors.append("live_qloo_music")
        if selected_content.get("tv_show", {}).get("source") == "qloo_intelligence":
            quality_factors.append("live_qloo_tv")
        
        # Determine overall quality
        if "exact_theme_match" in quality_factors:
            return "excellent"
        elif "live_qloo_music" in quality_factors and "live_qloo_tv" in quality_factors:
            return "very_good"
        elif any("live_qloo" in factor for factor in quality_factors):
            return "good"
        elif "complete" in quality_factors:
            return "acceptable"
        else:
            return "fallback"
    
    def _generate_fallback_dashboard(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback dashboard content when main synthesis fails"""
        logger.warning("🔄 Generating fallback dashboard content")
        
        theme_name = current_theme.get("name", "Memory Lane")
        
        return {
            "status": "fallback",
            "dashboard_content": {
                "theme_of_the_day": {
                    "name": theme_name,
                    "description": current_theme.get("description", "Today's theme for sharing memories"),
                    "id": current_theme.get("id", "general")
                },
                "selected_content": {
                    "music": {"artist": "Classic Artist", "song": "Memorable Tune", "youtube_url": "", "source": "fallback"},
                    "tv_show": {"name": "Beloved Show", "genre": "Classic", "youtube_url": "", "source": "fallback"},
                    "recipe": self._get_theme_fallback_recipe(current_theme),
                    "theme_info": {
                        "name": theme_name,
                        "description": current_theme.get("description", ""),
                        "id": current_theme.get("id", "")
                    }
                },
                "conversation_starters": [
                    "What brings back good memories for you?",
                    f"Tell me about something related to {theme_name.lower()}",
                    "What was special in your day?"
                ],
                "generation_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "theme_selection_quality": "fallback",
                    "agent": "MobileSynthesizer",
                    "version": "fallback_mode"
                }
            }
        }