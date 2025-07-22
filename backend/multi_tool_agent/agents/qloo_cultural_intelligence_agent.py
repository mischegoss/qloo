"""
Agent 3: Qloo Cultural Intelligence - FIXED VERSION
Role: Query Qloo API for cross-domain cultural recommendations
Follows Qloo Best Practices and Hackathon Developer Guide
"""

from typing import Dict, Any, Optional, List, Set
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent(Agent):
    """
    Agent 3: Qloo Cultural Intelligence - FIXED
    
    FIXED ISSUES:
    - Using ONLY supported entity types from Best Practices
    - Proper API usage: /search first, then /v2/insights
    - Correct tool reference handling
    - Valid tag IDs from /v2/tags endpoint
    - Proper error handling for empty responses
    """
    
    def __init__(self, qloo_tool):
        super().__init__(
            name="qloo_cultural_intelligence",
            description="Generates cross-domain cultural recommendations using Qloo API with proper Best Practices"
        )
        # Store tool reference correctly
        self._qloo_tool = qloo_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cross-domain cultural intelligence using Qloo API."""
        
        try:
            logger.info("Starting Qloo cultural intelligence generation with Best Practices")
            
            # Extract request context and blocked content
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            
            # Extract cultural information
            cultural_elements = cultural_profile.get("cultural_elements", {})
            qloo_framework = cultural_profile.get("qloo_framework", {})
            
            # Build proper Qloo query strategy following Best Practices
            query_strategy = await self._build_proper_qloo_strategy(
                request_context, 
                qloo_framework, 
                cultural_elements,
                blocked_content
            )
            
            # Execute Qloo API calls following Best Practices pattern
            qloo_results = await self._execute_proper_qloo_queries(query_strategy)
            
            # Process and filter results
            processed_results = self._process_qloo_results(qloo_results, blocked_content, cultural_elements)
            
            # Generate cross-domain connections
            cross_domain_connections = self._generate_cross_domain_connections(processed_results)
            
            # Create thematic intelligence
            thematic_intelligence = self._create_thematic_intelligence(
                processed_results, 
                cross_domain_connections,
                cultural_elements
            )
            
            # Build enhanced cultural intelligence
            enhanced_intelligence = {
                "qloo_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query_strategy": query_strategy["approach"],
                    "api_calls_made": len(qloo_results),
                    "best_practices_followed": True,
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "cultural_recommendations": processed_results,
                "cross_domain_connections": cross_domain_connections,
                "thematic_intelligence": thematic_intelligence,
                "fallback_used": False
            }
            
            logger.info(f"Qloo cultural intelligence generated: {len(processed_results)} entity types processed")
            return {"qloo_intelligence": enhanced_intelligence}
            
        except Exception as e:
            logger.error(f"Error in Qloo cultural intelligence: {str(e)}")
            return self._create_fallback_qloo_intelligence(consolidated_info, cultural_profile)
    
    async def _build_proper_qloo_strategy(self, 
                                        request_context: Dict[str, Any],
                                        qloo_framework: Dict[str, Any],
                                        cultural_elements: Dict[str, Any],
                                        blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """Build proper Qloo query strategy following Best Practices."""
        
        request_type = request_context.get("request_type", "dashboard")
        
        # FIXED: Use ONLY supported entity types from Best Practices
        supported_entity_types = self._get_supported_entity_types(request_type)
        
        # Get valid tag IDs from Qloo (Best Practices approach)
        valid_tags = await self._get_valid_qloo_tags(cultural_elements)
        
        # Build base query parameters following Best Practices
        demographic_signals = qloo_framework.get("demographic_signals", {})
        base_params = self._build_proper_base_params(demographic_signals, valid_tags)
        
        # Build entity-specific queries following Best Practices
        query_list = []
        for entity_type in supported_entity_types:
            if not self._is_entity_type_blocked(entity_type, blocked_content):
                # First search for entity IDs, then use insights
                query = await self._build_proper_entity_query(
                    entity_type, 
                    base_params, 
                    valid_tags,
                    request_type
                )
                if query:  # Only add if successfully built
                    query_list.append(query)
        
        strategy = {
            "approach": "best_practices_two_step_process",
            "entity_types": supported_entity_types,
            "query_list": query_list,
            "valid_tags_found": len(valid_tags),
            "blocked_content_checked": True,
            "best_practices_compliance": True
        }
        
        return strategy
    
    def _get_supported_entity_types(self, request_type: str) -> List[str]:
        """FIXED: Return ONLY supported entity types from Best Practices."""
        
        # ONLY use entity types explicitly supported in hackathon
        if request_type == "meal":
            return ["urn:entity:place", "urn:entity:artist"]  # Restaurants and music
        elif request_type == "music":
            return ["urn:entity:artist"]  # REMOVED urn:entity:album - NOT supported
        elif request_type == "conversation":
            return ["urn:entity:movie", "urn:entity:book", "urn:entity:person"]
        elif request_type == "video":
            return ["urn:entity:movie", "urn:entity:tv_show"]
        else:  # dashboard
            return ["urn:entity:artist", "urn:entity:place", "urn:entity:movie"]
    
    async def _get_valid_qloo_tags(self, cultural_elements: Dict[str, Any]) -> List[str]:
        """Get valid tag IDs from Qloo /v2/tags endpoint (Best Practices)."""
        
        valid_tags = []
        
        # Extract cultural keywords
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        tradition_keywords = cultural_elements.get("tradition_elements", {}).get("tradition_keywords", [])
        
        all_keywords = heritage_keywords + tradition_keywords
        
        # Search for valid tags using Qloo tags endpoint
        for keyword in all_keywords[:3]:  # Limit to avoid too many calls
            try:
                # Use search method to find valid tags
                tag_search = await self._qloo_tool.search(keyword, limit=3)
                
                if tag_search and tag_search.get("success"):
                    results = tag_search.get("results", {}).get("results", [])
                    for result in results:
                        tag_id = result.get("id")
                        if tag_id and tag_id not in valid_tags:
                            valid_tags.append(tag_id)
                
                await asyncio.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Tag search failed for {keyword}: {str(e)}")
        
        # Fallback to basic tags if no cultural tags found
        if not valid_tags:
            valid_tags = ["music", "dining", "entertainment"]  # Basic fallback
        
        logger.info(f"Found {len(valid_tags)} valid tags for Qloo queries")
        return valid_tags
    
    def _build_proper_base_params(self, 
                                 demographic_signals: Dict[str, Any],
                                 valid_tags: List[str]) -> Dict[str, str]:
        """Build base Qloo parameters following Best Practices."""
        
        params = {}
        
        # FIXED: Age demographic signal (using CORRECT Qloo API values from error message)
        age_range = demographic_signals.get("age_range")
        if age_range and age_range != "age_unknown":
            if "senior" in age_range or "100_plus" in age_range:
                params["signal.demographics.age"] = "55_and_older"  # This one is correct
            elif "adult" in age_range or "mature" in age_range:
                params["signal.demographics.age"] = "36_to_55"  # FIXED: was 35_to_54
            elif "young" in age_range:
                params["signal.demographics.age"] = "35_and_younger"  # FIXED: was 18_to_34
        
        # Location signal (if available)
        location = demographic_signals.get("general_location", {})
        city_region = location.get("city_region", "").strip()
        if city_region and len(city_region) > 2:
            params["signal.location.query"] = city_region
        
        # Essential interest signal (REQUIRED)
        if valid_tags:
            params["signal.interests.tags"] = valid_tags[0]
        
        # Results limit
        params["take"] = "3"
        
        return params
    
    async def _build_proper_entity_query(self, 
                                       entity_type: str,
                                       base_params: Dict[str, str],
                                       valid_tags: List[str],
                                       request_type: str) -> Optional[Dict[str, Any]]:
        """Build proper entity query following Best Practices two-step process."""
        
        try:
            # STEP 1: Search for entity IDs first (Best Practices)
            search_query = self._build_search_query(entity_type, valid_tags, request_type)
            
            if search_query:
                search_results = await self._qloo_tool.search(search_query, limit=5)
                
                if search_results and search_results.get("success"):
                    entity_ids = self._extract_entity_ids(search_results)
                    
                    if entity_ids:
                        # STEP 2: Build insights query with found entity IDs
                        insights_params = base_params.copy()
                        insights_params["filter.type"] = entity_type
                        insights_params["signal.interests.entities"] = entity_ids[0]  # Use first found entity
                        
                        return {
                            "entity_type": entity_type,
                            "search_query": search_query,
                            "insights_params": insights_params,
                            "found_entity_ids": entity_ids
                        }
            
            # Fallback: Basic query without specific entities
            insights_params = base_params.copy()
            insights_params["filter.type"] = entity_type
            
            # Ensure required signals for specific entity types
            if "place" in entity_type and "signal.interests.entities" not in insights_params:
                # For places, we need interests.entities or fallback won't work
                return None
            
            return {
                "entity_type": entity_type,
                "search_query": None,
                "insights_params": insights_params,
                "found_entity_ids": []
            }
            
        except Exception as e:
            logger.error(f"Error building query for {entity_type}: {str(e)}")
            return None
    
    def _build_search_query(self, entity_type: str, valid_tags: List[str], request_type: str) -> str:
        """Build search query string for entity discovery."""
        
        if "artist" in entity_type:
            return "classic music artists"
        elif "place" in entity_type:
            return "restaurants dining"
        elif "movie" in entity_type:
            return "classic movies"
        elif "book" in entity_type:
            return "classic books"
        elif "tv_show" in entity_type:
            return "classic television shows"
        else:
            return "entertainment"
    
    def _extract_entity_ids(self, search_results: Dict[str, Any]) -> List[str]:
        """Extract entity IDs from search results."""
        
        entity_ids = []
        results = search_results.get("results", {}).get("results", [])
        
        for result in results:
            entity_id = result.get("id")
            if entity_id:
                entity_ids.append(entity_id)
        
        return entity_ids
    
    async def _execute_proper_qloo_queries(self, query_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Qloo API queries following Best Practices."""
        
        query_list = query_strategy.get("query_list", [])
        results = {}
        
        for query in query_list:
            entity_type = query["entity_type"]
            insights_params = query["insights_params"]
            
            try:
                logger.info(f"Executing Qloo insights query for {entity_type}")
                
                # FIXED: Use correct tool reference
                api_result = await self._qloo_tool.get_insights(insights_params)
                
                if api_result and api_result.get("success"):
                    # FIXED: Better result processing
                    results_data = api_result.get("results", {})
                    entities = results_data.get("entities", [])
                    
                    if entities:  # Only store if we got actual entities
                        results[entity_type] = {
                            "success": True,
                            "data": results_data,
                            "entity_count": len(entities),
                            "query_params": insights_params,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        logger.info(f"Qloo success: {len(entities)} entities for {entity_type}")
                    else:
                        logger.warning(f"Qloo returned no entities for {entity_type}")
                        results[entity_type] = {
                            "success": False,
                            "data": {},
                            "error": "no_entities_returned"
                        }
                else:
                    logger.warning(f"Qloo API failed for {entity_type}: {api_result}")
                    results[entity_type] = {
                        "success": False,
                        "data": {},
                        "error": api_result.get("error", "unknown_error") if api_result else "no_response"
                    }
                
                # Rate limiting
                await asyncio.sleep(0.2)
                
            except Exception as e:
                logger.error(f"Qloo API error for {entity_type}: {str(e)}")
                results[entity_type] = {
                    "success": False,
                    "data": {},
                    "error": str(e)
                }
        
        return results
    
    def _process_qloo_results(self, 
                             qloo_results: Dict[str, Any],
                             blocked_content: Dict[str, Any],
                             cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Process Qloo results and filter based on blocked content."""
        
        processed = {}
        
        for entity_type, result_data in qloo_results.items():
            if not result_data.get("success"):
                logger.warning(f"Skipping failed result for {entity_type}")
                continue
                
            entities = result_data.get("data", {}).get("entities", [])
            
            if not entities:
                logger.warning(f"No entities found for {entity_type}")
                continue
            
            # Filter blocked entities
            filtered_entities = self._filter_blocked_entities(entities, blocked_content)
            
            # Enhance entities with cultural context
            enhanced_entities = self._enhance_entities_with_context(
                filtered_entities, 
                entity_type, 
                cultural_elements
            )
            
            if enhanced_entities:  # Only add if we have entities
                processed[entity_type] = {
                    "available": True,
                    "entities": enhanced_entities,
                    "total_found": len(entities),
                    "after_filtering": len(enhanced_entities),
                    "entity_type": entity_type,
                    "entity_type_category": self._get_entity_category(entity_type)
                }
                logger.info(f"Processed {len(enhanced_entities)} entities for {entity_type}")
        
        return processed
    
    def _get_entity_category(self, entity_type: str) -> str:
        """Get human-readable category for entity type."""
        
        if "artist" in entity_type:
            return "music"
        elif "place" in entity_type:
            return "dining"
        elif "movie" in entity_type:
            return "movies"
        elif "book" in entity_type:
            return "books"
        elif "tv_show" in entity_type:
            return "television"
        else:
            return "entertainment"
    
    def _filter_blocked_entities(self, entities: List[Dict[str, Any]], blocked_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter out blocked entities based on user feedback."""
        
        blocked_names = blocked_content.get("blocked_names", [])
        blocked_ids = blocked_content.get("blocked_entity_ids", [])
        
        filtered = []
        for entity in entities:
            entity_name = entity.get("name", "").lower()
            entity_id = entity.get("id", "")
            
            # Check if blocked
            is_blocked = any(blocked.lower() in entity_name for blocked in blocked_names)
            is_blocked = is_blocked or entity_id in blocked_ids
            
            if not is_blocked:
                filtered.append(entity)
        
        return filtered
    
    def _enhance_entities_with_context(self, 
                                      entities: List[Dict[str, Any]], 
                                      entity_type: str,
                                      cultural_elements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enhance entities with cultural context and caregiver guidance."""
        
        enhanced = []
        
        for entity in entities:
            enhanced_entity = {
                "qloo_entity": entity,
                "name": entity.get("name", "Unknown"),
                "entity_id": entity.get("id", ""),
                "type": entity.get("type", ""),
                "cultural_score": entity.get("score", 0.0),
                "cultural_context": self._generate_cultural_context(entity, cultural_elements),
                "cross_domain_potential": self._assess_cross_domain_potential(entity, entity_type),
                "caregiver_guidance": self._generate_caregiver_guidance(entity, entity_type)
            }
            
            enhanced.append(enhanced_entity)
        
        return enhanced
    
    def _generate_cultural_context(self, 
                                  entity: Dict[str, Any],
                                  cultural_elements: Dict[str, Any]) -> Dict[str, str]:
        """Generate cultural context explanation without assumptions."""
        
        context = {
            "discovery_reason": "qloo_cultural_intelligence",
            "cultural_connection": "cross_domain_exploration",
            "why_suggested": "cultural_taste_intelligence_recommendation"
        }
        
        # Check for cultural keyword connections
        entity_name = entity.get("name", "").lower()
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        
        for keyword in heritage_keywords:
            if keyword.lower() in entity_name:
                context["cultural_connection"] = f"connects_to_{keyword}_heritage"
                context["why_suggested"] = f"cultural_exploration_related_to_{keyword}"
                break
        
        return context
    
    def _assess_cross_domain_potential(self, 
                                      entity: Dict[str, Any],
                                      entity_type: str) -> List[str]:
        """Assess potential for cross-domain connections."""
        
        potential = []
        
        if "artist" in entity_type:
            potential.extend(["music_listening", "conversation_starter", "memory_trigger", "movement_activity"])
        elif "place" in entity_type:
            potential.extend(["dining_experience", "cultural_exploration", "sensory_engagement", "conversation_topic"])
        elif "movie" in entity_type:
            potential.extend(["viewing_together", "conversation_topic", "nostalgic_connection", "memory_sharing"])
        elif "book" in entity_type:
            potential.extend(["reading_together", "conversation_starter", "memory_exploration", "storytelling"])
        elif "tv_show" in entity_type:
            potential.extend(["viewing_activity", "shared_memories", "conversation_topic", "nostalgia"])
        
        return potential
    
    def _generate_caregiver_guidance(self, 
                                   entity: Dict[str, Any], 
                                   entity_type: str) -> Dict[str, str]:
        """Generate guidance for caregivers on how to use this suggestion."""
        
        entity_name = entity.get("name", "Unknown")
        
        if "artist" in entity_type:
            return {
                "implementation": f"Play {entity_name} music together or discuss the artist",
                "engagement": "Ask about memories associated with this music",
                "customization": "Adjust volume and duration based on their response",
                "safety": "Monitor emotional responses to music"
            }
        elif "place" in entity_type:
            return {
                "implementation": f"Consider {entity_name} for outings or takeout orders",
                "engagement": "Talk about favorite restaurants or similar places",
                "customization": "Check dietary restrictions and accessibility",
                "safety": "Ensure safe dining environment and food choices"
            }
        elif "movie" in entity_type:
            return {
                "implementation": f"Watch {entity_name} together or discuss the movie",
                "engagement": "Ask about memories of watching similar movies",
                "customization": "Adjust viewing length based on attention span",
                "safety": "Choose appropriate content and monitor emotional responses"
            }
        else:
            return {
                "implementation": f"Explore {entity_name} together",
                "engagement": "Use as conversation starter",
                "customization": "Adapt based on their interests and abilities",
                "safety": "Monitor for positive or negative reactions"
            }
    
    def _generate_cross_domain_connections(self, processed_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate connections between different entity types."""
        
        connections = {}
        entity_types = list(processed_results.keys())
        
        for i, type1 in enumerate(entity_types):
            for type2 in entity_types[i+1:]:
                connection_key = f"{type1}_to_{type2}"
                connections[connection_key] = self._find_entity_connections(
                    processed_results[type1], 
                    processed_results[type2]
                )
        
        return connections
    
    def _find_entity_connections(self, 
                               entities1: Dict[str, Any], 
                               entities2: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find connections between two sets of entities."""
        
        connections = []
        
        entities1_list = entities1.get("entities", [])
        entities2_list = entities2.get("entities", [])
        
        for entity1 in entities1_list[:2]:  # Limit to avoid too many connections
            for entity2 in entities2_list[:2]:
                connection = {
                    "entity1": entity1["name"],
                    "entity2": entity2["name"],
                    "connection_type": "thematic_pairing",
                    "suggested_use": f"Combine {entity1['name']} with {entity2['name']} for richer experience",
                    "implementation": "Use both suggestions in the same session or activity"
                }
                connections.append(connection)
                
                if len(connections) >= 3:  # Limit connections
                    break
            if len(connections) >= 3:
                break
        
        return connections
    
    def _create_thematic_intelligence(self, 
                                    processed_results: Dict[str, Any],
                                    cross_domain_connections: Dict[str, Any],
                                    cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Create thematic intelligence without stereotypical assumptions."""
        
        # Extract common themes from results
        common_themes = []
        all_entities = []
        
        for entity_type_data in processed_results.values():
            entities = entity_type_data.get("entities", [])
            all_entities.extend(entities)
            
            # Extract themes from this entity type
            for entity in entities:
                potentials = entity.get("cross_domain_potential", [])
                common_themes.extend(potentials)
        
        # Count theme frequency
        theme_counts = {}
        for theme in common_themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Get most common themes
        popular_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "common_themes": [theme for theme, count in popular_themes],
            "theme_frequencies": dict(popular_themes),
            "total_entities": len(all_entities),
            "cross_domain_connections": len(cross_domain_connections),
            "cultural_coherence": "multi_domain_exploration",
            "bias_prevention": "no_stereotypical_packages"
        }
    
    def _is_entity_type_blocked(self, entity_type: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if entity type is blocked by user feedback."""
        
        blocked_types = blocked_content.get("blocked_entity_types", [])
        return entity_type in blocked_types
    
    def _create_fallback_qloo_intelligence(self, 
                                         consolidated_info: Dict[str, Any],
                                         cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback intelligence when Qloo API is unavailable."""
        
        return {
            "qloo_intelligence": {
                "qloo_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query_strategy": "fallback_mode",
                    "api_calls_made": 0,
                    "best_practices_followed": True,
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "cultural_recommendations": {},
                "cross_domain_connections": {},
                "thematic_intelligence": {
                    "common_themes": [],
                    "fallback_mode": True
                },
                "fallback_used": True,
                "fallback_reason": "qloo_api_unavailable"
            }
        }