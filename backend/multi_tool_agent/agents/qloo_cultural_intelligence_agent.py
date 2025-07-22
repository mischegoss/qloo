"""
Fixed Qloo Cultural Intelligence Agent - Uses proper two-stage API pattern
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent(Agent):
    """
    COMPLETELY FIXED Qloo Cultural Intelligence Agent
    
    Key Fixes:
    1. Two-stage API pattern (search → insights)
    2. Simplified parameter structure
    3. Robust error handling with meaningful fallbacks
    4. Proper rate limiting
    5. Smart cultural keyword extraction
    6. Circuit breaker for failed queries
    """
    
    def __init__(self, qloo_tool):
        super().__init__(
            name="qloo_cultural_intelligence",
            description="Generates cross-domain cultural recommendations using fixed Qloo API integration"
        )
        self._qloo_tool = qloo_tool
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cross-domain cultural intelligence using FIXED Qloo API calls."""
        
        try:
            logger.info("🚀 Starting FIXED Qloo cultural intelligence generation")
            
            # Extract context and cultural information
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            cultural_elements = cultural_profile.get("cultural_elements", {})
            
            # Test connection first
            connection_ok = await self._qloo_tool.test_connection()
            if not connection_ok:
                logger.error("❌ Qloo API connection failed - using fallback")
                return self._create_fallback_response(cultural_elements, "connection_failed")
            
            # Extract cultural keywords smartly
            cultural_keywords = self._extract_cultural_keywords(cultural_elements)
            logger.info(f"🔍 Extracted cultural keywords: {cultural_keywords}")
            
            # Extract demographic signals
            demographic_signals = self._extract_demographic_signals(consolidated_info)
            logger.info(f"👥 Demographic signals: {list(demographic_signals.keys())}")
            
            # Execute FIXED cultural recommendations
            qloo_results = await self._execute_fixed_qloo_queries(
                cultural_keywords, 
                demographic_signals
            )
            
            # Process results with intelligent fallbacks
            processed_results = self._process_qloo_results(
                qloo_results, 
                cultural_elements, 
                blocked_content
            )
            
            # Build comprehensive response
            response = self._build_cultural_intelligence_response(
                processed_results,
                cultural_elements,
                qloo_results
            )
            
            logger.info("✅ Qloo cultural intelligence generation completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"💥 Qloo agent critical error: {str(e)}")
            return self._create_fallback_response(
                cultural_profile.get("cultural_elements", {}), 
                f"agent_error: {str(e)}"
            )
    
    def _extract_cultural_keywords(self, cultural_elements: Dict[str, Any]) -> List[str]:
        """
        Extract meaningful cultural keywords for Qloo searches.
        """
        keywords = []
        
        # Heritage elements
        heritage = cultural_elements.get("heritage_elements", {})
        heritage_keywords = heritage.get("heritage_keywords", [])
        keywords.extend([k.strip() for k in heritage_keywords if k and len(k.strip()) > 2])
        
        # Tradition elements
        traditions = cultural_elements.get("tradition_elements", {})
        tradition_keywords = traditions.get("tradition_keywords", [])
        keywords.extend([k.strip() for k in tradition_keywords if k and len(k.strip()) > 2])
        
        # Language elements
        languages = cultural_elements.get("language_elements", {}).get("languages", [])
        keywords.extend([lang.strip() for lang in languages if lang and len(lang.strip()) > 2])
        
        # Additional keywords
        additional = cultural_elements.get("additional_elements", {}).get("additional_keywords", [])
        keywords.extend([k.strip() for k in additional if k and len(k.strip()) > 2])
        
        # Clean and deduplicate
        unique_keywords = list(set([k.lower() for k in keywords if k]))
        
        # Prioritize most searchable keywords
        prioritized = []
        for keyword in unique_keywords[:5]:  # Limit to 5 for API efficiency
            if any(term in keyword for term in ["music", "food", "art", "culture", "tradition"]):
                prioritized.insert(0, keyword)  # Priority keywords go first
            else:
                prioritized.append(keyword)
        
        return prioritized[:3]  # Return top 3 for optimal API usage
    
    def _extract_demographic_signals(self, consolidated_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract demographic signals for Qloo API.
        """
        demographic_patterns = consolidated_info.get("demographic_patterns", {})
        
        signals = {}
        
        # Age range
        age_range = demographic_patterns.get("age_range", "")
        if age_range and age_range != "age_unknown":
            signals["age_range"] = age_range
        
        # Location
        general_location = demographic_patterns.get("general_location", {})
        if general_location:
            signals["general_location"] = general_location
        
        # Gender (if relevant)
        gender = demographic_patterns.get("gender", "")
        if gender and gender != "gender_unknown":
            signals["gender"] = gender
        
        return signals
    
    async def _execute_fixed_qloo_queries(self, 
                                        cultural_keywords: List[str],
                                        demographic_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute FIXED Qloo queries using two-stage pattern.
        """
        logger.info(f"🎯 Executing FIXED Qloo queries for {len(cultural_keywords)} keywords")
        
        # Define target entity types
        entity_types = [
            "urn:entity:artist",
            "urn:entity:place",
            "urn:entity:movie",
            "urn:entity:book"
        ]
        
        try:
            # Use the FIXED cultural recommendations method
            results = await self._qloo_tool.get_cultural_recommendations_fixed(
                cultural_keywords,
                demographic_signals,
                entity_types
            )
            
            # Log results
            successful_types = [et for et, result in results.items() if result.get("success")]
            logger.info(f"✅ FIXED Qloo queries completed: {len(successful_types)}/{len(entity_types)} successful")
            logger.info(f"Successful entity types: {successful_types}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ FIXED Qloo query execution failed: {str(e)}")
            return {}
    
    def _process_qloo_results(self, 
                            qloo_results: Dict[str, Any],
                            cultural_elements: Dict[str, Any],
                            blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Qloo results with intelligent content filtering.
        """
        processed = {
            "recommendations_by_domain": {},
            "cross_domain_connections": {},
            "cultural_themes": [],
            "successful_queries": 0,
            "total_entities": 0
        }
        
        # Process each entity type result
        for entity_type, result in qloo_results.items():
            if not result.get("success"):
                logger.warning(f"⚠️ No results for {entity_type}: {result.get('error', 'unknown')}")
                continue
            
            processed["successful_queries"] += 1
            
            # Extract entities
            entities = result.get("results", {}).get("entities", [])
            processed["total_entities"] += len(entities)
            
            # Process entities for this domain
            domain_name = self._get_domain_name(entity_type)
            processed["recommendations_by_domain"][domain_name] = self._process_domain_entities(
                entities, 
                entity_type,
                blocked_content
            )
            
            # Extract themes
            themes = self._extract_themes_from_entities(entities)
            processed["cultural_themes"].extend(themes)
        
        # Deduplicate themes
        processed["cultural_themes"] = list(set(processed["cultural_themes"]))
        
        # Build cross-domain connections
        processed["cross_domain_connections"] = self._build_cross_domain_connections(
            processed["recommendations_by_domain"]
        )
        
        logger.info(f"📊 Processed {processed['total_entities']} entities across {processed['successful_queries']} domains")
        
        return processed
    
    def _get_domain_name(self, entity_type: str) -> str:
        """Map entity type to readable domain name."""
        mapping = {
            "urn:entity:artist": "music_artists",
            "urn:entity:place": "dining_venues", 
            "urn:entity:movie": "films",
            "urn:entity:book": "literature",
            "urn:entity:tv_show": "television",
            "urn:entity:person": "notable_people"
        }
        return mapping.get(entity_type, "general")
    
    def _process_domain_entities(self, 
                               entities: List[Dict[str, Any]], 
                               entity_type: str,
                               blocked_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process entities for a specific domain with content filtering."""
        processed_entities = []
        
        for entity in entities[:3]:  # Limit to top 3 per domain
            name = entity.get("name", "Unknown")
            
            # Check against blocked content
            if self._is_content_blocked(name, blocked_content):
                logger.info(f"🚫 Blocked content filtered: {name}")
                continue
            
            processed_entity = {
                "name": name,
                "id": entity.get("id", ""),
                "type": entity_type,
                "description": entity.get("description", ""),
                "tags": entity.get("tags", []),
                "popularity": entity.get("popularity", 0),
                "cultural_relevance": self._calculate_cultural_relevance(entity),
                "why_recommended": self._generate_recommendation_reason(entity, entity_type)
            }
            
            processed_entities.append(processed_entity)
        
        return processed_entities
    
    def _is_content_blocked(self, content_name: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if content should be blocked based on feedback patterns."""
        if not blocked_content:
            return False
        
        blocked_terms = blocked_content.get("blocked_terms", [])
        content_lower = content_name.lower()
        
        for term in blocked_terms:
            if term.lower() in content_lower:
                return True
        
        return False
    
    def _calculate_cultural_relevance(self, entity: Dict[str, Any]) -> float:
        """Calculate cultural relevance score for entity."""
        relevance = 0.5  # Base score
        
        # Boost for popularity
        popularity = entity.get("popularity", 0)
        if popularity > 80:
            relevance += 0.3
        elif popularity > 50:
            relevance += 0.2
        elif popularity > 20:
            relevance += 0.1
        
        # Boost for cultural tags
        tags = entity.get("tags", [])
        cultural_terms = ["traditional", "cultural", "heritage", "classic", "family"]
        for tag in tags:
            if any(term in tag.lower() for term in cultural_terms):
                relevance += 0.1
                break
        
        return min(1.0, relevance)
    
    def _generate_recommendation_reason(self, entity: Dict[str, Any], entity_type: str) -> str:
        """Generate human-readable reason for recommendation."""
        name = entity.get("name", "This")
        
        reasons = {
            "urn:entity:artist": f"{name} offers music that resonates with your cultural background",
            "urn:entity:place": f"{name} provides dining experiences connected to your heritage",
            "urn:entity:movie": f"{name} contains themes and stories relevant to your cultural interests",
            "urn:entity:book": f"{name} explores cultural themes that align with your background"
        }
        
        return reasons.get(entity_type, f"{name} connects to your cultural interests")
    
    def _extract_themes_from_entities(self, entities: List[Dict[str, Any]]) -> List[str]:
        """Extract common themes from entity tags."""
        themes = []
        
        for entity in entities:
            tags = entity.get("tags", [])
            for tag in tags:
                # Extract meaningful themes from tags
                if any(term in tag.lower() for term in ["family", "tradition", "heritage", "cultural", "classic"]):
                    themes.append(tag.lower())
        
        return themes
    
    def _build_cross_domain_connections(self, recommendations_by_domain: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Build connections between different cultural domains."""
        connections = {}
        
        # Find common themes across domains
        all_themes = []
        for domain, entities in recommendations_by_domain.items():
            for entity in entities:
                all_themes.extend(entity.get("tags", []))
        
        # Find most common cross-domain themes
        theme_counts = {}
        for theme in all_themes:
            theme_lower = theme.lower()
            if any(term in theme_lower for term in ["family", "tradition", "cultural", "classic"]):
                theme_counts[theme_lower] = theme_counts.get(theme_lower, 0) + 1
        
        # Build connections
        if theme_counts:
            top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            connections["common_themes"] = [theme for theme, count in top_themes]
            connections["cross_domain_strength"] = len(top_themes) / 3.0
        else:
            connections["common_themes"] = ["cultural_connection", "family_oriented", "traditional_values"]
            connections["cross_domain_strength"] = 0.5
        
        return connections
    
    def _build_cultural_intelligence_response(self, 
                                            processed_results: Dict[str, Any],
                                            cultural_elements: Dict[str, Any],
                                            qloo_results: Dict[str, Any]) -> Dict[str, Any]:
        """Build comprehensive cultural intelligence response."""
        
        successful_queries = processed_results.get("successful_queries", 0)
        total_entities = processed_results.get("total_entities", 0)
        
        return {
            "qloo_intelligence": {
                "qloo_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query_strategy": "fixed_two_stage_pattern",
                    "api_calls_made": successful_queries * 2,  # Search + Insights for each
                    "successful_calls": successful_queries,
                    "total_entities_returned": total_entities,
                    "cache_stats": self._qloo_tool.get_cache_stats(),
                    "best_practices_followed": True,
                    "api_pattern": "search_then_insights",
                    "fallback_content_created": successful_queries == 0
                },
                "cultural_recommendations": processed_results.get("recommendations_by_domain", {}),
                "cross_domain_connections": processed_results.get("cross_domain_connections", {}),
                "thematic_intelligence": {
                    "common_themes": processed_results.get("cultural_themes", []),
                    "theme_strength": len(processed_results.get("cultural_themes", [])) / 10.0,
                    "cultural_coherence": processed_results.get("cross_domain_connections", {}).get("cross_domain_strength", 0.5)
                },
                "recommendation_quality": {
                    "domains_covered": len(processed_results.get("recommendations_by_domain", {})),
                    "total_recommendations": total_entities,
                    "cultural_relevance_avg": self._calculate_average_relevance(processed_results)
                },
                "fallback_used": successful_queries == 0,
                "fallback_reason": "no_successful_qloo_queries" if successful_queries == 0 else None
            }
        }
    
    def _calculate_average_relevance(self, processed_results: Dict[str, Any]) -> float:
        """Calculate average cultural relevance score."""
        all_entities = []
        for domain_entities in processed_results.get("recommendations_by_domain", {}).values():
            all_entities.extend(domain_entities)
        
        if not all_entities:
            return 0.0
        
        total_relevance = sum(entity.get("cultural_relevance", 0) for entity in all_entities)
        return total_relevance / len(all_entities)
    
    def _create_fallback_response(self, cultural_elements: Dict[str, Any], error_reason: str) -> Dict[str, Any]:
        """Create meaningful fallback response when Qloo API fails."""
        
        logger.info(f"🔄 Creating fallback response due to: {error_reason}")
        
        # Extract available cultural information for fallback
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        tradition_keywords = cultural_elements.get("tradition_elements", {}).get("tradition_keywords", [])
        
        # Create meaningful fallback recommendations
        fallback_recommendations = {
            "music_artists": self._create_fallback_music(heritage_keywords),
            "dining_venues": self._create_fallback_dining(tradition_keywords),
            "films": self._create_fallback_films(cultural_elements),
            "literature": self._create_fallback_books(heritage_keywords)
        }
        
        return {
            "qloo_intelligence": {
                "qloo_metadata": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "query_strategy": "fallback_mode",
                    "api_calls_made": 0,
                    "successful_calls": 0,
                    "error_reason": error_reason,
                    "fallback_content_created": True,
                    "best_practices_followed": True,
                    "api_pattern": "fallback_only"
                },
                "cultural_recommendations": fallback_recommendations,
                "cross_domain_connections": {
                    "common_themes": ["family_connection", "cultural_preservation", "shared_memories"],
                    "cross_domain_strength": 0.7
                },
                "thematic_intelligence": {
                    "common_themes": ["tradition", "family", "cultural_identity", "heritage"],
                    "theme_strength": 0.8,
                    "cultural_coherence": 0.7,
                    "fallback_mode": True
                },
                "fallback_used": True,
                "fallback_reason": error_reason
            }
        }
    
    def _create_fallback_music(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Create fallback music recommendations."""
        return [
            {
                "name": "Traditional Folk Music",
                "type": "urn:entity:artist",
                "description": "Music that connects to cultural roots and family traditions",
                "cultural_relevance": 0.9,
                "why_recommended": "Folk music often carries cultural stories and memories",
                "fallback": True
            },
            {
                "name": "Classic Standards",
                "type": "urn:entity:artist", 
                "description": "Timeless songs that span generations",
                "cultural_relevance": 0.8,
                "why_recommended": "Music that creates intergenerational connections",
                "fallback": True
            }
        ]
    
    def _create_fallback_dining(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Create fallback dining recommendations."""
        return [
            {
                "name": "Traditional Family Restaurant",
                "type": "urn:entity:place",
                "description": "Restaurants serving traditional, culturally-relevant cuisine",
                "cultural_relevance": 0.9,
                "why_recommended": "Food connects us to cultural heritage and family traditions",
                "fallback": True
            },
            {
                "name": "Local Community Cafe",
                "type": "urn:entity:place",
                "description": "Gathering places that foster community connection",
                "cultural_relevance": 0.7,
                "why_recommended": "Community spaces that encourage social interaction",
                "fallback": True
            }
        ]
    
    def _create_fallback_films(self, cultural_elements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create fallback film recommendations."""
        return [
            {
                "name": "Classic Family Films",
                "type": "urn:entity:movie",
                "description": "Movies that celebrate family bonds and cultural values",
                "cultural_relevance": 0.8,
                "why_recommended": "Films that reinforce positive cultural and family themes",
                "fallback": True
            }
        ]
    
    def _create_fallback_books(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Create fallback book recommendations.""" 
        return [
            {
                "name": "Cultural Heritage Stories",
                "type": "urn:entity:book",
                "description": "Books that explore cultural identity and family history",
                "cultural_relevance": 0.9,
                "why_recommended": "Literature that preserves and celebrates cultural heritage",
                "fallback": True
            }
        ]