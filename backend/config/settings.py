"""
Simple Configuration Settings
File: backend/config/settings.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for CareConnect"""
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("BACKEND_HOST", "localhost")
    
    # API Keys
    QLOO_API_KEY = os.getenv("QLOO_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", os.getenv("GOOGLE_CLOUD_API_KEY"))
    GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_CLOUD_API_KEY"))
    
    # Database (if needed)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careconnect.db")
    
    @classmethod
    def validate_required_keys(cls):
        """Validate that required API keys are present"""
        required_keys = {
            "QLOO_API_KEY": cls.QLOO_API_KEY,
            "GOOGLE_CLOUD_API_KEY": cls.GOOGLE_CLOUD_API_KEY
        }
        
        missing_keys = [key for key, value in required_keys.items() if not value]
        
        if missing_keys:
            print(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
            return False
        
        print("✅ All required API keys found")
        return True
    
    @classmethod
    def get_status(cls):
        """Get configuration status"""
        return {
            "port": cls.PORT,
            "debug": cls.DEBUG,
            "api_keys_configured": {
                "qloo": bool(cls.QLOO_API_KEY),
                "youtube": bool(cls.YOUTUBE_API_KEY),
                "google_cloud": bool(cls.GOOGLE_CLOUD_API_KEY),
                "gemini": bool(cls.GEMINI_API_KEY)
            }
        }