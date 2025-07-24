"""
Agent 3: Qloo Cultural Intelligence - FIXED for Simplified API
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

FIXED ISSUES:
- Removes non-existent search_entities() method calls
- Uses make_three_cultural_calls() from simplified API
- Properly passes birth_year to get_heritage_tags()
- Handles correct response structure from QlooInsightsAPI
"""

from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

# Import the updated nostalgia-based mappings
from config.cultural_mappings import get_heritage_tags, get_age_demographic

logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent:
    """
    Agent 3: Qloo Cultural Intelligence - FIXED for Simplified API
    
    FIXES:
    - Uses correct API methods (make_three_cultural_calls)
    - Properly handles simplified QlooInsightsAPI response structure
    - Passes birth_year parameter correctly
    - Removes non-existent method calls
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("Qloo Cultural Intelligence Agent initialized with FIXED API integration")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any], 
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cultural intelligence using FIXED nostalgia-based recommendations.
        
        Args:
            consolidated_info: Output from Agent 1 (Information Consolidator)
            cultural_profile: Output from Agent 2 (Cultural Profile Builder)
            
        Returns:
            Dictionary containing age-appropriate, dementia-friendly cultural recommendations
        """
        
        try:
            logger.info("🎭 Agent 3: Starting FIXED Qloo Cultural Intelligence")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            patient_location = patient_profile.get("location", "")
            
            # Get formative decades from cultural profile
            era_context = cultural_profile.get("era_context", {})
            formative_decades = era_context.get("formative_decades", [])
            
            if not formative_decades and birth_year:
                # Calculate formative decades if not provided
                formative_decades = self._calculate_formative_decades(birth_year)
            
            # FIXED: Properly pass birth_year parameter
            heritage_tags = get_heritage_tags(heritage, birth_year)
            age_demographic = get_age_demographic(birth_year) if birth_year else "55_and_older"
            
            logger.info(f"Heritage: {heritage} (cuisine only), Birth year: {birth_year}")
            logger.info(f"Nostalgia-based tags: {heritage_tags}")
            logger.info(f"Age demographic: {age_demographic}")
            logger.info(f"Formative decades: {formative_decades}")
            
            # FIXED: Use correct simplified API method
            cultural_recommendations = await self._make_simplified_qloo_calls(
                heritage_tags, age_demographic
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
        Calculate formative decades: childhood (10), teen (17), young adult (25).
        
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
    
    async def _make_simplified_qloo_calls(self, 
                                        heritage_tags: Dict[str, str], 
                                        age_demographic: str) -> Dict[str, Any]:
        """
        FIXED: Use the simplified QlooInsightsAPI make_three_cultural_calls method.
        
        Args:
            heritage_tags: Dictionary with cuisine, music, tv_shows tags
            age_demographic: Age demographic string
            
        Returns:
            Structured results from Qloo API
        """
        
        try:
            logger.info("Making simplified Qloo API calls using make_three_cultural_calls")
            
            # FIXED: Use the correct method from simplified API
            results = await self.qloo_tool.make_three_cultural_calls(
                heritage_tags=heritage_tags,
                age_demographic=age_demographic
            )
            
            if results.get("success"):
                logger.info(f"✅ Qloo calls successful: {results['successful_calls']}/3")
                logger.info(f"Total results: {results['total_results']}")
                
                # Extract cultural recommendations
                cultural_recommendations = results.get("cultural_recommendations", {})
                
                # Initialize result structure
                formatted_results = {
                    "tv_shows": {"available": False, "entities": [], "entity_count": 0},
                    "artists": {"available": False, "entities": [], "entity_count": 0}, 
                    "places": {"available": False, "entities": [], "entity_count": 0}
                }
                
                # Process each category
                for category in ["tv_shows", "artists", "places"]:
                    category_data = cultural_recommendations.get(category, {})
                    if category_data.get("available"):
                        formatted_results[category] = {
                            "available": True,
                            "entities": category_data.get("entities", []),
                            "entity_count": category_data.get("entity_count", 0)
                        }
                        logger.info(f"   {category}: {formatted_results[category]['entity_count']} entities")
                
                return formatted_results
            
            else:
                logger.warning("Qloo calls returned no successful results")
                return self._create_empty_recommendations()
                
        except Exception as e:
            logger.error(f"❌ Simplified Qloo calls failed: {e}")
            return self._create_empty_recommendations()
    
    def _create_empty_recommendations(self) -> Dict[str, Any]:
        """Create empty recommendation structure for fallback."""
        
        return {
            "tv_shows": {"available": False, "entities": [], "entity_count": 0},
            "artists": {"available": False, "entities": [], "entity_count": 0},
            "places": {"available": False, "entities": [], "entity_count": 0}
        }
    
    def _format_enhanced_response(self, 
                                cultural_recommendations: Dict[str, Any],
                                heritage: str,
                                heritage_tags: Dict[str, str],
                                age_demographic: str,
                                formative_decades: List[int]) -> Dict[str, Any]:
        """Format the enhanced response with cross-domain connections."""
        
        # Check what content is available
        available_themes = []
        for category, data in cultural_recommendations.items():
            if isinstance(data, dict) and data.get("available"):
                available_themes.append(category)
        
        connections = {
            "available": len(available_themes) > 1,
            "themes": available_themes,
            "suggested_combinations": []
        }
        
        # Add specific combinations if multiple themes available
        if "tv_shows" in available_themes and "places" in available_themes:
            connections["suggested_combinations"].append({
                "type": "tv_and_meal",
                "description": "Watch nostalgic TV shows with themed comfort food"
            })
        
        if "artists" in available_themes and "places" in available_themes:
            connections["suggested_combinations"].append({
                "type": "music_and_cooking",
                "description": "Listen to nostalgic music while preparing familiar recipes"
            })
        
        # Calculate success metrics
        successful_calls = sum(1 for data in cultural_recommendations.values() 
                             if data.get("available", False))
        total_results = sum(data.get("entity_count", 0) 
                          for data in cultural_recommendations.values())
        
        return {
            "qloo_intelligence": {
                "success": successful_calls > 0,
                "cultural_recommendations": cultural_recommendations,
                "metadata": {
                    "heritage_used": heritage,
                    "heritage_tags": heritage_tags,
                    "successful_calls": successful_calls,
                    "total_calls": 3,
                    "total_results": total_results,
                    "age_demographic": age_demographic,
                    "formative_decades": formative_decades,
                    "era_filtering_enabled": bool(formative_decades),
                    "approach": "simplified_nostalgia_based",
                    "generation_timestamp": datetime.now().isoformat(),
                    "status": "success" if successful_calls > 0 else "no_results"
                },
                "cross_domain_connections": connections,
                "status": "success" if successful_calls > 0 else "no_results"
            }
        }
    
    def _create_fallback_response(self, heritage: str) -> Dict[str, Any]:
        """Create fallback response when Qloo calls fail."""
        
        logger.warning("Creating fallback response for Qloo Cultural Intelligence")
        
        return {
            "qloo_intelligence": {
                "success": False,
                "cultural_recommendations": {
                    "tv_shows": {"available": False, "entities": [], "entity_count": 0},
                    "artists": {"available": False, "entities": [], "entity_count": 0},
                    "places": {"available": False, "entities": [], "entity_count": 0}
                },
                "metadata": {
                    "heritage_used": heritage,
                    "successful_calls": 0,
                    "total_calls": 0,
                    "total_results": 0,
                    "era_filtering_enabled": False,
                    "approach": "fallback_mode",
                    "status": "fallback"
                },
                "cross_domain_connections": {"available": False},
                "status": "fallback"
            }
        }

# Test function
async def test_fixed_qloo_cultural_intelligence():
    """Test the FIXED Qloo Cultural Intelligence Agent."""
    
    # Mock tool for testing
    class MockQlooTool:
        async def make_three_cultural_calls(self, heritage_tags, age_demographic):
            return {
                "success": True,
                "successful_calls": 3,
                "total_calls": 3,
                "total_results": 15,
                "cultural_recommendations": {
                    "tv_shows": {
                        "available": True,
                        "entities": [{"name": "Classic Family Show", "entity_id": "123"}],
                        "entity_count": 1
                    },
                    "artists": {
                        "available": True,
                        "entities": [{"name": "Era Musician", "entity_id": "456"}],
                        "entity_count": 1
                    },
                    "places": {
                        "available": True,
                        "entities": [{"name": "Cultural Restaurant", "entity_id": "789"}],
                        "entity_count": 1
                    }
                }
            }
    
    # Test data
    agent = QlooCulturalIntelligenceAgent(MockQlooTool())
    
    test_consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "location": "Brooklyn, New York"
        }
    }
    
    test_cultural_profile = {
        "era_context": {
            "formative_decades": [1950, 1960, 1970]
        }
    }
    
    # Run test
    result = await agent.run(test_consolidated_info, test_cultural_profile)
    
    qloo_intel = result.get("qloo_intelligence", {})
    print("FIXED Qloo Cultural Intelligence Test Results:")
    print(f"Success: {qloo_intel.get('success')}")
    print(f"TV Shows available: {qloo_intel.get('cultural_recommendations', {}).get('tv_shows', {}).get('available')}")
    print(f"Cross-domain connections: {qloo_intel.get('cross_domain_connections', {}).get('available')}")
    print(f"Approach: {qloo_intel.get('metadata', {}).get('approach')}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_fixed_qloo_cultural_intelligence())