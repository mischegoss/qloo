"""
Agent 4B: Recipe Selection Agent - Pure JSON-based System
File: backend/multi_tool_agent/agents/recipe_selection_agent.py

SIMPLIFIED APPROACH:
- Uses curated recipes.json (no external API failures)
- Filters by theme first, then heritage
- Uses pre-written conversation starters (no Gemini needed)
- Comprehensive fallbacks ensure it always works
- Perfect for dementia patients: microwave-safe, simple ingredients
- Fast, reliable, and cost-effective
"""

import logging
import json
import random
from typing import Dict, Any, List, Optional
from pathlib import Path

# Configure logger
logger = logging.getLogger(__name__)

class RecipeSelectionAgent:
    """
    Agent 4B: Recipe Selection with pure JSON-based filtering.
    
    Takes patient profile and theme, selects culturally-appropriate microwave-safe recipes.
    Uses curated conversation starters from JSON for reliability and speed.
    """
    
    def __init__(self):
        # Load recipes from JSON file
        self.recipes_database = self._load_recipes_database()
        
        logger.info("🍽️ Agent 4B: Recipe Selection initialized with pure JSON-based system")
        logger.info(f"📊 Loaded {len(self.recipes_database)} culturally-diverse recipes")
        logger.info("⚡ Using curated conversation starters for maximum reliability")
    
    def _load_recipes_database(self) -> List[Dict[str, Any]]:
        """Load recipes from the enhanced recipes.json file"""
        
        try:
            # Find the recipes.json file (relative to this file)
            recipes_file = Path(__file__).parent.parent.parent / "config" / "recipes.json"
            
            if recipes_file.exists():
                with open(recipes_file, 'r', encoding='utf-8') as f:
                    recipes = json.load(f)
                    logger.info(f"✅ Loaded {len(recipes)} recipes from {recipes_file}")
                    return recipes
            else:
                logger.warning(f"⚠️ Recipe file not found: {recipes_file}")
                return self._get_fallback_recipes()
                
        except Exception as e:
            logger.error(f"❌ Error loading recipes database: {e}")
            return self._get_fallback_recipes()
    
    def _get_fallback_recipes(self) -> List[Dict[str, Any]]:
        """Provide emergency fallback recipes if JSON loading fails"""
        
        return [
            {
                "name": "Microwave Mac and Cheese",
                "ingredients": ["1 cup pasta", "1/2 cup cheese", "1/4 cup milk", "1 tablespoon butter"],
                "instructions": [
                    "Cook pasta in microwave with water for 3 minutes",
                    "Drain and stir in cheese, milk, and butter",
                    "Heat for 1 more minute until creamy"
                ],
                "heritage_tags": ["american"],
                "theme_tags": ["comfort", "family"],
                "cultural_context": "Classic American comfort food loved by families everywhere",
                "conversation_starters": [
                    "Did you make mac and cheese for your children?",
                    "What was your favorite comfort food?",
                    "Do you remember cooking for your family?"
                ],
                "prep_time": "5 minutes",
                "difficulty": "Easy"
            },
            {
                "name": "Italian Microwave Risotto",
                "ingredients": ["1/2 cup instant rice", "1 cup chicken broth", "2 tablespoons Parmesan cheese", "1 teaspoon butter"],
                "instructions": [
                    "Combine rice and broth in microwave-safe bowl",
                    "Microwave for 3-4 minutes until rice is tender",
                    "Stir in Parmesan cheese and butter",
                    "Let sit for 2 minutes before serving"
                ],
                "heritage_tags": ["italian", "italian-american"],
                "theme_tags": ["family", "comfort"],
                "cultural_context": "Risotto is a beloved Italian comfort food, often made for family gatherings",
                "conversation_starters": [
                    "Did your family make risotto on special occasions?",
                    "Do you remember Italian dishes from your childhood?",
                    "What was your favorite Italian restaurant?"
                ],
                "prep_time": "5 minutes",
                "difficulty": "Easy"
            }
        ]
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select and enhance a recipe based on patient profile and theme.
        
        Args:
            enhanced_profile: Profile from previous agents containing patient_info, theme_info, qloo_intelligence
            
        Returns:
            Dict containing selected recipe with enhanced conversation starters
        """
        
        logger.info("🍽️ Agent 4B: Starting recipe selection with cultural matching")
        
        try:
            # Extract patient information
            patient_info = enhanced_profile.get("patient_info", {})
            theme_info = enhanced_profile.get("theme_info", {})
            
            heritage = patient_info.get("cultural_heritage", "american").lower()
            theme_id = theme_info.get("id", "comfort")
            theme_name = theme_info.get("name", "Comfort")
            patient_name = patient_info.get("first_name", "Friend")
            
            logger.info(f"🎯 Selecting recipe for {patient_name} (Theme: {theme_name}, Heritage: {heritage})")
            
            # Step 1: Filter recipes by THEME first (priority for daily variety)
            theme_matches = self._filter_by_theme(self.recipes_database, theme_id)
            logger.info(f"🎯 Found {len(theme_matches)} theme-matching recipes")
            
            # Step 2: Filter by heritage within theme matches (secondary filter)
            final_candidates = self._filter_by_heritage_within_theme(theme_matches, heritage)
            
            # Step 3: If no theme + heritage match, use theme-only
            if not final_candidates:
                logger.info(f"⚠️ No {theme_id} + {heritage} matches, using theme-only")
                final_candidates = theme_matches
            
            # Step 4: If no theme matches, fall back to heritage-only
            if not final_candidates:
                logger.info(f"⚠️ No theme matches, falling back to heritage-only")
                final_candidates = self._filter_by_heritage(heritage)
            
            # Step 5: Emergency fallback
            if not final_candidates:
                logger.warning("⚠️ No matches found, using emergency fallback")
                final_candidates = self._get_fallback_recipes()
            
            # Select recipe (could add randomization here)
            selected_recipe = final_candidates[0]
            recipe_name = selected_recipe.get("name", "Unknown Recipe")
            
            logger.info(f"✅ Selected: {recipe_name}")
            
            # Step 6: Format final output (no Gemini enhancement needed)
            theme_match_count = len(theme_matches)
            heritage_match_within_theme = len(final_candidates) < theme_match_count if theme_match_count > 0 else False
            
            return self._format_recipe_output(selected_recipe, heritage, theme_id, theme_match_count, heritage_match_within_theme)
            
        except Exception as e:
            logger.error(f"❌ Recipe selection failed: {e}")
            return await self._get_emergency_fallback(enhanced_profile)
    
    def _filter_by_heritage_within_theme(self, theme_recipes: List[Dict[str, Any]], heritage: str) -> List[Dict[str, Any]]:
        """Filter recipes by heritage within already-filtered theme recipes"""
        
        # Normalize heritage and create search terms
        heritage_terms = [heritage.lower()]
        
        # Add common variations
        if "italian" in heritage:
            heritage_terms.extend(["italian", "italian-american"])
        elif "irish" in heritage:
            heritage_terms.extend(["irish", "irish-american"])
        elif "german" in heritage:
            heritage_terms.extend(["german", "german-american"])
        elif "mexican" in heritage:
            heritage_terms.extend(["mexican", "mexican-american", "hispanic"])
        elif "chinese" in heritage:
            heritage_terms.extend(["chinese", "chinese-american", "asian"])
        elif "jewish" in heritage:
            heritage_terms.extend(["jewish", "jewish-american", "eastern-european"])
        
        matching_recipes = []
        
        for recipe in theme_recipes:
            recipe_heritage_tags = recipe.get("heritage_tags", [])
            
            # Check if any heritage term matches recipe tags
            for term in heritage_terms:
                if term in recipe_heritage_tags:
                    matching_recipes.append(recipe)
                    break  # Avoid duplicates
        
        logger.debug(f"🔍 Heritage filter within theme found {len(matching_recipes)} matches")
        return matching_recipes
    
    def _filter_by_heritage(self, heritage: str) -> List[Dict[str, Any]]:
        """Filter recipes by heritage tags"""
        
        # Normalize heritage and create search terms
        heritage_terms = [heritage.lower()]
        
        # Add common variations
        if "italian" in heritage:
            heritage_terms.extend(["italian", "italian-american"])
        elif "irish" in heritage:
            heritage_terms.extend(["irish", "irish-american"])
        elif "german" in heritage:
            heritage_terms.extend(["german", "german-american"])
        elif "mexican" in heritage:
            heritage_terms.extend(["mexican", "mexican-american", "hispanic"])
        elif "chinese" in heritage:
            heritage_terms.extend(["chinese", "chinese-american", "asian"])
        elif "jewish" in heritage:
            heritage_terms.extend(["jewish", "jewish-american", "eastern-european"])
        
        matching_recipes = []
        
        for recipe in self.recipes_database:
            recipe_heritage_tags = recipe.get("heritage_tags", [])
            
            # Check if any heritage term matches recipe tags
            for term in heritage_terms:
                if term in recipe_heritage_tags:
                    matching_recipes.append(recipe)
                    break  # Avoid duplicates
        
        logger.debug(f"🔍 Heritage filter '{heritage}' found {len(matching_recipes)} matches")
        return matching_recipes
    
    def _filter_by_theme(self, recipes: List[Dict[str, Any]], theme_id: str) -> List[Dict[str, Any]]:
        """Filter recipes by theme tags - matches exact theme IDs from themes.json"""
        
        # Use exact theme ID matching (no variations needed since we control the JSON)
        theme_search = theme_id.lower()
        
        matching_recipes = []
        
        for recipe in recipes:
            recipe_theme_tags = recipe.get("theme_tags", [])
            
            # Direct theme matching
            if theme_search in recipe_theme_tags:
                matching_recipes.append(recipe)
        
        logger.debug(f"🎯 Theme filter '{theme_id}' found {len(matching_recipes)} matches")
        return matching_recipes
    
    def _format_recipe_output(self, recipe: Dict[str, Any], heritage: str, theme_id: str, theme_match_count: int, heritage_match_within_theme: bool) -> Dict[str, Any]:
        """Format the final recipe output for the dashboard"""
        
        # Use original curated conversation starters from JSON
        conversation_starters = recipe.get("conversation_starters", [])
        
        return {
            "recipe_content": {
                "name": recipe.get("name", "Unknown Recipe"),
                "ingredients": recipe.get("ingredients", []),
                "instructions": recipe.get("instructions", []),
                "prep_time": recipe.get("prep_time", "5 minutes"),
                "difficulty": recipe.get("difficulty", "Easy"),
                "cultural_context": recipe.get("cultural_context", "A comforting dish perfect for any occasion"),
                "conversation_starters": conversation_starters[:3],  # Limit to 3 starters
                "heritage_connection": f"Selected for {heritage} heritage" if heritage_match_within_theme else "Theme-based selection",
                "theme_connection": f"Perfect for {theme_id} theme"
            },
            "metadata": {
                "heritage_match": heritage_match_within_theme,
                "theme_match": theme_id in recipe.get("theme_tags", []),
                "selection_method": "pure_json_based",
                "total_recipes_available": len(self.recipes_database),
                "theme_recipes_found": theme_match_count,
                "conversation_source": "curated_json",
                "agent": "recipe_selection_agent_4b",
                "safety_verified": True,  # All our recipes are microwave-safe
                "microwave_only": True,
                "filtering_approach": "theme_first_heritage_second"
            }
        }
    
    async def _get_emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback if everything fails"""
        
        logger.warning("🚨 Using emergency recipe fallback")
        
        emergency_recipe = {
            "name": "Simple Microwave Mac and Cheese",
            "ingredients": ["1 cup pasta", "1/2 cup cheese", "1/4 cup milk"],
            "instructions": [
                "Cook pasta in microwave with water for 3 minutes",
                "Stir in cheese and milk",
                "Heat for 1 more minute"
            ],
            "cultural_context": "A simple, comforting dish that everyone can enjoy",
            "conversation_starters": [
                "What was your favorite comfort food?",
                "Do you remember cooking for your family?",
                "What foods make you feel happy?"
            ]
        }
        
        return {
            "recipe_content": {
                "name": emergency_recipe["name"],
                "ingredients": emergency_recipe["ingredients"],
                "instructions": emergency_recipe["instructions"],
                "prep_time": "5 minutes",
                "difficulty": "Easy",
                "cultural_context": emergency_recipe["cultural_context"],
                "conversation_starters": emergency_recipe["conversation_starters"],
                "heritage_connection": "Universal comfort food",
                "theme_connection": "Always appropriate"
            },
            "metadata": {
                "heritage_match": False,
                "theme_match": False,
                "selection_method": "emergency_fallback",
                "total_recipes_available": 0,
                "conversation_source": "curated_json",
                "agent": "recipe_selection_agent_4b",
                "safety_verified": True,
                "microwave_only": True
            }
        }

# Simple test function for development
async def test_recipe_agent():
    """Test the recipe selection agent with sample data"""
    
    logger.info("🧪 Testing Recipe Selection Agent...")
    
    # Mock enhanced profile from previous agents
    mock_profile = {
        "patient_info": {
            "first_name": "Maria",
            "cultural_heritage": "Italian-American",
            "birth_year": 1945
        },
        "theme_info": {
            "id": "family",
            "name": "Family",
            "description": "Cherishing family bonds and togetherness"
        },
        "qloo_intelligence": {
            "cultural_recommendations": {
                "artists": {
                    "success": True,
                    "entities": [{"name": "Vivaldi"}]
                }
            }
        }
    }
    
    # Test with pure JSON approach (no external dependencies)
    logger.info("🧪 Testing pure JSON-based recipe selection...")
    agent = RecipeSelectionAgent()
    result = await agent.run(mock_profile)
    
    print(f"✅ Result: {result['recipe_content']['name']}")
    print(f"   Heritage Match: {result['metadata']['heritage_match']}")
    print(f"   Theme Match: {result['metadata']['theme_match']}")
    print(f"   Selection Method: {result['metadata']['selection_method']}")
    print(f"   Conversation Source: {result['metadata']['conversation_source']}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_recipe_agent())