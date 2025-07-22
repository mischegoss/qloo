"""
Simplified Qloo Tools with Gemini Preprocessing
Implements clean two-stage API pattern with intelligent query optimization
"""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional, List
import json

logger = logging.getLogger(__name__)

class QlooInsightsAPI:
    """
    Simplified Qloo API integration with Gemini-powered query optimization.
    
    Key Features:
    1. Gemini preprocessing for intelligent query generation
    2. Clean two-stage pattern: search → insights
    3. Quality over quantity approach
    4. Minimal error handling - fail fast, log clearly
    5. No complex fallbacks or circuit breakers
    """
    
    def __init__(self, api_key: str, gemini_client, base_url: str = "https://hackathon.api.qloo.com"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.gemini = gemini_client
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Simple caching for successful searches
        self._search_cache = {}
        
        logger.info(f"Qloo API initialized with Gemini preprocessing")
    
    async def get_cultural_recommendations_with_gemini(self, 
                                                      cultural_keywords: List[str],
                                                      demographic_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point: Use Gemini to optimize queries, then execute Qloo API calls.
        """
        logger.info("🤖 Starting Gemini-optimized Qloo recommendations")
        
        # Step 1: Gemini preprocessing - generate optimized search plan
        search_plan = await self._gemini_optimize_search_strategy(cultural_keywords, demographic_signals)
        
        if not search_plan.get("success"):
            logger.error("Gemini preprocessing failed")
            return {"success": False, "error": "gemini_preprocessing_failed"}
        
        # Step 2: Execute optimized searches
        search_results = await self._execute_optimized_searches(search_plan["search_queries"])
        
        # Step 3: Generate insights using found entities
        insights_results = await self._execute_insights_with_entities(search_results, demographic_signals)
        
        successful_results = sum(1 for r in insights_results.values() if r.get("success"))
        logger.info(f"✅ Completed: {successful_results}/{len(insights_results)} successful")
        
        return {
            "success": successful_results > 0,
            "results": insights_results,
            "search_plan": search_plan.get("search_queries", {}),
            "total_successful": successful_results
        }
    
    async def _gemini_optimize_search_strategy(self, 
                                             cultural_keywords: List[str], 
                                             demographic_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Gemini to generate intelligent, context-aware search queries.
        """
        try:
            # Build context for Gemini
            age_context = demographic_signals.get("age_range", "unknown")
            location_context = demographic_signals.get("general_location", {})
            city = location_context.get("city_region", "")
            
            prompt = f"""
You are helping generate precise search queries for the Qloo API to find culturally relevant recommendations.

Cultural Context: {', '.join(cultural_keywords)}
Age Group: {age_context}
Location: {city}

Generate specific, searchable terms that would find relevant entities in these categories:

1. PLACES (restaurants, venues, locations)
2. ARTISTS (musicians, performers) 
3. MOVIES (films, shows)
4. BOOKS (literature, reading)

Rules:
- Use specific terms, not generic words
- Consider cultural context (e.g., "italian" → "italian restaurants", "traditional italian music")
- Make searches likely to find real entities
- Include location context when relevant
- Focus on 2-3 high-quality searches per category

Return JSON format:
{{
    "places": ["specific restaurant/venue searches"],
    "artists": ["specific musician/artist searches"], 
    "movies": ["specific film/genre searches"],
    "books": ["specific book/author searches"]
}}

Example for Italian-American context:
{{
    "places": ["italian restaurants", "family dining"],
    "artists": ["Frank Sinatra", "italian american singers"],
    "movies": ["italian family movies", "classic italian films"],
    "books": ["italian cookbook", "italian american authors"]
}}
"""

            logger.info("🤖 Gemini: Optimizing search strategy...")
            gemini_response = await self.gemini.generate_content(prompt)
            
            if not gemini_response or not gemini_response.get("text"):
                logger.error("Gemini returned empty response")
                return {"success": False, "error": "empty_gemini_response"}
            
            # Parse Gemini response
            response_text = gemini_response["text"].strip()
            
            # Extract JSON from response
            try:
                # Find JSON in response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx == -1 or end_idx == 0:
                    raise ValueError("No JSON found in response")
                    
                json_str = response_text[start_idx:end_idx]
                search_queries = json.loads(json_str)
                
                # Validate structure
                required_keys = ["places", "artists", "movies", "books"]
                if not all(key in search_queries for key in required_keys):
                    raise ValueError(f"Missing required keys. Expected: {required_keys}")
                
                logger.info(f"✅ Gemini generated optimized queries: {len(search_queries)} categories")
                return {"success": True, "search_queries": search_queries}
                
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Failed to parse Gemini JSON response: {e}")
                logger.error(f"Raw response: {response_text}")
                
                # Fallback to simple queries
                return self._generate_fallback_queries(cultural_keywords)
                
        except Exception as e:
            logger.error(f"Gemini optimization failed: {e}")
            return self._generate_fallback_queries(cultural_keywords)
    
    def _generate_fallback_queries(self, cultural_keywords: List[str]) -> Dict[str, Any]:
        """
        Generate simple fallback queries if Gemini fails.
        """
        logger.info("🔄 Using fallback query generation")
        
        # Create basic queries from cultural keywords
        queries = {
            "places": [f"{kw} restaurants" for kw in cultural_keywords[:2]],
            "artists": [f"{kw} music" for kw in cultural_keywords[:2]], 
            "movies": [f"{kw} movies" for kw in cultural_keywords[:2]],
            "books": [f"{kw} books" for kw in cultural_keywords[:2]]
        }
        
        return {"success": True, "search_queries": queries}
    
    async def _execute_optimized_searches(self, search_queries: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
        """
        Execute the optimized searches generated by Gemini.
        """
        logger.info("🔍 Executing optimized searches...")
        
        entity_type_mapping = {
            "places": "urn:entity:place",
            "artists": "urn:entity:artist", 
            "movies": "urn:entity:movie",
            "books": "urn:entity:book"
        }
        
        search_results = {}
        
        for category, queries in search_queries.items():
            if category not in entity_type_mapping:
                continue
                
            entity_type = entity_type_mapping[category]
            search_results[entity_type] = []
            
            # Try each query in the category
            for query in queries[:2]:  # Limit to 2 queries per category
                logger.info(f"🔍 Searching: '{query}' in {category}")
                
                result = await self._search_entities_simple(query, [entity_type])
                
                if result.get("success") and result.get("entities"):
                    search_results[entity_type].extend(result["entities"])
                    logger.info(f"✅ Found {len(result['entities'])} entities for '{query}'")
                
                # Rate limiting
                await asyncio.sleep(1.0)
        
        # Log summary
        total_found = sum(len(entities) for entities in search_results.values())
        logger.info(f"🎯 Search complete: {total_found} total entities found")
        
        return search_results
    
    async def _search_entities_simple(self, query: str, entity_types: List[str]) -> Dict[str, Any]:
        """
        Simple, clean entity search with no complex logic.
        """
        try:
            # Check cache
            cache_key = f"{query.lower()}:{':'.join(entity_types)}"
            if cache_key in self._search_cache:
                return self._search_cache[cache_key]
            
            params = {
                "query": query.strip()[:50],
                "types": ",".join(entity_types),
                "limit": 3
            }
            
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                response = await client.get(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    entities = data.get("results", [])
                    
                    result = {"success": True, "entities": entities}
                    
                    # Cache successful results
                    self._search_cache[cache_key] = result
                    
                    return result
                
                else:
                    logger.warning(f"Search failed for '{query}': {response.status_code}")
                    return {"success": False, "error": f"http_{response.status_code}"}
        
        except Exception as e:
            logger.error(f"Search exception for '{query}': {e}")
            return {"success": False, "error": "exception"}
    
    async def _execute_insights_with_entities(self, 
                                            search_results: Dict[str, List[Dict]], 
                                            demographic_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute insights calls using found entities. Simple and direct.
        """
        logger.info("💡 Executing insights with found entities...")
        
        insights_results = {}
        
        for entity_type, entities in search_results.items():
            if not entities:
                logger.info(f"⏭️  Skipping {entity_type}: no entities found")
                insights_results[entity_type] = {"success": False, "error": "no_entities_found"}
                continue
            
            # Use the first entity found
            entity = entities[0]
            entity_id = entity.get("entity_id") or entity.get("id")
            
            if not entity_id:
                logger.warning(f"⚠️  No entity_id found for {entity_type}")
                insights_results[entity_type] = {"success": False, "error": "no_entity_id"}
                continue
            
            # Build simple, clean parameters
            params = await self._gemini_build_insights_params(entity_type, entity_id, demographic_signals)
            
            if not params:
                logger.error(f"❌ Failed to build params for {entity_type}")
                insights_results[entity_type] = {"success": False, "error": "param_build_failed"}
                continue
            
            # Execute insights call
            logger.info(f"💡 Getting insights for {entity_type} with entity {entity_id}")
            result = await self._get_insights_simple(params)
            
            insights_results[entity_type] = result
            
            # Rate limiting
            await asyncio.sleep(1.5)
        
        return insights_results
    
    async def _gemini_build_insights_params(self, 
                                          entity_type: str, 
                                          entity_id: str, 
                                          demographic_signals: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Use Gemini to build optimal insights parameters.
        """
        try:
            age_range = demographic_signals.get("age_range", "")
            location = demographic_signals.get("general_location", {})
            
            prompt = f"""
Build optimal parameters for Qloo Insights API call.

Entity Type: {entity_type}
Entity ID: {entity_id}
Age Range: {age_range}
Location: {location}

Rules:
1. Always include filter.type and signal.interests.entities
2. Add take=5 for results limit
3. Add demographics if age_range available: 18_to_34, 35_to_54, or 55_and_older
4. For places, add location if available
5. Only use supported parameters

Return clean JSON:
{{
    "filter.type": "{entity_type}",
    "signal.interests.entities": "{entity_id}",
    "take": "5"
}}
"""

            gemini_response = await self.gemini.generate_content(prompt)
            
            if gemini_response and gemini_response.get("text"):
                response_text = gemini_response["text"].strip()
                
                # Extract JSON
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    params = json.loads(json_str)
                    
                    # Validate required params
                    if "filter.type" in params and "signal.interests.entities" in params:
                        logger.info(f"✅ Gemini built params: {list(params.keys())}")
                        return params
            
            # Fallback to manual construction
            logger.info("🔄 Using manual parameter construction")
            return self._build_simple_params(entity_type, entity_id, demographic_signals)
            
        except Exception as e:
            logger.warning(f"Gemini param building failed: {e}")
            return self._build_simple_params(entity_type, entity_id, demographic_signals)
    
    def _build_simple_params(self, 
                           entity_type: str, 
                           entity_id: str, 
                           demographic_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build simple, guaranteed-to-work parameters.
        """
        params = {
            "filter.type": entity_type,
            "signal.interests.entities": entity_id,
            "take": "5"
        }
        
        # Add age if available
        age_range = demographic_signals.get("age_range", "")
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
    
    async def _get_insights_simple(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simple insights call with clear error handling.
        """
        try:
            entity_type = params.get("filter.type", "unknown")
            
            logger.info(f"💡 Insights request: {list(params.keys())}")
            
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
                        logger.info(f"✅ Insights success: {len(entities)} recommendations")
                        return {"success": True, "results": data, "count": len(entities)}
                    else:
                        logger.warning(f"⚠️  Insights returned no results for {entity_type}")
                        return {"success": False, "error": "no_results"}
                
                else:
                    logger.error(f"❌ Insights API error: {response.status_code}")
                    return {"success": False, "error": f"http_{response.status_code}"}
        
        except Exception as e:
            logger.error(f"💥 Insights exception: {e}")
            return {"success": False, "error": "exception"}
    
    async def test_connection(self) -> bool:
        """Simple connection test."""
        try:
            result = await self._search_entities_simple("music", ["urn:entity:artist"])
            return result.get("success", False)
        except Exception:
            return False
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get simple cache statistics."""
        return {"search_cache_size": len(self._search_cache)}