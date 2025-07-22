"""
Tools Initialization
File: backend/multi_tool_agent/tools/__init__.py

Initializes all tools required for the CareConnect 7-agent pipeline
"""

import os
import logging
from typing import Dict, Any

from .qloo_tools import QlooInsightsAPI
from .youtube_tools import YouTubeAPI
from .vision_ai_tools import VisionAIAnalyzer
from .gemini_tools import GeminiRecipeGenerator
from .session_storage_tools import SessionStorageManager

logger = logging.getLogger(__name__)

def initialize_tools() -> Dict[str, Any]:
    """
    Initialize all tools required for the CareConnect multi-agent system.
    
    Returns:
        Dictionary containing all initialized tools
    """
    
    try:
        # Get API keys from environment
        qloo_api_key = os.getenv("QLOO_API_KEY")
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        google_cloud_api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY")  # Could be same as google_cloud_api_key
        
        # Check required API keys
        missing_keys = []
        if not qloo_api_key:
            missing_keys.append("QLOO_API_KEY")
        if not youtube_api_key:
            missing_keys.append("YOUTUBE_API_KEY")
        if not google_cloud_api_key:
            missing_keys.append("GOOGLE_CLOUD_API_KEY")
        if not gemini_api_key:
            # Fallback to Google Cloud API key for Gemini
            gemini_api_key = google_cloud_api_key
            if not gemini_api_key:
                missing_keys.append("GEMINI_API_KEY or GOOGLE_CLOUD_API_KEY")
        
        if missing_keys:
            logger.error(f"Missing required API keys: {missing_keys}")
            raise ValueError(f"Missing API keys: {missing_keys}")
        
        # Initialize all tools
        tools = {
            "qloo_tool": QlooInsightsAPI(qloo_api_key),
            "youtube_tool": YouTubeAPI(youtube_api_key),
            "vision_ai_tool": VisionAIAnalyzer(google_cloud_api_key),
            "gemini_tool": GeminiRecipeGenerator(gemini_api_key),
            "session_storage_tool": SessionStorageManager()
        }
        
        logger.info("All tools initialized successfully")
        return tools
        
    except Exception as e:
        logger.error(f"Error initializing tools: {str(e)}")
        raise

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
    try:
        qloo_result = await tools["qloo_tool"].test_connection()
        test_results["qloo_tool"] = qloo_result
        logger.info(f"Qloo tool test: {'PASSED' if qloo_result else 'FAILED'}")
    except Exception as e:
        logger.error(f"Qloo tool test error: {str(e)}")
        test_results["qloo_tool"] = False
    
    # Test YouTube API
    try:
        youtube_result = await tools["youtube_tool"].test_connection()
        test_results["youtube_tool"] = youtube_result
        logger.info(f"YouTube tool test: {'PASSED' if youtube_result else 'FAILED'}")
    except Exception as e:
        logger.error(f"YouTube tool test error: {str(e)}")
        test_results["youtube_tool"] = False
    
    # Test Vision AI
    try:
        vision_result = await tools["vision_ai_tool"].test_connection()
        test_results["vision_ai_tool"] = vision_result
        logger.info(f"Vision AI tool test: {'PASSED' if vision_result else 'FAILED'}")
    except Exception as e:
        logger.error(f"Vision AI tool test error: {str(e)}")
        test_results["vision_ai_tool"] = False
    
    # Test Gemini
    try:
        gemini_result = await tools["gemini_tool"].test_connection()
        test_results["gemini_tool"] = gemini_result
        logger.info(f"Gemini tool test: {'PASSED' if gemini_result else 'FAILED'}")
    except Exception as e:
        logger.error(f"Gemini tool test error: {str(e)}")
        test_results["gemini_tool"] = False
    
    # Test Session Storage (always works since it's in-memory)
    try:
        session_id = await tools["session_storage_tool"].create_session("test_patient")
        session_data = await tools["session_storage_tool"].get_session(session_id)
        test_results["session_storage_tool"] = session_data is not None
        logger.info(f"Session storage tool test: {'PASSED' if test_results['session_storage_tool'] else 'FAILED'}")
    except Exception as e:
        logger.error(f"Session storage tool test error: {str(e)}")
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
    "GeminiRecipeGenerator",
    "SessionStorageManager",
    "initialize_tools",
    "test_all_tools",
    "get_tool_status"
]