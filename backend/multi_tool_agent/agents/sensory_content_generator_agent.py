"""
Sensory Content Generator Agent with LIMITED API Calls - FIXED DATA STRUCTURE
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

FIXES:
- Only use FIRST/BEST result from Qloo (not all results)
- Only make ONE YouTube call per dashboard refresh
- Only make ONE Gemini call per dashboard refresh (with caching)
- FIXED: Ensure gustatory content has proper 'elements' structure for Agent 6
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
    
    DATA STRUCTURE FIXES:
    - Ensures gustatory content has proper 'elements' array for Agent 6
    - Maintains consistent structure across all sensory content
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with LIMITED API calls and FIXED data structure")
    
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
            },
            {
                "name": "Simple Comfort Bread",
                "ingredients": ["2 slices bread", "1 tbsp butter", "Dash cinnamon"],
                "instructions": ["Toast bread lightly", "Spread butter while warm", "Sprinkle with cinnamon"],
                "notes": "Simple, comforting, and familiar."
            }
        ]
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any], 
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate sensory content with LIMITED API calls and FIXED data structure.
        
        RATE LIMITING STRATEGY:
        - Extract ONLY first/best results from Qloo
        - Make maximum 1 YouTube API call
        - Make maximum 1 Gemini API call  
        - Use caching for daily consistency
        
        DATA STRUCTURE FIX:
        - Ensure gustatory content returns proper 'elements' array
        """
        
        try:
            logger.info("🎵 Agent 4: Starting LIMITED sensory content generation with FIXED structure")
            
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
            
            # TASTE: ONE Gemini call maximum with caching - FIXED STRUCTURE
            sensory_content["gustatory"] = await self._generate_limited_recipe_FIXED(heritage, age)
            
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
                        "data_structure_fixed": True,
                        "max_api_calls": {
                            "youtube": 1,
                            "gemini": 1,
                            "qloo": 0  # Already called by Agent 3
                        },
                        "generation_timestamp": datetime.now().isoformat(),
                        "agent_version": "limited_api_calls_fixed_structure"
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
    
    async def _generate_limited_recipe_FIXED(self, heritage: str, age: int) -> Dict[str, Any]:
        """
        Generate recipe with LIMITED Gemini calls (maximum 1 per day via caching).
        FIXED: Returns proper 'elements' structure for Agent 6.
        """
        
        try:
            logger.info(f"LIMITED recipe generation for {heritage} heritage with FIXED structure")
            
            # Step 1: Select appropriate base recipe (no API call)
            base_recipe = self._select_base_recipe(heritage, age)
            
            # Step 2: ONE Gemini call maximum (cached daily)
            customized_recipe = await self._apply_limited_customization(base_recipe, heritage, age)
            
            # Step 3: Format response with FIXED structure (elements array)
            if customized_recipe:
                recipe_element = {
                    "content_type": "customized_recipe",
                    "name": customized_recipe.get("name", base_recipe["name"]),
                    "description": customized_recipe.get("description", f"Simple {heritage} comfort recipe"),
                    "total_time": customized_recipe.get("total_time", "20 minutes"),
                    "difficulty": "very_easy",
                    "ingredients": customized_recipe.get("ingredients", base_recipe["ingredients"]),
                    "instructions": customized_recipe.get("instructions", base_recipe["instructions"]),
                    "cultural_context": customized_recipe.get("cultural_context", f"Traditional {heritage} comfort food"),
                    "heritage_connection": customized_recipe.get("heritage_connection", base_recipe.get("notes", "")),
                    "nostalgic_description": customized_recipe.get("description", base_recipe.get("notes", "")),
                    "source": "recipes_json_limited_customization",
                    "base_recipe": base_recipe["name"],
                    "youtube_url": customized_recipe.get("youtube_url", "")
                }
                
                # FIXED: Return with proper 'elements' array structure
                return {
                    "sense_type": "gustatory", 
                    "available": True,
                    "elements": [recipe_element],  # FIXED: Array with single recipe element
                    "api_calls_made": 1,
                    "customization_applied": True,
                    "caching_used": True
                }
            else:
                # Use base recipe without customization - FIXED STRUCTURE
                logger.info("Using base recipe without Gemini customization")
                return self._format_base_recipe_FIXED(base_recipe, heritage)
                
        except Exception as e:
            logger.error(f"LIMITED recipe generation failed: {e}")
            return self._format_base_recipe_FIXED(random.choice(self.recipes_data), heritage)
    
    def _format_base_recipe_FIXED(self, base_recipe: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Format base recipe without customization (no API calls) - FIXED STRUCTURE."""
        
        recipe_element = {
            "content_type": "base_recipe",
            "name": f"Simple {heritage} {base_recipe['name']}",
            "description": f"Comforting {heritage} style {base_recipe['name'].lower()}",
            "total_time": "20 minutes",
            "difficulty": "very_easy",
            "ingredients": base_recipe["ingredients"],
            "instructions": base_recipe["instructions"],
            "cultural_context": f"Traditional {heritage} comfort food",
            "heritage_connection": base_recipe.get("notes", "Simple, familiar comfort food"),
            "nostalgic_description": base_recipe.get("notes", "Simple, familiar comfort food"),
            "source": "recipes_json_base_no_customization",
            "youtube_url": ""
        }
        
        # FIXED: Return with proper 'elements' array structure
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": [recipe_element],  # FIXED: Array with single recipe element
            "api_calls_made": 0,
            "customization_applied": False
        }
    
    def _select_base_recipe(self, heritage: str, age: int) -> Dict[str, Any]:
        """Select culturally appropriate base recipe without API calls."""
        
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
            # Step 1: Determine search query (no API call)
            if first_artist:
                search_query = first_artist["name"]
                logger.info(f"LIMITED music search for Qloo artist: {search_query}")
            else:
                # Fallback to heritage-based search
                heritage_music = {
                    "Italian-American": "Frank Sinatra Dean Martin",
                    "Irish-American": "Celtic Irish traditional",
                    "Mexican-American": "mariachi traditional Mexican",
                    "German-American": "polka traditional German",
                    "American": "classic American standards"
                }
                search_query = heritage_music.get(heritage, "classic nostalgic music")
                logger.info(f"LIMITED music search for heritage {heritage}: {search_query}")
            
            # Step 2: ONE YouTube call maximum (cached daily)
            youtube_results = await self.youtube_tool.search_music(search_query, max_results=3)
            
            # Step 3: Format response
            if youtube_results and youtube_results.get("items"):
                music_elements = []
                for item in youtube_results["items"][:2]:  # Limit to 2 results
                    snippet = item.get("snippet", {})
                    video_id = item.get("id", {}).get("videoId", "")
                    
                    music_elements.append({
                        "content_type": "youtube_music",
                        "title": snippet.get("title", "Classic Music"),
                        "artist": first_artist["name"] if first_artist else "Classic Artist",
                        "description": snippet.get("description", "Nostalgic music from the era")[:200],
                        "youtube_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
                        "thumbnail_url": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                        "cultural_context": f"Music popular in {heritage} heritage",
                        "source": "youtube_limited_search"
                    })
                
                return {
                    "sense_type": "auditory",
                    "available": True,
                    "elements": music_elements,
                    "api_calls_made": 1,
                    "search_query_used": search_query
                }
            else:
                # Fallback without API calls
                logger.info("LIMITED music generation using fallback (no YouTube results)")
                return self._generate_music_fallback(heritage, first_artist)
                
        except Exception as e:
            logger.error(f"LIMITED music generation failed: {e}")
            return self._generate_music_fallback(heritage, first_artist)
    
    def _generate_music_fallback(self, heritage: str, first_artist: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate music fallback without API calls."""
        
        if first_artist:
            title = f"Music by {first_artist['name']}"
            description = f"Classic songs by {first_artist['name']}"
        else:
            title = f"{heritage} Traditional Music"
            description = f"Classic {heritage} music and songs"
        
        fallback_element = {
            "content_type": "music_fallback",
            "title": title,
            "artist": first_artist["name"] if first_artist else "Classic Artist",
            "description": description,
            "youtube_url": "",
            "cultural_context": f"Traditional {heritage} music",
            "source": "fallback_no_api"
        }
        
        return {
            "sense_type": "auditory",
            "available": True,
            "elements": [fallback_element],
            "api_calls_made": 0,
            "fallback_used": True
        }
    
    def _generate_visual_from_qloo_only(self, first_tv_show: Optional[Dict[str, Any]], heritage: str) -> Dict[str, Any]:
        """Generate visual content using only Qloo data (no additional API calls)."""
        
        visual_elements = []
        
        if first_tv_show:
            visual_elements.append({
                "content_type": "tv_show_qloo",
                "title": first_tv_show.get("name", "Classic TV Show"),
                "description": first_tv_show.get("description", "Entertainment from the era"),
                "cultural_context": f"Popular show in {heritage} heritage",
                "era": first_tv_show.get("era", "Classic Era"),
                "source": "qloo_intelligence_only"
            })
        else:
            # Heritage-based fallback
            heritage_shows = {
                "Italian-American": "Classic variety shows and family entertainment",
                "Irish-American": "Traditional storytelling and music shows",
                "Mexican-American": "Family variety shows and cultural programming",
                "German-American": "Community and cultural programming",
                "American": "Classic American television and variety shows"
            }
            
            visual_elements.append({
                "content_type": "visual_fallback",
                "title": f"{heritage} Traditional Entertainment",
                "description": heritage_shows.get(heritage, "Classic television programming"),
                "cultural_context": f"Entertainment popular in {heritage} culture",
                "source": "heritage_fallback_no_api"
            })
        
        return {
            "sense_type": "visual",
            "available": True,
            "elements": visual_elements,
            "api_calls_made": 0,
            "qloo_based": True
        }
    
    def _generate_olfactory_content(self, heritage: str) -> Dict[str, Any]:
        """Generate cultural scent experiences (no API calls)."""
        
        heritage_scents = {
            "Italian-American": ["garlic and herbs", "fresh basil", "baking bread", "tomato sauce"],
            "Mexican-American": ["cumin and chili", "fresh cilantro", "corn tortillas", "lime"],
            "Irish-American": ["fresh baked soda bread", "hearty stew", "peat fire", "fresh air"],
            "German-American": ["baking bread", "apple strudel", "pine forest", "hearty soup"],
            "American": ["apple pie", "fresh bread", "coffee brewing", "vanilla"]
        }
        
        scents = heritage_scents.get(heritage, heritage_scents["American"])
        
        olfactory_elements = [{
            "content_type": "cultural_scents",
            "title": f"{heritage} Comfort Scents",
            "scents": scents[:3],  # Top 3 scents
            "description": f"Familiar scents from {heritage} heritage",
            "cultural_context": f"Scents that evoke {heritage} memories",
            "source": "cultural_knowledge_static"
        }]
        
        return {
            "sense_type": "olfactory",
            "available": True,
            "elements": olfactory_elements,
            "api_calls_made": 0
        }
    
    def _generate_tactile_content(self, heritage: str) -> Dict[str, Any]:
        """Generate cultural tactile experiences (no API calls)."""
        
        heritage_textures = {
            "Italian-American": ["smooth pasta", "crusty bread", "soft cheese", "warm fabric"],
            "Mexican-American": ["smooth avocado", "textured corn", "soft tortilla", "warm clay"],
            "Irish-American": ["soft wool", "smooth stone", "coarse fabric", "cool metal"],
            "German-American": ["smooth wood", "soft fabric", "cool metal", "warm bread"],
            "American": ["soft cotton", "smooth wood", "warm fabric", "cool metal"]
        }
        
        textures = heritage_textures.get(heritage, heritage_textures["American"])
        
        tactile_elements = [{
            "content_type": "cultural_textures",
            "title": f"{heritage} Comfort Textures",
            "textures": textures[:3],  # Top 3 textures
            "description": f"Familiar textures from {heritage} heritage",
            "cultural_context": f"Textures that evoke {heritage} memories",
            "source": "cultural_knowledge_static"
        }]
        
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
            "data_structure_fixed": True,
            "cross_sensory_potential": len(available_senses) >= 3,
            "generation_success": len(available_senses) >= 2
        }
    
    def _create_fallback_sensory_content(self, consolidated_info: Dict[str, Any], cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails (no API calls) - FIXED STRUCTURE."""
        
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
                    "gustatory": self._format_base_recipe_FIXED(base_recipe, heritage),
                    "auditory": self._generate_music_fallback(heritage, None)
                },
                "sensory_summary": {
                    "total_senses_activated": 2,
                    "available_senses": ["gustatory", "auditory"],
                    "total_api_calls_made": 0,
                    "generation_success": True,
                    "rate_limiting_applied": True,
                    "data_structure_fixed": True
                },
                "generation_metadata": {
                    "heritage_used": heritage,
                    "status": "fallback_no_api_calls_fixed_structure",
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
        }