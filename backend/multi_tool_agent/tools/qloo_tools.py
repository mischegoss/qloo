"""
Qloo API Tools - Complete Revised Version
File: backend/multi_tool_agent/tools/qloo_tools.py

Provides interface to Qloo Taste AI™ API for cultural intelligence
"""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    Qloo Insights API tool for cultural intelligence recommendations.
    Used by Agent 3: Qloo Cultural Intelligence Agent
    
    Provides access to Qloo's Taste AI™ for cross-domain cultural recommendations
    following responsible development principles.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Qloo API tool.
        
        Args:
            api_key: Qloo API key from hackathon registration
        """
        self.api_key = api_key
        self.base_url = "https://hackathon.api.qloo.com"
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        logger.info("Qloo API tool initialized")
        
    async def get_insights(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get cultural intelligence insights from Qloo API.
        
        Args:
            params: Query parameters for Qloo insights endpoint
                   Example: {
                       "filter.type": "urn:entity:artist",
                       "signal.demographics.age": "55_and_older",
                       "signal.interests.tags": "jazz music",
                       "take": 5
                   }
            
        Returns:
            Qloo API response with cultural recommendations or None if failed
        """
        
        try:
            logger.info(f"Qloo API request with params: {params}")
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entities_count = len(data.get('results', {}).get('entities', []))
                    logger.info(f"Qloo insights API success: {entities_count} entities returned")
                    return {"success": True, "results": data}
                
                elif response.status_code == 400:
                    error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                    logger.error(f"Qloo API bad request (400): {error_data}")
                    return {"success": False, "error": "bad_request", "details": error_data}
                
                elif response.status_code == 401:
                    logger.error("Qloo API authentication failed (401) - check API key")
                    return {"success": False, "error": "authentication_failed"}
                
                elif response.status_code == 403:
                    logger.error("Qloo API access forbidden (403) - check permissions")
                    return {"success": False, "error": "access_forbidden"}
                
                elif response.status_code == 429:
                    logger.error("Qloo API rate limit exceeded (429)")
                    return {"success": False, "error": "rate_limit_exceeded"}
                
                else:
                    logger.error(f"Qloo insights API error: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"http_{response.status_code}"}
                    
        except httpx.TimeoutException:
            logger.error("Qloo insights API timeout")
            return {"success": False, "error": "timeout"}
        except httpx.ConnectError:
            logger.error("Qloo insights API connection error")
            return {"success": False, "error": "connection_error"}
        except Exception as e:
            logger.error(f"Qloo insights API exception: {str(e)}")
            return {"success": False, "error": "exception", "details": str(e)}
    
    async def search(self, query: str, limit: int = 5) -> Optional[Dict[str, Any]]:
        """
        Search Qloo API for cultural content.
        
        Args:
            query: Search query string
            limit: Number of results to return
            
        Returns:
            Search results or None if failed
        """
        
        try:
            params = {
                "query": query,
                "limit": limit
            }
            
            logger.info(f"Qloo search request: '{query}' (limit: {limit})")
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results_count = len(data.get('results', []))
                    logger.info(f"Qloo search API success: {results_count} results for '{query}'")
                    return {"success": True, "results": data}
                else:
                    logger.error(f"Qloo search API error: {response.status_code} - {response.text}")
                    return {"success": False, "error": f"http_{response.status_code}"}
                    
        except Exception as e:
            logger.error(f"Qloo search API exception: {str(e)}")
            return {"success": False, "error": "exception", "details": str(e)}
    
    async def get_cultural_recommendations(self, 
                                         entity_type: str,
                                         cultural_signals: Dict[str, Any],
                                         demographic_signals: Dict[str, Any],
                                         take: int = 5) -> Optional[Dict[str, Any]]:
        """
        Get cultural recommendations for a specific entity type.
        
        Args:
            entity_type: Qloo entity type (e.g., "urn:entity:artist", "urn:entity:place")
            cultural_signals: Cultural context signals
            demographic_signals: Demographic context signals
            take: Number of results to return
            
        Returns:
            Cultural recommendations or None if failed
        """
        
        # Build parameters based on entity type and signals
        params = {
            "filter.type": entity_type,
            "take": take
        }
        
        # Add demographic signals
        age_range = demographic_signals.get("age_range")
        if age_range:
            if "senior" in age_range:
                params["signal.demographics.age"] = "55_and_older"
            elif "adult" in age_range:
                params["signal.demographics.age"] = "35_to_54"
            elif "young" in age_range:
                params["signal.demographics.age"] = "18_to_34"
        
        # Add cultural interest signals
        interests = cultural_signals.get("interests", [])
        if interests:
            # Use the first interest as a tag signal
            params["signal.interests.tags"] = interests[0]
        else:
            # Default interest signal to ensure API requirements are met
            if "artist" in entity_type:
                params["signal.interests.tags"] = "music"
            elif "place" in entity_type:
                params["signal.interests.tags"] = "restaurants"
            elif "movie" in entity_type:
                params["signal.interests.tags"] = "entertainment"
            else:
                params["signal.interests.tags"] = "culture"
        
        # Add location signal if available
        location = demographic_signals.get("location")
        if location and "place" in entity_type:
            params["signal.location.query"] = location
        
        logger.info(f"Getting cultural recommendations for {entity_type}")
        return await self.get_insights(params)
    
    async def test_connection(self) -> bool:
        """
        Test connection to Qloo API with proper required parameters.
        
        Returns:
            True if connection successful, False otherwise
        """
        
        try:
            logger.info("Testing Qloo API connection...")
            
            # Fixed test query with all required signals according to API docs
            test_params = {
                "filter.type": "urn:entity:artist",
                "signal.demographics.age": "55_and_older",
                "signal.interests.tags": "music",  # Required interest signal
                "take": 1
            }
            
            result = await self.get_insights(test_params)
            
            if result and result.get("success"):
                logger.info("Qloo API connection test successful")
                return True
            else:
                error_details = result.get("details", "Unknown error") if result else "No response"
                logger.error(f"Qloo API connection test failed: {error_details}")
                return False
                
        except Exception as e:
            logger.error(f"Qloo API connection test exception: {str(e)}")
            return False
    
    async def get_entity_recommendations(self, 
                                       entity_types: List[str],
                                       signals: Dict[str, Any],
                                       take_per_type: int = 3) -> Dict[str, Any]:
        """
        Get recommendations for multiple entity types in parallel.
        
        Args:
            entity_types: List of Qloo entity types to query
            signals: Combined signals for all queries
            take_per_type: Number of results per entity type
            
        Returns:
            Dictionary with results for each entity type
        """
        
        results = {}
        tasks = []
        
        # Create tasks for parallel execution
        for entity_type in entity_types:
            params = {
                "filter.type": entity_type,
                "take": take_per_type,
                **signals
            }
            
            # Ensure required signals are present for each entity type
            if "signal.interests.tags" not in params:
                if "artist" in entity_type:
                    params["signal.interests.tags"] = "music"
                elif "place" in entity_type:
                    params["signal.interests.tags"] = "dining"
                elif "movie" in entity_type:
                    params["signal.interests.tags"] = "movies"
                else:
                    params["signal.interests.tags"] = "culture"
            
            task = self.get_insights(params)
            tasks.append((entity_type, task))
        
        # Execute all tasks in parallel with rate limiting
        for entity_type, task in tasks:
            try:
                result = await task
                results[entity_type] = result
                
                # Rate limiting - small delay between requests
                await asyncio.sleep(0.2)
                
            except Exception as e:
                logger.error(f"Error getting recommendations for {entity_type}: {str(e)}")
                results[entity_type] = {"success": False, "error": str(e)}
        
        return results
    
    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate Qloo API parameters according to API requirements.
        
        Args:
            params: Parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        
        # Check required filter.type
        if "filter.type" not in params:
            return False, "filter.type is required"
        
        entity_type = params["filter.type"]
        
        # Check if at least one signal is provided
        has_signal = any(key.startswith("signal.") for key in params.keys())
        if not has_signal:
            return False, "At least one signal parameter is required"
        
        # Entity-specific validation
        if "artist" in entity_type or "album" in entity_type:
            # Music entities should have music-related signals
            if not any(tag in params.get("signal.interests.tags", "") 
                      for tag in ["music", "jazz", "rock", "classical", "pop"]):
                logger.warning("Music entity without music interest tag")
        
        return True, "Valid parameters"