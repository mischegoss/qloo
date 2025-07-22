"""
Updated Tools Initialization
Sets up Gemini-enhanced Qloo API integration
"""

import logging
import os
from typing import Dict, Any

# Set up logger first
logger = logging.getLogger(__name__)

# Import the enhanced tools with error handling
from .qloo_tools import QlooInsightsAPI
from .gemini_tools import GeminiAITool

# Import existing tools with fallbacks
try:
    from .youtube_tools import YouTubeAPI
except ImportError:
    logger.warning("YouTubeAPI not available")
    YouTubeAPI = None

# Handle vision tools more robustly
VisionAITool = None
try:
    from .vision_ai_tools import VisionAIAnalyzer as VisionAITool
except ImportError:
    try:
        # Try other possible names
        from .vision_ai_tools import VisionAITool
    except ImportError:
        try:
            # Try another common name
            from .vision_ai_tools import GoogleVisionAI as VisionAITool
        except ImportError:
            # Give up and skip vision tools
            logger.warning("VisionAITool not available - skipping vision functionality")
            VisionAITool = None

# Handle session storage tools
SessionStorageTool = None
try:
    from .session_storage_tools import SessionStorageManager as SessionStorageTool
except ImportError:
    try:
        # Try alternative import names
        from .session_storage_tools import SessionStorageTool
    except ImportError:
        try:
            # Try another name
            from .session_storage_tools import SessionStorage as SessionStorageTool
        except ImportError:
            logger.warning("SessionStorageTool not available - skipping session functionality")
            SessionStorageTool = None

logger = logging.getLogger(__name__)

