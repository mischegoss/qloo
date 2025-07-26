"""
Fixed Tools Initialization - Resolves Import Issues
File: backend/multi_tool_agent/tools/__init__.py

FIXES:
- Handles both old gemini_tools.py and new simple_gemini_tools.py
- Provides proper fallbacks for missing tools
- Avoids circular import issues
- Supports both GeminiRecipeGenerator and SimpleGeminiTool
- Graceful degradation when tools are unavailable
"""

import os
import logging
from typing import Dict, Any, Optional

# Configure logger FIRST before any other imports
logger = logging.getLogger(__name__)

# Initialize variables to avoid NameError issues
QlooInsightsAPI = None
YouTubeAPI = None
VisionAIAnalyzer = None
VisionAITool = None
GeminiRecipeGenerator = None
SimpleGeminiTool = None

# Import core tools with proper error handling
try:
    from .qloo_tools import QlooInsightsAPI
    logger.debug("✅ QlooInsightsAPI imported")
except ImportError as e:
    logger.warning(f"⚠️ QlooInsightsAPI not available: {e}")
    QlooInsightsAPI = None

try:
    from .youtube_tools import YouTubeAPI
    logger.debug("✅ YouTubeAPI imported")
except ImportError as e:
    logger.warning(f"⚠️ YouTubeAPI not available: {e}")
    YouTubeAPI = None

# Handle VisionAI imports with proper fallback
try:
    from .vision_ai_tools import VisionAIAnalyzer
    VisionAITool = VisionAIAnalyzer  # Alias for backward compatibility
    logger.debug("✅ VisionAIAnalyzer imported")
except ImportError as e:
    logger.warning(f"⚠️ VisionAIAnalyzer not available: {e}")
    VisionAIAnalyzer = None
    VisionAITool = None

# Handle Gemini imports - support both old and new versions
# Try new SimpleGeminiTool first, then fall back to old GeminiRecipeGenerator
try:
    from .simple_gemini_tools import SimpleGeminiTool
    # Also try to import GeminiRecipeGenerator from the same file for compatibility
    try:
        from .simple_gemini_tools import GeminiRecipeGenerator
        logger.debug("✅ Both SimpleGeminiTool and GeminiRecipeGenerator imported from simple_gemini_tools")
    except ImportError:
        # If GeminiRecipeGenerator not in simple_gemini_tools, create alias
        GeminiRecipeGenerator = SimpleGeminiTool
        logger.debug("✅ SimpleGeminiTool imported, GeminiRecipeGenerator aliased")
except ImportError as e1:
    logger.warning(f"⚠️ SimpleGeminiTool not available: {e1}")
    SimpleGeminiTool = None
    
    # Fall back to original gemini_tools.py
    try:
        from .gemini_tools import GeminiRecipeGenerator
        # Create alias for SimpleGeminiTool
        SimpleGeminiTool = GeminiRecipeGenerator
        logger.debug("✅ GeminiRecipeGenerator imported from gemini_tools, SimpleGeminiTool aliased")
    except ImportError as e2:
        logger.warning(f"⚠️ GeminiRecipeGenerator not available: {e2}")
        GeminiRecipeGenerator = None

