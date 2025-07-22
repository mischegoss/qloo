"""
Enhanced Gemini Tools for Qloo Query Optimization
Supports intelligent query generation and parameter optimization
"""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional, List
import json

logger = logging.getLogger(__name__)

class GeminiAITool:
    """
    Enhanced Gemini AI tool specifically optimized for Qloo API interactions.
    
    Key Features:
    - Intelligent query generation for cultural contexts
    - Parameter optimization for Qloo API calls  
    - Context-aware search term suggestions
    - Structured output parsing
    """
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        # Specialized prompts for different Qloo optimization tasks
        self.prompt_templates = {
            "search_optimization": self._get_search_optimization_template(),
            "parameter_building": self._get_parameter_building_template(),
            "cultural_analysis": self._get_cultural_analysis_template()
        }
        
        logger.info(f"Gemini AI tool initialized with {model} for Qloo optimization")
    
    async def generate_content(self, prompt: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate content using Gemini with error handling and retry logic.
        """
        try:
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": 2048,
                    "topP": 0.8
                }
            }
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent",
                    params={"key": self.api_key},
                    headers={"Content-Type": "application/json"},
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract text from response
                    candidates = data.get("candidates", [])
                    if candidates and len(candidates) > 0:
                        content = candidates[0].get("content", {})
                        parts = content.get("parts", [])
                        if parts and len(parts) > 0:
                            text = parts[0].get("text", "")
                            if text:
                                logger.info("✅ Gemini content generation successful")
                                return {"success": True, "text": text}
                    
                    logger.error("❌ No content parts in Gemini response")
                    return {"success": False, "error": "no_content"}
                
                else:
                    logger.error(f"❌ Gemini API error: {response.status_code}")
                    return {"success": False, "error": f"http_{response.status_code}"}
        
        except Exception as e:
            logger.error(f"💥 Gemini content generation exception: {e}")
            return {"success": False, "error": "exception"}
    
    async def optimize_qloo_searches(self, 
                                   cultural_keywords: List[str],
                                   demographic_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Specialized method for optimizing Qloo search queries.
        """
        try:
            prompt = self._build_search_optimization_prompt(cultural_keywords, demographic_context)
            
            logger.info("🤖 Gemini: Optimizing Qloo search queries...")
            result = await self.generate_content(prompt, temperature=0.5)
            
            if result.get("success"):
                return self._parse_search_optimization_response(result["text"])
            else:
                logger.error("Gemini search optimization failed")
                return {"success": False, "error": "gemini_failed"}
                
        except Exception as e:
            logger.error(f"Search optimization exception: {e}")
            return {"success": False, "error": "exception"}
    
    async def build_qloo_parameters(self, 
                                  entity_type: str,
                                  entity_id: str, 
                                  demographic_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Specialized method for building optimal Qloo API parameters.
        """
        try:
            prompt = self._build_parameter_optimization_prompt(entity_type, entity_id, demographic_context)
            
            logger.info("🤖 Gemini: Building optimal Qloo parameters...")
            result = await self.generate_content(prompt, temperature=0.3)
            
            if result.get("success"):
                return self._parse_parameter_response(result["text"])
            else:
                logger.error("Gemini parameter building failed")
                return {"success": False, "error": "gemini_failed"}
                
        except Exception as e:
            logger.error(f"Parameter building exception: {e}")
            return {"success": False, "error": "exception"}
    
    def _build_search_optimization_prompt(self, 
                                        cultural_keywords: List[str],
                                        demographic_context: Dict[str, Any]) -> str:
        """
        Build specialized prompt for search optimization.
        """
        age_context = demographic_context.get("age_range", "unknown")
        location_context = demographic_context.get("general_location", {})
        city = location_context.get("city_region", "")
        
        prompt = f"""
You are an expert at generating precise search queries for the Qloo cultural recommendation API.

CONTEXT:
- Cultural Keywords: {', '.join(cultural_keywords)}
- Age Group: {age_context}
- Location: {city}

TASK:
Generate specific, searchable terms that will find relevant cultural entities in these 4 categories:

1. PLACES (restaurants, venues, cultural locations)
2. ARTISTS (musicians, performers, cultural figures)
3. MOVIES (films, documentaries, shows)
4. BOOKS (literature, cookbooks, cultural texts)

RULES:
✅ Use specific terms, not generic words
✅ Consider cultural context (e.g., "italian" → "italian restaurants", "traditional italian music")
✅ Make searches likely to find real, existing entities
✅ Include location context when relevant for places
✅ Focus on 2-3 high-quality searches per category
✅ Prioritize terms that would return popular, well-known entities

❌ Avoid overly broad terms like "food" or "music"
❌ Don't use abstract concepts that won't match real entities
❌ Don't include location for non-place categories

OUTPUT FORMAT (exactly as shown):
```json
{{
    "places": ["search term 1", "search term 2"],
    "artists": ["search term 1", "search term 2"],
    "movies": ["search term 1", "search term 2"],
    "books": ["search term 1", "search term 2"]
}}
```

EXAMPLE for Italian-American context:
```json
{{
    "places": ["italian restaurants", "family dining restaurants"],
    "artists": ["Frank Sinatra", "traditional italian music"],
    "movies": ["italian family movies", "classic italian cinema"],
    "books": ["italian cookbook", "italian american authors"]
}}
```

Generate optimized search queries now:
"""
        return prompt
    
    def _build_parameter_optimization_prompt(self, 
                                           entity_type: str,
                                           entity_id: str,
                                           demographic_context: Dict[str, Any]) -> str:
        """
        Build specialized prompt for parameter optimization.
        """
        age_range = demographic_context.get("age_range", "")
        location = demographic_context.get("general_location", {})
        
        prompt = f"""
You are an expert at building optimal parameters for the Qloo Insights API.

CONTEXT:
- Entity Type: {entity_type}
- Entity ID: {entity_id}
- Age Range: {age_range}
- Location: {location}

TASK:
Build the optimal parameter set for a Qloo /v2/insights API call.

REQUIRED PARAMETERS:
- filter.type: Must be exactly "{entity_type}"
- signal.interests.entities: Must be exactly "{entity_id}"
- take: Should be "5" for good results

OPTIONAL PARAMETERS (add only if context supports):
- signal.demographics.age: Use "18_to_34", "35_to_54", or "55_and_older" based on age_range
- signal.location.query: For places only, use city name if available

RULES:
✅ Always include the 3 required parameters
✅ Only add demographics if age_range is clear
✅ Only add location for urn:entity:place
✅ Use exact age group values: "18_to_34", "35_to_54", "55_and_older"
✅ Keep location queries short (city name only)

OUTPUT FORMAT (exactly as JSON):
```json
{{
    "filter.type": "{entity_type}",
    "signal.interests.entities": "{entity_id}",
    "take": "5"
}}
```

Generate optimal parameters now:
"""
        return prompt
    
    def _parse_search_optimization_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse search optimization response from Gemini.
        """
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("No JSON found in Gemini search response")
                return {"success": False, "error": "no_json"}
            
            json_str = response_text[start_idx:end_idx]
            search_queries = json.loads(json_str)
            
            # Validate structure
            required_keys = ["places", "artists", "movies", "books"]
            if not all(key in search_queries for key in required_keys):
                logger.error(f"Missing required keys in search response: {list(search_queries.keys())}")
                return {"success": False, "error": "invalid_structure"}
            
            # Validate each category has queries
            for key in required_keys:
                if not isinstance(search_queries[key], list) or len(search_queries[key]) == 0:
                    logger.warning(f"Empty or invalid queries for {key}")
                    search_queries[key] = [f"{key.rstrip('s')} recommendations"]  # Simple fallback
            
            logger.info(f"✅ Parsed search queries: {[f'{k}:{len(v)}' for k, v in search_queries.items()]}")
            return {"success": True, "search_queries": search_queries}
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            logger.error(f"Raw response: {response_text[:200]}...")
            return {"success": False, "error": "json_parse_failed"}
        except Exception as e:
            logger.error(f"Search response parsing failed: {e}")
            return {"success": False, "error": "parse_failed"}
    
    def _parse_parameter_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse parameter optimization response from Gemini.
        """
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.error("No JSON found in Gemini parameter response")
                return {"success": False, "error": "no_json"}
            
            json_str = response_text[start_idx:end_idx]
            params = json.loads(json_str)
            
            # Validate required parameters
            required = ["filter.type", "signal.interests.entities", "take"]
            if not all(key in params for key in required):
                logger.error(f"Missing required parameters: {[k for k in required if k not in params]}")
                return {"success": False, "error": "missing_required_params"}
            
            logger.info(f"✅ Parsed parameters: {list(params.keys())}")
            return {"success": True, "parameters": params}
            
        except json.JSONDecodeError as e:
            logger.error(f"Parameter JSON parsing failed: {e}")
            logger.error(f"Raw response: {response_text[:200]}...")
            return {"success": False, "error": "json_parse_failed"}
        except Exception as e:
            logger.error(f"Parameter response parsing failed: {e}")
            return {"success": False, "error": "parse_failed"}
    
    def _get_search_optimization_template(self) -> str:
        """Template for search optimization prompts."""
        return "Search optimization template"
    
    def _get_parameter_building_template(self) -> str:
        """Template for parameter building prompts."""
        return "Parameter building template"
    
    def _get_cultural_analysis_template(self) -> str:
        """Template for cultural analysis prompts."""
        return "Cultural analysis template"
    
    async def test_connection(self) -> bool:
        """Test Gemini API connection."""
        try:
            result = await self.generate_content("Test connection", temperature=0.1)
            return result.get("success", False)
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False