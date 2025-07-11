#!/usr/bin/env python3
"""
CareConnect - Python API Integration Test
Tests all required APIs for the dementia care assistant
"""

import os
import json
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys from .env
API_KEYS = {
    'QLOO': os.getenv('QLOO_API_KEY'),
    'GOOGLE_CLOUD': os.getenv('GOOGLE_CLOUD_API_KEY'),  # Vision AI
    'YOUTUBE': os.getenv('YOUTUBE_API_KEY'),             # YouTube (same as GOOGLE_CLOUD)
}

# Logging setup
LOG_FILE = f"careconnect_api_test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
log_data = []

def log(message):
    """Log message to console and file"""
    print(message)
    log_data.append(message)

def save_log():
    """Save all logs to file"""
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(log_data))
        print(f"\n📄 Complete test results saved to: {LOG_FILE}")
    except Exception as e:
        print(f"❌ Failed to save log: {e}")

def test_qloo_api():
    """Test Qloo Cultural Intelligence API"""
    log('🎯 Testing Qloo API - Cultural Intelligence')
    
    url = 'https://hackathon.api.qloo.com/v2/insights'
    params = {
        'filter.type': 'urn:entity:place',
        'signal.demographics.age': '55_and_older',
        'signal.location.query': 'Brooklyn',
        'take': 3
    }
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEYS['QLOO']
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            log('✅ Qloo API: WORKING - Cultural intelligence confirmed')
            log(f"   📊 Found {len(data.get('results', []))} Brooklyn restaurants for seniors")
            
            # Show sample result
            if data.get('results'):
                first_result = data['results'][0]
                log(f"   🍽️ Sample: \"{first_result.get('name', 'Unnamed')}\"")
            
            log('')
            return True  # Return immediately on success
                
        else:
            log(f"❌ Qloo API: FAILED - Status {response.status_code}")
            log(f"   💡 Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        log(f"💥 Qloo API: ERROR - {str(e)}")
        log('')
        return False  # Add this line to fix the success reporting

def test_vision_api():
    """Test Google Vision AI for photo analysis"""
    log('👁️ Testing Vision AI - Photo Analysis')
    
    # Small test image (1x1 pixel PNG in base64)
    test_image_base64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    
    url = f'https://vision.googleapis.com/v1/images:annotate?key={API_KEYS["GOOGLE_CLOUD"]}'
    
    payload = {
        'requests': [{
            'image': {'content': test_image_base64},
            'features': [
                {'type': 'LABEL_DETECTION', 'maxResults': 5},
                {'type': 'SAFE_SEARCH_DETECTION'}
            ]
        }]
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            log('✅ Vision AI: WORKING - Photo analysis confirmed')
            log('   📷 API responding to image analysis requests')
            
            if data.get('responses') and data['responses'][0].get('labelAnnotations'):
                labels = len(data['responses'][0]['labelAnnotations'])
                log(f'   🏷️ Labels detected: {labels}')
            
        else:
            log(f"❌ Vision AI: FAILED - Status {response.status_code}")
            log(f"   💡 Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        log(f"💥 Vision AI: ERROR - {str(e)}")
        return False
    
    log('')
    return True

def test_youtube_api():
    """Test YouTube Data API for nostalgic content discovery"""
    log('📺 Testing YouTube API - Nostalgic Content Discovery')
    
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': 'Ed Sullivan Show 1960s classic',
        'type': 'video',
        'maxResults': 3,
        'order': 'relevance',
        'key': API_KEYS['YOUTUBE']
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            log('✅ YouTube API: WORKING - Nostalgic content discovery confirmed')
            
            items = data.get('items', [])
            log(f"   📺 Found {len(items)} videos for 'Ed Sullivan Show 1960s classic'")
            
            for i, video in enumerate(items[:2], 1):
                snippet = video.get('snippet', {})
                title = snippet.get('title', 'No title')[:50]
                published = snippet.get('publishedAt', '')[:4]  # Year only
                video_id = video.get('id', {}).get('videoId', '')
                
                log(f"   🎬 Video {i}: \"{title}...\"")
                log(f"      📅 Published: {published}")
                log(f"      🔗 Video ID: {video_id}")
            
        else:
            log(f"❌ YouTube API: FAILED - Status {response.status_code}")
            log(f"   💡 Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        log(f"💥 YouTube API: ERROR - {str(e)}")
        return False
    
    log('')
    return True

def test_musicbrainz_api():
    """Test MusicBrainz API for music artist details (free, no API key)"""
    log('🎵 Testing MusicBrainz API - Music Artist Discovery')
    
    # Search for classic 1940s artist
    artist_query = 'Glenn Miller'
    url = 'https://musicbrainz.org/ws/2/artist/'
    params = {
        'query': artist_query,
        'fmt': 'json',
        'limit': 3
    }
    headers = {
        'User-Agent': 'CareConnect/1.0 (dementia-care-app)'  # Required by MusicBrainz
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            log('✅ MusicBrainz API: WORKING - Music artist discovery confirmed')
            
            artists = data.get('artists', [])
            log(f"   🎵 Found {len(artists)} artists for '{artist_query}'")
            
            for i, artist in enumerate(artists[:2], 1):
                name = artist.get('name', 'Unknown')
                artist_type = artist.get('type', 'Unknown')
                life_span = artist.get('life-span', {})
                begin = life_span.get('begin', 'Unknown')
                end = life_span.get('end', 'Present')
                area = artist.get('area', {}).get('name', 'Unknown')
                
                log(f"   🎼 Artist {i}: \"{name}\"")
                log(f"      🏷️ Type: {artist_type}")
                log(f"      📅 Life span: {begin} - {end}")
                log(f"      🌍 Area: {area}")
                
                # Show genres if available
                if artist.get('tags'):
                    genres = [tag['name'] for tag in artist['tags'][:3]]
                    log(f"      🎭 Genres: {', '.join(genres)}")
            
            # Test detailed lookup for first artist
            if artists:
                first_artist = artists[0]
                artist_id = first_artist.get('id')
                log(f"   🔍 Testing detailed lookup for: {first_artist.get('name')}")
                
                # Respect rate limit (1 request per second)
                time.sleep(1.1)
                
                detail_url = f'https://musicbrainz.org/ws/2/artist/{artist_id}'
                detail_params = {'fmt': 'json', 'inc': 'genres'}
                
                detail_response = requests.get(detail_url, params=detail_params, 
                                             headers=headers, timeout=15)
                
                if detail_response.status_code == 200:
                    log('   ✅ Detailed artist info retrieved successfully')
                
        else:
            log(f"❌ MusicBrainz API: FAILED - Status {response.status_code}")
            log(f"   💡 Error: {response.text[:200]}")
            return False
            
    except Exception as e:
        log(f"💥 MusicBrainz API: ERROR - {str(e)}")
        return False
    
    log('')
    return True

def main():
    """Run all API tests"""
    log('🧪 CareConnect - Python API Integration Test')
    log(f'📅 Test Date: {datetime.now().isoformat()}')
    log('🔐 API Keys: Loaded from .env')
    
    # DEBUG: Check if keys are loading properly
    log('\n🔍 DEBUG - API Key Information:')
    for name, key in API_KEYS.items():
        if key:
            log(f'🔑 {name}: {key[:10]}...{key[-6:]} (length: {len(key)})')
        else:
            log(f'❌ {name}: NOT FOUND in .env')
    
    log('=' * 80)
    
    # Validate API keys
    missing_keys = [key for key, value in API_KEYS.items() if not value]
    if missing_keys:
        log(f"❌ Missing API keys: {missing_keys}")
        log("💡 Check your .env file")
        save_log()
        return
    
    # Test all APIs
    tests = [
        ('Qloo Cultural Intelligence', test_qloo_api),
        ('Vision AI Photo Analysis', test_vision_api),
        ('YouTube Content Discovery', test_youtube_api),
        ('MusicBrainz Music Discovery', test_musicbrainz_api),
    ]
    
    successful_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                successful_tests += 1
        except Exception as e:
            log(f"💥 {test_name}: CRITICAL ERROR - {str(e)}")
    
    # Results summary
    log('🎉 API Testing Complete!')
    log(f'📊 Results: {successful_tests}/{total_tests} APIs working')
    log('=' * 80)
    
    if successful_tests == total_tests:
        log('🚀 PERFECT: All APIs working!')
        log('')
        log('🏆 CareConnect ready for enterprise-grade implementation:')
        log('   ✅ Cultural Intelligence (Qloo)')
        log('   ✅ Photo Analysis (Vision AI)')
        log('   ✅ Content Discovery (YouTube)')
        log('   ✅ Music Discovery (MusicBrainz)')
        log('')
        log('🎯 Complete API stack confirmed - ready to build!')
        
    elif successful_tests >= 3:
        log('⚠️ GOOD: Core features working, some APIs need attention')
        log('🔧 Proceed with working APIs and debug others')
        
    else:
        log('❌ CRITICAL: Multiple API issues')
        log('🔧 Check API keys and enabled services in Google Cloud Console')
    
    log('')
    log('📋 Next Steps:')
    log('   1. Fix any failing APIs')
    log('   2. Start FastAPI backend development')
    log('   3. Implement sophisticated API integration pipeline')
    
    # Save results
    save_log()

if __name__ == '__main__':
    main()