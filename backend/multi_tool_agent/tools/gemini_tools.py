"""
Fixed Google Gemini AI Tools
File: backend/multi_tool_agent/tools/gemini_tools.py

Provides interface to Google Gemini AI for recipe generation and content creation
"""

import httpx
import json
import logging
import re
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

class GeminiRecipeGenerator:
    """
    Google Gemini AI tool for recipe generation and content creation.
    Used by Agent 4: Sensory Content Generator Agent
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        logger.info("Gemini AI tool initialized with gemini-2.5-flash model")
        
    async def generate_recipe(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate a recipe using Gemini AI.
        
        Args:
            prompt: Recipe generation prompt with cultural context and requirements
            
        Returns:
            Generated recipe data or None if failed
        """
        
        try:
            # Enhance prompt for better recipe generation
            enhanced_prompt = f"""
            {prompt}
            
            Please provide the response as a JSON object with the following structure:
            {{
                "name": "Recipe name",
                "description": "Brief description of the dish",
                "prep_time": "Preparation time",
                "cook_time": "Cooking time", 
                "total_time": "Total time",
                "servings": "Number of servings",
                "difficulty": "easy/medium/hard",
                "ingredients": [
                    {{"item": "ingredient name", "amount": "quantity", "notes": "optional notes"}}
                ],
                "instructions": [
                    {{"step": 1, "instruction": "Step description", "time": "time if applicable", "notes": "optional notes"}}
                ],
                "caregiver_customization_notes": [
                    "Adaptation note 1",
                    "Adaptation note 2"
                ],
                "dietary_alternatives": [
                    {{"dietary_need": "need", "substitution": "alternative ingredient"}}
                ],
                "sensory_engagement_tips": [
                    "Sensory tip 1",
                    "Sensory tip 2"
                ],
                "cultural_context": "Why this recipe connects to the cultural elements mentioned",
                "memory_connection_potential": "How this recipe might trigger positive memories"
            }}
            
            Focus on:
            - Simple, accessible ingredients
            - Clear, step-by-step instructions
            - Opportunities for caregiver-patient interaction
            - Sensory engagement (smells, textures, tastes)
            - Safety considerations for dementia care
            - Adaptability based on current abilities
            """
            
            # Use gemini-2.5-flash model
            url = f"{self.base_url}/models/gemini-2.5-flash:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": enhanced_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
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
            
            headers = {"Content-Type": "application/json"}
            
            logger.info(f"Generating recipe with Gemini 2.5 Flash")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info("Gemini recipe generation successful")
                    return self._process_gemini_response(data)
                elif response.status_code == 400:
                    logger.error(f"Gemini API bad request: {response.text}")
                    return None
                elif response.status_code == 403:
                    logger.error("Gemini API forbidden - check API key")
                    return None
                elif response.status_code == 404:
                    logger.error("Gemini model not found - check model name")
                    return None
                else:
                    logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("Gemini API timeout")
            return None
        except Exception as e:
            logger.error(f"Gemini API exception: {str(e)}")
            return None
    
    async def generate_content(self, prompt: str, content_type: str = "general") -> Optional[str]:
        """
        Generate general content using Gemini AI.
        
        Args:
            prompt: Content generation prompt
            content_type: Type of content to generate
            
        Returns:
            Generated content string or None if failed
        """
        
        try:
            # Use gemini-2.5-flash model
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
                    "maxOutputTokens": 1024,
                }
            }
            
            headers = {"Content-Type": "application/json"}
            
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("candidates") and data["candidates"][0].get("content"):
                        content = data["candidates"][0]["content"]["parts"][0].get("text", "")
                        logger.info(f"Gemini content generation successful ({content_type})")
                        return content
                    else:
                        logger.error("No content in Gemini response")
                        return None
                else:
                    logger.error(f"Gemini content generation error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Gemini content generation exception: {str(e)}")
            return None
    
    async def test_connection(self) -> bool:
        """
        Test connection to Gemini API with gemini-2.5-flash model.
        
        Returns:
            True if connection successful, False otherwise
        """
        
        try:
            logger.info("Testing Gemini API connection with gemini-2.5-flash...")
            
            test_prompt = "Generate a simple test response to verify the API connection is working."
            result = await self.generate_content(test_prompt, "test")
            
            if result and len(result.strip()) > 0:
                logger.info("Gemini AI connection test successful")
                return True
            else:
                logger.error("Gemini AI connection test failed - no response")
                return False
                
        except Exception as e:
            logger.error(f"Gemini AI connection test exception: {str(e)}")
            return False
    
    def _process_gemini_response(self, response_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process Gemini response and extract recipe data."""
        
        try:
            if not response_data.get("candidates"):
                logger.error("No candidates in Gemini response")
                return None
            
            candidate = response_data["candidates"][0]
            if not candidate.get("content", {}).get("parts"):
                logger.error("No content parts in Gemini response")
                return None
            
            # Extract text content
            text_content = candidate["content"]["parts"][0].get("text", "")
            
            if not text_content:
                logger.error("No text content in Gemini response")
                return None
            
            # Try to extract JSON from the response
            recipe_data = self._extract_json_from_text(text_content)
            
            if recipe_data:
                logger.info(f"Recipe generated successfully: {recipe_data.get('name', 'Unknown')}")
                return recipe_data
            else:
                # Fallback: create structured data from text
                return self._create_fallback_recipe(text_content)
                
        except Exception as e:
            logger.error(f"Error processing Gemini response: {str(e)}")
            return None
    
    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON object from Gemini response text with improved parsing."""
        
        try:
            logger.debug(f"Attempting to extract JSON from text: {text[:200]}...")
            
            # Method 1: Try to find JSON between code blocks
            json_pattern = r'```json\s*(.*?)\s*```'
            match = re.search(json_pattern, text, re.DOTALL | re.IGNORECASE)
            
            if match:
                json_str = match.group(1).strip()
                logger.debug(f"Found JSON in code block: {json_str[:100]}...")
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    logger.warning(f"Code block JSON parse failed: {e}")
            
            # Method 2: Try to find JSON in the text (greedy match)
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, text, re.DOTALL)
            
            if match:
                json_str = match.group(0).strip()
                logger.debug(f"Found JSON pattern: {json_str[:100]}...")
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    logger.warning(f"Pattern JSON parse failed: {e}")
            
            # Method 3: Try to find balanced braces
            start_idx = text.find('{')
            if start_idx != -1:
                brace_count = 0
                end_idx = start_idx
                
                for i, char in enumerate(text[start_idx:], start_idx):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
                
                if brace_count == 0:
                    json_str = text[start_idx:end_idx].strip()
                    logger.debug(f"Found balanced JSON: {json_str[:100]}...")
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Balanced JSON parse failed: {e}")
            
            # Method 4: Look for specific recipe structure indicators
            if any(indicator in text.lower() for indicator in ["name", "ingredients", "instructions"]):
                logger.info("Text contains recipe indicators but no valid JSON - using fallback parser")
                return self._parse_recipe_from_text(text)
            
            logger.warning("No valid JSON found in Gemini response")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting JSON: {str(e)}")
            return None
    
    def _parse_recipe_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse recipe information from plain text when JSON extraction fails."""
        
        try:
            lines = text.split('\n')
            recipe_data = {
                "name": "Generated Recipe",
                "description": "Recipe generated by AI",
                "prep_time": "15 minutes",
                "cook_time": "30 minutes",
                "total_time": "45 minutes",
                "servings": "4",
                "difficulty": "easy",
                "ingredients": [],
                "instructions": [],
                "caregiver_customization_notes": ["Adjust ingredients based on dietary needs"],
                "dietary_alternatives": [],
                "sensory_engagement_tips": ["Encourage participation in safe preparation"],
                "cultural_context": "Traditional comfort food",
                "memory_connection_potential": "May evoke positive food memories"
            }
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for section headers
                line_lower = line.lower()
                if any(word in line_lower for word in ["recipe", "name"]) and ":" in line:
                    recipe_data["name"] = line.split(":", 1)[1].strip()
                elif "ingredients" in line_lower:
                    current_section = "ingredients"
                elif any(word in line_lower for word in ["instructions", "directions", "steps"]):
                    current_section = "instructions"
                elif line.startswith(('-', '•', '*')) or line[0].isdigit():
                    # This is a list item
                    clean_line = re.sub(r'^[-•*\d.)\s]+', '', line).strip()
                    
                    if current_section == "ingredients" and clean_line:
                        recipe_data["ingredients"].append({
                            "item": clean_line,
                            "amount": "",
                            "notes": ""
                        })
                    elif current_section == "instructions" and clean_line:
                        recipe_data["instructions"].append({
                            "step": len(recipe_data["instructions"]) + 1,
                            "instruction": clean_line,
                            "time": "",
                            "notes": ""
                        })
            
            # Ensure we have at least some content
            if not recipe_data["ingredients"]:
                recipe_data["ingredients"].append({
                    "item": "Comfort food ingredients",
                    "amount": "As needed",
                    "notes": "Based on cultural preferences"
                })
            
            if not recipe_data["instructions"]:
                recipe_data["instructions"].append({
                    "step": 1,
                    "instruction": "Follow traditional preparation methods",
                    "time": "",
                    "notes": ""
                })
            
            logger.info(f"Successfully parsed recipe from text: {recipe_data['name']}")
            return recipe_data
            
        except Exception as e:
            logger.error(f"Failed to parse recipe from text: {e}")
            return None
    
    def _create_fallback_recipe(self, text_content: str) -> Dict[str, Any]:
        """Create fallback recipe structure from text content."""
        
        lines = text_content.split('\n')
        name = "Comfort Food Recipe"
        ingredients = []
        instructions = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'ingredients' in line.lower():
                current_section = "ingredients"
            elif 'instructions' in line.lower() or 'directions' in line.lower():
                current_section = "instructions"
            elif line.startswith('-') or line.startswith('•'):
                if current_section == "ingredients":
                    ingredients.append({"item": line[1:].strip(), "amount": "", "notes": ""})
                elif current_section == "instructions":
                    instructions.append({
                        "step": len(instructions) + 1,
                        "instruction": line[1:].strip(),
                        "time": "",
                        "notes": ""
                    })
        
        return {
            "name": name,
            "description": "A comforting recipe generated by AI",
            "prep_time": "15 minutes",
            "cook_time": "30 minutes",
            "total_time": "45 minutes",
            "servings": "4",
            "difficulty": "easy",
            "ingredients": ingredients if ingredients else [
                {"item": "Comfort food ingredients", "amount": "As needed", "notes": "Based on preferences"}
            ],
            "instructions": instructions if instructions else [
                {"step": 1, "instruction": "Follow traditional preparation methods", "time": "", "notes": ""}
            ],
            "caregiver_customization_notes": [
                "Adjust ingredients based on dietary needs",
                "Simplify steps as needed for current abilities"
            ],
            "dietary_alternatives": [],
            "sensory_engagement_tips": [
                "Encourage participation in safe preparation steps",
                "Focus on familiar aromas and textures"
            ],
            "cultural_context": "Recipe designed for comfort and familiarity",
            "memory_connection_potential": "May evoke positive food memories"
        }

# Export the main class
__all__ = ["GeminiRecipeGenerator"]