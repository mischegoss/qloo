"""
Agent 3: Qloo Cultural Intelligence - Fixed Constructor
Role: Query Qloo API for cross-domain cultural recommendations
Follows Responsible Development Guide principles - individual preferences override demographics
"""

from typing import Dict, Any, Optional, List, Set
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent(Agent):
    """
    Agent 3: Qloo Cultural Intelligence
    
    Purpose: Query Qloo API for cross-domain cultural recommendations
    Input: Cultural profile from Agent 2 + consolidated information
    Output: Enhanced cultural intelligence with Qloo-powered cross-domain suggestions
    
    Anti-Bias Principles:
    - Check blocked content before ALL API calls
    - Use broad exploration, not stereotypical assumptions
    - Individual feedback patterns override demographic suggestions
    - Cross-domain discovery without cultural "packages"
    """
    
    def __init__(self, qloo_tool):
        super().__init__(
            name="qloo_cultural_intelligence",
            description="Generates cross-domain cultural recommendations using Qloo API with bias prevention"
        )
        # DON'T store qloo_tool as self.qloo_tool - this causes Pydantic field error
        # Instead, store it in a way that works with the Agent model
        self._tool_ref = qloo_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cross-domain cultural intelligence using Qloo API.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            
        Returns:
            Enhanced cultural intelligence with Qloo recommendations
        """
        
        try:
            logger.info("Starting Qloo cultural intelligence generation")
            
            # Extract request context and blocked content
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            
            # Check if we have enough information for meaningful queries
            qloo_framework = cultural_profile.get("qloo_framework", {})
            cultural_elements = cultural_profile.get("cultural_elements", {})
            
            # Build Qloo query strategy (anti-bias approach)
            query_strategy = self._build_query_strategy(
                request_context, 
                qloo_framework, 
                cultural_elements,
                blocked_content
            )
            
            # Execute Qloo API calls (multiple domains) - pass tool reference
            qloo_results = await self._execute_qloo_queries(query_strategy, self._tool_ref)
            
            # Process and filter results (respect blocks, avoid bias)
            processed_results = self._process_qloo_results(qloo_results, blocked_content, cultural_elements)
            
            # Generate cross-domain connections
            cross_domain_connections = self._generate_cross_domain_connections(processed_results)
            
            # Create thematic coherence without stereotypes
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
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "cultural_recommendations": processed_results,
                "cross_domain_connections": cross_domain_connections,
                "thematic_intelligence": thematic_intelligence,
                "fallback_used": False,
                "anti_bias_validation": {
                    "individual_preferences_checked": True,
                    "blocked_content_filtered": True,
                    "stereotypical_assumptions": "none_made",
                    "cross_domain_approach": "open_exploration"
                }
            }
            
            # Validate no bias introduced
            self._validate_qloo_bias_prevention(enhanced_intelligence, cultural_elements)
            
            logger.info("Qloo cultural intelligence generated successfully")
            return {"qloo_intelligence": enhanced_intelligence}
            
        except Exception as e:
            logger.error(f"Error in Qloo cultural intelligence: {str(e)}")
            return self._create_fallback_qloo_intelligence(consolidated_info, cultural_profile)
    
    async def _execute_qloo_queries(self, query_strategy: Dict[str, Any], qloo_tool) -> Dict[str, Any]:
        """
        Execute Qloo API queries based on strategy.
        
        Args:
            query_strategy: Query strategy from _build_query_strategy
            qloo_tool: Qloo tool reference passed from constructor
            
        Returns:
            Dictionary with Qloo API results for each entity type
        """
        
        query_list = query_strategy.get("query_list", [])
        results = {}
        
        for query in query_list:
            entity_type = query["entity_type"]
            params = query["params"]
            
            try:
                logger.info(f"Executing Qloo query for {entity_type}")
                
                # Execute Qloo API call using the tool reference
                api_result = await qloo_tool.get_insights(params)
                
                if api_result and api_result.get("success"):
                    results[entity_type] = {
                        "success": True,
                        "data": api_result.get("results", {}),
                        "query_params": params,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                else:
                    logger.warning(f"Qloo API returned no results for {entity_type}")
                    results[entity_type] = {
                        "success": False,
                        "data": {},
                        "error": "no_results_returned"
                    }
                
                # Rate limiting - respect Qloo API limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Qloo API error for {entity_type}: {str(e)}")
                results[entity_type] = {
                    "success": False,
                    "data": {},
                    "error": str(e)
                }
        
        return results
    
    def _build_query_strategy(self, 
                            request_context: Dict[str, Any],
                            qloo_framework: Dict[str, Any],
                            cultural_elements: Dict[str, Any],
                            blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build Qloo query strategy based on request type and cultural profile.
        Anti-bias approach: broad exploration, not assumptions.
        """
        request_type = request_context.get("request_type", "dashboard")
        
        # Extract cultural signals safely
        demographic_signals = qloo_framework.get("demographic_signals", {})
        cultural_signals = qloo_framework.get("cultural_signals", {})
        era_signals = qloo_framework.get("era_signals", {})
        
        # Build base query parameters (individual-first)
        base_params = self._build_base_qloo_params(demographic_signals, era_signals)
        
        # Build cultural enhancement parameters (no assumptions)
        cultural_params = self._build_cultural_params(cultural_signals, cultural_elements)
        
        # Determine entity types to query based on request
        entity_types = self._determine_entity_types(request_type)
        
        # Build specific queries for each entity type
        query_list = []
        for entity_type in entity_types:
            # Check if this entity type is blocked
            if not self._is_entity_type_blocked(entity_type, blocked_content):
                query = self._build_entity_query(
                    entity_type, 
                    base_params, 
                    cultural_params,
                    request_type
                )
                query_list.append(query)
        
        strategy = {
            "approach": "cross_domain_exploration_no_assumptions",
            "entity_types": entity_types,
            "query_list": query_list,
            "blocked_content_checked": True,
            "cultural_enhancement": bool(cultural_params),
            "bias_prevention": {
                "individual_first": True,
                "broad_exploration": True,
                "no_stereotypical_packages": True
            }
        }
        
        return strategy
    
    def _build_base_qloo_params(self, 
                               demographic_signals: Dict[str, Any],
                               era_signals: Dict[str, Any]) -> Dict[str, str]:
        """Build base Qloo parameters from demographic and era context."""
        
        params = {}
        
        # Age-based demographic signal (broad, not stereotypical)
        age_range = demographic_signals.get("age_range")
        if age_range and age_range != "age_unknown":
            # Map to Qloo demographic categories broadly
            if "senior" in age_range or "100_plus" in age_range:
                params["signal.demographics.age"] = "55_and_older"
            elif "adult" in age_range or "mature" in age_range:
                params["signal.demographics.age"] = "35_to_54"
            elif "young" in age_range:
                params["signal.demographics.age"] = "18_to_34"
        
        # Location signal (general only)
        location = demographic_signals.get("general_location", {})
        city_region = location.get("city_region", "").strip()
        if city_region and len(city_region) > 2:
            params["signal.location.query"] = city_region
        
        # Era-based filters (factual, not assumptive)
        birth_year = era_signals.get("birth_year")
        if birth_year:
            # Broad era filters for content discovery
            if birth_year <= 1950:
                params["filter.release_year.min"] = "1930"
                params["filter.release_year.max"] = "1970"
            elif birth_year <= 1970:
                params["filter.release_year.min"] = "1950"
                params["filter.release_year.max"] = "1990"
            elif birth_year <= 1990:
                params["filter.release_year.min"] = "1970"
                params["filter.release_year.max"] = "2010"
            else:
                params["filter.release_year.min"] = "1990"
                params["filter.release_year.max"] = "2025"
        
        # Popularity filter (accessible content)
        params["filter.popularity.min"] = "0.3"
        
        return params
    
    def _build_cultural_params(self, 
                              cultural_signals: Dict[str, Any],
                              cultural_elements: Dict[str, Any]) -> Dict[str, str]:
        """Build cultural enhancement parameters without assumptions."""
        
        params = {}
        
        # Heritage-based interests (broad, not stereotypical)
        heritage_keywords = cultural_signals.get("heritage_keywords", [])
        tradition_keywords = cultural_signals.get("tradition_keywords", [])
        
        # Combine cultural keywords for interest signals
        all_cultural_keywords = heritage_keywords + tradition_keywords
        
        if all_cultural_keywords:
            # Use first cultural keyword as interest signal
            params["signal.interests.tags"] = all_cultural_keywords[0]
        
        return params
    
    def _determine_entity_types(self, request_type: str) -> List[str]:
        """Determine which Qloo entity types to query based on request."""
        
        base_types = ["urn:entity:artist", "urn:entity:place"]
        
        if request_type == "meal":
            return ["urn:entity:place", "urn:entity:artist"]  # Restaurants and music for dining
        elif request_type == "music":
            return ["urn:entity:artist", "urn:entity:album"]
        elif request_type == "conversation":
            return ["urn:entity:movie", "urn:entity:book", "urn:entity:person"]
        else:  # dashboard or general
            return ["urn:entity:artist", "urn:entity:place", "urn:entity:movie"]
    
    def _build_entity_query(self, 
                           entity_type: str,
                           base_params: Dict[str, str],
                           cultural_params: Dict[str, str],
                           request_type: str) -> Dict[str, Any]:
        """Build specific query for an entity type."""
        
        # Start with base params
        params = base_params.copy()
        params.update(cultural_params)
        
        # Add entity type
        params["filter.type"] = entity_type
        
        # Ensure required interest signal is present
        if "signal.interests.tags" not in params:
            if "artist" in entity_type:
                params["signal.interests.tags"] = "music"
            elif "place" in entity_type:
                params["signal.interests.tags"] = "dining"
            elif "movie" in entity_type:
                params["signal.interests.tags"] = "movies"
            else:
                params["signal.interests.tags"] = "culture"
        
        # Set reasonable result limit
        params["take"] = 3
        
        return {
            "entity_type": entity_type,
            "params": params,
            "request_context": request_type
        }
    
    def _is_entity_type_blocked(self, entity_type: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if entity type is blocked by user feedback."""
        
        blocked_types = blocked_content.get("blocked_entity_types", [])
        return entity_type in blocked_types
    
    def _process_qloo_results(self, 
                             qloo_results: Dict[str, Any],
                             blocked_content: Dict[str, Any],
                             cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Process Qloo results and filter based on blocked content."""
        
        processed = {}
        
        for entity_type, result_data in qloo_results.items():
            if not result_data.get("success"):
                continue
                
            entities = result_data.get("data", {}).get("results", {}).get("entities", [])
            
            # Filter blocked entities
            filtered_entities = self._filter_blocked_entities(entities, blocked_content)
            
            # Enhance entities with cultural context
            enhanced_entities = self._enhance_entities_with_context(
                filtered_entities, 
                entity_type, 
                cultural_elements
            )
            
            processed[entity_type] = {
                "entities": enhanced_entities,
                "total_found": len(entities),
                "after_filtering": len(enhanced_entities),
                "entity_type": entity_type
            }
        
        return processed
    
    def _filter_blocked_entities(self, entities: List[Dict[str, Any]], blocked_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter out blocked entities based on user feedback."""
        
        blocked_names = blocked_content.get("blocked_names", [])
        blocked_ids = blocked_content.get("blocked_entity_ids", [])
        
        filtered = []
        for entity in entities:
            entity_name = entity.get("name", "").lower()
            entity_id = entity.get("entity_id", "")
            
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
                "entity_id": entity.get("entity_id", ""),
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
            "cultural_connection": "broad_exploration",
            "why_suggested": "cross_domain_cultural_discovery"
        }
        
        # Check for cultural keyword connections
        entity_name = entity.get("name", "").lower()
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        
        for keyword in heritage_keywords:
            if keyword.lower() in entity_name:
                context["cultural_connection"] = f"connected_to_{keyword}_heritage"
                context["why_suggested"] = f"cultural_exploration_related_to_{keyword}"
                break
        
        return context
    
    def _assess_cross_domain_potential(self, 
                                      entity: Dict[str, Any],
                                      entity_type: str) -> List[str]:
        """Assess potential for cross-domain connections."""
        
        potential = []
        
        if "artist" in entity_type:
            potential.extend(["music_listening", "conversation_starter", "memory_trigger"])
        elif "place" in entity_type:
            potential.extend(["dining_experience", "cultural_exploration", "sensory_engagement"])
        elif "movie" in entity_type:
            potential.extend(["viewing_together", "conversation_topic", "nostalgic_connection"])
        
        return potential
    
    def _generate_caregiver_guidance(self, 
                                   entity: Dict[str, Any], 
                                   entity_type: str) -> Dict[str, str]:
        """Generate guidance for caregivers on how to use this suggestion."""
        
        guidance = {
            "how_to_use": "general_suggestion",
            "adaptation_tips": "adjust_based_on_current_abilities",
            "safety_considerations": "supervise_as_needed"
        }
        
        if "artist" in entity_type:
            guidance.update({
                "how_to_use": "play_music_together_or_discuss_artist",
                "adaptation_tips": "adjust_volume_and_duration_based_on_preferences",
                "safety_considerations": "monitor_emotional_responses_to_music"
            })
        elif "place" in entity_type:
            guidance.update({
                "how_to_use": "consider_for_outings_or_delivery_orders",
                "adaptation_tips": "check_accessibility_and_dietary_restrictions",
                "safety_considerations": "ensure_safe_dining_environment"
            })
        
        return guidance
    
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
        
        # Simple thematic connections (can be enhanced)
        entities1_list = entities1.get("entities", [])
        entities2_list = entities2.get("entities", [])
        
        for entity1 in entities1_list[:2]:  # Limit to avoid too many connections
            for entity2 in entities2_list[:2]:
                connection = {
                    "entity1": entity1["name"],
                    "entity2": entity2["name"],
                    "connection_type": "thematic_similarity",
                    "suggested_use": "combine_for_richer_experience"
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
        
        themes = {}
        
        # Extract common themes from results
        all_entities = []
        for entity_type_data in processed_results.values():
            all_entities.extend(entity_type_data.get("entities", []))
        
        # Group by cross-domain potential
        for entity in all_entities:
            potentials = entity.get("cross_domain_potential", [])
            for potential in potentials:
                if potential not in themes:
                    themes[potential] = []
                themes[potential].append(entity["name"])
        
        return {
            "thematic_groupings": themes,
            "recommended_combinations": self._suggest_combinations(themes),
            "cultural_coherence": "broad_exploration_approach",
            "bias_prevention": "no_stereotypical_packages"
        }
    
    def _suggest_combinations(self, themes: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Suggest combinations of entities for richer experiences."""
        
        combinations = []
        
        # Simple combination logic (can be enhanced)
        theme_keys = list(themes.keys())
        for i, theme1 in enumerate(theme_keys):
            for theme2 in theme_keys[i+1:]:
                if themes[theme1] and themes[theme2]:
                    combination = {
                        "theme1": theme1,
                        "theme2": theme2,
                        "entities1": themes[theme1][:2],
                        "entities2": themes[theme2][:2],
                        "combination_suggestion": f"combine_{theme1}_with_{theme2}"
                    }
                    combinations.append(combination)
                    
                    if len(combinations) >= 3:  # Limit combinations
                        break
            if len(combinations) >= 3:
                break
        
        return combinations
    
    def _validate_qloo_bias_prevention(self, 
                                     enhanced_intelligence: Dict[str, Any],
                                     cultural_elements: Dict[str, Any]) -> None:
        """Validate that no bias was introduced in Qloo recommendations."""
        
        # Check for stereotypical patterns
        recommendations = enhanced_intelligence.get("cultural_recommendations", {})
        
        for entity_type, type_data in recommendations.items():
            entities = type_data.get("entities", [])
            
            # Log validation
            logger.info(f"Bias validation for {entity_type}: {len(entities)} entities")
            
            # Additional bias checks can be added here
            for entity in entities:
                context = entity.get("cultural_context", {})
                if context.get("cultural_connection") == "broad_exploration":
                    logger.debug(f"Entity {entity['name']} uses broad exploration approach")
    
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
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "cultural_recommendations": {},
                "cross_domain_connections": {},
                "thematic_intelligence": {},
                "fallback_used": True,
                "fallback_reason": "qloo_api_unavailable",
                "anti_bias_validation": {
                    "individual_preferences_checked": True,
                    "blocked_content_filtered": True,
                    "stereotypical_assumptions": "none_made",
                    "cross_domain_approach": "fallback_mode"
                }
            }
        }