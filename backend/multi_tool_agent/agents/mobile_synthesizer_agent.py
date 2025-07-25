"""
Mobile Synthesizer Agent - Clean Dashboard with Theme Integration - FIXED
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

Agent 6: Returns ONLY the clean dashboard with theme-enhanced content selection
FIXES: 
- Fixed recipe data structure path (gustatory.elements instead of gustatory.recipes)
- Enhanced error handling for data structure mismatches
"""

import logging
import json
import os
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger FIRST
logger = logging.getLogger(__name__)

# Import theme manager for theme-aware functionality (FIXED import path)
try:
    # Try direct import path first (working path)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Mobile Synthesizer: theme_manager imported successfully")
    logger.info(f"🔍 DEBUG: theme_manager object: {theme_manager}")
except ImportError as e:
    logger.error(f"❌ Mobile Synthesizer: Failed to import theme_manager: {e}")
    theme_manager = None
except Exception as e:
    logger.error(f"❌ Mobile Synthesizer: Error with theme_manager: {e}")
    theme_manager = None

class MobileSynthesizerAgent:
    """
    Agent 6: Mobile Synthesizer with Theme Integration - FIXED
    
    Returns exactly one result per category in a clean response structure.
    NEW: Incorporates daily theme for enhanced content selection and conversation starters.
    FIXED: Correctly parses recipe data structure from Agent 4 + proper method signature
    """
    
    def __init__(self):
        self.fallback_data = self._load_fallback_content()
        logger.info("Mobile Synthesizer initialized with theme-aware content selection")
    
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
            "music": [
                {"artist": "Frank Sinatra", "song": "My Way", "youtube_url": "https://youtube.com/watch?v=qQzdAsjWGPg"},
                {"artist": "Ella Fitzgerald", "song": "Summertime", "youtube_url": "https://youtube.com/watch?v=MIDOmSQN6LU"}
            ],
            "tv_shows": [
                {"name": "I Love Lucy", "youtube_url": "https://youtube.com/watch?v=example1", "description": "Classic 1950s comedy"},
                {"name": "The Ed Sullivan Show", "youtube_url": "https://youtube.com/watch?v=example2", "description": "Variety show from the 1960s"}
            ],
            "conversation_starters": [
                "What was your favorite song when you were young?",
                "Tell me about TV shows your family watched together",
                "What foods remind you of home?"
            ]
        }
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any],
                  sensory_content: Dict[str, Any],
                  photo_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean dashboard synthesis with FIXED recipe data parsing.
        
        Args:
            consolidated_info: Consolidated information including patient profile and daily theme
            cultural_profile: Cultural profile data
            qloo_intelligence: Qloo API results
            sensory_content: Recipe and sensory data (FIXED parsing)
            photo_analysis: Photo analysis results
            
        Returns:
            Single selected result per category with theme consideration
        """
        
        # Extract data from consolidated_info
        patient_profile = consolidated_info.get("patient_profile", {})
        daily_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
        
        results = {}
        fallbacks_used = []
        theme_name = daily_theme.get("name", "General")
        
        # Get content priority with fallback
        content_priority = "places"  # Default fallback
        if theme_manager and daily_theme:
            try:
                if hasattr(theme_manager, 'get_theme_content_priority'):
                    content_priority = theme_manager.get_theme_content_priority(daily_theme)
                else:
                    logger.warning("theme_manager does not have get_theme_content_priority method")
            except Exception as e:
                logger.warning(f"Error getting theme content priority: {e}")
        else:
            logger.info("No theme_manager or daily_theme available, using default content priority")
        
        logger.info(f"🎯 Theme-aware selection for '{theme_name}' with priority on '{content_priority}'")
        
        # DEBUG: Log theme extraction path  
        logger.info(f"🔍 DEBUG: consolidated_info keys: {list(consolidated_info.keys())}")
        logger.info(f"🔍 DEBUG: daily_theme structure: {consolidated_info.get('daily_theme', 'MISSING')}")
        logger.info(f"🔍 DEBUG: extracted theme: {daily_theme}")
        
        # MUSIC: Enhanced with theme awareness
        try:
            music_result = self._select_theme_aware_music(sensory_content, qloo_intelligence, daily_theme)
        except Exception as e:
            logger.error(f"Error in theme-aware music selection: {e}")
            music_result = None
        
        if not music_result:
            music_result = random.choice(self.fallback_data["music"])
            fallbacks_used.append("music")
        results["music"] = music_result
        logger.info(f"Selected music: {music_result.get('song', 'Unknown')} (theme: {theme_name})")
        
        # TV SHOWS: Enhanced with theme awareness  
        try:
            tv_result = self._select_theme_aware_tv_show(qloo_intelligence, daily_theme)
        except Exception as e:
            logger.error(f"Error in theme-aware TV show selection: {e}")
            tv_result = None
            
        if not tv_result:
            tv_result = random.choice(self.fallback_data["tv_shows"])
            fallbacks_used.append("tv_show")
        results["tv_show"] = tv_result
        logger.info(f"Selected TV show: {tv_result.get('name', 'Unknown')} (theme: {theme_name})")
        
        # RECIPE: Enhanced with theme consideration - FIXED DATA STRUCTURE
        try:
            recipe_result = self._select_theme_aware_recipe_FIXED(sensory_content, daily_theme)
        except Exception as e:
            logger.error(f"Error in FIXED recipe selection: {e}")
            recipe_result = None
            
        if not recipe_result:
            recipe_result = {
                "name": "Simple Comfort Recipe",
                "total_time": "15 minutes",
                "ingredients": ["Simple ingredients"],
                "instructions": ["Easy preparation"],
                "nostalgic_description": "Comforting home-style cooking",
                "theme_connection": f"Perfect for {theme_name} theme",
                "theme_selected": False,
                "source": "fallback"
            }
            fallbacks_used.append("recipe")
        results["recipe"] = recipe_result
        logger.info(f"Selected recipe: {recipe_result.get('name', 'Unknown')} (theme: {theme_name})")
        
        # CONVERSATION: Theme-enhanced conversation starters
        try:
            conversation_result = self._select_theme_aware_conversation(daily_theme, patient_profile)
        except Exception as e:
            logger.error(f"Error in theme-aware conversation selection: {e}")
            conversation_result = "What brings back good memories for you?"
            
        results["conversation_starter"] = conversation_result
        logger.info(f"Selected conversation: {conversation_result[:50]}... (theme: {theme_name})")
        
        # PHOTO: Keep existing logic but theme-enhance
        try:
            photo_result = self._select_single_photo(photo_analysis, patient_profile)
        except Exception as e:
            logger.error(f"Error in photo selection: {e}")
            photo_result = None
            
        if photo_result:
            results["photo"] = photo_result
            logger.info(f"Selected photo: {photo_result.get('title', 'Unknown')}")
        
        # Dashboard metadata with theme info
        dashboard_metadata = {
            "theme": {
                "name": theme_name,
                "content_priority": content_priority,
                "theme_applied": True
            },
            "fallbacks_used": fallbacks_used,
            "total_fallbacks": len(fallbacks_used),
            "content_quality": "high" if len(fallbacks_used) == 0 else "mixed",
            "generation_timestamp": datetime.now().isoformat()
        }
        
        return {
            "mobile_experience": {
                "dashboard_content": results,
                "dashboard_metadata": dashboard_metadata
            }
        }
    
    def _select_theme_aware_recipe_FIXED(self, 
                                       sensory_content: Dict[str, Any], 
                                       daily_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        FIXED: Select theme-aware recipe with correct data structure parsing.
        
        Args:
            sensory_content: Sensory content including theme-filtered recipes
            daily_theme: Current theme configuration
            
        Returns:
            Single recipe selection with theme context
        """
        
        # DEBUG: Log sensory_content structure to understand the data format
        logger.info(f"🔍 DEBUG: sensory_content keys: {list(sensory_content.keys())}")
        if sensory_content.get("content_by_sense"):
            logger.info(f"🔍 DEBUG: content_by_sense keys: {list(sensory_content['content_by_sense'].keys())}")
            if sensory_content.get("content_by_sense", {}).get("gustatory"):
                gustatory = sensory_content["content_by_sense"]["gustatory"]
                logger.info(f"🔍 DEBUG: gustatory keys: {list(gustatory.keys()) if isinstance(gustatory, dict) else 'not a dict'}")
                if isinstance(gustatory, dict) and gustatory.get("elements"):
                    logger.info(f"🔍 DEBUG: gustatory.elements count: {len(gustatory['elements'])}")
        
        # Try multiple possible paths where recipes might be stored - CORRECTED PATHS
        recipe_data = None
        
        # Path 1: sensory_content.content_by_sense.gustatory.elements (CORRECTED - no double nesting)
        try:
            gustatory_content = sensory_content.get("content_by_sense", {}).get("gustatory")
            if isinstance(gustatory_content, dict) and gustatory_content.get("elements"):
                recipe_elements = gustatory_content["elements"]
                if recipe_elements and len(recipe_elements) > 0:
                    recipe_data = recipe_elements[0]  # Take first element
                    logger.info(f"🔍 SUCCESS: Found recipe via CORRECTED path (content_by_sense.gustatory.elements): {recipe_data.get('name', 'Unknown')}")
        except Exception as e:
            logger.warning(f"Error parsing gustatory elements: {e}")
        
        # Path 2: Legacy fallback paths (kept for compatibility)
        if not recipe_data:
            # Check sensory_content.recipes (direct)
            if sensory_content.get("recipes"):
                recipes_data = sensory_content["recipes"]
                recipe_data = recipes_data[0] if recipes_data else None
                logger.info(f"🔍 DEBUG: Found recipes via legacy direct path: {recipe_data.get('name', 'Unknown') if recipe_data else 'None'}")
        
        # Path 3: Check for nested sensory_content (legacy)
        if not recipe_data:
            if sensory_content.get("sensory_content", {}).get("content_by_sense", {}).get("gustatory"):
                gustatory_content = sensory_content["sensory_content"]["content_by_sense"]["gustatory"]
                if isinstance(gustatory_content, dict) and gustatory_content.get("elements"):
                    recipe_elements = gustatory_content["elements"]
                    if recipe_elements and len(recipe_elements) > 0:
                        recipe_data = recipe_elements[0]
                        logger.info(f"🔍 DEBUG: Found recipes via legacy nested path: {recipe_data.get('name', 'Unknown')}")
        
        if not recipe_data:
            logger.warning("🔍 WARNING: No recipes found in sensory_content - using fallback")
            return None
        
        # Ensure theme connection is included
        theme_name = daily_theme.get("name", "General")
        if not recipe_data.get("theme_connection"):
            recipe_data["theme_connection"] = f"Selected for {theme_name} theme"
        
        logger.info(f"🎯 SUCCESS: Selected theme-filtered recipe: {recipe_data.get('name', 'Unknown')}")
        
        # Format for dashboard - NORMALIZED STRUCTURE
        return {
            "name": recipe_data.get("name", "Comfort Recipe"),
            "total_time": self._estimate_recipe_time(recipe_data),
            "ingredients": recipe_data.get("ingredients", []),
            "instructions": recipe_data.get("instructions", []),
            "nostalgic_description": recipe_data.get("description", recipe_data.get("heritage_connection", "")),
            "theme_connection": recipe_data.get("theme_connection", ""),
            "youtube_url": recipe_data.get("youtube_url", ""),
            "cultural_context": recipe_data.get("cultural_context", ""),
            "theme_selected": True,
            "source": "sensory_content_theme_filtered"
        }
    
    def _estimate_recipe_time(self, recipe: Dict[str, Any]) -> str:
        """Estimate total time for a recipe"""
        # Look for existing time info first
        if recipe.get("total_time"):
            return recipe["total_time"]
        
        # Look for time indicators in instructions
        instructions = recipe.get("instructions", [])
        if any("microwave" in str(inst).lower() for inst in instructions):
            return "5-10 minutes"
        elif any("mix" in str(inst).lower() and "serve" in str(inst).lower() for inst in instructions):
            return "5 minutes"
        else:
            return "10-15 minutes"
    
    def _select_theme_aware_music(self, 
                                sensory_content: Dict[str, Any], 
                                qloo_intelligence: Dict[str, Any], 
                                daily_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select theme-aware music with enhanced logic."""
        
        try:
            # Try to get music from sensory content first
            auditory_content = sensory_content.get("sensory_content", {}).get("content_by_sense", {}).get("auditory")
            if auditory_content and auditory_content.get("elements"):
                music_elements = auditory_content["elements"]
                if music_elements:
                    music_data = music_elements[0]
                    theme_name = daily_theme.get("name", "General")
                    
                    return {
                        "artist": music_data.get("artist", "Unknown Artist"),
                        "song": music_data.get("title", music_data.get("song", "Unknown Song")),
                        "youtube_url": music_data.get("youtube_url", ""),
                        "description": music_data.get("description", ""),
                        "theme_connection": f"Selected for {theme_name} theme",
                        "source": "sensory_content"
                    }
            
            # Fallback to Qloo intelligence
            qloo_artists = qloo_intelligence.get("cultural_recommendations", {}).get("artists", {})
            if qloo_artists.get("available") and qloo_artists.get("entities"):
                artist_data = qloo_artists["entities"][0]
                return {
                    "artist": artist_data.get("name", "Unknown Artist"),
                    "song": "Classic Hit",
                    "youtube_url": "",
                    "description": f"Music by {artist_data.get('name', 'Unknown Artist')}",
                    "theme_connection": f"Cultural match for {daily_theme.get('name', 'General')} theme",
                    "source": "qloo_intelligence"
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error selecting theme-aware music: {e}")
            return None
    
    def _select_theme_aware_tv_show(self, 
                                  qloo_intelligence: Dict[str, Any], 
                                  daily_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select theme-aware TV show."""
        
        try:
            qloo_tv = qloo_intelligence.get("cultural_recommendations", {}).get("tv_shows", {})
            if qloo_tv.get("available") and qloo_tv.get("entities"):
                tv_data = qloo_tv["entities"][0]
                theme_name = daily_theme.get("name", "General")
                
                return {
                    "name": tv_data.get("name", "Classic TV Show"),
                    "description": tv_data.get("description", f"Entertainment from the era"),
                    "youtube_url": tv_data.get("youtube_url", ""),
                    "theme_connection": f"Perfect viewing for {theme_name} theme",
                    "source": "qloo_intelligence"
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error selecting theme-aware TV show: {e}")
            return None
    
    def _select_theme_aware_conversation(self, 
                                       daily_theme: Dict[str, Any], 
                                       patient_profile: Dict[str, Any]) -> str:
        """Generate SIMPLE theme-aware conversation starter for dementia care."""
        
        theme_name = daily_theme.get("name", "General")
        
        # SIMPLE theme-specific conversation starters (5-8 words max)
        theme_conversations = {
            "Memory Lane": [
                "What do you remember?",
                "Tell me about the old days.",
                "What made you happy then?"
            ],
            "Cultural Heritage": [
                "What was your family like?",
                "Tell me about your home.",
                "What did you celebrate?"
            ],
            "Family Traditions": [
                "What did your family do together?",
                "Tell me about family dinners.",
                "What holidays did you like?"
            ],
            "Music": [
                "What music do you like?",
                "Did you like to dance?",
                "What songs do you remember?"
            ],
            "Clothing": [
                "What did you like to wear?",
                "Did you have pretty clothes?",
                "What was your favorite outfit?"
            ],
            "Family": [
                "Tell me about your family.",
                "Who do you love?",
                "What makes you smile?"
            ]
        }
        
        # Simple fallback conversations
        conversations = theme_conversations.get(theme_name, [
            "What makes you happy?",
            "Tell me something nice.",
            "What do you like?"
        ])
        
        return random.choice(conversations)
    
    def _select_single_photo(self, 
                           photo_analysis: Dict[str, Any], 
                           patient_profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select one photo result (existing logic)."""
        
        try:
            if not photo_analysis or not photo_analysis.get("photos"):
                return None
            
            photos = photo_analysis["photos"]
            if not photos:
                return None
            
            # Select first available photo
            selected_photo = photos[0]
            
            return {
                "title": selected_photo.get("title", "Photo of the Day"),
                "description": selected_photo.get("description", "A meaningful moment"),
                "cultural_context": selected_photo.get("cultural_context", ""),
                "conversation_starter": selected_photo.get("conversation_starter", "Tell me about this photo"),
                "source": "photo_analysis"
            }
            
        except Exception as e:
            logger.error(f"Error selecting photo: {e}")
            return None