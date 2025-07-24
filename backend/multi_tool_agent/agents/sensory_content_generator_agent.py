"""
Enhanced Sensory Content Generator Agent with Recipes JSON + Light Customization
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

Agent 4: Uses pre-made recipes from JSON + light Gemini customization for reliability
"""

import logging
import json
import os
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent:
    """
    Agent 4: Sensory Content Generator with Recipes JSON + Light Customization
    
    Uses pre-made recipes from backend/config/recipes.json and applies light cultural
    customization via Gemini for fast, reliable recipe generation.
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with recipes.json + light customization")
    
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
        Generate comprehensive sensory content with recipe selection + light customization.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2  
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Dictionary containing multi-sensory content with customized recipes
        """
        
        try:
            logger.info("🎵 Agent 4: Starting sensory content generation with recipes.json")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            age = patient_profile.get("age", 75)
            birth_year = patient_profile.get("birth_year")
            if birth_year:
                age = 2024 - birth_year
            
            qloo_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # Generate content for each sense
            sensory_content = {}
            
            # TASTE: Select recipe + light customization
            sensory_content["gustatory"] = await self._generate_customized_recipe(
                heritage, age, qloo_recommendations
            )
            
            # SOUND: Era-appropriate music
            sensory_content["auditory"] = await self._generate_era_music_content(
                heritage, qloo_recommendations
            )
            
            # SIGHT: Visual content
            sensory_content["visual"] = await self._generate_visual_content(
                heritage, qloo_recommendations
            )
            
            # SMELL: Cultural scents
            sensory_content["olfactory"] = self._generate_olfactory_content(heritage)
            
            # TOUCH: Tactile experiences
            sensory_content["tactile"] = self._generate_tactile_content(heritage)
            
            return {
                "sensory_content": {
                    "content_by_sense": sensory_content,
                    "sensory_summary": self._create_sensory_summary(sensory_content),
                    "generation_metadata": {
                        "heritage_used": heritage,
                        "age_optimized_for": age,
                        "recipes_json_used": True,
                        "generation_timestamp": datetime.now().isoformat(),
                        "agent_version": "recipes_json_customization"
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    async def _generate_customized_recipe(self, 
                                        heritage: str, 
                                        age: int,
                                        qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Select recipe from JSON and apply light cultural customization.
        """
        
        try:
            logger.info(f"Selecting and customizing recipe for {heritage} heritage, age {age}")
            
            # Step 1: Select appropriate base recipe
            base_recipe = self._select_base_recipe(heritage, age)
            
            # Step 2: Apply light customization via Gemini
            customized_recipe = await self._apply_light_customization(base_recipe, heritage, age)
            
            # Step 3: Format for response
            if customized_recipe:
                recipe_elements = [{
                    "content_type": "customized_recipe",
                    "name": customized_recipe.get("name", base_recipe["name"]),
                    "description": customized_recipe.get("description", f"Simple {heritage} comfort recipe"),
                    "total_time": customized_recipe.get("total_time", "20 minutes"),
                    "difficulty": "very_easy",
                    "ingredients": customized_recipe.get("ingredients", base_recipe["ingredients"]),
                    "instructions": customized_recipe.get("instructions", base_recipe["instructions"]),
                    "cultural_context": customized_recipe.get("cultural_context", f"Traditional {heritage} comfort food"),
                    "heritage_connection": customized_recipe.get("heritage_connection", base_recipe.get("notes", "")),
                    "source": "recipes_json_customized",
                    "base_recipe": base_recipe["name"]
                }]
                
                return {
                    "sense_type": "gustatory", 
                    "available": True,
                    "elements": recipe_elements,
                    "customization_applied": True,
                    "implementation_notes": [
                        "Recipe selected from curated JSON collection",
                        "Culturally customized for individual preferences",
                        "All ingredients are dementia-safe and familiar"
                    ]
                }
            else:
                # If customization fails, use base recipe
                logger.warning("Customization failed, using base recipe")
                return self._format_base_recipe(base_recipe, heritage)
                
        except Exception as e:
            logger.error(f"Recipe customization failed: {e}")
            # Fallback to any base recipe
            return self._format_base_recipe(random.choice(self.recipes_data), heritage)
    
    def _select_base_recipe(self, heritage: str, age: int) -> Dict[str, Any]:
        """Select most appropriate base recipe from JSON."""
        
        # Heritage-based preferences
        heritage_preferences = {
            "Italian-American": ["apple", "oatmeal", "bread", "cocoa"],
            "Mexican-American": ["cinnamon", "cocoa", "banana"],
            "Irish-American": ["oatmeal", "bread", "cocoa"],
            "German-American": ["apple", "bread", "cocoa"],
            "American": ["apple", "oatmeal", "banana", "bread"]
        }
        
        preferred_keywords = heritage_preferences.get(heritage, heritage_preferences["American"])
        
        # Find recipes matching heritage preferences
        matching_recipes = []
        for recipe in self.recipes_data:
            recipe_text = (recipe["name"] + " " + " ".join(recipe["ingredients"])).lower()
            if any(keyword in recipe_text for keyword in preferred_keywords):
                matching_recipes.append(recipe)
        
        # If no matches, use any recipe
        if not matching_recipes:
            matching_recipes = self.recipes_data
        
        # Select random from matching recipes
        selected = random.choice(matching_recipes)
        logger.info(f"Selected base recipe: {selected['name']} for {heritage}")
        return selected
    
    async def _apply_light_customization(self, base_recipe: Dict[str, Any], heritage: str, age: int) -> Optional[Dict[str, Any]]:
        """Apply light cultural customization via Gemini."""
        
        try:
            customization_prompt = f"""
            Take this simple recipe and make small cultural customizations for a {age}-year-old {heritage} person:
            
            Base Recipe: {base_recipe['name']}
            Ingredients: {base_recipe['ingredients']}
            Instructions: {base_recipe['instructions']}
            Original Notes: {base_recipe.get('notes', '')}
            
            Make ONLY these small changes:
            1. Add 1-2 small ingredients/spices that fit {heritage} heritage (optional additions only)
            2. Modify ONE instruction to be more culturally relevant
            3. Add a brief cultural memory connection
            4. Keep it exactly as simple and safe as the original
            5. Do not change cooking method (keep microwave-based)
            
            Return as JSON with same structure:
            {{
                "name": "Modified recipe name (can add heritage reference)",
                "description": "One sentence about cultural comfort and memory",
                "total_time": "Same as original",
                "ingredients": ["Original ingredients with 1-2 optional cultural additions"],
                "instructions": ["Slightly modified instructions"],
                "cultural_context": "Why this connects to {heritage} heritage",
                "heritage_connection": "How this might trigger positive food memories"
            }}
            """
            
            # Try Gemini customization with short timeout
            customized = await self.gemini_tool.generate_recipe(customization_prompt)
            
            if customized and isinstance(customized, dict):
                logger.info(f"Successfully customized recipe: {customized.get('name')}")
                return customized
            else:
                logger.warning("Gemini customization returned invalid format")
                return None
                
        except Exception as e:
            logger.warning(f"Light customization failed: {e}")
            return None
    
    def _format_base_recipe(self, base_recipe: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Format base recipe without customization."""
        
        recipe_elements = [{
            "content_type": "base_recipe",
            "name": f"Simple {heritage} {base_recipe['name']}",
            "description": f"Comforting {heritage} style {base_recipe['name'].lower()}",
            "total_time": "20 minutes",
            "difficulty": "very_easy",
            "ingredients": base_recipe["ingredients"],
            "instructions": base_recipe["instructions"],
            "cultural_context": f"Traditional {heritage} comfort food",
            "heritage_connection": base_recipe.get("notes", "Simple, familiar comfort food"),
            "source": "recipes_json_base"
        }]
        
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": recipe_elements,
            "customization_applied": False,
            "implementation_notes": [
                "Recipe from curated JSON collection",
                "Dementia-safe and microwave-based",
                "Simple, familiar ingredients only"
            ]
        }
    
    async def _generate_era_music_content(self, 
                                        heritage: str,
                                        qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate era-appropriate music content."""
        
        try:
            # Check for Qloo artist recommendations first
            artists_data = qloo_recommendations.get("artists", {})
            
            if artists_data.get("available") and artists_data.get("entities"):
                # Use first Qloo artist recommendation
                artist = artists_data["entities"][0]
                artist_name = artist.get("name", "Classic Artist")
                
                # Search YouTube for this artist
                youtube_results = await self.youtube_tool.search_music(f"{artist_name} classic songs")
                
                if youtube_results and youtube_results.get("items"):
                    music_elements = []
                    for item in youtube_results["items"][:3]:  # Take first 3
                        music_elements.append({
                            "title": item.get("snippet", {}).get("title", "Classic Song"),
                            "description": item.get("snippet", {}).get("description", "")[:100],
                            "id": item.get("id", {}),
                            "cultural_relevance": "high",
                            "source": "qloo_youtube_enhanced"
                        })
                    
                    return {
                        "sense_type": "auditory",
                        "available": True, 
                        "elements": music_elements,
                        "qloo_enhanced": True
                    }
            
            # Fallback to heritage-based music search
            heritage_music_query = f"{heritage} traditional music classics"
            youtube_results = await self.youtube_tool.search_music(heritage_music_query)
            
            if youtube_results and youtube_results.get("items"):
                music_elements = []
                for item in youtube_results["items"][:5]:
                    music_elements.append({
                        "title": item.get("snippet", {}).get("title", "Traditional Music"),
                        "description": item.get("snippet", {}).get("description", "")[:100],
                        "id": item.get("id", {}),
                        "cultural_relevance": "high", 
                        "source": "heritage_youtube"
                    })
                
                return {
                    "sense_type": "auditory",
                    "available": True,
                    "elements": music_elements,
                    "heritage_focused": True
                }
        
        except Exception as e:
            logger.error(f"Music content generation failed: {e}")
        
        # Fallback music suggestion
        return {
            "sense_type": "auditory",
            "available": True,
            "elements": [{
                "title": f"{heritage} Traditional Music",
                "description": f"Gentle traditional {heritage} music",
                "source": "fallback_suggestion",
                "cultural_relevance": "high"
            }],
            "fallback_used": True
        }
    
    async def _generate_visual_content(self, 
                                     heritage: str,
                                     qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content from TV shows."""
        
        visual_elements = []
        
        try:
            # Use Qloo TV show recommendations if available
            tv_data = qloo_recommendations.get("tv_shows", {})
            
            if tv_data.get("available") and tv_data.get("entities"):
                for tv_show in tv_data["entities"][:3]:  # Top 3 shows
                    show_name = tv_show.get("name", "Classic Show")
                    
                    visual_elements.append({
                        "content_type": "tv_show",
                        "title": show_name,
                        "description": tv_show.get("properties", {}).get("description", f"Classic show: {show_name}")[:100],
                        "cultural_relevance": "high",
                        "source": "qloo_recommendation",
                        "viewing_notes": ["Watch together", "Pause for discussion", "Choose comfortable time"]
                    })
        except Exception as e:
            logger.warning(f"TV show visual content failed: {e}")
        
        # Add heritage photo suggestions
        visual_elements.append({
            "content_type": "photo_collection",
            "title": f"{heritage} Heritage Photos",
            "description": f"Traditional images and scenes from {heritage} culture",
            "suggestions": [
                f"Traditional {heritage} landscapes",
                f"{heritage} cultural celebrations", 
                f"Historical {heritage} photography"
            ],
            "cultural_relevance": "high",
            "source": "heritage_based"
        })
        
        return {
            "sense_type": "visual",
            "available": True if visual_elements else False,
            "elements": visual_elements,
            "implementation_notes": [
                "Use good lighting",
                "Ensure comfortable viewing angle", 
                "Consider visual clarity needs"
            ]
        }
    
    def _generate_olfactory_content(self, heritage: str) -> Dict[str, Any]:
        """Generate cultural scent experiences."""
        
        heritage_scents = {
            "Italian-American": ["basil", "oregano", "fresh bread"],
            "Irish-American": ["fresh bread", "tea", "herbs"],
            "Mexican-American": ["cinnamon", "vanilla", "lime"],
            "German-American": ["apple", "pine", "herbs"],
            "American": ["vanilla", "apple pie", "coffee"]
        }
        
        scents = heritage_scents.get(heritage, heritage_scents["American"])
        
        scent_elements = []
        for scent in scents:
            scent_elements.append({
                "scent_type": scent,
                "description": f"Gentle {scent} aroma",
                "source_suggestions": [f"{scent} essential oil", f"fresh {scent}", f"{scent} candle"],
                "cultural_relevance": "traditional",
                "safety_notes": ["Use mild concentrations", "Check for allergies"]
            })
        
        return {
            "sense_type": "olfactory",
            "available": True,
            "elements": scent_elements,
            "implementation_notes": [
                "Use gentle, natural scents",
                "Avoid overwhelming fragrances",
                "Consider personal scent preferences"
            ]
        }
    
    def _generate_tactile_content(self, heritage: str) -> Dict[str, Any]:
        """Generate tactile experiences."""
        
        tactile_elements = [
            {
                "content_type": "fabric_textures",
                "title": "Comfort Fabrics",
                "items": ["soft wool", "cotton", "silk", "fleece"],
                "cultural_connection": f"Traditional {heritage} textiles",
                "implementation": "Provide fabric samples to touch and hold"
            },
            {
                "content_type": "sensory_objects", 
                "title": "Familiar Objects",
                "items": ["smooth stones", "wooden items", "soft brushes", "textured balls"],
                "cultural_connection": "Objects that evoke positive memories",
                "implementation": "Gentle touching and manipulation activities"
            }
        ]
        
        return {
            "sense_type": "tactile",
            "available": True,
            "elements": tactile_elements,
            "implementation_notes": [
                "Ensure objects are clean and safe",
                "Consider temperature preferences",
                "Watch for comfort/discomfort reactions"
            ]
        }
    
    def _create_sensory_summary(self, sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create summary of generated sensory content."""
        
        available_senses = [sense for sense, data in sensory_content.items() if data.get("available")]
        total_elements = sum(len(data.get("elements", [])) for data in sensory_content.values())
        
        return {
            "total_senses_activated": len(available_senses),
            "available_senses": available_senses,
            "total_content_elements": total_elements,
            "cross_sensory_potential": len(available_senses) >= 3,
            "generation_success": len(available_senses) >= 2
        }
    
    def _create_fallback_sensory_content(self, consolidated_info: Dict[str, Any], cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails."""
        
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
                    "gustatory": self._format_base_recipe(base_recipe, heritage),
                    "auditory": {
                        "sense_type": "auditory",
                        "available": True,
                        "elements": [{
                            "title": f"{heritage} Traditional Music",
                            "description": "Gentle background music",
                            "source": "fallback"
                        }],
                        "fallback_used": True
                    }
                },
                "sensory_summary": {
                    "total_senses_activated": 2,
                    "available_senses": ["gustatory", "auditory"],
                    "generation_success": True
                },
                "generation_metadata": {
                    "heritage_used": heritage,
                    "status": "fallback",
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
        }