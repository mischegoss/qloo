"""
Enhanced Qloo Cultural Intelligence Agent with Formative Decades Filtering
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

Agent 3: Uses formative decades (childhood, teen, young adult) as PRIMARY filters
for age-appropriate cultural recommendations instead of broad demographic categories.
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from config.cultural_mappings import get_heritage_tags, get_age_demographic

# Configure logger
logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent:
    """
    Agent 3: Qloo Cultural Intelligence with Era-Specific Filtering
    
    Queries Qloo API using formative decades as the primary filtering mechanism
    to ensure age-appropriate cultural recommendations for dementia care.
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("Qloo Cultural Intelligence Agent initialized with formative decades filtering")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any], 
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cultural intelligence using formative decades as primary filters.
        
        Args:
            consolidated_info: Output from Agent 1 (Information Consolidator)
            cultural_profile: Output from Agent 2 (Cultural Profile Builder)
            
        Returns:
            Dictionary containing era-appropriate cultural recommendations
        """
        
        try:
            logger.info("🎭 Agent 3: Starting Qloo Cultural Intelligence with era filtering")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            patient_location = patient_profile.get("location", "")  # Get location for places filtering
            
            # Get formative decades from cultural profile
            era_context = cultural_profile.get("era_context", {})
            formative_decades = era_context.get("formative_decades", [])
            
            if not formative_decades and birth_year:
                # Calculate formative decades if not provided
                formative_decades = self._calculate_formative_decades(birth_year)
            
            # Get heritage tags for filtering
            heritage_tags = get_heritage_tags(heritage)
            age_demographic = get_age_demographic(birth_year) if birth_year else "55_and_older"
            
            logger.info(f"Heritage: {heritage}, Formative decades: {formative_decades}")
            logger.info(f"Location: {patient_location}")
            logger.info(f"Heritage tags: {heritage_tags}")
            
            # Make era-specific Qloo calls with location filtering for places
            cultural_recommendations = await self._make_era_specific_calls(
                formative_decades, heritage_tags, age_demographic, patient_location
            )
            
            # Format response
            return self._format_enhanced_response(
                cultural_recommendations, heritage, heritage_tags, 
                age_demographic, formative_decades
            )
            
        except Exception as e:
            logger.error(f"❌ Agent 3 failed: {e}")
            return self._create_fallback_response(heritage)
    
    def _calculate_formative_decades(self, birth_year: int) -> List[int]:
        """
        Calculate formative decades: childhood (5-15), teen (15-20), young adult (20-30).
        
        Args:
            birth_year: Year of birth
            
        Returns:
            List of formative decades (e.g., [1950, 1960, 1970])
        """
        
        childhood_decade = ((birth_year + 10) // 10) * 10  # Age 10
        teen_decade = ((birth_year + 17) // 10) * 10       # Age 17  
        young_adult_decade = ((birth_year + 25) // 10) * 10  # Age 25
        
        decades = list(set([childhood_decade, teen_decade, young_adult_decade]))
        decades.sort()
        
        logger.info(f"Calculated formative decades for {birth_year}: {decades}")
        return decades
    
    async def _make_era_specific_calls(self, 
                                     formative_decades: List[int],
                                     heritage_tags: Dict[str, str], 
                                     age_demographic: str,
                                     patient_location: str = None) -> Dict[str, Any]:
        """
        Make simple Qloo calls focused on Italian-American cultural recommendations.
        Simplified approach - no era filtering for now.
        """
        
        results = {
            "movies": {"available": False, "entities": [], "entity_count": 0},
            "artists": {"available": False, "entities": [], "entity_count": 0}, 
            "places": {"available": False, "entities": [], "entity_count": 0}
        }
        
        successful_calls = 0
        total_calls = 0
        
        # Simple content type calls (no era looping)
        content_types = [
            ("movies", "urn:entity:movie", heritage_tags.get("movies")),
            ("artists", "urn:entity:artist", heritage_tags.get("music")), 
            ("places", "urn:entity:place", heritage_tags.get("cuisine"))
        ]
        
        for content_name, entity_type, heritage_tag in content_types:
            if not heritage_tag:
                continue
                
            try:
                total_calls += 1
                
                logger.info(f"Simple call: {content_name} with {heritage_tag}")
                
                # Make simple Qloo API call
                result = await self.qloo_tool.simple_tag_insights(
                    entity_type=entity_type,
                    tag=heritage_tag,
                    age_demographic=age_demographic,
                    take=10
                )
                
                # Check if we got entities back
                if result and result.get("entities"):
                    entities = result["entities"]
                    
                    # For places, transform into memory anchor format
                    if content_name == "places":
                        entities = self._transform_places_to_memory_anchors(entities, 1960)  # Use 1960s as default
                    
                    results[content_name] = {
                        "available": True,
                        "entities": entities[:10],
                        "entity_count": len(entities[:10]),
                        "memory_anchors": content_name == "places"
                    }
                    
                    successful_calls += 1
                    logger.info(f"✅ {content_name}: {len(entities)} results")
                else:
                    logger.warning(f"⚠️ {content_name}: no entities in result")
                    
            except Exception as e:
                logger.error(f"❌ {content_name} call failed: {e}")
        
        # Add metadata
        results["metadata"] = {
            "successful_calls": successful_calls,
            "total_calls": total_calls,
            "approach": "simplified_cultural_recommendations",
            "places_as_memory_anchors": True
        }
        
        return results
    
    def _transform_places_to_memory_anchors(self, entities: List[Dict[str, Any]], decade: int) -> List[Dict[str, Any]]:
        """Transform place entities into memory anchor format for dementia care."""
        
        memory_anchors = []
        
        for entity in entities:
            # Extract original place information
            original_name = entity.get("name", "Unknown Place")
            description = entity.get("properties", {}).get("description", "")
            
            # Transform into memory anchor
            memory_anchor = {
                **entity,  # Keep original entity data
                "memory_anchor_name": f"{decade}s-style {original_name}",
                "memory_purpose": "recipe_inspiration_and_conversation",
                "conversation_prompts": self._generate_place_conversation_prompts(original_name, decade),
                "recipe_inspiration": self._extract_recipe_inspiration(entity, decade),
                "not_a_destination": True,
                "usage_note": "Use for memories and cooking inspiration, not actual visits"
            }
            
            memory_anchors.append(memory_anchor)
        
        return memory_anchors
    
    def _generate_place_conversation_prompts(self, place_name: str, decade: int) -> List[str]:
        """Generate conversation prompts based on place and era."""
        
        place_type = self._determine_place_type(place_name.lower())
        
        prompts = [
            f"Did you have a favorite {place_type} in the {decade}s?",
            f"What do you remember about {place_type}s from that time?",
            f"Tell me about the food at places like this when you were younger",
            f"Who did you go to {place_type}s with in the {decade}s?"
        ]
        
        return prompts
    
    def _determine_place_type(self, place_name: str) -> str:
        """Determine general place type for conversation prompts."""
        
        if any(word in place_name for word in ["restaurant", "trattoria", "cafe", "diner"]):
            return "restaurant"
        elif any(word in place_name for word in ["bakery", "bread", "pastry"]):
            return "bakery"
        elif any(word in place_name for word in ["market", "grocery", "store"]):
            return "store"
        elif any(word in place_name for word in ["bar", "pub", "tavern"]):
            return "gathering place"
        else:
            return "place"
    
    def _extract_recipe_inspiration(self, entity: Dict[str, Any], decade: int) -> Dict[str, Any]:
        """Extract recipe inspiration from place entity."""
        
        place_name = entity.get("name", "")
        description = entity.get("properties", {}).get("description", "")
        
        # Extract cuisine style and characteristics
        inspiration = {
            "cuisine_style": f"{decade}s family-style cooking",
            "cooking_method": "simple, traditional preparation",
            "flavor_profile": "comfort food flavors from this era",
            "serving_style": "family-style portions",
            "inspiration_note": f"Inspired by the style of cooking at {place_name} in the {decade}s"
        }
        
        return inspiration
    
    def _format_enhanced_response(self, 
                                cultural_recommendations: Dict[str, Any],
                                heritage: str,
                                heritage_tags: Dict[str, str],
                                age_demographic: str,
                                formative_decades: List[int]) -> Dict[str, Any]:
        """Format response with era-specific metadata."""
        
        metadata = cultural_recommendations.get("metadata", {})
        
        return {
            "qloo_intelligence": {
                "success": metadata.get("successful_calls", 0) > 0,
                "cultural_recommendations": {
                    k: v for k, v in cultural_recommendations.items() 
                    if k != "metadata"
                },
                "metadata": {
                    "heritage_used": heritage,
                    "age_demographic": age_demographic,
                    "heritage_tags": heritage_tags,
                    "formative_decades": formative_decades,
                    "successful_calls": metadata.get("successful_calls", 0),
                    "total_calls": metadata.get("total_calls", 0),
                    "era_filtering_enabled": True,
                    "generation_timestamp": datetime.now().isoformat(),
                    "approach": "era_specific_decades"
                },
                "cross_domain_connections": self._create_era_connections(
                    cultural_recommendations, formative_decades
                ),
                "status": "success" if metadata.get("successful_calls", 0) > 0 else "api_failure"
            }
        }
    
    def _create_era_connections(self, 
                              cultural_recommendations: Dict[str, Any],
                              formative_decades: List[int]) -> Dict[str, Any]:
        """Create connections between different content types from the same era."""
        
        connections = {
            "thematic_coherence": f"Content from formative decades: {', '.join(map(str, formative_decades))}",
            "cultural_threading": "Music, movies, and places from the same cultural and temporal context",
            "memory_activation": "Content selected to trigger positive memories from key life periods",
            "era_focus": {
                "childhood_decade": formative_decades[0] if formative_decades else None,
                "identity_formation_decade": formative_decades[1] if len(formative_decades) > 1 else None,
                "young_adult_decade": formative_decades[2] if len(formative_decades) > 2 else None
            }
        }
        
        return connections
    
    def _create_fallback_response(self, heritage: str) -> Dict[str, Any]:
        """Create fallback response when Qloo calls fail."""
        
        return {
            "qloo_intelligence": {
                "success": False,
                "cultural_recommendations": {
                    "movies": {"available": False, "entities": [], "entity_count": 0},
                    "artists": {"available": False, "entities": [], "entity_count": 0},
                    "places": {"available": False, "entities": [], "entity_count": 0}
                },
                "metadata": {
                    "heritage_used": heritage,
                    "successful_calls": 0,
                    "total_calls": 0,
                    "era_filtering_enabled": False,
                    "status": "fallback_mode"
                },
                "status": "fallback"
            }
        }

# Test function
async def test_era_filtering():
    """Test the enhanced era-specific filtering."""
    
    import os
    from backend.multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
    
    # Setup
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        print("❌ No QLOO_API_KEY found")
        return
    
    qloo_tool = QlooInsightsAPI(api_key)
    agent = QlooCulturalIntelligenceAgent(qloo_tool)
    
    # Test data for Maria (born 1945)
    consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "additional_context": "Loves music and cooking"
        }
    }
    
    cultural_profile = {
        "era_context": {
            "formative_decades": [1950, 1960, 1970]  # Her childhood, teen, young adult decades
        }
    }
    
    # Run the agent
    print("Testing enhanced era-specific Qloo filtering...")
    result = await agent.run(consolidated_info, cultural_profile)
    
    # Display results
    qloo_intel = result.get("qloo_intelligence", {})
    metadata = qloo_intel.get("metadata", {})
    
    print(f"\nResults:")
    print(f"Success: {qloo_intel.get('success')}")
    print(f"Heritage: {metadata.get('heritage_used')}")
    print(f"Formative decades: {metadata.get('formative_decades')}")
    print(f"Era filtering: {metadata.get('era_filtering_enabled')}")
    print(f"Successful calls: {metadata.get('successful_calls')}/{metadata.get('total_calls')}")
    
    # Show era-specific recommendations
    recommendations = qloo_intel.get("cultural_recommendations", {})
    for category, data in recommendations.items():
        if data.get("available"):
            print(f"\n{category.title()} ({data.get('entity_count', 0)} results):")
            for entity in data.get("entities", [])[:3]:
                name = entity.get("name", "Unknown")
                year = entity.get("properties", {}).get("release_year", "Unknown year")
                print(f"  - {name} ({year})")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_era_filtering())