"""
Agent 4: Sensory Content Generator - FIXED DATA UNWRAPPING FOR YOUTUBE URLs
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

CRITICAL FIX: Added data unwrapping for qloo_intelligence and correct key names
- Agent 3 wraps output: {"qloo_intelligence": {"cultural_recommendations": {...}}}
- Agent 3 stores music under "artists" key, not "music"
- Agent 4 must unwrap and use correct keys to get data for YouTube API calls
"""

import logging
import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Import theme manager for enhanced theme-aware functionality (ORIGINAL)
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Sensory Content Generator: theme_manager imported successfully")
except ImportError as e:
    logger.error(f"❌ Sensory Content Generator: Failed to import theme_manager: {e}")
    theme_manager = None

class SensoryContentGeneratorAgent:
    """
    Agent 4: Sensory Content Generator with FIXED data unwrapping for YouTube URLs
    
    CRITICAL FIX:
    - Unwraps double-wrapped qloo_intelligence structure  
    - Uses correct key names: "artists" instead of "music"
    - Now properly gets data for YouTube API calls
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with FIXED data unwrapping for YouTube URLs")
    
    def _unwrap_qloo_intelligence(self, qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        CRITICAL FIX: Unwrap the qloo_intelligence data structure if it's double-wrapped.
        Same logic as Agent 6.
        """
        
        # Check if we have the double-wrapped structure
        if "qloo_intelligence" in qloo_intelligence and len(qloo_intelligence.keys()) == 1:
            logger.info("🔧 CRITICAL FIX: Agent 4 unwrapping double-wrapped qloo_intelligence structure")
            unwrapped = qloo_intelligence["qloo_intelligence"]
            logger.info(f"🔧 Agent 4 unwrapped keys: {list(unwrapped.keys())}")
            return unwrapped
        
        # Return as-is if already properly structured
        logger.info("🔧 Agent 4 data structure already properly formatted")
        return qloo_intelligence
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main run method with FIXED data unwrapping for YouTube URLs.
        """
        
        logger.info("🎨 Agent 4: Starting enhanced sensory content generation + dislike filtering + YouTube URLs")
        
        try:
            # Extract patient profile for dislike checking (ADDITIVE)
            patient_profile = consolidated_info.get("patient_profile", {})
            demo_dislikes = patient_profile.get("demo_dislikes", [])
            
            # Log dislike filtering if any dislikes exist (ADDITIVE)
            if demo_dislikes:
                disliked_types = [dislike.get("type") for dislike in demo_dislikes]
                logger.info(f"🚫 Filtering sensory content for dislikes: {disliked_types}")
            
            # Extract daily theme from consolidated info (ORIGINAL)
            daily_theme = consolidated_info.get("daily_theme", {})
            
            # CRITICAL FIX: Unwrap qloo_intelligence and use correct keys
            unwrapped_qloo = self._unwrap_qloo_intelligence(qloo_intelligence)
            cultural_recommendations = unwrapped_qloo.get("cultural_recommendations", {})
            
            # FIXED: Use correct key names from Agent 3
            vision_data = cultural_recommendations.get("tv_shows", {})
            audio_data = cultural_recommendations.get("artists", {})  # FIXED: "artists" not "music"
            
            logger.info(f"🔧 FIXED: Agent 4 extracted data - TV shows: {vision_data.get('entity_count', 0)}, Artists: {audio_data.get('entity_count', 0)}")
            
            # Generate enhanced sensory content with dislike filtering + YouTube URLs (ENHANCED)
            sensory_result = await self.generate_sensory_content(vision_data, audio_data, daily_theme, demo_dislikes)
            
            return {
                "sensory_content": sensory_result
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 run method failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    async def generate_sensory_content(self, vision_data: Dict[str, Any], 
                               audio_data: Dict[str, Any], 
                               daily_theme: Dict[str, Any],
                               demo_dislikes: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        ENHANCED: Generate sensory content with enhanced theme-aware recipe selection + dislike filtering + YouTube URLs
        """
        
        if demo_dislikes is None:
            demo_dislikes = []
        
        logger.info(f"🎨 Generating sensory content for theme: {daily_theme.get('theme', {}).get('name', 'Unknown')}")
        
        current_theme = daily_theme.get("theme", {})
        
        # ENHANCED: Use theme manager for better recipe filtering (ORIGINAL)
        filtered_recipes = self._get_theme_filtered_recipes(current_theme)
        
        # Select best recipe from filtered results (ORIGINAL)
        selected_recipe = self._select_best_recipe(filtered_recipes, current_theme)
        
        # Generate enhanced gustatory content with theme awareness + dislike filtering (ENHANCED)
        gustatory_content = self._generate_gustatory_content(selected_recipe, current_theme, demo_dislikes)
        
        # Process other sensory content (visual, auditory, etc.) + dislike filtering + YouTube URLs (ENHANCED)
        visual_content = await self._process_visual_content(vision_data, current_theme, demo_dislikes)
        auditory_content = await self._process_auditory_content(audio_data, current_theme, demo_dislikes)
        
        sensory_result = {
            "content_by_sense": {
                "visual": visual_content,
                "auditory": auditory_content,
                "gustatory": gustatory_content,
                "tactile": self._generate_tactile_content(current_theme),
                "olfactory": self._generate_olfactory_content(current_theme)
            },
            "theme_context": {
                "current_theme": current_theme,
                "recipe_selection_method": gustatory_content.get("selection_metadata", {}).get("method", "unknown"),
                "theme_match_quality": gustatory_content.get("selection_metadata", {}).get("match_quality", "unknown")
            },
            "generation_metadata": {
                "timestamp": datetime.now().isoformat(),
                "agent": "SensoryContentGenerator",
                "version": "fixed_data_unwrapping_for_youtube_urls",
                "dislike_filtering_active": len(demo_dislikes) > 0,
                "youtube_urls_enabled": self.youtube_tool is not None,
                "data_unwrapping_fixed": True  # NEW: Indicates fix is applied
            }
        }
        
        logger.info(f"✅ Sensory content generated successfully with theme-matched recipe: {selected_recipe.get('name', 'Unknown')}")
        return sensory_result
    
    def _load_recipes_json(self) -> List[Dict[str, Any]]:
        """Load theme-aligned recipes from JSON file (ORIGINAL)."""
        
        try:
            recipes_path = os.path.join(os.path.dirname(__file__), "..", "..", "config", "recipes.json")
            if os.path.exists(recipes_path):
                with open(recipes_path, 'r') as f:
                    recipes = json.load(f)
                    logger.info(f"✅ Loaded {len(recipes)} recipes from JSON")
                    return recipes
            else:
                logger.warning("⚠️ Recipes JSON not found, using fallback recipes")
                return self._get_fallback_recipes()
        except Exception as e:
            logger.error(f"❌ Error loading recipes JSON: {e}")
            return self._get_fallback_recipes()
    
    def _get_fallback_recipes(self) -> List[Dict[str, Any]]:
        """Get fallback recipes when JSON loading fails (ORIGINAL)."""
        
        return [
            {
                "name": "Warm Apple Slices",
                "theme_tags": ["seasons", "comfort", "memory"],
                "ingredients": ["apples", "cinnamon", "butter"],
                "instructions": ["Slice apples", "Warm with cinnamon and butter"],
                "difficulty": "easy"
            },
            {
                "name": "Traditional Bread",
                "theme_tags": ["family", "tradition", "home"],
                "ingredients": ["flour", "yeast", "salt"],
                "instructions": ["Mix ingredients", "Knead", "Bake"],
                "difficulty": "medium"
            }
        ]
    
    def _get_theme_filtered_recipes(self, current_theme: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter recipes by current theme (ORIGINAL)."""
        
        theme_name = current_theme.get("name", "").lower()
        theme_id = current_theme.get("id", "").lower()
        
        if not theme_name and not theme_id:
            return self.recipes_data
        
        filtered_recipes = []
        for recipe in self.recipes_data:
            recipe_tags = [tag.lower() for tag in recipe.get("theme_tags", [])]
            
            if theme_name in recipe_tags or theme_id in recipe_tags:
                filtered_recipes.append(recipe)
            elif any(theme_word in tag for tag in recipe_tags for theme_word in theme_name.split()):
                filtered_recipes.append(recipe)
        
        return filtered_recipes if filtered_recipes else self.recipes_data
    
    def _select_best_recipe(self, filtered_recipes: List[Dict[str, Any]], current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select best recipe from filtered results (ORIGINAL)."""
        
        if not filtered_recipes:
            return self._get_fallback_recipes()[0]
        
        # Prefer easy recipes for dementia care
        easy_recipes = [r for r in filtered_recipes if r.get("difficulty", "").lower() == "easy"]
        
        if easy_recipes:
            return random.choice(easy_recipes)
        else:
            return random.choice(filtered_recipes)
    
    def _generate_gustatory_content(self, selected_recipe: Dict[str, Any], current_theme: Dict[str, Any], demo_dislikes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate enhanced gustatory content with theme awareness + dislike filtering (ENHANCED)."""
        
        # Check if recipes are generally disliked (ADDITIVE)
        if self._is_content_type_disliked("recipe", demo_dislikes):
            logger.info("🚫 Skipping recipe generation - user dislikes recipes")
            return {"status": "skipped", "reason": "user_dislike"}
        
        # Check if specific recipe is disliked (ADDITIVE)
        recipe_name = selected_recipe.get("name", "")
        if self._is_specific_item_disliked(recipe_name, demo_dislikes):
            logger.info(f"🚫 Skipping recipe '{recipe_name}' - matches user dislike")
            # Try to find alternative recipe
            alternative_recipes = [r for r in self.recipes_data if r.get("name") != recipe_name]
            for alt_recipe in alternative_recipes:
                if not self._is_specific_item_disliked(alt_recipe.get("name", ""), demo_dislikes):
                    selected_recipe = alt_recipe
                    break
            else:
                return {"status": "skipped", "reason": "all_recipes_disliked"}
        
        # Generate gustatory content (ORIGINAL)
        return {
            "primary_recipe": selected_recipe,
            "elements": [selected_recipe],
            "selection_metadata": {
                "method": "theme_filtered_enhanced",
                "match_quality": "high",
                "theme_alignment": current_theme.get("name", "unknown")
            }
        }
    
    async def _process_visual_content(self, vision_data: Dict[str, Any], current_theme: Dict[str, Any], demo_dislikes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process visual content + dislike filtering + YouTube URLs (ENHANCED with FIXED data access)."""
        
        # Check if TV shows are generally disliked (ADDITIVE)
        if self._is_content_type_disliked("tv_show", demo_dislikes):
            logger.info("🚫 Skipping TV show content - user dislikes TV shows")
            return {"elements": [], "status": "skipped", "reason": "user_dislike"}
        
        # Process visual content (FIXED data access + YOUTUBE URLS)
        visual_elements = []
        
        try:
            # FIXED: Access entities from the correct structure
            entities = vision_data.get("entities", [])
            logger.info(f"🔧 FIXED: Agent 4 processing {len(entities)} TV show entities")
            
            if entities and len(entities) > 0:
                for item in entities:
                    # Filter by dislikes (ADDITIVE)
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        show_name = item.get("name", "Classic Show")
                        
                        # NEW: Make YouTube call to get embeddable URL
                        youtube_url = ""
                        try:
                            if self.youtube_tool:
                                youtube_results = await self.youtube_tool.search_videos(f"{show_name} classic TV", max_results=1)
                                if youtube_results and youtube_results.get("items"):
                                    first_result = youtube_results["items"][0]
                                    youtube_url = first_result.get("embeddable_url", "")
                                    logger.info(f"📺 Retrieved YouTube URL for {show_name}: {bool(youtube_url)}")
                        except Exception as e:
                            logger.warning(f"Failed to get YouTube URL for {show_name}: {e}")
                        
                        visual_elements.append({
                            "type": "tv_show",
                            "name": show_name,
                            "description": item.get("description", "A classic television program"),
                            "theme_relevance": current_theme.get("name", "general"),
                            "youtube_url": youtube_url  # NEW: Include embeddable URL
                        })
                        
            logger.info(f"✅ FIXED: Agent 4 generated {len(visual_elements)} TV show elements with YouTube URLs")
                        
        except Exception as e:
            logger.error(f"Error processing visual content: {e}")
        
        return {
            "elements": visual_elements,
            "theme_context": current_theme,
            "processing_method": "qloo_enhanced_with_youtube_fixed_data_access"
        }
    
    async def _process_auditory_content(self, audio_data: Dict[str, Any], current_theme: Dict[str, Any], demo_dislikes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process auditory content + dislike filtering + YouTube URLs (ENHANCED with FIXED data access)."""
        
        # Check if music is generally disliked (ADDITIVE)
        if self._is_content_type_disliked("music", demo_dislikes):
            logger.info("🚫 Skipping music content - user dislikes music")
            return {"elements": [], "status": "skipped", "reason": "user_dislike"}
        
        # Process auditory content (FIXED data access + YOUTUBE URLS)
        auditory_elements = []
        
        try:
            # FIXED: Access entities from the correct structure
            entities = audio_data.get("entities", [])
            logger.info(f"🔧 FIXED: Agent 4 processing {len(entities)} artist entities")
            
            if entities and len(entities) > 0:
                for item in entities:
                    # Filter by dislikes (ADDITIVE)
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        artist_name = item.get("name", "Classic Music")
                        
                        # NEW: Make YouTube call to get embeddable URL
                        youtube_url = ""
                        try:
                            if self.youtube_tool:
                                youtube_results = await self.youtube_tool.search_music(f"{artist_name} greatest hits", max_results=1)
                                if youtube_results and youtube_results.get("items"):
                                    first_result = youtube_results["items"][0]
                                    youtube_url = first_result.get("embeddable_url", "")
                                    logger.info(f"🎵 Retrieved YouTube URL for {artist_name}: {bool(youtube_url)}")
                        except Exception as e:
                            logger.warning(f"Failed to get YouTube URL for {artist_name}: {e}")
                        
                        auditory_elements.append({
                            "type": "music",
                            "name": artist_name,
                            "artist": artist_name,
                            "theme_relevance": current_theme.get("name", "general"),
                            "youtube_url": youtube_url  # NEW: Include embeddable URL
                        })
                        
            logger.info(f"✅ FIXED: Agent 4 generated {len(auditory_elements)} music elements with YouTube URLs")
                        
        except Exception as e:
            logger.error(f"Error processing auditory content: {e}")
        
        return {
            "elements": auditory_elements,
            "theme_context": current_theme,
            "processing_method": "qloo_enhanced_with_youtube_fixed_data_access"
        }
    
    def _generate_tactile_content(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tactile content (ORIGINAL)."""
        
        return {
            "elements": [
                {
                    "type": "tactile_activity",
                    "name": "Gentle hand massage",
                    "description": "Soothing tactile experience",
                    "theme_relevance": current_theme.get("name", "general")
                }
            ]
        }
    
    def _generate_olfactory_content(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate olfactory content (ORIGINAL)."""
        
        return {
            "elements": [
                {
                    "type": "scent",
                    "name": "Familiar kitchen aromas",
                    "description": "Comforting cooking scents",
                    "theme_relevance": current_theme.get("name", "general")
                }
            ]
        }
    
    def _is_content_type_disliked(self, content_type: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """
        Check if a content type is generally disliked by the user (ADDITIVE).
        """
        for dislike in demo_dislikes:
            if dislike.get("type") == content_type:
                return True
        return False
    
    def _is_specific_item_disliked(self, item_name: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """
        Check if a specific item name is disliked (ADDITIVE).
        """
        item_name_lower = item_name.lower()
        
        for dislike in demo_dislikes:
            dislike_name = dislike.get("name", "").lower()
            
            # Check for exact match or partial match
            if (dislike_name in item_name_lower) or (item_name_lower in dislike_name):
                return True
        
        return False
    
    def _create_fallback_sensory_content(self, consolidated_info: Dict[str, Any], cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when errors occur (ORIGINAL)."""
        
        logger.warning("Creating fallback sensory content")
        
        heritage = cultural_profile.get("cultural_elements", {}).get("heritage", "American")
        
        return {
            "sensory_content": {
                "content_by_sense": {
                    "gustatory": {
                        "elements": [
                            {
                                "name": "Warm Apple Slices",
                                "ingredients": ["apples", "cinnamon"],
                                "instructions": ["Slice and warm gently"],
                                "heritage_connection": f"Simple {heritage} comfort food"
                            }
                        ]
                    },
                    "auditory": {"elements": []},
                    "visual": {"elements": []},
                    "tactile": {"elements": []},
                    "olfactory": {"elements": []}
                },
                "generation_metadata": {
                    "heritage_used": heritage,
                    "status": "fallback_simplified_approach",
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
        }

# Export the main class
__all__ = ["SensoryContentGeneratorAgent"]