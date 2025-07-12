import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    PORT = int(os.getenv("PORT", 8080))
    QLOO_API_KEY = os.getenv("QLOO_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

config = Config()

# Initialize FastAPI app
app = FastAPI(
    title="CareConnect Cultural Intelligence API",
    description="FastAPI backend - debug version",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class DailyDashboardRequest(BaseModel):
    patient_id: str
    caregiver_id: str
    preferences: Optional[Dict[str, Any]] = None

# Basic endpoints that definitely work
@app.get("/")
async def root():
    return {
        "message": "CareConnect API is running",
        "status": "healthy",
        "version": "1.0.0",
        "debug": "simplified_version",
        "api_keys_configured": {
            "qloo": bool(config.QLOO_API_KEY),
            "youtube": bool(config.YOUTUBE_API_KEY)
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-07-11"}

@app.get("/api/v1/config-check")
async def config_check():
    """Simple config check without external API calls"""
    return {
        "status": "success",
        "message": "Configuration check complete",
        "environment": {
            "port": config.PORT,
            "qloo_key_present": bool(config.QLOO_API_KEY),
            "qloo_key_length": len(config.QLOO_API_KEY) if config.QLOO_API_KEY else 0,
            "youtube_key_present": bool(config.YOUTUBE_API_KEY),
            "youtube_key_length": len(config.YOUTUBE_API_KEY) if config.YOUTUBE_API_KEY else 0
        }
    }

@app.get("/api/v1/test-simple")
async def test_simple():
    """Simple test endpoint that returns immediately"""
    logger.info("Simple test endpoint called")
    return {
        "status": "success", 
        "message": "Simple test passed",
        "timestamp": "2025-07-11"
    }

# Test individual APIs one by one
@app.get("/api/v1/test-musicbrainz")
async def test_musicbrainz_only():
    """Test only MusicBrainz API"""
    try:
        import httpx
        logger.info("Testing MusicBrainz API...")
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            headers = {"User-Agent": "CareConnect/1.0 (test@example.com)"}
            
            response = await client.get(
                "https://musicbrainz.org/ws/2/artist",
                headers=headers,
                params={
                    "query": "Frank Sinatra",
                    "fmt": "json", 
                    "limit": 1
                }
            )
            
            logger.info(f"MusicBrainz response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success",
                    "message": "MusicBrainz API working",
                    "sample_artist": data.get("artists", [{}])[0].get("name", "No artist found")
                }
            else:
                return {"status": "error", "message": f"Status code: {response.status_code}"}
                
    except Exception as e:
        logger.error(f"MusicBrainz test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/v1/test-qloo-insights")
async def test_qloo_insights():
    """Test Qloo cultural intelligence endpoint"""
    if not config.QLOO_API_KEY:
        return {"status": "no_key", "message": "Qloo API key not configured"}
    
    try:
        import httpx
        logger.info("Testing Qloo v2/insights API...")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {
                "X-API-Key": config.QLOO_API_KEY,
                "Content-Type": "application/json"
            }
            
            # Test the main cultural intelligence endpoint from your implementation
            params = {
                "filter.type": "urn:entity:artist",
                "signal.demographics.age": "55_and_older", 
                "filter.release_year.min": "1940",
                "filter.release_year.max": "1960",
                "filter.popularity.min": "0.4",
                "take": "3"
            }
            
            response = await client.get(
                "https://hackathon.api.qloo.com/v2/insights",
                headers=headers,
                params=params
            )
            
            logger.info(f"Qloo insights response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Qloo response data type: {type(data)}")
                logger.info(f"Qloo response keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")
                
                # Handle Qloo's actual response format: {"success": true, "results": {"entities": [...]}}
                if isinstance(data, dict) and data.get("success"):
                    results_obj = data.get("results", {})
                    entities = results_obj.get("entities", []) if isinstance(results_obj, dict) else []
                    
                    if isinstance(entities, list):
                        # Safely slice the entities
                        limited_entities = entities[:3] if len(entities) > 3 else entities
                        
                        sample_artists = []
                        for entity in limited_entities:
                            if isinstance(entity, dict):
                                sample_artists.append({
                                    "name": entity.get("name", "Unknown"),
                                    "entity_id": entity.get("entity_id", "Unknown"),
                                    "type": entity.get("subtype", entity.get("type", "Unknown")),
                                    "properties": entity.get("properties", {})
                                })
                        
                        return {
                            "status": "success",
                            "message": "Qloo cultural intelligence working perfectly!",
                            "total_entities": len(entities),
                            "sample_artists": sample_artists
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Entities is not a list",
                            "entities_type": str(type(entities)),
                            "raw_results": str(results_obj)[:500]
                        }
                else:
                    return {
                        "status": "error",
                        "message": "Qloo response missing 'success' field or success=false",
                        "raw_data": str(data)[:500]
                    }
            else:
                # Safely handle response text
                response_text = ""
                try:
                    response_text = response.text
                    if len(response_text) > 500:
                        response_text = response_text[:500] + "..."
                except:
                    response_text = "Could not read response text"
                
                return {
                    "status": "error", 
                    "message": f"Status code: {response.status_code}",
                    "response": response_text
                }
                
    except Exception as e:
        logger.error(f"Qloo insights test failed: {str(e)}")
        return {"status": "error", "message": str(e), "error_type": type(e).__name__}

@app.get("/api/v1/test-qloo")
async def test_qloo_only():
    """Test only Qloo API"""
    if not config.QLOO_API_KEY:
        return {"status": "no_key", "message": "Qloo API key not configured"}
    
    try:
        import httpx
        logger.info("Testing Qloo API...")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # CORRECT header format from your implementation
            headers = {
                "X-API-Key": config.QLOO_API_KEY,
                "Content-Type": "application/json"
            }
            
            # CORRECT base URL from your implementation
            # Test with a simple search endpoint
            response = await client.get(
                "https://hackathon.api.qloo.com/search",
                headers=headers,
                params={"query": "Italian music", "limit": 1}
            )
            
            logger.info(f"Qloo response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "success", 
                    "message": "Qloo API key working perfectly!",
                    "sample_result": data.get("results", [{}])[0] if data.get("results") else "No results"
                }
            elif response.status_code == 401:
                return {"status": "error", "message": "Qloo API key invalid"}
            elif response.status_code == 403:
                return {"status": "error", "message": "Qloo API key forbidden - check permissions"}
            else:
                return {"status": "error", "message": f"Status code: {response.status_code}", "response": response.text}
                
    except Exception as e:
        logger.error(f"Qloo test failed: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/v1/daily-dashboard")
async def get_daily_dashboard(request: DailyDashboardRequest):
    """Daily dashboard with real Qloo cultural intelligence"""
    logger.info(f"Generating dashboard for patient {request.patient_id}")
    
    # Extract patient preferences
    preferences = request.preferences or {}
    birth_year = preferences.get("birth_year", 1945)
    cultural_bg = preferences.get("cultural_background", "Italian-American")
    location = preferences.get("location", "Brooklyn")
    
    # Get real music recommendations if Qloo key is available
    music_recommendations = []
    api_status = "mock_mode"
    
    if config.QLOO_API_KEY:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10.0) as client:
                headers = {
                    "X-API-Key": config.QLOO_API_KEY,
                    "Content-Type": "application/json"
                }
                
                # Cultural music discovery based on era and demographics
                params = {
                    "filter.type": "urn:entity:artist",
                    "signal.demographics.age": "55_and_older",
                    "signal.location.query": location,
                    "filter.release_year.min": str(birth_year - 5),
                    "filter.release_year.max": str(birth_year + 20),
                    "filter.popularity.min": "0.3",
                    "take": "3"
                }
                
                response = await client.get(
                    "https://hackathon.api.qloo.com/v2/insights",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    music_recommendations = [
                        {
                            "title": f"Popular song by {result.get('name', 'Unknown Artist')}",
                            "artist": result.get("name", "Unknown Artist"),
                            "source": "qloo_cultural_intelligence",
                            "cultural_score": result.get("score", 0.8),
                            "era": f"{birth_year}s"
                        }
                        for result in data.get("results", [])[:3]
                    ]
                    api_status = "qloo_active"
                else:
                    api_status = f"qloo_error_{response.status_code}"
                    
        except Exception as e:
            logger.error(f"Qloo API error: {str(e)}")
            api_status = f"qloo_exception"
    
    # Fallback to mock data if Qloo unavailable
    if not music_recommendations:
        music_recommendations = [
            {"title": "Blue Moon", "artist": "Frank Sinatra", "source": "fallback", "era": f"{birth_year}s"},
            {"title": "That's Amore", "artist": "Dean Martin", "source": "fallback", "era": f"{birth_year}s"}
        ]
    
    return {
        "request_type": "DAILY_DASHBOARD",
        "patient_id": request.patient_id,
        "caregiver_id": request.caregiver_id,
        "patient_profile": {
            "birth_year": birth_year,
            "cultural_background": cultural_bg,
            "location": location
        },
        "daily_suggestions": {
            "music": music_recommendations,
            "conversation": f"Tell me about your favorite memory from the {birth_year}s in {location}",
            "recipe": {
                "name": f"Classic {cultural_bg.split('-')[0]} Comfort Food", 
                "difficulty": "easy",
                "cultural_context": f"Traditional {cultural_bg} family recipe"
            }
        },
        "cultural_context": f"Recommendations based on {cultural_bg} heritage, {birth_year} era, and {location} cultural influences",
        "api_status": api_status,
        "mode": "real_qloo_integration" if config.QLOO_API_KEY else "development_mode"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=config.PORT, 
        reload=True
    )