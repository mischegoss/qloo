"""
Enhanced Simple Gemini Tools - Added Cultural Photo Enhancement
File: backend/multi_tool_agent/tools/simple_gemini_tools.py

NEW ADDITION:
- Added enhance_photo_culturally() method specifically for Agent 4C
- Integrates Qloo cultural profile with photo descriptions
- Creates culturally-relevant conversation starters
- Maintains all existing functionality
"""

import httpx
import json
import logging
import os
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
    
    # NEW METHOD: Cultural Photo Enhancement for Agent 4C
    async def enhance_photo_culturally(self, photo_description: str, heritage: str, 
                                     birth_year: int, theme: str, patient_name: str = "Friend",
                                     original_starters: List[str] = None,
                                     qloo_artists: List[str] = None) -> Optional[Dict[str, Any]]:
        """
        NEW METHOD: Enhance photo interactions with cultural context for Agent 4C.
        
        Args:
            photo_description: Google Vision description of the photo
            heritage: Patient's cultural heritage (e.g., "Italian-American")
            birth_year: Year patient was born (e.g., 1945)
            theme: Today's theme (e.g., "Birthday", "Family")
            patient_name: Patient's first name
            original_starters: Original conversation starters from JSON
            qloo_artists: Artists from Qloo for cultural context
            
        Returns:
            Enhanced conversation starters with cultural context
        """
        
        current_age = 2024 - birth_year
        cultural_context = f"interested in {', '.join(qloo_artists[:2]) if qloo_artists else 'classical music'}"
        original_text = '\n'.join(f"- {starter}" for starter in (original_starters or []))
        
        prompt = f"""
PHOTO CONTEXT:
{photo_description}

PATIENT CONTEXT:
- Name: {patient_name}
- Cultural Heritage: {heritage}
- Born: {birth_year} (age {current_age})
- Cultural interests: {cultural_context}
- Today's theme: {theme}

ORIGINAL CONVERSATION STARTERS:
{original_text}

TASK:
Create 3 culturally-enhanced conversation starters that:

1. Connect this photo to their {heritage} heritage and cultural background
2. Reference experiences someone born in {birth_year} might have had
3. Stay gentle, positive, and appropriate for dementia care
4. Feel personally relevant and culturally meaningful
5. Build on what's shown in the photo

Make each question specific to their cultural background while staying connected to the photo content.
Avoid stereotypes - focus on genuine cultural experiences and memories.

Example approach:
- If Italian + birthday photo → "Did your Italian family sing 'Buon Compleanno' at birthday parties?"
- If Irish + music photo → "Do you remember Irish folk songs or fiddle music from your childhood?"
- If Jewish + family photo → "Did your family have special traditions for gatherings?"

IMPORTANT: Keep language simple, warm, and respectful. This is for someone with dementia.
"""
        
        schema = {
            "enhanced_conversation_starters": [
                "Cultural question 1 connecting photo to heritage",
                "Cultural question 2 referencing their generation", 
                "Cultural question 3 about personal cultural experiences"
            ],
            "cultural_connection_summary": "Brief explanation of how this connects to their background",
            "generation_context": "How this relates to their life experiences from their era"
        }
        
        result = await self.generate_structured_json(prompt, schema)
        
        if result:
            logger.info(f"🤖 ✅ Cultural photo enhancement completed for {heritage} heritage")
        else:
            logger.warning(f"🤖 ⚠️ Cultural photo enhancement failed, using fallback")
        
        return result
    
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
        Specialized method for photo descriptions (Agent 4C fallback).
        
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
    
    # NEW: Test cultural photo enhancement
    photo_result = await gemini.enhance_photo_culturally(
        photo_description="Children celebrating a birthday party with cake and candles",
        heritage="Italian-American",
        birth_year=1945,
        theme="Birthday",
        patient_name="Maria",
        original_starters=["How did you celebrate birthdays?"],
        qloo_artists=["Vivaldi", "Puccini"]
    )
    
    print(f"Cultural photo enhancement: {photo_result}")
    
    return result is not None


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simple_gemini())