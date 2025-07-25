"""
Sensory Content Generator Agent - FIXED with run() method
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

CHANGES:
- Added proper run() method that works with SequentialAgent
- Maintains enhanced theme matching functionality
- Compatible with existing pipeline interface
"""

import logging
import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

# Import theme manager for enhanced theme-aware functionality
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
    Agent 4: Sensory Content Generator with ENHANCED theme-aware recipe selection
    
    FIXED: Now includes proper run() method for pipeline compatibility
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with ENHANCED theme matching")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Main run method for pipeline compatibility
        
        Args:
            consolidated_info: Consolidated information including daily theme
            cultural_profile: Cultural profile data
            qloo_intelligence: Qloo API results
            
        Returns:
            Sensory content organized by sense with theme-matched recipes
        """
        
        logger.info("🎨 Agent 4: Starting enhanced sensory content generation")
        
        try:
            # Extract daily theme from consolidated info
            daily_theme = consolidated_info.get("daily_theme", {})
            
            # Extract other content
            vision_data = qloo_intelligence.get("tv_shows", {})
            audio_data = qloo_intelligence.get("music", {})
            
            # Generate enhanced sensory content
            sensory_result = self.generate_sensory_content(vision_data, audio_data, daily_theme)
            
            return {
                "sensory_content": sensory_result
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 run method failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    def generate_sensory_content(self, vision_data: Dict[str, Any], 
                               audio_data: Dict[str, Any], 
                               daily_theme: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCED: Generate sensory content with enhanced theme-aware recipe selection
        """
        
        logger.info(f"🎨 Generating sensory content for theme: {daily_theme.get('theme_of_the_day', {}).get('name', 'Unknown')}")
        
        current_theme = daily_theme.get("theme_of_the_day", {})
        
        # ENHANCED: Use theme manager for better recipe filtering
        filtered_recipes = self._get_theme_filtered_recipes(current_theme)
        
        # Select best recipe from filtered results
        selected_recipe = self._select_best_recipe(filtered_recipes, current_theme)
        
        # Generate enhanced gustatory content with theme awareness
        gustatory_content = self._generate_gustatory_content(selected_recipe, current_theme)
        
        # Process other sensory content (visual, auditory, etc.)
        visual_content = self._process_visual_content(vision_data, current_theme)
        auditory_content = self._process_auditory_content(audio_data, current_theme)
        
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
                "version": "enhanced_theme_matching"
            }
        }
        
        logger.info(f"✅ Sensory content generated successfully with theme-matched recipe: {selected_recipe.get('name', 'Unknown')}")
        return sensory_result
    
    def _load_recipes_json(self) -> List[Dict[str, Any]]:
        """Load theme-aligned recipes from JSON file."""
        try:
            recipes_path = os.path.join(os.path.dirname(__file__), "../../config/recipes.json")
            with open(recipes_path, 'r') as f:
                recipes = json.load(f)
                logger.info(f"✅ Loaded {len(recipes)} theme-aligned recipes from recipes.json")
                
                # Log theme distribution for debugging
                theme_counts = {}
                for recipe in recipes:
                    theme = None
                    if isinstance(recipe.get("notes"), dict):
                        theme = recipe["notes"].get("theme", "unknown")
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1
                
                logger.info(f"🎯 Recipe theme distribution: {theme_counts}")
                return recipes
                
        except Exception as e:
            logger.error(f"❌ Failed to load recipes.json: {e}")
            return self._get_hardcoded_fallback_recipes()
    
    def _get_hardcoded_fallback_recipes(self) -> List[Dict[str, Any]]:
        """Hardcoded recipes if JSON file unavailable."""
        logger.warning("🔄 Using hardcoded fallback recipes")
        return [
            {
                "name": "Warm Cinnamon Apples",
                "ingredients": ["1 apple (soft)", "1/2 tsp cinnamon", "1 tsp brown sugar", "1 tsp butter"],
                "instructions": ["Place apple slices in microwave-safe bowl", "Sprinkle with cinnamon and sugar, dot with butter", "Microwave 1-2 minutes until soft"],
                "notes": {
                    "text": "Smells like apple pie. Great for nostalgic memories.",
                    "theme": "food"
                },
                "conversation_starters": [
                    "What was your favorite dessert growing up?",
                    "Do you remember making or eating apple pie?",
                    "What foods remind you of home?"
                ]
            }
        ]
    
    def _get_theme_filtered_recipes(self, current_theme: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recipes filtered by current theme using theme manager"""
        
        if not theme_manager:
            logger.warning("⚠️ Theme manager not available, returning all recipes")
            return self.recipes_data
        
        if not current_theme:
            logger.warning("⚠️ No current theme provided, returning all recipes")
            return self.recipes_data
        
        try:
            # Use the enhanced theme filtering from theme manager
            filtered_recipes = theme_manager.filter_recipes_by_theme(self.recipes_data, current_theme)
            
            logger.info(f"🎯 Theme filtering complete: {len(filtered_recipes)} recipes available for theme '{current_theme.get('name', 'Unknown')}'")
            
            return filtered_recipes
            
        except Exception as e:
            logger.error(f"❌ Error in theme filtering: {e}")
            return self.recipes_data
    
    def _select_best_recipe(self, filtered_recipes: List[Dict[str, Any]], 
                           current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Select the best recipe from theme-filtered results"""
        
        if not filtered_recipes:
            logger.warning("⚠️ No filtered recipes available, using fallback")
            return self._get_hardcoded_fallback_recipes()[0]
        
        # The first recipe should be the best match due to theme filtering
        selected_recipe = filtered_recipes[0]
        
        # Determine match quality for logging
        match_quality = "exact_theme_match"
        if isinstance(selected_recipe.get("notes"), dict):
            recipe_theme = selected_recipe["notes"].get("theme")
            if recipe_theme != current_theme.get("id"):
                match_quality = "keyword_fallback"
        
        logger.info(f"🎯 Selected recipe: '{selected_recipe.get('name', 'Unknown')}' (match quality: {match_quality})")
        
        # Add selection metadata to recipe
        if "selection_metadata" not in selected_recipe:
            selected_recipe["selection_metadata"] = {}
        
        selected_recipe["selection_metadata"].update({
            "method": "theme_filtered",
            "match_quality": match_quality,
            "theme_id": current_theme.get("id"),
            "selected_at": datetime.now().isoformat()
        })
        
        return selected_recipe
    
    def _generate_gustatory_content(self, recipe: Dict[str, Any], 
                                  current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate gustatory content with improved recipe processing"""
        
        # Process conversation starters - prefer recipe-specific ones
        conversation_starters = recipe.get("conversation_starters", [])
        
        # If no recipe-specific starters, use theme-based ones as fallback
        if not conversation_starters and current_theme:
            conversation_starters = current_theme.get("conversation_prompts", [])
        
        # Ultimate fallback
        if not conversation_starters:
            conversation_starters = [
                "What foods remind you of special times?",
                "Do you have a favorite comfort food?",
                "What did you like to cook or eat?"
            ]
        
        # Create enhanced gustatory content
        gustatory_content = {
            "elements": [recipe],  # Maintained for compatibility with mobile synthesizer
            "primary_recipe": recipe,
            "conversation_starters": conversation_starters[:3],  # Limit to 3 for UI
            "sensory_notes": {
                "taste_profile": self._extract_taste_profile(recipe),
                "preparation_style": self._extract_preparation_style(recipe),
                "nostalgia_factor": recipe.get("notes", {}).get("text", "") if isinstance(recipe.get("notes"), dict) else str(recipe.get("notes", ""))
            },
            "selection_metadata": recipe.get("selection_metadata", {})
        }
        
        logger.info(f"🍽️ Gustatory content generated for recipe: {recipe.get('name', 'Unknown')}")
        return gustatory_content
    
    def _extract_taste_profile(self, recipe: Dict[str, Any]) -> str:
        """Extract taste profile from recipe ingredients and notes"""
        ingredients = recipe.get("ingredients", [])
        ingredient_text = " ".join(ingredients).lower()
        
        # Simple taste profiling
        if any(word in ingredient_text for word in ["sweet", "sugar", "honey", "fruit", "berry"]):
            return "sweet"
        elif any(word in ingredient_text for word in ["salt", "savory", "cheese", "meat"]):
            return "savory"
        elif any(word in ingredient_text for word in ["spice", "pepper", "garlic", "herb"]):
            return "aromatic"
        else:
            return "mild"
    
    def _extract_preparation_style(self, recipe: Dict[str, Any]) -> str:
        """Extract preparation style from recipe instructions"""
        instructions = recipe.get("instructions", [])
        instruction_text = " ".join(instructions).lower()
        
        if "microwave" in instruction_text:
            return "quick_microwave"
        elif any(word in instruction_text for word in ["bake", "oven"]):
            return "baked"
        elif any(word in instruction_text for word in ["boil", "simmer", "stove"]):
            return "stovetop"
        else:
            return "simple_prep"
    
    def _process_visual_content(self, vision_data: Dict[str, Any], 
                              current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Process visual content with theme awareness"""
        return vision_data
    
    def _process_auditory_content(self, audio_data: Dict[str, Any], 
                                current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Process auditory content with theme awareness"""
        return audio_data
    
    def _generate_tactile_content(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tactile content based on theme"""
        return {
            "texture_focus": current_theme.get("content_preferences", {}).get("sensory_focus") == "tactile",
            "elements": []
        }
    
    def _generate_olfactory_content(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate olfactory content based on theme"""
        return {
            "scent_focus": current_theme.get("content_preferences", {}).get("sensory_focus") == "olfactory", 
            "elements": []
        }
    
    def _create_fallback_sensory_content(self, consolidated_info: Dict[str, Any], 
                                       cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails"""
        
        heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
        
        # Use first available recipe as fallback
        base_recipe = self.recipes_data[0] if self.recipes_data else {
            "name": "Simple Comfort Food",
            "ingredients": ["Basic ingredients"],
            "instructions": ["Simple preparation"]
        }
        
        return {
            "sensory_content": {
                "content_by_sense": {
                    "gustatory": {
                        "elements": [base_recipe],
                        "primary_recipe": base_recipe,
                        "conversation_starters": ["What comfort foods do you remember?"]
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