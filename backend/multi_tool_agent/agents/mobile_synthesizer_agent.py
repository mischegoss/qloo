"""
Mobile Synthesizer Agent - REVISED for Enhanced Theme-Based Recipe Selection
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

CHANGES:
- Leverages improved theme-matched recipes from Agent 4
- Simplified data structure navigation due to better upstream filtering
- Enhanced error handling and logging
- More reliable recipe selection process
- FIXED: Added proper run() method for pipeline compatibility
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
    Agent 6: Mobile Synthesizer with ENHANCED Theme-Based Recipe Selection
    
    IMPROVEMENTS:
    - More reliable recipe data extraction due to better upstream theme matching
    - Simplified data structure navigation
    - Enhanced conversation starter integration
    - Better error handling and fallback mechanisms
    - FIXED: Added proper run() method for pipeline compatibility
    """
    
    def __init__(self):
        self.fallback_data = self._load_fallback_content()
        logger.info("Mobile Synthesizer initialized with ENHANCED theme-aware content selection")
    
    async def run(self, audio_content: Dict[str, Any], 
                  visual_content: Dict[str, Any], 
                  sensory_content: Dict[str, Any],
                  daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Main entry point for the Mobile Synthesizer Agent (async for pipeline compatibility)
        
        Args:
            audio_content: Audio content from Agent 3
            visual_content: Visual content from Agent 2
            sensory_content: Enhanced sensory content from Agent 4
            daily_theme: Current theme configuration
            
        Returns:
            Clean dashboard content with theme-matched selections
        """
        logger.info("🚀 Mobile Synthesizer Agent starting with async run() method")
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
            "music": [{"artist": "Unknown Artist", "song": "Unforgotten Melody"}],
            "tv_shows": [{"name": "Classic Show", "genre": "Drama"}],
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
        REVISED: Synthesize content for mobile dashboard with enhanced theme integration
        
        Args:
            audio_content: Audio content from Agent 3
            visual_content: Visual content from Agent 2
            sensory_content: Enhanced sensory content from Agent 4
            daily_theme: Current theme configuration
            
        Returns:
            Clean dashboard content with theme-matched selections
        """
        
        current_theme = daily_theme.get("theme_of_the_day", {})
        theme_name = current_theme.get("name", "Unknown")
        
        logger.info(f"🎯 Synthesizing dashboard content for theme: {theme_name}")
        
        try:
            # ENHANCED: Select content with better theme awareness
            selected_content = {
                "music": self._select_music_content(audio_content, current_theme),
                "tv_show": self._select_tv_content(visual_content, current_theme),
                "recipe": self._select_recipe_content(sensory_content, current_theme),  # IMPROVED
                "theme_info": {
                    "name": theme_name,
                    "description": current_theme.get("description", ""),
                    "id": current_theme.get("id", "")
                }
            }
            
            # ENHANCED: Generate theme-aware conversation starters
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
                        "version": "enhanced_theme_matching"
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
    
    def _select_recipe_content(self, sensory_content: Dict[str, Any], 
                             current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCED: Select recipe content with improved data structure navigation
        
        Args:
            sensory_content: Sensory content including theme-filtered recipes
            current_theme: Current theme configuration
            
        Returns:
            Single recipe selection with enhanced metadata
        """
        
        logger.info(f"🔍 Selecting recipe content for theme: {current_theme.get('name', 'Unknown')}")
        
        # IMPROVED: More robust recipe data extraction with better error handling
        recipe_data = None
        selection_method = "unknown"
        
        try:
            # Path 1: Enhanced gustatory content structure (expected from Agent 4)
            gustatory_content = sensory_content.get("content_by_sense", {}).get("gustatory", {})
            
            # Try primary_recipe first (new enhanced structure)
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
        
        # ENHANCED: Use theme-specific fallback if no recipe found
        if not recipe_data:
            logger.warning(f"⚠️ No recipe found in sensory content, using theme-specific fallback")
            recipe_data = self._get_theme_fallback_recipe(current_theme)
            selection_method = "theme_fallback"
        
        # ENHANCED: Validate and enrich recipe data
        validated_recipe = self._validate_and_enrich_recipe(recipe_data, current_theme, selection_method)
        
        logger.info(f"🍽️ Recipe selection complete: '{validated_recipe.get('name', 'Unknown')}' (method: {selection_method})")
        return validated_recipe
    
    def _validate_and_enrich_recipe(self, recipe_data: Dict[str, Any], 
                                  current_theme: Dict[str, Any], 
                                  selection_method: str) -> Dict[str, Any]:
        """
        ENHANCED: Validate and enrich recipe data with theme context
        
        Args:
            recipe_data: Raw recipe data
            current_theme: Current theme configuration
            selection_method: How the recipe was selected
            
        Returns:
            Validated and enriched recipe data
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
    
    def _get_theme_fallback_recipe(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCED: Get theme-specific fallback recipe
        
        Args:
            current_theme: Current theme configuration
            
        Returns:
            Theme-appropriate fallback recipe
        """
        
        theme_id = current_theme.get("id", "food")
        theme_name = current_theme.get("name", "Food")
        
        # Theme-specific fallback recipes
        theme_fallbacks = {
            "birthday": {
                "name": "Birthday Cookie (soft)",
                "ingredients": ["1 soft cookie", "Optional: small amount of frosting"],
                "instructions": ["If cookie is hard, soften slightly in microwave for 5-10 seconds", "Enjoy slowly"],
                "notes": {"text": "A sweet treat perfect for celebrating special moments", "theme": "birthday"}
            },
            "seasons": {
                "name": "Seasonal Fruit Cup", 
                "ingredients": ["1/2 cup canned or soft fresh fruit"],
                "instructions": ["Serve at room temperature or slightly warmed"],
                "notes": {"text": "Fresh flavors that change with the seasons", "theme": "seasons"}
            },
            "weather": {
                "name": "Warming Tea and Toast",
                "ingredients": ["1 slice soft bread", "Butter", "Warm tea or warm milk"],
                "instructions": ["Lightly toast bread until soft", "Add butter", "Serve with warm beverage"],
                "notes": {"text": "Perfect comfort for any weather", "theme": "weather"}
            },
            "travel": {
                "name": "Travel Snack Mix",
                "ingredients": ["Small crackers", "Soft cheese or spread"],
                "instructions": ["Arrange crackers", "Add small amount of spread"],
                "notes": {"text": "Reminiscent of snacks enjoyed while traveling", "theme": "travel"}
            }
        }
        
        fallback_recipe = theme_fallbacks.get(theme_id, {
            "name": f"{theme_name} Comfort Snack",
            "ingredients": ["Simple, nourishing ingredients"],
            "instructions": ["Prepare with care"],
            "notes": {"text": f"A comforting choice for {theme_name.lower()} memories", "theme": theme_id}
        })
        
        # Add conversation starters
        fallback_recipe["conversation_starters"] = self._get_default_recipe_starters(current_theme)
        
        logger.info(f"🔄 Using theme fallback recipe: {fallback_recipe['name']}")
        return fallback_recipe
    
    def _get_default_recipe_starters(self, current_theme: Dict[str, Any]) -> List[str]:
        """Get default conversation starters for recipes"""
        theme_prompts = current_theme.get("conversation_prompts", [])
        if theme_prompts:
            return theme_prompts[:3]
        
        return [
            "What foods bring back good memories?",
            "Do you have a favorite comfort food?",
            "What did you like to cook or eat?"
        ]
    
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
    
    def _select_music_content(self, audio_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select music content (existing logic maintained)"""
        try:
            songs = audio_content.get("songs", [])
            if songs and len(songs) > 0:
                selected_song = songs[0]
                return {
                    "artist": selected_song.get("artist", "Unknown Artist"),
                    "song": selected_song.get("title", "Unknown Song"),
                    "year": selected_song.get("year"),
                    "genre": selected_song.get("genre")
                }
        except Exception as e:
            logger.warning(f"Error selecting music content: {e}")
        
        # Fallback
        fallback_music = self.fallback_data.get("music", [{}])[0]
        return {
            "artist": fallback_music.get("artist", "Classic Artist"),
            "song": fallback_music.get("song", "Timeless Song"),
            "year": fallback_music.get("year"),
            "genre": fallback_music.get("genre")
        }
    
    def _select_tv_content(self, visual_content: Dict[str, Any], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select TV content (existing logic maintained)"""
        try:
            tv_shows = visual_content.get("tv_shows", [])
            if tv_shows and len(tv_shows) > 0:
                selected_show = tv_shows[0]
                return {
                    "name": selected_show.get("name", "Unknown Show"),
                    "genre": selected_show.get("genre"),
                    "year": selected_show.get("year"),
                    "description": selected_show.get("description")
                }
        except Exception as e:
            logger.warning(f"Error selecting TV content: {e}")
        
        # Fallback
        fallback_tv = self.fallback_data.get("tv_shows", [{}])[0]
        return {
            "name": fallback_tv.get("name", "Classic Television"),
            "genre": fallback_tv.get("genre"),
            "year": fallback_tv.get("year"),
            "description": fallback_tv.get("description")
        }
    
    def _generate_conversation_starters(self, selected_content: Dict[str, Any], 
                                      current_theme: Dict[str, Any]) -> List[str]:
        """
        ENHANCED: Generate conversation starters with improved theme integration
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
        
        # Determine overall quality
        if "exact_theme_match" in quality_factors:
            return "excellent"
        elif "good_with_starters" in quality_factors or "complete" in quality_factors:
            return "good"
        else:
            return "acceptable"
    
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
                    "music": {"artist": "Classic Artist", "song": "Memorable Tune"},
                    "tv_show": {"name": "Beloved Show", "genre": "Classic"},
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