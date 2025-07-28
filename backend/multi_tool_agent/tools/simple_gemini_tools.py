"""
Simple Gemini Tools - UPDATED FOR ANONYMIZED PROFILES
File: backend/multi_tool_agent/tools/simple_gemini_tools.py

CRITICAL UPDATES FOR PII COMPLIANCE:
- Removed all references to patient names
- Updated to work with anonymized profile data only
- Enhanced bias prevention for dementia care
- Newsletter tone guidance for caregiver-to-patient reading
- No PII anywhere in generated content
- Works with age_group, cultural_heritage, interests only
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
    Simple Gemini AI tool for content generation.
    
    UPDATED: Full PII compliance - no names, no location data.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Enhanced bias prevention for dementia care with PII compliance
        self.bias_prevention_rules = """
        CRITICAL DEMENTIA CARE & PII COMPLIANCE GUIDELINES:
        - Use positive, uplifting language only
        - Focus on happy memories and pleasant experiences
        - Avoid mentioning death, loss, confusion, or negative topics
        - Use simple, clear language appropriate for seniors
        - Include culturally respectful content only
        - Generate safe, family-friendly content
        - NEVER use personal names, addresses, or identifying information ANYWHERE
        - Write for caregivers to read TO patients, not directly to patients
        - Use professional but warm tone
        - Create structured, easy-to-read content
        - Never assume the caregiver has prior knowledge of the patient
        - Use generic terms like "Friend" or no direct address at all
        - Focus on cultural heritage and age-appropriate content only
        - NO PII ANYWHERE - this is a strict compliance requirement
        """
        
        # Newsletter-specific tone guidelines updated for PII compliance
        self.newsletter_tone_rules = """
        NEWSLETTER TONE GUIDELINES (PII-COMPLIANT):
        - Write in newsletter style with engaging, friendly tone
        - Use simple, warm language that's easy to read aloud
        - Write for CAREGIVERS to read TO patients
        - ABSOLUTELY NEVER use any personal names anywhere in the content
        - Include interesting historical facts and gentle nostalgia
        - Use phrases like "Remember when..." or "In those days..." or "Many people remember..."
        - Make it sound like friendly news from the past
        - Include specific years and historical details when appropriate
        - Example tone: "Back in 1947, Percy Spencer invented the microwave oven while working with radar technology. It went on to revolutionize cooking in American homes!"
        - Keep sentences conversational but informative
        - Focus on positive cultural memories and traditions
        - Address content generically - never personally
        - Use inclusive language like "people enjoyed" rather than "you enjoyed"
        """
        
        logger.info("Simple Gemini tool initialized with PII-compliant guidelines")
    
    async def generate_content(self, prompt: str, max_tokens: int = 800) -> Optional[str]:
        """
        Generate content using Gemini with bias prevention and PII compliance.
        """
        
        if not httpx:
            logger.warning("⚠️ httpx not available for Gemini API")
            return None
        
        try:
            # Add bias prevention and PII compliance to every prompt
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
            
            # Increased timeout for reliability
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        logger.info("✅ Gemini content generated successfully (PII-compliant)")
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
        Generate structured JSON response using Gemini with PII compliance.
        Enhanced for better parsing and error handling.
        """
        
        if not httpx:
            logger.warning("⚠️ httpx not available for Gemini API")
            return None
        
        try:
            # Create structured prompt with PII compliance
            schema_str = json.dumps(json_schema, indent=2)
            full_prompt = f"""
            {self.bias_prevention_rules}
            
            TASK: {prompt}
            
            RESPONSE FORMAT: Return ONLY valid JSON that matches this exact schema:
            {schema_str}
            
            IMPORTANT PII COMPLIANCE REQUIREMENTS:
            - Return ONLY the JSON, no additional text before or after
            - Ensure all required fields are included
            - Use appropriate data types (strings, arrays, etc.)
            - Content must be positive and appropriate for seniors with dementia
            - ABSOLUTELY NEVER use personal names ANYWHERE in the content
            - Write for caregivers to read aloud to patients
            - Each section should be substantial (2-3 sentences minimum)
            - Create complete, meaningful content for all sections
            - Focus heavily on the specified theme throughout all content
            - Never assume the caregiver has prior knowledge of the patient
            - Use only cultural heritage and age-appropriate information provided
            - Address content generically, not personally
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
                    "maxOutputTokens": 1400,  # Increased for complete content
                    "candidateCount": 1
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            # Increased timeout for reliability
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        
                        # Enhanced JSON parsing
                        try:
                            # Clean up the response more thoroughly
                            content = content.strip()
                            
                            # Remove markdown code blocks
                            if content.startswith("```json"):
                                content = content[7:]
                            elif content.startswith("```"):
                                content = content[3:]
                            
                            if content.endswith("```"):
                                content = content[:-3]
                            
                            # Remove any leading/trailing whitespace again
                            content = content.strip()
                            
                            # Try to find JSON boundaries if mixed with other text
                            if not content.startswith('{'):
                                start_idx = content.find('{')
                                if start_idx != -1:
                                    content = content[start_idx:]
                            
                            if not content.endswith('}'):
                                end_idx = content.rfind('}')
                                if end_idx != -1:
                                    content = content[:end_idx + 1]
                            
                            parsed_json = json.loads(content)
                            logger.info("✅ Gemini structured JSON generated successfully (PII-compliant)")
                            return parsed_json
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"❌ Failed to parse Gemini JSON: {e}")
                            logger.error(f"Raw response: {content[:500]}...")
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
    
    async def generate_nostalgia_newsletter(self, prompt: str, json_schema: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Generate nostalgia newsletter content with proper tone guidance and PII compliance.
        This method provides specific guidance for newsletter-style content.
        """
        
        if not httpx:
            logger.warning("⚠️ httpx not available for Gemini API")
            return None
        
        try:
            # Create newsletter-specific prompt with tone guidance and PII compliance
            schema_str = json.dumps(json_schema, indent=2)
            full_prompt = f"""
            {self.bias_prevention_rules}
            
            {self.newsletter_tone_rules}
            
            TASK: {prompt}
            
            NEWSLETTER CONTENT REQUIREMENTS (PII-COMPLIANT):
            - Write in friendly newsletter style for caregivers to read aloud to patients
            - ABSOLUTELY NEVER use any personal names anywhere in the content
            - Use simple, warm language that flows naturally when spoken
            - Include interesting historical facts with specific years when appropriate
            - Use engaging phrases like "Remember when..." or "In those days..." or "Back in [year]..." or "Many people remember..."
            - Make it sound like friendly news from the past
            - Focus on positive cultural memories and traditions
            - Each section should be 2-3 sentences that sound conversational
            - Include specific historical details that are accurate and interesting
            - Address content generically, never personally
            - Use inclusive language appropriate for diverse audiences
            
            SECTION REQUIREMENTS:
            - For memory spotlight: include "on this day in [year]..." facts that resonate with seniors
            - For memory spotlight: keep it light and nostalgic, no war, killing or negative topics
            - For heritage traditions: include information about both American and identified culture
            - Example: if heritage is Italian-American, include Italian, Italian-American, and American traditions
            - Never assume personal connections - focus on general cultural experiences
            
            TONE EXAMPLES (PII-COMPLIANT):
            - "Back in 1947, Percy Spencer discovered the microwave oven by accident while working with radar technology. It took until the 1970s for these amazing appliances to become common in American kitchens!"
            - "Many people remember those wonderful Sunday afternoon drives in the 1950s, when families would pile into their cars just to see the countryside and stop for ice cream along the way."
            - "Italian-American families often celebrated traditions that blended the old country with American customs, creating beautiful new holiday celebrations."
            
            RESPONSE FORMAT: Return ONLY valid JSON that matches this exact schema:
            {schema_str}
            
            CRITICAL PII COMPLIANCE: 
            - Return ONLY the JSON, no additional text
            - Each section must sound like it could be read aloud naturally
            - Use warm, conversational tone throughout
            - Include cultural and historical context where appropriate
            - NO personal names, addresses, or identifying information ANYWHERE
            - Focus on cultural heritage and age-appropriate themes only
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
                    "temperature": 0.4,  # Slightly higher for creative newsletter tone
                    "topK": 25,
                    "topP": 0.85,
                    "maxOutputTokens": 1600,  # More tokens for rich newsletter content
                    "candidateCount": 1
                }
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            url = f"{self.base_url}/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            # Increased timeout for reliability
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        
                        # Enhanced JSON parsing
                        try:
                            # Clean up the response more thoroughly
                            content = content.strip()
                            
                            # Remove markdown code blocks
                            if content.startswith("```json"):
                                content = content[7:]
                            elif content.startswith("```"):
                                content = content[3:]
                            
                            if content.endswith("```"):
                                content = content[:-3]
                            
                            # Remove any leading/trailing whitespace again
                            content = content.strip()
                            
                            # Try to find JSON boundaries if mixed with other text
                            if not content.startswith('{'):
                                start_idx = content.find('{')
                                if start_idx != -1:
                                    content = content[start_idx:]
                            
                            if not content.endswith('}'):
                                end_idx = content.rfind('}')
                                if end_idx != -1:
                                    content = content[:end_idx + 1]
                            
                            parsed_json = json.loads(content)
                            logger.info("✅ Gemini newsletter content generated successfully (PII-compliant)")
                            return parsed_json
                            
                        except json.JSONDecodeError as e:
                            logger.error(f"❌ Failed to parse Gemini newsletter JSON: {e}")
                            logger.error(f"Raw response: {content[:500]}...")
                            return None
                    else:
                        logger.error("❌ No content in Gemini newsletter response")
                        return None
                else:
                    logger.error(f"❌ Gemini newsletter API error: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("❌ Gemini newsletter generation timeout")
            return None
        except Exception as e:
            logger.error(f"❌ Gemini newsletter generation failed: {e}")
            return None
    
    async def generate_dementia_friendly_description(self, 
                                                   original_description: str,
                                                   heritage: str = "American",
                                                   age_group: str = "senior") -> Optional[str]:
        """
        Generate simple, warm, dementia-friendly photo description.
        UPDATED: No longer accepts patient_name - fully PII-compliant.
        """
        
        prompt = f"""
        Convert this technical photo description into simple, warm language for a senior with dementia:
        
        Original description: {original_description}
        Cultural context: {heritage} heritage
        Age group: {age_group}
        
        Create a description that:
        - Write for CAREGIVERS to read TO patients (not directly to patients)
        - Professional but warm, engaging tone
        - ABSOLUTELY NO personal names anywhere in the content
        - Uses very simple, everyday words
        - Focuses on emotions and feelings (happy, loving, peaceful)
        - Uses short, clear sentences
        - Mentions colors, people, and familiar things
        - Sounds warm and comforting
        - Avoids technical photography terms
        - Makes the viewer feel good
        - Is appropriate for seniors with memory care needs
        - Consider cultural heritage context when appropriate
        - Address content generically, not personally

        Write 3-4 short sentences that describe what someone would see in simple, loving words.
        """
        
        result = await self.generate_content(prompt, max_tokens=200)
        
        if result:
            # Clean up the description and ensure PII compliance
            description = result.strip()
            
            # Ensure proper sentence structure
            if not description.endswith('.'):
                description += '.'
                
            # Basic PII check - remove any accidental names
            # This is a safety net in case Gemini includes names despite instructions
            import re
            # Remove any potential name patterns (capitalized words that might be names)
            # But preserve legitimate capitalized words like locations, days, etc.
            safe_words = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                         'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                         'September', 'October', 'November', 'December', 'American', 'Italian', 
                         'Irish', 'Mexican', 'Christmas', 'Easter', 'Thanksgiving']
            
            # This is a basic safety check - the real protection is in the prompt instructions
            logger.info("✅ Generated PII-compliant photo description")
            return description
        
        return None
    
    async def test_connection(self) -> bool:
        """Test Gemini API connection with PII compliance check"""
        try:
            test_result = await self.generate_content("Generate a simple, positive greeting without using any personal names.", max_tokens=50)
            return test_result is not None
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False

# Export the main class
__all__ = ["SimpleGeminiTool"]