"""
Enhanced Sensory Content Generator Agent with Dementia-Specific Recipe Generation
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

Agent 4: Generates very simple, complete recipes optimized for dementia care
along with other sensory content (music, visual, tactile, olfactory).
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent:
    """
    Agent 4: Sensory Content Generator with Dementia-Optimized Recipes
    
    Creates multi-sensory experiences with special focus on very simple,
    complete recipes designed specifically for dementia care scenarios.
    """
    
    def __init__(self, gemini_tool, youtube_tool):
        self.gemini_tool = gemini_tool
        self.youtube_tool = youtube_tool
        logger.info("Sensory Content Generator initialized with dementia-optimized recipe generation")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any], 
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive sensory content with dementia-specific recipes.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2  
            qloo_intelligence: Output from Agent 3
            
        Returns:
            Dictionary containing multi-sensory content with optimized recipes
        """
        
        try:
            logger.info("🎵 Agent 4: Starting sensory content generation")
            
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
                        "agent_version": "dementia_optimized"
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 4 failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    async def _generate_dementia_optimized_recipes(self, 
                                                 heritage: str, 
                                                 age: int,
                                                 qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate VERY SIMPLE, COMPLETE recipes with better error handling.
        """
        
        try:
            # Create enhanced dementia-specific prompt
            prompt = self._create_dementia_recipe_prompt(heritage, age, qloo_recommendations)
            
            logger.info(f"Generating dementia-optimized recipe: {heritage} heritage for age {age}")
            
            # Call Gemini with enhanced prompt
            recipe_result = await self.gemini_tool.generate_recipe(prompt)
            
            # Better handling of Gemini response
            if recipe_result and isinstance(recipe_result, dict) and recipe_result.get("name"):
                # Successfully generated dementia-optimized recipe
                recipe_elements = [{
                    "content_type": "dementia_optimized_recipe",
                    "name": recipe_result.get("name", f"Simple {heritage} Comfort Recipe"),
                    "description": recipe_result.get("description", "A very simple, comforting recipe"),
                    "total_time": recipe_result.get("total_time", "25 minutes including breaks"),
                    "difficulty": "very_easy",
                    "ingredients": recipe_result.get("ingredients", []),
                    "instructions": recipe_result.get("instructions", []),
                    "caregiver_notes": recipe_result.get("caregiver_notes", []),
                    "sensory_engagement": recipe_result.get("sensory_engagement", []),
                    "success_indicators": recipe_result.get("success_indicators", []),
                    "cultural_context": recipe_result.get("cultural_context", f"Traditional {heritage} comfort food"),
                    "dementia_optimized": True,
                    "source": "gemini_dementia_focused"
                }]
                
                return {
                    "sense_type": "gustatory", 
                    "available": True,
                    "elements": recipe_elements,
                    "dementia_optimized": True,
                    "implementation_notes": [
                        "Recipe designed for cognitive support",
                        "Every step includes visual/sensory cues", 
                        "Built-in rest breaks and safety considerations",
                        "Success indicators help build confidence"
                    ]
                }
            else:
                logger.warning("Gemini recipe result was empty or invalid format")
        
        except Exception as e:
            logger.error(f"Dementia recipe generation failed: {e}")
        
        # Fallback to very simple recipe structure
        logger.info("Using fallback dementia recipe")
        return self._create_fallback_dementia_recipe(heritage)
    
    def _create_dementia_recipe_prompt(self, 
                                     heritage: str, 
                                     age: int,
                                     qloo_recommendations: Dict[str, Any]) -> str:
        """
        Create DEMENTIA-SPECIFIC recipe prompt using places as recipe inspiration.
        Places are used as memory anchors and cooking style inspiration, not destinations.
        """
        
        # Extract recipe inspiration from places (not destination suggestions)
        places_data = qloo_recommendations.get("places", {})
        recipe_inspiration = ""
        cooking_style_notes = ""
        
        if places_data.get("available") and places_data.get("entities"):
            # Use first place as recipe inspiration
            place_entity = places_data["entities"][0]
            
            # Check if this is a memory anchor (from our enhanced system)
            if place_entity.get("memory_anchor_name"):
                place_inspiration = place_entity.get("memory_anchor_name")
                recipe_style = place_entity.get("recipe_inspiration", {})
                cooking_style_notes = f"\nCooking Style: {recipe_style.get('cuisine_style', 'traditional family-style')}"
                recipe_inspiration = f" inspired by the cooking style of {place_inspiration}"
            else:
                # Fallback for regular place entities
                place_name = place_entity.get("name", "")
                if place_name:
                    recipe_inspiration = f" inspired by the style of cooking at places like {place_name}"
                    cooking_style_notes = f"\nCooking Style: Traditional family restaurant style"
        
        prompt = f"""Create a VERY SIMPLE recipe for dementia care for a {age}-year-old person with {heritage} cultural heritage{recipe_inspiration}.

CRITICAL REQUIREMENTS FOR DEMENTIA CARE:
- Maximum 5 ingredients (familiar items only - no exotic ingredients)
- Maximum 8 steps total  
- Each step takes 2-5 minutes maximum
- NO sharp knives, NO stovetop (oven/microwave/cold prep only)
- Every measurement EXACT (no "pinch", "dash", or "to taste")
- Every step has WHAT TO LOOK FOR (visual/smell/sound cues)
- Include REST BREAKS between steps
- Every ingredient includes WHERE TO FIND IT in kitchen
- Safety considerations for each step
- Success indicators so they know it's working{cooking_style_notes}

RECIPE INSPIRATION CONTEXT:
- Focus on comfort food that would remind them of family restaurants from their youth
- Use simple, traditional preparation methods that were common in the 1950s-1970s
- Emphasize familiar flavors and textures from their cultural background
- Create a sense of nostalgia and positive food memories

RESPONSE FORMAT (JSON):
{{
    "name": "Simple {heritage} [dish name]",
    "description": "One sentence about comfort, familiarity, and memory connection",
    "total_time": "Maximum 25 minutes including rest breaks",
    "difficulty": "very_easy",
    "ingredients": [
        {{
            "item": "exact ingredient name",
            "amount": "precise measurement (1 cup, 2 tablespoons)",
            "location": "where to find it (pantry, refrigerator)",
            "safety_note": "any handling considerations"
        }}
    ],
    "instructions": [
        {{
            "step": 1,
            "instruction": "One simple action only - be very specific",
            "time": "exact time (2 minutes, 5 minutes)",
            "what_to_look_for": "visual, smell, or sound cue",
            "safety_note": "any safety consideration for this step",
            "rest_break": "if needed after this step (true/false)"
        }}
    ],
    "caregiver_notes": [
        "How to help if they get confused or frustrated",
        "What to do if they want to stop midway",
        "How to adapt if motor skills are limited",
        "Signs that they're enjoying the process"
    ],
    "sensory_engagement": [
        "Specific smells to notice and enjoy together",
        "Textures to feel and describe together", 
        "Sounds to listen for (sizzling, bubbling)",
        "Colors and visual changes to watch for"
    ],
    "success_indicators": [
        "How to know each step is working correctly",
        "What good results look like at each stage",
        "Positive signs that the person is engaged"
    ],
    "cultural_context": "Why this recipe connects to {heritage} heritage and family restaurant memories",
    "memory_connection_potential": "How this might trigger positive food memories from family dining experiences",
    "recipe_inspiration_source": "Inspired by traditional family restaurant cooking{recipe_inspiration}"
}}

EXAMPLE INSTRUCTION STYLE:
"Put 1 cup flour in the large blue mixing bowl. Time: 2 minutes. What to look for: Flour should be level in the measuring cup and create a small mound in the bowl. Safety note: Keep flour container away from counter edge to prevent spills. Rest break: Not needed."

Focus on:
- Extreme simplicity and clarity
- Building confidence through small successes  
- Sensory engagement at every step
- Cultural comfort and familiarity from family restaurant memories
- Safety as the top priority
- Caregiver support and guidance"""
        
        return prompt
    
    def _create_fallback_dementia_recipe(self, heritage: str) -> Dict[str, Any]:
        """Create simple fallback recipe when Gemini fails."""
        
        simple_recipe = {
            "content_type": "dementia_optimized_recipe",
            "name": f"Simple {heritage} Comfort Bread",
            "description": f"A very simple, no-bake comfort food from {heritage} tradition",
            "total_time": "15 minutes with rest breaks",
            "difficulty": "very_easy",
            "ingredients": [
                {
                    "item": "Soft bread slices",
                    "amount": "4 slices",
                    "location": "bread drawer or counter",
                    "safety_note": "Use pre-sliced bread only"
                },
                {
                    "item": "Butter",
                    "amount": "2 tablespoons", 
                    "location": "refrigerator door",
                    "safety_note": "Let soften for 5 minutes before using"
                }
            ],
            "instructions": [
                {
                    "step": 1,
                    "instruction": "Place 4 bread slices on clean plate",
                    "time": "1 minute",
                    "what_to_look_for": "Bread lies flat on plate",
                    "safety_note": "Use clean hands only",
                    "rest_break": False
                },
                {
                    "step": 2,
                    "instruction": "Spread soft butter on each slice with spoon",
                    "time": "3 minutes", 
                    "what_to_look_for": "Butter spreads easily and evenly",
                    "safety_note": "Use spoon, not knife",
                    "rest_break": True
                }
            ],
            "caregiver_notes": [
                "This is about the process, not perfection",
                "If they get tired, it's okay to help finish",
                "Focus on the butter smell and soft textures"
            ],
            "sensory_engagement": [
                "Smell the fresh bread and creamy butter",
                "Feel the soft bread texture",
                "Listen for spreading sounds"
            ],
            "success_indicators": [
                "Butter spreads without tearing bread",
                "Person seems engaged with the process",
                "Pleasant bread and butter aroma"
            ],
            "cultural_context": f"Simple bread preparation from {heritage} tradition",
            "dementia_optimized": True,
            "source": "fallback_dementia_focused"
        }
        
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": [simple_recipe],
            "dementia_optimized": True,
            "fallback_used": True
        }
    
    async def _generate_era_music_content(self, 
                                        heritage: str,
                                        qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate era-appropriate music content with proper error handling."""
        
        try:
            # Check for Qloo artist recommendations
            artists_data = qloo_recommendations.get("artists", {})
            
            if artists_data.get("available") and artists_data.get("entities"):
                # Use Qloo artist recommendations
                artist_entities = artists_data["entities"]
                if len(artist_entities) > 3:
                    artist_entities = artist_entities[:3]  # Top 3 artists
                
                music_elements = []
                for artist in artist_entities:
                    artist_name = artist.get("name", "Unknown Artist")
                    
                    # Search YouTube for this specific artist
                    try:
                        youtube_results = await self.youtube_tool.search_music(
                            f"{artist_name} classic songs"
                        )
                        
                        # Safely handle YouTube results
                        if youtube_results and isinstance(youtube_results, list):
                            # Take first 2 songs per artist, safely
                            for result in youtube_results[:2]:
                                if isinstance(result, dict):
                                    music_elements.append(result)
                    
                    except Exception as e:
                        logger.warning(f"YouTube search failed for {artist_name}: {e}")
                
                if music_elements:
                    return {
                        "sense_type": "auditory",
                        "available": True, 
                        "elements": music_elements,
                        "qloo_enhanced": True,
                        "era_appropriate": True
                    }
            
            # Fallback to heritage-based music search
            heritage_music_query = f"{heritage} traditional music classics"
            youtube_results = await self.youtube_tool.search_music(heritage_music_query)
            
            # Safely handle fallback results
            if youtube_results and isinstance(youtube_results, list):
                safe_results = []
                for result in youtube_results[:5]:  # Limit to 5
                    if isinstance(result, dict):
                        safe_results.append(result)
                
                if safe_results:
                    return {
                        "sense_type": "auditory",
                        "available": True,
                        "elements": safe_results,
                        "heritage_focused": True
                    }
        
        except Exception as e:
            logger.error(f"Music content generation failed: {e}")
        
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
    
    async def _generate_visual_content(self, 
                                     heritage: str,
                                     qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content and photo opportunities."""
        
        # Use Qloo movie recommendations if available
        movies_data = qloo_recommendations.get("tv_shows", {})
        
        visual_elements = []
        
        if movies_data.get("available") and movies_data.get("entities"):
            # Convert movie recommendations to visual content
            for movie in movies_data["entities"][:3]:
                movie_name = movie.get("name", "Classic Film")
                description = movie.get("properties", {}).get("description", "")
                image_url = movie.get("properties", {}).get("image", {}).get("url", "")
                
                visual_elements.append({
                    "content_type": "movie_visual",
                    "name": movie_name,
                    "description": description[:100] + "..." if len(description) > 100 else description,
                    "image_url": image_url,
                    "viewing_guidance": f"Classic {heritage} film for gentle viewing",
                    "cultural_connection": f"From the era of great {heritage} cinema"
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
            "elements": visual_elements
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
        
        available_senses = sum(1 for content in sensory_content.values() if content.get("available"))
        total_elements = sum(len(content.get("elements", [])) for content in sensory_content.values())
        
        return {
            "total_senses_activated": available_senses,
            "total_elements_generated": total_elements,
            "dementia_optimized": True,
            "generation_success": available_senses > 0,
            "primary_focus": "taste (recipes)" if sensory_content.get("taste", {}).get("available") else "multi_sensory"
        }
    
    def _create_fallback_sensory_content(self, 
                                       consolidated_info: Dict[str, Any],
                                       cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback sensory content when generation fails."""
        
        heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
        
        return {
            "sensory_content": {
                "content_by_sense": {
                    "taste": self._create_fallback_dementia_recipe(heritage),
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
                    "agent_version": "fallback_dementia_focused"
                }
            }
        }

# Test function
async def test_enhanced_recipe_generation():
    """Test the enhanced dementia-optimized recipe generation."""
    
    import os
    from backend.multi_tool_agent.tools.gemini_tools import GeminiRecipeGenerator
    from backend.multi_tool_agent.tools.youtube_tools import YouTubeMusicSearch
    
    # Setup tools
    gemini_key = os.getenv("GEMINI_API_KEY")
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    
    if not all([gemini_key, youtube_key]):
        print("❌ Missing API keys")
        return
    
    gemini_tool = GeminiRecipeGenerator(gemini_key)
    youtube_tool = YouTubeMusicSearch(youtube_key)
    agent = SensoryContentGeneratorAgent(gemini_tool, youtube_tool)
    
    # Test data for Maria (age 79, Italian-American)
    consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "age": 79,
            "additional_context": "Loves cooking and music"
        }
    }
    
    cultural_profile = {
        "era_context": {
            "formative_decades": [1950, 1960, 1970]
        }
    }
    
    qloo_intelligence = {
        "cultural_recommendations": {
            "places": {
                "available": True,
                "entities": [{"name": "Italian Family Restaurant", "type": "urn:entity:place"}]
            }
        }
    }
    
    # Run the agent
    print("Testing enhanced dementia-optimized recipe generation...")
    result = await agent.run(consolidated_info, cultural_profile, qloo_intelligence)
    
    # Display results
    sensory_content = result.get("sensory_content", {})
    taste_content = sensory_content.get("content_by_sense", {}).get("taste", {})
    
    if taste_content.get("available"):
        recipe = taste_content.get("elements", [{}])[0]
        print(f"\nGenerated Recipe:")
        print(f"Name: {recipe.get('name')}")
        print(f"Description: {recipe.get('description')}")
        print(f"Total time: {recipe.get('total_time')}")
        print(f"Dementia optimized: {recipe.get('dementia_optimized')}")
        print(f"Ingredients: {len(recipe.get('ingredients', []))}")
        print(f"Instructions: {len(recipe.get('instructions', []))}")
        
        # Show first instruction as example
        if recipe.get('instructions'):
            first_step = recipe['instructions'][0]
            print(f"\nExample instruction:")
            print(f"Step {first_step.get('step')}: {first_step.get('instruction')}")
            print(f"Time: {first_step.get('time')}")
            print(f"Look for: {first_step.get('what_to_look_for')}")
            print(f"Safety: {first_step.get('safety_note')}")
    else:
        print("❌ Recipe generation failed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_enhanced_recipe_generation())