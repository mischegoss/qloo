"""
Enhanced Google Gemini AI Tools with Structured JSON Output
File: backend/multi_tool_agent/tools/gemini_tools.py

Provides interface to Google Gemini AI for dementia-optimized recipe generation
with structured JSON schema output for reliable parsing.
"""

import httpx
import json
import logging
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

class GeminiRecipeGenerator:
    """
    Google Gemini AI tool for dementia-optimized recipe generation.
    Enhanced with structured JSON output for reliable parsing.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        logger.info("Gemini AI tool initialized with structured JSON output")
    
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
                                "description": "Any handling considerations"
                            }
                        },
                        "required": ["item", "amount", "location", "safety_note"]
                    }
                },
                "instructions": {
                    "type": "array",
                    "maxItems": 8,
                    "items": {
                        "type": "object",
                        "properties": {
                            "step": {
                                "type": "integer",
                                "description": "Step number"
                            },
                            "instruction": {
                                "type": "string",
                                "description": "One simple action only - be very specific"
                            },
                            "time": {
                                "type": "string",
                                "description": "Exact time (2 minutes, 5 minutes)"
                            },
                            "what_to_look_for": {
                                "type": "string",
                                "description": "Visual, smell, or sound cue"
                            },
                            "safety_note": {
                                "type": "string", 
                                "description": "Any safety consideration for this step"
                            },
                            "rest_break": {
                                "type": "boolean",
                                "description": "If needed after this step"
                            }
                        },
                        "required": ["step", "instruction", "time", "what_to_look_for", "safety_note", "rest_break"]
                    }
                },
                "caregiver_notes": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Guidance for caregivers"
                },
                "sensory_engagement": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Sensory experiences to notice together"
                },
                "success_indicators": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "How to know each step is working correctly"
                },
                "cultural_context": {
                    "type": "string",
                    "description": "Why this recipe connects to heritage and memories"
                },
                "memory_connection_potential": {
                    "type": "string",
                    "description": "How this might trigger positive food memories"
                }
            },
            "required": [
                "name", "description", "total_time", "difficulty",
                "ingredients", "instructions", "caregiver_notes",
                "sensory_engagement", "success_indicators", 
                "cultural_context", "memory_connection_potential"
            ]
        }
    
    async def generate_recipe(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate a dementia-optimized recipe using structured JSON output.
        
        Args:
            prompt: Recipe generation prompt with dementia-specific requirements
            
        Returns:
            Structured recipe data or None if failed
        """
        
        try:
            logger.info("Generating recipe with Gemini 2.5 Flash using structured JSON")
            
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
                    "maxOutputTokens": 2048,
                    "response_mime_type": "application/json",  # KEY: Request JSON output
                    "response_schema": self._get_dementia_recipe_schema()  # KEY: Define structure
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
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                
                response_data = response.json()
                logger.info("Gemini API response received successfully")
                
                # Debug: Log the raw response structure
                logger.info(f"DEBUG: Raw Gemini response structure: {list(response_data.keys())}")
                
                # Check for candidates
                if not response_data.get("candidates"):
                    logger.error("No candidates in Gemini response")
                    logger.info(f"DEBUG: Full response: {response_data}")
                    return None
                
                candidate = response_data["candidates"][0]
                
                # Check for content
                if not candidate.get("content"):
                    logger.error("No content in Gemini candidate")
                    logger.info(f"DEBUG: Candidate structure: {list(candidate.keys())}")
                    
                    # Check if blocked by safety filters
                    if candidate.get("finishReason") == "SAFETY":
                        logger.warning("Recipe generation blocked by Gemini safety filters")
                        safety_ratings = candidate.get("safetyRatings", [])
                        for rating in safety_ratings:
                            logger.warning(f"Safety: {rating.get('category')} - {rating.get('probability')}")
                    
                    return None
                
                # Check for parts
                if not candidate["content"].get("parts"):
                    logger.error("No content parts in Gemini response")
                    logger.info(f"DEBUG: Content structure: {list(candidate['content'].keys())}")
                    return None
                
                # Extract JSON content directly (should be JSON due to response_mime_type)
                json_content = candidate["content"]["parts"][0].get("text", "")
                
                if not json_content:
                    logger.error("No text content in Gemini response")
                    return None
                
                logger.info("Gemini recipe generation successful")
                logger.info(f"DEBUG: JSON content length: {len(json_content)} characters")
                
                # Parse the JSON response directly
                try:
                    recipe_data = json.loads(json_content)
                    logger.info("✅ Successfully parsed structured JSON recipe")
                    
                    # Validate required fields
                    required_fields = ["name", "ingredients", "instructions"]
                    if all(field in recipe_data for field in required_fields):
                        logger.info(f"✅ Recipe validation passed: {recipe_data.get('name')}")
                        return recipe_data
                    else:
                        missing_fields = [f for f in required_fields if f not in recipe_data]
                        logger.warning(f"Recipe missing required fields: {missing_fields}")
                        return None
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON response: {e}")
                    logger.info(f"DEBUG: Raw content that failed to parse: {json_content[:200]}...")
                    return None
                
        except httpx.TimeoutException:
            logger.error("Gemini API request timed out")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"Gemini API HTTP error: {e.response.status_code}")
            logger.info(f"DEBUG: Error response: {e.response.text}")
            return None  
        except Exception as e:
            logger.error(f"Gemini recipe generation exception: {e}")
            return None
    
    async def test_connection(self) -> bool:
        """Test the Gemini API connection with a simple structured request."""
        
        try:
            simple_prompt = """Create a very simple 2-ingredient comfort food recipe suitable for dementia care. 
            Focus on safety and simplicity with exact measurements and clear visual cues."""
            
            result = await self.generate_recipe(simple_prompt)
            
            if result and isinstance(result, dict) and result.get("name"):
                logger.info("Gemini structured JSON connection test successful")
                return True
            else:
                logger.error("Gemini structured JSON test failed - no valid recipe returned")
                return False
                
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False

# Export the main class
__all__ = ["GeminiRecipeGenerator"]