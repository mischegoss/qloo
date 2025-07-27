"""
Simple Gemini Tools - Fixed Timeouts Version
File: backend/multi_tool_agent/tools/simple_gemini_tools.py

TIMEOUT FIX: Increased from 30 seconds to 90 seconds for all Gemini API calls
(Gemini can take longer due to complex prompts and generation)
"""

import asyncio
import logging
import json
from typing import Dict, Any, Optional, List

try:
    import httpx
except ImportError:
    httpx = None

logger = logging.getLogger(__name__)

class SimpleGeminiTool:
    """
    Simplified Gemini AI tool for content generation.
    
    TIMEOUT FIX: Increased all timeouts to 90 seconds for reliability.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Bias prevention for dementia care
        self.bias_prevention_rules = """
        CRITICAL DEMENTIA CARE GUIDELINES:
        - Use positive, uplifting language only
        - Focus on happy memories and pleasant experiences
        - Avoid mentioning death, loss, confusion, or negative topics
        - Use simple, clear language appropriate for seniors
        - Include culturally respectful content only
        - Generate safe, family-friendly content
        """
        
        logger.info("Simple Gemini tool initialized for general content curation")
    
    async def generate_content(self, prompt: str, max_tokens: int = 500) -> Optional[str]:
        """
        Generate content using Gemini with bias prevention.
        
        Args:
            prompt: The prompt to send to Gemini
            max_tokens: Maximum response length
            
        Returns:
            Generated text content or None if failed
        """
        
        if not httpx:
            logger.warning("⚠️ httpx not available for Gemini API")
            return None
        
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
            
            # TIMEOUT FIX: Increased from 30.0 to 90.0 seconds
            async with httpx.AsyncClient(timeout=90.0) as client:
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
            prompt: The prompt describing what to generate
            json_schema: Expected JSON structure
            
        Returns:
            Parsed JSON dict or None if failed
        """
        
        if not httpx:
            logger.warning("⚠️ httpx not available for Gemini API")
            return None
        
        try:
            # Create structured prompt
            schema_str = json.dumps(json_schema, indent=2)
            full_prompt = f"""
            {self.bias_prevention_rules}
            
            TASK: {prompt}
            
            RESPONSE FORMAT: Return ONLY valid JSON that matches this exact schema:
            {schema_str}
            
            IMPORTANT:
            - Return ONLY the JSON, no additional text
            - Ensure all required fields are included
            - Use appropriate data types (strings, arrays, etc.)
            - Content must be positive and appropriate for seniors with dementia
            """
            
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
                    "temperature": 0.3,  # Lower temperature for structured output
                    "topK": 20,
                    "topP": 0.8,
                    "maxOutputTokens": 1000,
                    "candidateCount": 1
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            # TIMEOUT FIX: Increased from 30.0 to 90.0 seconds
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        
                        # Try to parse JSON
                        try:
                            # Clean up the response (remove code blocks if present)
                            content = content.strip()
                            if content.startswith("```json"):
                                content = content[7:]
                            if content.endswith("```"):
                                content = content[:-3]
                            content = content.strip()
                            
                            parsed_json = json.loads(content)
                            logger.info("✅ Gemini structured JSON generated successfully")
                            return parsed_json
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"❌ Failed to parse Gemini JSON: {e}")
                            logger.error(f"Raw response: {content[:200]}...")
                            return None
                    else:
                        logger.error("❌ No content in Gemini response")
                        return None
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("❌ Gemini structured generation timeout")
            return None
        except Exception as e:
            logger.error(f"❌ Gemini structured generation failed: {e}")
            return None
    
    async def curate_music_selection(self, 
                                   heritage: str, 
                                   available_artists: List[str],
                                   theme: str = "classical music") -> Optional[Dict[str, Any]]:
        """
        Use Gemini to intelligently curate music selection.
        
        Args:
            heritage: Patient's cultural heritage
            available_artists: List of available artist names
            theme: Music theme (default: classical music)
            
        Returns:
            Curated music selection or None if failed
        """
        
        prompt = f"""
        Select the most appropriate classical music for a {heritage} senior citizen.
        
        Available artists: {', '.join(available_artists) if available_artists else 'None'}
        Theme: {theme}
        
        Consider:
        - Cultural connection to {heritage} heritage
        - Calming, familiar classical pieces
        - Appropriate for seniors with memory care needs
        - Well-known, accessible compositions
        
        If no artists provided, suggest appropriate classical composer.
        """
        
        schema = {
            "selected_artist": "string",
            "piece_suggestions": ["string"],
            "conversation_starters": ["string"],
            "fun_fact": "string",
            "heritage_connection": "string"
        }
        
        return await self.generate_structured_json(prompt, schema)
    
    async def enhance_photo_description(self, 
                                      photo_info: Dict[str, Any],
                                      patient_heritage: str,
                                      theme: str) -> Optional[Dict[str, Any]]:
        """
        Use Gemini to enhance photo descriptions with cultural context.
        
        Args:
            photo_info: Existing photo analysis data
            patient_heritage: Patient's cultural heritage
            theme: Current theme
            
        Returns:
            Enhanced photo content or None if failed
        """
        
        photo_desc = photo_info.get("google_vision_description", "A meaningful photograph")
        existing_starters = photo_info.get("conversation_starters", [])
        
        prompt = f"""
        Enhance this photo description for a {patient_heritage} senior with dementia:
        
        Original description: {photo_desc}
        Theme: {theme}
        Existing conversation starters: {existing_starters}
        
        Create culturally appropriate conversation starters that:
        - Connect to {patient_heritage} heritage when relevant
        - Are positive and memory-triggering
        - Avoid complex or potentially upsetting topics
        - Focus on happy, universal experiences
        """
        
        schema = {
            "cultural_description": "string",
            "conversation_starters": ["string"],
            "heritage_connections": ["string"],
            "memory_triggers": ["string"]
        }
        
        return await self.generate_structured_json(prompt, schema)
    
    async def generate_nostalgia_news(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate personalized nostalgia news using Gemini.
        
        Args:
            context: Full context including profile, cultural data, content data
            
        Returns:
            Generated news content or None if failed
        """
        
        profile = context.get("profile", {})
        content = context.get("today_content", {})
        
        prompt = f"""
        Create a warm, personalized news story for {profile.get('first_name', 'our friend')} today.
        
        Person: {profile.get('first_name')} from {profile.get('heritage', 'America')} background
        Age: {profile.get('age', 80)} years old
        Era: {profile.get('era', '1940s')}
        Theme: {profile.get('theme_display', 'Memory Lane')}
        Date: {profile.get('full_date')}
        
        Today's Content:
        - Music: {content.get('music', {}).get('artist', 'Classical music')}
        - Recipe: {content.get('recipe', {}).get('name', 'Comfort food')}
        - Photo: {content.get('photo', {}).get('description', 'Family memories')}
        
        Create a short, heartwarming news story (like a local newspaper) that:
        - Feels personal and relevant to their era and heritage
        - Mentions today's content naturally
        - Uses positive, uplifting language
        - Includes specific details that feel authentic
        - Avoids current events or potentially upsetting topics
        """
        
        schema = {
            "headline": "string",
            "story": "string",
            "date": "string",
            "theme": "string",
            "personal_touches": ["string"]
        }
        
        return await self.generate_structured_json(prompt, schema)
    
    async def test_connection(self) -> bool:
        """Test Gemini API connection with increased timeout"""
        try:
            test_result = await self.generate_content("Hello, this is a test.", max_tokens=50)
            return test_result is not None
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False

# Export the main class
__all__ = ["SimpleGeminiTool"]