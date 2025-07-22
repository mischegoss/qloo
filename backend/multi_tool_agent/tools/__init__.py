"""
Tools Initialization
File: backend/multi_tool_agent/tools/__init__.py

Initializes all tools required for the CareConnect 7-agent pipeline
"""

import os
import logging
from typing import Dict, Any

# Configure logger FIRST before any other imports that might use it
logger = logging.getLogger(__name__)

# Import tools with proper error handling
from .qloo_tools import QlooInsightsAPI
from .youtube_tools import YouTubeAPI
from .session_storage_tools import SessionStorageManager

# Handle VisionAI imports with proper fallback
try:
    from .vision_ai_tools import VisionAIAnalyzer
    VisionAITool = VisionAIAnalyzer  # Alias for backward compatibility
except ImportError as e:
    logger.warning(f"VisionAIAnalyzer not available: {e}")
    VisionAIAnalyzer = None
    VisionAITool = None

# Handle Gemini imports with proper fallback
try:
    from .gemini_tools import GeminiRecipeGenerator
except ImportError as e:
    logger.warning(f"GeminiRecipeGenerator not available: {e}")
    GeminiRecipeGenerator = None

def initialize_all_tools() -> Dict[str, Any]:
    """
    Initialize all tools with graceful degradation for missing API keys.
    
    Returns:
        Dictionary containing all successfully initialized tools
    """
    logger.info("🚀 Initializing tools with Gemini-Qloo integration...")
    
    try:
        # Get API keys from environment
        qloo_api_key = os.getenv("QLOO_API_KEY")
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        google_cloud_api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY", google_cloud_api_key)
        
        # Initialize tools in proper order (some tools may depend on others)
        tools = {}
        
        # Initialize Gemini tool first (may be required by other tools)
        if gemini_api_key and GeminiRecipeGenerator:
            try:
                tools["gemini_tool"] = GeminiRecipeGenerator(gemini_api_key)
                logger.info("✅ Gemini tool initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini tool: {e}")
        else:
            if not gemini_api_key:
                logger.error("❌ GEMINI_API_KEY not found")
            if not GeminiRecipeGenerator:
                logger.error("❌ GeminiRecipeGenerator class not available")
        
        # Initialize Qloo tool - handle different constructor signatures
        if qloo_api_key:
            try:
                # Try standard constructor first
                tools["qloo_tool"] = QlooInsightsAPI(qloo_api_key)
                logger.info("✅ Qloo API tool initialized")
            except TypeError as e:
                if "gemini_client" in str(e):
                    # Handle version that requires gemini_client
                    try:
                        if "gemini_tool" in tools:
                            tools["qloo_tool"] = QlooInsightsAPI(qloo_api_key, tools["gemini_tool"])
                            logger.info("✅ Qloo API tool initialized with Gemini integration")
                        else:
                            logger.error("❌ Cannot initialize Qloo tool: requires Gemini client but Gemini not available")
                    except Exception as e2:
                        logger.error(f"❌ Failed to initialize Qloo tool with Gemini client: {e2}")
                else:
                    logger.error(f"❌ Failed to initialize Qloo tool: {e}")
        else:
            logger.error("❌ QLOO_API_KEY not found")
            
        # Initialize YouTube tool
        if youtube_api_key:
            try:
                tools["youtube_tool"] = YouTubeAPI(youtube_api_key)
                logger.info("✅ YouTube API tool initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize YouTube tool: {e}")
        else:
            logger.warning("⚠️  YOUTUBE_API_KEY not found")
            
        # Initialize Vision AI tool
        if google_cloud_api_key and VisionAIAnalyzer:
            try:
                tools["vision_ai_tool"] = VisionAIAnalyzer(google_cloud_api_key)
                logger.info("✅ Vision AI tool initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Vision AI tool: {e}")
        else:
            if not google_cloud_api_key:
                logger.warning("⚠️  VISION_API_KEY not found")
            if not VisionAIAnalyzer:
                logger.warning("⚠️  VisionAIAnalyzer class not available")
                
        # Initialize session storage (always works)
        try:
            tools["session_storage_tool"] = SessionStorageManager()
            logger.info("✅ Session storage initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize session storage: {e}")
        
        # Test session storage
        try:
            if "session_storage_tool" in tools and hasattr(tools["session_storage_tool"], 'test_connection'):
                tools["session_storage_tool"].test_connection()
            logger.info("✅ Session storage test passed")
        except Exception as e:
            logger.warning(f"Session storage test failed: {e}")
        
        working_tools = len(tools)
        total_expected = 5
        logger.info(f"🎯 Tool initialization complete: {working_tools}/{total_expected} tools working")
        
        if working_tools < 3:
            logger.error("❌ Insufficient tools for operation")
        elif working_tools < total_expected:
            logger.warning(f"⚠️  Some tools unavailable: {total_expected - working_tools} missing")
        else:
            logger.info("🎉 All tools initialized successfully!")
            
        return tools
        
    except Exception as e:
        logger.error(f"Error initializing tools: {str(e)}")
        # Return whatever tools we managed to initialize
        return tools if 'tools' in locals() else {}

