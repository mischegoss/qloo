"""
Dynamic Theme Manager - FIXED with True Rotation
File: backend/config/theme_config.py

FIXED:
- TRUE ROTATION: Themes cycle in order, never repeat consecutively
- Persistent theme tracking across refreshes
- Guaranteed variety for users
- Simple, predictable rotation
"""

import json
import os
import random
import time
from datetime import date, datetime
from typing import Dict, Any, Optional, List
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SimplifiedThemeManager:
    """
    Dynamic Theme Manager with True Rotation
    
    PURPOSE:
    - Select themes from themes.json (9 themes)
    - NEW: TRUE ROTATION - never repeats consecutively
    - Persistent tracking across refreshes
    - Clean data structure for pipeline
    """
    
    def __init__(self):
        self.themes_data = self._load_themes_config()
        self.themes_list = self.themes_data.get("themes", [])
        self.state_file = os.path.join(os.path.dirname(__file__), "theme_state.json")
        
        logger.info(f"🎯 Dynamic Theme Manager initialized with ROTATION")
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
    
    def _load_theme_state(self) -> Dict[str, Any]:
        """Load current rotation state from persistent storage"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    logger.info(f"📖 Loaded theme state: index {state.get('current_index', 0)}")
                    return state
        except Exception as e:
            logger.warning(f"⚠️ Could not load theme state: {e}")
        
        # Default state
        return {"current_index": 0, "total_themes": len(self.themes_list)}
    
    def _save_theme_state(self, current_index: int):
        """Save current rotation state to persistent storage"""
        try:
            state = {
                "current_index": current_index,
                "total_themes": len(self.themes_list),
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
                
            logger.info(f"💾 Saved theme state: index {current_index}")
            
        except Exception as e:
            logger.error(f"❌ Could not save theme state: {e}")
    
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
                "description": "Cherishing family bonds and togetherness",
                "conversation_prompts": [
                    "Tell me about your family",
                    "What family traditions were special to you?",
                    "Who made you laugh the most?"
                ]
            },
            {
                "id": "birthday",
                "name": "Birthday",
                "description": "Celebrating special occasions and joyful milestones",
                "conversation_prompts": [
                    "How did you celebrate birthdays?",
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
            },
            {
                "id": "music",
                "name": "Music",
                "description": "Musical memories and favorite songs",
                "conversation_prompts": [
                    "What music did you love?",
                    "Did you sing or play instruments?",
                    "What songs bring back memories?"
                ]
            },
            {
                "id": "travel",
                "name": "Travel",
                "description": "Adventures and places you've been",
                "conversation_prompts": [
                    "What's your favorite place you've visited?",
                    "Tell me about a memorable trip",
                    "Where did you dream of going?"
                ]
            },
            {
                "id": "seasons",
                "name": "Seasons",
                "description": "Seasonal memories and favorite times of year",
                "conversation_prompts": [
                    "What's your favorite season?",
                    "What did you enjoy about winter/summer?",
                    "Tell me about seasonal traditions"
                ]
            },
            {
                "id": "hobbies",
                "name": "Hobbies",
                "description": "Favorite activities and pastimes",
                "conversation_prompts": [
                    "What hobbies did you enjoy?",
                    "How did you spend your free time?",
                    "What activities made you happy?"
                ]
            },
            {
                "id": "nature",
                "name": "Nature",
                "description": "Outdoor memories and nature experiences",
                "conversation_prompts": [
                    "Do you enjoy being outdoors?",
                    "Tell me about your favorite natural place",
                    "What animals or plants do you love?"
                ]
            }
        ]
        
        return {"themes": fallback_themes}
    
    def get_daily_theme(self, session_id: Optional[str] = None, force_refresh: bool = True) -> Dict[str, Any]:
        """
        Get theme with TRUE ROTATION - never repeats consecutively
        
        Args:
            session_id: Optional session ID (not used in rotation)
            force_refresh: If True, advances to next theme (default)
            
        Returns:
            Next theme in rotation sequence
        """
        
        if not self.themes_list:
            logger.error("❌ No themes available")
            return self._create_fallback_theme_response()
        
        # Load current rotation state
        state = self._load_theme_state()
        current_index = state.get("current_index", 0)
        
        # Ensure index is valid (handle case where themes.json changed)
        if current_index >= len(self.themes_list):
            current_index = 0
            logger.info(f"🔄 Reset theme index to 0 (was {state.get('current_index')})")
        
        # Get current theme
        selected_theme = self.themes_list[current_index]
        
        if force_refresh:
            # ROTATION LOGIC: Move to next theme
            next_index = (current_index + 1) % len(self.themes_list)
            self._save_theme_state(next_index)
            
            logger.info(f"🔄 ROTATION: Theme {current_index} → Next will be {next_index}")
        
        # Get photo filename for UI
        photo_filename = self._get_photo_filename(selected_theme)
        
        theme_name = selected_theme.get("name", "Unknown")
        logger.info(f"🎯 Theme selected: {theme_name} (index: {current_index})")
        logger.info(f"📷 Photo filename: {photo_filename}")
        
        return {
            "theme_of_the_day": selected_theme,
            "photo_filename": photo_filename,
            "selection_metadata": {
                "date": datetime.now().isoformat(),
                "theme_index": current_index,
                "next_theme_index": (current_index + 1) % len(self.themes_list),
                "total_themes_available": len(self.themes_list),
                "selection_method": "true_rotation",
                "refresh_enabled": force_refresh
            }
        }
    
    def _get_photo_filename(self, theme: Dict[str, Any]) -> str:
        """
        Map theme to photo filename for UI - FIXED for consistency
        
        Args:
            theme: Theme data
            
        Returns:
            Photo filename for UI (e.g. "seasons.png")
        """
        
        theme_id = theme.get("id", "")
        theme_name = theme.get("name", "")
        
        # FIXED: Explicit mapping for known themes to prevent mismatches
        theme_photo_map = {
            "birthday": "birthday.png",
            "family": "family.png", 
            "music": "music.png",
            "food": "food.png",
            "travel": "travel.png",
            "seasons": "seasons.png",
            "holidays": "holidays.png",
            "school": "school.png",
            "pets": "pets.png",
            "memory_lane": "memory_lane.png",
            "hobbies": "hobbies.png",
            "nature": "nature.png"
        }
        
        # Try explicit mapping first
        if theme_id and theme_id.lower() in theme_photo_map:
            filename = theme_photo_map[theme_id.lower()]
        else:
            # Fallback to ID-based mapping
            if theme_id:
                filename = f"{theme_id.lower()}.png"
            else:
                # Last resort: theme name
                clean_name = theme_name.lower().replace(" ", "_").replace("'", "")
                filename = f"{clean_name}.png"
        
        logger.info(f"📷 Theme '{theme_name}' (ID: {theme_id}) → Photo '{filename}'")
        return filename
    
    def get_next_theme_preview(self) -> Optional[str]:
        """Get the name of the next theme in rotation (for debugging)"""
        if not self.themes_list:
            return None
            
        state = self._load_theme_state()
        current_index = state.get("current_index", 0)
        next_index = (current_index + 1) % len(self.themes_list)
        
        if next_index < len(self.themes_list):
            return self.themes_list[next_index].get("name", "Unknown")
        return None
    
    def reset_rotation(self):
        """Reset rotation to start from beginning (for testing)"""
        self._save_theme_state(0)
        logger.info("🔄 Theme rotation reset to beginning")
    
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
                "date": datetime.now().isoformat(),
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

# Global instance for easy import - with rotation enabled by default
simplified_theme_manager = SimplifiedThemeManager()

# Export
__all__ = ["SimplifiedThemeManager", "simplified_theme_manager"]