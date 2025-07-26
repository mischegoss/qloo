"""
Agent 3: Simplified Qloo Cultural Analysis - CORRECTED METHOD SIGNATURE
File: backend/multi_tool_agent/agents/qloo_cultural_analysis_agent.py

CORRECTED FOR TEST COMPATIBILITY:
- Fixed run() method signature to match test expectations
- Heritage → classical artists + cuisine places
- No complex age/location/URN filtering  
- Uses new simplified qloo_tools.py methods
- Clean, reliable, fast
"""

import logging
from datetime import datetime, date
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class QlooCulturalAnalysisAgent:
    """
    SIMPLIFIED Agent 3: Cultural Analysis using heritage-only approach.
    CORRECTED: Method signature matches test expectations.
    """
    
    def __init__(self, qloo_tool):
        self.qloo_tool = qloo_tool
        logger.info("✅ Step 3: Simple Qloo Cultural Analysis Agent initialized")
    
    async def run(self,
                  consolidated_info: Dict[str, Any],
                  cultural_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        SIMPLIFIED: Generate cultural intelligence using heritage only.
        CORRECTED: Accepts both consolidated_info and cultural_profile parameters.
        
        Args:
            consolidated_info: Contains patient_profile with cultural_heritage
            cultural_profile: Optional cultural profile data (not used in simplified version)
        """
        
        logger.info("🚀 Step 3: Starting Qloo Cultural Analysis")
        
        try:
            # Extract heritage from consolidated info - handle both formats
            patient_profile = consolidated_info.get("patient_profile", {})
            
            # Fallback to patient_info if patient_profile not found
            if not patient_profile:
                patient_profile = consolidated_info.get("patient_info", {})
            
            cultural_heritage = patient_profile.get("cultural_heritage", "American")
            birth_year = patient_profile.get("birth_year", 1945)
            
            logger.info(f"🎯 Cultural heritage: {cultural_heritage}")
            logger.info(f"🎯 Birth year: {birth_year}")
            
            # Check if Qloo tool is available
            if not self.qloo_tool:
                logger.info("⚠️ No Qloo tool - will use fallback data only")
                return self._create_fallback_response(cultural_heritage)
            
            logger.info("✅ Qloo tool available - will attempt API calls")
            
            # Generate daily seed for variety
            today_str = date.today().isoformat()
            daily_seed = hash(f"{today_str}-{cultural_heritage}")
            logger.info(f"📅 Daily seed: {daily_seed}")
            
            # SIMPLIFIED: Make heritage-based cultural calls
            logger.info("🎵🍽️ Making focused Qloo calls: Artists + Places")
            
            cultural_results = await self.qloo_tool.make_cultural_calls(cultural_heritage)
            
            # Check results
            successful_calls = cultural_results.get("successful_calls", 0)
            total_results = cultural_results.get("total_results", 0)
            
            logger.info(f"🎯 Cultural calls completed: {successful_calls}/2 successful")
            
            # Format response
            qloo_intelligence = {
                "cultural_recommendations": cultural_results.get("cultural_recommendations", {}),
                "metadata": {
                    "agent": "qloo_cultural_analysis",
                    "version": "simplified_heritage_only",
                    "approach": "heritage_based_calls",
                    "heritage": cultural_heritage,
                    "birth_year": birth_year,
                    "successful_calls": successful_calls,
                    "total_results": total_results,
                    "daily_seed": daily_seed,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            logger.info("✅ Step 3: Qloo cultural analysis completed")
            
            return {"qloo_intelligence": qloo_intelligence}
            
        except Exception as e:
            logger.error(f"❌ Step 3: Cultural analysis failed: {e}")
            heritage = consolidated_info.get("patient_profile", {}).get("cultural_heritage", "American")
            if not heritage:
                heritage = consolidated_info.get("patient_info", {}).get("cultural_heritage", "American")
            return self._create_fallback_response(heritage)
    
    def _create_fallback_response(self, heritage: str) -> Dict[str, Any]:
        """
        Create fallback cultural intelligence when Qloo is unavailable.
        """
        
        logger.info("🔄 Creating fallback cultural intelligence")
        
        # Heritage-specific fallbacks
        heritage_data = {
            "Italian-American": {
                "artists": [
                    {"name": "Pavarotti", "type": "Opera singer", "era": "1935-2007"},
                    {"name": "Vivaldi", "type": "Baroque composer", "era": "1678-1741"},
                    {"name": "Puccini", "type": "Opera composer", "era": "1858-1924"}
                ],
                "places": [
                    {"name": "Traditional Italian Trattoria", "type": "Italian restaurant"},
                    {"name": "Family-Style Italian Kitchen", "type": "Casual Italian dining"}
                ]
            },
            "Irish": {
                "artists": [
                    {"name": "Celtic Orchestra", "type": "Traditional ensemble"},
                    {"name": "Irish Traditional Musicians", "type": "Folk group"},
                    {"name": "Dublin Philharmonic", "type": "Classical orchestra"}
                ],
                "places": [
                    {"name": "Traditional Irish Pub", "type": "Irish restaurant"},
                    {"name": "Celtic Kitchen", "type": "Irish comfort food"}
                ]
            },
            "American": {
                "artists": [
                    {"name": "Aaron Copland", "type": "American composer", "era": "1900-1990"},
                    {"name": "George Gershwin", "type": "American composer", "era": "1898-1937"},
                    {"name": "John Philip Sousa", "type": "March composer", "era": "1854-1932"}
                ],
                "places": [
                    {"name": "Classic American Diner", "type": "American restaurant"},
                    {"name": "Hometown Comfort Food", "type": "Family dining"}
                ]
            }
        }
        
        # Get appropriate fallback data
        fallback_data = heritage_data.get(heritage, heritage_data["American"])
        
        qloo_intelligence = {
            "cultural_recommendations": {
                "artists": {
                    "success": True,
                    "entities": fallback_data["artists"],
                    "entity_count": len(fallback_data["artists"]),
                    "content_type": "fallback"
                },
                "places": {
                    "success": True,
                    "entities": fallback_data["places"],
                    "entity_count": len(fallback_data["places"]),
                    "content_type": "fallback"
                }
            },
            "metadata": {
                "agent": "qloo_cultural_analysis",
                "version": "simplified_heritage_only",
                "approach": "fallback_heritage_data",
                "heritage": heritage,
                "successful_calls": 0,
                "total_results": len(fallback_data["artists"]) + len(fallback_data["places"]),
                "fallback_reason": "qloo_unavailable",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return {"qloo_intelligence": qloo_intelligence}

# Export for backwards compatibility with existing imports
QlooCulturalIntelligenceAgent = QlooCulturalAnalysisAgent

# Export for imports
__all__ = ["QlooCulturalAnalysisAgent", "QlooCulturalIntelligenceAgent"]