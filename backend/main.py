"""
Updated Main Application
Initializes CareConnect system with Gemini-enhanced Qloo integration
"""

import logging
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Dict, Any

# Import the updated tools and agents
from multi_tool_agent.tools import initialize_all_tools, get_tool_manager

# Import agents with error handling
try:
    from multi_tool_agent.sequential_agent import CareConnectSequentialAgent
except ImportError:
    logger.warning("CareConnectSequentialAgent not available - using minimal mode")
    CareConnectSequentialAgent = None

try:
    from multi_tool_agent.agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
except ImportError:
    logger.warning("QlooCulturalIntelligenceAgent not available")
    QlooCulturalIntelligenceAgent = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variables
sequential_agent = None
tool_status = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown.
    """
    # Startup
    logger.info("🚀 Initializing CareConnect multi-agent system with Gemini-Qloo integration...")
    
    try:
        # Initialize tools with enhanced integration
        global tool_status
        tool_status = await initialize_all_tools()
        
        tool_manager = get_tool_manager()
        
        # Check tool availability
        qloo_available = tool_manager.is_qloo_available()
        gemini_available = tool_manager.is_gemini_available()
        
        logger.info(f"🔧 Tool Status:")
        logger.info(f"   - Qloo API: {'✅ Available' if qloo_available else '❌ Unavailable'}")
        logger.info(f"   - Gemini API: {'✅ Available' if gemini_available else '❌ Unavailable'}")
        
        if not qloo_available:
            logger.warning("⚠️  Qloo API unavailable - cultural recommendations will be limited")
        
        if not gemini_available:
            logger.warning("⚠️  Gemini API unavailable - query optimization disabled")
        
        # Initialize the sequential agent with enhanced tools
        global sequential_agent
        if CareConnectSequentialAgent:
            sequential_agent = CareConnectSequentialAgent(tool_manager)
            logger.info("✅ Sequential agent initialized")
        else:
            logger.warning("⚠️  Sequential agent not available - using direct Qloo mode")
            sequential_agent = None
        
        logger.info("✅ CareConnect system initialization complete")
        
        # Log final status
        status = tool_manager.get_tool_status()
        logger.info(f"📊 System Status: {status['total_tools']} tools, "
                   f"Qloo: {status['qloo_available']}, "
                   f"Gemini: {status['gemini_available']}")
        
    except Exception as e:
        logger.error(f"💥 Initialization failed: {e}")
        raise e
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down CareConnect system...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="CareConnect API",
    description="Multi-agent system for personalized care recommendations with Gemini-enhanced Qloo integration",
    version="2.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with system status."""
    tool_manager = get_tool_manager()
    status = tool_manager.get_tool_status()
    
    return {
        "message": "CareConnect API with Gemini-Enhanced Qloo Integration",
        "version": "2.0.0",
        "status": "operational",
        "features": {
            "gemini_query_optimization": status["gemini_available"],
            "cultural_recommendations": status["qloo_available"],
            "total_tools": status["total_tools"]
        },
        "tool_status": tool_status
    }

@app.get("/api/v1/status")
async def get_system_status():
    """Detailed system status endpoint."""
    tool_manager = get_tool_manager()
    status = tool_manager.get_tool_status()
    
    return {
        "system": "CareConnect Multi-Agent System",
        "version": "2.0.0",
        "initialization": {
            "completed": status["initialized"],
            "tools_available": status["available_tools"],
            "total_tools": status["total_tools"]
        },
        "capabilities": {
            "gemini_optimization": status["gemini_available"],
            "qloo_recommendations": status["qloo_available"],
            "enhanced_cultural_intelligence": status["gemini_available"] and status["qloo_available"]
        },
        "performance": status.get("qloo_cache_stats", {}),
        "tool_test_results": tool_status
    }

