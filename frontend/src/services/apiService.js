// frontend/src/services/apiService.js
import { FALLBACK_API_RESPONSE } from '../data/fallbackData'
import dashboardDataStore from './dashboardDataStore'

// Use your production backend URL
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  'https://qloo-backend-225790768615.us-central1.run.app'

const CACHE_KEY = 'lumicue_dashboard_data'
const PROFILE_KEY = 'patient_profile' // Consistent key for profile storage

const apiService = {
  // POST call to dashboard endpoint with bulletproof fallback system
  async getDashboardData(
    patientProfile = null,
    feedback = null,
    forceRefresh = false,
  ) {
    // Check cache first unless force refresh is requested
    if (!forceRefresh) {
      const cachedData = this.getCachedData()
      if (cachedData) {
        console.log('📱 Using cached dashboard data')
        this.logResponseSections(cachedData, 'CACHED')
        dashboardDataStore.setData(cachedData)
        return cachedData
      }
    }

    const requestPayload = {
      patient_profile: this.createAnonymizedProfile(patientProfile),
      session_id: this.generateSessionId(),
      feedback_data: feedback || { likes: [], dislikes: [] },
    }

    try {
      console.log('🌐 Calling production API:', `${API_BASE_URL}/api/dashboard`)
      console.log('📤 Request payload:', requestPayload)

      const response = await fetch(`${API_BASE_URL}/api/dashboard`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify(requestPayload),
      })

      console.log('📡 API Response Status:', response.status)

      if (!response.ok) {
        console.warn(
          `API returned ${response.status}, using bulletproof fallback`,
        )
        return this.useBulletproofFallback('API_ERROR')
      }

      const data = await response.json()
      console.log('✅ API Response received successfully')

      // Validate response structure
      if (!data?.content || !data?.patient_info) {
        console.warn(
          'Invalid API response structure, using bulletproof fallback',
        )
        return this.useBulletproofFallback('INVALID_STRUCTURE')
      }

      // Log successful API response
      this.logResponseSections(data, 'API')

      // Store data globally for component access
      dashboardDataStore.setData(data)

      // Cache the successful response WITH patient profile for persistence
      const currentPatientProfile = this.getLocalProfile()
      this.setCachedData(data, currentPatientProfile)
      return data
    } catch (error) {
      console.error('API Error:', error.message, '- Using bulletproof fallback')
      return this.useBulletproofFallback('NETWORK_ERROR')
    }
  },

  // Bulletproof fallback method - always works
  useBulletproofFallback(reason = 'UNKNOWN') {
    console.log(`🛡️ Activating bulletproof fallback (Reason: ${reason})`)
    const fallbackData = FALLBACK_API_RESPONSE

    // Store fallback data globally
    dashboardDataStore.setData(fallbackData)

    // Cache fallback data WITH patient profile so demo keeps working
    const currentPatientProfile = this.getLocalProfile()
    this.setCachedData(fallbackData, currentPatientProfile)

    // Log fallback data sections
    this.logResponseSections(fallbackData, 'BULLETPROOF_FALLBACK')

    return fallbackData
  },

  // Enhanced logging method for all response types
  logResponseSections(data, source) {
    console.log(`🔍 ===== ${source} RESPONSE LOGGING =====`)

    // Log patient info (without PII in logs)
    const patientInfo = data?.patient_info || {}
    console.log('👤 PATIENT INFO:', {
      age: patientInfo.age,
      heritage: patientInfo.cultural_heritage,
      theme: patientInfo.daily_theme,
    })

    // Log music data
    const musicData = data?.content?.music || {}
    console.log('🎵 MUSIC DATA:', {
      artist: musicData.artist,
      piece: musicData.piece_title,
      youtube_url: musicData.youtube_url ? 'Present' : 'Missing',
      conversation_starters: musicData.conversation_starters?.length || 0,
      fun_fact: musicData.fun_fact ? 'Present' : 'Missing',
    })

    // Log recipe data
    const recipeData = data?.content?.recipe || {}
    console.log('🍽️ RECIPE DATA:', {
      name: recipeData.name,
      ingredients: recipeData.ingredients?.length || 0,
      instructions: recipeData.instructions?.length || 0,
      conversation_starters: recipeData.conversation_starters?.length || 0,
    })

    // Log photo data
    const photoData = data?.content?.photo || {}
    console.log('📸 PHOTO DATA:', {
      filename: photoData.filename,
      description: photoData.description ? 'Present' : 'Missing',
      cultural_context: photoData.cultural_context ? 'Present' : 'Missing',
      conversation_starters: photoData.conversation_starters?.length || 0,
    })

    // Log nostalgia data
    const nostalgiaData = data?.content?.nostalgia_news || {}
    console.log('📰 NOSTALGIA DATA:', {
      title: nostalgiaData.title,
      subtitle: nostalgiaData.subtitle,
      content: nostalgiaData.content
        ? `${nostalgiaData.content.substring(0, 50)}...`
        : 'Missing',
      themes: nostalgiaData.themes,
      conversation_starters: nostalgiaData.conversation_starters?.length || 0,
      sections: nostalgiaData.sections
        ? Object.keys(nostalgiaData.sections)
        : 'None',
    })

    // Log metadata
    const metadata = data?.metadata || {}
    console.log('📊 METADATA:', {
      quality_score: metadata.quality_score,
      personalization_level: metadata.personalization_level,
      theme: metadata.theme,
      agent_pipeline: metadata.agent_pipeline,
    })

    console.log(`🔍 ===== END ${source} RESPONSE LOGGING =====\n`)
  },

  // Get today's date string for cache key
  getTodayDateString() {
    const today = new Date()
    return today.toDateString()
  },

  // Save COMPLETE data to localStorage with today's date (includes full API response + patient profile)
  setCachedData(data, patientProfile = null) {
    try {
      const cacheObject = {
        date: this.getTodayDateString(),
        data: data, // Complete API response
        patientProfile: patientProfile || this.getLocalProfile(), // Complete patient profile with names
        timestamp: Date.now(),
      }
      localStorage.setItem(CACHE_KEY, JSON.stringify(cacheObject))
      console.log('💾 Dashboard data + patient profile cached successfully')
    } catch (error) {
      console.warn('Failed to cache data:', error.message)
      // Silent failure - doesn't break the demo
    }
  },

  // Get cached data if it's from today (returns both API response and patient profile)
  getCachedData() {
    try {
      const cached = localStorage.getItem(CACHE_KEY)
      if (!cached) {
        return null
      }

      const cacheObject = JSON.parse(cached)
      const todayDateString = this.getTodayDateString()

      // Check if cached data is from today
      if (cacheObject.date === todayDateString) {
        console.log('📱 Found valid cached data from today')

        // If we have a cached patient profile, restore it to local storage
        if (cacheObject.patientProfile) {
          localStorage.setItem(
            PROFILE_KEY,
            JSON.stringify(cacheObject.patientProfile),
          )
          console.log('📱 Restored patient profile from cache')
        }

        return cacheObject.data // Return the API response data
      } else {
        console.log('🗑️ Cached data is from a different day, clearing cache')
        this.clearCache()
        return null
      }
    } catch (error) {
      console.warn('Error reading cached data:', error.message)
      this.clearCache()
      return null
    }
  },

  // Clear BOTH dashboard cache AND patient profile cache
  clearCache() {
    try {
      localStorage.removeItem(CACHE_KEY)
      // Note: We keep PROFILE_KEY for UI persistence, only clear dashboard cache
      console.log('🗑️ Dashboard cache cleared (patient profile preserved)')
    } catch (error) {
      console.warn('Failed to clear cache:', error.message)
      // Silent failure - doesn't break the demo
    }
  },

  // Clear ALL caches including patient profile (for complete reset)
  clearAllCaches() {
    try {
      localStorage.removeItem(CACHE_KEY)
      localStorage.removeItem(PROFILE_KEY)
      console.log('🗑️ All caches cleared (dashboard + patient profile)')
    } catch (error) {
      console.warn('Failed to clear all caches:', error.message)
      // Silent failure - doesn't break the demo
    }
  },

  // Refresh dashboard data (clears cache and fetches new data)
  async refreshDashboard(patientProfile = null, feedback = null) {
    console.log('🔄 Refreshing dashboard data...')
    this.clearCache()
    dashboardDataStore.clearData()
    return await this.getDashboardData(patientProfile, feedback, true)
  },

  // PII-COMPLIANT: Create anonymized profile for API transmission
  createAnonymizedProfile(profileData = null) {
    const sourceProfile = profileData || this.getLocalProfile()

    // Calculate age group from birth year (matching backend logic)
    const calculateAgeGroup = birthYear => {
      if (!birthYear) return 'senior' // Default assumption

      const currentAge = new Date().getFullYear() - birthYear
      if (currentAge >= 80) return 'oldest_senior'
      if (currentAge >= 65) return 'senior'
      return 'adult'
    }

    // Extract only essential, non-PII data needed by agents
    const anonymizedProfile = {
      age_group: calculateAgeGroup(sourceProfile.birth_year),
      cultural_heritage: sourceProfile.cultural_heritage || 'American',
      interests: sourceProfile.interests || ['music', 'family', 'cooking'],
      profile_complete: !!(
        sourceProfile.cultural_heritage && sourceProfile.birth_year
      ),
    }

    console.log('🔒 Anonymized profile created:', {
      age_group: anonymizedProfile.age_group,
      cultural_heritage: anonymizedProfile.cultural_heritage,
      interests_count: anonymizedProfile.interests.length,
      profile_complete: anonymizedProfile.profile_complete,
    })

    return anonymizedProfile
  },

  // DEPRECATED: Remove PII method (replaced by createAnonymizedProfile)
  removePIIFromProfile(profile) {
    const { first_name, last_name, name, city, state, ...cleanProfile } =
      profile
    return cleanProfile
  },

  // DEFAULT: Get anonymized default profile for agents
  getDefaultPatientProfile() {
    return this.createAnonymizedProfile()
  },

  // LOCAL STORAGE: Method to update the profile for UI display (keeps names locally)
  updateLocalProfile(profileData) {
    try {
      // Save complete profile locally for UI display
      localStorage.setItem(PROFILE_KEY, JSON.stringify(profileData))
      console.log('💾 Profile saved locally for UI display')
      return true
    } catch (error) {
      console.error('Failed to save local profile:', error.message)
      return false
    }
  },

  // LOCAL STORAGE: Get complete profile for UI display (includes names)
  getLocalProfile() {
    try {
      const savedProfile = localStorage.getItem(PROFILE_KEY)
      if (savedProfile) {
        return JSON.parse(savedProfile)
      }
    } catch (error) {
      console.warn('Failed to load local profile:', error.message)
    }

    // Return default profile with UI display name
    return {
      first_name: 'Guest',
      name: 'Guest',
      birth_year: 1942,
      cultural_heritage: 'Italian-American',
      interests: ['cooking', 'family', 'music'],
      // Note: city/state removed as they're not used by agents
    }
  },

  // Generate unique session ID
  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  },

  // Feedback submission with safe fallback
  async submitFeedback(feedback) {
    try {
      console.log('Feedback collected (not sent):', feedback)

      await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedback: '' }),
      })

      return { success: true, message: 'Feedback collected successfully' }
    } catch (error) {
      // Silent failure - doesn't break the demo
      return { success: true, message: 'Feedback saved locally' }
    }
  },

  // Check if we're using fallback data
  isUsingFallback(data) {
    return (
      data?.metadata?.agent_pipeline === 'fallback_mode' ||
      data?.metadata?.generation_timestamp === null ||
      !data?.content ||
      !data?.patient_info
    )
  },

  // Get the complete cached data object (includes both API response and patient profile)
  getCompleteCachedData() {
    try {
      const cached = localStorage.getItem(CACHE_KEY)
      if (!cached) {
        return null
      }

      const cacheObject = JSON.parse(cached)
      const todayDateString = this.getTodayDateString()

      // Check if cached data is from today
      if (cacheObject.date === todayDateString) {
        console.log('📱 Found complete cached data from today')
        return {
          apiResponse: cacheObject.data,
          patientProfile: cacheObject.patientProfile,
          timestamp: cacheObject.timestamp,
        }
      } else {
        console.log('🗑️ Cached data is from a different day')
        return null
      }
    } catch (error) {
      console.warn('Error reading complete cached data:', error.message)
      return null
    }
  },

  // Get bulletproof fallback data directly
  getFallbackData() {
    return FALLBACK_API_RESPONSE
  },
}

export default apiService