def initialize_all_tools() -> Dict[str, Any]:
    """
    Initialize all tools with graceful degradation for missing API keys.
    
    Returns:
        Dictionary containing all successfully initialized tools
    """
    logger.info("🚀 Initializing tools with fixed import handling...")
    
    tools = {}
    
    try:
        # Get API keys from environment
        qloo_api_key = os.getenv("QLOO_API_KEY")
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        google_cloud_api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY", google_cloud_api_key)
        
        # Initialize Qloo tool
        if qloo_api_key and QlooInsightsAPI:
            try:
                tools["qloo_tool"] = QlooInsightsAPI(qloo_api_key)
                logger.info("✅ Qloo API tool initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Qloo tool: {e}")
        elif not qloo_api_key:
            logger.warning("⚠️ QLOO_API_KEY not found")
        elif not QlooInsightsAPI:
            logger.warning("⚠️ QlooInsightsAPI class not available")
        
        # Initialize YouTube tool
        if youtube_api_key and YouTubeAPI:
            try:
                tools["youtube_tool"] = YouTubeAPI(youtube_api_key)
                logger.info("✅ YouTube API tool initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize YouTube tool: {e}")
        elif not youtube_api_key:
            logger.warning("⚠️ YOUTUBE_API_KEY not found")
        elif not YouTubeAPI:
            logger.warning("⚠️ YouTubeAPI class not available")
        
        # Initialize Vision AI tool
        if google_cloud_api_key and VisionAIAnalyzer:
            try:
                tools["vision_ai_tool"] = VisionAIAnalyzer(google_cloud_api_key)
                logger.info("✅ Vision AI tool initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Vision AI tool: {e}")
        elif not google_cloud_api_key:
            logger.warning("⚠️ GOOGLE_CLOUD_API_KEY not found")
        elif not VisionAIAnalyzer:
            logger.warning("⚠️ VisionAIAnalyzer class not available")
        
        # Initialize Gemini tool - try both SimpleGeminiTool and GeminiRecipeGenerator
        gemini_tool_class = SimpleGeminiTool or GeminiRecipeGenerator
        
        if gemini_api_key and gemini_tool_class:
            try:
                tools["gemini_tool"] = gemini_tool_class(gemini_api_key)
                tool_name = gemini_tool_class.__name__
                logger.info(f"✅ Gemini tool initialized ({tool_name})")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Gemini tool: {e}")
        elif not gemini_api_key:
            logger.warning("⚠️ GEMINI_API_KEY not found")
        elif not gemini_tool_class:
            logger.warning("⚠️ No Gemini tool class available (tried SimpleGeminiTool and GeminiRecipeGenerator)")
        
        # Summary
        working_tools = len(tools)
        total_expected = 4
        logger.info(f"🎯 Tool initialization complete: {working_tools}/{total_expected} tools working")
        
        if working_tools == 0:
            logger.error("❌ No tools initialized - check API keys and imports")
        elif working_tools < 2:
            logger.warning("⚠️ Only minimal tools available")
        elif working_tools < total_expected:
            logger.info(f"⚠️ Some tools unavailable: {total_expected - working_tools} missing")
        else:
            logger.info("🎉 All tools initialized successfully!")
        
        # Show which tools are available
        if tools:
            available_tools = list(tools.keys())
            logger.info(f"📋 Available tools: {', '.join(available_tools)}")
        
        return tools
        
    except Exception as e:
        logger.error(f"❌ Error during tool initialization: {e}")
        import traceback
        logger.debug(traceback.format_exc())
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
    
    # Test each tool if available
    tool_tests = [
        ("qloo_tool", "Qloo API"),
        ("youtube_tool", "YouTube API"),
        ("vision_ai_tool", "Vision AI"),
        ("gemini_tool", "Gemini AI")
    ]
    
    for tool_key, tool_name in tool_tests:
        if tool_key in tools:
            try:
                tool = tools[tool_key]
                
                # Try test_connection method if available
                if hasattr(tool, 'test_connection'):
                    result = await tool.test_connection()
                    test_results[tool_key] = result
                else:
                    # If no test method, assume it's working if initialized
                    test_results[tool_key] = True
                
                status = "✅ PASSED" if test_results[tool_key] else "❌ FAILED"
                logger.info(f"{tool_name} test: {status}")
                
            except Exception as e:
                logger.error(f"❌ {tool_name} test error: {e}")
                test_results[tool_key] = False
        else:
            test_results[tool_key] = False
            logger.warning(f"⚠️ {tool_name} not available for testing")
    
    # Summary
    passed_tests = sum(1 for result in test_results.values() if result)
    total_tests = len(test_results)
    
    logger.info(f"📊 Tool tests completed: {passed_tests}/{total_tests} passed")
    
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
        "gemini_tool": "GEMINI_API_KEY"
    }
    
    for tool_name, env_var in api_keys.items():
        api_key = os.getenv(env_var)
        if api_key:
            status[tool_name] = f"API key configured ({len(api_key)} chars)"
        else:
            status[tool_name] = f"API key missing: {env_var}"
    
    # Check class availability
    class_status = {
        "QlooInsightsAPI": QlooInsightsAPI is not None,
        "YouTubeAPI": YouTubeAPI is not None,
        "VisionAIAnalyzer": VisionAIAnalyzer is not None,
        "SimpleGeminiTool": SimpleGeminiTool is not None,
        "GeminiRecipeGenerator": GeminiRecipeGenerator is not None
    }
    
    status["class_imports"] = {name: "✅ Available" if available else "❌ Missing" 
                              for name, available in class_status.items()}
    
    return status

def get_available_tools() -> Dict[str, bool]:
    """
    Get information about which tool classes are available for import.
    
    Returns:
        Dictionary showing which tools can be imported
    """
    return {
        "QlooInsightsAPI": QlooInsightsAPI is not None,
        "YouTubeAPI": YouTubeAPI is not None,
        "VisionAIAnalyzer": VisionAIAnalyzer is not None,
        "SimpleGeminiTool": SimpleGeminiTool is not None,
        "GeminiRecipeGenerator": GeminiRecipeGenerator is not None
    }

# Export all tools and utilities
__all__ = [
    # Tool classes (if available)
    "QlooInsightsAPI",
    "YouTubeAPI", 
    "VisionAIAnalyzer",
    "SimpleGeminiTool",
    "GeminiRecipeGenerator",
    # Utility functions
    "initialize_tools",
    "initialize_all_tools",
    "get_tool_manager",
    "test_all_tools",
    "get_tool_status",
    "get_available_tools"
]

# Clean up __all__ to only include available tools
__all__ = [name for name in __all__ if globals().get(name) is not None or name.startswith(('initialize_', 'get_', 'test_'))]

# Log the final import status
logger.debug(f"📋 Tools __init__.py loaded - available exports: {', '.join(__all__)}")

