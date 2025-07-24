"""
Theme Configuration Manager for Dementia-Friendly Daily Themes
File: backend/config/theme_config.py

Manages daily theme selection and theme-aware content filtering
"""

import json
import os
import random
from datetime import date
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

class ThemeManager:
    """Manages daily theme selection and theme-aware content filtering"""
    
    def __init__(self):
        self.themes_data = self._load_themes_config()
        self.themes_list = self.themes_data.get("themes", [])
        logger.info(f"🎯 Theme Manager initialized with {len(self.themes_list)} themes")
        
        # Debug: Log theme names if available
        if self.themes_list:
            theme_names = [theme.get("name", "Unknown") for theme in self.themes_list[:5]]
            logger.info(f"🔍 DEBUG: Available themes (first 5): {', '.join(theme_names)}")
        else:
            logger.error("❌ DEBUG: No themes loaded during initialization!")
    
    def debug_theme_status(self) -> Dict[str, Any]:
        """Debug method to check theme loading status"""
        return {
            "themes_loaded": len(self.themes_list),
            "theme_names": [theme.get("name", "Unknown") for theme in self.themes_list],
            "config_file_path": os.path.join(os.path.dirname(__file__), "themes.json"),
            "file_exists": os.path.exists(os.path.join(os.path.dirname(__file__), "themes.json"))
        }
    
    def _load_themes_config(self) -> Dict[str, Any]:
        """Load themes configuration from JSON file"""
        try:
            # Try the correct filename first
            config_path = os.path.join(os.path.dirname(__file__), "themes.json")
            logger.info(f"Attempting to load themes from: {config_path}")
            
            with open(config_path, 'r') as f:
                themes_data = json.load(f)
                logger.info(f"✅ Successfully loaded {len(themes_data.get('themes', []))} dementia-friendly themes from themes.json")
                return themes_data
                
        except FileNotFoundError:
            logger.error(f"❌ themes.json not found at {config_path}")
            # Try alternative filename as fallback
            try:
                alt_path = os.path.join(os.path.dirname(__file__), "dementia_themes.json")
                logger.info(f"Trying alternative path: {alt_path}")
                with open(alt_path, 'r') as f:
                    themes_data = json.load(f)
                    logger.info(f"✅ Loaded themes from alternative file: dementia_themes.json")
                    return themes_data
            except Exception as alt_e:
                logger.error(f"❌ Alternative file also failed: {alt_e}")
                
        except Exception as e:
            logger.error(f"❌ Failed to load themes config: {e}")
            
        logger.warning("🔄 Using fallback themes due to file loading issues")
        return self._get_fallback_themes()
    
    def _get_fallback_themes(self) -> Dict[str, Any]:
        """Fallback themes if JSON loading fails"""
        return {
            "themes": [
                {
                    "id": "music",
                    "name": "Music", 
                    "description": "Songs and musical memories",
                    "conversation_prompts": ["What was your favorite song when you were young?"],
                    "recipe_keywords": ["comfort", "celebration"],
                    "content_preferences": {"qloo_priority": "artists", "sensory_focus": "auditory"}
                },
                {
                    "id": "family",
                    "name": "Family",
                    "description": "Family memories and relationships", 
                    "conversation_prompts": ["Tell me about your family"],
                    "recipe_keywords": ["traditional", "sharing"],
                    "content_preferences": {"qloo_priority": "places", "sensory_focus": "gustatory"}
                }
            ]
        }
    
    def get_daily_theme(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the theme of the day using daily seed for consistency
        
        Args:
            session_id: Optional session identifier for additional randomization
            
        Returns:
            Selected theme with full configuration
        """
        
        # Debug: Check if themes are loaded
        logger.info(f"🔍 DEBUG: Available themes count: {len(self.themes_list)}")
        if len(self.themes_list) > 0:
            logger.info(f"🔍 DEBUG: First theme: {self.themes_list[0].get('name', 'Unknown')}")
        else:
            logger.error("❌ DEBUG: No themes available - using fallback")
            # Force reload fallback
            self.themes_data = self._get_fallback_themes()
            self.themes_list = self.themes_data.get("themes", [])
        
        # Use daily seed for consistent theme throughout the day
        today = date.today()
        daily_seed = hash(f"{today.year}-{today.month}-{today.day}")
        
        # Add session variation if provided (but keep daily consistency)
        if session_id:
            daily_seed = hash(f"{daily_seed}-{session_id}")
        
        # Set seed and select theme
        random.seed(daily_seed)
        selected_theme = random.choice(self.themes_list)
        
        logger.info(f"🎯 Daily theme selected: {selected_theme['name']} (ID: {selected_theme['id']})")
        logger.info(f"🔍 DEBUG: Theme description: {selected_theme.get('description', 'No description')}")
        
        return {
            "theme_of_the_day": selected_theme,
            "selection_metadata": {
                "date": today.isoformat(),
                "daily_seed": daily_seed,
                "total_themes_available": len(self.themes_list),
                "selection_method": "daily_consistent",
                "debug_info": {
                    "themes_loaded": len(self.themes_list) > 0,
                    "themes_source": "themes.json" if len(self.themes_list) > 2 else "fallback"
                }
            }
        }
    
    def get_theme_by_id(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Get specific theme by ID"""
        for theme in self.themes_list:
            if theme["id"] == theme_id:
                return theme
        return None
    
    def get_theme_conversation_starters(self, theme: Dict[str, Any], 
                                      selected_content: Dict[str, Any]) -> List[str]:
        """
        Generate theme-aware conversation starters
        
        Args:
            theme: Current theme configuration
            selected_content: Selected music, tv_show, recipe content
            
        Returns:
            List of conversation starters tailored to theme and content
        """
        starters = []
        
        # Add theme-specific prompts
        theme_prompts = theme.get("conversation_prompts", [])
        if theme_prompts:
            starters.extend(random.sample(theme_prompts, min(2, len(theme_prompts))))
        
        # Add content-aware prompts based on selected content
        if selected_content.get("music"):
            music = selected_content["music"]
            if music.get("artist"):
                starters.append(f"Do you remember {music['artist']}?")
        
        if selected_content.get("tv_show"):
            tv_show = selected_content["tv_show"]
            if tv_show.get("name"):
                starters.append(f"Did you ever watch {tv_show['name']}?")
        
        if selected_content.get("recipe"):
            recipe = selected_content["recipe"]
            if recipe.get("name"):
                starters.append(f"Does {recipe['name']} remind you of anything special?")
        
        # Ensure we have at least one fallback
        if not starters:
            starters = [
                "What brings back good memories for you?",
                "Tell me about something that makes you happy"
            ]
        
        return starters
    
    def filter_recipes_by_theme(self, recipes: List[Dict[str, Any]], 
                               theme: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter and prioritize recipes based on theme keywords
        
        Args:
            recipes: List of available recipes
            theme: Current theme configuration
            
        Returns:
            Filtered and prioritized recipe list
        """
        if not recipes or not theme:
            return recipes
        
        theme_keywords = theme.get("recipe_keywords", [])
        if not theme_keywords:
            return recipes
        
        # Score recipes based on theme keyword matches
        scored_recipes = []
        for recipe in recipes:
            score = 0
            recipe_text = (recipe.get("name", "") + " " + 
                          recipe.get("notes", "") + " " +
                          " ".join(recipe.get("ingredients", []))).lower()
            
            # Check for theme keyword matches
            for keyword in theme_keywords:
                if keyword.lower() in recipe_text:
                    score += 1
            
            scored_recipes.append((recipe, score))
        
        # Sort by score (highest first) and return recipes
        scored_recipes.sort(key=lambda x: x[1], reverse=True)
        filtered_recipes = [recipe for recipe, score in scored_recipes]
        
        logger.info(f"Filtered {len(recipes)} recipes by theme '{theme['name']}', "
                   f"top recipe: {filtered_recipes[0]['name'] if filtered_recipes else 'none'}")
        
        return filtered_recipes
    
    def get_theme_content_priority(self, theme: Dict[str, Any]) -> str:
        """
        Get content priority for theme (which type of content to emphasize)
        
        Args:
            theme: Current theme configuration
            
        Returns:
            Priority content type ('artists', 'places', 'tv_shows')
        """
        return theme.get("content_preferences", {}).get("qloo_priority", "places")
    
    def get_theme_sensory_focus(self, theme: Dict[str, Any]) -> str:
        """
        Get sensory focus for theme (which sense to emphasize)
        
        Args:
            theme: Current theme configuration
            
        Returns:
            Sensory focus type
        """
        return theme.get("content_preferences", {}).get("sensory_focus", "visual")

# Global theme manager instance
theme_manager = ThemeManager()