"""
Comprehensive Test Script for Simplified CareConnect Implementation
File: backend/test_simplified_implementation.py

Tests the complete simplified pipeline from cultural mappings through agent execution.
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(backend_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, parent_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

async def test_cultural_mappings():
    """Test the cultural heritage mapping system."""
    
    logger.info("🧪 Testing Cultural Heritage Mappings")
    
    try:
        from config.cultural_mappings import (
            get_heritage_tags, 
            get_interest_tags, 
            get_age_demographic,
            validate_heritage_coverage
        )
        
        # Test heritage mapping
        heritage = "Italian-American"
        tags = get_heritage_tags(heritage)
        logger.info(f"✅ Heritage '{heritage}' mapped to: {tags}")
        
        # Test interest mapping
        interests = ["loves music", "cooking", "family activities"]
        interest_tags = get_interest_tags(interests)
        logger.info(f"✅ Interests {interests} mapped to: {interest_tags}")
        
        # Test age demographic
        age_demo = get_age_demographic(1945)
        logger.info(f"✅ Birth year 1945 → Age demographic: {age_demo}")
        
        # Test validation
        validation = validate_heritage_coverage()
        logger.info(f"✅ Heritage coverage validation: {validation['total_heritages']} heritages, {len(validation['valid_heritages'])} valid")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Cultural mappings test failed: {e}")
        return False

async def test_qloo_tools():
    """Test the simplified Qloo tools."""
    
    logger.info("🧪 Testing Simplified Qloo Tools")
    
    try:
        from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
        from config.cultural_mappings import get_heritage_tags, get_age_demographic
        
        api_key = os.getenv("QLOO_API_KEY")
        if not api_key:
            logger.warning("⚠️  No QLOO_API_KEY found, skipping Qloo tests")
            return True
        
        # Initialize tool
        qloo = QlooInsightsAPI(api_key)
        
        # Test connection
        connected = await qloo.test_connection()
        if not connected:
            logger.error("❌ Qloo connection test failed")
            return False
        
        logger.info("✅ Qloo connection successful")
        
        # Test cultural calls
        heritage_tags = get_heritage_tags("Italian-American")
        age_demo = get_age_demographic(1945)
        
        results = await qloo.make_three_cultural_calls(heritage_tags, age_demo)
        
        logger.info(f"✅ Qloo cultural calls: {results['successful_calls']}/3 successful")
        logger.info(f"   Total results: {results['total_results']}")
        
        # Show sample results
        for category, data in results["cultural_recommendations"].items():
            if data.get("available"):
                entity_count = data.get("entity_count", 0)
                logger.info(f"   {category.title()}: {entity_count} entities")
        
        return results["successful_calls"] > 0
        
    except Exception as e:
        logger.error(f"❌ Qloo tools test failed: {e}")
        return False

async def test_individual_agents():
    """Test individual agents in isolation."""
    
    logger.info("🧪 Testing Individual Agents")
    
    # Test data matching curl example
    test_patient_profile = {
        "cultural_heritage": "Italian-American",
        "birth_year": 1945,
        "city": "Brooklyn",
        "state": "New York", 
        "additional_context": "Loves music and cooking"
    }
    
    success_count = 0
    
    # Test Agent 1
    try:
        from multi_tool_agent.agents.information_consolidator_agent import InformationConsolidatorAgent
        
        agent1 = InformationConsolidatorAgent()
        result1 = await agent1.run(
            patient_profile=test_patient_profile,
            request_type="dashboard"
        )
        
        consolidated = result1.get("consolidated_info", {})
        patient = consolidated.get("patient_profile", {})
        
        logger.info(f"✅ Agent 1: Heritage={patient.get('cultural_heritage')}, Age={patient.get('age')}")
        success_count += 1
        
    except Exception as e:
        logger.error(f"❌ Agent 1 test failed: {e}")
    
    # Test Agent 2
    try:
        from multi_tool_agent.agents.cultural_profile_agent import CulturalProfileBuilderAgent
        
        agent2 = CulturalProfileBuilderAgent()
        result2 = await agent2.run(consolidated_info=consolidated)
        
        profile = result2.get("cultural_profile", {})
        elements = profile.get("cultural_elements", {})
        mappings = profile.get("qloo_tag_mappings", {})
        
        logger.info(f"✅ Agent 2: Heritage={elements.get('heritage')}, Tags={len(mappings)}")
        success_count += 1
        
    except Exception as e:
        logger.error(f"❌ Agent 2 test failed: {e}")
    
    # Test Agent 3 (if Qloo available)
    try:
        api_key = os.getenv("QLOO_API_KEY")
        if api_key:
            from multi_tool_agent.agents.qloo_cultural_intelligence_agent import QlooCulturalIntelligenceAgent
            from multi_tool_agent.tools.qloo_tools import QlooInsightsAPI
            
            qloo_tool = QlooInsightsAPI(api_key)
            agent3 = QlooCulturalIntelligenceAgent(qloo_tool)
            
            result3 = await agent3.run(
                consolidated_info=consolidated,
                cultural_profile=profile
            )
            
            qloo_intel = result3.get("qloo_intelligence", {})
            metadata = qloo_intel.get("metadata", {})
            
            logger.info(f"✅ Agent 3: Calls={metadata.get('successful_calls')}/3, Results={metadata.get('total_results')}")
            success_count += 1
        else:
            logger.warning("⚠️  Agent 3 skipped: No QLOO_API_KEY")
            
    except Exception as e:
        logger.error(f"❌ Agent 3 test failed: {e}")
    
    logger.info(f"Individual agents test: {success_count}/3 successful")
    return success_count >= 2  # At least Agent 1 and 2 should work

async def test_full_pipeline():
    """Test the complete agent pipeline."""
    
    logger.info("🧪 Testing Complete Agent Pipeline")
    
    try:
        from multi_tool_agent.sequential_agent import SequentialAgentCoordinator
        
        # Initialize coordinator (without tools for basic test)
        coordinator = SequentialAgentCoordinator()
        
        # Test data
        test_patient_profile = {
            "cultural_heritage": "Italian-American",
            "birth_year": 1945,
            "city": "Brooklyn",
            "state": "New York",
            "additional_context": "Loves music and cooking"
        }
        
        # Execute pipeline
        result = await coordinator.execute_pipeline(
            patient_profile=test_patient_profile,
            request_type="dashboard"
        )
        
        # Analyze results
        metadata = result.get("pipeline_metadata", {})
        pipeline_success = metadata.get("pipeline_success", False)
        agents_executed = metadata.get("agents_executed", 0)
        
        logger.info(f"✅ Pipeline: Success={pipeline_success}, Agents={agents_executed}")
        
        # Check cultural profile results
        cultural_profile = result.get("pipeline_results", {}).get("cultural_profile", {})
        if cultural_profile:
            elements = cultural_profile.get("cultural_elements", {})
            mappings = cultural_profile.get("qloo_tag_mappings", {})
            logger.info(f"   Cultural Profile: Heritage={elements.get('heritage')}, Tags={mappings}")
        
        return pipeline_success and agents_executed >= 2
        
    except Exception as e:
        logger.error(f"❌ Full pipeline test failed: {e}")
        return False

async def test_curl_format():
    """Test the curl input format processing."""
    
    logger.info("🧪 Testing Curl Input Format")
    
    try:
        # Simulate the exact curl input from the plan
        curl_input = {
            "patient_profile": {
                "cultural_heritage": "Italian-American",
                "birth_year": 1945,
                "city": "Brooklyn",
                "state": "New York",
                "additional_context": "Loves music and cooking"
            },
            "request_type": "dashboard"
        }
        
        # Test input processing
        patient_profile = curl_input.get("patient_profile", {})
        heritage = patient_profile.get("cultural_heritage")
        birth_year = patient_profile.get("birth_year")
        age = 2024 - birth_year if birth_year else None
        location = f"{patient_profile.get('city')}, {patient_profile.get('state')}"
        
        logger.info(f"✅ Curl format parsing:")
        logger.info(f"   Heritage: {heritage}")
        logger.info(f"   Age: {age} (from birth year {birth_year})")
        logger.info(f"   Location: {location}")
        logger.info(f"   Context: {patient_profile.get('additional_context')}")
        
        # Test expected mappings
        from config.cultural_mappings import get_heritage_tags, get_age_demographic
        
        heritage_tags = get_heritage_tags(heritage)
        age_demo = get_age_demographic(birth_year)
        
        logger.info(f"   Expected tags: {heritage_tags}")
        logger.info(f"   Age demographic: {age_demo}")
        
        # Simulate expected Qloo calls
        expected_calls = [
            f"filter.type=urn:entity:place, filter.tags={heritage_tags.get('cuisine')}, age={age_demo}",
            f"filter.type=urn:entity:artist, filter.tags={heritage_tags.get('music')}, age={age_demo}",
            f"filter.type=urn:entity:movie, filter.tags={heritage_tags.get('movies')}, age={age_demo}"
        ]
        
        logger.info("   Expected Qloo calls:")
        for i, call in enumerate(expected_calls, 1):
            logger.info(f"     {i}. {call}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Curl format test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests and provide summary."""
    
    logger.info("🚀 Starting Comprehensive Test Suite for Simplified CareConnect")
    logger.info("=" * 80)
    
    test_results = {}
    
    # Run all tests
    test_results["cultural_mappings"] = await test_cultural_mappings()
    logger.info("-" * 40)
    
    test_results["qloo_tools"] = await test_qloo_tools()
    logger.info("-" * 40)
    
    test_results["individual_agents"] = await test_individual_agents()
    logger.info("-" * 40)
    
    test_results["full_pipeline"] = await test_full_pipeline()
    logger.info("-" * 40)
    
    test_results["curl_format"] = await test_curl_format()
    logger.info("=" * 80)
    
    # Generate summary
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    logger.info(f"🎯 TEST SUMMARY: {passed_tests}/{total_tests} tests passed")
    
    for test_name, passed in test_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        logger.info(f"   {test_name}: {status}")
    
    if passed_tests == total_tests:
        logger.info("🎉 ALL TESTS PASSED! Simplified implementation is working correctly.")
        logger.info("Ready to test with actual curl commands:")
        logger.info("""
curl -X POST http://localhost:8000/api/v1/test-curl \\
  -H "Content-Type: application/json" \\
  -d '{
    "patient_profile": {
      "cultural_heritage": "Italian-American",
      "birth_year": 1945,
      "city": "Brooklyn",
      "state": "New York",
      "additional_context": "Loves music and cooking"
    },
    "request_type": "dashboard"
  }'
        """)
    else:
        logger.warning(f"⚠️  {total_tests - passed_tests} tests failed. Check implementation.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    success = asyncio.run(run_all_tests())
    
    # Exit with appropriate code
    exit(0 if success else 1)