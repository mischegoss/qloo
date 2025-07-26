"""
Enhanced Google Gemini AI Tools - Caching Removed for Hackathon Demo
File: backend/multi_tool_agent/tools/gemini_tools.py

CHANGES:
- Removed all daily caching logic
- Direct API calls every time
- Removed cache management methods
"""

import httpx
import json
import logging
from typing import Dict, Any, Optional
from datetime import date
import hashlib

# Configure logger
logger = logging.getLogger(__name__)

class GeminiRecipeGenerator:
    """
    Google Gemini AI tool without caching.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        logger.info("Gemini AI tool initialized without caching")
    
    def _get_dementia_recipe_schema(self) -> Dict[str, Any]:
        """
        Define the JSON schema for dementia-optimized recipes.
        This ensures Gemini returns exactly the structure we need.
        """
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Recipe name that's culturally relevant and appealing"
                },
                "total_time": {
                    "type": "string", 
                    "description": "Total cooking time (e.g., '15 minutes', '1 hour')"
                },
                "ingredients": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "amount": {"type": "string"},
                            "item": {"type": "string"},
                            "location": {
                                "type": "string",
                                "enum": ["pantry", "refrigerator", "freezer", "spice_rack", "fresh"]
                            },
                            "safety_note": {
                                "type": "string",
                                "description": "Safety guidance for dementia patients if needed"
                            }
                        },
                        "required": ["amount", "item", "location"]
                    }
                },
                "instructions": {
                    "type": "array",
                    "items": {
                        "type": "object", 
                        "properties": {
                            "step": {"type": "integer"},
                            "instruction": {"type": "string"},
                            "safety_note": {"type": "string"},
                            "difficulty": {
                                "type": "string",
                                "enum": ["easy", "moderate"] 
                            }
                        },
                        "required": ["step", "instruction", "difficulty"]
                    }
                },
                "conversation_starters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "3-5 conversation prompts related to the recipe"
                },
                "cultural_significance": {
                    "type": "string",
                    "description": "Why this recipe connects to the person's heritage"
                },
                "dementia_adaptations": {
                    "type": "array", 
                    "items": {"type": "string"},
                    "description": "Specific adaptations for dementia patients"
                }
            },
            "required": ["name", "total_time", "ingredients", "instructions", "conversation_starters", "cultural_significance"]
        }
    
    def _create_recipe_prompt(self, cultural_heritage: str, recipe_name: str, theme_context: str = "") -> str:
        """
        Create a comprehensive prompt for Gemini recipe generation.
        """
        
        base_prompt = f"""
Create a culturally authentic {cultural_heritage} recipe for "{recipe_name}" that's specifically adapted for someone with dementia.

CRITICAL REQUIREMENTS:
- Must be from {cultural_heritage} culinary tradition
- Steps must be simple and clear for dementia patients
- Include safety considerations for cognitive impairment
- 5 ingredients maximum for simplicity
- Cooking time under 30 minutes preferred
- Include conversation starters about cultural memories

THEME CONTEXT: {theme_context}

DEMENTIA-SPECIFIC ADAPTATIONS REQUIRED:
- Clear, numbered steps
- Safety warnings where needed
- Simple ingredient list with locations (pantry, refrigerator, etc.)
- Conversation prompts to trigger positive memories
- Cultural significance explanation

Return ONLY valid JSON matching this exact schema:
{json.dumps(self._get_dementia_recipe_schema(), indent=2)}

EXAMPLE INGREDIENT FORMAT:
"ingredients": [
  {
    "amount": "2 cups",
    "item": "all-purpose flour",
    "location": "pantry",
    "safety_note": "Check expiration date"
  }
]

EXAMPLE INSTRUCTION FORMAT:
"instructions": [
  {
    "step": 1,
    "instruction": "Preheat oven to 350°F",
    "difficulty": "easy",
    "safety_note": "Ask for help with oven if needed"
  }
]

