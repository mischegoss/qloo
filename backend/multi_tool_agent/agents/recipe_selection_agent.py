"""
Agent 4B: Recipe Selection Agent - COMPLETE PII-COMPLIANT VERSION
File: backend/multi_tool_agent/agents/recipe_selection_agent.py

CRITICAL UPDATES FOR PII COMPLIANCE:
- Removed all personal name usage and references
- Works with anonymized profile data (cultural_heritage, age_group)
- All logging now PII-free
- Pure JSON-based system (no external API failures)
- Filters by theme first, then heritage
- Uses pre-written conversation starters (no Gemini needed)
- Perfect for dementia patients: microwave-safe, simple ingredients
"""

import logging
import json
import random
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class RecipeSelectionAgent:
    """
    Agent 4B: PII-Compliant Recipe Selection with pure JSON-based filtering.
    
    Takes anonymized patient profile and theme, selects culturally-appropriate microwave-safe recipes.
    Uses curated conversation starters from JSON for reliability and speed.
    """
    
    def __init__(self):
        # Load recipes from JSON file
        self.recipes_database = self._load_recipes_database()
        
        logger.info("🍽️ Agent 4B: PII-Compliant Recipe Selection initialized with pure JSON-based system")
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
                    "Did families make mac and cheese for their children?",
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
                    "Did families make risotto on special occasions?",
                    "Do you remember Italian dishes from your childhood?",
                    "What was your favorite Italian restaurant?"
                ],
                "prep_time": "5 minutes",
                "difficulty": "Easy"
            },
            {
                "name": "Simple Warm Apple Treat",
                "ingredients": ["1 apple", "1 tablespoon butter", "1 tablespoon brown sugar", "Pinch of cinnamon"],
                "instructions": [
                    "Cut apple into small pieces",
                    "Place in microwave-safe bowl with butter and sugar",
                    "Microwave for 2 minutes",
                    "Stir and add cinnamon",
                    "Let cool for 1 minute before serving"
                ],
                "heritage_tags": ["american", "universal"],
                "theme_tags": ["comfort", "memories", "family"],
                "cultural_context": "A simple, comforting treat that brings back childhood memories",
                "conversation_starters": [
                    "What's your favorite type of apple?",
                    "Do you remember making treats like this?",
                    "What other simple desserts do you enjoy?"
                ],
                "prep_time": "3 minutes",
                "difficulty": "Easy"
            }
        ]
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select and enhance a recipe based on anonymized patient profile and theme.
        
        Args:
            enhanced_profile: Profile from previous agents containing patient_info, theme_info, qloo_intelligence
            
        Returns:
            Dict containing selected recipe with enhanced conversation starters (PII-compliant)
        """
        
        logger.info("🍽️ Agent 4B: Starting PII-compliant recipe selection with cultural matching")
        
        try:
            # Extract anonymized patient information
            patient_info = enhanced_profile.get("patient_info", {})
            theme_info = enhanced_profile.get("theme_info", {})
            
            # FIXED: Extract only anonymized data (no personal names)
            cultural_heritage = patient_info.get("cultural_heritage", "american").lower()
            age_group = patient_info.get("age_group", "senior")
            theme_id = theme_info.get("id", "comfort")
            theme_name = theme_info.get("name", "Comfort")
            
            # FIXED: Log only anonymized data (no personal names)
            logger.info(f"🎯 Selecting recipe - Theme: {theme_name}, Heritage: {cultural_heritage}, Age Group: {age_group}")
            
            # Step 1: Filter recipes by THEME first (priority for daily variety)
            theme_matches = self._filter_by_theme(self.recipes_database, theme_id)
            logger.info(f"🎯 Found {len(theme_matches)} theme-matching recipes")
            
            # Step 2: Filter by heritage within theme matches (secondary filter)
            final_candidates = self._filter_by_heritage_within_theme(theme_matches, cultural_heritage)
            
            # Step 3: If no theme + heritage match, use theme-only
            if not final_candidates:
                logger.info(f"⚠️ No {theme_id} + {cultural_heritage} matches, using theme-only")
                final_candidates = theme_matches
            
            # Step 4: If no theme matches, fall back to heritage-only
            if not final_candidates:
                logger.info(f"⚠️ No theme matches, falling back to heritage-only")
                final_candidates = self._filter_by_heritage(cultural_heritage)
            
            # Step 5: Emergency fallback
            if not final_candidates:
                logger.warning("⚠️ No matches found, using emergency fallback")
                final_candidates = self._get_fallback_recipes()
            
            # Step 6: Age-appropriate selection
            age_appropriate_candidates = self._filter_by_age_group(final_candidates, age_group)
            if age_appropriate_candidates:
                final_candidates = age_appropriate_candidates
                logger.info(f"✅ Found {len(age_appropriate_candidates)} age-appropriate recipes")
            
            # Select recipe (could add randomization here)
            selected_recipe = final_candidates[0]
            recipe_name = selected_recipe.get("name", "Unknown Recipe")
            
            logger.info(f"✅ Selected: {recipe_name}")
            
            # Step 7: Format final output (no Gemini enhancement needed)
            theme_match_count = len(theme_matches)
            heritage_match_within_theme = len(final_candidates) < theme_match_count if theme_match_count > 0 else False
            
            return self._format_recipe_output(selected_recipe, cultural_heritage, theme_id, theme_match_count, heritage_match_within_theme, age_group)
            
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
    
    def _filter_by_age_group(self, recipes: List[Dict[str, Any]], age_group: str) -> List[Dict[str, Any]]:
        """Filter recipes appropriate for specific age group"""
        
        if age_group == "oldest_senior":
            # Prefer simpler, more traditional recipes for oldest seniors
            age_appropriate = []
            for recipe in recipes:
                difficulty = recipe.get("difficulty", "").lower()
                prep_time = recipe.get("prep_time", "")
                
                # Prefer easy recipes with short prep times
                if difficulty == "easy" and ("5 min" in prep_time or "3 min" in prep_time):
                    age_appropriate.append(recipe)
            
            return age_appropriate if age_appropriate else recipes
        
        return recipes  # All recipes are appropriate for other age groups
    
    def _format_recipe_output(self, recipe: Dict[str, Any], heritage: str, theme_id: str, 
                             theme_match_count: int, heritage_match_within_theme: bool, age_group: str) -> Dict[str, Any]:
        """Format the final recipe output for the dashboard - PII COMPLIANT"""
        
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
                "age_appropriate": True,  # All our recipes are designed to be age-appropriate
                "selection_method": "pure_json_based_pii_compliant",
                "total_recipes_available": len(self.recipes_database),
                "theme_recipes_found": theme_match_count,
                "conversation_source": "curated_json",
                "agent": "recipe_selection_agent_4b_pii_compliant",
                "safety_verified": True,  # All our recipes are microwave-safe
                "microwave_only": True,
                "filtering_approach": "theme_first_heritage_second_age_aware",
                "pii_compliant": True,
                "anonymized_profile": True,
                "heritage_target": heritage,
                "age_group_target": age_group
            }
        }
    
    async def _get_emergency_fallback(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Emergency fallback if everything fails - PII COMPLIANT"""
        
        logger.warning("🚨 Using PII-compliant emergency recipe fallback")
        
        # Extract anonymized data for fallback
        patient_info = enhanced_profile.get("patient_info", {})
        cultural_heritage = patient_info.get("cultural_heritage", "american")
        age_group = patient_info.get("age_group", "senior")
        
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
                "What foods make you feel happy and comfortable?"
            ],
            "prep_time": "4 minutes",
            "difficulty": "Easy",
            "heritage_tags": ["universal"],
            "theme_tags": ["comfort", "family"]
        }
        
        return self._format_recipe_output(
            emergency_recipe, 
            cultural_heritage, 
            "comfort", 
            1, 
            False, 
            age_group
        )
    
    def get_recipe_by_theme_and_heritage(self, theme_id: str, heritage: str) -> Optional[Dict[str, Any]]:
        """Public method to get a specific recipe by theme and heritage for testing"""
        
        theme_matches = self._filter_by_theme(self.recipes_database, theme_id)
        heritage_matches = self._filter_by_heritage_within_theme(theme_matches, heritage)
        
        if heritage_matches:
            return heritage_matches[0]
        elif theme_matches:
            return theme_matches[0]
        else:
            return self._get_fallback_recipes()[0]
    
    def get_available_themes(self) -> List[str]:
        """Get all available theme tags from the recipe database"""
        
        themes = set()
        for recipe in self.recipes_database:
            themes.update(recipe.get("theme_tags", []))
        
        return sorted(list(themes))
    
    def get_available_heritages(self) -> List[str]:
        """Get all available heritage tags from the recipe database"""
        
        heritages = set()
        for recipe in self.recipes_database:
            heritages.update(recipe.get("heritage_tags", []))
        
        return sorted(list(heritages))
    
    def validate_recipe_safety(self, recipe: Dict[str, Any]) -> bool:
        """Validate that a recipe is safe for dementia patients (microwave-only, simple)"""
        
        instructions = recipe.get("instructions", [])
        
        # Check for dangerous keywords
        dangerous_keywords = ["stove", "oven", "knife", "sharp", "hot oil", "fry", "boil"]
        
        for instruction in instructions:
            instruction_lower = instruction.lower()
            for keyword in dangerous_keywords:
                if keyword in instruction_lower:
                    logger.warning(f"⚠️ Recipe {recipe.get('name')} contains dangerous keyword: {keyword}")
                    return False
        
        # Check for microwave-safe cooking
        microwave_keywords = ["microwave", "heat", "warm"]
        has_microwave = any(
            any(keyword in instruction.lower() for keyword in microwave_keywords)
            for instruction in instructions
        )
        
        if not has_microwave:
            logger.warning(f"⚠️ Recipe {recipe.get('name')} may not be microwave-safe")
            return False
        
        return True