"""
Agent 3: Qloo Cultural Intelligence - SIMPLIFIED VERSION
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

Complete rewrite using simple tag-based approach.
Removes all complex entity searching and keyword extraction.
"""

from typing import Dict, Any
import logging
from datetime import datetime
from google.adk.agents import Agent

# Import our new cultural mappings
from config.cultural_mappings import get_heritage_tags, get_age_demographic, get_interest_tags

logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent(Agent):
    """
    Agent 3: Qloo Cultural Intelligence - SIMPLIFIED
    
    MAJOR SIMPLIFICATION:
    - Uses direct cultural heritage → tag mappings
    - Makes exactly 3 simple Qloo API calls
    - No complex entity searching
    - No keyword extraction complexity
    - No fallback strategies
    
    NEW APPROACH:
    - Extract heritage from consolidated info
    - Map heritage to predefined Qloo tags  
    - Make 3 direct tag-based insights calls
    - Return simple, structured results
    """
    
    def __init__(self, qloo_tool):
        super().__init__(
            name="qloo_cultural_intelligence_simplified",
            description="Generates cross-domain cultural recommendations using simplified tag-based approach"
        )
        self._qloo_tool = qloo_tool
        logger.info("Qloo Cultural Intelligence Agent initialized with simplified approach")
    
    async def run(self, 
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cultural intelligence using simplified tag-based Qloo calls.
        
        Args:
            consolidated_info: Output from Agent 1
            cultural_profile: Output from Agent 2
            
        Returns:
            Simple cultural recommendations from Qloo
        """
        
        try:
            logger.info("Starting simplified Qloo cultural intelligence")
            
            # STEP 1: Extract simple inputs
            heritage = self._extract_heritage(consolidated_info, cultural_profile)
            age_demographic = self._extract_age_demographic(consolidated_info)
            
            logger.info(f"Heritage: {heritage}, Age: {age_demographic}")
            
            # STEP 2: Map heritage to Qloo tags
            heritage_tags = get_heritage_tags(heritage)
            
            logger.info(f"Mapped to tags: {heritage_tags}")
            
            # STEP 3: Make 3 simple Qloo API calls
            qloo_results = await self._qloo_tool.make_three_cultural_calls(
                heritage_tags=heritage_tags,
                age_demographic=age_demographic
            )
            
            # STEP 4: Format results for Agent 4 consumption
            formatted_response = self._format_simple_response(
                qloo_results=qloo_results,
                heritage=heritage,
                heritage_tags=heritage_tags,
                age_demographic=age_demographic
            )
            
            logger.info(f"Qloo intelligence complete: {qloo_results.get('successful_calls', 0)}/3 calls successful")
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"❌ Qloo Cultural Intelligence failed: {e}")
            return self._create_fallback_response()
    
    def _extract_heritage(self, consolidated_info: Dict[str, Any], cultural_profile: Dict[str, Any]) -> str:
        """Extract cultural heritage from available data."""
        
        # Try cultural profile first
        heritage = cultural_profile.get("cultural_elements", {}).get("heritage")
        if heritage:
            return heritage
        
        # Try consolidated info patient profile
        patient_profile = consolidated_info.get("patient_profile", {})
        heritage = patient_profile.get("cultural_heritage")
        if heritage:
            return heritage
        
        # Try request context
        request_context = consolidated_info.get("request_context", {})
        heritage = request_context.get("cultural_heritage")
        if heritage:
            return heritage
        
        # Default fallback
        logger.warning("No cultural heritage found, using American fallback")
        return "American"
    
    def _extract_age_demographic(self, consolidated_info: Dict[str, Any]) -> str:
        """Extract and convert age to Qloo demographic."""
        
        # Try to get birth year from patient profile
        patient_profile = consolidated_info.get("patient_profile", {})
        birth_year = patient_profile.get("birth_year")
        
        if birth_year:
            return get_age_demographic(birth_year)
        
        # Try to get age directly
        age = patient_profile.get("age")
        if age:
            birth_year = 2024 - age
            return get_age_demographic(birth_year)
        
        # Default to older adult demographic
        logger.warning("No age information found, defaulting to 55_and_older")
        return "55_and_older"
    
    def _format_simple_response(self, 
                               qloo_results: Dict[str, Any],
                               heritage: str,
                               heritage_tags: Dict[str, str],
                               age_demographic: str) -> Dict[str, Any]:
        """Format Qloo results into simple structure for Agent 4."""
        
        return {
            "qloo_intelligence": {
                "success": qloo_results.get("success", False),
                "cultural_recommendations": qloo_results.get("cultural_recommendations", {}),
                "metadata": {
                    "heritage_used": heritage,
                    "age_demographic": age_demographic,
                    "heritage_tags": heritage_tags,
                    "successful_calls": qloo_results.get("successful_calls", 0),
                    "total_calls": qloo_results.get("total_calls", 3),
                    "total_results": qloo_results.get("total_results", 0),
                    "generation_timestamp": datetime.now().isoformat(),
                    "approach": "simplified_tag_based"
                },
                "cross_domain_connections": self._create_cross_domain_connections(qloo_results),
                "status": "success" if qloo_results.get("success") else "api_failure"
            }
        }
    
    def _create_cross_domain_connections(self, qloo_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create simple cross-domain connections from Qloo results."""
        
        cultural_recs = qloo_results.get("cultural_recommendations", {})
        
        connections = {
            "available": False,
            "themes": [],
            "suggested_combinations": []
        }
        
        # Simple connection logic
        available_categories = [cat for cat, data in cultural_recs.items() if data.get("available")]
        
        if len(available_categories) >= 2:
            connections["available"] = True
            connections["themes"] = available_categories
            
            # Create simple combination suggestions
            if "places" in available_categories and "music" in available_categories:
                connections["suggested_combinations"].append({
                    "type": "dining_with_music",
                    "description": "Combine cultural dining with matching music"
                })
            
            if "movies" in available_categories and "places" in available_categories:
                connections["suggested_combinations"].append({
                    "type": "movie_and_meal",
                    "description": "Watch cultural films with themed snacks"
                })
        
        return connections
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response when Qloo fails."""
        
        return {
            "qloo_intelligence": {
                "success": False,
                "cultural_recommendations": {
                    "places": {"available": False, "error": "api_failure", "entities": []},
                    "artists": {"available": False, "error": "api_failure", "entities": []},
                    "movies": {"available": False, "error": "api_failure", "entities": []}
                },
                "metadata": {
                    "heritage_used": "unknown",
                    "age_demographic": "55_and_older",
                    "successful_calls": 0,
                    "total_calls": 0,
                    "total_results": 0,
                    "generation_timestamp": datetime.now().isoformat(),
                    "approach": "fallback_due_to_api_failure"
                },
                "cross_domain_connections": {"available": False},
                "status": "fallback_used"
            }
        }

# Test function for the simplified agent
async def test_simplified_agent():
    """Test the simplified Qloo agent."""
    import os
    from backend.multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
    
    # Setup
    api_key = os.getenv("QLOO_API_KEY")
    if not api_key:
        print("❌ No QLOO_API_KEY found")
        return
    
    qloo_tool = QlooInsightsAPI(api_key)
    agent = QlooCulturalIntelligenceAgent(qloo_tool)
    
    # Test data matching the curl example
    consolidated_info = {
        "patient_profile": {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "additional_context": "Loves music and cooking"
        },
        "request_context": {
            "request_type": "dashboard"
        }
    }
    
    cultural_profile = {
        "cultural_elements": {
            "heritage": "Italian-American"
        }
    }
    
    # Run the agent
    print("Testing simplified Qloo Cultural Intelligence Agent...")
    result = await agent.run(consolidated_info, cultural_profile)
    
    # Display results
    qloo_intel = result.get("qloo_intelligence", {})
    print(f"\nResults:")
    print(f"Success: {qloo_intel.get('success')}")
    print(f"Heritage: {qloo_intel.get('metadata', {}).get('heritage_used')}")
    print(f"Age demographic: {qloo_intel.get('metadata', {}).get('age_demographic')}")
    print(f"Successful calls: {qloo_intel.get('metadata', {}).get('successful_calls')}/3")
    print(f"Total results: {qloo_intel.get('metadata', {}).get('total_results')}")
    
    # Show sample recommendations
    recommendations = qloo_intel.get("cultural_recommendations", {})
    for category, data in recommendations.items():
        if data.get("available"):
            print(f"\n{category.title()}: {data.get('entity_count', 0)} results")
            for entity in data.get("entities", [])[:2]:
                print(f"  - {entity.get('name', 'Unknown')}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simplified_agent())