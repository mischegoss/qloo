"""
Mobile Synthesizer Agent - Clean Dashboard with Theme Integration
File: backend/multi_tool_agent/agents/mobile_synthesizer_agent.py

Agent 6: Returns ONLY the clean dashboard with theme-enhanced content selection
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
    Agent 6: Mobile Synthesizer with Theme Integration
    
    Returns exactly one result per category in a clean response structure.
    NEW: Incorporates daily theme for enhanced content selection and conversation starters.
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
        Create clean dashboard with theme-enhanced content selection.
        
        Returns ONLY the dashboard with theme integration - no raw agent outputs.
        """
        
        try:
            logger.info("📱 Agent 6: Creating theme-aware dashboard (single results only)")
            
            # Extract daily theme (NEW)
            daily_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
            theme_name = daily_theme.get("name", "General")
            
            # DEBUG: Log theme extraction
            logger.info(f"🔍 DEBUG Agent 6: consolidated_info keys: {list(consolidated_info.keys())}")
            logger.info(f"🔍 DEBUG Agent 6: daily_theme structure: {consolidated_info.get('daily_theme', 'MISSING')}")
            logger.info(f"🔍 DEBUG Agent 6: extracted theme name: {theme_name}")
            
            logger.info(f"🎯 Dashboard theme: {theme_name}")
            
            # Set daily random seed for uniqueness (existing logic)
            today = date.today()
            daily_seed = hash(f"{today.year}-{today.month}-{today.day}")
            random.seed(daily_seed)
            
            # Select exactly one result per category with theme awareness (ENHANCED)
            selected_results = self._select_theme_aware_single_results(
                qloo_intelligence, sensory_content, photo_analysis, 
                consolidated_info.get("patient_profile", {}),
                daily_theme  # NEW: Theme-aware selection
            )
            
            # Generate theme-aware conversation starters (NEW)
            if theme_manager and daily_theme:
                try:
                    theme_conversation_starters = theme_manager.get_theme_conversation_starters(
                        daily_theme, selected_results
                    )
                except Exception as e:
                    logger.error(f"Error generating theme conversation starters: {e}")
                    theme_conversation_starters = [
                        "What brings back good memories for you?",
                        "Tell me about something that makes you happy"
                    ]
            else:
                theme_conversation_starters = [
                    "What brings back good memories for you?",
                    "Tell me about something that makes you happy"
                ]
            
            # Create ONLY the clean dashboard with theme integration
            dashboard = {
                "music": selected_results["music"],
                "tv_show": selected_results["tv_show"], 
                "recipe": selected_results["recipe"],
                "photo": selected_results["photo"],
                "conversation_starters": theme_conversation_starters,
                # NEW: Theme information in dashboard
                "theme_of_the_day": {
                    "name": daily_theme.get("name", "General"),
                    "description": daily_theme.get("description", "General daily activities"),
                    "applied_to_content": True,
                    "sensory_focus": theme_manager.get_theme_sensory_focus(daily_theme) if theme_manager and daily_theme else "visual"
                }
            }
            
            logger.info(f"✅ Theme-aware dashboard created: {theme_name} theme with single results")
            
            # Return ONLY the dashboard with theme metadata
            return {
                "dashboard": dashboard,
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "request_type": "dashboard",
                    "results_per_category": 1,
                    "daily_seed": daily_seed,
                    "theme_applied": theme_name,
                    "theme_enhanced_selection": True,
                    "fallbacks_used": selected_results.get("fallbacks_used", []),
                    "response_type": "clean_dashboard_with_theme"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 6 failed: {e}")
            return self._create_fallback_dashboard(consolidated_info)
    
    def _select_theme_aware_single_results(self, 
                                         qloo_intelligence: Dict[str, Any],
                                         sensory_content: Dict[str, Any], 
                                         photo_analysis: Dict[str, Any],
                                         patient_profile: Dict[str, Any],
                                         daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCED: Select exactly ONE result per category with theme awareness.
        
        Args:
            qloo_intelligence: Qloo API results
            sensory_content: Recipe and sensory data
            photo_analysis: Photo analysis results
            patient_profile: Patient information
            daily_theme: Current daily theme configuration
            
        Returns:
            Single selected result per category with theme consideration
        """
        
        results = {}
        fallbacks_used = []
        theme_name = daily_theme.get("name", "General")
        
        # Get content priority with fallback
        if theme_manager and daily_theme:
            try:
                content_priority = theme_manager.get_theme_content_priority(daily_theme)
            except Exception as e:
                logger.warning(f"Error getting theme content priority: {e}")
                content_priority = "places"
        else:
            content_priority = "places"
        
        logger.info(f"🎯 Theme-aware selection for '{theme_name}' with priority on '{content_priority}'")
        
        # MUSIC: Enhanced with theme awareness
        music_result = self._select_theme_aware_music(sensory_content, qloo_intelligence, daily_theme)
        if not music_result:
            music_result = random.choice(self.fallback_data["music"])
            fallbacks_used.append("music")
        results["music"] = music_result
        logger.info(f"Selected music: {music_result.get('song', 'Unknown')} (theme: {theme_name})")
        
        # TV SHOWS: Enhanced with theme awareness  
        tv_result = self._select_theme_aware_tv_show(qloo_intelligence, daily_theme)
        if not tv_result:
            tv_result = random.choice(self.fallback_data["tv_shows"])
            fallbacks_used.append("tv_show")
        results["tv_show"] = tv_result
        logger.info(f"Selected TV show: {tv_result.get('name', 'Unknown')} (theme: {theme_name})")
        
        # RECIPE: Enhanced with theme consideration
        recipe_result = self._select_theme_aware_recipe(sensory_content, daily_theme)
        if not recipe_result:
            recipe_result = {
                "name": "Simple Comfort Recipe",
                "total_time": "15 minutes",
                "ingredients": ["Basic ingredients"],
                "instructions": ["Simple preparation steps"],
                "theme_connection": f"Selected for {theme_name} theme"
            }
            fallbacks_used.append("recipe")
        results["recipe"] = recipe_result
        logger.info(f"Selected recipe: {recipe_result.get('name', 'Unknown')} (theme: {theme_name})")
        
        # PHOTO: Existing logic (could be enhanced with theme in future)
        photo_result = self._select_single_photo(photo_analysis, patient_profile)
        results["photo"] = photo_result
        
        results["fallbacks_used"] = fallbacks_used
        return results
    
    def _select_theme_aware_music(self, 
                                sensory_content: Dict[str, Any],
                                qloo_intelligence: Dict[str, Any],
                                daily_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        ENHANCED: Select music with theme awareness.
        
        Args:
            sensory_content: Sensory content from Agent 4
            qloo_intelligence: Qloo results from Agent 3
            daily_theme: Current theme configuration
            
        Returns:
            Single music selection with theme consideration
        """
        
        # Try to get music from Qloo results first
        qloo_artists = self._get_english_filtered_qloo_results(
            qloo_intelligence, "cultural_recommendations", "artists"
        )
        
        # If theme prioritizes music content, prefer Qloo artists
        theme_priority = theme_manager.get_theme_content_priority(daily_theme) if daily_theme else "places"
        
        if qloo_artists and (theme_priority == "artists" or daily_theme.get("name") == "Music"):
            # Select first English artist from Qloo for theme-appropriate music
            artist_data = qloo_artists[0]
            return {
                "artist": artist_data.get("name", "Unknown Artist"),
                "song": "Popular song",  # Could be enhanced with specific song lookup
                "youtube_url": "",
                "theme_selected": True,
                "source": "qloo_theme_priority"
            }
        
        # Fallback to general music selection
        return self._select_single_music(sensory_content)
    
    def _select_theme_aware_tv_show(self,
                                  qloo_intelligence: Dict[str, Any],
                                  daily_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        ENHANCED: Select TV show with theme awareness.
        
        Args:
            qloo_intelligence: Qloo results from Agent 3
            daily_theme: Current theme configuration
            
        Returns:
            Single TV show selection with theme consideration
        """
        
        # Get English-filtered TV shows from Qloo
        qloo_tv_shows = self._get_english_filtered_qloo_results(
            qloo_intelligence, "cultural_recommendations", "tv_shows"
        )
        
        if not qloo_tv_shows:
            return None
        
        # Theme-aware selection logic
        theme_name = daily_theme.get("name", "General")
        
        # Get theme priority with fallback
        if theme_manager and daily_theme:
            try:
                theme_priority = theme_manager.get_theme_content_priority(daily_theme)
            except Exception as e:
                logger.warning(f"Error getting theme priority: {e}")
                theme_priority = "places"
        else:
            theme_priority = "places"
        
        # If theme emphasizes visual content, prioritize TV shows
        if theme_priority == "tv_shows" or theme_name in ["Movies", "Childhood", "Family"]:
            # Select the first available TV show for theme relevance
            selected_show = qloo_tv_shows[0]
            logger.info(f"Theme-prioritized TV show selection for '{theme_name}'")
        else:
            # Random selection from available shows
            selected_show = random.choice(qloo_tv_shows)
        
        return {
            "name": selected_show.get("name", "Classic TV Show"),
            "description": selected_show.get("description", "Nostalgic television program"),
            "youtube_url": "",  # Could be enhanced with YouTube search
            "theme_selected": theme_priority == "tv_shows",
            "source": "qloo_theme_aware"
        }
    
    def _select_theme_aware_recipe(self,
                                 sensory_content: Dict[str, Any],
                                 daily_theme: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        ENHANCED: Select recipe with theme consideration.
        
        Args:
            sensory_content: Sensory content including theme-filtered recipes
            daily_theme: Current theme configuration
            
        Returns:
            Single recipe selection with theme context
        """
        
        # DEBUG: Log sensory_content structure to understand the data format
        logger.info(f"🔍 DEBUG: sensory_content keys: {list(sensory_content.keys())}")
        if sensory_content.get("sensory_content"):
            logger.info(f"🔍 DEBUG: inner sensory_content keys: {list(sensory_content['sensory_content'].keys())}")
        
        # Try multiple possible paths where recipes might be stored
        recipes_data = None
        
        # Path 1: sensory_content.sensory_content.recipes (most likely)
        if sensory_content.get("sensory_content", {}).get("recipes"):
            recipes_data = sensory_content["sensory_content"]["recipes"]
            logger.info(f"🔍 DEBUG: Found recipes via path 1: {len(recipes_data)} recipes")
        
        # Path 2: sensory_content.recipes (alternative)
        elif sensory_content.get("recipes"):
            recipes_data = sensory_content["recipes"]
            logger.info(f"🔍 DEBUG: Found recipes via path 2: {len(recipes_data)} recipes")
        
        # Path 3: Check for gustatory content
        elif sensory_content.get("sensory_content", {}).get("content_by_sense", {}).get("gustatory"):
            gustatory_content = sensory_content["sensory_content"]["content_by_sense"]["gustatory"]
            if isinstance(gustatory_content, dict) and gustatory_content.get("recipes"):
                recipes_data = gustatory_content["recipes"]
                logger.info(f"🔍 DEBUG: Found recipes via path 3 (gustatory): {len(recipes_data)} recipes")
        
        if not recipes_data:
            logger.warning("🔍 DEBUG: No recipes found in sensory_content - using fallback")
            return None
        
        # Select first recipe (Agent 4 already did theme filtering and prioritization)
        selected_recipe = recipes_data[0]
        
        # Ensure theme connection is included
        theme_name = daily_theme.get("name", "General")
        if not selected_recipe.get("theme_connection"):
            selected_recipe["theme_connection"] = f"Selected for {theme_name} theme"
        
        logger.info(f"🎯 SUCCESS: Selected theme-filtered recipe: {selected_recipe.get('name', 'Unknown')}")
        
        # Format for dashboard
        return {
            "name": selected_recipe.get("name", "Comfort Recipe"),
            "total_time": self._estimate_recipe_time(selected_recipe),
            "ingredients": selected_recipe.get("ingredients", []),
            "instructions": selected_recipe.get("instructions", []),
            "nostalgic_description": selected_recipe.get("nostalgic_description", ""),
            "theme_connection": selected_recipe.get("theme_connection", ""),
            "youtube_url": selected_recipe.get("youtube_url", ""),
            "theme_selected": True,
            "source": "sensory_content_theme_filtered"
        }
    
    def _estimate_recipe_time(self, recipe: Dict[str, Any]) -> str:
        """Estimate total time for a recipe"""
        # Look for time indicators in instructions
        instructions = recipe.get("instructions", [])
        if any("microwave" in str(inst).lower() for inst in instructions):
            return "5-10 minutes"
        elif any("mix" in str(inst).lower() and "serve" in str(inst).lower() for inst in instructions):
            return "5 minutes"
        else:
            return "10-15 minutes"
    
    def _select_single_music(self, sensory_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select one music result from sensory content (existing logic with minor enhancements)."""
        
        # This is the existing logic - kept for compatibility
        try:
            # Try to extract music from sensory content
            # (This would need to be implemented based on actual sensory content structure)
            return None
        except Exception as e:
            logger.warning(f"Error selecting music from sensory content: {e}")
            return None
    
    def _select_single_photo(self, 
                           photo_analysis: Dict[str, Any], 
                           patient_profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select one photo result (existing logic)."""
        
        if not photo_analysis or photo_analysis.get("status") == "skipped":
            return None
        
        try:
            # Extract photo information
            photo_data = photo_analysis.get("photo_analysis", {})
            if photo_data and photo_data.get("available"):
                return {
                    "description": photo_data.get("description", "Personal photo"),
                    "emotional_context": photo_data.get("emotional_context", ""),
                    "conversation_starters": photo_data.get("conversation_starters", []),
                    "available": True,
                    "source": "photo_analysis"
                }
        except Exception as e:
            logger.warning(f"Error selecting photo: {e}")
        
        return None
    
    def _get_english_filtered_qloo_results(self, 
                                         qloo_intelligence: Dict[str, Any],
                                         category: str,
                                         subcategory: str) -> List[Dict[str, Any]]:
        """Extract English-filtered results from Qloo intelligence (existing helper method)."""
        
        try:
            results = qloo_intelligence.get("qloo_intelligence", {}).get(category, {}).get(subcategory, {})
            if results.get("available") and results.get("entities"):
                return results["entities"]
        except Exception as e:
            logger.warning(f"Error extracting Qloo results for {subcategory}: {e}")
        
        return []
    
    def _create_fallback_dashboard(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback dashboard if main processing fails."""
        
        logger.warning("Creating fallback dashboard with theme information")
        
        # Extract theme for fallback
        daily_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
        theme_name = daily_theme.get("name", "Comfort")
        
        # Create simple fallback dashboard
        fallback_dashboard = {
            "music": {"artist": "Frank Sinatra", "song": "My Way", "youtube_url": ""},
            "tv_show": {"name": "I Love Lucy", "description": "Classic comedy", "youtube_url": ""},
            "recipe": {
                "name": "Warm Comfort Food",
                "ingredients": ["Simple ingredients"],
                "instructions": ["Easy preparation"],
                "theme_connection": f"Selected for {theme_name} theme"
            },
            "photo": None,
            "conversation_starters": [
                f"Let's talk about {theme_name.lower()}",
                "What brings back good memories for you?",
                "Tell me about something that makes you happy"
            ],
            "theme_of_the_day": {
                "name": theme_name,
                "description": daily_theme.get("description", "Daily comfort activities"),
                "applied_to_content": False,
                "sensory_focus": "comfort"
            }
        }
        
        return {
            "dashboard": fallback_dashboard,
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "request_type": "dashboard",
                "results_per_category": 1,
                "theme_applied": theme_name,
                "fallback_used": True,
                "response_type": "fallback_dashboard_with_theme"
            }
        }