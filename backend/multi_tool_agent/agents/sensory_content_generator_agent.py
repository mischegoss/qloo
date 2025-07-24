"""
Enhanced Sensory Content Generator Agent with Theme-Aware Recipe Selection
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

Agent 4: Uses pre-made recipes from JSON + light Gemini customization + theme awareness
"""

import logging
import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger FIRST
logger = logging.getLogger(__name__)

# Import theme manager for theme-aware filtering (FIXED import path)
try:
    # Try direct import path first (working path)
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config.theme_config import theme_manager
    logger.info("✅ Sensory Content Generator: theme_manager imported successfully")
    logger.info(f"🔍 DEBUG: theme_manager object: {theme_manager}")
    logger.info(f"🔍 DEBUG: theme_manager methods: {[m for m in dir(theme_manager) if not m.startswith('_')]}")
except ImportError as e:
    logger.error(f"❌ Sensory Content Generator: Failed to import theme_manager: {e}")
    theme_manager = None
except Exception as e:
    logger.error(f"❌ Sensory Content Generator: Error with theme_manager: {e}")
    theme_manager = None

class SensoryContentGeneratorAgent:
    """
    Agent 4: Sensory Content Generator with Theme-Aware Recipe Selection
    
    Uses pre-made recipes from backend/config/recipes.json and applies:
    1. Theme-aware recipe filtering (NEW)
    2. Light cultural customization via Gemini (IMPROVED - no cultural prefixes)
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with theme-aware recipe selection")
    
    def _load_recipes_json(self) -> List[Dict[str, Any]]:
        """Load simple recipes from JSON file."""
        try:
            recipes_path = os.path.join(os.path.dirname(__file__), "../../config/recipes.json")
            with open(recipes_path, 'r') as f:
                recipes = json.load(f)
                logger.info(f"Loaded {len(recipes)} recipes from recipes.json")
                return recipes
        except Exception as e:
            logger.error(f"Failed to load recipes.json: {e}")
            return self._get_hardcoded_fallback_recipes()
    
    def _get_hardcoded_fallback_recipes(self) -> List[Dict[str, Any]]:
        """Hardcoded recipes if JSON file unavailable."""
        return [
            {
                "name": "Warm Cinnamon Apples",
                "ingredients": ["1 apple (soft)", "1/2 tsp cinnamon", "1 tsp brown sugar", "1 tsp butter"],
                "instructions": ["Place apple slices in microwave-safe bowl", "Sprinkle with cinnamon and sugar, dot with butter", "Microwave 1-2 minutes until soft"],
                "notes": "Smells like apple pie. Great for nostalgic memories."
            },
            {
                "name": "Microwave Oatmeal with Raisins", 
                "ingredients": ["1/2 cup oats", "1 cup milk", "1 tbsp raisins", "Dash cinnamon"],
                "instructions": ["Mix all ingredients in microwave-safe bowl", "Microwave 90 seconds to 2 minutes", "Let cool 1 minute before serving"],
                "notes": "Warm and sweet, often served by grandparents."
            }
        ]
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any], 
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive sensory content with theme-aware recipe selection.
        
        Args:
            consolidated_info: Output from Agent 1 (now includes daily_theme)
            cultural_profile: Output from Agent 2
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Comprehensive sensory content including recipes and YouTube links
        """
        
        try:
            logger.info("🍳 Agent 4: Generating sensory content with theme awareness")
            
            # Extract daily theme (NEW - additive)
            daily_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
            theme_name = daily_theme.get("name", "General")
            
            # DEBUG: Log theme extraction
            logger.info(f"🔍 DEBUG Agent 4: consolidated_info keys: {list(consolidated_info.keys())}")
            logger.info(f"🔍 DEBUG Agent 4: daily_theme structure: {consolidated_info.get('daily_theme', 'MISSING')}")
            logger.info(f"🔍 DEBUG Agent 4: extracted theme name: {theme_name}")
            
            # Extract patient and cultural info (existing logic)
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = cultural_profile.get("heritage_analysis", {}).get("primary_heritage", "universal")
            
            logger.info(f"🎯 Theme: {theme_name}, Heritage: {heritage}")
            
            # 1. SELECT RECIPES with theme awareness (NEW)
            selected_recipes = await self._select_theme_aware_recipes(daily_theme, patient_profile)
            
            # 2. CUSTOMIZE selected recipes (IMPROVED - no cultural prefixes)
            customized_recipes = await self._customize_recipes_with_gemini(
                selected_recipes, heritage, daily_theme, patient_profile
            )
            
            # 3. GENERATE YOUTUBE links for recipes (existing logic)
            recipes_with_youtube = await self._add_youtube_links_to_recipes(customized_recipes)
            
            # 4. CREATE sensory recommendations (existing logic)
            sensory_recommendations = self._create_sensory_recommendations(
                daily_theme, heritage, patient_profile
            )
            
            # 5. BUILD comprehensive response
            sensory_content = {
                "recipes": recipes_with_youtube,
                "theme_context": {
                    "daily_theme": daily_theme,
                    "theme_applied": True,
                    "theme_filtering_used": len(selected_recipes) > 0
                },
                "sensory_recommendations": sensory_recommendations,
                "youtube_integration": {
                    "recipes_with_videos": len([r for r in recipes_with_youtube if r.get("youtube_url")]),
                    "total_recipes": len(recipes_with_youtube)
                },
                "generation_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "theme_aware_selection": True,
                    "cultural_customization": "light_without_prefixes",
                    "agent_version": "4.1_theme_aware"
                }
            }
            
            logger.info(f"✅ Agent 4 completed: {len(recipes_with_youtube)} recipes generated with theme '{theme_name}'")
            
            return {"sensory_content": sensory_content}
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info)
    
    async def _select_theme_aware_recipes(self, 
                                        daily_theme: Dict[str, Any],
                                        patient_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        NEW: Select recipes with theme awareness while maintaining variety.
        
        Args:
            daily_theme: Current daily theme configuration
            patient_profile: Patient preferences and restrictions
            
        Returns:
            Theme-filtered and prioritized recipes
        """
        
        # Start with all available recipes
        available_recipes = self.recipes_data.copy()
        
        # If theme filtering available, use it
        if daily_theme and daily_theme.get("recipe_keywords") and theme_manager:
            logger.info(f"🎯 Filtering recipes by theme: {daily_theme['name']}")
            try:
                theme_filtered = theme_manager.filter_recipes_by_theme(available_recipes, daily_theme)
                
                # Use theme-filtered recipes but ensure we have enough variety
                if len(theme_filtered) >= 3:
                    selected_recipes = theme_filtered[:5]  # Top 5 theme-matched recipes
                else:
                    # Mix theme-matched with general recipes for variety
                    selected_recipes = theme_filtered + available_recipes[:3]
            except Exception as e:
                logger.error(f"❌ Theme filtering failed: {e}")
                selected_recipes = available_recipes
        else:
            # No theme filtering - use all recipes
            logger.warning(f"⚠️ No theme filtering available - theme_manager: {theme_manager is not None}, daily_theme: {daily_theme.get('name', 'None')}, keywords: {daily_theme.get('recipe_keywords', 'None')}")
            selected_recipes = available_recipes
        
        # Shuffle for variety while respecting theme priority
        random.shuffle(selected_recipes)
        
        logger.info(f"Selected {len(selected_recipes)} recipes for customization")
        return selected_recipes[:6]  # Limit to 6 for processing efficiency
    
    async def _customize_recipes_with_gemini(self, 
                                           recipes: List[Dict[str, Any]],
                                           heritage: str,
                                           daily_theme: Dict[str, Any],
                                           patient_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        IMPROVED: Customize recipes via Gemini WITHOUT adding cultural prefixes.
        
        Args:
            recipes: Selected recipes to customize
            heritage: Cultural heritage (for context only)
            daily_theme: Daily theme for context
            patient_profile: Patient information
            
        Returns:
            Customized recipes with enhanced descriptions
        """
        
        if not recipes or not self.gemini_tool:
            logger.warning("No recipes to customize or Gemini unavailable")
            return recipes
        
        customized_recipes = []
        theme_name = daily_theme.get("name", "General")
        theme_description = daily_theme.get("description", "")
        
        for recipe in recipes[:3]:  # Limit to 3 for API efficiency
            try:
                # IMPROVED PROMPT: Much shorter to avoid token limits
                customization_prompt = f"""
                Enhance this recipe for dementia care with theme: {theme_name}

                Recipe: {recipe.get('name', 'Unnamed Recipe')}
                
                Add brief nostalgic description (2-3 sentences) and simple caregiver tip.
                Keep original name exactly: "{recipe.get('name', '')}"
                
                JSON format:
                {{
                  "name": "{recipe.get('name', '')}",
                  "nostalgic_description": "Brief sensory description here",
                  "caregiver_tips": "One simple tip here"
                }}
                """
                
                # Call Gemini for customization (with proper method handling)
                try:
                    if hasattr(self.gemini_tool, 'generate_recipe'):
                        # Use the specific recipe generation method with shorter prompt
                        gemini_response = await self.gemini_tool.generate_recipe(customization_prompt)
                    elif hasattr(self.gemini_tool, 'generate_content'):
                        gemini_response = await self.gemini_tool.generate_content(customization_prompt)
                    elif hasattr(self.gemini_tool, 'generate'):
                        gemini_response = await self.gemini_tool.generate(customization_prompt)
                    elif hasattr(self.gemini_tool, 'call'):
                        gemini_response = await self.gemini_tool.call(customization_prompt)
                    else:
                        logger.error(f"Gemini tool missing expected methods. Available: {dir(self.gemini_tool)}")
                        gemini_response = None
                except Exception as gemini_error:
                    logger.error(f"Gemini API call failed: {gemini_error}")
                    gemini_response = None
                
                if gemini_response and gemini_response.get("success"):
                    try:
                        # Parse JSON response with better error handling
                        content = gemini_response.get("content", "")
                        if len(content) < 50:  # Too short, likely truncated
                            logger.warning(f"Gemini response too short ({len(content)} chars), using original recipe")
                            customized_data = None
                        else:
                            customized_data = json.loads(content)
                        
                        if customized_data:
                            # Build enhanced recipe with simplified data
                            enhanced_recipe = {
                                **recipe,  # Keep original recipe data
                                "name": recipe.get("name"),  # KEEP ORIGINAL NAME
                                "nostalgic_description": customized_data.get("nostalgic_description", ""),
                                "caregiver_tips": customized_data.get("caregiver_tips", ""),
                                "theme_connection": f"Selected for {theme_name} theme",
                                "customization_applied": True
                            }
                            
                            customized_recipes.append(enhanced_recipe)
                            logger.info(f"✅ Customized recipe: {enhanced_recipe['name']}")
                        else:
                            # Use original recipe
                            enhanced_recipe = {
                                **recipe,
                                "theme_connection": f"Selected for {theme_name} theme",
                                "customization_applied": False,
                                "fallback_reason": "gemini_response_too_short"
                            }
                            customized_recipes.append(enhanced_recipe)
                            logger.info(f"📝 Using original recipe: {recipe['name']} (Gemini response insufficient)")
                        
                    except json.JSONDecodeError as e:
                        # Better JSON error handling
                        logger.warning(f"JSON parse failed for {recipe['name']}: {e}")
                        logger.debug(f"Failed JSON content: {gemini_response.get('content', 'No content')[:200]}...")
                        # Use original recipe with theme connection
                        enhanced_recipe = {
                            **recipe,
                            "theme_connection": f"Selected for {theme_name} theme",
                            "customization_applied": False,
                            "fallback_reason": "json_parse_error"
                        }
                        customized_recipes.append(enhanced_recipe)
                        logger.info(f"📝 Using original recipe: {recipe['name']} (JSON parse failed)")
                
                else:
                    # Gemini call failed - use original recipe
                    enhanced_recipe = {
                        **recipe,
                        "theme_connection": f"Selected for {theme_name} theme",
                        "customization_applied": False,
                        "fallback_reason": "gemini_api_error"
                    }
                    customized_recipes.append(enhanced_recipe)
                    logger.info(f"📝 Using original recipe: {recipe['name']} (Gemini API failed)")
                
            except Exception as e:
                logger.error(f"Error customizing recipe {recipe.get('name', 'unknown')}: {e}")
                # Always include the original recipe as fallback
                customized_recipes.append({
                    **recipe,
                    "theme_connection": f"Selected for {theme_name} theme",
                    "customization_applied": False,
                    "fallback_reason": "customization_error"
                })
        
        logger.info(f"Customized {len(customized_recipes)} recipes with theme context")
        return customized_recipes
    
    async def _add_youtube_links_to_recipes(self, recipes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add YouTube links to recipes using YouTube tool (existing logic)."""
        
        if not recipes or not self.youtube_tool:
            return recipes
        
        recipes_with_youtube = []
        
        for recipe in recipes:
            try:
                recipe_name = recipe.get("name", "cooking recipe")
                search_query = f"how to make {recipe_name} simple recipe"
                
                # Search for YouTube video
                youtube_result = await self.youtube_tool.search_videos(
                    query=search_query,
                    max_results=1
                )
                
                # Add YouTube link if found
                enhanced_recipe = recipe.copy()
                if youtube_result and youtube_result.get("success") and youtube_result.get("videos"):
                    video = youtube_result["videos"][0]
                    enhanced_recipe["youtube_url"] = video.get("url", "")
                    enhanced_recipe["youtube_title"] = video.get("title", "")
                    enhanced_recipe["youtube_available"] = True
                else:
                    enhanced_recipe["youtube_available"] = False
                
                recipes_with_youtube.append(enhanced_recipe)
                
            except Exception as e:
                logger.error(f"Error adding YouTube to {recipe.get('name', 'unknown')}: {e}")
                # Include recipe without YouTube link
                recipes_with_youtube.append({
                    **recipe, 
                    "youtube_available": False,
                    "youtube_error": str(e)
                })
        
        return recipes_with_youtube
    
    def _create_sensory_recommendations(self, 
                                      daily_theme: Dict[str, Any],
                                      heritage: str,
                                      patient_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create sensory recommendations based on theme and heritage (enhanced).
        """
        
        theme_name = daily_theme.get("name", "General")
        
        # Get sensory focus with fallback
        if theme_manager and daily_theme:
            try:
                sensory_focus = theme_manager.get_theme_sensory_focus(daily_theme)
            except Exception as e:
                logger.warning(f"Error getting theme sensory focus: {e}")
                sensory_focus = "visual"
        else:
            sensory_focus = "visual"
        
        recommendations = {
            "theme_sensory_focus": sensory_focus,
            "recommendations": []
        }
        
        # Theme-based sensory recommendations
        if theme_name == "Music":
            recommendations["recommendations"].extend([
                {"type": "auditory", "activity": "Listen to nostalgic songs together"},
                {"type": "kinesthetic", "activity": "Gentle swaying or hand movements to music"}
            ])
        elif theme_name == "Food":
            recommendations["recommendations"].extend([
                {"type": "olfactory", "activity": "Smell spices and cooking aromas"},
                {"type": "gustatory", "activity": "Taste small samples of familiar flavors"}
            ])
        elif theme_name == "Flowers":
            recommendations["recommendations"].extend([
                {"type": "olfactory", "activity": "Smell fresh flowers or herbs"},
                {"type": "visual", "activity": "Look at colorful flower photos"}
            ])
        else:
            # General recommendations
            recommendations["recommendations"].extend([
                {"type": "tactile", "activity": "Touch soft textures or familiar objects"},
                {"type": "visual", "activity": "Look at meaningful photos together"}
            ])
        
        return recommendations
    
    def _create_fallback_sensory_content(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content if main processing fails."""
        
        logger.warning("Creating fallback sensory content")
        
        # Get theme for fallback context
        daily_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
        theme_name = daily_theme.get("name", "Comfort")
        
        fallback_recipes = self._get_hardcoded_fallback_recipes()
        
        return {
            "sensory_content": {
                "recipes": fallback_recipes,
                "theme_context": {
                    "daily_theme": daily_theme,
                    "theme_applied": False,
                    "fallback_used": True
                },
                "sensory_recommendations": {
                    "theme_sensory_focus": "comfort",
                    "recommendations": [
                        {"type": "tactile", "activity": "Hold hands or gentle touch"},
                        {"type": "auditory", "activity": "Play soft, familiar music"}
                    ]
                },
                "youtube_integration": {
                    "recipes_with_videos": 0,
                    "total_recipes": len(fallback_recipes)
                },
                "generation_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "theme_aware_selection": False,
                    "cultural_customization": "fallback",
                    "agent_version": "4.1_fallback",
                    "fallback_reason": "main_processing_failed"
                }
            }
        }