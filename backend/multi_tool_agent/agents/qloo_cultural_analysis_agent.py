"""
Step 3: Simple Qloo Cultural Analysis Agent
File: backend/multi_tool_agent/agents/qloo_cultural_analysis_agent_simple.py

SIMPLIFIED APPROACH:
- Just get classical artists (no complex heritage mapping)
- Just get restaurants for recipe inspiration (simple cuisine calls)
- Minimal parameters, maximum results
- Clean fallbacks when API calls don't work
"""

import logging
import asyncio
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class QlooCulturalAnalysisAgent:
    """
    Step 3: Simple Qloo Cultural Analysis Agent
    
    Makes TWO simple Qloo API calls:
    - Artists: Just get classical music artists
    - Places: Just get restaurants for recipe inspiration
    
    No overcomplicated parameters or heritage mappings.
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("✅ Step 3: Simple Qloo Cultural Analysis Agent initialized")
    
    async def run(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Generate cultural intelligence using simple Qloo API calls
        
        Args:
            enhanced_profile: Complete profile from Steps 1-2
            
        Returns:
            Enhanced profile with cultural intelligence data
        """
        
        logger.info("🚀 Step 3: Starting Simple Qloo Cultural Analysis")
        
        try:
            # Extract basic data
            patient_info = enhanced_profile.get("patient_info", {})
            cultural_heritage = patient_info.get("cultural_heritage") or "American"
            birth_year = patient_info.get("birth_year") or 1945
            demo_dislikes = patient_info.get("demo_dislikes", [])
            
            logger.info(f"🎯 Cultural heritage: {cultural_heritage}")
            logger.info(f"🎯 Birth year: {birth_year}")
            
            # Set daily seed for consistency
            today_str = date.today().isoformat()
            daily_seed = hash(f"{today_str}-{cultural_heritage}-{birth_year}")
            random.seed(abs(daily_seed))
            
            # Get age demographic 
            age_demographic = self._get_age_demographic(birth_year)
            
            # Make simple Qloo cultural calls
            cultural_intelligence = await self._make_simple_cultural_calls(
                cultural_heritage, age_demographic, demo_dislikes
            )
            
            # Enhance profile with cultural intelligence
            enhanced_profile_with_culture = self._enhance_profile_with_cultural_intelligence(
                enhanced_profile, cultural_intelligence
            )
            
            logger.info("✅ Step 3: Simple Qloo cultural analysis completed")
            
            return enhanced_profile_with_culture
            
        except Exception as e:
            logger.error(f"❌ Step 3 failed: {e}")
            return self._create_fallback_enhanced_profile(enhanced_profile)
    
    def _get_age_demographic(self, birth_year: int) -> str:
        """Get age demographic for recommendations"""
        
        current_year = datetime.now().year
        age = current_year - birth_year if birth_year else 80
        
        if age >= 55:
            return "55_and_older"
        elif age >= 36:
            return "36_to_55"
        else:
            return "18_to_35"
    
    async def _make_simple_cultural_calls(self, 
                                        cultural_heritage: str,
                                        age_demographic: str, 
                                        demo_dislikes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Make simple Qloo API calls for artists and restaurants
        
        Returns:
            Cultural intelligence data with artists and places
        """
        
        logger.info("🎵🍽️ Making simple Qloo calls: Artists + Restaurants")
        
        cultural_results = {
            "cultural_recommendations": {},
            "successful_calls": 0,
            "total_results": 0,
            "metadata": {
                "approach": "simple_qloo_calls",
                "heritage": cultural_heritage,
                "age_demographic": age_demographic
            }
        }
        
        # Call 1: Simple classical artists
        if not self._is_content_type_disliked("music", demo_dislikes):
            artists_result = await self._get_simple_classical_artists()
            if artists_result and artists_result.get("success"):
                cultural_results["cultural_recommendations"]["artists"] = artists_result
                cultural_results["successful_calls"] += 1
                cultural_results["total_results"] += len(artists_result.get("entities", []))
                logger.info(f"✅ Artists call: {len(artists_result.get('entities', []))} results")
            else:
                logger.warning("⚠️ Artists call failed, using fallback")
                cultural_results["cultural_recommendations"]["artists"] = self._get_fallback_artists()
        else:
            logger.info("🚫 Skipping music - user dislikes")
            cultural_results["cultural_recommendations"]["artists"] = {"status": "skipped", "reason": "user_dislike"}
        
        # Call 2: Simple restaurants for recipe inspiration
        if not self._is_content_type_disliked("food", demo_dislikes):
            places_result = await self._get_simple_restaurants(cultural_heritage)
            if places_result and places_result.get("success"):
                cultural_results["cultural_recommendations"]["places"] = places_result
                cultural_results["successful_calls"] += 1
                cultural_results["total_results"] += len(places_result.get("entities", []))
                logger.info(f"✅ Places call: {len(places_result.get('entities', []))} results")
            else:
                logger.warning("⚠️ Places call failed, using fallback")
                cultural_results["cultural_recommendations"]["places"] = self._get_fallback_places(cultural_heritage)
        else:
            logger.info("🚫 Skipping cuisine - user dislikes")
            cultural_results["cultural_recommendations"]["places"] = {"status": "skipped", "reason": "user_dislike"}
        
        logger.info(f"🎯 Simple cultural calls completed: {cultural_results['successful_calls']}/2 successful")
        
        return cultural_results
    
    async def _get_simple_classical_artists(self) -> Dict[str, Any]:
        """Get classical artists using simple Qloo API call"""
        
        # Check if Qloo tool is available
        if not self.qloo_tool:
            logger.info("🔄 No Qloo tool available, skipping artists API call")
            return {"success": False, "error": "No Qloo tool available"}
        
        try:
            # Make SIMPLE direct API call for classical artists
            import httpx
            
            # Minimal parameters - just get classical artists
            params = {
                "filter.type": "urn:entity:artist",
                "signal.interests.tags": "classical",  # Just one simple tag
                "take": 10
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.qloo_tool.base_url}/v2/insights",
                    params=params,
                    headers=self.qloo_tool.headers
                )
                
                logger.info(f"🎵 Classical artists API call: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("results", [])
                    
                    if entities and len(entities) > 0:
                        logger.info(f"✅ Found {len(entities)} classical artists")
                        return {
                            "success": True,
                            "available": True,
                            "entities": entities,
                            "entity_count": len(entities),
                            "method": "simple_qloo_api"
                        }
                    else:
                        logger.info("📝 No classical artists found, trying fallback")
                        return {"success": False, "error": "No classical artists found"}
                else:
                    logger.warning(f"⚠️ Classical artists API error: {response.status_code}")
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"❌ Classical artists call failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _get_simple_restaurants(self, cultural_heritage: str) -> Dict[str, Any]:
        """Get restaurants using simple Qloo API call for recipe inspiration"""
        
        # Check if Qloo tool is available
        if not self.qloo_tool:
            logger.info("🔄 No Qloo tool available, skipping places API call")
            return {"success": False, "error": "No Qloo tool available"}
        
        try:
            # Simple cuisine mapping for recipe inspiration
            simple_cuisine_map = {
                "Italian-American": "italian",
                "Italian": "italian",
                "Irish-American": "irish",
                "Irish": "irish", 
                "Mexican-American": "mexican",
                "Mexican": "mexican",
                "Chinese-American": "chinese",
                "Chinese": "chinese",
                "German-American": "german",
                "German": "german"
            }
            
            # Get simple cuisine tag or default to "restaurant"
            cuisine_tag = simple_cuisine_map.get(cultural_heritage, "restaurant")
            
            logger.info(f"🍽️ Using simple cuisine tag: {cuisine_tag} for heritage: {cultural_heritage}")
            
            # Make SIMPLE direct API call for places
            import httpx
            
            # Minimal parameters - just get restaurants
            params = {
                "filter.type": "urn:entity:place",
                "signal.interests.tags": cuisine_tag,  # Simple cuisine tag
                "take": 10
            }
            
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.qloo_tool.base_url}/v2/insights",
                    params=params,
                    headers=self.qloo_tool.headers
                )
                
                logger.info(f"🍽️ Restaurants API call: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("results", [])
                    
                    if entities and len(entities) > 0:
                        logger.info(f"✅ Found {len(entities)} restaurants")
                        return {
                            "success": True,
                            "available": True,
                            "entities": entities,
                            "entity_count": len(entities),
                            "method": "simple_qloo_api",
                            "cuisine_tag": cuisine_tag,
                            "heritage": cultural_heritage
                        }
                    else:
                        logger.info("📝 No restaurants found, trying fallback")
                        return {"success": False, "error": "No restaurants found"}
                else:
                    logger.warning(f"⚠️ Restaurants API error: {response.status_code}")
                    return {"success": False, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            logger.error(f"❌ Restaurants call failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _is_content_type_disliked(self, content_type: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """Check if user has disliked this content type"""
        
        for dislike in demo_dislikes:
            if dislike.get("type") == content_type:
                return True
        return False
    
    def _get_fallback_artists(self) -> Dict[str, Any]:
        """Get fallback classical artists when API fails"""
        
        fallback_artists = [
            {"name": "Wolfgang Amadeus Mozart", "music_genre": "classical", "properties": {"year": "1780s"}},
            {"name": "Ludwig van Beethoven", "music_genre": "classical", "properties": {"year": "1800s"}},
            {"name": "Johann Sebastian Bach", "music_genre": "classical", "properties": {"year": "1720s"}},
            {"name": "Frédéric Chopin", "music_genre": "classical", "properties": {"year": "1840s"}},
            {"name": "Antonio Vivaldi", "music_genre": "classical", "properties": {"year": "1720s"}}
        ]
        
        return {
            "success": True,
            "available": True,
            "entities": fallback_artists,
            "entity_count": len(fallback_artists),
            "method": "fallback"
        }
    
    def _get_fallback_places(self, cultural_heritage: str) -> Dict[str, Any]:
        """Get fallback restaurants when API fails"""
        
        # Heritage-specific fallbacks for recipe inspiration
        heritage_fallbacks = {
            "Italian-American": [
                {"name": "Traditional Italian Restaurant", "properties": {"cuisine": "Italian", "specialties": ["pasta", "pizza"]}},
                {"name": "Family Italian Bistro", "properties": {"cuisine": "Italian", "specialties": ["marinara", "garlic bread"]}}
            ],
            "Irish-American": [
                {"name": "Irish Pub & Eatery", "properties": {"cuisine": "Irish", "specialties": ["shepherd's pie", "soda bread"]}},
                {"name": "Traditional Irish Kitchen", "properties": {"cuisine": "Irish", "specialties": ["corned beef", "cabbage"]}}
            ],
            "Mexican-American": [
                {"name": "Traditional Mexican Restaurant", "properties": {"cuisine": "Mexican", "specialties": ["tacos", "enchiladas"]}},
                {"name": "Family Mexican Kitchen", "properties": {"cuisine": "Mexican", "specialties": ["beans", "rice"]}}
            ]
        }
        
        # Get heritage-specific or default American
        fallback_restaurants = heritage_fallbacks.get(cultural_heritage, [
            {"name": "American Family Restaurant", "properties": {"cuisine": "American", "specialties": ["comfort food", "home cooking"]}},
            {"name": "Classic American Diner", "properties": {"cuisine": "American", "specialties": ["meatloaf", "apple pie"]}}
        ])
        
        return {
            "success": True,
            "available": True,
            "entities": fallback_restaurants,
            "entity_count": len(fallback_restaurants),
            "method": "fallback",
            "heritage": cultural_heritage
        }
    
    def _enhance_profile_with_cultural_intelligence(self, 
                                                  enhanced_profile: Dict[str, Any],
                                                  cultural_intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Add cultural intelligence data to enhanced profile"""
        
        enhanced_profile["cultural_intelligence"] = {
            "cultural_recommendations": cultural_intelligence.get("cultural_recommendations", {}),
            "metadata": {
                **cultural_intelligence.get("metadata", {}),
                "agent": "simple_qloo_cultural_analysis",
                "step": 3,
                "timestamp": datetime.now().isoformat(),
                "successful_calls": cultural_intelligence.get("successful_calls", 0),
                "total_results": cultural_intelligence.get("total_results", 0),
                "qloo_tool_available": self.qloo_tool is not None,
                "approach": "simple_qloo_calls"
            }
        }
        
        # Update pipeline state
        enhanced_profile["pipeline_state"] = {
            "current_step": 3,
            "next_step": 4,
            "step_name": "simple_qloo_cultural_analysis",
            "completion_time": datetime.now().isoformat(),
            "ready_for_step4": True
        }
        
        return enhanced_profile
    
    def _create_fallback_enhanced_profile(self, enhanced_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback profile when Step 3 fails completely"""
        
        logger.warning("🔄 Creating Step 3 fallback profile")
        
        # Extract basic info for fallback
        patient_info = enhanced_profile.get("patient_info", {})
        cultural_heritage = patient_info.get("cultural_heritage") or "American"
        
        # Create emergency cultural intelligence
        fallback_cultural_intelligence = {
            "cultural_recommendations": {
                "artists": self._get_fallback_artists(),
                "places": self._get_fallback_places(cultural_heritage)
            },
            "metadata": {
                "agent": "simple_qloo_cultural_analysis",
                "step": 3,
                "method": "emergency_fallback",
                "timestamp": datetime.now().isoformat(),
                "successful_calls": 0,
                "total_results": 10,  # From fallback data
                "qloo_tool_available": self.qloo_tool is not None,
                "approach": "emergency_fallback",
                "heritage": cultural_heritage
            }
        }
        
        enhanced_profile["cultural_intelligence"] = fallback_cultural_intelligence
        
        # Update pipeline state
        enhanced_profile["pipeline_state"] = {
            "current_step": 3,
            "next_step": 4,
            "step_name": "simple_qloo_cultural_analysis",
            "completion_time": datetime.now().isoformat(),
            "ready_for_step4": True,
            "fallback_used": True
        }
        
        return enhanced_profile