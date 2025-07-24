"""
Qloo Cultural Intelligence Agent - English Filtering + Daily Uniqueness
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

Agent 3: Filters non-English content and ensures daily unique results
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
    Agent 3: Qloo Cultural Intelligence with English Filtering + Daily Uniqueness
    
    Filters out non-English multilingual data and ensures unique results per day.
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("Qloo Cultural Intelligence Agent initialized with English filtering")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cultural intelligence with English filtering and daily uniqueness.
        """
        
        try:
            logger.info("🚀 Agent 3: Starting Qloo intelligence with English filtering")
            
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
            
            # Make the 3 Qloo calls
            qloo_results = await self._make_three_qloo_calls(heritage_tags, age_demographic)
            
            # FILTER ENGLISH ONLY before processing
            filtered_results = self._filter_english_only(qloo_results)
            
            # Process and format results with daily uniqueness
            cultural_recommendations = self._process_qloo_results_with_uniqueness(filtered_results)
            
            # Create cross-domain connections
            cross_domain_connections = self._create_cross_domain_connections(cultural_recommendations)
            
            return {
                "qloo_intelligence": {
                    "cultural_recommendations": cultural_recommendations,
                    "metadata": {
                        "heritage_used": heritage,
                        "age_demographic": age_demographic,
                        "heritage_tags": heritage_tags,
                        "successful_calls": sum(1 for r in filtered_results.values() if r.get("success")),
                        "total_calls": 3,
                        "total_results": sum(r.get("results_count", 0) for r in filtered_results.values()),
                        "generation_timestamp": datetime.now().isoformat(),
                        "english_filtering_applied": True,
                        "daily_uniqueness_seed": daily_seed,
                        "approach": "english_filtered_unique"
                    },
                    "cross_domain_connections": cross_domain_connections,
                    "status": "success"
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Agent 3 failed: {e}")
            return self._create_fallback_response(
                consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
            )
    
    def _filter_english_only(self, qloo_results: Dict[str, Any]) -> Dict[str, Any]:
        """Filter out non-English content from Qloo results."""
        
        logger.info("🔤 Filtering non-English content from Qloo results")
        filtered_results = {}
        
        for category, result in qloo_results.items():
            if not result.get("success") or not result.get("entities"):
                filtered_results[category] = result
                continue
            
            # Filter entities for English content
            english_entities = []
            for entity in result.get("entities", []):
                filtered_entity = self._filter_entity_english(entity)
                if filtered_entity:
                    english_entities.append(filtered_entity)
            
            # Update result with filtered entities
            filtered_result = result.copy()
            filtered_result["entities"] = english_entities
            filtered_result["results_count"] = len(english_entities)
            
            filtered_results[category] = filtered_result
            
            logger.info(f"Category {category}: {len(result.get('entities', []))} → {len(english_entities)} (English only)")
        
        return filtered_results
    
    def _filter_entity_english(self, entity: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Filter a single entity to keep only English content."""
        
        # Always keep the entity, but clean up non-English fields
        filtered_entity = {
            "name": entity.get("name", "Unknown"),
            "entity_id": entity.get("entity_id"),
            "type": entity.get("subtype", "unknown"),  
            "qloo_source": True
        }
        
        # Filter properties to English only
        properties = entity.get("properties", {})
        if properties:
            filtered_properties = {}
            
            # Keep basic properties (always in English)
            english_fields = [
                "description", "address", "website", "phone", "business_rating",
                "release_year", "finale_year", "content_rating", "duration",
                "date_of_birth", "place_of_birth", "year_of_death"
            ]
            
            for field in english_fields:
                if field in properties:
                    filtered_properties[field] = properties[field]
            
            # Filter multilingual fields to English only
            if "akas" in properties:
                english_akas = []
                for aka in properties["akas"]:
                    if isinstance(aka, dict) and aka.get("languages"):
                        if "en" in aka.get("languages", []):
                            english_akas.append({
                                "value": aka.get("value"),
                                "languages": ["en"]
                            })
                
                if english_akas:
                    filtered_properties["akas"] = english_akas[:3]  # Max 3 English aliases
            
            # Filter short descriptions to English only
            if "short_descriptions" in properties:
                english_descriptions = []
                for desc in properties["short_descriptions"]:
                    if isinstance(desc, dict) and desc.get("languages"):
                        if "en" in desc.get("languages", []):
                            english_descriptions.append(desc)
                
                if english_descriptions:
                    filtered_properties["short_descriptions"] = english_descriptions[:1]  # Just 1 description
            
            # Keep image if present
            if "image" in properties:
                filtered_properties["image"] = properties["image"]
            
            filtered_entity["properties"] = filtered_properties
        
        return filtered_entity
    
    def _process_qloo_results_with_uniqueness(self, filtered_results: Dict[str, Any]) -> Dict[str, Any]:
        """Process filtered results with daily uniqueness randomization."""
        
        cultural_recommendations = {}
        
        # Process each category with randomization
        for category, qloo_category in [("places", "cuisine"), ("artists", "music"), ("tv_shows", "tv_shows")]:
            result = filtered_results.get(qloo_category, {})
            
            if result.get("success") and result.get("entities"):
                entities = result["entities"]
                
                # Randomize the order for daily uniqueness
                random.shuffle(entities)
                logger.info(f"Randomized {len(entities)} {category} for daily uniqueness")
                
                cultural_recommendations[category] = {
                    "available": True,
                    "entity_count": len(entities),
                    "entities": entities,  # Already randomized for uniqueness
                    "tag_used": result.get("tag"),
                    "entity_type": result.get("entity_type"),
                    "english_filtered": True,
                    "daily_randomized": True
                }
            else:
                cultural_recommendations[category] = {
                    "available": False,
                    "entities": [],
                    "entity_count": 0,
                    "error": result.get("error", "no_results")
                }
        
        return cultural_recommendations
    
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
            "55_and_older": "urn:tag:genre:music:jazz",  # 1940s-1960s music
            "36_to_55": "urn:tag:genre:music:rock",      # 1970s-1980s music
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
    
    async def _make_three_qloo_calls(self, heritage_tags: Dict[str, str], age_demographic: str) -> Dict[str, Any]:
        """Make the 3 Qloo API calls with relaxed parameters."""
        
        results = {}
        
        # Call 1: Cuisine (Places)
        logger.info("Making Qloo call 1: Cuisine/Places")
        results["cuisine"] = await self._call_qloo_places(heritage_tags["cuisine"], age_demographic)
        await asyncio.sleep(1.0)  # Rate limiting
        
        # Call 2: Music (Artists)
        logger.info("Making Qloo call 2: Music/Artists")
        results["music"] = await self._call_qloo_artists(heritage_tags["music"], age_demographic)
        await asyncio.sleep(1.0)  # Rate limiting
        
        # Call 3: TV Shows (Relaxed parameters)
        logger.info("Making Qloo call 3: TV Shows (relaxed)")
        results["tv_shows"] = await self._call_qloo_tv_shows_relaxed(heritage_tags["tv_shows"], age_demographic)
        
        return results
    
    async def _call_qloo_places(self, cuisine_tag: str, age_demographic: str) -> Dict[str, Any]:
        """Call Qloo for cuisine/places recommendations."""
        try:
            result = await self.qloo_tool.simple_tag_insights(
                entity_type="urn:entity:place",
                tag=cuisine_tag,
                age_demographic=age_demographic,
                take=10  # Get more, will filter to English and randomize
            )
            return result
        except Exception as e:
            logger.error(f"Qloo places call failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _call_qloo_artists(self, music_tag: str, age_demographic: str) -> Dict[str, Any]:
        """Call Qloo for music/artists recommendations."""
        try:
            result = await self.qloo_tool.simple_tag_insights(
                entity_type="urn:entity:artist",
                tag=music_tag,
                age_demographic=age_demographic,
                take=10  # Get more, will filter to English and randomize
            )
            return result
        except Exception as e:
            logger.error(f"Qloo artists call failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _call_qloo_tv_shows_relaxed(self, tv_tag: str, age_demographic: str) -> Dict[str, Any]:
        """Call Qloo for TV shows with relaxed parameters."""
        try:
            logger.info(f"Calling Qloo TV shows: tag={tv_tag}")
            
            result = await self.qloo_tool.simple_tag_insights(
                entity_type="urn:entity:tv_show",
                tag=tv_tag,
                age_demographic=age_demographic,
                take=15,  # Get more for better English filtering + uniqueness
            )
            
            if result.get("success") and result.get("entities"):
                logger.info(f"✅ TV shows call successful: {len(result.get('entities', []))} results")
            else:
                logger.warning("TV shows call returned zero results, trying fallback")
                # Try more relaxed fallback
                result = await self.qloo_tool.simple_tag_insights(
                    entity_type="urn:entity:tv_show",
                    tag="urn:tag:genre:media:family",  # Very broad category
                    age_demographic=age_demographic,
                    take=20
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Qloo TV shows call failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_cross_domain_connections(self, cultural_recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """Create cross-domain connections between different categories."""
        
        # Check what content is available
        available_themes = []
        for category, data in cultural_recommendations.items():
            if isinstance(data, dict) and data.get("available"):
                available_themes.append(category)
        
        connections = {
            "available": len(available_themes) > 1,
            "themes": available_themes,
            "suggested_combinations": []
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
    
    def _create_fallback_response(self, heritage: str) -> Dict[str, Any]:
        """Create fallback response when all Qloo calls fail."""
        
        logger.warning("Creating fallback response for Qloo Cultural Intelligence")
        
        return {
            "qloo_intelligence": {
                "cultural_recommendations": {
                    "places": {"available": False, "entities": [], "entity_count": 0},
                    "artists": {"available": False, "entities": [], "entity_count": 0},
                    "tv_shows": {"available": False, "entities": [], "entity_count": 0}
                },
                "metadata": {
                    "heritage_used": heritage,
                    "successful_calls": 0,
                    "total_calls": 0,
                    "total_results": 0,
                    "english_filtering_applied": True,
                    "approach": "complete_fallback",
                    "status": "fallback"
                },
                "cross_domain_connections": {"available": False},
                "status": "fallback"
            }
        }