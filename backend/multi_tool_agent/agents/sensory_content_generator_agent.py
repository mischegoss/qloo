"""
Sensory Content Generator Agent with LIMITED API Calls - RATE LIMITING SOLUTION
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

FIXES:
- Only use FIRST/BEST result from Qloo (not all results)
- Only make ONE YouTube call per dashboard refresh
- Only make ONE Gemini call per dashboard refresh (with caching)
- Early exit strategies to prevent unnecessary API calls
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
    Agent 4: Sensory Content Generator with LIMITED API calls to prevent rate limiting.
    
    RATE LIMITING FIXES:
    - Uses ONLY the first/best Qloo result (not multiple)
    - Makes maximum 1 YouTube call per dashboard refresh
    - Makes maximum 1 Gemini call per dashboard refresh
    - Leverages daily caching in both APIs
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with LIMITED API calls")
    
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
        Generate sensory content with LIMITED API calls to prevent rate limiting.
        
        RATE LIMITING STRATEGY:
        - Extract ONLY first/best results from Qloo
        - Make maximum 1 YouTube API call
        - Make maximum 1 Gemini API call  
        - Use caching for daily consistency
        """
        
        try:
            logger.info("🎵 Agent 4: Starting LIMITED sensory content generation")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            age = patient_profile.get("age", 75)
            birth_year = patient_profile.get("birth_year")
            if birth_year:
                age = 2024 - birth_year
            
            qloo_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # RATE LIMITING: Extract ONLY first/best results from Qloo
            first_artist = self._get_first_qloo_result(qloo_recommendations, "artists")
            first_tv_show = self._get_first_qloo_result(qloo_recommendations, "tv_shows")
            first_place = self._get_first_qloo_result(qloo_recommendations, "places")
            
            logger.info(f"LIMITED extraction - Artist: {first_artist.get('name') if first_artist else 'None'}")
            logger.info(f"LIMITED extraction - TV: {first_tv_show.get('name') if first_tv_show else 'None'}")
            logger.info(f"LIMITED extraction - Place: {first_place.get('name') if first_place else 'None'}")
            
            # Generate content for each sense with LIMITED API calls
            sensory_content = {}
            
            # TASTE: ONE Gemini call maximum with caching
            sensory_content["gustatory"] = await self._generate_limited_recipe(heritage, age)
            
            # SOUND: ONE YouTube call maximum with caching
            sensory_content["auditory"] = await self._generate_limited_music_content(heritage, first_artist)
            
            # SIGHT: Use Qloo data only (no additional API calls)
            sensory_content["visual"] = self._generate_visual_from_qloo_only(first_tv_show, heritage)
            
            # SMELL & TOUCH: No API calls (static data)
            sensory_content["olfactory"] = self._generate_olfactory_content(heritage)
            sensory_content["tactile"] = self._generate_tactile_content(heritage)
            
            return {
                "sensory_content": {
                    "content_by_sense": sensory_content,
                    "sensory_summary": self._create_sensory_summary(sensory_content),
                    "generation_metadata": {
                        "heritage_used": heritage,
                        "age_optimized_for": age,
                        "rate_limiting_applied": True,
                        "max_api_calls": {
                            "youtube": 1,
                            "gemini": 1,
                            "qloo": 0  # Already called by Agent 3
                        },
                        "generation_timestamp": datetime.now().isoformat(),
                        "agent_version": "limited_api_calls"
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    def _get_first_qloo_result(self, qloo_recommendations: Dict[str, Any], category: str) -> Optional[Dict[str, Any]]:
        """Extract ONLY the first/best result from Qloo to limit downstream API calls."""
        
        category_data = qloo_recommendations.get(category, {})
        
        if category_data.get("available") and category_data.get("entities"):
            entities = category_data["entities"]
            if entities:
                first_result = entities[0]  # Take ONLY the first result
                logger.info(f"Using first {category} result: {first_result.get('name', 'Unknown')}")
                return first_result
        
        logger.info(f"No {category} results available from Qloo")
        return None
    
    async def _generate_limited_recipe(self, heritage: str, age: int) -> Dict[str, Any]:
        """
        Generate recipe with LIMITED Gemini calls (maximum 1 per day via caching).
        """
        
        try:
            logger.info(f"LIMITED recipe generation for {heritage} heritage")
            
            # Step 1: Select appropriate base recipe (no API call)
            base_recipe = self._select_base_recipe(heritage, age)
            
            # Step 2: ONE Gemini call maximum (cached daily)
            customized_recipe = await self._apply_limited_customization(base_recipe, heritage, age)
            
            # Step 3: Format response
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
                    "source": "recipes_json_limited_customization",
                    "base_recipe": base_recipe["name"]
                }]
                
                return {
                    "sense_type": "gustatory", 
                    "available": True,
                    "elements": recipe_elements,
                    "api_calls_made": 1 if customized_recipe else 0,
                    "caching_used": True
                }
            else:
                # Use base recipe without customization
                logger.info("Using base recipe without Gemini customization")
                return self._format_base_recipe(base_recipe, heritage)
                
        except Exception as e:
            logger.error(f"LIMITED recipe generation failed: {e}")
            return self._format_base_recipe(random.choice(self.recipes_data), heritage)
    
    async def _apply_limited_customization(self, base_recipe: Dict[str, Any], heritage: str, age: int) -> Optional[Dict[str, Any]]:
        """Apply customization with LIMITED Gemini calls (cached daily)."""
        
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
            
            # ONE Gemini call maximum (with daily caching built into the tool)
            customized = await self.gemini_tool.generate_recipe(
                customization_prompt, 
                heritage=heritage, 
                base_recipe_name=base_recipe["name"]
            )
            
            if customized and isinstance(customized, dict):
                logger.info(f"LIMITED Gemini customization successful: {customized.get('name')}")
                return customized
            else:
                logger.info("LIMITED Gemini customization returned invalid format - using base recipe")
                return None
                
        except Exception as e:
            logger.warning(f"LIMITED Gemini customization failed: {e}")
            return None
    
    async def _generate_limited_music_content(self, heritage: str, first_artist: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate music content with LIMITED YouTube calls (maximum 1)."""
        
        try:
            # If we have a Qloo artist, use it for ONE YouTube search
            if first_artist and first_artist.get("name"):
                artist_name = first_artist["name"]
                logger.info(f"LIMITED YouTube search for first artist: {artist_name}")
                
                # ONE YouTube call maximum (with daily caching built into the tool)
                youtube_results = await self.youtube_tool.search_music(f"{artist_name} classic songs", max_results=3)
                
                if youtube_results and youtube_results.get("items"):
                    music_elements = []
                    for item in youtube_results["items"]:  # Use all results from the single call
                        music_elements.append({
                            "title": item.get("snippet", {}).get("title", "Classic Song"),
                            "description": item.get("snippet", {}).get("description", "")[:100],
                            "id": item.get("id", {}),
                            "cultural_relevance": "high",
                            "source": "limited_qloo_youtube",
                            "artist_source": artist_name
                        })
                    
                    return {
                        "sense_type": "auditory",
                        "available": True, 
                        "elements": music_elements,
                        "api_calls_made": 1,
                        "caching_used": True,
                        "artist_used": artist_name
                    }
            
            # Fallback: No YouTube call, use heritage-based suggestion
            logger.info("No Qloo artist available - using fallback music suggestion")
            return {
                "sense_type": "auditory",
                "available": True,
                "elements": [{
                    "title": f"{heritage} Traditional Music",
                    "description": f"Gentle traditional {heritage} music",
                    "source": "heritage_fallback_no_api",
                    "cultural_relevance": "high"
                }],
                "api_calls_made": 0,
                "fallback_used": True
            }
        
        except Exception as e:
            logger.error(f"LIMITED music content generation failed: {e}")
            # Return fallback without any API calls
            return {
                "sense_type": "auditory",
                "available": True,
                "elements": [{
                    "title": f"{heritage} Music",
                    "description": "Traditional background music",
                    "source": "error_fallback_no_api"
                }],
                "api_calls_made": 0,
                "fallback_used": True
            }
    
    def _generate_visual_from_qloo_only(self, first_tv_show: Optional[Dict[str, Any]], heritage: str) -> Dict[str, Any]:
        """Generate visual content using ONLY Qloo data (no additional API calls)."""
        
        visual_elements = []
        
        try:
            # Use the first TV show from Qloo (no additional API calls)
            if first_tv_show and first_tv_show.get("name"):
                show_name = first_tv_show["name"]
                
                visual_elements.append({
                    "content_type": "tv_show",
                    "title": show_name,
                    "description": first_tv_show.get("properties", {}).get("description", f"Classic show: {show_name}")[:100],
                    "cultural_relevance": "high",
                    "source": "qloo_only_no_additional_api",
                    "viewing_notes": ["Watch together", "Pause for discussion", "Choose comfortable time"]
                })
        except Exception as e:
            logger.warning(f"TV show visual content failed: {e}")
        
        # Add heritage photo suggestions (no API calls)
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
            "source": "heritage_based_no_api"
        })
        
        return {
            "sense_type": "visual",
            "available": True if visual_elements else False,
            "elements": visual_elements,
            "api_calls_made": 0,
            "data_source": "qloo_only"
        }
    
    def _select_base_recipe(self, heritage: str, age: int) -> Dict[str, Any]:
        """Select most appropriate base recipe from JSON (no API calls)."""
        
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
    
    def _format_base_recipe(self, base_recipe: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Format base recipe without customization (no API calls)."""
        
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
            "source": "recipes_json_base_no_customization"
        }]
        
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": recipe_elements,
            "api_calls_made": 0,
            "customization_applied": False
        }
    
    def _generate_olfactory_content(self, heritage: str) -> Dict[str, Any]:
        """Generate cultural scent experiences (no API calls)."""
        
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
            "api_calls_made": 0
        }
    
    def _generate_tactile_content(self, heritage: str) -> Dict[str, Any]:
        """Generate tactile experiences (no API calls)."""
        
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
            "api_calls_made": 0
        }
    
    def _create_sensory_summary(self, sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create summary of generated sensory content."""
        
        available_senses = [sense for sense, data in sensory_content.items() if data.get("available")]
        total_elements = sum(len(data.get("elements", [])) for data in sensory_content.values())
        total_api_calls = sum(data.get("api_calls_made", 0) for data in sensory_content.values())
        
        return {
            "total_senses_activated": len(available_senses),
            "available_senses": available_senses,
            "total_content_elements": total_elements,
            "total_api_calls_made": total_api_calls,
            "rate_limiting_applied": True,
            "cross_sensory_potential": len(available_senses) >= 3,
            "generation_success": len(available_senses) >= 2
        }
    
    def _create_fallback_sensory_content(self, consolidated_info: Dict[str, Any], cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails (no API calls)."""
        
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
                            "source": "fallback_no_api"
                        }],
                        "api_calls_made": 0,
                        "fallback_used": True
                    }
                },
                "sensory_summary": {
                    "total_senses_activated": 2,
                    "available_senses": ["gustatory", "auditory"],
                    "total_api_calls_made": 0,
                    "generation_success": True,
                    "rate_limiting_applied": True
                },
                "generation_metadata": {
                    "heritage_used": heritage,
                    "status": "fallback_no_api_calls",
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
        }