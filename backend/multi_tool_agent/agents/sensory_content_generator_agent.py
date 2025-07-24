"""
Agent 4: Sensory Content Generator - FIXED for Data Structure Issues
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

FIXED ISSUES:
- Handles list vs dictionary data structure correctly
- Properly processes Qloo response format
- Uses tv_shows instead of movies throughout
- Adds proper error handling for data access
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent:
    """
    Agent 4: Sensory Content Generator - FIXED for Data Structure Issues
    
    FIXES:
    - Properly handles dictionary vs list data structures
    - Uses tv_shows instead of movies 
    - Adds robust error handling for data access
    - Creates multi-sensory experiences with dementia-optimized recipes
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        logger.info("Sensory Content Generator initialized with FIXED data structure handling")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any], 
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive sensory content with FIXED data handling.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2  
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Dictionary containing multi-sensory content with optimized recipes
        """
        
        try:
            logger.info("🎵 Agent 4: Starting FIXED sensory content generation")
            
            # Extract key information safely
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            age = patient_profile.get("age", 75)
            birth_year = patient_profile.get("birth_year")
            if birth_year:
                age = 2024 - birth_year
            
            # FIXED: Safely extract Qloo recommendations
            qloo_recommendations = self._safely_extract_qloo_recommendations(qloo_intelligence)
            
            logger.info(f"Processing sensory content for {heritage} heritage, age {age}")
            logger.info(f"Available Qloo categories: {list(qloo_recommendations.keys())}")
            
            # Generate content for each sense
            sensory_content = {}
            
            # TASTE: Enhanced dementia-specific recipes
            sensory_content["taste"] = await self._generate_dementia_optimized_recipes(
                heritage, age, qloo_recommendations
            )
            
            # SOUND: Era-appropriate music
            sensory_content["sound"] = await self._generate_era_music_content(
                heritage, qloo_recommendations
            )
            
            # SIGHT: Visual content and photo opportunities  
            sensory_content["sight"] = await self._generate_visual_content(
                heritage, qloo_recommendations
            )
            
            # SMELL: Cultural scents and aromas
            sensory_content["smell"] = await self._generate_olfactory_content(heritage)
            
            # TOUCH: Tactile experiences
            sensory_content["touch"] = await self._generate_tactile_content(heritage)
            
            return {
                "sensory_content": {
                    "content_by_sense": sensory_content,
                    "sensory_summary": self._create_sensory_summary(sensory_content),
                    "generation_metadata": {
                        "heritage_used": heritage,
                        "age_optimized_for": age,
                        "dementia_care_focused": True,
                        "generation_timestamp": datetime.now().isoformat(),
                        "agent_version": "fixed_data_structures"
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    def _safely_extract_qloo_recommendations(self, qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        FIXED: Safely extract Qloo recommendations handling various data structures.
        
        Args:
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Dictionary with safely extracted recommendations
        """
        
        try:
            # Navigate to cultural_recommendations safely
            qloo_data = qloo_intelligence.get("qloo_intelligence", {})
            recommendations = qloo_data.get("cultural_recommendations", {})
            
            # Ensure we have a dictionary, not a list
            if not isinstance(recommendations, dict):
                logger.warning(f"Expected dict, got {type(recommendations)}. Using empty dict.")
                return {}
            
            # Validate each category
            safe_recommendations = {}
            expected_categories = ["tv_shows", "artists", "places"]
            
            for category in expected_categories:
                category_data = recommendations.get(category, {})
                
                # Ensure category_data is a dictionary
                if isinstance(category_data, dict):
                    safe_recommendations[category] = {
                        "available": category_data.get("available", False),
                        "entities": category_data.get("entities", []),
                        "entity_count": category_data.get("entity_count", 0)
                    }
                else:
                    logger.warning(f"Category {category} data is not a dict: {type(category_data)}")
                    safe_recommendations[category] = {
                        "available": False,
                        "entities": [],
                        "entity_count": 0
                    }
            
            logger.info(f"Safely extracted {len(safe_recommendations)} recommendation categories")
            return safe_recommendations
            
        except Exception as e:
            logger.error(f"Error safely extracting Qloo recommendations: {e}")
            return {
                "tv_shows": {"available": False, "entities": [], "entity_count": 0},
                "artists": {"available": False, "entities": [], "entity_count": 0},
                "places": {"available": False, "entities": [], "entity_count": 0}
            }
    
    async def _generate_dementia_optimized_recipes(self, 
                                                 heritage: str, 
                                                 age: int,
                                                 qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate FIXED dementia-optimized recipes with proper error handling.
        """
        
        try:
            logger.info(f"Generating dementia-optimized recipes for {heritage} heritage")
            
            # Use Qloo place recommendations for cultural cuisine inspiration
            places_data = qloo_recommendations.get("places", {})
            cultural_cuisines = []
            
            if places_data.get("available") and places_data.get("entities"):
                # Safely extract cuisine inspiration from places
                entities = places_data.get("entities", [])
                if isinstance(entities, list):
                    for entity in entities[:3]:  # Use first 3 places
                        if isinstance(entity, dict):
                            name = entity.get("name", "")
                            if name:
                                cultural_cuisines.append(name)
            
            # Generate cultural comfort food recipe
            recipe_elements = []
            
            # Create a simple, culturally-inspired comfort food recipe
            cultural_base = heritage.split("-")[0] if "-" in heritage else heritage
            
            recipe_elements.append({
                "content_type": "comfort_food_recipe",
                "name": f"Simple {cultural_base} Comfort Dish",
                "description": f"A very simple, comforting dish inspired by {heritage} traditions",
                "prep_time": "15 minutes",
                "difficulty": "very_easy",
                "ingredients": self._get_simple_ingredients(cultural_base),
                "instructions": self._get_simple_instructions(cultural_base),
                "dementia_friendly": True,
                "cultural_connection": f"Traditional comfort food from {heritage} heritage",
                "caregiver_notes": "Perfect for cooking together - simple steps, familiar flavors"
            })
            
            # Add a no-cook option
            recipe_elements.append({
                "content_type": "no_cook_comfort",
                "name": f"{cultural_base} Memory Plate",
                "description": f"Simple assembled foods that evoke {heritage} memories",
                "prep_time": "5 minutes",
                "difficulty": "no_cooking",
                "ingredients": self._get_no_cook_ingredients(cultural_base),
                "instructions": ["Arrange ingredients on a beautiful plate", "Share memories while enjoying together"],
                "dementia_friendly": True,
                "cultural_connection": f"Familiar flavors from {heritage} tradition"
            })
            
            return {
                "sense_type": "gustatory",
                "available": True,
                "elements": recipe_elements,
                "cultural_inspiration": cultural_cuisines,
                "dementia_optimized": True
            }
            
        except Exception as e:
            logger.error(f"Recipe generation failed: {e}")
            return self._create_fallback_recipe(heritage)
    
    def _get_simple_ingredients(self, cultural_base: str) -> List[str]:
        """Get simple ingredients based on cultural background."""
        
        ingredient_map = {
            "Italian": ["pasta", "olive oil", "garlic", "parmesan cheese", "butter"],
            "Irish": ["potatoes", "butter", "milk", "cheese", "herbs"],
            "Mexican": ["tortillas", "cheese", "beans", "tomatoes", "avocado"],
            "American": ["bread", "butter", "eggs", "cheese", "milk"],
            "German": ["potatoes", "butter", "cheese", "herbs", "cream"]
        }
        
        return ingredient_map.get(cultural_base, ingredient_map["American"])
    
    def _get_simple_instructions(self, cultural_base: str) -> List[str]:
        """Get very simple cooking instructions."""
        
        instruction_map = {
            "Italian": [
                "Boil pasta according to package directions",
                "Heat olive oil and garlic in pan",
                "Toss pasta with oil and cheese",
                "Serve warm with extra cheese"
            ],
            "Irish": [
                "Boil potatoes until tender",
                "Mash with butter and milk",
                "Add cheese and herbs",
                "Serve hot with butter on top"
            ],
            "Mexican": [
                "Warm tortillas in dry pan",
                "Heat beans in small pot",
                "Fill tortillas with beans and cheese",
                "Top with tomatoes and avocado"
            ],
            "American": [
                "Beat eggs in bowl",
                "Cook eggs in buttered pan",
                "Add cheese when almost done",
                "Serve on buttered toast"
            ]
        }
        
        return instruction_map.get(cultural_base, instruction_map["American"])
    
    def _get_no_cook_ingredients(self, cultural_base: str) -> List[str]:
        """Get no-cook ingredients for memory plates."""
        
        no_cook_map = {
            "Italian": ["fresh mozzarella", "tomatoes", "basil", "crackers", "olives"],
            "Irish": ["aged cheese", "crackers", "butter", "jam", "tea"],
            "Mexican": ["cheese", "crackers", "salsa", "avocado", "tortilla chips"],
            "American": ["cheese", "crackers", "grapes", "nuts", "apple slices"]
        }
        
        return no_cook_map.get(cultural_base, no_cook_map["American"])
    
    async def _generate_era_music_content(self, 
                                         heritage: str,
                                         qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate era-appropriate music content using YouTube API."""
        
        try:
            logger.info(f"Generating era music content for {heritage}")
            
            # Extract music inspiration from Qloo artists
            artists_data = qloo_recommendations.get("artists", {})
            search_terms = [f"{heritage} traditional music", "nostalgic music", "classic songs"]
            
            if artists_data.get("available") and artists_data.get("entities"):
                entities = artists_data.get("entities", [])
                if isinstance(entities, list):
                    for entity in entities[:2]:  # Use first 2 artists
                        if isinstance(entity, dict):
                            name = entity.get("name", "")
                            if name:
                                search_terms.append(name)
            
            # Try to get music from YouTube
            music_results = []
            if self.youtube_tool:
                for term in search_terms[:3]:  # Limit API calls
                    try:
                        results = await self.youtube_tool.search_music(term, max_results=2)
                        if results and isinstance(results, list):
                            for result in results:
                                if isinstance(result, dict):
                                    music_results.append({
                                        "title": result.get("title", "Unknown Song"),
                                        "description": result.get("description", "")[:100],
                                        "video_id": result.get("video_id", ""),
                                        "source": "youtube",
                                        "cultural_relevance": "high",
                                        "search_term": term
                                    })
                        break  # Stop after first successful search
                    except Exception as e:
                        logger.warning(f"YouTube search failed for {term}: {e}")
                        continue
            
            if music_results:
                return {
                    "sense_type": "auditory",
                    "available": True,
                    "elements": music_results,
                    "heritage_focused": True
                }
            else:
                # Fallback to simple music suggestion
                return {
                    "sense_type": "auditory",
                    "available": True,
                    "elements": [{
                        "title": f"{heritage} Traditional Music",
                        "description": f"Play gentle traditional {heritage} music",
                        "source": "fallback_suggestion",
                        "cultural_relevance": "high",
                        "implementation": "Use any available music source"
                    }],
                    "fallback_used": True
                }
                
        except Exception as e:
            logger.error(f"Music content generation failed: {e}")
            return {
                "sense_type": "auditory",
                "available": False,
                "fallback_used": True,
                "error": str(e)
            }
    
    async def _generate_visual_content(self, 
                                     heritage: str,
                                     qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content and photo opportunities."""
        
        try:
            # FIXED: Use TV show recommendations instead of movies
            tv_shows_data = qloo_recommendations.get("tv_shows", {})
            
            visual_elements = []
            
            if tv_shows_data.get("available") and tv_shows_data.get("entities"):
                # Convert TV show recommendations to visual content
                entities = tv_shows_data.get("entities", [])
                if isinstance(entities, list):
                    for show in entities[:3]:
                        if isinstance(show, dict):
                            show_name = show.get("name", "Classic Show")
                            properties = show.get("properties", {})
                            description = properties.get("description", "") if isinstance(properties, dict) else ""
                            
                            visual_elements.append({
                                "content_type": "tv_show_visual",
                                "name": show_name,
                                "description": description[:100] + "..." if len(description) > 100 else description,
                                "viewing_guidance": f"Classic {heritage} television for gentle viewing",
                                "cultural_connection": f"From the era of great {heritage} television"
                            })
            
            # Add photo opportunities
            visual_elements.append({
                "content_type": "photo_opportunity",
                "name": f"{heritage} Heritage Photos",
                "description": f"Look through family photos or {heritage} cultural images",
                "activity": "Photo viewing and memory sharing",
                "engagement_tips": [
                    "Ask about people in the photos",
                    "Let them lead the conversation",
                    "Focus on positive memories"
                ]
            })
            
            return {
                "sense_type": "visual",
                "available": True if visual_elements else False,
                "elements": visual_elements,
                "tv_show_focused": True  # FIXED: TV show focused
            }
            
        except Exception as e:
            logger.error(f"Visual content generation failed: {e}")
            return {
                "sense_type": "visual",
                "available": False,
                "fallback_used": True,
                "error": str(e)
            }
    
    async def _generate_olfactory_content(self, heritage: str) -> Dict[str, Any]:
        """Generate cultural scent experiences."""
        
        heritage_scents = {
            "Italian-American": ["basil", "garlic", "olive oil", "fresh bread"],
            "Irish-American": ["fresh herbs", "baking bread", "tea", "wool"],
            "Mexican-American": ["cinnamon", "vanilla", "fresh tortillas", "lime"],
            "German-American": ["baking bread", "apple", "pine", "herbs"],
            "American": ["vanilla", "apple pie", "fresh bread", "coffee"]
        }
        
        scents = heritage_scents.get(heritage, heritage_scents["American"])
        
        scent_elements = []
        for scent in scents[:3]:
            scent_elements.append({
                "content_type": "cultural_scent",
                "name": f"{scent.title()} Aroma",
                "description": f"Experience the comforting scent of {scent}",
                "implementation": f"Use {scent} essential oil or actual {scent} if available",
                "safety_note": "Ensure no allergies before using",
                "cultural_connection": f"Traditional {heritage} scent memory"
            })
        
        return {
            "sense_type": "olfactory",
            "available": True,
            "elements": scent_elements
        }
    
    async def _generate_tactile_content(self, heritage: str) -> Dict[str, Any]:
        """Generate tactile experiences."""
        
        tactile_elements = [
            {
                "content_type": "texture_exploration",
                "name": "Soft Fabric Touch",
                "description": "Feel different textures of comfortable fabrics",
                "materials": ["soft blanket", "smooth silk", "textured wool"],
                "guidance": "Let them explore textures at their own pace",
                "benefits": "Calming and grounding sensory experience"
            },
            {
                "content_type": "cultural_touch",
                "name": f"{heritage} Craft Materials",
                "description": f"Touch materials associated with {heritage} crafts",
                "materials": ["smooth wood", "soft yarn", "natural fibers"],
                "cultural_connection": f"Materials from {heritage} traditional crafts"
            }
        ]
        
        return {
            "sense_type": "tactile",
            "available": True,
            "elements": tactile_elements
        }
    
    def _create_sensory_summary(self, sensory_content: Dict[str, Any]) -> Dict[str, Any]:
        """Create summary of generated sensory content."""
        
        available_senses = sum(1 for content in sensory_content.values() 
                             if isinstance(content, dict) and content.get("available"))
        total_elements = sum(len(content.get("elements", [])) 
                           for content in sensory_content.values() 
                           if isinstance(content, dict))
        
        return {
            "total_senses_activated": available_senses,
            "total_elements_generated": total_elements,
            "dementia_optimized": True,
            "generation_success": available_senses > 0,
            "primary_focus": "taste (recipes)" if sensory_content.get("taste", {}).get("available") else "multi_sensory"
        }
    
    def _create_fallback_recipe(self, heritage: str) -> Dict[str, Any]:
        """Create a simple fallback recipe."""
        
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": [{
                "content_type": "simple_comfort_food",
                "name": f"Simple {heritage} Comfort Food",
                "description": "A very easy, comforting dish",
                "prep_time": "10 minutes",
                "difficulty": "very_easy",
                "ingredients": ["simple ingredients", "comfort food basics"],
                "instructions": ["Very simple steps", "Easy to follow"],
                "dementia_friendly": True,
                "fallback_used": True
            }],
            "fallback_used": True
        }
    
    def _create_fallback_sensory_content(self, 
                                       consolidated_info: Dict[str, Any],
                                       cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails."""
        
        heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
        
        return {
            "sensory_content": {
                "content_by_sense": {
                    "taste": self._create_fallback_recipe(heritage),
                    "sound": {"sense_type": "auditory", "available": False, "fallback_used": True},
                    "sight": {"sense_type": "visual", "available": False, "fallback_used": True},
                    "smell": {"sense_type": "olfactory", "available": False, "fallback_used": True},
                    "touch": {"sense_type": "tactile", "available": False, "fallback_used": True}
                },
                "sensory_summary": {
                    "total_senses_activated": 1,
                    "generation_success": True,
                    "fallback_mode": True,
                    "dementia_optimized": True
                },
                "generation_metadata": {
                    "fallback_used": True,
                    "agent_version": "fallback_fixed_structures"
                }
            }
        }

# Test function
async def test_fixed_sensory_content_generator():
    """Test the FIXED Sensory Content Generator Agent."""
    
    # Mock tools for testing
    class MockYouTubeTool:
        async def search_music(self, query, max_results=5):
            return [{"title": f"Test Song for {query}", "video_id": "test123", "description": "Test description"}]
    
    class MockGeminiTool:
        async def generate_recipe(self, prompt):
            return {"recipe": "Test recipe content"}
    
    # Test data with proper structure
    agent = SensoryContentGeneratorAgent(MockGeminiTool(), MockYouTubeTool())
    
    test_consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "age": 79
        }
    }
    
    test_cultural_profile = {
        "era_context": {"formative_decades": [1950, 1960, 1970]}
    }
    
    test_qloo_intelligence = {
        "qloo_intelligence": {
            "cultural_recommendations": {
                "tv_shows": {
                    "available": True,
                    "entities": [{"name": "Classic Family Show", "properties": {"description": "A wholesome family show"}}],
                    "entity_count": 1
                },
                "artists": {
                    "available": True,
                    "entities": [{"name": "Frank Sinatra"}],
                    "entity_count": 1
                },
                "places": {
                    "available": True,
                    "entities": [{"name": "Italian Restaurant"}],
                    "entity_count": 1
                }
            }
        }
    }
    
    # Run test
    result = await agent.run(test_consolidated_info, test_cultural_profile, test_qloo_intelligence)
    
    sensory = result.get("sensory_content", {})
    print("FIXED Sensory Content Generator Test Results:")
    print(f"Senses activated: {sensory.get('sensory_summary', {}).get('total_senses_activated')}")
    print(f"Taste available: {sensory.get('content_by_sense', {}).get('taste', {}).get('available')}")
    print(f"TV show focused: {sensory.get('content_by_sense', {}).get('sight', {}).get('tv_show_focused')}")
    print(f"Agent version: {sensory.get('generation_metadata', {}).get('agent_version')}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_fixed_sensory_content_generator())