Generate the recipe now:
"""
        return base_prompt.strip()
    
    async def generate_cultural_recipe(self, 
                                       cultural_heritage: str, 
                                       recipe_name: str,
                                       theme_context: str = "") -> Optional[Dict[str, Any]]:
        """
        Generate a culturally relevant, dementia-optimized recipe using Gemini AI.
        """
        
        try:
            logger.info(f"Gemini recipe generation (LIVE API): {cultural_heritage} - {recipe_name}")
            
            prompt = self._create_recipe_prompt(cultural_heritage, recipe_name, theme_context)
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
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
                    
                    # Extract the generated content
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        
                        try:
                            # Parse the JSON response
                            recipe_data = json.loads(content)
                            logger.info(f"✅ Gemini recipe generated successfully: {recipe_data.get('name', 'Unknown')}")
                            
                            return recipe_data
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"❌ Failed to parse Gemini JSON response: {e}")
                            logger.error(f"Raw content: {content[:200]}...")
                            return None
                    else:
                        logger.error("❌ No content in Gemini response")
                        return None
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("❌ Gemini API timeout")
            return None
        except Exception as e:
            logger.error(f"❌ Gemini recipe generation failed: {e}")
            return None
    
    def _get_fallback_recipes(self) -> Dict[str, Dict[str, Any]]:
        """
        Fallback recipes for when Gemini API fails.
        """
        return {
            "italian-american": {
                "name": "Simple Italian-American Mozzarella Toast",
                "total_time": "5 minutes",
                "ingredients": [
                    {
                        "amount": "2 slices",
                        "item": "Italian bread",
                        "location": "pantry",
                        "safety_note": "Check for mold before using"
                    },
                    {
                        "amount": "4 slices",
                        "item": "fresh mozzarella",
                        "location": "refrigerator"
                    }
                ],
                "instructions": [
                    {
                        "step": 1,
                        "instruction": "Toast bread lightly",
                        "difficulty": "easy",
                        "safety_note": "Watch toaster carefully"
                    },
                    {
                        "step": 2,
                        "instruction": "Place mozzarella on warm toast",
                        "difficulty": "easy"
                    }
                ],
                "conversation_starters": [
                    "Did you ever make this with your family?",
                    "What's your favorite Italian bread?",
                    "Do you remember the smell of fresh mozzarella?"
                ],
                "cultural_significance": "A simple comfort food from Italian-American tradition",
                "dementia_adaptations": ["Very simple preparation", "Familiar ingredients", "Quick to make"]
            },
            "general": {
                "name": "Warm Comfort Toast",
                "total_time": "3 minutes", 
                "ingredients": [
                    {
                        "amount": "1 slice",
                        "item": "bread",
                        "location": "pantry"
                    },
                    {
                        "amount": "1 tbsp",
                        "item": "butter",
                        "location": "refrigerator"
                    }
                ],
                "instructions": [
                    {
                        "step": 1,
                        "instruction": "Toast bread until golden",
                        "difficulty": "easy"
                    },
                    {
                        "step": 2,
                        "instruction": "Spread butter while warm",
                        "difficulty": "easy"
                    }
                ],
                "conversation_starters": [
                    "What kind of bread did you eat growing up?",
                    "Do you like your toast light or dark?",
                    "Did you ever make breakfast for your family?"
                ],
                "cultural_significance": "A universal comfort food that brings warmth and familiarity",
                "dementia_adaptations": ["Extremely simple", "Familiar process", "Comforting smell and taste"]
            }
        }
    
    async def get_recipe_suggestion(self, cultural_heritage: str, theme_context: str = "") -> Dict[str, Any]:
        """
        Get a recipe suggestion, with fallback to predefined recipes.
        """
        
        # Common recipe names by heritage
        recipe_suggestions = {
            "italian-american": ["Pasta with Garlic", "Mozzarella Toast", "Simple Marinara", "Herb Bread"],
            "irish": ["Soda Bread", "Irish Stew", "Colcannon", "Tea Cake"],
            "german": ["Apple Strudel", "Sauerbraten", "Potato Salad", "Pretzel Bread"],
            "mexican": ["Quesadilla", "Rice and Beans", "Tortilla Soup", "Guacamole"],
            "jewish": ["Matzo Ball Soup", "Challah Bread", "Brisket", "Latkes"],
            "chinese": ["Fried Rice", "Dumpling Soup", "Tea Eggs", "Steamed Buns"],
            "general": ["Chicken Soup", "Grilled Cheese", "Apple Pie", "Meatloaf"]
        }
        
        heritage_key = cultural_heritage.lower().replace(" ", "-") if cultural_heritage else "general"
        recipe_names = recipe_suggestions.get(heritage_key, recipe_suggestions["general"])
        
        # Try first recipe name
        recipe_name = recipe_names[0]
        
        # Try Gemini generation
        gemini_result = await self.generate_cultural_recipe(cultural_heritage, recipe_name, theme_context)
        
        if gemini_result:
            return gemini_result
        
        # Fallback to predefined recipes
        logger.warning(f"⚠️ Gemini failed, using fallback recipe for {heritage_key}")
        fallback_recipes = self._get_fallback_recipes()
        return fallback_recipes.get(heritage_key, fallback_recipes["general"])

# Export the main class
__all__ = ["GeminiRecipeGenerator"]