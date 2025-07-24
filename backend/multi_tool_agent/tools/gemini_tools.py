"""
Enhanced Google Gemini AI Tools with Daily Caching - RATE LIMITING SOLUTION
File: backend/multi_tool_agent/tools/gemini_tools.py

FIXES:
- Daily caching using in-memory dictionary
- Cache keys based on daily seed + heritage + recipe
- Immediate cache returns to avoid API calls
- Graceful fallback to base recipes if rate limited
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
    Google Gemini AI tool with daily caching to prevent rate limiting.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # DAILY CACHE - Reset each day automatically
        self._daily_cache = {}
        self._cache_date = None
        
        logger.info("Gemini AI tool initialized with daily caching")
    
    def _get_daily_seed(self) -> str:
        """Get daily seed for cache consistency."""
        today = date.today()
        return f"{today.year}-{today.month}-{today.day}"
    
    def _get_cache_key(self, heritage: str, recipe_name: str) -> str:
        """Generate cache key for daily consistency."""
        daily_seed = self._get_daily_seed()
        # Create short hash to avoid key length issues
        content_hash = hashlib.md5(f"{heritage}_{recipe_name}".lower().encode()).hexdigest()[:8]
        return f"{daily_seed}_recipe_{content_hash}"
    
    def _check_and_update_daily_cache(self):
        """Reset cache if new day."""
        today = date.today()
        if self._cache_date != today:
            logger.info("New day detected - clearing Gemini cache")
            self._daily_cache = {}
            self._cache_date = today
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from daily cache."""
        self._check_and_update_daily_cache()
        result = self._daily_cache.get(cache_key)
        if result:
            logger.info(f"Gemini cache HIT: {cache_key}")
            return result
        return None
    
    def _store_in_cache(self, cache_key: str, result: Dict[str, Any]):
        """Store result in daily cache."""
        self._check_and_update_daily_cache()
        self._daily_cache[cache_key] = result
        logger.info(f"Gemini cache STORED: {cache_key}")
    
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
                    "description": "Recipe name starting with 'Simple [Heritage] [Dish Name]'"
                },
                "description": {
                    "type": "string", 
                    "description": "One sentence about comfort, familiarity, and memory connection"
                },
                "total_time": {
                    "type": "string",
                    "description": "Maximum 25 minutes including rest breaks"
                },
                "difficulty": {
                    "type": "string",
                    "enum": ["very_easy"],
                    "description": "Always 'very_easy' for dementia care"
                },
                "ingredients": {
                    "type": "array",
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "item": {
                                "type": "string",
                                "description": "Exact ingredient name"
                            },
                            "amount": {
                                "type": "string", 
                                "description": "Precise measurement (1 cup, 2 tablespoons)"
                            },
                            "location": {
                                "type": "string",
                                "description": "Where to find it (pantry, refrigerator)"
                            },
                            "safety_note": {
                                "type": "string",
                                "description": "Safety tip for this ingredient"
                            }
                        },
                        "required": ["item", "amount", "location", "safety_note"]
                    }
                },
                "instructions": {
                    "type": "array",
                    "maxItems": 6,
                    "items": {
                        "type": "object",
                        "properties": {
                            "step": {
                                "type": "integer",
                                "description": "Step number"
                            },
                            "instruction": {
                                "type": "string",
                                "description": "Clear, simple instruction"
                            },
                            "time": {
                                "type": "string",
                                "description": "Time for this step"
                            },
                            "what_to_look_for": {
                                "type": "string",
                                "description": "Visual or sensory cues"
                            },
                            "safety_note": {
                                "type": "string",
                                "description": "Safety reminder for this step"
                            }
                        },
                        "required": ["step", "instruction", "time", "what_to_look_for", "safety_note"]
                    }
                },
                "caregiver_notes": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Tips for caregivers"
                },
                "dementia_optimized": {
                    "type": "boolean",
                    "description": "Always true for dementia care recipes"
                }
            },
            "required": ["name", "description", "total_time", "difficulty", "ingredients", "instructions", "caregiver_notes", "dementia_optimized"]
        }
    
    async def generate_recipe(self, prompt: str, heritage: str = "American", base_recipe_name: str = "comfort_food") -> Optional[Dict[str, Any]]:
        """
        Generate a dementia-optimized recipe with daily caching to prevent rate limiting.
        
        Args:
            prompt: Recipe generation prompt with dementia-specific requirements
            heritage: Heritage for cache key generation
            base_recipe_name: Base recipe name for cache key generation
            
        Returns:
            Structured recipe data or None if failed
        """
        
        # Check cache first
        cache_key = self._get_cache_key(heritage, base_recipe_name)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        try:
            logger.info(f"Generating recipe with Gemini 2.5 Flash (LIVE API): {heritage} {base_recipe_name}")
            
            # Use gemini-2.5-flash model with structured output
            url = f"{self.base_url}/models/gemini-2.5-flash:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 4096,
                    "response_mime_type": "application/json",
                    "response_schema": self._get_dementia_recipe_schema()
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH", 
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 429:
                    logger.error("Gemini API rate limit exceeded - returning None")
                    return None
                    
                response.raise_for_status()
                
                result = response.json()
                logger.info("Gemini API response received successfully")
                
                # Check if we have candidates
                if not result.get("candidates"):
                    logger.error("No candidates in Gemini response")
                    return None
                
                candidate = result["candidates"][0]
                
                # Check for safety blocks or rate limits
                if candidate.get("finishReason") == "SAFETY":
                    logger.warning("Recipe generation blocked by Gemini safety filters")
                    return None
                
                # Check for max tokens reached
                if candidate.get("finishReason") == "MAX_TOKENS":
                    logger.warning("Recipe generation hit token limit - response may be truncated")
                
                # Check for parts
                if not candidate["content"].get("parts"):
                    logger.error("No content parts in Gemini response")
                    return None
                
                # Extract JSON content directly
                json_content = candidate["content"]["parts"][0].get("text", "")
                
                if not json_content:
                    logger.error("No text content in Gemini response")
                    return None
                
                # Enhanced JSON parsing with better error handling
                try:
                    # Clean up any potential formatting issues
                    json_content = json_content.strip()
                    
                    # Check if JSON is complete
                    if not json_content.endswith('}'):
                        logger.warning("JSON response appears to be truncated")
                        
                        # Try to fix common truncation issues
                        if json_content.endswith('",'):
                            json_content = json_content[:-1] + '"'
                        elif json_content.endswith(','):
                            json_content = json_content[:-1]
                        
                        # Try to close the JSON properly
                        if not json_content.endswith('}'):
                            open_braces = json_content.count('{')
                            close_braces = json_content.count('}')
                            
                            for _ in range(open_braces - close_braces):
                                json_content += '}'
                    
                    recipe_data = json.loads(json_content)
                    logger.info("✅ Successfully parsed structured JSON recipe")
                    
                    # Validate required fields
                    required_fields = ["name", "ingredients", "instructions"]
                    if all(field in recipe_data for field in required_fields):
                        logger.info(f"✅ Recipe validation passed: {recipe_data.get('name')}")
                        
                        # Store in cache before returning
                        self._store_in_cache(cache_key, recipe_data)
                        return recipe_data
                    else:
                        missing_fields = [f for f in required_fields if f not in recipe_data]
                        logger.warning(f"Recipe missing required fields: {missing_fields}")
                        return None
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    return None
                
        except httpx.TimeoutException:
            logger.error("Gemini API request timed out")
            return None
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.error("Gemini API rate limit exceeded")
            else:
                logger.error(f"Gemini API HTTP error: {e.response.status_code}")
            return None  
        except Exception as e:
            logger.error(f"Gemini recipe generation exception: {e}")
            return None
    
    async def test_connection(self) -> bool:
        """Test the Gemini API connection with a simple cached request."""
        
        try:
            simple_prompt = """Create a very simple 2-ingredient comfort food recipe suitable for dementia care. 
            Focus on safety and simplicity with exact measurements and clear visual cues."""
            
            result = await self.generate_recipe(simple_prompt, "test", "connection_test")
            
            if result and isinstance(result, dict) and result.get("name"):
                logger.info("Gemini connection test successful")
                return True
            else:
                logger.error("Gemini test failed - no valid recipe returned")
                return False
                
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for debugging."""
        self._check_and_update_daily_cache()
        return {
            "cache_size": len(self._daily_cache),
            "cache_date": str(self._cache_date),
            "daily_seed": self._get_daily_seed(),
            "cached_keys": list(self._daily_cache.keys())
        }

# Export the main class
__all__ = ["GeminiRecipeGenerator"]