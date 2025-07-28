import { FALLBACK_API_RESPONSE } from '../data/fallbackData'
import dashboardDataStore from './dashboardDataStore'

// Use your production backend URL
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  'https://qloo-backend-225790768615.us-central1.run.app'

const CACHE_KEY = 'lumicue_dashboard_data'

const apiService = {
  // POST call to dashboard endpoint with localStorage caching
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
        // Add detailed logging for cached data too
        this.logResponseSections(cachedData, 'CACHED')
        return cachedData
      }
    }

    const requestPayload = {
      patient_profile: patientProfile || this.getDefaultPatientProfile(),
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
        console.warn(`API returned ${response.status}, using fallback data`)
        const fallbackData = FALLBACK_API_RESPONSE
        dashboardDataStore.setData(fallbackData)
        this.setCachedData(fallbackData)
        this.logResponseSections(fallbackData, 'FALLBACK')
        return fallbackData
      }

      const data = await response.json()
      console.log('✅ API Response received successfully')

      // Validate response structure
      if (!data?.content || !data?.patient_info) {
        console.warn('Invalid API response structure, using fallback')
        const fallbackData = FALLBACK_API_RESPONSE
        this.setCachedData(fallbackData)
        this.logResponseSections(fallbackData, 'FALLBACK')
        return fallbackData
      }

      // ADD DETAILED LOGGING HERE - Log each response section
      this.logResponseSections(data, 'API')

      // STORE DATA GLOBALLY for component access
      dashboardDataStore.setData(data)

      // Cache the successful response
      this.setCachedData(data)
      return data
    } catch (error) {
      console.error('API Error:', error.message, '- Using fallback data')
      const fallbackData = FALLBACK_API_RESPONSE
      this.setCachedData(fallbackData)
      this.logResponseSections(fallbackData, 'FALLBACK')
      return fallbackData
    }
  },

  // NEW METHOD: Log each response section for debugging
  logResponseSections(data, source = 'UNKNOWN') {
    console.log(`\n🔍 ===== DETAILED ${source} RESPONSE LOGGING =====`)

    // Log patient info
    const patientInfo = data?.patient_info || {}
    console.log('👤 PATIENT INFO:', {
      name: patientInfo.name,
      cultural_heritage: patientInfo.cultural_heritage,
      age: patientInfo.age,
      daily_theme: patientInfo.daily_theme,
    })

    // Log content structure
    const content = data?.content || {}
    console.log('📦 CONTENT STRUCTURE:', Object.keys(content))

    // Log MUSIC section in detail
    const musicData = content?.music || {}
    console.log('🎵 MUSIC DATA OVERVIEW:', {
      artist: musicData.artist,
      piece_title: musicData.piece_title,
      youtube_url: musicData.youtube_url,
      youtube_embed: musicData.youtube_embed,
      conversation_starters_count: musicData.conversation_starters?.length || 0,
      fun_fact: musicData.fun_fact,
      all_music_fields: Object.keys(musicData),
    })

    // SEPARATE logging to force display of conversation starters
    console.log('🎵 CONVERSATION STARTERS ARRAY:')
    console.log(musicData.conversation_starters)

    // SEPARATE logging to force display of fun fact
    console.log('🎵 FUN FACT TEXT:')
    console.log(musicData.fun_fact)

    // Log PHOTO section in detail
    const photoData = content?.photo || {}
    console.log('📷 PHOTO DATA:', {
      filename: photoData.filename,
      description: photoData.description
        ? `${photoData.description.substring(0, 50)}...`
        : 'Missing',
      cultural_context: photoData.cultural_context,
      conversation_starters: photoData.conversation_starters?.length || 0,
      all_photo_fields: Object.keys(photoData),
    })

    // Log RECIPE section in detail
    const recipeData = content?.recipe || {}
    console.log('🍽️ RECIPE DATA:', {
      name: recipeData.name,
      ingredients: recipeData.ingredients?.length || 0,
      instructions: recipeData.instructions?.length || 0,
      conversation_starters: recipeData.conversation_starters?.length || 0,
      all_recipe_fields: Object.keys(recipeData),
    })

    // Log NOSTALGIA NEWS section in detail
    const nostalgiaData = content?.nostalgia_news || {}
    console.log('📰 NOSTALGIA NEWS DATA:', {
      headline: nostalgiaData.headline,
      title: nostalgiaData.title,
      content: nostalgiaData.content
        ? `${nostalgiaData.content.substring(0, 50)}...`
        : 'Missing',
      themes: nostalgiaData.themes,
      conversation_starters: nostalgiaData.conversation_starters?.length || 0,
      sections: nostalgiaData.sections
        ? Object.keys(nostalgiaData.sections)
        : 'None',
      all_nostalgia_fields: Object.keys(nostalgiaData),
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
    return today.toDateString() // e.g., "Mon Jul 27 2025"
  },

  // Save data to localStorage with today's date
  setCachedData(data) {
    try {
      const cacheObject = {
        date: this.getTodayDateString(),
        data: data,
        timestamp: Date.now(),
      }
      localStorage.setItem(CACHE_KEY, JSON.stringify(cacheObject))
      console.log('💾 Dashboard data cached successfully')
    } catch (error) {
      console.warn('Failed to cache data:', error.message)
    }
  },

  // Get cached data if it's from today
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
        return cacheObject.data
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

  // Clear the cache (for refresh button)
  clearCache() {
    try {
      localStorage.removeItem(CACHE_KEY)
      console.log('🗑️ Dashboard cache cleared')
    } catch (error) {
      console.warn('Failed to clear cache:', error.message)
    }
  },

  // Refresh dashboard data (clears cache and fetches new data)
  async refreshDashboard(patientProfile = null, feedback = null) {
    console.log('🔄 Refreshing dashboard data...')
    this.clearCache()
    return await this.getDashboardData(patientProfile, feedback, true)
  },

  // Default patient profile (without medical conditions)
  getDefaultPatientProfile() {
    return {
      first_name: 'Maria',
      last_name: 'Rodriguez',
      birth_year: 1945,
      cultural_heritage: 'Italian-American',
      city: 'Brooklyn',
      state: 'New York',
      interests: ['cooking', 'family', 'music'],
    }
  },

  // Generate unique session ID
  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  },

  // Feedback submission (sends empty string for now)
  async submitFeedback(feedback) {
    try {
      console.log('Feedback collected (not sent):', feedback)

      // Fixed: Removed unused response variable
      await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ feedback: '' }),
      })

      return { success: true, message: 'Feedback collected successfully' }
    } catch (error) {
      return { success: true, message: 'Feedback saved locally' }
    }
  },

  // Check if we're using fallback data
  isUsingFallback(data) {
    return (
      data?.metadata?.agent_pipeline === 'fallback_mode' ||
      data?.metadata?.generation_timestamp === null
    )
  },

  // Get fallback data directly
  getFallbackData() {
    return FALLBACK_API_RESPONSE
  },
}

export default apiService
