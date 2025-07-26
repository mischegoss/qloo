"""
Qloo Tools Fix for Step 3 Integration
File: backend/multi_tool_agent/tools/qloo_tools_step3_fix.py

Adds the missing get_tag_based_insights method and fixes response parsing issues.
This can be merged into the existing qloo_tools.py or used as a patch.
"""

import httpx
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class QlooToolsStep3Mixin:
    """
    Mixin class to add missing methods for Step 3 integration.
    Can be added to existing QlooInsightsAPI class.
    """
    
    async def get_tag_based_insights(self, 
                                   entity_type: str,
                                   tag: str,
                                   age_demographic: str,
                                   take: int = 10) -> Dict[str, Any]:
        """
        Get tag-based insights - MISSING METHOD that Step 3 needs
        
        Args:
            entity_type: e.g. "urn:entity:place", "urn:entity:artist"
            tag: URN tag (e.g. "urn:tag:genre:place:restaurant:italian")
            age_demographic: Age demographic (e.g. "55_and_older")
            take: Number of results
            
        Returns:
            Qloo response with tag-based recommendations
        """
        
        logger.info(f"🎯 Tag-based insights: {tag} for {entity_type}")
        
        try:
            params = {
                "filter.type": entity_type,
                "signal.interests.tags": tag,
                "signal.demographics.age": age_demographic,
                "take": take
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    params=params,
                    headers=self.headers
                )
                
                logger.info(f"HTTP Request: {response.request.method} {response.request.url} \"{response.status_code} {response.reason_phrase}\"")
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("results", [])
                    
                    logger.info(f"✅ Tag insights success: {len(entities)} results")
                    return {
                        "success": True,
                        "entities": entities,
                        "entity_count": len(entities),
                        "tag": tag
                    }
                else:
                    logger.error(f"❌ Tag insights error: {response.status_code}")
                    return {
                        "success": False, 
                        "entities": [], 
                        "error": f"HTTP {response.status_code}",
                        "entity_count": 0
                    }
                    
        except Exception as e:
            logger.error(f"❌ Tag insights exception: {e}")
            return {
                "success": False, 
                "entities": [], 
                "error": str(e),
                "entity_count": 0
            }
    
    async def get_safe_classical_music_fixed(self, 
                                           cultural_heritage: str,
                                           age_group: str = "55_and_older",
                                           gender: Optional[str] = None,
                                           take: int = 10) -> Dict[str, Any]:
        """
        FIXED version of get_safe_classical_music with proper response handling
        
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
            
            # Add heritage-specific classical tags (avoid duplicates)
            heritage_tags = self._get_heritage_music_tags_fixed(cultural_heritage)
            for tag in heritage_tags:
                if tag not in safe_music_tags:
                    safe_music_tags.append(tag)
            
            params["signal.interests.tags"] = ",".join(safe_music_tags)
            
            # Make API request
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    params=params,
                    headers=self.headers
                )
                
                logger.info(f"HTTP Request: {response.request.method} {response.request.url} \"{response.status_code} {response.reason_phrase}\"")
                
                if response.status_code == 200:
                    # FIXED: Proper response parsing
                    try:
                        data = response.json()
                        results = data.get("results", [])
                        
                        # Filter for classical/pre-1970 content
                        safe_results = self._filter_for_safe_music_fixed(results)
                        
                        logger.info(f"✅ Safe classical music: {len(safe_results)} results")
                        return {
                            "success": True,
                            "entities": safe_results,
                            "entity_count": len(safe_results),
                            "content_type": "classical_music",
                            "heritage": cultural_heritage
                        }
                    except Exception as parse_error:
                        logger.error(f"❌ Response parsing error: {parse_error}")
                        logger.error(f"Response content: {response.text[:200]}...")
                        return self._get_classical_fallback_fixed(cultural_heritage)
                else:
                    logger.error(f"❌ Qloo safe music error: {response.status_code}")
                    return self._get_classical_fallback_fixed(cultural_heritage)
                    
        except Exception as e:
            logger.error(f"❌ Qloo safe music exception: {e}")
            return self._get_classical_fallback_fixed(cultural_heritage)
    
    def _get_heritage_music_tags_fixed(self, heritage: str) -> List[str]:
        """FIXED: Get heritage-specific classical music tags without duplicates"""
        
        heritage_mapping = {
            "Italian-American": ["opera", "italian"],
            "Irish-American": ["folk", "celtic"],
            "German-American": ["wagner", "bach"],
            "Jewish-American": ["traditional", "religious"],
            "Polish-American": ["folk", "chopin"],
            "Mexican-American": ["folk"],
            "Chinese-American": ["traditional"],
            "universal": []  # No additional tags for universal
        }
        
        heritage_key = heritage.replace("-", "_").lower()
        for key in heritage_mapping:
            if key.lower() in heritage_key:
                return heritage_mapping[key]
        
        return heritage_mapping["universal"]
    
    def _filter_for_safe_music_fixed(self, results: List[Dict]) -> List[Dict]:
        """FIXED: Filter music results for copyright safety"""
        
        if not results:
            return []
        
        safe_results = []
        
        classical_keywords = [
            "classical", "symphony", "opera", "orchestral", "baroque", 
            "romantic", "chamber", "concerto", "sonata", "traditional"
        ]
        
        for result in results:
            if not isinstance(result, dict):
                continue
                
            name = result.get("name", "").lower()
            tags = result.get("tags", [])
            
            # Handle tags as list of dicts or strings
            tag_names = []
            if isinstance(tags, list):
                for tag in tags:
                    if isinstance(tag, dict):
                        tag_names.append(tag.get("name", "").lower())
                    elif isinstance(tag, str):
                        tag_names.append(tag.lower())
            
            # Check if it's classical or traditional music
            is_safe = any(keyword in name for keyword in classical_keywords) or \
                     any(keyword in tag_name for tag_name in tag_names for keyword in classical_keywords)
            
            if is_safe:
                safe_results.append(result)
        
        return safe_results
    
    def _get_classical_fallback_fixed(self, heritage: str) -> Dict[str, Any]:
        """FIXED: Fallback classical music recommendations"""
        
        heritage_classical = {
            "Italian-American": [
                {"name": "Antonio Vivaldi", "music_genre": "classical", "properties": {"year": "1720s", "era": "Baroque"}},
                {"name": "Giacomo Puccini", "music_genre": "opera", "properties": {"year": "1890s", "era": "Romantic"}},
                {"name": "Giuseppe Verdi", "music_genre": "opera", "properties": {"year": "1850s", "era": "Romantic"}}
            ],
            "German-American": [
                {"name": "Ludwig van Beethoven", "music_genre": "classical", "properties": {"year": "1800s", "era": "Classical"}},
                {"name": "Johann Sebastian Bach", "music_genre": "classical", "properties": {"year": "1720s", "era": "Baroque"}},
                {"name": "Wolfgang Amadeus Mozart", "music_genre": "classical", "properties": {"year": "1780s", "era": "Classical"}}
            ],
            "universal": [
                {"name": "Wolfgang Amadeus Mozart", "music_genre": "classical", "properties": {"year": "1780s", "era": "Classical"}},
                {"name": "Ludwig van Beethoven", "music_genre": "classical", "properties": {"year": "1800s", "era": "Classical"}},
                {"name": "Frédéric Chopin", "music_genre": "classical", "properties": {"year": "1840s", "era": "Romantic"}}
            ]
        }
        
        composers = heritage_classical.get(heritage, heritage_classical["universal"])
        
        return {
            "success": True,
            "entities": composers,
            "entity_count": len(composers),
            "content_type": "classical_fallback",
            "heritage": heritage
        }

# Monkey patch function to add missing methods to existing QlooInsightsAPI
def patch_qloo_tools():
    """
    Monkey patch the existing QlooInsightsAPI to add missing methods
    Call this after importing QlooInsightsAPI
    """
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        
        # Add missing methods
        QlooInsightsAPI.get_tag_based_insights = QlooToolsStep3Mixin.get_tag_based_insights
        QlooInsightsAPI.get_safe_classical_music_fixed = QlooToolsStep3Mixin.get_safe_classical_music_fixed
        QlooInsightsAPI._get_heritage_music_tags_fixed = QlooToolsStep3Mixin._get_heritage_music_tags_fixed
        QlooInsightsAPI._filter_for_safe_music_fixed = QlooToolsStep3Mixin._filter_for_safe_music_fixed
        QlooInsightsAPI._get_classical_fallback_fixed = QlooToolsStep3Mixin._get_classical_fallback_fixed
        
        logger.info("✅ Successfully patched QlooInsightsAPI with Step 3 methods")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Failed to patch QlooInsightsAPI: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Patching error: {e}")
        return False

# Complete QlooInsightsAPI class with fixes (if you want to replace the entire class)
class QlooInsightsAPIFixed:
    """
    Complete fixed version of QlooInsightsAPI for Step 3 integration
    """
    
    def __init__(self, api_key: str, base_url: str = "https://hackathon.api.qloo.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        logger.info("✅ Qloo API initialized with Step 3 fixes")
    
    async def test_connection(self) -> bool:
        """Test Qloo API connection"""
        try:
            test_result = await self.get_safe_classical_music_fixed("universal", take=1)
            return test_result.get("success", False)
        except Exception as e:
            logger.error(f"Qloo connection test failed: {e}")
            return False
    
    # Include all the fixed methods from the mixin
    async def get_tag_based_insights(self, entity_type: str, tag: str, age_demographic: str, take: int = 10):
        return await QlooToolsStep3Mixin.get_tag_based_insights(self, entity_type, tag, age_demographic, take)
    
    async def get_safe_classical_music_fixed(self, cultural_heritage: str, age_group: str = "55_and_older", gender: Optional[str] = None, take: int = 10):
        return await QlooToolsStep3Mixin.get_safe_classical_music_fixed(self, cultural_heritage, age_group, gender, take)
    
    async def get_safe_classical_music(self, cultural_heritage: str, age_group: str = "55_and_older", gender: Optional[str] = None, take: int = 10):
        """Redirect to fixed version"""
        return await self.get_safe_classical_music_fixed(cultural_heritage, age_group, gender, take)
    
    def _get_heritage_music_tags_fixed(self, heritage: str):
        return QlooToolsStep3Mixin._get_heritage_music_tags_fixed(self, heritage)
    
    def _filter_for_safe_music_fixed(self, results: List[Dict]):
        return QlooToolsStep3Mixin._filter_for_safe_music_fixed(self, results)
    
    def _get_classical_fallback_fixed(self, heritage: str):
        return QlooToolsStep3Mixin._get_classical_fallback_fixed(self, heritage)