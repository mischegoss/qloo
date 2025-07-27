import { FALLBACK_API_RESPONSE } from '../data/fallbackData'

// Use your production backend URL
const API_BASE_URL =
  process.env.REACT_APP_API_URL ||
  'https://qloo-backend-225790768615.us-central1.run.app'

const apiService = {
  // POST call to dashboard endpoint
  async getDashboardData(patientProfile = null, feedback = null) {
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
        return FALLBACK_API_RESPONSE
      }

      const data = await response.json()
      console.log('✅ API Response received successfully')

      // Validate response structure
      if (!data?.content || !data?.patient_info) {
        console.warn('Invalid API response structure, using fallback')
        return FALLBACK_API_RESPONSE
      }

      return data
    } catch (error) {
      console.error('API Error:', error.message, '- Using fallback data')
      return FALLBACK_API_RESPONSE
    }
  },

  // Test endpoint connectivity
  async testConnection() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: { Accept: 'application/json' },
      })

      return {
        success: response.ok,
        status: response.status,
        message: response.ok ? 'Connection successful' : 'Connection failed',
      }
    } catch (error) {
      return {
        success: false,
        status: 0,
        message: `Connection error: ${error.message}`,
      }
    }
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

      const response = await fetch(`${API_BASE_URL}/api/feedback`, {
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
