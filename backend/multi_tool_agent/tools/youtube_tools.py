"""
YouTube API Tools
File: backend/multi_tool_agent/tools/youtube_tools.py

Provides interface to YouTube Data API for music and video content discovery
"""

import httpx
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    YouTube Data API tool for music and video content discovery.
    Used by Agent 4: Sensory Content Generator Agent
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    async def search_music(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """
        Search YouTube for music content.
        
        Args:
            query: Search query (e.g., "Frank Sinatra best songs classic")
            max_results: Maximum number of results to return
            
        Returns:
            YouTube search results or None if failed
        """
        
        try:
            params = {
                "part": "snippet",
                "q": f"{query} music",
                "type": "video",
                "maxResults": max_results,
                "order": "relevance",
                "videoCategoryId": "10",  # Music category
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"YouTube music search success: {len(data.get('items', []))} results for '{query}'")
                    return data
                elif response.status_code == 403:
                    logger.error("YouTube API quota exceeded or permission denied")
                    return None
                else:
                    logger.error(f"YouTube music search error: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("YouTube music search timeout")
            return None
        except Exception as e:
            logger.error(f"YouTube music search exception: {str(e)}")
            return None
    
    async def search_videos(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """
        Search YouTube for video content.
        
        Args:
            query: Search query (e.g., "Ed Sullivan Show 1960s classic")
            max_results: Maximum number of results to return
            
        Returns:
            YouTube search results or None if failed
        """
        
        try:
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "order": "relevance",
                "safeSearch": "strict",  # Family-friendly content
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"YouTube video search success: {len(data.get('items', []))} results for '{query}'")
                    return data
                elif response.status_code == 403:
                    logger.error("YouTube API quota exceeded or permission denied")
                    return None
                else:
                    logger.error(f"YouTube video search error: {response.status_code} - {response.text}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error("YouTube video search timeout")
            return None
        except Exception as e:
            logger.error(f"YouTube video search exception: {str(e)}")
            return None
    
    async def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video details or None if failed
        """
        
        try:
            params = {
                "part": "snippet,contentDetails,statistics",
                "id": video_id,
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/videos",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"YouTube video details success for video {video_id}")
                    return data
                else:
                    logger.error(f"YouTube video details error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"YouTube video details exception: {str(e)}")
            return None
    
    async def search_era_content(self, era: str, content_type: str = "music", max_results: int = 3) -> Optional[Dict[str, Any]]:
        """
        Search for content from a specific era.
        
        Args:
            era: Era descriptor (e.g., "1940s", "1950s", "1960s")
            content_type: Type of content ("music", "variety", "entertainment")
            max_results: Maximum number of results
            
        Returns:
            Era-specific search results or None if failed
        """
        
        era_queries = {
            "music": f"{era} classic music hits nostalgic songs",
            "variety": f"{era} variety show entertainment classic TV",
            "entertainment": f"{era} classic entertainment shows nostalgic"
        }
        
        query = era_queries.get(content_type, f"{era} {content_type}")
        
        if content_type == "music":
            return await self.search_music(query, max_results)
        else:
            return await self.search_videos(query, max_results)
    
    async def test_connection(self) -> bool:
        """
        Test connection to YouTube Data API.
        
        Returns:
            True if connection successful, False otherwise
        """
        
        try:
            # Simple test search
            result = await self.search_music("test", max_results=1)
            
            if result and "items" in result:
                logger.info("YouTube API connection test successful")
                return True
            else:
                logger.error("YouTube API connection test failed")
                return False
                
        except Exception as e:
            logger.error(f"YouTube API connection test exception: {str(e)}")
            return False