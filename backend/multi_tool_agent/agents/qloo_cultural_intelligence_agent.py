"""
Agent 3: Qloo Cultural Intelligence - FIXED LOCATION-ONLY PLACES FILTERING
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

CRITICAL FIX: Location-only places filtering with fallback cities
- No more cuisine/restaurant tags for places
- Uses location from Agent 1 with fallback to major cities
- Gets community buildings, landmarks, museums instead of restaurants
- Maintains same data structure and error handling
"""

import logging
import asyncio
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent:
    """
    Agent 3: Qloo Cultural Intelligence with FIXED Location-Only Places Filtering
    
    CRITICAL FIX: Now gets community buildings by location instead of restaurants by cuisine
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("✅ Qloo Cultural Intelligence Agent initialized with LOCATION-ONLY places filtering")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate enhanced cultural intelligence using FIXED location-only places filtering.
        """
        
        logger.info("🚀 Agent 3: Starting Qloo intelligence with LOCATION-ONLY places filtering")
        
        try:
            # Extract patient profile for dislike checking
            patient_profile = consolidated_info.get("patient_profile", {})
            demo_dislikes = patient_profile.get("demo_dislikes", [])
            
            # Log dislike filtering if any dislikes exist
            if demo_dislikes:
                disliked_types = [dislike.get("type") for dislike in demo_dislikes]
                logger.info(f"🚫 Filtering Qloo recommendations for dislikes: {disliked_types}")
            
            # Extract URN tags from Agent 2 (for music and TV only)
            profile_data = cultural_profile.get("cultural_profile", {})
            qloo_tag_mappings = profile_data.get("qloo_tag_mappings", {})
            
            logger.info(f"🔧 Using URN tags from Agent 2: {qloo_tag_mappings}")
            
            # Get age demographic for local filtering
            birth_year = profile_data.get("cultural_elements", {}).get("birth_year", 1945)
            current_year = datetime.now().year
            age = current_year - birth_year if birth_year else 80
            
            if age >= 55:
                age_demographic = "55_and_older"
            elif age >= 36:
                age_demographic = "36_to_55"
            else:
                age_demographic = "18_to_35"
            
            # Create daily seed for consistent but varied recommendations
            today_str = date.today().isoformat()
            heritage = profile_data.get("cultural_elements", {}).get("heritage", "American")
            daily_seed = hash(f"{today_str}-{heritage}-{age_demographic}")
            random.seed(abs(daily_seed))
            
            logger.info(f"📅 Daily seed set: {daily_seed} for date {today_str}")
            logger.info(f"👤 Age demographic for LOCAL filtering: {age_demographic}")
            
            # Make cultural calls using FIXED location-only places
            cultural_results = await self.enhanced_three_cultural_calls(
                consolidated_info, qloo_tag_mappings, age_demographic, demo_dislikes
            )
            
            # Format final response
            qloo_intelligence = {
                "cultural_recommendations": cultural_results.get("cultural_recommendations", {}),
                "metadata": {
                    "agent": "qloo_cultural_intelligence",
                    "version": "location_only_places_filtering",
                    "approach": cultural_results.get("approach", "location_only_places"),
                    "total_results": cultural_results.get("total_results", 0),
                    "successful_calls": cultural_results.get("successful_calls", 0),
                    "age_demographic": age_demographic,
                    "heritage": heritage,
                    "daily_seed": daily_seed,
                    "music_enhancement": cultural_results.get("metadata", {}).get("music_enhancement", ""),
                    "genres_included": cultural_results.get("metadata", {}).get("genres_included", []),
                    "dislike_filtering_active": len(demo_dislikes) > 0,
                    "location_only_places": True  # Indicates the fix is applied
                }
            }
            
            logger.info(f"✅ FIXED Qloo intelligence complete: {cultural_results.get('successful_calls', 0)}/3 successful")
            
            return {"qloo_intelligence": qloo_intelligence}
            
        except Exception as e:
            logger.error(f"❌ FIXED Qloo intelligence failed: {e}")
            return {"qloo_intelligence": {"error": str(e), "fallback_used": True}}
    
    async def enhanced_three_cultural_calls(self, 
                                          consolidated_info: Dict[str, Any],
                                          qloo_tag_mappings: Dict[str, str], 
                                          age_demographic: str, 
                                          demo_dislikes: List[Dict[str, Any]]):
        """
        Make enhanced cultural calls using FIXED location-only places filtering.
        """
        
        cultural_results = {
            "cultural_recommendations": {},
            "successful_calls": 0,
            "total_results": 0,
            "approach": "location_only_places_filtering",
            "metadata": {
                "music_enhancement": "multi_genre_classical_emphasis",
                "genres_included": []
            }
        }
        
        try:
            # Extract URN tags for music and TV (unchanged)
            music_tag = qloo_tag_mappings.get("music", "urn:tag:genre:music:classical") 
            tv_shows_tag = qloo_tag_mappings.get("tv_shows", "urn:tag:genre:tv:classic")
            
            logger.info(f"🔧 Using URN tags - music: {music_tag}, tv: {tv_shows_tag}")
            
            # FIXED: Places Call with location-only filtering (no cuisine tags)
            if not self._is_content_type_disliked("place", demo_dislikes):
                places_results = await self._places_call_location_only(consolidated_info, age_demographic, demo_dislikes)
                if places_results:
                    cultural_results["cultural_recommendations"]["places"] = places_results
                    cultural_results["successful_calls"] += 1
                    cultural_results["total_results"] += len(places_results.get("entities", []))
            else:
                logger.info("🚫 Skipping places recommendations - user dislikes places")
                cultural_results["cultural_recommendations"]["places"] = {"status": "skipped", "reason": "user_dislike"}
            
            # Music Call (unchanged - still uses URN tags)
            if not self._is_content_type_disliked("music", demo_dislikes):
                music_results = await self._music_call_fixed(music_tag, age_demographic, demo_dislikes)
                if music_results:
                    cultural_results["cultural_recommendations"]["artists"] = music_results
                    cultural_results["successful_calls"] += 1
                    cultural_results["total_results"] += len(music_results.get("entities", []))
                    cultural_results["metadata"]["genres_included"] = music_results.get("genres_used", [])
                    logger.info(f"✅ Stored music data under 'artists' key for Agent 6")
            else:
                logger.info("🚫 Skipping music recommendations - user dislikes music")
                cultural_results["cultural_recommendations"]["artists"] = {"status": "skipped", "reason": "user_dislike"}
            
            # TV Shows Call (unchanged - still uses URN tags)
            if not self._is_content_type_disliked("tv_show", demo_dislikes):
                tv_results = await self._tv_shows_call_fixed(tv_shows_tag, age_demographic, demo_dislikes)
                if tv_results:
                    cultural_results["cultural_recommendations"]["tv_shows"] = tv_results
                    cultural_results["successful_calls"] += 1
                    cultural_results["total_results"] += len(tv_results.get("entities", []))
            else:
                logger.info("🚫 Skipping TV show recommendations - user dislikes TV shows")
                cultural_results["cultural_recommendations"]["tv_shows"] = {"status": "skipped", "reason": "user_dislike"}
            
            return cultural_results
            
        except Exception as e:
            logger.error(f"Error in enhanced cultural calls: {str(e)}")
            return cultural_results
    
    async def _places_call_location_only(self, 
                                       consolidated_info: Dict[str, Any],
                                       age_demographic: str, 
                                       demo_dislikes: List[Dict[str, Any]]):
        """
        FIXED: Location-only places call with fallback cities.
        Gets community buildings, landmarks, museums by location instead of restaurants by cuisine.
        """
        
        try:
            # Extract location from Agent 1
            location_info = consolidated_info.get("location_info", {})
            primary_location = location_info.get("primary_location", "")
            
            # Define fallback cities for demo reliability
            fallback_cities = ["New York City, NY", "Chicago, IL", "Boston, MA", "Los Angeles, CA"]
            
            # Create list of locations to try (actual location first, then fallbacks)
            locations_to_try = [primary_location] + fallback_cities if primary_location else fallback_cities
            
            logger.info(f"🏛️ FIXED: Location-only places search starting with: {locations_to_try[0]}")
            
            # Try each location until we get results
            for location in locations_to_try:
                if not location:  # Skip empty locations
                    continue
                    
                logger.info(f"🔍 Trying location: {location}")
                
                # Use new location-only method from Qloo tools
                places_result = await self.qloo_tool.location_only_insights(
                    "urn:entity:place", 
                    location,
                    age_demographic
                )
                
                if places_result and places_result.get("success"):
                    places_results = places_result.get("entities", [])
                    
                    if len(places_results) > 0:
                        # Filter results by dislikes
                        filtered_results = []
                        for item in places_results:
                            if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                                filtered_results.append(item)
                        
                        logger.info(f"✅ FIXED location-only success: {len(filtered_results)} community places in {location}")
                        
                        return {
                            "entities": filtered_results,
                            "location_used": location,
                            "location_type": "primary" if location == primary_location else "fallback",
                            "available": len(filtered_results) > 0,
                            "entity_count": len(filtered_results),
                            "filtered_count": len(places_results) - len(filtered_results)
                        }
                    else:
                        logger.info(f"⚠️ No places found in {location}, trying next...")
                else:
                    logger.warning(f"❌ Location call failed for {location}")
            
            # If all locations failed
            logger.warning("❌ All location attempts failed for places")
            return None
            
        except Exception as e:
            logger.error(f"FIXED location-only places call error: {str(e)}")
            return None
    
    async def _music_call_fixed(self, music_tag: str, age_demographic: str, demo_dislikes: List[Dict[str, Any]]):
        """FIXED music call using proper URN tags (unchanged)."""
        
        try:
            logger.info(f"🎵 FIXED music call with URN tag: {music_tag}")
            
            # Use the URN tag directly (it's already properly formatted)
            music_result = await self.qloo_tool.simple_tag_insights("urn:entity:artist", music_tag, age_demographic)
            
            if music_result and music_result.get("success"):
                music_results = music_result.get("entities", [])
                
                # Filter results by dislikes
                filtered_results = []
                for item in music_results:
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        filtered_results.append(item)
                
                logger.info(f"✅ FIXED music call success: {len(filtered_results)} results")
                
                return {
                    "entities": filtered_results,
                    "query": music_tag,
                    "genres_used": ["classical"],  # From URN tag
                    "available": len(filtered_results) > 0,
                    "entity_count": len(filtered_results),
                    "filtered_count": len(music_results) - len(filtered_results)
                }
            else:
                logger.warning(f"❌ FIXED music call returned no results for {music_tag}")
            
            return None
            
        except Exception as e:
            logger.error(f"FIXED music call error: {str(e)}")
            return None
    
    async def _tv_shows_call_fixed(self, tv_tag: str, age_demographic: str, demo_dislikes: List[Dict[str, Any]]):
        """FIXED TV shows call using proper URN tags (unchanged)."""
        
        try:
            logger.info(f"📺 FIXED TV call with URN tag: {tv_tag}")
            
            # Use the URN tag directly (it's already properly formatted)
            tv_result = await self.qloo_tool.simple_tag_insights("urn:entity:tv_show", tv_tag, age_demographic)
            
            if tv_result and tv_result.get("success"):
                tv_results = tv_result.get("entities", [])
                
                # Filter results by dislikes
                filtered_results = []
                for item in tv_results:
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        filtered_results.append(item)
                
                logger.info(f"✅ FIXED TV call success: {len(filtered_results)} results")
                
                return {
                    "entities": filtered_results,
                    "query": tv_tag,
                    "available": len(filtered_results) > 0,
                    "entity_count": len(filtered_results),
                    "filtered_count": len(tv_results) - len(filtered_results)
                }
            else:
                logger.warning(f"❌ FIXED TV call returned no results for {tv_tag}")
            
            return None
            
        except Exception as e:
            logger.error(f"FIXED TV call error: {str(e)}")
            return None
    
    def _is_content_type_disliked(self, content_type: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """Check if a content type is generally disliked by the user."""
        for dislike in demo_dislikes:
            if dislike.get("type") == content_type:
                return True
        return False
    
    def _is_specific_item_disliked(self, item_name: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """Check if a specific item name is disliked."""
        item_name_lower = item_name.lower()
        
        for dislike in demo_dislikes:
            dislike_name = dislike.get("name", "").lower()
            
            # Check for exact match or partial match
            if (dislike_name in item_name_lower) or (item_name_lower in dislike_name):
                return True
        
        return False