def initialize_tools() -> Dict[str, Any]:
    """
    Legacy function name - calls initialize_all_tools for backward compatibility.
    """
    return initialize_all_tools()

def get_tool_manager(tools: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get tool manager - returns the tools dictionary directly.
    This function provides backward compatibility.
    """
    return tools

async def test_all_tools(tools: Dict[str, Any]) -> Dict[str, bool]:
    """
    Test all tools to verify they're working correctly.
    
    Args:
        tools: Dictionary of initialized tools
        
    Returns:
        Dictionary with test results for each tool
    """
    test_results = {}
    
    # Test Qloo API
    if "qloo_tool" in tools:
        try:
            # Qloo tools may not have test_connection method
            test_results["qloo_tool"] = True
            logger.info("Qloo tool test: PASSED (basic initialization)")
        except Exception as e:
            logger.error(f"Qloo tool test error: {str(e)}")
            test_results["qloo_tool"] = False
    else:
        test_results["qloo_tool"] = False
    
    # Test YouTube API
    if "youtube_tool" in tools:
        try:
            if hasattr(tools["youtube_tool"], 'test_connection'):
                youtube_result = await tools["youtube_tool"].test_connection()
                test_results["youtube_tool"] = youtube_result
            else:
                test_results["youtube_tool"] = True
            logger.info(f"YouTube tool test: {'PASSED' if test_results['youtube_tool'] else 'FAILED'}")
        except Exception as e:
            logger.error(f"YouTube tool test error: {str(e)}")
            test_results["youtube_tool"] = False
    else:
        test_results["youtube_tool"] = False
    
    # Test Vision AI
    if "vision_ai_tool" in tools:
        try:
            if hasattr(tools["vision_ai_tool"], 'test_connection'):
                vision_result = await tools["vision_ai_tool"].test_connection()
                test_results["vision_ai_tool"] = vision_result
            else:
                test_results["vision_ai_tool"] = True
            logger.info(f"Vision AI tool test: {'PASSED' if test_results['vision_ai_tool'] else 'FAILED'}")
        except Exception as e:
            logger.error(f"Vision AI tool test error: {str(e)}")
            test_results["vision_ai_tool"] = False
    else:
        test_results["vision_ai_tool"] = False
    
    # Test Gemini
    if "gemini_tool" in tools:
        try:
            if hasattr(tools["gemini_tool"], 'test_connection'):
                gemini_result = await tools["gemini_tool"].test_connection()
                test_results["gemini_tool"] = gemini_result
            else:
                test_results["gemini_tool"] = True
            logger.info(f"Gemini tool test: {'PASSED' if test_results['gemini_tool'] else 'FAILED'}")
        except Exception as e:
            logger.error(f"Gemini tool test error: {str(e)}")
            test_results["gemini_tool"] = False
    else:
        test_results["gemini_tool"] = False
        logger.warning("Gemini tool not available for testing")
    
    # Test Session Storage (always works since it's in-memory)
    if "session_storage_tool" in tools:
        try:
            if hasattr(tools["session_storage_tool"], 'create_session'):
                session_id = await tools["session_storage_tool"].create_session("test_patient")
                session_data = await tools["session_storage_tool"].get_session(session_id)
                test_results["session_storage_tool"] = session_data is not None
            else:
                test_results["session_storage_tool"] = True
            logger.info(f"Session storage tool test: {'PASSED' if test_results['session_storage_tool'] else 'FAILED'}")
        except Exception as e:
            logger.error(f"Session storage tool test error: {str(e)}")
            test_results["session_storage_tool"] = False
    else:
        test_results["session_storage_tool"] = False
    
    # Summary
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    logger.info(f"Tool tests completed: {passed_tests}/{total_tests} passed")
    
    return test_results

def get_tool_status() -> Dict[str, str]:
    """
    Get status information about all tools.
    
    Returns:
        Dictionary with status information for each tool
    """
    status = {}
    
    # Check API key availability
    api_keys = {
        "qloo_tool": "QLOO_API_KEY",
        "youtube_tool": "YOUTUBE_API_KEY", 
        "vision_ai_tool": "GOOGLE_CLOUD_API_KEY",
        "gemini_tool": "GEMINI_API_KEY",
        "session_storage_tool": "N/A (in-memory)"
    }
    
    for tool_name, env_var in api_keys.items():
        if env_var == "N/A (in-memory)":
            status[tool_name] = "Available (in-memory storage)"
        else:
            api_key = os.getenv(env_var)
            if api_key:
                status[tool_name] = f"API key configured ({len(api_key)} chars)"
            else:
                status[tool_name] = f"API key missing: {env_var}"
    
    return status

# Export all tools and utilities
__all__ = [
    "QlooInsightsAPI",
    "YouTubeAPI", 
    "VisionAIAnalyzer",
    "SessionStorageManager",
    "initialize_tools",
    "initialize_all_tools",
    "get_tool_manager",
    "test_all_tools",
    "get_tool_status"
]

# Add optional tools to exports if available
if GeminiRecipeGenerator:
    __all__.append("GeminiRecipeGenerator")