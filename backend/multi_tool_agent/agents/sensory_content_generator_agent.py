"""
Sensory Content Generator Agent - FIXED to use theme-based recipes
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

CRITICAL FIX:
- Now uses theme-based recipe filtering from config/theme_config.py
- Loads recipes from config/recipes.json
- Properly filters recipes by theme (e.g., "pets" theme gets pet-related recipes)
- Keeps Gemini AI as fallback only
- Maintains all existing functionality for music/TV content
"""

import logging
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent:
    """
    Agent 4: Generates sensory content using FIXED theme-based recipe system.
    
    FIXED WORKFLOW:
    1. Use theme-based recipe filtering from config/recipes.json
    2. Use Qloo for cultural intelligence (classical composers, vintage TV)
    3. Search YouTube for public domain versions
    4. Fall back to Gemini AI only if theme recipes fail
    """
    
    def __init__(self, gemini_tool=None, youtube_tool=None):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        
        # CRITICAL FIX: Load theme-based recipes
        self.recipes_data = self._load_theme_recipes()
        
        logger.info("🎨 Sensory Content Generator initialized with FIXED theme-based recipe system")
        logger.info("🎼 Focus: Classical music + vintage TV (public domain) + Theme recipes")
    
    def _load_theme_recipes(self) -> list:
        """CRITICAL FIX: Load theme-based recipes from config/recipes.json"""
        try:
            recipes_file = Path(__file__).parent.parent.parent / "config" / "recipes.json"
            if recipes_file.exists():
                with open(recipes_file, 'r') as f:
                    recipes = json.load(f)
                    logger.info(f"✅ FIXED: Loaded {len(recipes)} theme-based recipes")
                    return recipes
            else:
                logger.warning(f"⚠️ Recipe file not found: {recipes_file}")
                return []
        except Exception as e:
            logger.error(f"❌ Error loading theme recipes: {e}")
            return []
    
    async def run(self, consolidated_info: Dict[str, Any], 
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sensory content using FIXED theme-based recipe system.
        """
        
        logger.info("🎨 Agent 4: Generating sensory content with FIXED theme-based recipes")
        
        try:
            # Extract patient information
            patient_profile = consolidated_info.get("patient_profile", {})
            current_theme = consolidated_info.get("daily_theme", {}).get("theme", {})
            
            heritage = patient_profile.get("cultural_heritage", "universal")
            birth_year = patient_profile.get("birth_year", 1945)
            gender = patient_profile.get("gender")
            
            # Calculate age group for Qloo
            current_year = datetime.now().year
            age = current_year - birth_year if birth_year else 80
            age_group = "75_and_older" if age >= 75 else "55_to_74"
            
            logger.info(f"🎯 Generating content for {heritage}, age group {age_group}, theme: {current_theme.get('name', 'Unknown')}")
            
            # Generate content using FIXED pipeline
            sensory_content = await self._generate_fixed_sensory_content(
                heritage=heritage,
                age_group=age_group,
                gender=gender,
                current_theme=current_theme,
                qloo_intelligence=qloo_intelligence
            )
            
            logger.info("✅ Agent 4: FIXED sensory content generated successfully")
            return {
                "sensory_content": sensory_content,
                "generation_metadata": {
                    "content_safety": "THEME_BASED_RECIPES",
                    "heritage": heritage,
                    "age_group": age_group,
                    "pipeline": "theme_recipes_fixed",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._generate_fixed_fallback_content(heritage, current_theme)
    
    async def _generate_fixed_sensory_content(self,
                                            heritage: str,
                                            age_group: str, 
                                            gender: Optional[str],
                                            current_theme: Dict[str, Any],
                                            qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sensory content using FIXED theme-based recipe system.
        """
        
        logger.info("🔄 Starting FIXED theme-based content pipeline")
        
        # Generate classical music content (unchanged)
        music_content = await self._generate_safe_music_content(
            heritage, age_group, gender, current_theme, qloo_intelligence
        )
        
        # Generate vintage TV content (unchanged)
        tv_content = await self._generate_safe_tv_content(
            heritage, age_group, gender, current_theme, qloo_intelligence
        )
        
        # CRITICAL FIX: Generate theme-based recipe content
        recipe_content = await self._generate_theme_based_recipe_content(current_theme)
        
        return {
            "content_by_sense": {
                "auditory": {
                    "elements": [music_content],
                    "primary_focus": "classical_music",
                    "safety_level": "public_domain"
                },
                "visual": {
                    "elements": [tv_content], 
                    "primary_focus": "vintage_television",
                    "safety_level": "public_domain"
                },
                "gustatory": {
                    "elements": [recipe_content],
                    "primary_focus": "theme_based_recipes",
                    "safety_level": "theme_filtered"
                }
            },
            "content_safety": {
                "copyright_status": "SAFE",
                "music_type": "classical_public_domain", 
                "tv_type": "vintage_public_domain",
                "recipe_type": "theme_based_filtered"
            }
        }
    
    async def _generate_theme_based_recipe_content(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """CRITICAL FIX: Generate recipe content using theme-based filtering"""
        
        theme_id = current_theme.get("id", "family")
        theme_name = current_theme.get("name", "Family")
        
        logger.info(f"🍽️ FIXED: Generating theme-based recipe for '{theme_name}' (ID: {theme_id})")
        
        try:
            if not self.recipes_data:
                logger.warning("⚠️ No theme recipes loaded, using Gemini fallback")
                return await self._generate_gemini_recipe_fallback(current_theme)
            
            # CRITICAL FIX: Filter recipes by theme
            theme_recipes = self._filter_recipes_by_theme(self.recipes_data, theme_id)
            
            if not theme_recipes:
                logger.warning(f"⚠️ No recipes found for theme '{theme_id}', using Gemini fallback")
                return await self._generate_gemini_recipe_fallback(current_theme)
            
            # Select the first matching recipe (could be randomized later)
            selected_recipe = theme_recipes[0]
            recipe_name = selected_recipe.get("name", "Unknown Recipe")
            
            logger.info(f"✅ FIXED: Selected theme recipe: {recipe_name} for theme '{theme_name}'")
            
            # Convert recipe format to expected structure
            return {
                "name": recipe_name,
                "ingredients": self._format_ingredients(selected_recipe.get("ingredients", [])),
                "instructions": self._format_instructions(selected_recipe.get("instructions", [])),
                "prep_time": "15 minutes",  # Default since not in recipe data
                "difficulty": "Easy",
                "cultural_context": selected_recipe.get("notes", {}).get("text", ""),
                "conversation_starters": selected_recipe.get("conversation_starters", []),
                "theme_connection": f"Perfect for {theme_name} theme",
                "source": "theme_based_filtered"
            }
            
        except Exception as e:
            logger.error(f"❌ FIXED theme recipe generation failed: {e}")
            return await self._generate_gemini_recipe_fallback(current_theme)
    
    def _filter_recipes_by_theme(self, recipes: list, theme_id: str) -> list:
        """CRITICAL FIX: Filter recipes by theme ID"""
        
        matching_recipes = []
        
        for recipe in recipes:
            # Check if recipe has explicit theme field that matches
            recipe_theme = None
            
            # Look for theme in notes
            notes = recipe.get("notes", {})
            if isinstance(notes, dict):
                recipe_theme = notes.get("theme")
            
            if recipe_theme == theme_id:
                matching_recipes.append(recipe)
                logger.debug(f"✅ FIXED: Recipe '{recipe.get('name')}' matches theme '{theme_id}'")
        
        logger.info(f"🔍 FIXED: Found {len(matching_recipes)} recipes for theme '{theme_id}'")
        return matching_recipes
    
    def _format_ingredients(self, ingredients: list) -> list:
        """Convert simple ingredient list to structured format"""
        formatted = []
        for ingredient in ingredients:
            if isinstance(ingredient, str):
                formatted.append({
                    "amount": "As needed",
                    "item": ingredient,
                    "location": "pantry"
                })
            else:
                formatted.append(ingredient)
        return formatted
    
    def _format_instructions(self, instructions: list) -> list:
        """Convert simple instruction list to structured format"""
        formatted = []
        for i, instruction in enumerate(instructions):
            if isinstance(instruction, str):
                formatted.append({
                    "step": i + 1,
                    "instruction": instruction,
                    "difficulty": "easy"
                })
            else:
                formatted.append(instruction)
        return formatted
    
    async def _generate_gemini_recipe_fallback(self, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback to Gemini AI recipe generation"""
        
        logger.info("🔄 FIXED: Falling back to Gemini AI for recipe generation")
        
        try:
            if self.gemini_tool:
                theme_name = current_theme.get("name", "comfort")
                heritage = "universal"
                
                recipe_result = await self.gemini_tool.get_recipe_suggestion(
                    cultural_heritage=heritage,
                    theme_context=f"Simple recipe for {theme_name} theme"
                )
                
                if recipe_result:
                    return {
                        "name": recipe_result.get("name", "Comfort Recipe"),
                        "ingredients": recipe_result.get("ingredients", []),
                        "instructions": recipe_result.get("instructions", []),
                        "prep_time": recipe_result.get("total_time", "30 minutes"),
                        "difficulty": "Easy",
                        "cultural_context": "Generated recipe",
                        "source": "gemini_fallback"
                    }
        
        except Exception as e:
            logger.error(f"❌ Gemini fallback also failed: {e}")
        
        # Final fallback
        return self._get_hardcoded_recipe_fallback()
    
    def _get_hardcoded_recipe_fallback(self) -> Dict[str, Any]:
        """Final hardcoded recipe fallback"""
        return {
            "name": "Warm Apple Slices",
            "ingredients": [
                {"amount": "2", "item": "apples", "location": "fresh"},
                {"amount": "1 tsp", "item": "cinnamon", "location": "spice_rack"}
            ],
            "instructions": [
                {"step": 1, "instruction": "Slice apples thinly", "difficulty": "easy"},
                {"step": 2, "instruction": "Sprinkle with cinnamon", "difficulty": "easy"},
                {"step": 3, "instruction": "Microwave for 30 seconds", "difficulty": "easy"}
            ],
            "prep_time": "5 minutes",
            "difficulty": "Easy",
            "cultural_context": "A simple, comforting treat",
            "source": "hardcoded_fallback"
        }
    
    # Keep all existing music and TV methods unchanged
    async def _generate_safe_music_content(self,
                                         heritage: str,
                                         age_group: str,
                                         gender: Optional[str], 
                                         current_theme: Dict[str, Any],
                                         qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safe classical music content (unchanged)"""
        
        logger.info(f"🎼 Generating safe classical music for {heritage}")
        
        try:
            # Try to get Qloo classical recommendations from existing intelligence
            classical_recommendations = self._extract_classical_from_qloo(qloo_intelligence, heritage)
            
            # Search YouTube for public domain classical content
            if self.youtube_tool:
                youtube_result = await self.youtube_tool.search_public_domain_classical(
                    classical_recommendations
                )
                
                if youtube_result and youtube_result.get("items"):
                    item = youtube_result["items"][0]
                    snippet = item.get("snippet", {})
                    
                    return {
                        "name": snippet.get("title", "Classical Music"),
                        "artist": snippet.get("channelTitle", "Classical Composer"),
                        "youtube_url": item.get("embeddable_url", ""),
                        "genre": "Classical",
                        "era": "Public Domain",
                        "theme_relevance": current_theme.get("name", "Memory"),
                        "safety_status": "public_domain",
                        "source": "qloo_youtube_classical"
                    }
            
            # Fallback to safe classical content
            return self._get_classical_music_fallback(heritage)
            
        except Exception as e:
            logger.error(f"Error generating safe music: {e}")
            return self._get_classical_music_fallback(heritage)
    
    async def _generate_safe_tv_content(self,
                                      heritage: str,
                                      age_group: str,
                                      gender: Optional[str],
                                      current_theme: Dict[str, Any],
                                      qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Generate safe vintage TV content (unchanged)"""
        
        logger.info(f"📺 Generating safe vintage TV for {heritage}")
        
        try:
            # Try to get vintage TV recommendations from Qloo
            vintage_recommendations = self._extract_vintage_tv_from_qloo(qloo_intelligence)
            
            # Search YouTube for public domain vintage TV
            if self.youtube_tool:
                youtube_result = await self.youtube_tool.search_public_domain_vintage_tv(
                    vintage_recommendations
                )
                
                if youtube_result and youtube_result.get("items"):
                    item = youtube_result["items"][0]
                    snippet = item.get("snippet", {})
                    
                    return {
                        "name": snippet.get("title", "Classic Television"),
                        "youtube_url": item.get("embeddable_url", ""),
                        "description": snippet.get("description", "Vintage family entertainment"),
                        "era": "1940s-1950s",
                        "theme_relevance": current_theme.get("name", "Memory"),
                        "safety_status": "public_domain",
                        "source": "qloo_youtube_vintage"
                    }
            
            # Fallback to safe vintage content
            return self._get_vintage_tv_fallback()
            
        except Exception as e:
            logger.error(f"Error generating safe TV: {e}")
            return self._get_vintage_tv_fallback()
    
    def _extract_classical_from_qloo(self, qloo_intelligence: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Extract classical music recommendations from Qloo data (unchanged)"""
        
        # Look for classical composers in Qloo results
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        artists_data = cultural_recommendations.get("artists", {})
        entities = artists_data.get("entities", [])
        
        classical_entities = []
        classical_keywords = ["classical", "opera", "symphony", "baroque", "romantic"]
        
        for entity in entities:
            name = entity.get("name", "").lower()
            tags = [tag.get("name", "").lower() for tag in entity.get("tags", [])]
            
            # Check if it's classical music
            is_classical = any(keyword in name or any(keyword in tag for tag in tags)
                              for keyword in classical_keywords)
            
            if is_classical:
                classical_entities.append(entity)
        
        return {
            "success": len(classical_entities) > 0,
            "entities": classical_entities,
            "heritage": heritage
        }
    
    def _extract_vintage_tv_from_qloo(self, qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Extract vintage TV recommendations from Qloo data (unchanged)"""
        
        cultural_recommendations = qloo_intelligence.get("cultural_recommendations", {})
        tv_data = cultural_recommendations.get("tv_shows", {})
        entities = tv_data.get("entities", [])
        
        vintage_entities = []
        vintage_keywords = ["classic", "vintage", "1940", "1950", "1960", "anthology", "variety"]
        
        for entity in entities:
            name = entity.get("name", "").lower()
            tags = [tag.get("name", "").lower() for tag in entity.get("tags", [])]
            
            # Check if it's vintage content
            is_vintage = any(keyword in name or any(keyword in tag for tag in tags)
                            for keyword in vintage_keywords)
            
            if is_vintage:
                vintage_entities.append(entity)
        
        return {
            "success": len(vintage_entities) > 0,
            "entities": vintage_entities
        }
    
    def _get_classical_music_fallback(self, heritage: str) -> Dict[str, Any]:
        """Safe classical music fallback (unchanged)"""
        
        heritage_composers = {
            "Italian-American": {"artist": "Vivaldi", "name": "Four Seasons"},
            "German": {"artist": "Beethoven", "name": "Moonlight Sonata"},
            "universal": {"artist": "Mozart", "name": "Eine kleine Nachtmusik"}
        }
        
        composer_info = heritage_composers.get(heritage, heritage_composers["universal"])
        
        return {
            "name": composer_info["name"],
            "artist": composer_info["artist"],
            "youtube_url": "",  # No specific URL for safety
            "genre": "Classical",
            "era": "Public Domain",
            "safety_status": "classical_fallback",
            "source": "safe_fallback"
        }
    
    def _get_vintage_tv_fallback(self) -> Dict[str, Any]:
        """Safe vintage TV fallback (unchanged)"""
        return {
            "name": "Classic Family Variety Show",
            "youtube_url": "",  # No specific URL for safety
            "description": "Wholesome family entertainment from the 1950s",
            "era": "1950s",
            "safety_status": "vintage_fallback",
            "source": "safe_fallback"
        }
    
    def _generate_fixed_fallback_content(self, heritage: str, current_theme: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete FIXED fallback content"""
        return {
            "sensory_content": {
                "content_by_sense": {
                    "auditory": {
                        "elements": [self._get_classical_music_fallback(heritage)],
                        "safety_level": "public_domain"
                    },
                    "visual": {
                        "elements": [self._get_vintage_tv_fallback()],
                        "safety_level": "public_domain"
                    },
                    "gustatory": {
                        "elements": [self._get_hardcoded_recipe_fallback()],
                        "safety_level": "theme_fallback"
                    }
                }
            },
            "generation_metadata": {
                "content_safety": "FIXED_THEME_FALLBACK",
                "pipeline": "theme_recipes_fallback"
            }
        }

# Export the main class
__all__ = ["SensoryContentGeneratorAgent"]