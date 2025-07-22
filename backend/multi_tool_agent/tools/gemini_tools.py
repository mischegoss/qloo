"""
Google Gemini AI Tools
File: backend/multi_tool_agent/tools/gemini_tools.py

Provides interface to Google Gemini AI for recipe generation and content creation
"""

import httpx
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class GeminiRecipeGenerator:
    """
    Google Gemini AI tool for recipe generation and content creation.
    Used by Agent 4: Sensory Content Generator Agent
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
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
            
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
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
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._process_gemini_response(data)
                elif response.status_code == 400:
                    logger.error("Gemini API bad request - check prompt format")
                    return None
                elif response.status_code == 403:
                    logger.error("Gemini API forbidden - check API key")
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
        """Extract JSON object from Gemini response text."""
        
        try:
            # Look for JSON blocks in the text
            start_markers = ["{", "```json", "```"]
            end_markers = ["}", "```"]
            
            for start_marker in start_markers:
                start_idx = text.find(start_marker)
                if start_idx != -1:
                    # Find the corresponding end marker
                    if start_marker == "{":
                        # Find matching closing brace
                        brace_count = 0
                        for i, char in enumerate(text[start_idx:], start_idx):
                            if char == "{":
                                brace_count += 1
                            elif char == "}":
                                brace_count -= 1
                                if brace_count == 0:
                                    json_text = text[start_idx:i+1]
                                    return json.loads(json_text)
                    else:
                        # Look for end marker
                        for end_marker in end_markers:
                            end_idx = text.find(end_marker, start_idx + len(start_marker))
                            if end_idx != -1:
                                json_text = text[start_idx + len(start_marker):end_idx]
                                if json_text.strip().startswith("{"):
                                    return json.loads(json_text.strip())
            
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error extracting JSON: {str(e)}")
            return None
    
    def _create_fallback_recipe(self, text_content: str) -> Dict[str, Any]:
        """Create fallback recipe structure from unstructured text."""
        
        lines = text_content.split('\n')
        
        # Try to extract basic information
        name = "Generated Comfort Food Recipe"
        ingredients = []
        instructions = []
        
        # Simple parsing logic
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for section headers
            if any(keyword in line.lower() for keyword in ["ingredient", "what you need"]):
                current_section = "ingredients"
                continue
            elif any(keyword in line.lower() for keyword in ["instruction", "steps", "method", "how to"]):
                current_section = "instructions"
                continue
            elif any(keyword in line.lower() for keyword in ["recipe", "dish"]) and len(line) < 100:
                name = line
                continue
            
            # Add content to appropriate section
            if current_section == "ingredients" and line:
                ingredients.append({"item": line, "amount": "", "notes": ""})
            elif current_section == "instructions" and line:
                instructions.append({
                    "step": len(instructions) + 1,
                    "instruction": line,
                    "time": "",
                    "notes": ""
                })
        
        return {
            "name": name,
            "description": "A comforting recipe for shared cooking experiences",
            "prep_time": "15-20 minutes",
            "cook_time": "Varies",
            "total_time": "30-45 minutes",
            "servings": "2-4 people",
            "difficulty": "easy",
            "ingredients": ingredients if ingredients else [
                {"item": "Simple, familiar ingredients", "amount": "As needed", "notes": "Adapt to preferences"}
            ],
            "instructions": instructions if instructions else [
                {"step": 1, "instruction": "Follow simple cooking steps together", "time": "", "notes": "Adapt based on abilities"}
            ],
            "caregiver_customization_notes": [
                "Adapt recipe based on individual dietary needs and preferences",
                "Simplify steps based on current cooking abilities",
                "Focus on the sensory experience and shared time together"
            ],
            "dietary_alternatives": [
                {"dietary_need": "Low sodium", "substitution": "Reduce salt, use herbs and spices"},
                {"dietary_need": "Soft texture", "substitution": "Cook ingredients until very tender"}
            ],
            "sensory_engagement_tips": [
                "Enjoy the cooking aromas together",
                "Let them touch and feel safe ingredients",
                "Talk about the colors and textures of the food"
            ],
            "cultural_context": "This recipe provides opportunities for shared cooking and cultural food memories",
            "memory_connection_potential": "Cooking together can trigger positive memories of family meals and kitchen experiences"
        }
    
    async def generate_content(self, prompt: str, content_type: str = "general") -> Optional[str]:
        """
        Generate general content using Gemini AI.
        
        Args:
            prompt: Content generation prompt
            content_type: Type of content (recipe, conversation, description)
            
        Returns:
            Generated content text or None if failed
        """
        
        try:
            url = f"{self.base_url}/models/gemini-pro:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.8,
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
                        logger.info(f"Gemini content generation successful for {content_type}")
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
        Test connection to Gemini AI.
        
        Returns:
            True if connection successful, False otherwise
        """
        
        try:
            # Simple test prompt
            test_content = await self.generate_content(
                "Generate a one-sentence response confirming the API is working.",
                "test"
            )
            
            if test_content and len(test_content.strip()) > 0:
                logger.info("Gemini AI connection test successful")
                return True
            else:
                logger.error("Gemini AI connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"Gemini AI connection test exception: {str(e)}")
            return False