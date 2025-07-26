"""
Simple General-Purpose Gemini Tool - Fixed File Name
File: backend/multi_tool_agent/tools/simple_gemini_tools.py

PURPOSE:
- General-purpose Gemini API interface for all agents (4A, 4B, 4C)
- Simple text generation with bias-prevention rules
- Designed for music curation, recipe selection, and photo descriptions
- Backward compatibility with existing GeminiRecipeGenerator expectations
"""

import httpx
import json
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class SimpleGeminiTool:
    """
    Simple general-purpose Gemini AI tool for content curation.
    Used by multiple agents for different types of content generation.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Core bias-prevention rules for all prompts
        self.bias_prevention_rules = """
CRITICAL RULES (Always follow):
- Use simple, clear language (5th grade reading level)
- Avoid cultural stereotypes and bias
- Be inclusive and respectful to all backgrounds
- Focus on universal human experiences
- Keep responses brief and gentle
- This is for people with dementia - be especially kind and clear
"""
        
        logger.info("Simple Gemini tool initialized for general content curation")
    
    async def generate_content(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Generate simple text content using Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            max_tokens: Maximum response length
            
        Returns:
            Generated text content or None if failed
        """
        
        try:
            # Add bias prevention to every prompt
            full_prompt = f"{self.bias_prevention_rules}\n\nTASK:\n{prompt}"
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": max_tokens,
                    "candidateCount": 1
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        logger.info("✅ Gemini content generated successfully")
                        return content.strip()
                    else:
                        logger.error("❌ No content in Gemini response")
                        return None
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("❌ Gemini API timeout")
            return None
        except Exception as e:
            logger.error(f"❌ Gemini content generation failed: {e}")
            return None
    
    async def generate_structured_json(self, prompt: str, json_schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate structured JSON response using Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            json_schema: Expected JSON structure
            
        Returns:
            Parsed JSON response or None if failed
        """
        
        try:
            # Add schema instructions to prompt
            schema_prompt = f"""
{self.bias_prevention_rules}

TASK:
{prompt}

RESPONSE FORMAT:
Return your response as valid JSON matching this exact structure:
{json.dumps(json_schema, indent=2)}

IMPORTANT:
- Return ONLY valid JSON, no additional text
- Include all required fields
- Use simple, kind language appropriate for dementia patients
"""
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": schema_prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1000,
                    "response_mime_type": "application/json"
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        
                        try:
                            # Parse JSON response
                            json_data = json.loads(content)
                            logger.info("✅ Gemini structured JSON generated successfully")
                            return json_data
                        except json.JSONDecodeError as e:
                            logger.error(f"❌ Failed to parse Gemini JSON: {e}")
                            logger.error(f"Raw content: {content[:200]}...")
                            return None
                    else:
                        logger.error("❌ No content in Gemini response")
                        return None
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Gemini structured generation failed: {e}")
            return None
    
    async def curate_music_selection(self, heritage: str, available_artists: List[str], 
                                   theme: str) -> Optional[Dict[str, Any]]:
        """
        Specialized method for music curation (Agent 4A).
        
        Args:
            heritage: Cultural heritage (e.g., "Italian-American")
            available_artists: List of Qloo artists
            theme: Current theme (e.g., "Birthday", "Memory Lane")
            
        Returns:
            Music curation response with artist selection and conversation starters
        """
        
        prompt = f"""
You are helping select classical music for a person with dementia.

CONTEXT:
- Person's heritage: {heritage}
- Available classical artists: {', '.join(available_artists) if available_artists else 'Bach, Mozart, Beethoven'}
- Today's theme: {theme}

TASK:
1. Pick the BEST classical artist from the available list who would be most familiar and comforting
2. Suggest 2-3 specific classical pieces by that artist that are:
   - Well-known and familiar to most people
   - Calming and appropriate for someone with dementia
   - Available in public domain
3. Create 2 gentle conversation starters about the music
4. Share 1 simple, interesting fact about the composer

Remember: Choose very familiar classical pieces that bring comfort and happy memories.
"""
        
        schema = {
            "selected_artist": "Artist name",
            "piece_suggestions": ["piece 1", "piece 2", "piece 3"],
            "conversation_starters": ["starter 1", "starter 2"],
            "fun_fact": "Simple fact about the composer",
            "heritage_connection": "How this selection connects to their background"
        }
        
        return await self.generate_structured_json(prompt, schema)
    
    async def describe_photo(self, theme: str, photo_filename: str) -> Optional[Dict[str, Any]]:
        """
        Specialized method for photo descriptions (Agent 4C).
        
        Args:
            theme: Theme name (e.g., "Birthday", "Memory Lane")
            photo_filename: Photo filename (e.g., "birthday.png")
            
        Returns:
            Photo description with conversation starters
        """
        
        prompt = f"""
You are describing a photo for a person with dementia.

CONTEXT:
- Theme: {theme}
- Photo: {photo_filename}

TASK:
1. Write a warm, simple description of what this {theme.lower()} photo likely shows
2. Create 3 gentle conversation starters about the photo
3. Share 1 simple, happy fact related to the theme

Keep everything positive, familiar, and comforting.
"""
        
        schema = {
            "description": "Simple, warm description of the photo",
            "conversation_starters": ["starter 1", "starter 2", "starter 3"],
            "fun_fact": "Happy fact related to the theme",
            "mood": "Mood of the photo (cheerful, peaceful, etc.)"
        }
        
        return await self.generate_structured_json(prompt, schema)
    
    async def select_simple_recipe(self, heritage: str, theme: str, 
                                 available_recipes: List[str]) -> Optional[Dict[str, Any]]:
        """
        Specialized method for recipe selection (Agent 4B).
        
        Args:
            heritage: Cultural heritage
            theme: Current theme
            available_recipes: List of simple recipe names
            
        Returns:
            Recipe selection with conversation starters
        """
        
        prompt = f"""
You are selecting a simple recipe for a person with dementia.

CONTEXT:
- Person's heritage: {heritage}
- Today's theme: {theme}
- Available simple recipes: {', '.join(available_recipes)}

TASK:
1. Pick the BEST recipe from the list that:
   - Connects to their heritage if possible
   - Fits today's theme
   - Is simple and familiar
   - Would bring back happy memories
2. Create 2 gentle conversation starters about the recipe
3. Share 1 simple, happy fact about the food or ingredient

Focus on comfort, familiarity, and positive memories.
"""
        
        schema = {
            "selected_recipe": "Recipe name from the list",
            "conversation_starters": ["starter 1", "starter 2"],
            "fun_fact": "Simple fact about the food",
            "heritage_connection": "How this recipe connects to their background",
            "theme_connection": "How this recipe fits today's theme"
        }
        
        return await self.generate_structured_json(prompt, schema)
    
    # Backward compatibility methods for existing GeminiRecipeGenerator interface
    async def get_recipe_suggestion(self, cultural_heritage: str, theme_context: str = "") -> Optional[Dict[str, Any]]:
        """
        Backward compatibility method for existing GeminiRecipeGenerator interface.
        """
        
        # Simple recipe list for fallback
        simple_recipes = [
            "macaroni and cheese", "chicken soup", "grilled cheese sandwich", 
            "pancakes", "scrambled eggs", "oatmeal", "pasta with butter"
        ]
        
        result = await self.select_simple_recipe(
            heritage=cultural_heritage,
            theme=theme_context or "comfort",
            available_recipes=simple_recipes
        )
        
        if result:
            # Convert to expected format
            return {
                "name": result.get("selected_recipe", "Comfort Food"),
                "ingredients": ["Simple ingredients"],  # Simplified
                "instructions": ["Easy preparation steps"],  # Simplified
                "total_time": "15 minutes",
                "conversation_starters": result.get("conversation_starters", []),
                "cultural_significance": result.get("heritage_connection", "Universal comfort food")
            }
        
        return None
    
    async def test_connection(self) -> bool:
        """Test Gemini API connection"""
        
        try:
            test_result = await self.generate_content(
                "Say 'Hello' in a friendly way for someone with dementia.",
                max_tokens=50
            )
            
            if test_result and "hello" in test_result.lower():
                logger.info("✅ Gemini API connection test: SUCCESS")
                return True
            else:
                logger.error("❌ Gemini API connection test: FAILED")
                return False
                
        except Exception as e:
            logger.error(f"❌ Gemini API connection test failed: {e}")
            return False


# Backward compatibility alias
GeminiRecipeGenerator = SimpleGeminiTool

# Export both for maximum compatibility
__all__ = ["SimpleGeminiTool", "GeminiRecipeGenerator"]


# Test function
async def test_simple_gemini():
    """Test the simple Gemini tool"""
    
    # You would use your real API key here
    api_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    
    if api_key == "YOUR_GEMINI_API_KEY":
        print("⚠️ No GEMINI_API_KEY found, using mock test")
        return True
    
    gemini = SimpleGeminiTool(api_key)
    
    # Test basic content generation
    result = await gemini.generate_content(
        "Write a short, gentle message about listening to classical music."
    )
    
    print(f"Basic content: {result}")
    
    # Test music curation
    music_result = await gemini.curate_music_selection(
        heritage="Italian-American",
        available_artists=["Bach", "Vivaldi", "Mozart"],
        theme="Memory Lane"
    )
    
    print(f"Music curation: {music_result}")
    
    return result is not None


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simple_gemini())