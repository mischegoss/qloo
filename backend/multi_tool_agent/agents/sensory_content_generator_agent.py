"""
Agent 4: Sensory Content Generator - FIXED VERSION  
File: backend/multi_tool_agent/agents/sensory_content_generator_agent.py

Fixed Gemini response parsing and simplified content generation.
Uses cultural heritage directly in prompts and processes simple Qloo results.
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class SensoryContentGeneratorAgent(Agent):
    """
    Agent 4: Sensory Content Generator - FIXED
    
    FIXES:
    - Fixed Gemini response parsing (JSON extraction)
    - Use cultural heritage directly in prompts
    - Simplified content generation 
    - Process simple Qloo results from Agent 3
    - Better error handling and fallback content
    """
    
    def __init__(self, youtube_tool, gemini_tool):
        super().__init__(
            name="sensory_content_generator_fixed",
            description="Creates practical multi-sensory experiences with fixed Gemini parsing"
        )
        self._youtube_tool = youtube_tool
        self._gemini_tool = gemini_tool
        logger.info("Sensory Content Generator initialized with Gemini fixes")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any],
                  qloo_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Generate connected sensory content with fixed processing."""
        
        try:
            logger.info("Starting sensory content generation with fixed approach")
            
            # Extract basic context
            request_context = consolidated_info.get("request_context", {})
            patient_profile = consolidated_info.get("patient_profile", {})
            
            # Extract cultural information
            heritage = patient_profile.get("cultural_heritage", "American")
            age = patient_profile.get("age", 75)
            preferences = patient_profile.get("preferences", [])
            
            # Extract Qloo recommendations
            qloo_recommendations = qloo_intelligence.get("cultural_recommendations", {})
            
            logger.info(f"Generating content for {heritage} heritage, age {age}")
            
            # Generate content for each sense
            sensory_content = {
                "auditory": await self._generate_auditory_content_fixed(heritage, preferences, qloo_recommendations),
                "gustatory": await self._generate_gustatory_content_fixed(heritage, age, qloo_recommendations),
                "olfactory": await self._generate_olfactory_content_fixed(heritage),
                "visual": await self._generate_visual_content_fixed(heritage, qloo_recommendations),
                "tactile": await self._generate_tactile_content_fixed(heritage, age)
            }
            
            # Create sensory summary
            sensory_summary = self._create_sensory_summary(sensory_content)
            
            # Build final response
            response = {
                "sensory_content": {
                    "content_by_sense": sensory_content,
                    "sensory_summary": sensory_summary,
                    "cultural_context": {
                        "heritage_used": heritage,
                        "age_considered": age,
                        "preferences_integrated": preferences
                    },
                    "generation_metadata": {
                        "qloo_integration": qloo_intelligence.get("success", False),
                        "content_generation_timestamp": datetime.now().isoformat(),
                        "agent_version": "fixed_gemini_parsing"
                    }
                }
            }
            
            logger.info("Sensory content generation completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"❌ Sensory content generation failed: {e}")
            return self._create_fallback_sensory_content(consolidated_info, cultural_profile)
    
    async def _generate_auditory_content_fixed(self, 
                                             heritage: str, 
                                             preferences: List[str],
                                             qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate auditory content with fixed YouTube integration."""
        
        try:
            # Use Qloo artist recommendations if available
            artists_data = qloo_recommendations.get("artists", {})
            if artists_data.get("available") and artists_data.get("entities"):
                # Use first Qloo artist recommendation
                artist_entity = artists_data["entities"][0]
                search_query = artist_entity.get("name", "classical music")
                search_context = f"Qloo recommended: {search_query}"
            else:
                # Fallback to heritage-based search
                if "music" in preferences:
                    search_query = f"{heritage} traditional music"
                else:
                    search_query = f"{heritage} classical music peaceful"
                search_context = f"Heritage-based search: {search_query}"
            
            logger.info(f"Searching YouTube: {search_query}")
            
            # Search YouTube
            youtube_results = await self._youtube_tool.search_music(
                query=search_query,
                max_results=3
            )
            
            if youtube_results.get("success") and youtube_results.get("results"):
                music_items = []
                for item in youtube_results["results"][:3]:
                    music_items.append({
                        "title": item.get("title", "Unknown Title"),
                        "youtube_url": f"https://www.youtube.com/watch?v={item.get('video_id')}",
                        "channel": item.get("channel_title", "Unknown Channel"),
                        "description": item.get("description", "")[:100],
                        "cultural_relevance": "high",
                        "source": "youtube_search"
                    })
                
                return {
                    "sense_type": "auditory",
                    "available": True,
                    "elements": music_items,
                    "search_context": search_context,
                    "implementation_notes": [
                        "Play at comfortable volume",
                        "Consider time of day preferences",
                        "Watch for positive/negative reactions"
                    ]
                }
        
        except Exception as e:
            logger.error(f"Auditory content generation failed: {e}")
        
        # Fallback auditory content
        return self._create_fallback_auditory_content(heritage)
    
    async def _generate_gustatory_content_fixed(self, 
                                              heritage: str, 
                                              age: int,
                                              qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate gustatory content with fixed Gemini integration."""
        
        try:
            # Create enhanced Gemini prompt
            prompt = self._create_recipe_prompt(heritage, age, qloo_recommendations)
            
            logger.info(f"Generating recipe with Gemini: {heritage} heritage for age {age}")
            
            # Call Gemini with improved prompt
            recipe_result = await self._gemini_tool.generate_recipe(prompt)
            
            if recipe_result:
                # Successfully parsed recipe
                recipe_elements = [{
                    "content_type": "recipe",
                    "name": recipe_result.get("name", f"{heritage} Comfort Recipe"),
                    "description": recipe_result.get("description", "A comforting traditional recipe"),
                    "prep_time": recipe_result.get("prep_time", "30 minutes"),
                    "difficulty": recipe_result.get("difficulty", "easy"),
                    "ingredients": recipe_result.get("ingredients", []),
                    "instructions": recipe_result.get("instructions", []),
                    "cultural_context": recipe_result.get("cultural_context", f"Traditional {heritage} cooking"),
                    "caregiver_notes": recipe_result.get("caregiver_customization_notes", []),
                    "source": "gemini_generated"
                }]
                
                return {
                    "sense_type": "gustatory", 
                    "available": True,
                    "elements": recipe_elements,
                    "gemini_success": True,
                    "implementation_notes": [
                        "Adapt complexity based on cooking abilities",
                        "Consider dietary restrictions",
                        "Focus on familiar flavors"
                    ]
                }
        
        except Exception as e:
            logger.error(f"Gustatory content generation failed: {e}")
        
        # Fallback gustatory content
        return self._create_fallback_gustatory_content(heritage)
    
    def _create_recipe_prompt(self, 
                            heritage: str, 
                            age: int,
                            qloo_recommendations: Dict[str, Any]) -> str:
        """Create enhanced recipe prompt for Gemini."""
        
        # Check for Qloo place recommendations
        places_data = qloo_recommendations.get("places", {})
        cuisine_context = ""
        
        if places_data.get("available") and places_data.get("entities"):
            first_place = places_data["entities"][0]
            place_name = first_place.get("name", "")
            if place_name:
                cuisine_context = f" inspired by places like {place_name}"
        
        prompt = f"""Create a simple, comforting recipe suitable for a {age}-year-old person with {heritage} cultural heritage{cuisine_context}.

Requirements:
- Simple preparation (30 minutes or less)
- Familiar, comforting flavors
- Easy to follow instructions
- Ingredients commonly available
- Adaptable for different dietary needs
- Focus on taste and aroma that evoke positive memories

Please provide the response as a JSON object with this exact structure:
{{
    "name": "Recipe name",
    "description": "Brief description emphasizing comfort and cultural connection",
    "prep_time": "Preparation time",
    "cook_time": "Cooking time",
    "total_time": "Total time",
    "servings": "Number of servings",
    "difficulty": "easy",
    "ingredients": [
        {{"item": "ingredient name", "amount": "quantity", "notes": "optional notes"}}
    ],
    "instructions": [
        {{"step": 1, "instruction": "Clear step description", "time": "time if needed"}}
    ],
    "caregiver_customization_notes": [
        "How to simplify if needed",
        "Dietary substitution options"
    ],
    "cultural_context": "Why this recipe connects to {heritage} heritage",
    "memory_connection_potential": "How this might evoke positive memories"
}}"""
        
        return prompt
    
    async def _generate_olfactory_content_fixed(self, heritage: str) -> Dict[str, Any]:
        """Generate simple olfactory content."""
        
        # Heritage-based scent suggestions
        heritage_scents = {
            "Italian-American": ["basil", "oregano", "fresh bread", "lemon"],
            "Irish-American": ["lavender", "fresh grass", "baking bread", "vanilla"],
            "Mexican-American": ["cinnamon", "vanilla", "lime", "fresh herbs"],
            "American": ["vanilla", "cinnamon", "fresh flowers", "baking bread"]
        }
        
        base_heritage = heritage.split("-")[0] if "-" in heritage else heritage
        scents = heritage_scents.get(heritage, heritage_scents.get(base_heritage, heritage_scents["American"]))
        
        scent_elements = []
        for scent in scents[:3]:
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
    
    async def _generate_visual_content_fixed(self, heritage: str, qloo_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual content using Qloo movie recommendations."""
        
        visual_elements = []
        
        # Use Qloo movie recommendations if available
        movies_data = qloo_recommendations.get("movies", {})
        if movies_data.get("available") and movies_data.get("entities"):
            for movie in movies_data["entities"][:2]:
                visual_elements.append({
                    "content_type": "movie",
                    "title": movie.get("name", "Unknown Movie"),
                    "description": movie.get("properties", {}).get("description", "A culturally relevant film"),
                    "cultural_relevance": "high",
                    "source": "qloo_recommendation",
                    "viewing_notes": ["Watch together", "Pause for discussion", "Choose comfortable time"]
                })
        
        # Add heritage-based photo suggestions
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
            "available": True,
            "elements": visual_elements,
            "implementation_notes": [
                "Use good lighting",
                "Ensure comfortable viewing angle", 
                "Consider visual clarity needs"
            ]
        }
    
    async def _generate_tactile_content_fixed(self, heritage: str, age: int) -> Dict[str, Any]:
        """Generate simple tactile content."""
        
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
        
        total_elements = 0
        available_senses = []
        
        for sense, content in sensory_content.items():
            if content.get("available"):
                available_senses.append(sense)
                total_elements += len(content.get("elements", []))
        
        return {
            "total_senses_activated": len(available_senses),
            "available_senses": available_senses,
            "total_content_elements": total_elements,
            "cross_sensory_potential": len(available_senses) >= 3,
            "generation_success": len(available_senses) > 0
        }
    
    def _create_fallback_auditory_content(self, heritage: str) -> Dict[str, Any]:
        """Create fallback auditory content when YouTube fails."""
        
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
    
    def _create_fallback_gustatory_content(self, heritage: str) -> Dict[str, Any]:
        """Create fallback gustatory content when Gemini fails."""
        
        simple_recipe = {
            "name": f"Simple {heritage} Comfort Food",
            "description": f"A simple, comforting dish from {heritage} tradition",
            "ingredients": ["Basic pantry ingredients", "Familiar spices", "Simple preparation"],
            "instructions": ["Simple preparation steps", "Focus on familiar flavors"],
            "cultural_context": f"Traditional {heritage} comfort cooking"
        }
        
        return {
            "sense_type": "gustatory",
            "available": True,
            "elements": [simple_recipe],
            "gemini_success": False,
            "fallback_used": True
        }
    
    def _create_fallback_sensory_content(self, 
                                       consolidated_info: Dict[str, Any],
                                       cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create complete fallback sensory content."""
        
        heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
        
        return {
            "sensory_content": {
                "content_by_sense": {
                    "auditory": self._create_fallback_auditory_content(heritage),
                    "gustatory": self._create_fallback_gustatory_content(heritage),
                    "olfactory": {"sense_type": "olfactory", "available": False, "fallback_used": True},
                    "visual": {"sense_type": "visual", "available": False, "fallback_used": True},
                    "tactile": {"sense_type": "tactile", "available": False, "fallback_used": True}
                },
                "sensory_summary": {
                    "total_senses_activated": 2,
                    "generation_success": True,
                    "fallback_mode": True
                },
                "generation_metadata": {
                    "fallback_used": True,
                    "agent_version": "fallback_mode"
                }
            }
        }

# Test function
async def test_sensory_content_generator():
    """Test the fixed sensory content generator."""
    
    # Mock tools for testing
    class MockYouTubeTool:
        async def search_music(self, query, max_results=3):
            return {
                "success": True,
                "results": [{
                    "title": f"Test Music: {query}",
                    "video_id": "test123",
                    "channel_title": "Test Channel"
                }]
            }
    
    class MockGeminiTool:
        async def generate_recipe(self, prompt):
            return {
                "name": "Test Italian Recipe",
                "description": "A simple test recipe",
                "difficulty": "easy",
                "ingredients": [{"item": "test ingredient", "amount": "1 cup"}],
                "instructions": [{"step": 1, "instruction": "Test instruction"}]
            }
    
    # Create agent with mock tools
    youtube_tool = MockYouTubeTool()
    gemini_tool = MockGeminiTool()
    agent = SensoryContentGeneratorAgent(youtube_tool, gemini_tool)
    
    # Test data
    consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "age": 79,
            "preferences": ["music", "cooking"]
        },
        "request_context": {"request_type": "dashboard"}
    }
    
    cultural_profile = {"cultural_elements": {"heritage": "Italian-American"}}
    
    qloo_intelligence = {
        "success": True,
        "cultural_recommendations": {
            "artists": {
                "available": True,
                "entities": [{"name": "Andrea Bocelli"}]
            },
            "places": {
                "available": True,
                "entities": [{"name": "Tony's Italian Restaurant"}]
            }
        }
    }
    
    # Run test
    result = await agent.run(consolidated_info, cultural_profile, qloo_intelligence)
    
    sensory_content = result.get("sensory_content", {})
    print("Sensory Content Generator Test Results:")
    print(f"Senses activated: {sensory_content.get('sensory_summary', {}).get('total_senses_activated')}")
    print(f"Total elements: {sensory_content.get('sensory_summary', {}).get('total_content_elements')}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_sensory_content_generator())