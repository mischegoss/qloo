"""
Qloo API Tools
File: backend/multi_tool_agent/tools/qloo_tools.py

Provides interface to Qloo Taste AI™ API for cultural intelligence
"""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    Qloo Insights API tool for cultural intelligence recommendations.
    Used by Agent 3: Qloo Cultural Intelligence Agent
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://hackathon.api.qloo.com"
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
    async def get_insights(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get cultural intelligence insights from Qloo API.
        
        Args:
            params: Query parameters for Qloo insights endpoint
                   Example: {
                       "filter.type": "urn:entity:artist",
                       "signal.demographics.age": "55_and_older",
                       "take": "5"
                   }
            
        Returns:
            Qloo API response with cultural recommendations or None if failed
        """
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Qloo insights API success: {len(data.get('results', {}).get('entities', []))} entities returned")
                    return data
                elif response.status_code == 401:
                    logger.error("Qloo API authentication failed - check API key")
                    return None
                elif response.status_code == 403:
                    logger.error("Qloo API access forbidden - check permissions")
                    return None
                else:
                    logger.error(f"Qloo insights API error: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("Qloo insights API timeout")
            return None
        except Exception as e:
            logger.error(f"Qloo insights API exception: {str(e)}")
            return None
    
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
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"Qloo search API success: {len(data.get('results', []))} results for '{query}'")
                    return data
                else:
                    logger.error(f"Qloo search API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Qloo search API exception: {str(e)}")
            return None
    
    async def test_connection(self) -> bool:
        """
        Test connection to Qloo API.
        
        Returns:
            True if connection successful, False otherwise
        """
        
        try:
            # Simple test query
            test_params = {
                "filter.type": "urn:entity:artist",
                "take": "1"
            }
            
            result = await self.get_insights(test_params)
            
            if result and result.get("success"):
                logger.info("Qloo API connection test successful")
                return True
            else:
                logger.error("Qloo API connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"Qloo API connection test exception: {str(e)}")
            return False