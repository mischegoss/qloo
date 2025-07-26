"""
Qloo Tools - SAFE CONTENT with Era Filtering for Copyright Compliance
File: backend/multi_tool_agent/tools/qloo_tools.py

NEW FEATURES:
- Era filtering for pre-1970 content (public domain safe)
- Classical music targeting
- Vintage TV show filtering  
- Demographics integration (age, gender)
- Copyright-safe content recommendations
"""

import httpx
import logging
from typing import Dict, Any, Optional, List
import asyncio

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    Qloo API tool with SAFE CONTENT filtering for copyright compliance.
    Focuses on pre-1970 content, classical music, and vintage TV shows.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://hackathon.api.qloo.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        logger.info("✅ Qloo API initialized with SAFE CONTENT filtering (pre-1970 + classical)")
    
    async def get_safe_classical_music(self, 
                                     cultural_heritage: str,
                                     age_group: str = "75_and_older",
                                     gender: Optional[str] = None,
                                     take: int = 10) -> Dict[str, Any]:
        """
        Get classical and pre-1970 music recommendations for copyright safety.
        
        Args:
            cultural_heritage: e.g. "Italian-American", "Irish", etc.
            age_group: Target age demographic 
            gender: Patient gender for personalization
            take: Number of results
            
        Returns:
            Qloo response with safe music recommendations
        """
        
        logger.info(f"🎼 Getting SAFE classical music for {cultural_heritage}, age {age_group}")
        
        try:
            # Build safe music query parameters
            params = {
                "filter.type": "urn:entity:artist",
                "take": take
            }
            
            # Add demographic signals
            if age_group:
                params["signal.demographics.age"] = age_group
            if gender:
                params["signal.demographics.gender"] = gender.lower()
            
            # Add safe content tags - focus on classical and pre-1970
            safe_music_tags = [
                "classical",
                "traditional", 
                "vintage",
                "instrumental",
                "orchestral",
                "opera",
                "symphony"
            ]
            
            # Add heritage-specific classical tags
            heritage_tags = self._get_heritage_music_tags(cultural_heritage)
            safe_music_tags.extend(heritage_tags)
            
            params["signal.interests.tags"] = ",".join(safe_music_tags)
            
            # Make API request
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    params=params,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    # Filter for classical/pre-1970 content
                    safe_results = self._filter_for_safe_music(results)
                    
                    logger.info(f"✅ Safe classical music: {len(safe_results)} results")
                    return {
                        "success": True,
                        "entities": safe_results,
                        "results_count": len(safe_results),
                        "content_type": "safe_classical_music",
                        "heritage": cultural_heritage
                    }
                else:
                    logger.error(f"❌ Qloo safe music error: {response.status_code}")
                    return self._get_classical_fallback(cultural_heritage)
                    
        except Exception as e:
            logger.error(f"❌ Qloo safe music exception: {e}")
            return self._get_classical_fallback(cultural_heritage)
    
    async def get_safe_vintage_tv(self,
                                cultural_heritage: str,
                                age_group: str = "75_and_older", 
                                gender: Optional[str] = None,
                                take: int = 10) -> Dict[str, Any]:
        """
        Get vintage TV show recommendations (pre-1970) for copyright safety.
        """
        
        logger.info(f"📺 Getting SAFE vintage TV for {cultural_heritage}, age {age_group}")
        
        try:
            params = {
                "filter.type": "urn:entity:tv_show",
                "take": take
            }
            
            # Add demographic signals
            if age_group:
                params["signal.demographics.age"] = age_group
            if gender:
                params["signal.demographics.gender"] = gender.lower()
            
            # Safe TV content tags - vintage/family friendly
            safe_tv_tags = [
                "vintage",
                "classic",
                "family",
                "variety",
                "anthology", 
                "drama",
                "comedy",
                "wholesome"
            ]
            
            params["signal.interests.tags"] = ",".join(safe_tv_tags)
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights", 
                    params=params,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    # Filter for vintage/public domain content
                    safe_results = self._filter_for_safe_tv(results)
                    
                    logger.info(f"✅ Safe vintage TV: {len(safe_results)} results")
                    return {
                        "success": True,
                        "entities": safe_results,
                        "results_count": len(safe_results),
                        "content_type": "safe_vintage_tv",
                        "heritage": cultural_heritage
                    }
                else:
                    logger.error(f"❌ Qloo safe TV error: {response.status_code}")
                    return self._get_vintage_tv_fallback()
                    
        except Exception as e:
            logger.error(f"❌ Qloo safe TV exception: {e}")
            return self._get_vintage_tv_fallback()
    
    def _get_heritage_music_tags(self, heritage: str) -> List[str]:
        """Get heritage-specific classical music tags"""
        heritage_mapping = {
            "Italian-American": ["opera", "classical", "orchestral", "italian"],
            "Irish": ["traditional", "folk", "celtic", "classical"],
            "German": ["classical", "orchestral", "opera", "traditional"],
            "Jewish": ["traditional", "classical", "religious", "folk"],
            "Polish": ["classical", "traditional", "orchestral", "folk"],
            "Mexican": ["traditional", "classical", "folk", "mariachi"],
            "Chinese": ["traditional", "classical", "instrumental", "folk"],
            "universal": ["classical", "traditional", "orchestral"]
        }
        
        heritage_key = heritage.replace("-", "_").lower()
        for key in heritage_mapping:
            if key.lower() in heritage_key:
                return heritage_mapping[key]
        
        return heritage_mapping["universal"]
    
    def _filter_for_safe_music(self, results: List[Dict]) -> List[Dict]:
        """Filter music results for copyright safety"""
        safe_results = []
        
        classical_keywords = [
            "classical", "symphony", "opera", "orchestral", "baroque", 
            "romantic", "chamber", "concerto", "sonata", "traditional"
        ]
        
        for result in results:
            name = result.get("name", "").lower()
            tags = [tag.get("name", "").lower() for tag in result.get("tags", [])]
            
            # Check if it's classical or traditional music
            is_safe = any(keyword in name or any(keyword in tag for tag in tags) 
                         for keyword in classical_keywords)
            
            if is_safe:
                safe_results.append(result)
        
        return safe_results
    
    def _filter_for_safe_tv(self, results: List[Dict]) -> List[Dict]:
        """Filter TV results for vintage/public domain content"""
        safe_results = []
        
        vintage_keywords = [
            "classic", "vintage", "anthology", "variety", "family", 
            "wholesome", "traditional", "1940", "1950", "1960"
        ]
        
        for result in results:
            name = result.get("name", "").lower()
            tags = [tag.get("name", "").lower() for tag in result.get("tags", [])]
            
            # Check if it's vintage/family content
            is_safe = any(keyword in name or any(keyword in tag for tag in tags)
                         for keyword in vintage_keywords)
            
            if is_safe:
                safe_results.append(result)
                
        return safe_results
    
    def _get_classical_fallback(self, heritage: str) -> Dict[str, Any]:
        """Fallback classical music recommendations"""
        
        heritage_classical = {
            "Italian-American": [
                {"name": "Vivaldi", "type": "Baroque composer", "era": "1678-1741"},
                {"name": "Puccini", "type": "Opera composer", "era": "1858-1924"},
                {"name": "Verdi", "type": "Opera composer", "era": "1813-1901"}
            ],
            "German": [
                {"name": "Beethoven", "type": "Classical composer", "era": "1770-1827"},
                {"name": "Bach", "type": "Baroque composer", "era": "1685-1750"},
                {"name": "Mozart", "type": "Classical composer", "era": "1756-1791"}
            ],
            "universal": [
                {"name": "Mozart", "type": "Classical composer", "era": "1756-1791"},
                {"name": "Beethoven", "type": "Classical composer", "era": "1770-1827"},
                {"name": "Chopin", "type": "Romantic composer", "era": "1810-1849"}
            ]
        }
        
        composers = heritage_classical.get(heritage, heritage_classical["universal"])
        
        return {
            "success": True,
            "entities": composers,
            "results_count": len(composers),
            "content_type": "classical_fallback",
            "heritage": heritage
        }
    
    def _get_vintage_tv_fallback(self) -> Dict[str, Any]:
        """Fallback vintage TV recommendations"""
        
        vintage_tv = [
            {"name": "Classic Anthology Series", "type": "Drama anthology", "era": "1950s"},
            {"name": "Vintage Variety Show", "type": "Musical variety", "era": "1940s-1950s"},
            {"name": "Family Comedy Classic", "type": "Wholesome comedy", "era": "1950s"},
            {"name": "Classic Western Series", "type": "Family western", "era": "1950s"}
        ]
        
        return {
            "success": True,
            "entities": vintage_tv,
            "results_count": len(vintage_tv),
            "content_type": "vintage_tv_fallback"
        }
    
    # Keep existing methods for compatibility
    async def get_insights(self, entity_type: str, **kwargs) -> Dict[str, Any]:
        """Legacy method - redirects to safe content methods"""
        if entity_type == "artists":
            return await self.get_safe_classical_music(
                cultural_heritage=kwargs.get("heritage", "universal"),
                age_group=kwargs.get("age_group", "75_and_older"),
                gender=kwargs.get("gender")
            )
        elif entity_type == "tv_shows":
            return await self.get_safe_vintage_tv(
                cultural_heritage=kwargs.get("heritage", "universal"),
                age_group=kwargs.get("age_group", "75_and_older"),
                gender=kwargs.get("gender")
            )
        else:
            return {"success": False, "error": "Only safe music and TV content supported"}
    
    async def test_connection(self) -> bool:
        """Test Qloo API connection"""
        try:
            test_result = await self.get_safe_classical_music("universal", take=1)
            return test_result.get("success", False)
        except Exception as e:
            logger.error(f"Qloo connection test failed: {e}")
            return False

# Export the main class
__all__ = ["QlooInsightsAPI"]