@app.post("/api/v1/careconnect")
async def process_careconnect_request(request_data: Dict[str, Any]):
    """
    Main CareConnect processing endpoint with Gemini-enhanced Qloo integration.
    """
    try:
        request_type = request_data.get("request_type", "dashboard")
        logger.info(f"🎯 Processing CareConnect request: {request_type}")
        
        if sequential_agent:
            # Use full sequential agent pipeline
            result = await sequential_agent.process_request(request_data)
        else:
            # Use direct Qloo processing as fallback
            result = await process_direct_qloo_request(request_data)
        
        # Add system metadata
        tool_manager = get_tool_manager()
        result["system_metadata"] = {
            "version": "2.0.0",
            "processing_mode": "gemini_enhanced" if sequential_agent else "direct_qloo",
            "qloo_optimization": tool_manager.is_qloo_available() and tool_manager.is_gemini_available(),
            "timestamp": result.get("timestamp")
        }
        
        # Log processing summary
        qloo_success = result.get("qloo_recommendations", {})
        if qloo_success:
            successful_types = sum(1 for r in qloo_success.values() if r.get("success"))
            logger.info(f"✅ CareConnect completed: {successful_types} successful recommendation types")
        
        return result
        
    except Exception as e:
        logger.error(f"💥 CareConnect request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

async def process_direct_qloo_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Direct Qloo processing when sequential agent is not available.
    """
    try:
        tool_manager = get_tool_manager()
        qloo_api = tool_manager.get_qloo_api()
        
        if not qloo_api:
            return {
                "success": False,
                "error": "Qloo API not available",
                "qloo_recommendations": {}
            }
        
        # Extract basic cultural information
        cultural_keywords = request_data.get("cultural_keywords", ["family", "food", "music"])
        demographic_signals = request_data.get("demographic_signals", {})
        
        # Process with Qloo
        logger.info("🎯 Processing direct Qloo request")
        qloo_results = await qloo_api.get_cultural_recommendations_with_gemini(
            cultural_keywords=cultural_keywords,
            demographic_signals=demographic_signals
        )
        
        return {
            "success": qloo_results.get("success", False),
            "qloo_recommendations": qloo_results.get("results", {}),
            "search_plan": qloo_results.get("search_plan", {}),
            "total_successful": qloo_results.get("total_successful", 0),
            "processing_mode": "direct_qloo",
            "timestamp": "2025-01-22"  # You might want to use actual timestamp
        }
        
    except Exception as e:
        logger.error(f"Direct Qloo processing failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "qloo_recommendations": {}
        }

@app.get("/api/v1/test/qloo")
async def test_qloo_integration():
    """
    Test endpoint for Qloo-Gemini integration.
    """
    try:
        tool_manager = get_tool_manager()
        qloo_api = tool_manager.get_qloo_api()
        
        if not qloo_api:
            return {"status": "unavailable", "error": "Qloo API not initialized"}
        
        # Test basic search
        search_result = await qloo_api._search_entities_simple("music", ["urn:entity:artist"])
        
        # Test Gemini optimization if available
        gemini_test = {"available": False}
        if tool_manager.is_gemini_available():
            cultural_keywords = ["italian", "family", "food"]
            demographic_signals = {"age_range": "adult", "general_location": {"city_region": "Chicago"}}
            
            gemini_result = await qloo_api._gemini_optimize_search_strategy(cultural_keywords, demographic_signals)
            gemini_test = {
                "available": True,
                "optimization_success": gemini_result.get("success", False),
                "query_categories": list(gemini_result.get("search_queries", {}).keys()) if gemini_result.get("success") else []
            }
        
        return {
            "qloo_search": {
                "success": search_result.get("success", False),
                "entities_found": len(search_result.get("entities", []))
            },
            "gemini_optimization": gemini_test,
            "integration_status": "operational" if search_result.get("success") else "limited"
        }
        
    except Exception as e:
        logger.error(f"Qloo test failed: {e}")
        return {"status": "error", "error": str(e)}

@app.post("/api/v1/test/cultural-recommendations")
async def test_cultural_recommendations(test_request: Dict[str, Any]):
    """
    Test endpoint for cultural recommendations with Gemini optimization.
    """
    try:
        tool_manager = get_tool_manager()
        qloo_api = tool_manager.get_qloo_api()
        
        if not qloo_api:
            return {"status": "unavailable", "error": "Qloo API not initialized"}
        
        # Extract test parameters
        cultural_keywords = test_request.get("cultural_keywords", ["italian", "family", "music"])
        demographic_signals = test_request.get("demographic_signals", {
            "age_range": "adult",
            "general_location": {"city_region": "Chicago"}
        })
        
        # Test the full Gemini-enhanced flow
        logger.info(f"🧪 Testing cultural recommendations with keywords: {cultural_keywords}")
        
        result = await qloo_api.get_cultural_recommendations_with_gemini(
            cultural_keywords=cultural_keywords,
            demographic_signals=demographic_signals
        )
        
        return {
            "test_status": "completed",
            "input": {
                "cultural_keywords": cultural_keywords,
                "demographic_signals": demographic_signals
            },
            "results": {
                "overall_success": result.get("success", False),
                "successful_types": result.get("total_successful", 0),
                "search_plan": result.get("search_plan", {}),
                "recommendations": result.get("results", {})
            },
            "system": {
                "gemini_available": tool_manager.is_gemini_available(),
                "qloo_available": tool_manager.is_qloo_available()
            }
        }
        
    except Exception as e:
        logger.error(f"Cultural recommendations test failed: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)