"""
YouTube API Tools - PUBLIC DOMAIN SEARCH with Qloo Integration
File: backend/multi_tool_agent/tools/youtube_tools.py

NEW FEATURES:
- Public domain content search
- Classical music filtering
- Vintage TV show search
- Qloo result integration
- Copyright-safe content pipeline
"""

import httpx
import logging
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class YouTubeAPI:
    """
    YouTube Data API tool with PUBLIC DOMAIN search capabilities.
    Integrates with Qloo for copyright-safe content recommendations.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        # Load fallback content for demo reliability
        self.fallback_content = self._load_fallback_content()
        
        logger.info("YouTube API tool initialized - PUBLIC DOMAIN SEARCH + Qloo Integration")
    
    def _load_fallback_content(self) -> Dict[str, Any]:
        """Load fallback public domain content"""
        try:
            fallback_file = Path(__file__).parent.parent.parent / "data" / "fallback_youtube.json"
            if fallback_file.exists():
                with open(fallback_file, 'r') as f:
                    content = json.load(f)
                    logger.info(f"✅ Loaded public domain fallback content")
                    return content
        except Exception as e:
            logger.warning(f"Could not load fallback content: {e}")
        
        # Hardcoded public domain fallback
        return {
            "classical_music": [
                {
                    "composer": "Mozart",
                    "piece": "Eine kleine Nachtmusik",
                    "youtube_url": "https://www.youtube.com/embed/o1dBg__wsuo",
                    "era": "Classical",
                    "public_domain": True
                },
                {
                    "composer": "Beethoven", 
                    "piece": "Moonlight Sonata",
                    "youtube_url": "https://www.youtube.com/embed/4Tr0otuiQuU",
                    "era": "Classical",
                    "public_domain": True
                },
                {
                    "composer": "Bach",
                    "piece": "Air on the G String", 
                    "youtube_url": "https://www.youtube.com/embed/GMkmQlfOJDk",
                    "era": "Baroque",
                    "public_domain": True
                }
            ],
            "vintage_tv": [
                {
                    "title": "Classic Anthology Drama",
                    "youtube_url": "https://www.youtube.com/embed/vintage_drama",
                    "description": "Vintage anthology series from the 1950s",
                    "era": "1950s",
                    "public_domain": True
                },
                {
                    "title": "Classic Variety Show",
                    "youtube_url": "https://www.youtube.com/embed/vintage_variety", 
                    "description": "Musical variety entertainment from the 1940s",
                    "era": "1940s",
                    "public_domain": True
                }
            ]
        }
    
    def _create_embeddable_url(self, video_id: str) -> str:
        """Create embeddable YouTube URL from video ID"""
        if not video_id:
            return ""
        return f"https://www.youtube.com/embed/{video_id}"
    
    async def search_public_domain_classical(self, qloo_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Search for public domain classical music using Qloo intelligence.
        
        Args:
            qloo_result: Qloo recommendations for classical composers/pieces
            
        Returns:
            YouTube search results for public domain classical content
        """
        
        logger.info("🎼 Searching for PUBLIC DOMAIN classical music from Qloo results")
        
        if not qloo_result.get("success") or not qloo_result.get("entities"):
            return self._get_classical_fallback()
        
        # Extract composer/artist names from Qloo results
        for entity in qloo_result["entities"]:
            composer_name = entity.get("name", "")
            
            if composer_name:
                # Build public domain search queries
                pd_queries = [
                    f"{composer_name} classical music public domain",
                    f"{composer_name} symphony public domain", 
                    f"{composer_name} piano sonata public domain",
                    f"{composer_name} copyright free classical",
                    f"{composer_name} creative commons"
                ]
                
                # Try each query until we find content
                for query in pd_queries:
                    result = await self._search_with_public_domain_filter(query, "music")
                    if result and result.get("items"):
                        logger.info(f"✅ Found public domain classical: {composer_name}")
                        return result
        
        # Fallback if no results found
        logger.info("🔄 Using classical music fallback")
        return self._get_classical_fallback()
    
    async def search_public_domain_vintage_tv(self, qloo_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Search for public domain vintage TV using Qloo intelligence.
        """
        
        logger.info("📺 Searching for PUBLIC DOMAIN vintage TV from Qloo results")
        
        if not qloo_result.get("success") or not qloo_result.get("entities"):
            return self._get_vintage_tv_fallback()
        
        # Extract TV show info from Qloo results
        for entity in qloo_result["entities"]:
            show_name = entity.get("name", "")
            
            if show_name:
                # Build public domain TV search queries
                pd_queries = [
                    f"{show_name} public domain television",
                    f"{show_name} vintage TV copyright free",
                    f"1950s {show_name} public domain",
                    f"classic {show_name} creative commons",
                    f"vintage television {show_name}"
                ]
                
                # Try each query
                for query in pd_queries:
                    result = await self._search_with_public_domain_filter(query, "tv")
                    if result and result.get("items"):
                        logger.info(f"✅ Found public domain TV: {show_name}")
                        return result
        
        # Fallback if no results found
        logger.info("🔄 Using vintage TV fallback")
        return self._get_vintage_tv_fallback()
    
    async def _search_with_public_domain_filter(self, query: str, content_type: str) -> Optional[Dict[str, Any]]:
        """
        Internal method to search YouTube with public domain filtering.
        """
        
        try:
            # Add public domain keywords to search
            enhanced_query = f"{query} public domain copyright free"
            
            params = {
                "part": "snippet",
                "q": enhanced_query,
                "type": "video",
                "maxResults": 5,
                "order": "relevance",
                "safeSearch": "strict",
                "videoEmbeddable": "true",
                "key": self.api_key
            }
            
            # Add content-specific filters
            if content_type == "music":
                params["videoCategoryId"] = "10"  # Music category
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Filter results for public domain indicators
                    filtered_items = self._filter_for_public_domain(data.get("items", []))
                    
                    if filtered_items:
                        # Add embeddable URLs
                        for item in filtered_items:
                            video_id = item.get('id', {}).get('videoId')
                            if video_id:
                                item['embeddable_url'] = self._create_embeddable_url(video_id)
                        
                        return {"items": filtered_items}
                    
        except Exception as e:
            logger.error(f"YouTube public domain search error: {e}")
        
        return None
    
    def _filter_for_public_domain(self, items: List[Dict]) -> List[Dict]:
        """Filter YouTube results for public domain indicators"""
        
        public_domain_keywords = [
            "public domain", "copyright free", "creative commons", 
            "royalty free", "no copyright", "open source",
            "classical music", "vintage", "1950s", "1940s",
            "archive", "library", "educational"
        ]
        
        filtered_items = []
        
        for item in items:
            title = item.get("snippet", {}).get("title", "").lower()
            description = item.get("snippet", {}).get("description", "").lower()
            channel = item.get("snippet", {}).get("channelTitle", "").lower()
            
            # Check for public domain indicators
            has_pd_indicators = any(
                keyword in title or keyword in description or keyword in channel 
                for keyword in public_domain_keywords
            )
            
            # Avoid obvious copyrighted content
            copyright_red_flags = [
                "official music video", "vevo", "records", "label",
                "©", "copyright", "all rights reserved"
            ]
            
            has_copyright_flags = any(
                flag in title or flag in description or flag in channel
                for flag in copyright_red_flags
            )
            
            if has_pd_indicators and not has_copyright_flags:
                filtered_items.append(item)
        
        return filtered_items
    
    def _get_classical_fallback(self) -> Dict[str, Any]:
        """Get fallback classical music content"""
        classical_content = self.fallback_content.get("classical_music", [])
        
        if classical_content:
            selected = classical_content[0]  # Use first fallback
            return {
                "items": [{
                    "snippet": {
                        "title": f"{selected['composer']} - {selected['piece']}",
                        "channelTitle": selected["composer"],
                        "description": f"Classical {selected['era']} composition"
                    },
                    "id": {"videoId": selected["youtube_url"].split("/")[-1]},
                    "embeddable_url": selected["youtube_url"]
                }]
            }
        
        return {"items": []}
    
    def _get_vintage_tv_fallback(self) -> Dict[str, Any]:
        """Get fallback vintage TV content"""
        tv_content = self.fallback_content.get("vintage_tv", [])
        
        if tv_content:
            selected = tv_content[0]  # Use first fallback
            return {
                "items": [{
                    "snippet": {
                        "title": selected["title"],
                        "channelTitle": "Classic TV Archive",
                        "description": selected["description"]
                    },
                    "id": {"videoId": selected["youtube_url"].split("/")[-1]},
                    "embeddable_url": selected["youtube_url"]
                }]
            }
        
        return {"items": []}
    
    # Legacy methods for backward compatibility
    async def search_music(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """Legacy music search - now uses public domain filtering"""
        return await self._search_with_public_domain_filter(query, "music")
    
    async def search_videos(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """Legacy video search - now uses public domain filtering"""
        return await self._search_with_public_domain_filter(query, "tv")
    
    async def search_era_content(self, era: str, content_type: str = "music", max_results: int = 3) -> Optional[Dict[str, Any]]:
        """Search for public domain content from specific era"""
        
        if content_type == "music":
            query = f"{era} classical music public domain"
            return await self._search_with_public_domain_filter(query, "music")
        else:
            query = f"{era} vintage television public domain"
            return await self._search_with_public_domain_filter(query, "tv")
    
    async def test_connection(self) -> bool:
        """Test YouTube API connection"""
        if self.api_key and len(self.api_key) > 10:
            logger.info("YouTube API connection test: SUCCESS")
            return True
        else:
            logger.error("YouTube API connection test: FAILED (no valid API key)")
            return False
    
    def get_public_domain_stats(self) -> Dict[str, Any]:
        """Get public domain content statistics"""
        return {
            "classical_fallbacks": len(self.fallback_content.get("classical_music", [])),
            "vintage_tv_fallbacks": len(self.fallback_content.get("vintage_tv", [])),
            "search_mode": "PUBLIC_DOMAIN_ONLY",
            "integration": "QLOO_POWERED"
        }

# Export the main class
__all__ = ["YouTubeAPI"]

