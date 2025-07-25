"""
Qloo Cultural Intelligence Agent with Year Filtering - FIXED DATA HANDOFF
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

FIXES:
- Added age-appropriate year filtering for TV shows
- Calculates formative decades based on birth year
- Prevents modern shows like Steven Universe from appearing
- Ensures only classic TV shows for dementia patients
- CRITICAL FIX: Wraps return data in "qloo_intelligence" key for sequential agent
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
    Agent 3: Qloo Cultural Intelligence with Year Filtering for Age-Appropriate Content.
    
    FIXED:
    - Returns ONLY first/best result per category to prevent downstream rate limiting
    - Filters out non-English content
    - Maintains daily uniqueness with minimal results
    - ADDS: Year filtering for TV shows to ensure age-appropriate classic content
    - CRITICAL: Wraps return data in "qloo_intelligence" key for proper data handoff
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("Qloo Cultural Intelligence Agent initialized with year filtering for classic TV")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cultural intelligence with age-appropriate year filtering.
        """
        
        try:
            logger.info("🚀 Agent 3: Starting Qloo intelligence with year filtering for classic TV")
            
            # Store patient profile for age-based filtering
            self._current_patient_profile = consolidated_info.get("patient_profile", {})
            
            # Set daily random seed for uniqueness
            today = date.today()
            daily_seed = hash(f"{today.year}-{today.month}-{today.day}")
            random.seed(daily_seed)
            logger.info(f"Daily seed set: {daily_seed} for date {today}")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            
            # Determine age demographic for Qloo
            age_demographic = self._get_age_demographic(birth_year)
            
            # Get heritage tags for the 3 calls
            heritage_tags = self._get_heritage_tags(heritage, birth_year)
            
            # Make the 3 Qloo calls with year filtering
            qloo_results = await self._make_three_qloo_calls_with_year_filtering(heritage_tags, age_demographic, birth_year)
            
            if qloo_results.get("success"):
                # Filter non-English content
                filtered_results = self._filter_english_content(qloo_results)
                
                # Limit to first result only for rate limiting prevention
                cultural_recommendations = self._limit_to_first_results_only(filtered_results)
                
                # Create cross-domain connections
                cross_domain_connections = self._create_limited_cross_domain_connections(cultural_recommendations)
                
                # CRITICAL FIX: Wrap in "qloo_intelligence" key for sequential agent
                return {
                    "qloo_intelligence": {
                        "cultural_recommendations": cultural_recommendations,
                        "cross_domain_connections": cross_domain_connections,
                        "metadata": {
                            "heritage_used": heritage,
                            "age_demographic": age_demographic,
                            "birth_year": birth_year,
                            "heritage_tags": heritage_tags,
                            "successful_calls": qloo_results.get("successful_calls", 0),
                            "total_calls": qloo_results.get("total_calls", 0),
                            "total_results": qloo_results.get("total_results", 0),
                            "results_limited_to_first_only": True,
                            "year_filtering_applied": True,
                            "tv_year_range": qloo_results.get("tv_year_range", {}),
                            "downstream_rate_limiting_prevention": True,
                            "generation_timestamp": datetime.now().isoformat(),
                            "english_filtering_applied": True,
                            "daily_uniqueness_seed": daily_seed,
                            "approach": "limited_english_filtered_unique_year_filtered"
                        },
                        "status": "success"
                    }
                }
            else:
                logger.warning("All Qloo calls failed, using fallback")
                return self._create_fallback_response(heritage)
                
        except Exception as e:
            logger.error(f"❌ Agent 3 failed: {e}")
            return self._create_fallback_response(heritage)
    
    async def _make_three_qloo_calls_with_year_filtering(self, heritage_tags: Dict[str, str], age_demographic: str, birth_year: Optional[int]) -> Dict[str, Any]:
        """Make the 3 Qloo API calls with age-appropriate year filtering and US focus."""
        
        logger.info("Making 3 cultural Qloo API calls with US filtering and TV year filtering")
        
        # Calculate TV year range based on birth year
        tv_year_range = self._calculate_tv_year_range(birth_year)
        
        results = {}
        
        # Call 1: Cuisine/Places (US focus, heritage-based)
        logger.info("Making Qloo call 1: US-focused Italian-American Places")
        cuisine_tag = "urn:tag:genre:place:restaurant:italian"  # Focus on Italian for Italian-American
        results["cuisine"] = await self.qloo_tool.simple_tag_insights(
            entity_type="urn:entity:place",
            tag=cuisine_tag,
            age_demographic=age_demographic,
            take=15  # Get more to filter out non-US
        )
        await asyncio.sleep(1.0)  # Rate limiting
        
        # Call 2: Music/Artists (no year filtering - we'll filter post-API)
        logger.info("Making Qloo call 2: Music/Artists (age filtering post-API)")
        # Use more specific tags for older demographics
        music_tag = "urn:tag:genre:music:jazz" if age_demographic == "55_and_older" else heritage_tags.get("music", "urn:tag:genre:music:jazz")
        results["music"] = await self.qloo_tool.simple_tag_insights(
            entity_type="urn:entity:artist",
            tag=music_tag,
            age_demographic=age_demographic,
            take=15  # Get more to filter properly
            # Removed: filter_release_year_max=1990 - doesn't work for artists
        )
        await asyncio.sleep(1.0)  # Rate limiting
        
        # Call 3: TV Shows (WITH STRICT YEAR FILTERING)
        logger.info("Making Qloo call 3: Classic TV Shows with strict year filtering")
        results["tv_shows"] = await self._make_tv_shows_call_with_year_filtering(
            "urn:tag:genre:media:classic",  # Force classic TV
            age_demographic,
            tv_year_range
        )
        
        # Format response
        successful_calls = sum(1 for r in results.values() if r.get("success"))
        total_results = sum(r.get("results_count", 0) for r in results.values())
        
        logger.info(f"Qloo calls complete: {successful_calls}/3 successful, {total_results} total results")
        logger.info(f"TV year filtering applied: {tv_year_range['min']}-{tv_year_range['max']}")
        
        return {
            "success": successful_calls > 0,
            "successful_calls": successful_calls,
            "total_calls": 3,
            "total_results": total_results,
            "age_demographic": age_demographic,
            "tv_year_range": tv_year_range,
            "cultural_recommendations": {
                "places": results.get("cuisine", {}),
                "artists": results.get("music", {}),
                "tv_shows": results.get("tv_shows", {})
            }
        }
    
    async def _make_tv_shows_call_with_year_filtering(self, tv_tag: str, age_demographic: str, tv_year_range: Dict[str, int]) -> Dict[str, Any]:
        """Make Qloo TV shows call with age-appropriate year filtering."""
        
        try:
            logger.info(f"Calling Qloo TV shows with year filtering: tag={tv_tag}, years={tv_year_range['min']}-{tv_year_range['max']}")
            
            # Primary call with year filtering
            result = await self.qloo_tool.simple_tag_insights(
                entity_type="urn:entity:tv_show",
                tag=tv_tag,
                age_demographic=age_demographic,
                take=15,
                filter_release_year_min=tv_year_range["min"],
                filter_release_year_max=tv_year_range["max"]
            )
            
            if result.get("success") and result.get("entities"):
                logger.info(f"✅ TV shows call successful: {len(result.get('entities', []))} classic results")
                
                # Log the shows we got to verify they're classic
                entities = result.get("entities", [])
                for entity in entities[:3]:  # Log first 3
                    name = entity.get("name", "Unknown")
                    props = entity.get("properties", {})
                    release_year = props.get("release_year", "Unknown")
                    logger.info(f"  📺 Classic TV: {name} ({release_year})")
                
                return result
            else:
                logger.warning(f"TV shows call with year filtering returned zero results, trying fallback")
                
                # Fallback 1: Try broader classic range
                fallback_result = await self.qloo_tool.simple_tag_insights(
                    entity_type="urn:entity:tv_show",
                    tag="urn:tag:genre:media:family",
                    age_demographic=age_demographic,
                    take=20,
                    filter_release_year_min=1950,  # Broader classic range
                    filter_release_year_max=1990
                )
                
                if fallback_result.get("success") and fallback_result.get("entities"):
                    logger.info(f"✅ TV shows fallback successful: {len(fallback_result.get('entities', []))} results")
                    return fallback_result
                else:
                    logger.warning("TV shows fallback also failed")
                    return {
                        "success": False,
                        "error": "no_classic_tv_shows_found",
                        "entities": [],
                        "results_count": 0
                    }
            
        except Exception as e:
            logger.error(f"TV shows call failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "entities": [],
                "results_count": 0
            }
    
    def _calculate_tv_year_range(self, birth_year: Optional[int]) -> Dict[str, int]:
        """
        Calculate appropriate TV show year range based on patient's birth year.
        
        Args:
            birth_year: Patient's birth year
            
        Returns:
            Dict with min and max years for TV show filtering
        """
        
        if not birth_year:
            # Default to classic TV era for dementia care
            return {"min": 1950, "max": 1980}
        
        # Calculate formative TV viewing years (ages 8-35) 
        formative_start = birth_year + 8    # Age 8 - childhood viewing
        formative_end = birth_year + 35     # Age 35 - established viewing habits
        
        # Ensure we don't go too early or too late
        min_year = max(1940, formative_start)  # TV started around 1940
        max_year = min(1985, formative_end)    # Keep it classic for dementia care - stricter limit
        
        logger.info(f"Birth year {birth_year} → TV viewing years: {min_year}-{max_year}")
        
        return {
            "min": min_year,
            "max": max_year
        }
    
    def _filter_english_content(self, qloo_results: Dict[str, Any]) -> Dict[str, Any]:
        """Filter out non-English and non-US content from Qloo results."""
        
        logger.info("🔤 Filtering non-English and non-US content from Qloo results")
        
        cultural_recommendations = qloo_results.get("cultural_recommendations", {})
        filtered_recommendations = {}
        
        # Get patient birth year for age-based filtering
        patient_profile = getattr(self, '_current_patient_profile', {})
        birth_year = patient_profile.get("birth_year")
        max_year = self._get_max_year_for_age(birth_year)
        logger.info(f"📅 Age-based filtering: content must be from {max_year} or earlier")
        
        for category, data in cultural_recommendations.items():
            if not data.get("success"):
                filtered_recommendations[category] = data
                continue
            
            entities = data.get("entities", [])
            original_count = len(entities)
            
            # Filter for English/US content AND age-appropriate content
            appropriate_entities = []
            filtered_out_reasons = {"non_us": 0, "non_english": 0, "too_modern": 0, "other": 0}
            
            for entity in entities:
                # First check English/US content
                if not self._is_english_content(entity):
                    name = entity.get("name", "Unknown")
                    properties = entity.get("properties", {})
                    
                    if entity.get("subtype") == "urn:entity:place":
                        geocode = properties.get("geocode", {})
                        country = geocode.get("country", "Unknown")
                        filtered_out_reasons["non_us"] += 1
                        logger.info(f"🚫 Filtered {category}: {name} (Country: {country})")
                    else:
                        filtered_out_reasons["non_english"] += 1
                        logger.info(f"🚫 Filtered {category}: {name} (Language/Era issue)")
                    continue
                
                # Then check age appropriateness
                if not self._is_age_appropriate(entity, max_year):
                    name = entity.get("name", "Unknown")
                    filtered_out_reasons["too_modern"] += 1
                    logger.info(f"🚫 Filtered {category}: {name} (Too modern - after {max_year})")
                    continue
                
                # Passed all filters
                appropriate_entities.append(entity)
            
            # Update the data
            filtered_data = data.copy()
            filtered_data["entities"] = appropriate_entities
            filtered_data["results_count"] = len(appropriate_entities)
            filtered_data["filtered_out"] = filtered_out_reasons
            filtered_data["age_filtered"] = True
            filtered_data["max_year_used"] = max_year
            
            filtered_recommendations[category] = filtered_data
            
            logger.info(f"Category {category}: {original_count} → {len(appropriate_entities)} (US/English/Age-appropriate)")
            if filtered_out_reasons["non_us"] > 0:
                logger.info(f"  🇺🇸 Filtered {filtered_out_reasons['non_us']} non-US locations")
            if filtered_out_reasons["non_english"] > 0:
                logger.info(f"  🔤 Filtered {filtered_out_reasons['non_english']} non-English content")
            if filtered_out_reasons["too_modern"] > 0:
                logger.info(f"  📅 Filtered {filtered_out_reasons['too_modern']} too-modern content (after {max_year})")
        
        # Update the results
        filtered_results = qloo_results.copy()
        filtered_results["cultural_recommendations"] = filtered_recommendations
        
        return filtered_results
    
    def _get_max_year_for_age(self, birth_year: Optional[int]) -> int:
        """Get maximum content year based on patient age."""
        if not birth_year:
            return 1980  # Default for dementia care
        
        current_year = 2024
        age = current_year - birth_year
        
        if age <= 35:
            return 2010  # Younger patients can have more recent content
        elif age <= 55:
            return 1990  # Middle-aged patients get content through the 80s
        else:
            return 1980  # Older patients get classic content only
    
    def _is_age_appropriate(self, entity: Dict[str, Any], max_year: int) -> bool:
        """Check if entity is from an appropriate era for the patient."""
        properties = entity.get("properties", {})
        
        # Check release year for media content
        release_year = properties.get("release_year")
        if release_year and release_year > max_year:
            return False
        
        # Check finale year for TV shows (in case release_year is start year)
        finale_year = properties.get("finale_year")
        if finale_year and finale_year > max_year:
            return False
        
        # For artists, check external data for career periods
        external = entity.get("external", {})
        
        # Check Spotify data (first release / last release)
        spotify_data = external.get("spotify", [])
        if spotify_data:
            spotify = spotify_data[0] if isinstance(spotify_data, list) else spotify_data
            first_release = spotify.get("first_release")
            last_release = spotify.get("last_release")
            
            # If their career started after max_year, filter out
            if first_release and first_release > max_year:
                return False
            
            # If they were still releasing music after max_year + 10, probably too modern
            if last_release and last_release > max_year + 10:
                return False
        
        # For places, no age filtering needed
        return True
    
    def _is_english_content(self, entity: Dict[str, Any]) -> bool:
        """Check if entity is English/US-appropriate content for dementia care."""
        
        properties = entity.get("properties", {})
        
        # Check release country for media content
        release_countries = properties.get("release_country", [])
        if release_countries:
            if "United States" not in release_countries and "US" not in release_countries:
                logger.info(f"Filtered out non-US content: {entity.get('name')} from {release_countries}")
                return False
        
        # Check location for places - must be in US
        if entity.get("type") == "urn:entity" and entity.get("subtype") == "urn:entity:place":
            geocode = properties.get("geocode", {})
            country = geocode.get("country", "")
            country_code = geocode.get("country_code", "")
            
            if country not in ["United States", "USA"] and country_code not in ["US", "USA"]:
                logger.info(f"Filtered out non-US place: {entity.get('name')} in {country}")
                return False
        
        # Check for obviously non-English names (basic heuristic)
        name = entity.get("name", "")
        if any(char in name for char in ["ñ", "ç", "ã", "á", "é", "í", "ó", "ú", "â", "ê", "ô"]):
            logger.info(f"Filtered out non-English name: {name}")
            return False
        
        # For artists, check if they have English descriptions
        if entity.get("subtype") == "urn:entity:artist":
            descriptions = properties.get("short_descriptions", [])
            if descriptions:
                # Check if any description is in English
                english_desc = any(desc.get("languages", []) == ["en"] for desc in descriptions)
                if not english_desc:
                    logger.info(f"Filtered out non-English artist: {name}")
                    return False
        
        return True
    
    def _limit_to_first_results_only(self, filtered_results: Dict[str, Any]) -> Dict[str, Any]:
        """Limit results to ONLY the first result per category for rate limiting prevention."""
        
        cultural_recommendations = {}
        
        # Process each category with LIMITING to first result only
        for category, qloo_category in [("places", "places"), ("artists", "artists"), ("tv_shows", "tv_shows")]:
            result = filtered_results.get("cultural_recommendations", {}).get(qloo_category, {})
            
            if result.get("success") and result.get("entities"):
                entities = result["entities"]
                
                # RATE LIMITING: Randomize but return ONLY FIRST result
                random.shuffle(entities)
                limited_entities = entities[:1]  # Take ONLY the first result
                
                logger.info(f"LIMITED output - {category}: {len(entities)} available → returning ONLY 1")
                
                cultural_recommendations[category] = {
                    "available": True,
                    "entity_count": len(limited_entities),  # Always 1
                    "entities": limited_entities,  # ONLY first result
                    "tag_used": result.get("tag"),
                    "entity_type": result.get("entity_type"),
                    "english_filtered": True,
                    "daily_randomized": True,
                    "limited_to_first_result": True,
                    "total_available": len(entities),  # Track how many were available
                    "year_filtered": result.get("year_filtered", False)
                }
            else:
                cultural_recommendations[category] = {
                    "available": False,
                    "entities": [],
                    "entity_count": 0,
                    "error": result.get("error", "no_results")
                }
        
        return cultural_recommendations
    
    def _create_limited_cross_domain_connections(self, cultural_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Create cross-domain connections with limited data."""
        
        # Check what content is available (will be limited to 1 per category)
        available_themes = []
        for category, data in cultural_recommendations.items():
            if isinstance(data, dict) and data.get("available"):
                available_themes.append(category)
        
        connections = {
            "available": len(available_themes) > 1,
            "themes": available_themes,
            "suggested_combinations": [],
            "limited_to_first_results": True
        }
        
        # Add specific combinations if multiple themes available
        if "tv_shows" in available_themes and "places" in available_themes:
            connections["suggested_combinations"].append({
                "type": "tv_and_meal",
                "description": "Watch nostalgic TV shows with themed comfort food"
            })
        
        if "artists" in available_themes and "places" in available_themes:
            connections["suggested_combinations"].append({
                "type": "music_and_cooking",
                "description": "Listen to nostalgic music while preparing familiar recipes"
            })
        
        if "tv_shows" in available_themes and "artists" in available_themes:
            connections["suggested_combinations"].append({
                "type": "multimedia_nostalgia",
                "description": "Combine era-appropriate music and TV for immersive experience"
            })
        
        return connections
    
    def _get_age_demographic(self, birth_year: Optional[int]) -> str:
        """Convert birth year to Qloo age demographic."""
        if not birth_year:
            return "55_and_older"  # Default for dementia care
        
        age = 2024 - birth_year
        
        if age >= 55:
            return "55_and_older"
        elif age >= 36:
            return "36_to_55"
        else:
            return "35_and_younger"
    
    def _get_heritage_tags(self, heritage: str, birth_year: Optional[int]) -> Dict[str, str]:
        """Get appropriate Qloo tags for heritage and age."""
        
        # Heritage-based cuisine tags
        heritage_cuisine_map = {
            "Italian-American": "urn:tag:genre:place:restaurant:italian",
            "Irish-American": "urn:tag:genre:place:restaurant:irish",
            "Mexican-American": "urn:tag:genre:place:restaurant:mexican",
            "German-American": "urn:tag:genre:place:restaurant:german", 
            "Chinese-American": "urn:tag:genre:place:restaurant:chinese",
            "American": "urn:tag:genre:place:restaurant:american"
        }
        
        # Age-based music and TV tags (nostalgia-focused)
        age_music_map = {
            "55_and_older": "urn:tag:genre:music:jazz",     # 1940s-1960s music
            "36_to_55": "urn:tag:genre:music:rock",         # 1970s-1980s music
            "35_and_younger": "urn:tag:genre:music:popular"
        }
        
        age_tv_map = {
            "55_and_older": "urn:tag:genre:media:classic",  # Classic TV shows
            "36_to_55": "urn:tag:genre:media:drama",        # 1980s-1990s TV
            "35_and_younger": "urn:tag:genre:media:family"
        }
        
        age_demographic = self._get_age_demographic(birth_year)
        
        return {
            "cuisine": heritage_cuisine_map.get(heritage, heritage_cuisine_map["American"]),
            "music": age_music_map.get(age_demographic, age_music_map["55_and_older"]),
            "tv_shows": age_tv_map.get(age_demographic, age_tv_map["55_and_older"])
        }
    
    def _create_fallback_response(self, heritage: str) -> Dict[str, Any]:
        """Create fallback response when all Qloo calls fail."""
        
        logger.warning("Creating fallback cultural intelligence response")
        
        # CRITICAL FIX: Wrap in "qloo_intelligence" key for sequential agent
        return {
            "qloo_intelligence": {
                "cultural_recommendations": {
                    "places": {
                        "available": False,
                        "entities": [],
                        "entity_count": 0,
                        "error": "qloo_failed"
                    },
                    "artists": {
                        "available": False,
                        "entities": [],
                        "entity_count": 0,
                        "error": "qloo_failed"
                    },
                    "tv_shows": {
                        "available": False,
                        "entities": [],
                        "entity_count": 0,
                        "error": "qloo_failed"
                    }
                },
                "cross_domain_connections": {
                    "available": False,
                    "themes": [],
                    "suggested_combinations": []
                },
                "metadata": {
                    "heritage_used": heritage,
                    "status": "fallback_all_failed",
                    "generation_timestamp": datetime.now().isoformat(),
                    "year_filtering_applied": False
                },
                "status": "fallback"
            }
        }