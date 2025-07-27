import { useState, useEffect } from 'react'
import apiService from './services/apiService'
import mapApiToUIData from './utils/dataMappers'
import feedbackManager from './utils/feedbackManager'

// Import your existing components
import Dashboard from './components/Dashboard'
import MusicDetail from './components/MusicDetail'
import PhotoDetail from './components/PhotoDetail'
import RecipeDetail from './components/RecipeDetail'
import NostalgiaDetail from './components/NostalgiaDetail'
import Profile from './components/ProfileInfo'
import Demo from './components/Demo'

// Loading and Error Components
const LoadingSpinner = () => (
  <div
    className='min-h-screen flex items-center justify-center'
    style={{ backgroundColor: '#F8F7ED' }}
  >
    <div className='text-center'>
      <div className='animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto mb-4'></div>
      <p className='text-gray-600 text-lg'>
        Loading your personalized content...
      </p>
    </div>
  </div>
)

const ErrorMessage = ({ error, onRetry }) => (
  <div
    className='min-h-screen flex items-center justify-center'
    style={{ backgroundColor: '#F8F7ED' }}
  >
    <div className='text-center max-w-md'>
      <div className='text-red-500 text-6xl mb-4'>⚠️</div>
      <h2 className='text-2xl font-bold text-gray-800 mb-2'>
        Connection Issue
      </h2>
      <p className='text-gray-600 mb-6'>{error}</p>
      <button
        onClick={onRetry}
        className='px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors'
      >
        Try Again
      </button>
    </div>
  </div>
)

const App = () => {
  // State management
  const [dashboardData, setDashboardData] = useState(null)
  const [patientProfile, setPatientProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [currentView, setCurrentView] = useState('app')
  const [connectionStatus, setConnectionStatus] = useState(null)

  // Load dashboard data on mount
  useEffect(() => {
    loadDashboardData()
    testBackendConnection()
  }, [])

  // Test backend connection
  const testBackendConnection = async () => {
    const result = await apiService.testConnection()
    setConnectionStatus(result)
    console.log('Backend connection test:', result)
  }

  // Load dashboard data from API
  const loadDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Get current feedback for API call
      const currentFeedback = feedbackManager.formatForAPI()

      console.log('📡 Loading dashboard data...')

      // Make API call with feedback
      const apiResponse = await apiService.getDashboardData(
        patientProfile,
        currentFeedback,
      )

      console.log('🔄 Transforming API response to UI data...')

      // Transform API response to UI format
      const uiData = mapApiToUIData(apiResponse)
      setDashboardData(uiData)

      // Store patient profile for display
      const profileData = {
        first_name: apiResponse.patient_info?.name?.split(' ')[0] || 'Guest',
        last_name: apiResponse.patient_info?.name?.split(' ')[1] || '',
        current_age: apiResponse.patient_info?.age || 0,
        cultural_heritage: apiResponse.patient_info?.cultural_heritage || '',
        birth_year:
          new Date().getFullYear() - (apiResponse.patient_info?.age || 0),
        city: 'Brooklyn', // Default from our API payload
        state: 'New York',
        interests: ['cooking', 'family', 'music'],
      }
      setPatientProfile(profileData)

      console.log('✅ Dashboard data loaded successfully')
    } catch (err) {
      console.error('Failed to load dashboard:', err)
      setError(err.message || 'Failed to load content')
    } finally {
      setLoading(false)
    }
  }

  // Handle feedback collection
  const handleFeedback = (type, item, category) => {
    console.log(`📝 Collecting feedback: ${type} for ${category}`)
    feedbackManager.collectFeedback(type, item, category)

    // Optional: Show a brief confirmation
    // Could add a toast notification here
  }

  // Navigation handlers
  const handleNavigate = page => {
    console.log(`🧭 Navigating to: ${page}`)
    setCurrentPage(page)
  }

  const handleBack = () => {
    console.log('🔙 Navigating back to dashboard')
    setCurrentPage('dashboard')
  }

  const handleViewChange = view => {
    console.log(`👀 Changing view to: ${view}`)
    setCurrentView(view)
  }

  const handleProfileClick = () => {
    console.log('👤 Opening profile')
    setCurrentPage('profile')
  }

  // Render loading state
  if (loading) {
    return <LoadingSpinner />
  }

  // Render error state
  if (error && !dashboardData) {
    return <ErrorMessage error={error} onRetry={loadDashboardData} />
  }

  // Main app render
  return (
    <div className='app min-h-screen' style={{ backgroundColor: '#F8F7ED' }}>
      {/* Optional: Connection status indicator */}
      {connectionStatus && !connectionStatus.success && (
        <div className='bg-yellow-50 border-b border-yellow-200 p-3'>
          <div className='max-w-6xl mx-auto flex items-center justify-between'>
            <p className='text-yellow-800 text-sm flex items-center'>
              <span className='mr-2'>📡</span>
              Backend connection: {connectionStatus.message} - Using demo data
            </p>
            <button
              onClick={testBackendConnection}
              className='text-yellow-700 hover:text-yellow-900 text-sm underline'
            >
              Test Again
            </button>
          </div>
        </div>
      )}

      {/* Optional: Fallback indicator */}
      {dashboardData?.metadata?.isUsingFallback && (
        <div className='bg-blue-50 border-b border-blue-200 p-3'>
          <div className='max-w-6xl mx-auto'>
            <p className='text-blue-800 text-sm flex items-center'>
              <span className='mr-2'>🎭</span>
              Demo mode - showing sample personalized content
            </p>
          </div>
        </div>
      )}

      <main className='min-h-screen'>
        {currentView === 'demo' ? (
          <Demo />
        ) : (
          <>
            {currentPage === 'dashboard' && (
              <Dashboard
                data={dashboardData}
                onNavigate={handleNavigate}
                onFeedback={handleFeedback}
                onRefresh={loadDashboardData}
                onViewChange={handleViewChange}
                onProfileClick={handleProfileClick}
                currentView={currentView}
              />
            )}
            {currentPage === 'music' && (
              <MusicDetail
                data={dashboardData?.music}
                onBack={handleBack}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'photo' && (
              <PhotoDetail
                data={dashboardData?.photo}
                onBack={handleBack}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'recipe' && (
              <RecipeDetail
                data={dashboardData?.recipe}
                onBack={handleBack}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'nostalgia' && (
              <NostalgiaDetail
                data={dashboardData?.nostalgia}
                onBack={handleBack}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'profile' && (
              <Profile
                patientProfile={patientProfile}
                feedback={feedbackManager.getFeedback()}
                feedbackSummary={feedbackManager.getFeedbackSummary()}
                onBack={handleBack}
                onClearFeedback={() => {
                  feedbackManager.clearFeedback()
                  window.location.reload() // Simple refresh
                }}
              />
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default App
