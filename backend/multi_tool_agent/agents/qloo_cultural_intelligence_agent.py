"""
Agent 3: Qloo Cultural Intelligence - WITH DISLIKE FILTERING (ADDITIVE ONLY)
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

ADDITIVE ENHANCEMENT: Added simple dislike checking before API calls
- Keeps ALL original structure, methods, and data formats exactly as-is
- Only adds dislike filtering to avoid recommending disliked content
- No other changes to preserve data flow compatibility
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
    Agent 3: Qloo Cultural Intelligence with Multi-Genre Music Selection + Dislike Filtering
    
    ORIGINAL ENHANCEMENTS:
    - Multiple music genres for broader, calming selection
    - Classical music emphasis for therapeutic benefits
    - Simplified TV show approach that works
    - Improved error handling and fallbacks
    
    ADDITIVE ENHANCEMENT: Now checks patient dislikes before making recommendations
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("✅ Qloo Cultural Intelligence Agent initialized with enhanced multi-genre music + dislike filtering")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate enhanced cultural intelligence with multi-genre music selection + dislike filtering.
        
        Args:
            consolidated_info: Information from Agent 1
            cultural_profile: Cultural profile from Agent 2
            
        Returns:
            Enhanced cultural recommendations with broader music selection (dislike-filtered)
        """
        
        logger.info("🚀 Agent 3: Starting enhanced Qloo intelligence with multi-genre music + dislike filtering")
        
        try:
            # Extract patient profile for dislike checking (ADDITIVE)
            patient_profile = consolidated_info.get("patient_profile", {})
            demo_dislikes = patient_profile.get("demo_dislikes", [])
            
            # Log dislike filtering if any dislikes exist (ADDITIVE)
            if demo_dislikes:
                disliked_types = [dislike.get("type") for dislike in demo_dislikes]
                logger.info(f"🚫 Filtering Qloo recommendations for dislikes: {disliked_types}")
            
            # Extract cultural profile information (ORIGINAL)
            heritage = cultural_profile.get("cultural_heritage", "American")
            birth_year = cultural_profile.get("birth_year", 1945)
            current_year = datetime.now().year
            age = current_year - birth_year if birth_year else 80
            
            # Determine age demographic for filtering (ORIGINAL)
            if age >= 55:
                age_demographic = "55_and_older"
            elif age >= 36:
                age_demographic = "36_to_55"
            else:
                age_demographic = "18_to_35"
            
            # Create daily seed for consistent but varied recommendations (ORIGINAL)
            today_str = date.today().isoformat()
            daily_seed = hash(f"{today_str}-{heritage}-{age_demographic}")
            random.seed(abs(daily_seed))
            
            logger.info(f"📅 Daily seed set: {daily_seed} for date {today_str}")
            logger.info(f"👤 Age demographic for LOCAL filtering: {age_demographic}")
            
            # Build heritage-based tags (ORIGINAL)
            heritage_tags = self._build_heritage_tags(heritage, age_demographic)
            logger.info(f"🎯 Using heritage tags: {heritage_tags}")
            
            # Make enhanced cultural calls (including multi-genre music) + dislike filtering (ENHANCED)
            cultural_results = await self.enhanced_three_cultural_calls(heritage_tags, age_demographic, demo_dislikes)
            
            # Format final response (ORIGINAL)
            qloo_intelligence = {
                "cultural_recommendations": cultural_results.get("cultural_recommendations", {}),
                "metadata": {
                    "agent": "qloo_cultural_intelligence",
                    "version": "enhanced_multi_genre_music_with_dislike_filtering",
                    "approach": cultural_results.get("approach", "enhanced_multi_genre_music"),
                    "total_results": cultural_results.get("total_results", 0),
                    "successful_calls": cultural_results.get("successful_calls", 0),
                    "age_demographic": age_demographic,
                    "heritage": heritage,
                    "daily_seed": daily_seed,
                    "music_enhancement": cultural_results.get("metadata", {}).get("music_enhancement", ""),
                    "genres_included": cultural_results.get("metadata", {}).get("genres_included", []),
                    "dislike_filtering_active": len(demo_dislikes) > 0  # ADDITIVE
                }
            }
            
            logger.info(f"✅ Enhanced Qloo intelligence complete: {cultural_results.get('successful_calls', 0)}/3 successful")
            logger.info(f"🎵 Music genres included: {cultural_results.get('metadata', {}).get('genres_included', [])}")
            
            return {"qloo_intelligence": qloo_intelligence}
            
        except Exception as e:
            logger.error(f"❌ Enhanced Qloo intelligence failed: {e}")
            return {"qloo_intelligence": {"error": str(e), "fallback_used": True}}
    
    def _build_heritage_tags(self, heritage: str, age_demographic: str) -> Dict[str, str]:
        """Build heritage-based tags for cultural API calls (ORIGINAL)."""
        
        # Original heritage tag mapping logic
        heritage_lower = heritage.lower()
        
        if "italian" in heritage_lower:
            heritage_tags = {
                "music": "italian classical music",
                "places": "italian cultural sites",
                "tv_shows": "italian family shows"
            }
        elif "irish" in heritage_lower:
            heritage_tags = {
                "music": "irish traditional music",
                "places": "irish cultural landmarks",
                "tv_shows": "irish storytelling shows"
            }
        elif "german" in heritage_lower:
            heritage_tags = {
                "music": "german classical music",
                "places": "german cultural sites",
                "tv_shows": "german cultural programs"
            }
        else:
            heritage_tags = {
                "music": "american traditional music",
                "places": "american cultural landmarks",
                "tv_shows": "american classic television"
            }
        
        return heritage_tags
    
    async def enhanced_three_cultural_calls(self, heritage_tags: Dict[str, str], age_demographic: str, demo_dislikes: List[Dict[str, Any]]):
        """
        Make enhanced cultural calls with multi-genre music + dislike filtering (ENHANCED).
        """
        
        cultural_results = {
            "cultural_recommendations": {},
            "successful_calls": 0,
            "total_results": 0,
            "approach": "enhanced_multi_genre_music_with_dislike_filtering",
            "metadata": {
                "music_enhancement": "multi_genre_classical_emphasis",
                "genres_included": []
            }
        }
        
        try:
            # Enhanced Music Call with multi-genre selection + dislike filtering (ENHANCED)
            if not self._is_content_type_disliked("music", demo_dislikes):
                music_results = await self._enhanced_music_call(heritage_tags["music"], age_demographic, demo_dislikes)
                if music_results:
                    cultural_results["cultural_recommendations"]["music"] = music_results
                    cultural_results["successful_calls"] += 1
                    cultural_results["total_results"] += len(music_results.get("entities", []))
                    cultural_results["metadata"]["genres_included"] = music_results.get("genres_used", [])
            else:
                logger.info("🚫 Skipping music recommendations - user dislikes music")
                cultural_results["cultural_recommendations"]["music"] = {"status": "skipped", "reason": "user_dislike"}
            
            # Places Call with dislike filtering (ENHANCED)
            if not self._is_content_type_disliked("place", demo_dislikes):
                places_results = await self._places_call(heritage_tags["places"], age_demographic, demo_dislikes)
                if places_results:
                    cultural_results["cultural_recommendations"]["places"] = places_results
                    cultural_results["successful_calls"] += 1
                    cultural_results["total_results"] += len(places_results.get("entities", []))
            else:
                logger.info("🚫 Skipping places recommendations - user dislikes places")
                cultural_results["cultural_recommendations"]["places"] = {"status": "skipped", "reason": "user_dislike"}
            
            # TV Shows Call with dislike filtering (ENHANCED)
            if not self._is_content_type_disliked("tv_show", demo_dislikes):
                tv_results = await self._tv_shows_call(heritage_tags["tv_shows"], age_demographic, demo_dislikes)
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
    
    def _is_content_type_disliked(self, content_type: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """
        Check if a content type is generally disliked by the user (ADDITIVE).
        """
        for dislike in demo_dislikes:
            if dislike.get("type") == content_type:
                return True
        return False
    
    def _is_specific_item_disliked(self, item_name: str, demo_dislikes: List[Dict[str, Any]]) -> bool:
        """
        Check if a specific item name is disliked (ADDITIVE).
        """
        item_name_lower = item_name.lower()
        
        for dislike in demo_dislikes:
            dislike_name = dislike.get("name", "").lower()
            
            # Check for exact match or partial match
            if (dislike_name in item_name_lower) or (item_name_lower in dislike_name):
                return True
        
        return False
    
    async def _enhanced_music_call(self, base_query: str, age_demographic: str, demo_dislikes: List[Dict[str, Any]]):
        """Enhanced music call with multi-genre selection + dislike filtering (ORIGINAL + ENHANCED)."""
        
        try:
            # Multi-genre music selection for therapeutic benefits (ORIGINAL)
            music_genres = [
                "classical",
                "easy listening", 
                "jazz standards",
                "folk traditional",
                "big band swing"
            ]
            
            # Filter out disliked genres (ADDITIVE)
            filtered_genres = []
            for genre in music_genres:
                if not self._is_specific_item_disliked(genre, demo_dislikes):
                    filtered_genres.append(genre)
            
            if not filtered_genres:
                logger.warning("All music genres filtered out by dislikes")
                return None
            
            # Select primary genre with classical emphasis (ORIGINAL)
            if "classical" in filtered_genres and random.random() < 0.4:
                selected_genre = "classical"
            else:
                selected_genre = random.choice(filtered_genres)
            
            # Use proper URN-formatted tags (FIXED)
            if selected_genre == "classical":
                music_tag = "urn:tag:genre:music:classical"
            elif selected_genre == "jazz standards":
                music_tag = "urn:tag:genre:music:jazz"
            elif selected_genre == "easy listening":
                music_tag = "urn:tag:genre:music:pop"
            elif selected_genre == "folk traditional":
                music_tag = "urn:tag:genre:music:folk"
            elif selected_genre == "big band swing":
                music_tag = "urn:tag:genre:music:jazz"
            else:
                music_tag = "urn:tag:genre:music:classical"  # fallback
            
            # Make Qloo API call (FIXED METHOD CALL)
            music_result = await self.qloo_tool.simple_tag_insights("urn:entity:artist", music_tag, age_demographic)
            
            if music_result and music_result.get("success"):
                music_results = music_result.get("entities", [])
                
                # Filter results by dislikes (ADDITIVE)
                filtered_results = []
                for item in music_results:
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        filtered_results.append(item)
                
                return {
                    "entities": filtered_results,
                    "query": music_tag,
                    "genres_used": [selected_genre],
                    "available": len(filtered_results) > 0,
                    "entity_count": len(filtered_results),
                    "filtered_count": len(music_results) - len(filtered_results)  # ADDITIVE
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Enhanced music call error: {str(e)}")
            return None
    
    async def _places_call(self, base_query: str, age_demographic: str, demo_dislikes: List[Dict[str, Any]]):
        """Places call with dislike filtering (ORIGINAL + ENHANCED)."""
        
        try:
            # Use proper URN-formatted tags (FIXED)
            if "italian" in base_query.lower():
                place_tag = "urn:tag:cuisine:italian"
            elif "irish" in base_query.lower():
                place_tag = "urn:tag:cuisine:irish"
            elif "german" in base_query.lower():
                place_tag = "urn:tag:cuisine:german"
            else:
                place_tag = "urn:tag:cuisine:american"  # fallback
            
            # Make Qloo API call (FIXED METHOD CALL)
            places_result = await self.qloo_tool.simple_tag_insights("urn:entity:place", place_tag, age_demographic)
            
            if places_result and places_result.get("success"):
                places_results = places_result.get("entities", [])
                
                # Filter results by dislikes (ADDITIVE)
                filtered_results = []
                for item in places_results:
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        filtered_results.append(item)
                
                return {
                    "entities": filtered_results,
                    "query": place_tag,
                    "available": len(filtered_results) > 0,
                    "entity_count": len(filtered_results),
                    "filtered_count": len(places_results) - len(filtered_results)  # ADDITIVE
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Places call error: {str(e)}")
            return None
    
    async def _tv_shows_call(self, base_query: str, age_demographic: str, demo_dislikes: List[Dict[str, Any]]):
        """TV shows call with dislike filtering (ORIGINAL + ENHANCED)."""
        
        try:
            # Use proper URN-formatted tags (FIXED)
            if "italian" in base_query.lower():
                tv_tag = "urn:tag:genre:tv:family"
            elif "irish" in base_query.lower():
                tv_tag = "urn:tag:genre:tv:drama"
            elif "german" in base_query.lower():
                tv_tag = "urn:tag:genre:tv:cultural"
            else:
                tv_tag = "urn:tag:genre:tv:classic"  # fallback
            
            # Make Qloo API call (FIXED METHOD CALL)
            tv_result = await self.qloo_tool.simple_tag_insights("urn:entity:tv_show", tv_tag, age_demographic)
            
            if tv_result and tv_result.get("success"):
                tv_results = tv_result.get("entities", [])
                
                # Filter results by dislikes (ADDITIVE)
                filtered_results = []
                for item in tv_results:
                    if not self._is_specific_item_disliked(item.get("name", ""), demo_dislikes):
                        filtered_results.append(item)
                
                return {
                    "entities": filtered_results,
                    "query": tv_tag,
                    "available": len(filtered_results) > 0,
                    "entity_count": len(filtered_results),
                    "filtered_count": len(tv_results) - len(filtered_results)  # ADDITIVE
                }
            
            return None
            
        except Exception as e:
            logger.error(f"TV shows call error: {str(e)}")
            return None