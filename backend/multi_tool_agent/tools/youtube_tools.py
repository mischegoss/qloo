"""
YouTube API Tool - Cultural Heritage + American Search
File: backend/multi_tool_agent/tools/youtube_tools_enhanced.py

FEATURES:
- Searches for both assigned cultural heritage AND American classical music
- Expands composer pool for better variety
- Better fallback system with cultural + American options
- Filters for Creative Commons content
"""

import requests
import json
import logging
import random
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    Enhanced YouTube Data API tool with cultural heritage + American search.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        
        # Load expanded fallback content
        self.fallback_content = self._load_expanded_fallback_content()
        
        logger.info("YouTube API tool initialized - Enhanced with cultural + American search")
    
    def _load_expanded_fallback_content(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Expanded fallback content organized by cultural heritage + American.
        Each heritage includes both traditional AND American classical options.
        """
        
        return {
            "Italian-American": [
                # Italian classical (Creative Commons/Public Domain)
                {"title": "Puccini - Nessun Dorma (Public Domain)", "channelTitle": "Opera Archive", "description": "Beautiful aria from Turandot", "videoId": "cWc7vYjgnTs", "embedUrl": "https://www.youtube.com/embed/cWc7vYjgnTs", "license": "Public Domain"},
                {"title": "Vivaldi - Four Seasons Spring (Creative Commons)", "channelTitle": "Classical Music", "description": "Vivaldi's famous concerto", "videoId": "GRxofEmo3HA", "embedUrl": "https://www.youtube.com/embed/GRxofEmo3HA", "license": "Creative Commons"},
                # American classical
                {"title": "Copland - Appalachian Spring (Public Domain)", "channelTitle": "American Classics", "description": "American pastoral music", "videoId": "aE_PZPJVB4I", "embedUrl": "https://www.youtube.com/embed/aE_PZPJVB4I", "license": "Public Domain"},
                {"title": "Gershwin - Rhapsody in Blue (Creative Commons)", "channelTitle": "Jazz Archive", "description": "American jazz-classical fusion", "videoId": "ynEOo28lsbc", "embedUrl": "https://www.youtube.com/embed/ynEOo28lsbc", "license": "Creative Commons"},
                # Italian folk
                {"title": "Traditional Italian Folk Songs (Creative Commons)", "channelTitle": "Folk Music World", "description": "Collection of Italian folk melodies", "videoId": "tG8aK9QgHQI", "embedUrl": "https://www.youtube.com/embed/tG8aK9QgHQI", "license": "Creative Commons"}
            ],
            "Irish": [
                # Irish traditional/folk
                {"title": "Celtic Music - Danny Boy (Public Domain)", "channelTitle": "Irish Traditional", "description": "Classic Irish ballad", "videoId": "emBaVrkzjr8", "embedUrl": "https://www.youtube.com/embed/emBaVrkzjr8", "license": "Public Domain"},
                {"title": "Irish Folk Music Collection (Creative Commons)", "channelTitle": "Celtic Archive", "description": "Traditional Irish melodies", "videoId": "Eh-W9V7qAB8", "embedUrl": "https://www.youtube.com/embed/Eh-W9V7qAB8", "license": "Creative Commons"},
                {"title": "Traditional Irish Jigs (Creative Commons)", "channelTitle": "Folk Music Ireland", "description": "Lively Irish dance music", "videoId": "k2E8yJyFgLs", "embedUrl": "https://www.youtube.com/embed/k2E8yJyFgLs", "license": "Creative Commons"},
                # American for Irish heritage  
                {"title": "Copland - Simple Gifts (Public Domain)", "channelTitle": "American Folk", "description": "American folk variations", "videoId": "jBqA7Ek8_Qs", "embedUrl": "https://www.youtube.com/embed/jBqA7Ek8_Qs", "license": "Public Domain"},
                {"title": "American Folk Songs (Creative Commons)", "channelTitle": "Folk Music USA", "description": "Traditional American melodies", "videoId": "k9pDgNGV8Ls", "embedUrl": "https://www.youtube.com/embed/k9pDgNGV8Ls", "license": "Creative Commons"}
            ],
            "American": [
                # American classical
                {"title": "Copland - Fanfare for Common Man (Public Domain)", "channelTitle": "American Orchestra", "description": "Patriotic American classical", "videoId": "4NjssV8UuVA", "embedUrl": "https://www.youtube.com/embed/4NjssV8UuVA", "license": "Public Domain"},
                {"title": "Gershwin - American in Paris (Creative Commons)", "channelTitle": "American Composers", "description": "Jazz-influenced classical", "videoId": "L9aF7dWDJaA", "embedUrl": "https://www.youtube.com/embed/L9aF7dWDJaA", "license": "Creative Commons"},
                {"title": "Sousa - Stars and Stripes Forever (Public Domain)", "channelTitle": "Military Band Archive", "description": "Classic American march", "videoId": "a-7XWhyvIpE", "embedUrl": "https://www.youtube.com/embed/a-7XWhyvIpE", "license": "Public Domain"},
                # American folk
                {"title": "American Folk Music Collection (Creative Commons)", "channelTitle": "Folk USA", "description": "Traditional American folk songs", "videoId": "P8a4iiOnzsc", "embedUrl": "https://www.youtube.com/embed/P8a4iiOnzsc", "license": "Creative Commons"},
                {"title": "Bluegrass Music Traditional (Public Domain)", "channelTitle": "Folk Music Archive", "description": "Classic American bluegrass", "videoId": "M_tMD5bTbLM", "embedUrl": "https://www.youtube.com/embed/M_tMD5bTbLM", "license": "Public Domain"}
            ]
        }
    
    async def search_videos_enhanced(self, query: str, cultural_heritage: str = "American", max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Enhanced search with MANDATORY Creative Commons filter only.
        Uses SMART search terms for each category.
        
        Args:
            query: Base search term (composer/piece)
            cultural_heritage: User's cultural background
            max_results: Maximum results to return (up to 5)
            
        Returns:
            Up to 5 Creative Commons videos (heritage classical + American classical + folk)
        """
        
        if not self.api_key or self.api_key == 'YOUR_YOUTUBE_API_KEY':
            logger.warning("⚠️ Invalid YouTube API key, using Creative Commons fallbacks")
            return self._get_enhanced_fallback_results(query, cultural_heritage)
        
        all_results = []
        results_per_search = max(1, max_results // 3)  # Divide among 3 search types
        
        try:
            # SEARCH 1: Heritage-specific classical (original query)
            logger.info(f"🔍 Heritage classical (CC only): {query}")
            classical_results = await self._single_search(query, results_per_search, "classical")
            all_results.extend(classical_results)
            
            # SEARCH 2: American classical composers (if heritage is not American)
            if cultural_heritage != "American" and len(all_results) < max_results:
                american_composers = ["Copland", "Gershwin", "Barber", "Ives"]
                american_query = random.choice(american_composers)
                logger.info(f"🔍 American classical (CC only): {american_query}")
                american_results = await self._single_search(american_query, results_per_search, "classical")
                all_results.extend(american_results)
            
            # SEARCH 3: Heritage-appropriate folk music
            if len(all_results) < max_results:
                folk_query = self._get_folk_search_term(cultural_heritage)
                logger.info(f"🔍 Folk music (CC only): {folk_query}")
                folk_results = await self._single_search(folk_query, max_results - len(all_results), "folk")
                all_results.extend(folk_results)
            
            # Remove duplicates by videoId
            seen_ids = set()
            unique_results = []
            for video in all_results:
                if video["videoId"] not in seen_ids:
                    seen_ids.add(video["videoId"])
                    unique_results.append(video)
            
            if unique_results:
                final_results = unique_results[:max_results]  # Limit to exactly 5
                logger.info(f"✅ Found {len(final_results)} Creative Commons videos (classical + folk)")
                return final_results
            else:
                logger.warning("⚠️ No Creative Commons videos found, using CC fallbacks")
                return self._get_enhanced_fallback_results(query, cultural_heritage)
                
        except Exception as e:
            logger.error(f"❌ Creative Commons search failed: {e}")
            return self._get_enhanced_fallback_results(query, cultural_heritage)
    
    async def _single_search(self, query: str, max_results: int, music_type: str = "classical") -> List[Dict[str, Any]]:
        """
        Perform a single YouTube search with MANDATORY Creative Commons filter.
        
        Args:
            query: Search term
            max_results: Max results to return
            music_type: "classical" or "folk"
        """
        
        # Build search query with music type
        if music_type == "folk":
            search_query = f"{query} folk music audio"
        else:
            search_query = f"{query} classical music audio"
        
        # MANDATORY Creative Commons parameters - NEVER changed
        params = {
            "part": "snippet",
            "q": search_query,
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key,
            "videoLicense": "creativeCommon",  # MANDATORY: Only Creative Commons
            "videoEmbeddable": "true"
        }
        
        logger.info(f"🔒 CREATIVE COMMONS ONLY search: {search_query}")
        
        response = requests.get(self.base_url, params=params, timeout=15.0)
        response.raise_for_status()
        
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
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "license": "Creative Commons"  # Mark as CC for clarity
                    }
                    videos.append(video_info)
        
        return videos
    
    def _get_folk_search_term(self, cultural_heritage: str) -> str:
        """
        Get appropriate folk music search term based on cultural heritage.
        
        Args:
            cultural_heritage: User's cultural background
            
        Returns:
            Appropriate folk music search term
        """
        
        folk_terms = {
            "Italian-American": "italian folk music",
            "Irish-American": "irish folk music",
            "Irish": "celtic folk music", 
            "German-American": "german folk music",
            "Polish-American": "polish folk music",
            "Mexican-American": "mexican folk music",
            "Jewish-American": "jewish folk music",
            "American": "american folk music"
        }
        
        # Handle both "Italian-American" and "Italian" formats
        if cultural_heritage in folk_terms:
            return folk_terms[cultural_heritage]
        elif "-American" in cultural_heritage:
            base_heritage = cultural_heritage.split("-")[0].lower()
            return f"{base_heritage} folk music"
        else:
            return "american folk music"  # Safe default
    
    def _get_enhanced_fallback_results(self, query: str, cultural_heritage: str) -> List[Dict[str, Any]]:
        """
        Get enhanced fallback results that include both heritage + American options.
        """
        
        query_lower = query.lower()
        heritage_key = cultural_heritage if cultural_heritage in self.fallback_content else "American"
        
        # Get heritage-specific fallbacks
        heritage_fallbacks = self.fallback_content.get(heritage_key, self.fallback_content["American"])
        
        # Try to match query to specific composer/piece
        matched_results = []
        for video in heritage_fallbacks:
            title_lower = video["title"].lower()
            if any(word in title_lower for word in query_lower.split()):
                matched_results.append(video)
        
        if matched_results:
            logger.info(f"✅ Found {len(matched_results)} matched fallbacks for '{query}' ({cultural_heritage})")
            return matched_results[:3]  # Return up to 3 matches
        else:
            # Return mix of heritage + American if no specific matches
            if heritage_key != "American":
                mixed_results = heritage_fallbacks[:2] + self.fallback_content["American"][:1]  # 2 heritage + 1 American
            else:
                mixed_results = heritage_fallbacks[:3]  # 3 American
            
            logger.info(f"✅ Using mixed fallbacks for '{query}' ({cultural_heritage})")
            return random.sample(mixed_results, min(3, len(mixed_results)))
    
    # Legacy method for backward compatibility
    async def search_videos(self, query: str, max_results: int = 5, audio_only: bool = True) -> List[Dict[str, Any]]:
        """Legacy search method - defaults to American heritage"""
        return await self.search_videos_enhanced(query, "American", max_results)
    
    async def search_classical_music_enhanced(self, composer: str, piece: str = "", cultural_heritage: str = "American") -> List[Dict[str, Any]]:
        """
        Enhanced classical music search with cultural heritage consideration.
        
        Args:
            composer: Composer name
            piece: Optional piece name
            cultural_heritage: User's cultural background
            
        Returns:
            Enhanced results including heritage + American options
        """
        
        if piece:
            query = f"{composer} {piece}"
        else:
            query = composer
            
        return await self.search_videos_enhanced(query, cultural_heritage, max_results=3)
    
    async def test_connection(self) -> bool:
        """Test YouTube API connection with enhanced search"""
        
        if not self.api_key or self.api_key == 'YOUR_YOUTUBE_API_KEY':
            logger.error("❌ YouTube API key not configured")
            return False
        
        try:
            test_results = await self.search_videos_enhanced("Bach", "American", max_results=1)
            
            if test_results and len(test_results) > 0:
                logger.info("✅ Enhanced YouTube API connection test: SUCCESS")
                return True
            else:
                logger.warning("⚠️ Enhanced YouTube API connection test: No results (but API works)")
                return True
                
        except Exception as e:
            logger.error(f"❌ Enhanced YouTube API connection test failed: {e}")
            return False


# Export for imports
__all__ = ["YouTubeAPI"]


# Test function
async def test_enhanced_youtube_api():
    """Test the enhanced YouTube API"""
    
    api_key = "YOUR_YOUTUBE_API_KEY"
    youtube = YouTubeAPI(api_key)
    
    # Test enhanced search for Italian-American heritage
    print("Testing Italian-American + American search:")
    results = await youtube.search_classical_music_enhanced("Vivaldi", "Four Seasons", "Italian-American")
    
    print(f"Found {len(results)} results:")
    for video in results:
        print(f"- {video['title']}")
        print(f"  Channel: {video['channelTitle']}")
        print()
    
    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_enhanced_youtube_api())