class ToolManager:
    """
    Manages all tools with enhanced Gemini-Qloo integration.
    """
    
    def __init__(self):
        self.tools = {}
        self.initialized = False
        
    async def initialize_tools(self) -> Dict[str, bool]:
        """
        Initialize all tools with enhanced integration.
        """
        logger.info("🚀 Initializing tools with Gemini-Qloo integration...")
        
        results = {}
        
        try:
            # 1. Initialize Gemini first (needed for Qloo optimization)
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            if gemini_api_key:
                self.tools["gemini"] = GeminiAITool(
                    api_key=gemini_api_key,
                    model="gemini-2.5-flash"
                )
                gemini_test = await self.tools["gemini"].test_connection()
                results["gemini_tool"] = gemini_test
                logger.info(f"✅ Gemini tool: {'PASSED' if gemini_test else 'FAILED'}")
            else:
                logger.error("❌ GEMINI_API_KEY not found")
                results["gemini_tool"] = False
            
            # 2. Initialize Qloo with Gemini integration
            qloo_api_key = os.getenv("QLOO_API_KEY")
            if qloo_api_key and self.tools.get("gemini"):
                self.tools["qloo"] = QlooInsightsAPI(
                    api_key=qloo_api_key,
                    gemini_client=self.tools["gemini"],
                    base_url="https://hackathon.api.qloo.com"
                )
                qloo_test = await self.tools["qloo"].test_connection()
                results["qloo_tool"] = qloo_test
                logger.info(f"✅ Qloo tool: {'PASSED' if qloo_test else 'FAILED'}")
            else:
                logger.error("❌ QLOO_API_KEY not found or Gemini not available")
                results["qloo_tool"] = False
            
            # 3. Initialize YouTube API (if available)
            if YouTubeAPI:
                youtube_api_key = os.getenv("YOUTUBE_API_KEY")
                if youtube_api_key:
                    self.tools["youtube"] = YouTubeAPI(api_key=youtube_api_key)
                    try:
                        youtube_test = await self.tools["youtube"].test_connection()
                        results["youtube_tool"] = youtube_test
                        logger.info(f"✅ YouTube tool: {'PASSED' if youtube_test else 'FAILED'}")
                    except Exception as e:
                        logger.warning(f"YouTube test failed: {e}")
                        results["youtube_tool"] = False
                else:
                    logger.warning("⚠️  YOUTUBE_API_KEY not found")
                    results["youtube_tool"] = False
            else:
                logger.warning("⚠️  YouTube tool not available")
                results["youtube_tool"] = False
            
            # 4. Initialize Vision AI (if available)
            if VisionAITool:
                vision_api_key = os.getenv("VISION_API_KEY")
                if vision_api_key:
                    self.tools["vision"] = VisionAITool(api_key=vision_api_key)
                    try:
                        vision_test = await self.tools["vision"].test_connection()
                        results["vision_ai_tool"] = vision_test
                        logger.info(f"✅ Vision AI tool: {'PASSED' if vision_test else 'FAILED'}")
                    except Exception as e:
                        logger.warning(f"Vision AI test failed: {e}")
                        results["vision_ai_tool"] = False
                else:
                    logger.warning("⚠️  VISION_API_KEY not found")
                    results["vision_ai_tool"] = False
            else:
                logger.warning("⚠️  Vision AI tool not available")
                results["vision_ai_tool"] = False
            
            # 5. Initialize Session Storage (if available)
            if SessionStorageTool:
                self.tools["session_storage"] = SessionStorageTool()
                try:
                    session_test = self.tools["session_storage"].test_connection()
                    results["session_storage_tool"] = session_test
                    logger.info(f"✅ Session storage tool: {'PASSED' if session_test else 'FAILED'}")
                except Exception as e:
                    logger.warning(f"Session storage test failed: {e}")
                    results["session_storage_tool"] = False
            else:
                logger.warning("⚠️  Session storage tool not available")
                results["session_storage_tool"] = False
            
            # Summary
            passed_tools = sum(1 for passed in results.values() if passed)
            total_tools = len(results)
            
            logger.info(f"🎯 Tool initialization complete: {passed_tools}/{total_tools} tools working")
            
            # Check for minimum viable tools (Gemini + Qloo for core functionality)
            core_tools_available = results.get("gemini_tool", False) and results.get("qloo_tool", False)
            
            if core_tools_available:
                self.initialized = True
                logger.info("✅ Core tools (Gemini + Qloo) available - system operational")
            elif passed_tools >= 2:  # At least some tools working
                self.initialized = True
                logger.warning("⚠️  Limited functionality - some tools unavailable")
            else:
                logger.error("❌ Insufficient tools for operation")
            
            return results
            
        except Exception as e:
            logger.error(f"💥 Tool initialization failed: {e}")
            return {"error": str(e)}
    
    def get_tool(self, tool_name: str):
        """Get a specific tool."""
        return self.tools.get(tool_name)
    
    def get_qloo_api(self) -> QlooInsightsAPI:
        """Get the Gemini-enhanced Qloo API."""
        return self.tools.get("qloo")
    
    def get_gemini_api(self) -> GeminiAITool:
        """Get the Gemini API."""
        return self.tools.get("gemini")
    
    def is_qloo_available(self) -> bool:
        """Check if Qloo API is available and working."""
        qloo_tool = self.tools.get("qloo")
        return qloo_tool is not None
    
    def is_gemini_available(self) -> bool:
        """Check if Gemini API is available and working."""
        gemini_tool = self.tools.get("gemini")
        return gemini_tool is not None
    
    def get_tool_status(self) -> Dict[str, Any]:
        """Get status of all tools."""
        status = {
            "initialized": self.initialized,
            "available_tools": list(self.tools.keys()),
            "qloo_available": self.is_qloo_available(),
            "gemini_available": self.is_gemini_available(),
            "total_tools": len(self.tools)
        }
        
        # Add cache stats for performance monitoring
        if self.is_qloo_available():
            qloo_stats = self.tools["qloo"].get_cache_stats()
            status["qloo_cache_stats"] = qloo_stats
        
        return status

# Global tool manager instance
tool_manager = ToolManager()

async def initialize_all_tools():
    """Initialize all tools - main entry point."""
    return await tool_manager.initialize_tools()

def get_qloo_api():
    """Get the Gemini-enhanced Qloo API."""
    return tool_manager.get_qloo_api()

def get_gemini_api():
    """Get the Gemini API."""
    return tool_manager.get_gemini_api()

def get_tool_manager():
    """Get the tool manager instance."""
    return tool_manager

# Export the enhanced tools
__all__ = [
    "tool_manager",
    "initialize_all_tools", 
    "get_qloo_api",
    "get_gemini_api",
    "get_tool_manager",
    "QlooInsightsAPI",
    "GeminiAITool"
]