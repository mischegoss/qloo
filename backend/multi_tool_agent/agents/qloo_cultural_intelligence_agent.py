"""
Qloo Cultural Intelligence Agent - UPDATED: Works with Improved TV Show Calls
File: backend/multi_tool_agent/agents/qloo_cultural_intelligence_agent.py

IMPROVEMENTS:
- Compatible with improved qloo_tools.py TV show handling
- Simplified approach relies on qloo_tools broad API calls + local filtering
- No complex year filtering logic needed - handled in qloo_tools
- Clean, simple tag passing
"""

import logging
import asyncio
import random
from datetime import datetime, date
from typing import Dict, Any, List, Optional

# Configure logger
logger = logging.getLogger(__name__)

class QlooCulturalIntelligenceAgent:
    """
    Agent 3: Improved Qloo Cultural Intelligence that works with updated TV show handling.
    
    IMPROVEMENTS:
    - Simplified approach - complex filtering moved to qloo_tools.py
    - No API-level age filtering (prevents zero results)
    - All age-appropriate filtering happens locally in qloo_tools
    - TV shows use broad API calls with local classic show filtering
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("✅ Qloo Cultural Intelligence Agent initialized - NO API age filtering, LOCAL filtering only")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate cultural intelligence with LOCAL age-appropriate filtering only.
        """
        
        try:
            logger.info("🚀 Agent 3: Starting Qloo intelligence - BROAD API calls + LOCAL filtering")
            
            # Set daily random seed for uniqueness
            today = date.today()
            daily_seed = hash(f"{today.year}-{today.month}-{today.day}")
            random.seed(daily_seed)
            logger.info(f"📅 Daily seed set: {daily_seed} for date {today}")
            
            # Extract key information
            patient_profile = consolidated_info.get("patient_profile", {})
            heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year")
            
            # Determine age demographic for LOCAL filtering only
            age_demographic = self._get_age_demographic(birth_year)
            logger.info(f"👤 Age demographic for LOCAL filtering: {age_demographic}")
            
            # Get heritage tags (simplified - qloo_tools handles complexity)
            heritage_tags = self._get_simple_heritage_tags(heritage)
            
            # Make the 3 Qloo calls - qloo_tools handles all the complexity
            qloo_results = await self._make_three_simple_qloo_calls(heritage_tags, age_demographic)
            
            if qloo_results.get("success"):
                logger.info("✅ Agent 3: Qloo intelligence complete - returning results")
                
                # Wrap in "qloo_intelligence" key for downstream agents
                return {
                    "qloo_intelligence": qloo_results,
                    "agent_metadata": {
                        "agent": "QlooCulturalIntelligence",
                        "version": "improved_tv_show_handling",
                        "approach": "broad_api_calls_local_filtering_tv_improved",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            else:
                logger.error("❌ Agent 3: All Qloo calls failed")
                return self._create_empty_response(heritage)
                
        except Exception as e:
            logger.error(f"❌ Agent 3 exception: {e}")
            return self._create_empty_response(heritage)
    
    def _get_age_demographic(self, birth_year: Optional[int]) -> str:
        """Convert birth year to age demographic for LOCAL filtering."""
        if not birth_year:
            return "55_and_older"  # Default for dementia care
        
        age = 2024 - birth_year
        
        if age >= 55:
            return "55_and_older"
        elif age >= 36:
            return "36_to_55"
        else:
            return "35_and_younger"
    
    def _get_simple_heritage_tags(self, heritage: str) -> Dict[str, str]:
        """
        Get simple heritage tags - complexity is handled in qloo_tools.py.
        
        This is much simpler now since qloo_tools handles:
        - TV show broad API calls + local filtering
        - Music filtering for age-appropriateness
        - Progressive fallback strategies
        """
        
        # Heritage-based cuisine tags (keep heritage-specific for places)
        heritage_cuisine_map = {
            "Italian-American": "urn:tag:genre:place:restaurant:italian",
            "Irish-American": "urn:tag:genre:place:restaurant:irish",
            "Mexican-American": "urn:tag:genre:place:restaurant:mexican",
            "German-American": "urn:tag:genre:place:restaurant:german", 
            "Chinese-American": "urn:tag:genre:place:restaurant:chinese",
            "American": "urn:tag:genre:place:restaurant:american"
        }
        
        # Simple, broad tags - qloo_tools handles the complexity
        tags = {
            "cuisine": heritage_cuisine_map.get(heritage, heritage_cuisine_map["American"]),
            "music": "urn:tag:genre:music:jazz",        # Works perfectly!
            "tv_shows": "broad_tv_call"                 # Special signal for qloo_tools
        }
        
        logger.info(f"🎯 Using simple heritage tags: {tags}")
        return tags
    
    async def _make_three_simple_qloo_calls(self, heritage_tags: Dict[str, str], age_demographic: str) -> Dict[str, Any]:
        """
        Make 3 simple Qloo API calls - qloo_tools handles all complexity.
        
        This is much simpler now since qloo_tools.py handles:
        - Broad API calls for TV shows
        - Local filtering for age-appropriateness  
        - Progressive fallback strategies
        - All the complex logic we used to have here
        """
        
        logger.info("🌐 Making 3 SIMPLE Qloo API calls - complexity handled in qloo_tools")
        
        try:
            # Use the improved qloo_tools three_cultural_calls method
            # It handles all the complexity: broad calls, local filtering, fallbacks
            results = await self.qloo_tool.three_cultural_calls(heritage_tags, age_demographic)
            
            if results.get("success"):
                total_results = results.get("total_results", 0)
                successful_calls = results.get("successful_calls", 0)
                
                logger.info(f"✅ Simple Qloo calls complete: {successful_calls}/3 successful, {total_results} total results")
                logger.info(f"🎯 All results are locally filtered for age: {age_demographic}")
                
                # Log what we got for each category
                cultural_recs = results.get("cultural_recommendations", {})
                for category, data in cultural_recs.items():
                    if isinstance(data, dict) and data.get("available"):
                        count = data.get("entity_count", 0)
                        filtering = data.get("filtering_applied", "unknown")
                        logger.info(f"   📋 {category}: {count} results (filtering: {filtering})")
                
                return results
            else:
                logger.error("❌ Simple Qloo calls failed")
                return {"success": False, "error": "all_simple_calls_failed"}
                
        except Exception as e:
            logger.error(f"❌ Exception in simple Qloo calls: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_empty_response(self, heritage: str) -> Dict[str, Any]:
        """Create empty response when all calls fail (should be rare with broad calls)."""
        
        logger.warning("⚠️ Creating empty response - should be rare with broad API calls")
        
        return {
            "qloo_intelligence": {
                "success": False,
                "successful_calls": 0,
                "total_calls": 3,
                "total_results": 0,
                "age_demographic": "unknown",
                "approach": "failed_fallback",
                "cultural_recommendations": {
                    "places": {"available": False, "entities": []},
                    "artists": {"available": False, "entities": []},
                    "tv_shows": {"available": False, "entities": []}
                },
                "error": "all_api_calls_failed"
            },
            "agent_metadata": {
                "agent": "QlooCulturalIntelligence",
                "version": "improved_tv_show_handling", 
                "approach": "empty_fallback",
                "timestamp": datetime.now().isoformat()
            }
        }

# Export the main class  
__all__ = ["QlooCulturalIntelligenceAgent"]