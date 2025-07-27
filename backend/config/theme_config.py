"""
Step 1: Enhanced Theme Manager (Simplified for Pipeline)
File: backend/config/theme_config.py

SIMPLIFIED FOR NEW PIPELINE:
- Clean theme selection from themes.json
- Daily consistency with session variation
- Photo filename mapping for UI
- No complex filtering - just clean theme data
"""

import json
import os
import random
from datetime import date
from typing import Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SimplifiedThemeManager:
    """
    Step 1: Simplified Theme Manager for Clean Pipeline
    
    PURPOSE:
    - Select themes from themes.json (10 themes)
    - Provide daily consistency with session variation
    - Map themes to photo filenames for UI
    - Clean data structure for pipeline
    """
    
    def __init__(self):
        self.themes_data = self._load_themes_config()
        self.themes_list = self.themes_data.get("themes", [])
        
        logger.info(f"🎯 Simplified Theme Manager initialized")
        logger.info(f"📁 Loaded {len(self.themes_list)} themes from themes.json")
        
        # Debug log theme names
        if self.themes_list:
            theme_names = [theme.get("name", "Unknown") for theme in self.themes_list[:5]]
            logger.info(f"🔍 Available themes (first 5): {', '.join(theme_names)}")
    
    def _load_themes_config(self) -> Dict[str, Any]:
        """Load themes from themes.json with clean fallback"""
        
        try:
            config_path = os.path.join(os.path.dirname(__file__), "themes.json")
            logger.info(f"📁 Loading themes from: {config_path}")
            
            with open(config_path, 'r') as f:
                themes_data = json.load(f)
                loaded_count = len(themes_data.get('themes', []))
                logger.info(f"✅ Successfully loaded {loaded_count} themes from themes.json")
                return themes_data
                
        except FileNotFoundError:
            logger.error(f"❌ themes.json not found at {config_path}")
        except Exception as e:
            logger.error(f"❌ Failed to load themes config: {e}")
        
        logger.warning("🔄 Using fallback themes")
        return self._get_fallback_themes()
    
    def _get_fallback_themes(self) -> Dict[str, Any]:
        """Clean fallback themes for demo reliability"""
        
        fallback_themes = [
            {
                "id": "memory_lane",
                "name": "Memory Lane",
                "description": "A journey through cherished memories and special moments",
                "conversation_prompts": [
                    "Tell me about a happy memory",
                    "What's something that always makes you smile?",
                    "Share a story from the good old days"
                ]
            },
            {
                "id": "family",
                "name": "Family",
                "description": "Celebrating family bonds and togetherness",
                "conversation_prompts": [
                    "Tell me about your family",
                    "What family traditions were special to you?",
                    "Who in your family made you laugh the most?"
                ]
            },
            {
                "id": "music",
                "name": "Music",
                "description": "The soundtrack of life and memorable melodies",
                "conversation_prompts": [
                    "What was your favorite song when you were young?",
                    "Did you ever dance to this kind of music?",
                    "What music did your family listen to together?"
                ]
            },
            {
                "id": "birthday",
                "name": "Birthday",
                "description": "Celebrating special occasions and milestones",
                "conversation_prompts": [
                    "How did you celebrate birthdays when you were young?",
                    "What was your favorite kind of birthday cake?",
                    "Do you remember a special birthday gift?"
                ]
            },
            {
                "id": "food",
                "name": "Food",
                "description": "Favorite foods and cooking memories",
                "conversation_prompts": [
                    "What was your favorite food growing up?",
                    "Did you enjoy cooking?",
                    "What foods remind you of home?"
                ]
            }
        ]
        
        return {"themes": fallback_themes}
    
    def get_daily_theme(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get theme of the day with daily consistency and session variation
        
        Args:
            session_id: Optional session ID for variation
            
        Returns:
            Selected theme with photo mapping
        """
        
        if not self.themes_list:
            logger.error("❌ No themes available")
            return self._create_fallback_theme_response()
        
        # Create daily seed for consistency
        today = date.today()
        daily_seed = hash(f"{today.year}-{today.month}-{today.day}")
        
        # Add session variation if provided
        if session_id:
            daily_seed = hash(f"{daily_seed}-{session_id}")
        
        # Select theme using seed
        random.seed(daily_seed)
        selected_theme = random.choice(self.themes_list)
        
        # Get photo filename for UI
        photo_filename = self._get_photo_filename(selected_theme)
        
        theme_name = selected_theme.get("name", "Unknown")
        logger.info(f"🎯 Daily theme selected: {theme_name}")
        logger.info(f"📷 Photo filename: {photo_filename}")
        
        return {
            "theme_of_the_day": selected_theme,
            "photo_filename": photo_filename,
            "selection_metadata": {
                "date": today.isoformat(),
                "daily_seed": daily_seed,
                "total_themes_available": len(self.themes_list),
                "selection_method": "daily_consistent_with_session_variation"
            }
        }
    
    def _get_photo_filename(self, theme: Dict[str, Any]) -> str:
        """
        Map theme to photo filename for UI
        
        Args:
            theme: Theme data
            
        Returns:
            Photo filename for UI (e.g. "birthday.png")
        """
        
        theme_id = theme.get("id", "")
        theme_name = theme.get("name", "")
        
        # Try theme ID first (most reliable)
        if theme_id:
            filename = f"{theme_id.lower()}.png"
        else:
            # Fallback to theme name
            clean_name = theme_name.lower().replace(" ", "_").replace("'", "")
            filename = f"{clean_name}.png"
        
        logger.debug(f"📷 Theme '{theme_name}' → Photo '{filename}'")
        return filename
    
    def get_theme_by_id(self, theme_id: str) -> Optional[Dict[str, Any]]:
        """Get specific theme by ID"""
        
        for theme in self.themes_list:
            if theme.get("id") == theme_id:
                return theme
        
        logger.warning(f"⚠️ Theme ID '{theme_id}' not found")
        return None
    
    def get_all_themes(self) -> List[Dict[str, Any]]:
        """Get all available themes"""
        return self.themes_list.copy()
    
    def _create_fallback_theme_response(self) -> Dict[str, Any]:
        """Create fallback when no themes available"""
        
        fallback_theme = {
            "id": "memory_lane",
            "name": "Memory Lane",
            "description": "A time for remembering special moments",
            "conversation_prompts": [
                "Tell me about a happy memory",
                "What's something that always makes you smile?"
            ]
        }
        
        return {
            "theme_of_the_day": fallback_theme,
            "photo_filename": "memory_lane.png",
            "selection_metadata": {
                "date": date.today().isoformat(),
                "fallback_used": True,
                "fallback_reason": "no_themes_available"
            }
        }
    
    def validate_themes(self) -> Dict[str, Any]:
        """Validate theme configuration for debugging"""
        
        validation_results = {
            "total_themes": len(self.themes_list),
            "valid_themes": [],
            "invalid_themes": [],
            "missing_fields": []
        }
        
        required_fields = ["id", "name", "description", "conversation_prompts"]
        
        for i, theme in enumerate(self.themes_list):
            theme_name = theme.get("name", f"Theme_{i}")
            
            # Check required fields
            missing = [field for field in required_fields if not theme.get(field)]
            
            if missing:
                validation_results["invalid_themes"].append({
                    "name": theme_name,
                    "missing_fields": missing
                })
                validation_results["missing_fields"].extend(missing)
            else:
                validation_results["valid_themes"].append(theme_name)
        
        # Remove duplicates
        validation_results["missing_fields"] = list(set(validation_results["missing_fields"]))
        
        logger.info(f"📊 Theme validation: {len(validation_results['valid_themes'])}/{validation_results['total_themes']} valid")
        
        return validation_results

# Global instance for easy import
simplified_theme_manager = SimplifiedThemeManager()

# Export
__all__ = ["SimplifiedThemeManager", "simplified_theme_manager"]