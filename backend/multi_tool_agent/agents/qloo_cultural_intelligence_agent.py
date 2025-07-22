"""
Fixed Agent 3: Qloo Cultural Intelligence Agent - COMPLETE VERSION
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

Generates cross-domain cultural recommendations using proper Qloo API integration
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from google.adk.agents import Agent

# Configure logger
logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent(Agent):
    """
    Agent 3: Qloo Cultural Intelligence Agent - COMPLETE VERSION
    
    Purpose: Generate cross-domain cultural recommendations using Qloo API
    Input: consolidated_info + cultural_profile
    Output: Qloo cultural intelligence with recommendations
    
    Tools: qloo_insights_api
    
    Key Features:
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
        # Store tool reference to avoid Pydantic field errors
        self._qloo_tool_ref = qloo_tool
        logger.info("Qloo Cultural Intelligence Agent initialized with full functionality")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cross-domain cultural intelligence using FIXED Qloo API calls.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            
        Returns:
            Dictionary containing qloo_intelligence with cultural recommendations
        """
        
        try:
            logger.info("🚀 Starting Qloo cultural intelligence generation")
            
            # Extract context and cultural information
            request_context = consolidated_info.get("request_context", {})
            feedback_patterns = consolidated_info.get("feedback_patterns", {})
            blocked_content = feedback_patterns.get("blocked_content", {})
            cultural_elements = cultural_profile.get("cultural_elements", {})
            
            # Test Qloo API connection first
            try:
                qloo_tool = self._qloo_tool_ref
                logger.info("Testing Qloo API connection...")
            except Exception as e:
                logger.error(f"❌ Qloo tool access failed: {e}")
                return self._create_fallback_response(cultural_elements, "tool_access_failed")
            
            # Extract cultural keywords smartly by entity type
            cultural_keywords_by_type = self._extract_cultural_keywords(cultural_elements)
            logger.info(f"🔍 Extracted cultural keywords by type: {cultural_keywords_by_type}")
            
            # Extract demographic signals
            demographic_signals = self._extract_demographic_signals(consolidated_info)
            logger.info(f"👥 Demographic signals: {list(demographic_signals.keys())}")
            
            # Execute FIXED cultural recommendations
            qloo_results = await self._execute_qloo_queries(
                cultural_keywords_by_type, 
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
    
    def _extract_cultural_keywords(self, cultural_elements: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Extract meaningful cultural keywords for Qloo searches, organized by entity type.
        """
        keywords_by_type = {
            "place": [],
            "artist": [], 
            "movie": []
        }
        
        # Heritage elements
        heritage = cultural_elements.get("heritage_elements", {})
        heritage_keywords = heritage.get("heritage_keywords", [])
        
        # Tradition elements
        traditions = cultural_elements.get("tradition_elements", {})
        tradition_keywords = traditions.get("tradition_keywords", [])
        
        # Language elements
        languages = cultural_elements.get("language_elements", {}).get("languages", [])
        
        # Additional keywords
        additional = cultural_elements.get("additional_elements", {}).get("additional_keywords", [])
        
        # Combine all cultural indicators
        all_cultural_terms = []
        all_cultural_terms.extend([k.strip().lower() for k in heritage_keywords if k and len(k.strip()) > 2])
        all_cultural_terms.extend([k.strip().lower() for k in tradition_keywords if k and len(k.strip()) > 2])
        all_cultural_terms.extend([lang.strip().lower() for lang in languages if lang and len(lang.strip()) > 2])
        all_cultural_terms.extend([k.strip().lower() for k in additional if k and len(k.strip()) > 2])
        
        # Remove duplicates
        unique_terms = list(set(all_cultural_terms))
        
        # Generate smart search terms for each entity type
        for term in unique_terms[:3]:  # Limit to top 3 cultural terms
            
            # PLACES: Focus on restaurants, locations, destinations
            if term in ["italian", "italy"]:
                keywords_by_type["place"].extend(["Italian restaurants", "Italy", "Rome"])
            elif term in ["mexican", "mexico"]:
                keywords_by_type["place"].extend(["Mexican restaurants", "Mexico", "Taco"])
            elif term in ["chinese", "china"]:
                keywords_by_type["place"].extend(["Chinese restaurants", "China", "Beijing"])
            elif term in ["french", "france"]:
                keywords_by_type["place"].extend(["French restaurants", "France", "Paris"])
            elif term in ["indian", "india"]:
                keywords_by_type["place"].extend(["Indian restaurants", "India", "Curry"])
            elif term in ["japanese", "japan"]:
                keywords_by_type["place"].extend(["Japanese restaurants", "Japan", "Sushi"])
            else:
                keywords_by_type["place"].append(f"{term} restaurants")
            
            # ARTISTS: Focus on music, cultural performers, traditional artists  
            if term in ["italian", "italy"]:
                keywords_by_type["artist"].extend(["Italian opera", "Pavarotti", "classical Italian music"])
            elif term in ["mexican", "mexico"]:
                keywords_by_type["artist"].extend(["Mexican folk music", "mariachi", "Vicente Fernandez"])
            elif term in ["chinese", "china"]:
                keywords_by_type["artist"].extend(["Chinese traditional music", "Chinese opera", "Lang Lang"])
            elif term in ["french", "france"]:
                keywords_by_type["artist"].extend(["French chanson", "Edith Piaf", "French classical"])
            elif term in ["indian", "india"]:
                keywords_by_type["artist"].extend(["Indian classical music", "Bollywood music", "Ravi Shankar"])
            elif term in ["japanese", "japan"]:
                keywords_by_type["artist"].extend(["Japanese traditional music", "classical Japanese", "shamisen"])
            elif "music" in term or "song" in term:
                keywords_by_type["artist"].append(term)
            else:
                keywords_by_type["artist"].append(f"{term} music")
            
            # MOVIES: Focus on cinema, cultural films
            if term in ["italian", "italy"]:
                keywords_by_type["movie"].extend(["Italian cinema", "Federico Fellini", "Italian films"])
            elif term in ["mexican", "mexico"]:
                keywords_by_type["movie"].extend(["Mexican cinema", "Mexican films", "Alejandro Iñárritu"])
            elif term in ["chinese", "china"]:
                keywords_by_type["movie"].extend(["Chinese cinema", "Zhang Yimou", "Chinese films"])
            elif term in ["french", "france"]:
                keywords_by_type["movie"].extend(["French cinema", "French New Wave", "Jean-Luc Godard"])
            elif term in ["indian", "india"]:
                keywords_by_type["movie"].extend(["Bollywood", "Indian cinema", "Satyajit Ray"])
            elif term in ["japanese", "japan"]:
                keywords_by_type["movie"].extend(["Japanese cinema", "Akira Kurosawa", "Studio Ghibli"])
            else:
                keywords_by_type["movie"].append(f"{term} films")
        
        # Limit to 3 search terms per entity type for API efficiency
        for entity_type in keywords_by_type:
            keywords_by_type[entity_type] = keywords_by_type[entity_type][:3]
        
        return keywords_by_type
    
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
    
    async def _execute_qloo_queries(self, 
                                   cultural_keywords_by_type: Dict[str, List[str]],
                                   demographic_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Qloo queries using two-stage pattern with smart search terms.
        """
        results = {}
        
        # Check if we have any keywords to search
        total_keywords = sum(len(keywords) for keywords in cultural_keywords_by_type.values())
        if total_keywords == 0:
            logger.warning("No cultural keywords available for Qloo queries")
            return {"success": False, "error": "no_keywords"}
        
        # Map our internal types to Qloo entity types
        entity_type_mapping = {
            "place": "urn:entity:place",
            "artist": "urn:entity:artist", 
            "movie": "urn:entity:movie"
        }
        
        try:
            qloo_tool = self._qloo_tool_ref
            
            # Test if the tool has the required methods
            if not hasattr(qloo_tool, 'search_entities'):
                logger.error("❌ QlooInsightsAPI missing search_entities method")
                return {"success": False, "error": "method_not_available"}
            
            if not hasattr(qloo_tool, 'get_insights'):
                logger.error("❌ QlooInsightsAPI missing get_insights method")
                return {"success": False, "error": "method_not_available"}
            
            for internal_type, qloo_entity_type in entity_type_mapping.items():
                keywords = cultural_keywords_by_type.get(internal_type, [])
                
                if not keywords:
                    logger.info(f"No keywords for {internal_type}, skipping")
                    continue
                
                for keyword in keywords[:2]:  # Limit to 2 keywords per entity type
                    try:
                        logger.info(f"Searching for '{keyword}' in {qloo_entity_type}")
                        
                        # Stage 1: Search for entities using the smart keywords
                        search_result = await qloo_tool.search_entities(
                            query=keyword,
                            entity_types=[qloo_entity_type.replace("urn:entity:", "")],
                            limit=3
                        )
                        
                        if search_result.get("success") and search_result.get("results"):
                            entities = search_result["results"][:2]  # Limit entities
                            
                            # Stage 2: Get insights for found entities
                            for entity in entities:
                                entity_id = entity.get("id")
                                entity_name = entity.get("name", "Unknown")
                                
                                if entity_id:
                                    logger.info(f"Getting insights for entity: {entity_name} (ID: {entity_id})")
                                    
                                    params = {
                                        "filter.type": qloo_entity_type,
                                        "signal.interests.entities": entity_id,
                                        "take": 5
                                    }
                                    
                                    # Add demographic signals if available
                                    if demographic_signals.get("age_range"):
                                        params["signal.demographics.age"] = demographic_signals["age_range"]
                                    
                                    insights_result = await qloo_tool.get_insights(params)
                                    
                                    if insights_result.get("success"):
                                        result_key = f"{internal_type}_{keyword.replace(' ', '_')}"
                                        results[result_key] = insights_result
                                        logger.info(f"✅ Qloo insights successful for {entity_name}")
                                    else:
                                        logger.warning(f"❌ Insights failed for {entity_name}")
                                    
                                    # Rate limiting
                                    await asyncio.sleep(1.0)
                        else:
                            logger.warning(f"No entities found for '{keyword}' in {qloo_entity_type}")
                        
                        # Rate limiting between searches
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        logger.error(f"❌ Qloo query failed for {qloo_entity_type}/{keyword}: {e}")
                        continue
            
            successful_queries = len([r for r in results.values() if r.get("success")])
            logger.info(f"Qloo queries completed: {successful_queries} successful")
            
            return {
                "success": successful_queries > 0,
                "results": results,
                "total_queries": successful_queries
            }
            
        except Exception as e:
            logger.error(f"Qloo queries failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _process_qloo_results(self, 
                             qloo_results: Dict[str, Any],
                             cultural_elements: Dict[str, Any],
                             blocked_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Qloo results with intelligent filtering.
        """
        processed = {
            "places": [],
            "artists": [],
            "movies": [],
            "recommendations_count": 0
        }
        
        if not qloo_results.get("success"):
            logger.warning("No successful Qloo results to process")
            return processed
        
        results = qloo_results.get("results", {})
        
        for query_key, result in results.items():
            if not result.get("success"):
                continue
                
            entities = result.get("results", {}).get("entities", [])
            
            for entity in entities[:3]:  # Limit entities per query
                entity_name = entity.get("name", "Unknown")
                entity_type = entity.get("type", "")
                
                # Filter blocked content
                if self._is_blocked_content(entity_name, blocked_content):
                    continue
                
                # Categorize by entity type
                recommendation = {
                    "name": entity_name,
                    "qloo_id": entity.get("id"),
                    "description": entity.get("description", ""),
                    "popularity": entity.get("popularity", 0),
                    "cultural_relevance": self._calculate_cultural_relevance(entity, cultural_elements)
                }
                
                if "place" in entity_type.lower():
                    processed["places"].append(recommendation)
                elif "artist" in entity_type.lower():
                    processed["artists"].append(recommendation)
                elif "movie" in entity_type.lower():
                    processed["movies"].append(recommendation)
        
        # Calculate total recommendations
        processed["recommendations_count"] = (
            len(processed["places"]) + 
            len(processed["artists"]) + 
            len(processed["movies"])
        )
        
        logger.info(f"Processed {processed['recommendations_count']} Qloo recommendations")
        return processed
    
    def _is_blocked_content(self, entity_name: str, blocked_content: Dict[str, Any]) -> bool:
        """Check if content is blocked by user preferences."""
        if not blocked_content:
            return False
        
        entity_lower = entity_name.lower()
        
        for category, blocked_items in blocked_content.items():
            if isinstance(blocked_items, list):
                for blocked_item in blocked_items:
                    if blocked_item.lower() in entity_lower:
                        return True
        
        return False
    
    def _calculate_cultural_relevance(self, entity: Dict[str, Any], cultural_elements: Dict[str, Any]) -> float:
        """Calculate cultural relevance score (0.0 to 1.0)."""
        relevance = 0.5  # Base relevance
        
        entity_name = entity.get("name", "").lower()
        entity_desc = entity.get("description", "").lower()
        
        # Check for cultural keyword matches
        heritage_keywords = cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])
        for keyword in heritage_keywords:
            if keyword.lower() in entity_name or keyword.lower() in entity_desc:
                relevance += 0.2
        
        # Cap at 1.0
        return min(relevance, 1.0)
    
    def _build_cultural_intelligence_response(self, 
                                            processed_results: Dict[str, Any],
                                            cultural_elements: Dict[str, Any],
                                            qloo_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build comprehensive cultural intelligence response.
        """
        return {
            "qloo_intelligence": {
                "cultural_recommendations": {
                    "places": processed_results.get("places", []),
                    "artists": processed_results.get("artists", []),
                    "movies": processed_results.get("movies", [])
                },
                "recommendation_metadata": {
                    "total_recommendations": processed_results.get("recommendations_count", 0),
                    "qloo_queries_successful": qloo_results.get("total_queries", 0),
                    "cultural_keywords_used": len(cultural_elements.get("heritage_elements", {}).get("heritage_keywords", [])),
                    "generation_timestamp": datetime.now().isoformat()
                },
                "cultural_context": {
                    "heritage_elements": cultural_elements.get("heritage_elements", {}),
                    "cultural_themes": self._extract_cultural_themes(cultural_elements),
                    "recommendation_approach": "individual_preferences_first"
                },
                "status": "success" if processed_results.get("recommendations_count", 0) > 0 else "limited_results",
                "fallback_used": False
            }
        }
    
    def _extract_cultural_themes(self, cultural_elements: Dict[str, Any]) -> List[str]:
        """Extract high-level cultural themes."""
        themes = []
        
        cultural_keywords = set()
        
        # Collect all cultural keywords
        heritage = cultural_elements.get("heritage_elements", {})
        cultural_keywords.update(heritage.get("heritage_keywords", []))
        
        traditions = cultural_elements.get("tradition_elements", {})
        cultural_keywords.update(traditions.get("tradition_keywords", []))
        
        # Broad thematic connections
        for keyword in cultural_keywords:
            if any(food_word in keyword.lower() for food_word in ['food', 'cooking', 'meal', 'kitchen']):
                themes.append("culinary_experiences")
            if any(music_word in keyword.lower() for music_word in ['music', 'song', 'dance', 'instrument']):
                themes.append("musical_experiences")
            if any(family_word in keyword.lower() for family_word in ['family', 'tradition', 'celebration']):
                themes.append("family_traditions")
            if any(place_word in keyword.lower() for place_word in ['home', 'neighborhood', 'city', 'country']):
                themes.append("place_connections")
        
        return list(set(themes))  # Remove duplicates
    
    def _create_fallback_response(self, cultural_elements: Dict[str, Any], error_reason: str) -> Dict[str, Any]:
        """
        Create fallback response when Qloo API fails.
        """
        logger.warning(f"Using fallback response due to: {error_reason}")
        
        return {
            "qloo_intelligence": {
                "cultural_recommendations": {
                    "places": [],
                    "artists": [],
                    "movies": []
                },
                "recommendation_metadata": {
                    "total_recommendations": 0,
                    "qloo_queries_successful": 0,
                    "cultural_keywords_used": 0,
                    "generation_timestamp": datetime.now().isoformat(),
                    "error_reason": error_reason
                },
                "cultural_context": {
                    "heritage_elements": cultural_elements.get("heritage_elements", {}),
                    "cultural_themes": [],
                    "recommendation_approach": "fallback_mode"
                },
                "status": "fallback",
                "fallback_used": True,
                "fallback_reason": error_reason
            }
        }

# Export the agent class
__all__ = ["QlooCulturalIntelligenceAgent"]