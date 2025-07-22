"""
Fixed Qloo Tools - Implements proper two-stage API pattern with robust error handling
"""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional, List
import json

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    COMPLETELY FIXED Qloo API integration following Sarah Qloo's best practices.
    
    Qloo Insights API tool for cultural intelligence recommendations.
    Used by Agent 3: Qloo Cultural Intelligence Agent
    
    Key Fixes:
    1. Two-stage API pattern: search → insights
    2. Simplified query structure with essential parameters only
    3. Proper rate limiting (1-2 second delays)
    4. Entity-specific parameter validation
    5. Robust error recovery with meaningful timeouts
    6. Smart caching for entity_ids and tags
    """
    
    def __init__(self, api_key: str, base_url: str = "https://hackathon.api.qloo.com"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Smart caching to reduce API calls
        self._entity_cache = {}
        self._tag_cache = {}
        
        # Circuit breaker for failed entity types
        self._failed_entity_types = set()
        
        logger.info(f"Qloo API initialized with base URL: {self.base_url}")
    
    async def search_entities(self, query: str, entity_types: List[str] = None, limit: int = 3) -> Dict[str, Any]:
        """
        Stage 1: Search for entities using /search endpoint.
        This is the CORRECT way to find entity_ids according to best practices.
        """
        try:
            # Default to most useful entity types if none specified
            if not entity_types:
                entity_types = ["urn:entity:movie", "urn:entity:artist", "urn:entity:place"]
            
            params = {
                "query": query.strip()[:50],  # Limit query length
                "types": ",".join(entity_types),
                "limit": limit
            }
            
            logger.info(f"Qloo search: '{query}' for types: {entity_types}")
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])  # FIXED: Correct parsing
                    
                    # Cache successful results
                    for result in results:
                        entity_id = result.get("id")
                        if entity_id:
                            self._entity_cache[query.lower()] = entity_id
                    
                    logger.info(f"Search success: {len(results)} entities found")
                    return {"success": True, "results": results}  # FIXED: Return results directly
                
                elif response.status_code == 400:
                    logger.error(f"Search bad request (400): {response.text}")
                    return {"success": False, "error": "bad_request"}
                
                elif response.status_code == 429:
                    logger.warning("Search rate limited (429)")
                    await asyncio.sleep(2.0)  # Wait before retry
                    return {"success": False, "error": "rate_limited"}
                
                else:
                    logger.error(f"Search API error: {response.status_code}")
                    return {"success": False, "error": f"http_{response.status_code}"}
        
        except httpx.TimeoutException:
            logger.error("Search API timeout")
            return {"success": False, "error": "timeout"}
        except Exception as e:
            logger.error(f"Search API exception: {str(e)}")
            return {"success": False, "error": "exception"}
    
    async def search_tags(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search for valid tags using /tags/search endpoint.
        """
        try:
            # Check cache first
            cache_key = query.lower()
            if cache_key in self._tag_cache:
                return {"success": True, "results": self._tag_cache[cache_key]}
            
            params = {
                "query": query.strip()[:30],
                "limit": limit
            }
            
            logger.info(f"Tag search: '{query}'")
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(8.0)) as client:
                response = await client.get(
                    f"{self.base_url}/tags/search",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    # Cache results
                    self._tag_cache[cache_key] = results
                    
                    logger.info(f"Tag search success: {len(results)} tags found")
                    return {"success": True, "results": results}
                
                else:
                    logger.error(f"Tag search error: {response.status_code}")
                    return {"success": False, "error": f"http_{response.status_code}"}
        
        except Exception as e:
            logger.error(f"Tag search exception: {str(e)}")
            return {"success": False, "error": "exception"}
    
    async def get_insights(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 2: Get insights using /v2/insights endpoint with proper parameters.
        Only called after we have valid entity_ids from search.
        """
        try:
            entity_type = params.get("filter.type")
            
            # Circuit breaker - skip if this entity type failed recently
            if entity_type in self._failed_entity_types:
                logger.warning(f"Skipping {entity_type} due to circuit breaker")
                return {"success": False, "error": "circuit_breaker"}
            
            # Validate parameters before sending
            validation_result = self._validate_insights_params(params)
            if not validation_result["valid"]:
                logger.error(f"Parameter validation failed: {validation_result['error']}")
                return {"success": False, "error": "invalid_params", "details": validation_result['error']}
            
            logger.info(f"Insights request for {entity_type}: {list(params.keys())}")
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.get(
                    f"{self.base_url}/v2/insights",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("entities", [])
                    
                    if entities:
                        logger.info(f"Insights success: {len(entities)} entities for {entity_type}")
                        return {"success": True, "results": data}
                    else:
                        logger.warning(f"Insights returned no entities for {entity_type}")
                        return {"success": False, "error": "no_entities"}
                
                elif response.status_code == 400:
                    # Bad request - add to circuit breaker
                    self._failed_entity_types.add(entity_type)
                    error_data = response.text
                    logger.error(f"Insights bad request (400) for {entity_type}: {error_data}")
                    return {"success": False, "error": "bad_request", "details": error_data}
                
                elif response.status_code == 403:
                    # Forbidden - add to circuit breaker
                    self._failed_entity_types.add(entity_type)
                    logger.error(f"Insights forbidden (403) for {entity_type}")
                    return {"success": False, "error": "forbidden"}
                
                elif response.status_code == 429:
                    logger.warning(f"Insights rate limited (429) for {entity_type}")
                    await asyncio.sleep(3.0)  # Longer wait for rate limit
                    return {"success": False, "error": "rate_limited"}
                
                else:
                    logger.error(f"Insights API error: {response.status_code} for {entity_type}")
                    return {"success": False, "error": f"http_{response.status_code}"}
        
        except httpx.TimeoutException:
            logger.error(f"Insights timeout for {entity_type}")
            return {"success": False, "error": "timeout"}
        except Exception as e:
            logger.error(f"Insights exception for {entity_type}: {str(e)}")
            return {"success": False, "error": "exception"}
    
    def _validate_insights_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate parameters against Entity Type Parameter Guide.
        """
        entity_type = params.get("filter.type")
        if not entity_type:
            return {"valid": False, "error": "filter.type is required"}
        
        # Check for at least one signal
        signal_params = [key for key in params.keys() if key.startswith("signal.")]
        if not signal_params:
            return {"valid": False, "error": "At least one signal parameter is required"}
        
        # Entity-specific validation based on Parameter Guide
        valid_params = self._get_valid_params_for_entity(entity_type)
        
        for param in params.keys():
            if param not in valid_params and param != "take":
                logger.warning(f"Parameter {param} may not be valid for {entity_type}")
        
        return {"valid": True, "error": None}
    
    def _get_valid_params_for_entity(self, entity_type: str) -> List[str]:
        """
        Return valid parameters for each entity type based on Parameter Guide.
        """
        # Core parameters valid for all entity types
        base_params = [
            "filter.type", "take", "offset",
            "signal.demographics.age", "signal.demographics.gender",
            "signal.interests.entities", "signal.interests.tags"
        ]
        
        # Entity-specific parameters
        entity_specific = {
            "urn:entity:place": base_params + [
                "signal.location.query", "filter.location", "filter.geocode.name"
            ],
            "urn:entity:movie": base_params + [
                "filter.release_year.min", "filter.release_year.max", "filter.rating.min"
            ],
            "urn:entity:artist": base_params + [
                "filter.popularity.min", "filter.popularity.max"
            ],
            "urn:entity:book": base_params + [
                "filter.publication_year.min", "filter.publication_year.max"
            ]
        }
        
        return entity_specific.get(entity_type, base_params)
    
    async def get_cultural_recommendations_fixed(self, 
                                               cultural_keywords: List[str],
                                               demographic_signals: Dict[str, Any],
                                               entity_types: List[str] = None) -> Dict[str, Any]:
        """
        FIXED: Two-stage cultural recommendations following best practices.
        
        Stage 1: Search for entities based on cultural keywords
        Stage 2: Get insights using found entity_ids
        """
        if not entity_types:
            entity_types = [
                "urn:entity:artist",
                "urn:entity:place", 
                "urn:entity:movie"
            ]
        
        results = {}
        
        # Stage 1: Find entities for cultural concepts
        entity_findings = {}
        for keyword in cultural_keywords[:3]:  # Limit to avoid too many API calls
            search_result = await self.search_entities(keyword, entity_types, limit=2)
            
            if search_result.get("success"):
                search_entities = search_result.get("results", [])
                logger.info(f"Search for '{keyword}' returned {len(search_entities)} entities")
                
                # Debug: Log first entity structure
                if search_entities:
                    logger.info(f"Sample entity structure: {search_entities[0]}")
                
                for entity in search_entities:
                    entity_types_array = entity.get("types", [])
                    entity_id = entity.get("entity_id", "")
                    
                    # Debug logging
                    logger.info(f"Processing entity: entity_id={entity_id}, types={entity_types_array}")
                    
                    if entity_types_array and entity_id:
                        # Use the first type from the types array
                        entity_type = entity_types_array[0] if entity_types_array else ""
                        
                        if entity_type and entity_id:
                            if entity_type not in entity_findings:
                                entity_findings[entity_type] = []
                            if entity_id not in entity_findings[entity_type]:  # Avoid duplicates
                                entity_findings[entity_type].append(entity_id)
                            logger.info(f"✅ Found entity {entity_id} for type {entity_type}")
                        else:
                            logger.warning(f"❌ Invalid entity: missing entity_id or type")
                    else:
                        logger.warning(f"❌ Invalid entity: missing entity_id or types array")
            
            # Rate limiting between searches
            await asyncio.sleep(1.5)
        
        logger.info(f"Entity findings summary: {[(k, len(v)) for k, v in entity_findings.items()]}")
        logger.info(f"Total entity IDs found: {sum(len(v) for v in entity_findings.values())}")
        
        # Stage 2: Get insights for each entity type with found entities
        for entity_type in entity_types:
            if entity_type in self._failed_entity_types:
                logger.warning(f"Skipping {entity_type} due to circuit breaker")
                continue
            
            # Build minimal, focused parameters
            params = self._build_minimal_params(entity_type, entity_findings, demographic_signals)
            
            if params:
                logger.info(f"Executing insights for {entity_type} with params: {list(params.keys())}")
                insights_result = await self.get_insights(params)
                results[entity_type] = insights_result
                
                # Rate limiting between insights calls
                await asyncio.sleep(2.0)
            else:
                logger.error(f"Could not build params for {entity_type}")
                results[entity_type] = {"success": False, "error": "no_params"}
        
        successful_results = sum(1 for r in results.values() if r.get("success"))
        logger.info(f"Cultural recommendations complete: {successful_results}/{len(entity_types)} successful")
        
        return results
    
    def _build_minimal_params(self, 
                            entity_type: str, 
                            entity_findings: Dict[str, List[str]], 
                            demographic_signals: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Build minimal, focused parameters for insights API.
        """
        params = {
            "filter.type": entity_type,
            "take": "3"
        }
        
        # Add entity signals if we found relevant entities
        found_entities = entity_findings.get(entity_type, [])
        if found_entities:
            params["signal.interests.entities"] = found_entities[0]  # Use first found entity
            logger.info(f"Using entity signal for {entity_type}: {found_entities[0]}")
        else:
            # Try to use entities from other types if available
            all_entities = []
            for entities_list in entity_findings.values():
                all_entities.extend(entities_list)
            
            if all_entities:
                params["signal.interests.entities"] = all_entities[0]
                logger.info(f"Using cross-type entity signal for {entity_type}: {all_entities[0]}")
            else:
                # Last resort: use more specific interest tags
                specific_tags = {
                    "urn:entity:artist": "urn:tag:genre:music:jazz",
                    "urn:entity:place": "urn:tag:cuisine:media:italian", 
                    "urn:entity:movie": "urn:tag:genre:movie:drama",
                    "urn:entity:book": "urn:tag:genre:book:fiction"
                }
                fallback_tag = specific_tags.get(entity_type, "music")
                params["signal.interests.tags"] = fallback_tag
                logger.warning(f"No entities found, using fallback tag for {entity_type}: {fallback_tag}")
        
        # Add demographics if available
        age_range = demographic_signals.get("age_range", "")
        if age_range and age_range != "age_unknown":
            if "senior" in age_range or "older" in age_range:
                params["signal.demographics.age"] = "55_and_older"
            elif "adult" in age_range or "mature" in age_range:
                params["signal.demographics.age"] = "35_to_54"
            elif "young" in age_range:
                params["signal.demographics.age"] = "18_to_34"
        
        # Add location for places
        if entity_type == "urn:entity:place":
            location = demographic_signals.get("general_location", {})
            city = location.get("city_region", "").strip()
            if city and len(city) > 2:
                params["signal.location.query"] = city[:30]
        
        return params
    
    async def test_connection(self) -> bool:
        """
        Test connection with a simple, guaranteed-to-work query.
        """
        try:
            test_result = await self.search_entities("music", ["urn:entity:artist"], limit=1)
            return test_result.get("success", False)
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False
    
    def reset_circuit_breaker(self):
        """Reset circuit breaker for failed entity types."""
        self._failed_entity_types.clear()
        logger.info("Circuit breaker reset")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics for monitoring."""
        return {
            "entity_cache_size": len(self._entity_cache),
            "tag_cache_size": len(self._tag_cache),
            "failed_entity_types": len(self._failed_entity_types)
        }
    
    async def _discover_tag_for_entity_type(self, entity_type: str) -> Optional[str]:
        """
        Discover valid tags for entity type using /tags/search endpoint.
        """
        try:
            # Map entity types to search queries
            search_queries = {
                "urn:entity:artist": "music",
                "urn:entity:place": "restaurant",
                "urn:entity:movie": "movies", 
                "urn:entity:book": "books"
            }
            
            search_query = search_queries.get(entity_type, "entertainment")
            tag_result = await self.search_tags(search_query, limit=3)
            
            if tag_result.get("success"):
                tags = tag_result.get("results", [])
                if tags:
                    # Use the first valid tag ID
                    tag_id = tags[0].get("id", "")
                    if tag_id:
                        logger.info(f"Discovered tag via /tags/search: {tag_id}")
                        return tag_id
            
            logger.warning(f"No tags discovered for {entity_type}, using simple fallback")
            return None
            
        except Exception as e:
            logger.error(f"Tag discovery failed for {entity_type}: {str(e)}")
            return None