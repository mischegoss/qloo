"""
Sensory Content Generator Agent - SIMPLIFIED for Dementia Care with ENHANCED LOGGING
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

FIXES:
- Recipes keep original names (no "Italian-American Cinnamon Toast")
- Only improve readability, not change content
- Simple conversation starters for dementia patients
- ENHANCED: Better logging to debug data handoff from Agent 3
- ENHANCED: More robust error handling for missing data
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
    Agent 4: Sensory Content Generator with SIMPLIFIED approach for dementia care.
    
    FIXES:
    - Keeps original recipe names without cultural prefixes
    - Only improves readability, doesn't change recipes significantly
    - Simple, short conversation starters
    - ENHANCED: Better logging and error handling for data handoff issues
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        self.recipes_data = self._load_recipes_json()
        logger.info("Sensory Content Generator initialized with SIMPLIFIED approach")
    
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
        Generate sensory content with SIMPLIFIED approach for dementia care.
        """
        
        try:
            logger.info("🎵 Agent 4: Starting SIMPLIFIED sensory content generation")
            
            # ENHANCED: Debug the qloo_intelligence structure
            logger.info(f"🔍 DEBUG: qloo_intelligence keys: {list(qloo_intelligence.keys())}")
            if "cultural_recommendations" in qloo_intelligence:
                qloo_recs = qloo_intelligence["cultural_recommendations"]
                logger.info(f"🔍 DEBUG: cultural_recommendations keys: {list(qloo_recs.keys())}")
                for category in ["artists", "tv_shows", "places"]:
                    if category in qloo_recs:
                        cat_data = qloo_recs[category]
                        available = cat_data.get("available", False)
                        entity_count = cat_data.get("entity_count", 0)
                        logger.info(f"🔍 DEBUG: {category} - available: {available}, count: {entity_count}")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            age = patient_profile.get("age", 75)
            birth_year = patient_profile.get("birth_year")
            if birth_year:
                age = 2024 - birth_year
            
            qloo_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            # Extract ONLY first/best results from Qloo
            first_artist = self._get_first_qloo_result(qloo_recommendations, "artists")
            first_tv_show = self._get_first_qloo_result(qloo_recommendations, "tv_shows")
            first_place = self._get_first_qloo_result(qloo_recommendations, "places")
            
            logger.info(f"LIMITED extraction - Artist: {first_artist.get('name') if first_artist else 'None'}")
            logger.info(f"LIMITED extraction - TV: {first_tv_show.get('name') if first_tv_show else 'None'}")
            logger.info(f"LIMITED extraction - Place: {first_place.get('name') if first_place else 'None'}")
            
            # Generate content for each sense
            sensory_content = {}
            
            # TASTE: SIMPLIFIED recipe approach
            sensory_content["gustatory"] = await self._generate_simplified_recipe(heritage, age)
            
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
                        "simplified_approach": True,
                        "qloo_data_received": bool(qloo_recommendations),
                        "qloo_categories_available": [k for k, v in qloo_recommendations.items() if isinstance(v, dict) and v.get("available")],
                        "max_api_calls": {
                            "youtube": 1,
                            "gemini": 1,
                            "qloo": 0  # Already called by Agent 3
                        },
                        "generation_timestamp": datetime.now().isoformat(),
                        "agent_version": "simplified_dementia_friendly_enhanced_logging"
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    def _get_first_qloo_result(self, qloo_recommendations: Dict[str, Any], category: str) -> Optional[Dict[str, Any]]:
        """Extract ONLY the first/best result from Qloo to limit downstream API calls."""
        
        category_data = qloo_recommendations.get(category, {})
        
        # ENHANCED: Log what we're looking at
        logger.info(f"🔍 DEBUG: Looking for {category} in qloo_recommendations")
        if category_data:
            logger.info(f"🔍 DEBUG: {category} data keys: {list(category_data.keys())}")
            logger.info(f"🔍 DEBUG: {category} available: {category_data.get('available')}")
            logger.info(f"🔍 DEBUG: {category} entity_count: {category_data.get('entity_count')}")
        
        if category_data.get("available") and category_data.get("entities"):
            entities = category_data["entities"]
            if entities:
                first_result = entities[0]  # Take ONLY the first result
                logger.info(f"✅ Using first {category} result: {first_result.get('name', 'Unknown')}")
                return first_result
        
        logger.info(f"❌ No {category} results available from Qloo")
        return None
    
    async def _generate_simplified_recipe(self, heritage: str, age: int) -> Dict[str, Any]:
        """
        Generate recipe with SIMPLIFIED approach - keep original name, only improve readability.
        """
        
        try:
            logger.info(f"SIMPLIFIED recipe generation for {heritage} heritage")
            
            # Step 1: Select appropriate base recipe (no API call)
            base_recipe = self._select_base_recipe(heritage, age)
            
            # Step 2: ONE Gemini call for readability improvement only
            improved_recipe = await self._improve_recipe_readability_only(base_recipe)
            
            # Step 3: Format response with ORIGINAL NAME
            if improved_recipe:
                recipe_element = {
                    "content_type": "improved_recipe",
                    "name": base_recipe["name"],  # KEEP ORIGINAL NAME
                    "description": improved_recipe.get("description", f"Simple, comforting {base_recipe['name'].lower()}"),
                    "total_time": improved_recipe.get("total_time", "10 minutes"),
                    "difficulty": "very_easy",
                    "ingredients": improved_recipe.get("ingredients", base_recipe["ingredients"]),
                    "instructions": improved_recipe.get("instructions", base_recipe["instructions"]),
                    "cultural_context": f"Comfort food",
                    "heritage_connection": base_recipe.get("notes", "Simple, familiar comfort food"),
                    "nostalgic_description": improved_recipe.get("description", base_recipe.get("notes", "")),
                    "source": "recipes_json_readability_improved",
                    "base_recipe": base_recipe["name"],
                    "youtube_url": "",
                    "theme_connection": "Selected for Dancing theme"  # Add theme connection
                }
                
                return {
                    "sense_type": "gustatory", 
                    "available": True,
                    "elements": [recipe_element],
                    "api_calls_made": 1,
                    "readability_improved": True,
                    "original_name_kept": True
                }
            else:
                # Use base recipe without improvement
                logger.info("Using base recipe without Gemini improvement")
                return self._format_base_recipe_simple(base_recipe, heritage)
                
        except Exception as e:
            logger.error(f"SIMPLIFIED recipe generation failed: {e}")
            return self._format_base_recipe_simple(random.choice(self.recipes_data), heritage)
    
    async def _improve_recipe_readability_only(self, base_recipe: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Improve recipe readability ONLY - no cultural changes, keep original name."""
        
        try:
            readability_prompt = f"""
            Take this recipe and make it easier to read and follow for dementia care patients. 
            
            IMPORTANT RULES:
            1. KEEP THE EXACT SAME NAME: "{base_recipe['name']}"
            2. Do NOT add cultural prefixes like "Italian-American" or "Jewish"
            3. Only improve clarity, safety, and readability
            4. Use simple, clear language
            5. Add safety notes for dementia care
            6. Keep ingredients and method the same
            
            Original Recipe: {base_recipe['name']}
            Ingredients: {base_recipe['ingredients']}
            Instructions: {base_recipe['instructions']}
            Notes: {base_recipe.get('notes', '')}
            
            Return as JSON with same structure but improved readability:
            {{
                "name": "{base_recipe['name']}",
                "description": "One simple sentence about why this is comforting",
                "total_time": "Estimated time",
                "ingredients": ["Clearer ingredient descriptions with safety notes"],
                "instructions": ["Step-by-step with safety guidance"],
                "notes": "Simple memory connection"
            }}
            """
            
            # ONE Gemini call for readability improvement only
            improved = await self.gemini_tool.generate_recipe(
                readability_prompt, 
                heritage="readability", 
                base_recipe_name=base_recipe["name"]
            )
            
            if improved and isinstance(improved, dict):
                # Ensure name wasn't changed
                improved["name"] = base_recipe["name"]  # Force original name
                logger.info(f"SIMPLIFIED readability improvement successful: {improved.get('name')}")
                return improved
            else:
                logger.info("SIMPLIFIED readability improvement failed - using base recipe")
                return None
                
        except Exception as e:
            logger.warning(f"SIMPLIFIED readability improvement failed: {e}")
            return None
    
    def _format_base_recipe_simple(self, base_recipe: Dict[str, Any], heritage: str) -> Dict[str, Any]:
        """Format base recipe with original name (no API calls)."""
        
        recipe_element = {
            "content_type": "base_recipe",
            "name": base_recipe["name"],  # KEEP ORIGINAL NAME
            "description": f"Simple, comforting {base_recipe['name'].lower()}",
            "total_time": "10 minutes",
            "difficulty": "very_easy",
            "ingredients": base_recipe["ingredients"],
            "instructions": base_recipe["instructions"],
            "cultural_context": "Comfort food",
            "heritage_connection": base_recipe.get("notes", "Simple, familiar comfort food"),
            "nostalgic_description": base_recipe.get("notes", "Simple, familiar comfort food"),
            "source": "recipes_json_original_name",
            "youtube_url": "",
            "theme_connection": "Selected for Dancing theme"  # Add theme connection
        }
        
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": [recipe_element],
            "api_calls_made": 0,
            "original_name_kept": True
        }
    
    def _select_base_recipe(self, heritage: str, age: int) -> Dict[str, Any]:
        """Select culturally appropriate base recipe without API calls."""
        
        # Heritage-based preferences (for selection only, not naming)
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
            artist_name = first_artist["name"]
        else:
            title = f"{heritage} Traditional Music"
            description = f"Classic {heritage} music and songs"
            artist_name = "Classic Artist"
        
        fallback_element = {
            "content_type": "music_fallback",
            "title": title,
            "artist": artist_name,
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
                "cultural_context": f"Popular show from the era",
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
                "title": f"Classic Entertainment",
                "description": heritage_shows.get(heritage, "Classic television programming"),
                "cultural_context": f"Entertainment from the era",
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
            "title": f"Comfort Scents",
            "scents": scents[:3],  # Top 3 scents
            "description": f"Familiar scents from home",
            "cultural_context": f"Scents that evoke memories",
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
            "title": f"Comfort Textures",
            "textures": textures[:3],  # Top 3 textures
            "description": f"Familiar textures from home",
            "cultural_context": f"Textures that evoke memories",
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
            "simplified_approach": True,
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
                    "gustatory": self._format_base_recipe_simple(base_recipe, heritage),
                    "auditory": self._generate_music_fallback(heritage, None)
                },
                "sensory_summary": {
                    "total_senses_activated": 2,
                    "available_senses": ["gustatory", "auditory"],
                    "total_api_calls_made": 0,
                    "generation_success": True,
                    "rate_limiting_applied": True,
                    "simplified_approach": True
                },
                "generation_metadata": {
                    "heritage_used": heritage,
                    "status": "fallback_simplified_approach",
                    "generation_timestamp": datetime.now().isoformat()
                }
            }
        }