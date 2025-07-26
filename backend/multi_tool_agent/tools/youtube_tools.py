"""
YouTube API Tools - FIXED to Prevent Excessive API Calls
File: backend/multi_tool_agent/tools/youtube_tools.py

CRITICAL FIXES:
- Fixed cache reset bug across midnight
- Longer hash keys to prevent collisions  
- Mock test_connection to avoid real API calls
- Cache API failures to prevent retries
- Better cache persistence strategy
"""

import httpx
import logging
from typing import Dict, Any, Optional, List
from datetime import date
import hashlib
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    YouTube Data API tool with FIXED caching to prevent excessive API calls.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        # FIXED: Persistent cache file + in-memory cache
        self.cache_dir = Path(__file__).parent.parent.parent / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "youtube_cache.json"
        
        # Load persistent cache
        self._daily_cache = self._load_persistent_cache()
        self._cache_date = date.today()
        
        logger.info("YouTube API tool initialized with FIXED caching (prevents excessive calls)")
    
    def _load_persistent_cache(self) -> Dict[str, Any]:
        """Load cache from file to survive app restarts."""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    
                # Check if cache is from today
                cache_date = cache_data.get("date")
                if cache_date == date.today().isoformat():
                    logger.info(f"Loaded {len(cache_data.get('cache', {}))} YouTube cache entries from file")
                    return cache_data.get("cache", {})
                else:
                    logger.info("YouTube cache expired (different day), starting fresh")
                    
        except Exception as e:
            logger.warning(f"Could not load YouTube cache: {e}")
        
        return {}
    
    def _save_persistent_cache(self):
        """Save cache to file for persistence."""
        try:
            cache_data = {
                "date": date.today().isoformat(),
                "cache": self._daily_cache
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f)
                
        except Exception as e:
            logger.warning(f"Could not save YouTube cache: {e}")
    
    def _get_daily_seed(self) -> str:
        """Get daily seed for cache consistency."""
        today = date.today()
        return f"{today.year}-{today.month}-{today.day}"
    
    def _get_cache_key(self, search_type: str, query: str) -> str:
        """Generate cache key - FIXED to prevent collisions."""
        daily_seed = self._get_daily_seed()
        # FIXED: Use longer hash to prevent collisions (16 chars instead of 8)
        query_hash = hashlib.md5(query.lower().encode()).hexdigest()[:16]
        return f"{daily_seed}_{search_type}_{query_hash}"
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from cache - FIXED to not reset cache unnecessarily."""
        # FIXED: Don't reset cache on every access
        result = self._daily_cache.get(cache_key)
        if result:
            logger.info(f"YouTube cache HIT: {cache_key}")
            return result
        return None
    
    def _store_in_cache(self, cache_key: str, result: Dict[str, Any]):
        """Store result in cache - FIXED with persistence."""
        self._daily_cache[cache_key] = result
        logger.info(f"YouTube cache STORED: {cache_key}")
        
        # Save to file every 10 cache entries to balance performance/persistence
        if len(self._daily_cache) % 10 == 0:
            self._save_persistent_cache()
    
    def _cache_api_failure(self, cache_key: str, error_info: str):
        """FIXED: Cache API failures to prevent immediate retries."""
        failure_result = {
            "error": True,
            "error_info": error_info,
            "timestamp": date.today().isoformat()
        }
        self._daily_cache[cache_key] = failure_result
        logger.info(f"YouTube FAILURE cached: {cache_key}")
    
    def _create_embeddable_url(self, video_id: str) -> str:
        """Create embeddable YouTube URL from video ID."""
        if not video_id:
            return ""
        return f"https://www.youtube.com/embed/{video_id}"
    
    async def search_music(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """
        Search YouTube for music content with FIXED caching.
        """
        
        # Check cache first
        cache_key = self._get_cache_key("music", query)
        cached_result = self._get_from_cache(cache_key)
        
        if cached_result:
            # FIXED: Check if it's a cached failure
            if cached_result.get("error"):
                logger.info(f"YouTube cache HIT (previous failure): {cache_key}")
                return None
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
                    error_msg = f"Status {response.status_code}"
                    logger.error(f"YouTube music search error: {error_msg}")
                    # FIXED: Cache the failure
                    self._cache_api_failure(cache_key, error_msg)
                    return None
                    
        except httpx.TimeoutException:
            logger.error("YouTube music search timeout")
            self._cache_api_failure(cache_key, "timeout")
            return None
        except Exception as e:
            error_msg = str(e)
            logger.error(f"YouTube music search exception: {error_msg}")
            self._cache_api_failure(cache_key, error_msg)
            return None
    
    async def search_videos(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """
        Search YouTube for video content with FIXED caching.
        """
        
        # Check cache first
        cache_key = self._get_cache_key("videos", query)
        cached_result = self._get_from_cache(cache_key)
        
        if cached_result:
            if cached_result.get("error"):
                logger.info(f"YouTube cache HIT (previous failure): {cache_key}")
                return None
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
                    error_msg = f"Status {response.status_code}"
                    logger.error(f"YouTube video search error: {error_msg}")
                    self._cache_api_failure(cache_key, error_msg)
                    return None
                    
        except httpx.TimeoutException:
            logger.error("YouTube video search timeout")
            self._cache_api_failure(cache_key, "timeout")
            return None
        except Exception as e:
            error_msg = str(e)
            logger.error(f"YouTube video search exception: {error_msg}")
            self._cache_api_failure(cache_key, error_msg)
            return None
    
    async def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific video with FIXED caching.
        """
        
        # Check cache first
        cache_key = self._get_cache_key("details", video_id)
        cached_result = self._get_from_cache(cache_key)
        
        if cached_result:
            if cached_result.get("error"):
                return None
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
                    error_msg = f"Status {response.status_code}"
                    logger.error(f"YouTube video details error: {error_msg}")
                    self._cache_api_failure(cache_key, error_msg)
                    return None
                    
        except Exception as e:
            error_msg = str(e)
            logger.error(f"YouTube video details exception: {error_msg}")
            self._cache_api_failure(cache_key, error_msg)
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
        FIXED: Mock test connection to avoid real API calls.
        """
        
        # FIXED: Don't make real API calls for testing
        if self.api_key and len(self.api_key) > 10:
            logger.info("YouTube API connection test: MOCKED SUCCESS (prevents quota usage)")
            return True
        else:
            logger.error("YouTube API connection test: FAILED (no valid API key)")
            return False
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for debugging."""
        total_entries = len(self._daily_cache)
        error_entries = sum(1 for v in self._daily_cache.values() if v.get("error"))
        success_entries = total_entries - error_entries
        
        return {
            "cache_size": total_entries,
            "success_entries": success_entries,
            "error_entries": error_entries,
            "cache_date": str(self._cache_date),
            "daily_seed": self._get_daily_seed(),
            "cache_file": str(self.cache_file),
            "cache_file_exists": self.cache_file.exists()
        }
    
    def clear_cache(self):
        """Clear cache manually if needed."""
        self._daily_cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
        logger.info("YouTube cache cleared manually")

# Export the main class
__all__ = ["YouTubeAPI"]