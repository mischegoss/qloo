"""
Simple Gemini Tools - FIXED: PII-Compliant newsletter tone guidance
File: backend/multi_tool_agent/tools/simple_gemini_tools.py

CRITICAL FIX:
- Enhanced generate_nostalgia_newsletter method with PII compliance
- Ensures newsletter-style content that's appropriate for caregivers to read aloud
- Clear guidelines for dementia care content without personal information
- Returns FLAT content structure that frontend expects
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
    
    FIXED: Added PII-compliant newsletter tone guidance for nostalgia content.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Bias prevention for dementia care with PII compliance
        self.bias_prevention_rules = """
        CRITICAL DEMENTIA CARE GUIDELINES:
        - Use positive, uplifting language only
        - Focus on happy memories and pleasant experiences
        - Avoid mentioning death, loss, confusion, or negative topics
        - Use simple, clear language appropriate for seniors
        - Include culturally respectful content only
        - Generate safe, family-friendly content
        - NEVER use personal names anywhere in the content including Friend
        - NEVER use Friend in place of a name like, "Friend, do you know about?"
        - Write for caregivers to read TO patients, not directly to patients
        - Use professional but warm tone
        - Create structured, easy-to-read content
        - Never assume the caregiver has prior knowledge of the patient or shared heritage
        - Content must work for any patient regardless of their personal details
        """
        
        # Newsletter-specific tone guidelines with PII compliance
        self.newsletter_tone_rules = """
        NEWSLETTER TONE GUIDELINES (PII-COMPLIANT):
        - Write in newsletter style with engaging, friendly tone
        - Use simple, warm language that's easy to read aloud
        - Write for CAREGIVERS to read TO patients
        - ABSOLUTELY NEVER use patient names anywhere in the content
        - ABSOLUTELY NEVER use Friend in place of a patient name in the content
        - NEVER use personal pronouns like "you" or "your" - use general terms
        - Include interesting historical facts and gentle nostalgia
        - Use phrases like "Remember when..." or "In those days..." or "Back in the 1950s..."
        - Make it sound like friendly news from the past
        - Include specific years and historical details when appropriate
        - Example tone: "Remember those wonderful Sunday drives? Back in the 1950s, families would pile into their cars just to see the countryside and stop for ice cream along the way."
        - Keep sentences conversational but informative
        - Focus on positive cultural memories and traditions
        - Create content that any caregiver could read to any patient
        - Avoid assumptions about the listener's personal experiences
        """
        
        logger.info("Simple Gemini tool initialized with PII-compliant newsletter tone guidance")
    
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
            
            CRITICAL PII COMPLIANCE:
            - Return ONLY the JSON, no additional text before or after
            - Ensure all required fields are included
            - Use appropriate data types (strings, arrays, etc.)
            - Content must be positive and appropriate for seniors with dementia
            - ABSOLUTELY NEVER use personal names anywhere in the content
            - ABSOLUTELY NEVER use Friend in place of a personal name anywhere in the content
            - Write for caregivers to read aloud to patients
            - Each section should be substantial (2-3 sentences minimum)
            - Create complete, meaningful content for all sections
            - Focus heavily on the specified theme throughout all content
            - Never assume the caregiver has prior knowledge of the patient or shared heritage
            - Use only general, universally applicable language
            - Content should work for any patient regardless of their background
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
                            logger.info("✅ Gemini structured JSON generated successfully")
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
        Generate nostalgia newsletter content with PII-compliant tone guidance.
        This method provides specific guidance for newsletter-style content.
        
        CRITICAL: Returns FLAT content structure that frontend expects.
        """
        
        if not httpx:
            logger.warning("⚠️ httpx not available for Gemini API")
            return None
        
        try:
            # Create newsletter-specific prompt with PII-compliant tone guidance
            schema_str = json.dumps(json_schema, indent=2)
            full_prompt = f"""
            {self.bias_prevention_rules}
            
            {self.newsletter_tone_rules}
            
            TASK: {prompt}
            
            NEWSLETTER CONTENT REQUIREMENTS (PII-COMPLIANT):
            - Write in friendly newsletter style for caregivers to read aloud to patients
            - ABSOLUTELY NEVER use patient names anywhere in the content
            - ABSOLUTELY NEVER use Friend as a substitute for patient names anywhere in the content
            - NEVER use personal pronouns like "you" or "your" - use general terms
            - Use simple, warm language that flows naturally when spoken
            - Include interesting historical facts with specific years when appropriate
            - Use engaging phrases like "Remember when..." or "In those days..." or "Back in [year]..."
            - Make it sound like friendly news from the past
            - Focus on positive cultural memories and traditions
            - Each section should be 2-3 sentences that sound conversational
            - Include specific historical details that are accurate and interesting
            - Create content that any caregiver could read to any patient
            - Avoid assumptions about the listener's personal experiences
            
            SECTION REQUIREMENTS:
            - For memory spotlight: include historical facts that would resonate with seniors (no war, killing, or negative topics)
            - For era highlights: focus on positive cultural moments from the 1940s-1960s
            - For heritage traditions: include information about both American and the identified culture
            - For conversation starters: create open-ended questions that don't assume personal experiences
            
            FLAT CONTENT STRUCTURE CRITICAL:
            - Each section should return a simple STRING, not nested objects
            - Do NOT create nested content structures
            - The frontend expects flat string content for each section
            
            TONE EXAMPLES:
            - "Back in 1947, Percy Spencer discovered the microwave oven by accident while working with radar technology. It took until the 1970s for these amazing appliances to become common in American kitchens!"
            - "Remember those wonderful Sunday afternoon drives? In the 1950s, families would pile into their cars just to see the countryside and stop for ice cream along the way."
            
            RESPONSE FORMAT: Return ONLY valid JSON that matches this exact schema:
            {schema_str}
            
            CRITICAL: 
            - Return ONLY the JSON, no additional text
            - Each section must be a FLAT STRING (not nested objects)
            - Content should sound natural when read aloud
            - Use warm, conversational tone throughout
            - Include cultural and historical context where appropriate
            - NEVER use personal names or specific personal references
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
                            
                            # Validate that we have flat content structure
                            for key, value in parsed_json.items():
                                if key != "conversation_starters" and isinstance(value, dict):
                                    logger.warning(f"⚠️ Section {key} has nested structure, should be flat string")
                                    return None
                            
                            logger.info("✅ Gemini newsletter content generated successfully with flat structure")
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
                                                   heritage: str = "American") -> Optional[str]:
        """
        Generate simple, warm, dementia-friendly photo description (PII-COMPLIANT).
        """
        
        prompt = f"""
        Convert this technical photo description into simple, warm language for a senior with dementia:
        
        Original description: {original_description}
        
        Create a description that:
        - Write for CAREGIVERS to read TO patients (not directly to patients)
        - Professional but warm, engaging tone
        - NO personal names anywhere in the content
        - NEVER use "you" or "your" - use general terms like "someone" or "people"
        - Uses very simple, everyday words
        - Focuses on emotions and feelings (happy, loving, peaceful)
        - Uses short, clear sentences
        - Mentions colors, people, and familiar things
        - Sounds warm and comforting
        - Avoids technical photography terms
        - Makes the listener feel good
        - Is appropriate for seniors with memory care needs
        - Creates content that any caregiver could read to any patient
        - DO NOT include any prefacing text like "Here's a description..." or "This is a description..."
        - Return ONLY the description itself, nothing else

        Write 3-4 short sentences that describe what someone would see in simple, loving words. Return ONLY the description with no prefacing text.
        """
        
        result = await self.generate_content(prompt, max_tokens=200)
        
        if result:
            # Clean up the description and ensure PII compliance
            description = result.strip()
            # Remove any potential personal references
            description = description.replace("you", "someone").replace("your", "their")
            # Remove any unwanted prefacing text that might slip through
            description = description.replace("Here's a description", "").replace("This is a description", "")
            description = description.replace("Here is a description", "").replace("Below is a description", "")
            # Clean up any remaining artifacts
            description = description.strip(' :"')
            # Ensure proper sentence structure
            if not description.endswith('.'):
                description += '.'
            return description
        
        return None
    
    async def test_connection(self) -> bool:
        """Test Gemini API connection"""
        try:
            test_result = await self.generate_content("Hello, this is a test.", max_tokens=50)
            return test_result is not None
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False

# Export the main class
__all__ = ["SimpleGeminiTool"]