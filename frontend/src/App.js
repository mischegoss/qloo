import { useState, useEffect, useCallback } from 'react'
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

// Import the new professional LoadingSpinner component
import LoadingSpinner from './components/LoadingSpinner'

// Error Component (keeping this inline since it's simple)
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

  // Load dashboard data from API (wrapped with useCallback to fix useEffect dependency warning)
  const loadDashboardData = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      // Get current feedback for API call
      const currentFeedback = feedbackManager.formatForAPI()

      console.log('📡 Loading dashboard data...')

      // Make API call with feedback
      const apiResponse = await apiService.getDashboardData(
        null, // Remove patientProfile dependency to avoid loop
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
  }, []) // Empty dependency array - function doesn't depend on changing values

  // Load dashboard data on mount
  useEffect(() => {
    loadDashboardData()
  }, [loadDashboardData]) // Fixed: Added loadDashboardData to dependencies

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
    if (view === 'app') {
      setCurrentPage('dashboard')
    }
  }

  const handleProfileClick = () => {
    console.log('👤 Opening profile')
    setCurrentPage('profile')
  }

  // Demo-specific handlers
  const handleDashboardUpdate = newData => {
    console.log('📊 Dashboard updated with new data from demo:', newData)
    // Optionally refresh the dashboard data to show the new content
    // loadDashboardData()
  }

  const handleReturnToDashboard = () => {
    console.log('🔄 Returning to dashboard from demo')
    setCurrentView('app')
    setCurrentPage('dashboard')
    // Optionally refresh the dashboard to show new cached content
    loadDashboardData()
  }

  // Render loading state with professional branded spinner
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
      <main className='min-h-screen'>
        {currentView === 'demo' ? (
          <Demo
            onDashboardUpdate={handleDashboardUpdate}
            onReturnToDashboard={handleReturnToDashboard}
          />
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
