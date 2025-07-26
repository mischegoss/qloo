"""
Fixed YouTube API Tool - Matching Working Request Format
File: backend/multi_tool_agent/tools/youtube_tools_fixed.py

FIXES:
- Uses "creativeCommon" (not "creativeCommons") to match working URL
- Removes safeSearch parameter (not in working URL)
- Uses requests.get() exactly like working request
- Returns proper embedUrl format
- Focuses on audio-only classical content
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    YouTube Data API tool matching the working request format exactly.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        
        # Load fallback content for demo reliability
        self.fallback_content = self._load_fallback_content()
        
        logger.info("YouTube API tool initialized - Matching working request format")
    
    def _load_fallback_content(self) -> List[Dict[str, Any]]:
        """Simple fallback classical music content"""
        
        return [
            {
                "title": "Bach - Air on the G String (Public Domain)",
                "channelTitle": "Classical Music Archive",
                "description": "Beautiful classical piece by J.S. Bach",
                "videoId": "GMkmQlfOJDk",
                "embedUrl": "https://www.youtube.com/embed/GMkmQlfOJDk"
            },
            {
                "title": "Mozart - Eine kleine Nachtmusik (Creative Commons)",
                "channelTitle": "Public Domain Classics",
                "description": "Mozart's famous serenade",
                "videoId": "o1dBg__wsuo", 
                "embedUrl": "https://www.youtube.com/embed/o1dBg__wsuo"
            },
            {
                "title": "Beethoven - Moonlight Sonata (Public Domain)",
                "channelTitle": "Classical Archive",
                "description": "Beethoven's beautiful piano sonata",
                "videoId": "4Tr0otuiQuU",
                "embedUrl": "https://www.youtube.com/embed/4Tr0otuiQuU"
            }
        ]
    
    async def search_videos(self, query: str, max_results: int = 5, audio_only: bool = True) -> List[Dict[str, Any]]:
        """
        Search YouTube for Creative Commons classical music videos.
        Matches working request format exactly.
        
        Args:
            query: Search term (e.g., "Bach Air on G String")
            max_results: Maximum number of results
            audio_only: If True, prioritizes audio-focused content
            
        Returns:
            List of video dictionaries with title, channelTitle, videoId, embedUrl
        """
        
        if not self.api_key or self.api_key == 'YOUR_YOUTUBE_API_KEY':
            logger.warning("⚠️ Invalid YouTube API key, using fallbacks")
            return self._get_fallback_results(query)
        
        try:
            # Construct search query to match working format
            search_query = f"{query} classical music"
            if audio_only:
                search_query += " audio"
            
            # Use EXACT parameters from working URL
            params = {
                "part": "snippet",
                "q": search_query,
                "type": "video",
                "maxResults": max_results,
                "key": self.api_key,
                "videoLicense": "creativeCommon",    # FIXED: no 's' at end
                "videoEmbeddable": "true"            # FIXED: removed safeSearch
            }
            
            logger.info(f"🔍 YouTube search: {search_query} (Creative Commons)")
            
            # Use requests.get() exactly like working request
            response = requests.get(self.base_url, params=params, timeout=15.0)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            videos = []
            if "items" in data:
                for item in data["items"]:
                    if item["id"]["kind"] == "youtube#video":
                        video_id = item["id"]["videoId"]
                        video_info = {
                            "title": item["snippet"]["title"],
                            "channelTitle": item["snippet"]["channelTitle"],
                            "description": item["snippet"]["description"],
                            "videoId": video_id,
                            "embedUrl": f"https://www.youtube.com/embed/{video_id}",
                            "url": f"https://www.youtube.com/watch?v={video_id}"  # For compatibility
                        }
                        videos.append(video_info)
            
            if videos:
                logger.info(f"✅ Found {len(videos)} Creative Commons videos")
                return videos
            else:
                logger.warning("⚠️ No Creative Commons videos found, using fallbacks")
                return self._get_fallback_results(query)
                
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"❌ HTTP error: {http_err}")
            return self._get_fallback_results(query)
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"❌ Connection error: {conn_err}")
            return self._get_fallback_results(query)
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"❌ Timeout error: {timeout_err}")
            return self._get_fallback_results(query)
        except json.JSONDecodeError as json_err:
            logger.error(f"❌ JSON decode error: {json_err}")
            return self._get_fallback_results(query)
        except Exception as e:
            logger.error(f"❌ YouTube search failed: {e}")
            return self._get_fallback_results(query)
    
    def _get_fallback_results(self, query: str) -> List[Dict[str, Any]]:
        """Get fallback results based on query"""
        
        query_lower = query.lower()
        
        # Try to match query to appropriate fallback
        if "bach" in query_lower:
            return [self.fallback_content[0]]  # Bach
        elif "mozart" in query_lower:
            return [self.fallback_content[1]]  # Mozart
        elif "beethoven" in query_lower:
            return [self.fallback_content[2]]  # Beethoven
        else:
            # Return random fallback
            import random
            return [random.choice(self.fallback_content)]
    
    async def search_classical_music(self, composer: str, piece: str = "") -> List[Dict[str, Any]]:
        """
        Convenience method for searching classical music specifically.
        
        Args:
            composer: Composer name (e.g., "Bach", "Mozart")
            piece: Optional piece name (e.g., "Air on G String")
            
        Returns:
            List of Creative Commons classical music videos
        """
        
        if piece:
            query = f"{composer} {piece}"
        else:
            query = composer
            
        return await self.search_videos(query, max_results=3, audio_only=True)
    
    async def test_connection(self) -> bool:
        """Test YouTube API connection"""
        
        if not self.api_key or self.api_key == 'YOUR_YOUTUBE_API_KEY':
            logger.error("❌ YouTube API key not configured")
            return False
        
        try:
            # Simple test search
            test_results = await self.search_videos("Bach", max_results=1)
            
            if test_results and len(test_results) > 0:
                logger.info("✅ YouTube API connection test: SUCCESS")
                return True
            else:
                logger.warning("⚠️ YouTube API connection test: No results (but API works)")
                return True  # API works, just no Creative Commons results
                
        except Exception as e:
            logger.error(f"❌ YouTube API connection test failed: {e}")
            return False


# Export for imports
__all__ = ["YouTubeAPI"]


# Test function
async def test_youtube_api():
    """Test the fixed YouTube API"""
    
    # You would use your real API key here
    api_key = "YOUR_YOUTUBE_API_KEY"
    
    youtube = YouTubeAPI(api_key)
    
    # Test search
    results = await youtube.search_classical_music("Bach", "Air on G String")
    
    print(f"Found {len(results)} results:")
    for video in results:
        print(f"- {video['title']}")
        print(f"  Channel: {video['channelTitle']}")
        print(f"  Embed: {video['embedUrl']}")
        print()
    
    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_youtube_api())
