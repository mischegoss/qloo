"""
Simplified Qloo Tools - REVISED for TV Shows with Year Filtering
File: backend/multi_tool_agent/tools/qloo_tools.py

FIXES:
- Added year filtering parameters for classic TV shows
- filter.release_year.min and filter.release_year.max support
- Prevents modern shows like Steven Universe from appearing
"""

import httpx
import logging
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    Simplified Qloo API tool with year filtering for age-appropriate content.
    
    NEW: Added release year filtering to ensure classic TV shows only.
    """
    
    def __init__(self, api_key: str, base_url: str = "https://hackathon.api.qloo.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        logger.info("Qloo API initialized with year filtering support")
    
    async def simple_tag_insights(self, 
                                 entity_type: str, 
                                 tag: str, 
                                 age_demographic: str,
                                 take: int = 5,
                                 filter_release_year_min: Optional[int] = None,
                                 filter_release_year_max: Optional[int] = None) -> Dict[str, Any]:
        """
        Make a simple Qloo insights call with optional year filtering.
        
        Args:
            entity_type: Qloo entity type (e.g., "urn:entity:tv_show")
            tag: Qloo tag (e.g., "urn:tag:genre:media:classic")
            age_demographic: Age demographic ("55_and_older", "36_to_55", "35_and_younger")
            take: Number of results to return
            filter_release_year_min: Earliest desired release year (e.g., 1950)
            filter_release_year_max: Latest desired release year (e.g., 1980)
            
        Returns:
            Dict with success, entities, and metadata
        """
        
        try:
            # Build base parameters
            params = {
                "filter.type": entity_type,
                "filter.tags": tag,
                "signal.demographics.age": age_demographic,
                "take": take
            }
            
            # Add year filtering if provided
            if filter_release_year_min:
                params["filter.release_year.min"] = filter_release_year_min
                logger.info(f"Added min year filter: {filter_release_year_min}")
                
            if filter_release_year_max:
                params["filter.release_year.max"] = filter_release_year_max
                logger.info(f"Added max year filter: {filter_release_year_max}")
            
            # Log the full request for debugging
            logger.info(f"Qloo API call: {entity_type} + {tag} + {age_demographic}")
            if filter_release_year_min or filter_release_year_max:
                year_range = f"{filter_release_year_min or 'any'}-{filter_release_year_max or 'any'}"
                logger.info(f"Year range: {year_range}")
            
            # Make the API call
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        entities = data.get("results", {}).get("entities", [])
                        logger.info(f"✅ Qloo success: {len(entities)} results for {tag}")
                        
                        # Log year info for TV shows to verify filtering
                        if entity_type == "urn:entity:tv_show" and entities:
                            for entity in entities[:3]:  # Log first 3
                                name = entity.get("name", "Unknown")
                                props = entity.get("properties", {})
                                release_year = props.get("release_year", "Unknown")
                                logger.info(f"  📺 {name} ({release_year})")
                        
                        return {
                            "success": True,
                            "entities": entities,
                            "results_count": len(entities),
                            "tag": tag,
                            "entity_type": entity_type,
                            "year_filtered": bool(filter_release_year_min or filter_release_year_max),
                            "year_range": {
                                "min": filter_release_year_min,
                                "max": filter_release_year_max
                            }
                        }
                    else:
                        logger.warning(f"Qloo API returned success=false for {tag}")
                        return {
                            "success": False,
                            "error": "api_returned_false",
                            "entities": [],
                            "results_count": 0
                        }
                else:
                    logger.error(f"Qloo API error: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"http_error_{response.status_code}",
                        "entities": [],
                        "results_count": 0
                    }
                    
        except httpx.TimeoutException:
            logger.error("Qloo API timeout")
            return {
                "success": False,
                "error": "timeout",
                "entities": [],
                "results_count": 0
            }
        except Exception as e:
            logger.error(f"Qloo API exception: {e}")
            return {
                "success": False,
                "error": str(e),
                "entities": [],
                "results_count": 0
            }
    
    async def three_cultural_calls(self, heritage_tags: Dict[str, str], age_demographic: str) -> Dict[str, Any]:
        """
        Make 3 cultural Qloo API calls with year filtering for TV shows.
        
        UPDATED: Movies → TV Shows with age-appropriate year filtering
        
        Args:
            heritage_tags: Dictionary with cuisine, music, tv_shows tags
            age_demographic: Age demographic string
            
        Returns:
            Structured results from all 3 calls
        """
        logger.info("Making 3 cultural Qloo API calls with year filtering")
        
        # Calculate year range for TV shows based on age demographic
        tv_year_range = self._get_tv_year_range(age_demographic)
        
        # Define the 3 calls we'll make
        calls = [
            {
                "category": "cuisine",
                "entity_type": "urn:entity:place",
                "tag": heritage_tags.get("cuisine", "urn:tag:cuisine:comfort"),
                "year_filter": False  # No year filtering for places
            },
            {
                "category": "music", 
                "entity_type": "urn:entity:artist",
                "tag": heritage_tags.get("music", "urn:tag:genre:music:popular"),
                "year_filter": False  # No year filtering for artists
            },
            {
                "category": "tv_shows",
                "entity_type": "urn:entity:tv_show",
                "tag": heritage_tags.get("tv_shows", "urn:tag:genre:media:family"),
                "year_filter": True,  # Apply year filtering for TV shows
                "year_min": tv_year_range["min"],
                "year_max": tv_year_range["max"]
            }
        ]
        
        results = {}
        
        # Execute all 3 calls
        for call in calls:
            category = call["category"]
            
            # Build call parameters
            call_params = {
                "entity_type": call["entity_type"],
                "tag": call["tag"],
                "age_demographic": age_demographic,
                "take": 10  # Get more for better variety
            }
            
            # Add year filtering for TV shows
            if call.get("year_filter"):
                call_params["filter_release_year_min"] = call["year_min"]
                call_params["filter_release_year_max"] = call["year_max"]
            
            result = await self.simple_tag_insights(**call_params)
            results[category] = result
            
            # Rate limiting between calls
            await asyncio.sleep(1.0)
        
        # Format final response
        successful_calls = sum(1 for r in results.values() if r.get("success"))
        total_results = sum(r.get("results_count", 0) for r in results.values())
        
        logger.info(f"Qloo calls complete: {successful_calls}/3 successful, {total_results} total results")
        
        return {
            "success": successful_calls > 0,
            "successful_calls": successful_calls,
            "total_calls": 3,
            "total_results": total_results,
            "age_demographic": age_demographic,
            "year_filtering_applied": True,
            "tv_year_range": tv_year_range,
            "cultural_recommendations": {
                "places": self._format_category_results(results.get("cuisine", {})),
                "artists": self._format_category_results(results.get("music", {})),
                "tv_shows": self._format_category_results(results.get("tv_shows", {}))
            },
            "metadata": {
                "calls_made": [call["category"] for call in calls],
                "tags_used": [call["tag"] for call in calls],
                "year_filtering": "tv_shows_only"
            }
        }
    
    def _get_tv_year_range(self, age_demographic: str) -> Dict[str, int]:
        """
        Get appropriate year range for TV shows based on age demographic.
        
        Args:
            age_demographic: Qloo age demographic
            
        Returns:
            Dict with min and max years for TV show filtering
        """
        
        # Age-appropriate TV show years (formative viewing years)
        year_ranges = {
            "55_and_older": {  # Ages 55+ (born 1969 or earlier)
                "min": 1950,   # Classic TV era
                "max": 1985    # End of their prime viewing years
            },
            "36_to_55": {     # Ages 36-55 (born 1969-1988)
                "min": 1970,   # Childhood TV
                "max": 2000    # Young adult viewing
            },
            "35_and_younger": {  # Ages 35 and under (born 1989+)
                "min": 1985,   # 80s/90s nostalgia
                "max": 2010    # Early 2000s shows
            }
        }
        
        range_info = year_ranges.get(age_demographic, year_ranges["55_and_older"])
        logger.info(f"TV year range for {age_demographic}: {range_info['min']}-{range_info['max']}")
        
        return range_info
    
    def _format_category_results(self, category_result: Dict[str, Any]) -> Dict[str, Any]:
        """Format results for a single category."""
        
        if not category_result.get("success"):
            return {
                "available": False,
                "error": category_result.get("error", "unknown"),
                "entities": []
            }
        
        entities = category_result.get("entities", [])
        
        # Simple entity formatting
        formatted_entities = []
        for entity in entities:
            formatted_entity = {
                "name": entity.get("name", "Unknown"),
                "entity_id": entity.get("entity_id"),
                "type": entity.get("subtype", "unknown"),
                "properties": entity.get("properties", {}),
                "qloo_source": True
            }
            
            # Add release year info for TV shows
            if entity.get("subtype") == "urn:entity:tv_show":
                props = entity.get("properties", {})
                formatted_entity["release_year"] = props.get("release_year")
                formatted_entity["finale_year"] = props.get("finale_year")
            
            formatted_entities.append(formatted_entity)
        
        return {
            "available": True,
            "entity_count": len(formatted_entities),
            "entities": formatted_entities,
            "tag_used": category_result.get("tag"),
            "entity_type": category_result.get("entity_type"),
            "year_filtered": category_result.get("year_filtered", False)
        }
    
    async def test_connection(self) -> bool:
        """Test if Qloo API is accessible with year filtering."""
        try:
            test_result = await self.simple_tag_insights(
                entity_type="urn:entity:tv_show",
                tag="urn:tag:genre:media:family", 
                age_demographic="55_and_older",
                take=1,
                filter_release_year_min=1950,
                filter_release_year_max=1980
            )
            
            success = test_result.get("success", False)
            logger.info(f"Qloo connection test (with year filtering): {'PASSED' if success else 'FAILED'}")
            return success
            
        except Exception as e:
            logger.error(f"Qloo connection test failed: {e}")
            return False

# Test function for year filtering
async def test_tv_year_filtering():
    """Test TV show year filtering functionality."""
    
    # This would be called in testing/development
    api_key = "your_api_key_here"
    qloo = QlooInsightsAPI(api_key)
    
    # Test different year ranges
    test_cases = [
        {
            "name": "Classic TV (1950-1980)",
            "min_year": 1950,
            "max_year": 1980
        },
        {
            "name": "Modern TV (2000-2020)", 
            "min_year": 2000,
            "max_year": 2020
        },
        {
            "name": "No Year Filter",
            "min_year": None,
            "max_year": None
        }
    ]
    
    for test in test_cases:
        print(f"\n🔍 Testing: {test['name']}")
        
        result = await qloo.simple_tag_insights(
            entity_type="urn:entity:tv_show",
            tag="urn:tag:genre:media:family",
            age_demographic="55_and_older",
            take=5,
            filter_release_year_min=test["min_year"],
            filter_release_year_max=test["max_year"]
        )
        
        if result.get("success"):
            entities = result.get("entities", [])
            print(f"✅ Found {len(entities)} shows:")
            for entity in entities:
                name = entity.get("name", "Unknown")
                props = entity.get("properties", {})
                year = props.get("release_year", "Unknown")
                print(f"  📺 {name} ({year})")
        else:
            print(f"❌ Failed: {result.get('error')}")

# Export the main class
__all__ = ["QlooInsightsAPI"]