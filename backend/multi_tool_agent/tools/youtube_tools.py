"""
YouTube API Tools with Daily Caching - SIMPLIFIED RATE LIMITING + EMBEDDABLE URLS
File: backend/multi_tool_agent/tools/youtube_tools.py

FIXES:
- Daily caching using in-memory dictionary
- Cache keys based on daily seed + search term
- Immediate cache returns to avoid API calls
- EMBEDDABLE URLs: videoEmbeddable=true and embed format transformation
- SIMPLIFIED: Removed complex 403 error tracking (overkill for minimal usage)
"""

import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import date
import hashlib

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    YouTube Data API tool with daily caching and embeddable URL support.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        # DAILY CACHE - Reset each day automatically
        self._daily_cache = {}
        self._cache_date = None
        
        logger.info("YouTube API tool initialized with daily caching + embeddable URLs")
    
    def _get_daily_seed(self) -> str:
        """Get daily seed for cache consistency."""
        today = date.today()
        return f"{today.year}-{today.month}-{today.day}"
    
    def _get_cache_key(self, search_type: str, query: str) -> str:
        """Generate cache key for daily consistency."""
        daily_seed = self._get_daily_seed()
        # Create short hash to avoid key length issues
        query_hash = hashlib.md5(query.lower().encode()).hexdigest()[:8]
        return f"{daily_seed}_{search_type}_{query_hash}"
    
    def _check_and_update_daily_cache(self):
        """Reset cache if new day."""
        today = date.today()
        if self._cache_date != today:
            logger.info("New day detected - clearing YouTube cache")
            self._daily_cache = {}
            self._cache_date = today
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from daily cache."""
        self._check_and_update_daily_cache()
        result = self._daily_cache.get(cache_key)
        if result:
            logger.info(f"YouTube cache HIT: {cache_key}")
            return result
        return None
    
    def _store_in_cache(self, cache_key: str, result: Dict[str, Any]):
        """Store result in daily cache."""
        self._check_and_update_daily_cache()
        self._daily_cache[cache_key] = result
        logger.info(f"YouTube cache STORED: {cache_key}")
    
    def _create_embeddable_url(self, video_id: str) -> str:
        """Create embeddable YouTube URL from video ID."""
        if not video_id:
            return ""
        return f"https://www.youtube.com/embed/{video_id}"
    
    async def search_music(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """
        Search YouTube for music content with daily caching and embeddable URLs.
        """
        
        # Check cache first
        cache_key = self._get_cache_key("music", query)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        try:
            logger.info(f"YouTube music search (LIVE API): {query}")
            
            params = {
                "part": "snippet",
                "q": f"{query} music",
                "type": "video",
                "maxResults": max_results,
                "order": "relevance",
                "videoCategoryId": "10",  # Music category
                "videoEmbeddable": "true",  # Only embeddable videos
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
                    
                    # Transform video IDs to embeddable URLs
                    for item in data.get('items', []):
                        video_id = item.get('id', {}).get('videoId')
                        if video_id:
                            item['embeddable_url'] = self._create_embeddable_url(video_id)
                    
                    # Store in cache before returning
                    self._store_in_cache(cache_key, data)
                    return data
                    
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
        Search YouTube for video content with daily caching and embeddable URLs.
        """
        
        # Check cache first
        cache_key = self._get_cache_key("videos", query)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        try:
            logger.info(f"YouTube video search (LIVE API): {query}")
            
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "order": "relevance",
                "safeSearch": "strict",  # Family-friendly content
                "videoEmbeddable": "true",  # Only embeddable videos
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
                    
                    # Transform video IDs to embeddable URLs
                    for item in data.get('items', []):
                        video_id = item.get('id', {}).get('videoId')
                        if video_id:
                            item['embeddable_url'] = self._create_embeddable_url(video_id)
                    
                    # Store in cache before returning
                    self._store_in_cache(cache_key, data)
                    return data
                    
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
        Get detailed information about a specific video with caching.
        """
        
        # Check cache first
        cache_key = self._get_cache_key("details", video_id)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result
        
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
                    
                    # Add embeddable URL
                    for item in data.get('items', []):
                        item['embeddable_url'] = self._create_embeddable_url(video_id)
                    
                    # Store in cache before returning
                    self._store_in_cache(cache_key, data)
                    return data
                else:
                    logger.error(f"YouTube video details error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"YouTube video details exception: {str(e)}")
            return None
    
    async def search_era_content(self, era: str, content_type: str = "music", max_results: int = 3) -> Optional[Dict[str, Any]]:
        """
        Search for content from a specific era with caching.
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
        """
        
        try:
            # Simple test search with minimal results
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
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for debugging."""
        self._check_and_update_daily_cache()
        return {
            "cache_size": len(self._daily_cache),
            "cache_date": str(self._cache_date),
            "daily_seed": self._get_daily_seed(),
            "cached_keys": list(self._daily_cache.keys())
        }

# Export the main class
__all__ = ["YouTubeAPI"]