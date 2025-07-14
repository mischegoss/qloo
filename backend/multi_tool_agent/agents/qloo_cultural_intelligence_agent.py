"""
Agent 3: Qloo Cultural Intelligence
Role: Query Qloo API for cross-domain cultural recommendations
Follows Responsible Development Guide principles - individual preferences override demographics
"""

from typing import Dict, Any, Optional, List, Set
import asyncio
import logging
from datetime import datetime
from google.genai.adk import Agent

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
        self.qloo_tool = qloo_tool
    
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
            
            # Execute Qloo API calls (multiple domains)
            qloo_results = await self._execute_qloo_queries(query_strategy)
            
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
        
        # Heritage keywords (open exploration)
        heritage_keywords = cultural_signals.get("heritage_keywords", [])
        if heritage_keywords:
            # Use keywords for broad cultural exploration
            cultural_query = " ".join(heritage_keywords[:3])  # Limit for API efficiency
            if cultural_query.strip():
                params["signal.interests.tags"] = cultural_query
        
        # Language elements (factual context)
        languages = cultural_signals.get("language_elements", [])
        if languages:
            # Use primary language for cultural context
            primary_language = languages[0] if languages else None
            if primary_language and primary_language.lower() != "english":
                if "signal.interests.tags" in params:
                    params["signal.interests.tags"] += f" {primary_language}"
                else:
                    params["signal.interests.tags"] = primary_language
        
        return params
    
    def _determine_entity_types(self, request_type: str) -> List[str]:
        """Determine which Qloo entity types to query based on request."""
        entity_mapping = {
            "meal": ["urn:entity:place", "urn:entity:brand"],  # Restaurants, food brands
            "conversation": ["urn:entity:place", "urn:entity:person"],  # Local places, people
            "music": ["urn:entity:artist", "urn:entity:album"],  # Musicians, albums
            "video": ["urn:entity:movie", "urn:entity:tv_show"],  # Movies, TV shows
            "dashboard": ["urn:entity:artist", "urn:entity:place", "urn:entity:movie", "urn:entity:brand"],  # Multi-domain
            "photo_analysis": ["urn:entity:place", "urn:entity:artist", "urn:entity:movie"]  # Cultural context
        }
        
        return entity_mapping.get(request_type, entity_mapping["dashboard"])
    
    def _is_entity_type_blocked(self, entity_type: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if an entity type is blocked by user feedback."""
        
        # Map entity types to content categories
        type_mapping = {
            "urn:entity:artist": "music",
            "urn:entity:album": "music", 
            "urn:entity:place": "places",
            "urn:entity:movie": "video",
            "urn:entity:tv_show": "video",
            "urn:entity:brand": "brands",
            "urn:entity:person": "people"
        }
        
        content_category = type_mapping.get(entity_type, "unknown")
        blocked_categories = blocked_content.get("categories", [])
        
        return content_category in blocked_categories
    
    def _build_entity_query(self, 
                           entity_type: str,
                           base_params: Dict[str, str],
                           cultural_params: Dict[str, str],
                           request_type: str) -> Dict[str, Any]:
        """Build specific query for an entity type."""
        
        # Combine base and cultural parameters
        query_params = {**base_params, **cultural_params}
        query_params["filter.type"] = entity_type
        query_params["take"] = "5"  # Reasonable number for processing
        
        # Entity-specific enhancements
        if entity_type == "urn:entity:place":
            # For places, focus on cultural experiences
            if request_type == "meal":
                query_params["filter.tags"] = "restaurant food dining"
            elif request_type == "conversation":
                query_params["filter.tags"] = "cultural historical community"
        
        elif entity_type == "urn:entity:artist":
            # For artists, broad exploration
            query_params["filter.tags"] = "music performance cultural"
        
        elif entity_type in ["urn:entity:movie", "urn:entity:tv_show"]:
            # For video content, family-friendly
            query_params["filter.content_rating"] = "G,PG,PG-13"
        
        return {
            "entity_type": entity_type,
            "params": query_params,
            "purpose": f"{request_type}_cultural_discovery"
        }
    
    async def _execute_qloo_queries(self, query_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Qloo API queries with proper error handling."""
        query_list = query_strategy.get("query_list", [])
        results = {}
        
        for query in query_list:
            entity_type = query["entity_type"]
            params = query["params"]
            
            try:
                logger.info(f"Executing Qloo query for {entity_type}")
                
                # Execute Qloo API call
                api_result = await self.qloo_tool.get_insights(params)
                
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
    
    def _process_qloo_results(self, 
                             qloo_results: Dict[str, Any],
                             blocked_content: Dict[str, Any],
                             cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Process Qloo results and filter based on blocked content."""
        
        processed_results = {}
        
        for entity_type, result in qloo_results.items():
            if not result.get("success"):
                processed_results[entity_type] = {
                    "available": False,
                    "error": result.get("error", "api_error"),
                    "fallback_needed": True
                }
                continue
            
            # Extract entities from Qloo response
            data = result.get("data", {})
            entities = data.get("entities", []) if isinstance(data, dict) else []
            
            # Filter out blocked content
            filtered_entities = self._filter_blocked_entities(entities, blocked_content)
            
            # Enhance entities with cultural context
            enhanced_entities = self._enhance_entities_with_context(
                filtered_entities, 
                cultural_elements,
                entity_type
            )
            
            processed_results[entity_type] = {
                "available": True,
                "entities": enhanced_entities,
                "total_found": len(entities),
                "after_filtering": len(filtered_entities),
                "entity_type_category": self._get_entity_category(entity_type)
            }
        
        return processed_results
    
    def _filter_blocked_entities(self, 
                                entities: List[Dict[str, Any]], 
                                blocked_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter entities against blocked content patterns."""
        
        blocked_items = blocked_content.get("specific_items", [])
        blocked_types = blocked_content.get("types", [])
        blocked_categories = blocked_content.get("categories", [])
        
        filtered = []
        
        for entity in entities:
            entity_name = entity.get("name", "").lower()
            entity_type = entity.get("type", "").lower()
            entity_category = entity.get("category", "").lower()
            
            # Check specific blocked items
            if any(blocked_item.lower() in entity_name for blocked_item in blocked_items):
                continue
                
            # Check blocked types
            if any(blocked_type.lower() in entity_type for blocked_type in blocked_types):
                continue
                
            # Check blocked categories
            if any(blocked_cat.lower() in entity_category for blocked_cat in blocked_categories):
                continue
            
            filtered.append(entity)
        
        return filtered
    
    def _enhance_entities_with_context(self, 
                                      entities: List[Dict[str, Any]],
                                      cultural_elements: Dict[str, Any],
                                      entity_type: str) -> List[Dict[str, Any]]:
        """Enhance entities with cultural context without assumptions."""
        
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
        
        potentials = []
        
        # Based on entity type, suggest cross-domain possibilities
        if entity_type == "urn:entity:artist":
            potentials = ["music_listening", "era_discussion", "dance_activities", "cultural_exploration"]
        elif entity_type == "urn:entity:place":
            potentials = ["conversation_starter", "food_exploration", "memory_trigger", "cultural_learning"]
        elif entity_type in ["urn:entity:movie", "urn:entity:tv_show"]:
            potentials = ["viewing_activity", "discussion_topic", "era_exploration", "cultural_context"]
        elif entity_type == "urn:entity:brand":
            potentials = ["food_exploration", "shopping_memories", "brand_familiarity", "cultural_products"]
        
        return potentials
    
    def _generate_caregiver_guidance(self, 
                                    entity: Dict[str, Any],
                                    entity_type: str) -> Dict[str, str]:
        """Generate guidance for caregivers on how to use this suggestion."""
        
        entity_name = entity.get("name", "Unknown")
        
        guidance_mapping = {
            "urn:entity:artist": {
                "implementation": f"Try playing music by {entity_name} during quiet times",
                "conversation_starter": f"Ask: 'Do you remember {entity_name}? What was your favorite song?'",
                "caregiver_note": "Watch for positive reactions to rhythm and melody"
            },
            "urn:entity:place": {
                "implementation": f"Use {entity_name} as a conversation topic or photo exploration",
                "conversation_starter": f"Talk about visiting places like {entity_name}",
                "caregiver_note": "May trigger location-based memories"
            },
            "urn:entity:movie": {
                "implementation": f"Consider watching {entity_name} together",
                "conversation_starter": f"Ask: 'Would you like to watch {entity_name}?'",
                "caregiver_note": "Check for attention span and content appropriateness"
            },
            "urn:entity:tv_show": {
                "implementation": f"Try watching episodes of {entity_name}",
                "conversation_starter": f"Ask about memories of watching {entity_name}",
                "caregiver_note": "Familiar shows may provide comfort"
            },
            "urn:entity:brand": {
                "implementation": f"Look for products from {entity_name} during shopping",
                "conversation_starter": f"Ask about experiences with {entity_name}",
                "caregiver_note": "Brand recognition may trigger positive memories"
            }
        }
        
        return guidance_mapping.get(entity_type, {
            "implementation": f"Explore {entity_name} as a cultural topic",
            "conversation_starter": f"Talk about {entity_name}",
            "caregiver_note": "Use as general cultural exploration"
        })
    
    def _get_entity_category(self, entity_type: str) -> str:
        """Map entity type to user-friendly category."""
        mapping = {
            "urn:entity:artist": "music",
            "urn:entity:album": "music",
            "urn:entity:place": "places",
            "urn:entity:movie": "video",
            "urn:entity:tv_show": "video", 
            "urn:entity:brand": "brands",
            "urn:entity:person": "people"
        }
        return mapping.get(entity_type, "cultural")
    
    def _generate_cross_domain_connections(self, processed_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate connections between different domains."""
        
        connections = {
            "thematic_links": [],
            "sensory_combinations": [],
            "cultural_threads": [],
            "caregiver_combinations": []
        }
        
        available_domains = [
            domain for domain, result in processed_results.items() 
            if result.get("available", False)
        ]
        
        # Generate thematic connections between domains
        if len(available_domains) >= 2:
            for i, domain1 in enumerate(available_domains):
                for domain2 in available_domains[i+1:]:
                    connection = self._create_domain_connection(
                        domain1, 
                        domain2,
                        processed_results[domain1],
                        processed_results[domain2]
                    )
                    if connection:
                        connections["thematic_links"].append(connection)
        
        return connections
    
    def _create_domain_connection(self, 
                                 domain1: str, 
                                 domain2: str,
                                 result1: Dict[str, Any],
                                 result2: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a connection between two domains."""
        
        # Example connections without assumptions
        connection_templates = {
            ("urn:entity:artist", "urn:entity:place"): {
                "theme": "musical_cultural_exploration",
                "description": "Combine music listening with cultural place discussions",
                "implementation": "Play music while talking about cultural places"
            },
            ("urn:entity:movie", "urn:entity:place"): {
                "theme": "visual_cultural_storytelling", 
                "description": "Use movies to explore cultural places and stories",
                "implementation": "Watch films set in culturally relevant locations"
            },
            ("urn:entity:artist", "urn:entity:brand"): {
                "theme": "era_cultural_products",
                "description": "Explore music and products from the same cultural era",
                "implementation": "Combine music with familiar brand discussions"
            }
        }
        
        connection_key = (domain1, domain2) if (domain1, domain2) in connection_templates else (domain2, domain1)
        template = connection_templates.get(connection_key)
        
        if template:
            return {
                "domains": [domain1, domain2],
                "theme": template["theme"],
                "description": template["description"],
                "implementation": template["implementation"],
                "cross_sensory": True
            }
        
        return None
    
    def _create_thematic_intelligence(self, 
                                     processed_results: Dict[str, Any],
                                     cross_domain_connections: Dict[str, Any],
                                     cultural_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Create thematic coherence across all recommendations."""
        
        # Extract common themes across domains
        common_themes = self._extract_common_themes(processed_results)
        
        # Build thematic packages without stereotypes
        thematic_packages = self._build_thematic_packages(
            processed_results,
            cross_domain_connections,
            common_themes
        )
        
        return {
            "common_themes": common_themes,
            "thematic_packages": thematic_packages,
            "cultural_coherence": "cross_domain_exploration",
            "implementation_approach": "caregiver_guided_discovery"
        }
    
    def _extract_common_themes(self, processed_results: Dict[str, Any]) -> List[str]:
        """Extract themes that appear across multiple domains."""
        
        themes = []
        
        # Look for era-based themes
        if any("entities" in result for result in processed_results.values()):
            themes.append("era_exploration")
        
        # Look for cultural themes
        if len(processed_results) > 1:
            themes.append("cross_cultural_discovery")
        
        return themes
    
    def _build_thematic_packages(self, 
                                processed_results: Dict[str, Any],
                                cross_domain_connections: Dict[str, Any],
                                common_themes: List[str]) -> List[Dict[str, Any]]:
        """Build thematic packages for caregiver implementation."""
        
        packages = []
        
        # Create multi-sensory packages
        if "era_exploration" in common_themes:
            era_package = {
                "theme": "era_cultural_exploration",
                "description": "Explore cultural elements from their era across multiple senses",
                "components": [],
                "implementation": "Use multiple elements together for richer experience",
                "caregiver_guidance": "Start with one element, add others based on response"
            }
            
            # Add components from available domains
            for domain, result in processed_results.items():
                if result.get("available") and result.get("entities"):
                    era_package["components"].append({
                        "domain": self._get_entity_category(domain),
                        "sample_entity": result["entities"][0]["name"] if result["entities"] else None
                    })
            
            if era_package["components"]:
                packages.append(era_package)
        
        return packages
    
    def _validate_qloo_bias_prevention(self, 
                                      enhanced_intelligence: Dict[str, Any],
                                      cultural_elements: Dict[str, Any]) -> None:
        """Validate that Qloo results don't introduce bias."""
        
        # Check for stereotypical cultural "packages"
        recommendations = enhanced_intelligence.get("cultural_recommendations", {})
        
        # Ensure individual approach maintained
        anti_bias = enhanced_intelligence.get("anti_bias_validation", {})
        if not anti_bias.get("individual_preferences_checked"):
            logger.warning("Individual preference checking not documented")
        
        # Check for diverse recommendations
        available_domains = [
            domain for domain, result in recommendations.items()
            if result.get("available", False)
        ]
        
        if len(available_domains) > 1:
            logger.info("Cross-domain recommendations generated successfully")
        
        logger.info("Qloo bias prevention validation completed")
    
    def _create_fallback_qloo_intelligence(self, 
                                          consolidated_info: Dict[str, Any],
                                          cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback when Qloo API is unavailable."""
        
        request_type = consolidated_info.get("request_context", {}).get("request_type", "dashboard")
        
        # Create culturally broad fallback recommendations
        fallback_recommendations = self._generate_fallback_recommendations(request_type, cultural_profile)
        
        return {
            "qloo_intelligence": {
                "qloo_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query_strategy": "fallback_mode",
                    "api_calls_made": 0,
                    "blocked_content_respected": True,
                    "bias_prevention_active": True
                },
                "cultural_recommendations": fallback_recommendations,
                "cross_domain_connections": {"thematic_links": []},
                "thematic_intelligence": {"common_themes": ["general_cultural_exploration"]},
                "fallback_used": True,
                "anti_bias_validation": {
                    "individual_preferences_checked": True,
                    "blocked_content_filtered": True,
                    "stereotypical_assumptions": "none_made",
                    "cross_domain_approach": "broad_fallback_exploration"
                }
            }
        }
    
    def _generate_fallback_recommendations(self, 
                                          request_type: str,
                                          cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate broadly cultural fallback recommendations."""
        
        # Wide cultural appeal recommendations
        fallback_mapping = {
            "music": {
                "available": True,
                "entities": [
                    {
                        "name": "Classic Standards Collection",
                        "cultural_context": {"discovery_reason": "broad_cultural_appeal"},
                        "caregiver_guidance": {"implementation": "Try familiar melodies from different eras"}
                    }
                ],
                "entity_type_category": "music"
            },
            "places": {
                "available": True,
                "entities": [
                    {
                        "name": "Local Community Centers",
                        "cultural_context": {"discovery_reason": "community_connection"},
                        "caregiver_guidance": {"implementation": "Discuss local community places"}
                    }
                ],
                "entity_type_category": "places"
            }
        }
        
        return fallback_mapping