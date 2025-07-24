"""
Simplified Qloo Tools - REVISED for TV Shows
File: backend/multi_tool_agent/tools/qloo_tools.py

Drastically simplified Qloo API integration focused on tag-based insights only.
UPDATED: Changed from movies to TV shows throughout.
Removes all complex entity searching, multi-signal logic, and error-prone patterns.
"""

import httpx
import logging
from typing import Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    Simplified Qloo API tool focused on reliable tag-based insights.
    UPDATED: Movies → TV Shows
    
    REMOVED COMPLEXITY:
    - Entity searching logic
    - Multi-signal parameter building  
    - Keyword extraction complexity
    - Fallback strategies
    - Caching complexity
    
    KEPT SIMPLE:
    - Direct tag-based insights
    - Basic demographic mapping
    - Simple result formatting
    """
    
    def __init__(self, api_key: str, base_url: str = "https://hackathon.api.qloo.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        logger.info("Simplified Qloo API initialized")
    
    async def simple_tag_insights(self, 
                                 entity_type: str, 
                                 tag: str, 
                                 age_demographic: str,
                                 take: int = 5) -> Dict[str, Any]:
        """
        Make a single, simple Qloo insights call using tags and demographics.
        
        Args:
            entity_type: Qloo entity type (e.g., "urn:entity:place", "urn:entity:tv_show")
            tag: Qloo tag (e.g., "urn:tag:cuisine:italian")  
            age_demographic: Age demographic (e.g., "55_and_older")
            take: Number of results to return
            
        Returns:
            Simple results dictionary
        """
        try:
            logger.info(f"Qloo API call: {entity_type} + {tag} + {age_demographic}")
            
            params = {
                "filter.type": entity_type,
                "filter.tags": tag,
                "signal.demographics.age": age_demographic,
                "take": take
            }
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("results", {}).get("entities", [])
                    
                    logger.info(f"✅ Qloo success: {len(entities)} results for {tag}")
                    
                    return {
                        "success": True,
                        "entity_type": entity_type,
                        "tag": tag,
                        "results_count": len(entities),
                        "entities": entities[:take],  # Ensure we don't exceed limit
                        "metadata": {
                            "age_demographic": age_demographic,
                            "api_call_successful": True
                        }
                    }
                
                else:
                    logger.warning(f"❌ Qloo API error {response.status_code} for {tag}")
                    return {
                        "success": False,
                        "entity_type": entity_type,
                        "tag": tag,
                        "error": f"http_{response.status_code}",
                        "results_count": 0,
                        "entities": []
                    }
        
        except Exception as e:
            logger.error(f"❌ Qloo API exception for {tag}: {e}")
            return {
                "success": False,
                "entity_type": entity_type,
                "tag": tag,
                "error": "exception",
                "results_count": 0,
                "entities": []
            }
    
    async def make_three_cultural_calls(self, 
                                      heritage_tags: Dict[str, str],
                                      age_demographic: str) -> Dict[str, Any]:
        """
        Make exactly 3 simple Qloo calls for cultural recommendations.
        UPDATED: Movies → TV Shows
        
        Args:
            heritage_tags: Dictionary with cuisine, music, tv_shows tags
            age_demographic: Age demographic string
            
        Returns:
            Structured results from all 3 calls
        """
        logger.info("Making 3 cultural Qloo API calls")
        
        # Define the 3 calls we'll make - UPDATED FOR TV SHOWS
        calls = [
            {
                "category": "cuisine",
                "entity_type": "urn:entity:place",
                "tag": heritage_tags.get("cuisine", "urn:tag:cuisine:comfort")
            },
            {
                "category": "music", 
                "entity_type": "urn:entity:artist",
                "tag": heritage_tags.get("music", "urn:tag:genre:music:popular")
            },
            {
                "category": "tv_shows",  # CHANGED: movies → tv_shows
                "entity_type": "urn:entity:tv_show",  # CHANGED: movie → tv_show
                "tag": heritage_tags.get("tv_shows", "urn:tag:genre:media:family")  # CHANGED: movies → tv_shows
            }
        ]
        
        results = {}
        
        # Execute all 3 calls
        for call in calls:
            category = call["category"]
            
            result = await self.simple_tag_insights(
                entity_type=call["entity_type"],
                tag=call["tag"],
                age_demographic=age_demographic,
                take=5
            )
            
            results[category] = result
            
            # Rate limiting between calls
            await asyncio.sleep(1.0)
        
        # Format final response - UPDATED FOR TV SHOWS
        successful_calls = sum(1 for r in results.values() if r.get("success"))
        total_results = sum(r.get("results_count", 0) for r in results.values())
        
        logger.info(f"Qloo calls complete: {successful_calls}/3 successful, {total_results} total results")
        
        return {
            "success": successful_calls > 0,
            "successful_calls": successful_calls,
            "total_calls": 3,
            "total_results": total_results,
            "age_demographic": age_demographic,
            "cultural_recommendations": {
                "places": self._format_category_results(results.get("cuisine", {})),
                "artists": self._format_category_results(results.get("music", {})),
                "tv_shows": self._format_category_results(results.get("tv_shows", {}))  # CHANGED: movies → tv_shows
            },
            "metadata": {
                "calls_made": [call["category"] for call in calls],
                "tags_used": [call["tag"] for call in calls]
            }
        }
    
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
            formatted_entities.append({
                "name": entity.get("name", "Unknown"),
                "entity_id": entity.get("entity_id"),
                "type": entity.get("subtype", "unknown"),
                "properties": entity.get("properties", {}),
                "qloo_source": True
            })
        
        return {
            "available": True,
            "entity_count": len(formatted_entities),
            "entities": formatted_entities,
            "tag_used": category_result.get("tag"),
            "entity_type": category_result.get("entity_type")
        }
    
    async def test_connection(self) -> bool:
        """Test if Qloo API is accessible."""
        try:
            test_result = await self.simple_tag_insights(
                entity_type="urn:entity:tv_show",  # CHANGED: movie → tv_show
                tag="urn:tag:genre:media:family", 
                age_demographic="55_and_older",
                take=1
            )
            
            success = test_result.get("success", False)
            logger.info(f"Qloo connection test: {'PASSED' if success else 'FAILED'}")
            return success
            
        except Exception as e:
            logger.error(f"Qloo connection test failed: {e}")
            return False

# Test function
async def test_qloo_tools():
    """Test the simplified Qloo tools - UPDATED for TV Shows."""
    import os
    from backend.config.cultural_mappings import get_heritage_tags, get_age_demographic
    
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        print("❌ No QLOO_API_KEY found")
        return
    
    qloo = QlooInsightsAPI(api_key)
    
    # Test connection
    connected = await qloo.test_connection()
    print(f"Connection test: {'✅ PASSED' if connected else '❌ FAILED'}")
    
    if connected:
        # Test cultural heritage mapping
        heritage_tags = get_heritage_tags("Italian-American")
        age_demo = get_age_demographic(1945)
        
        print(f"\nTesting with heritage tags: {heritage_tags}")
        print(f"Age demographic: {age_demo}")
        
        # Make the 3 cultural calls
        results = await qloo.make_three_cultural_calls(heritage_tags, age_demo)
        
        print(f"\nResults: {results['successful_calls']}/3 calls successful")
        print(f"Total entities: {results['total_results']}")
        
        # Show sample results - UPDATED FOR TV SHOWS
        for category, data in results["cultural_recommendations"].items():
            if data.get("available"):
                print(f"\n{category.title()}: {data['entity_count']} results")
                for entity in data["entities"][:2]:  # Show first 2
                    name = entity.get('name', 'Unknown')
                    # Show additional info for TV shows
                    if category == "tv_shows":
                        properties = entity.get('properties', {})
                        release_year = properties.get('release_year', 'Unknown year')
                        print(f"  - {name} ({release_year})")
                    else:
                        print(f"  - {name}")

if __name__ == "__main__":
    asyncio.run(test_qloo_tools())