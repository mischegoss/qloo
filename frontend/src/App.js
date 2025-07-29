import { useState, useEffect, useCallback } from 'react'
import apiService from './services/apiService'
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

// LumiCue Logo Component with subtle animation
const LumiCueLogo = () => (
  <div className='flex items-center'>
    {/* Animated dots - centered and sized to match font */}
    <div className='flex items-center space-x-1 mr-3'>
      <div
        className='w-4 h-4 rounded-full animate-bounce-subtle'
        style={{ backgroundColor: '#B8B0D7', animationDelay: '0ms' }}
      ></div>
      <div
        className='w-4 h-4 rounded-full animate-bounce-subtle'
        style={{ backgroundColor: '#FFDAC0', animationDelay: '400ms' }}
      ></div>
      <div
        className='w-4 h-4 rounded-full animate-bounce-subtle'
        style={{ backgroundColor: '#8B7CB6', animationDelay: '800ms' }}
      ></div>
    </div>
    <span
      className='text-2xl font-light tracking-wide'
      style={{ color: '#4A4A4A' }}
    >
      LumiCue
    </span>

    {/* Custom styles for subtle header animation */}
    <style>{`
      @keyframes header-bounce-subtle {
        0%, 10% { 
          transform: translateY(0); 
          opacity: 0.7;
        }
        5% { 
          transform: translateY(-3px); 
          opacity: 1;
        }
        15%, 100% { 
          transform: translateY(0); 
          opacity: 0.7;
        }
      }
      
      .animate-bounce-subtle { 
        animation: header-bounce-subtle 8s ease-in-out infinite; 
      }
    `}</style>
  </div>
)

// Header Component
const Header = ({ currentView, onViewChange, onProfileClick }) => {
  return (
    <header
      className='text-gray-700 p-4 shadow-sm border-b border-gray-200'
      style={{ backgroundColor: '#F8F7ED' }}
    >
      <div className='max-w-6xl mx-auto flex justify-between items-center'>
        <LumiCueLogo />
        <div className='flex items-center space-x-6'>
          <nav className='flex space-x-4'>
            <button
              onClick={() => onViewChange('app')}
              className={`px-6 py-3 rounded-lg text-lg font-medium transition-colors min-h-12 ${
                currentView === 'app'
                  ? 'text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
              style={{
                backgroundColor:
                  currentView === 'app' ? '#8B7CB6' : 'transparent',
              }}
              title='Access the personalized recommendations dashboard.'
            >
              App
            </button>
            <button
              onClick={() => onViewChange('demo')}
              className={`px-6 py-3 rounded-lg text-lg font-medium transition-colors min-h-12 ${
                currentView === 'demo'
                  ? 'text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
              style={{
                backgroundColor:
                  currentView === 'demo' ? '#8B7CB6' : 'transparent',
              }}
              title='Watch the AI agents at work making personalized recommendations.'
            >
              Demo
            </button>
          </nav>
          {currentView === 'app' && (
            <button
              onClick={onProfileClick}
              className='p-3 rounded-full hover:bg-orange-200 transition-colors min-h-12 min-w-12'
              style={{ backgroundColor: '#D4A574' }}
            >
              <svg
                className='w-6 h-6 text-white'
                fill='currentColor'
                viewBox='0 0 24 24'
              >
                <path d='M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z' />
              </svg>
            </button>
          )}
        </div>
      </div>
    </header>
  )
}

// Error Component
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
  const loadDashboardData = useCallback(async (profileToUse = null) => {
    try {
      setLoading(true)
      setError(null)

      // Get current feedback for API call
      const currentFeedback = feedbackManager.formatForAPI()

      console.log('📡 Loading dashboard data...')

      // Get stored profile from localStorage or use default
      let currentProfile = profileToUse
      if (!currentProfile) {
        try {
          const storedProfile = localStorage.getItem('patient_profile')
          currentProfile = storedProfile ? JSON.parse(storedProfile) : null
        } catch (error) {
          console.warn('Failed to load stored profile:', error)
        }
      }

      // If no stored profile, use default
      if (!currentProfile) {
        currentProfile = {
          name: 'Lily', // Use 'name' for API
          first_name: 'Lily',
          last_name: '',
          birth_year: 1942,
          cultural_heritage: 'Italian-American',
          city: 'Brooklyn',
          state: 'New York',
          interests: ['cooking', 'family', 'music'],
          current_age: new Date().getFullYear() - 1942,
        }
        // Store the default profile
        try {
          localStorage.setItem(
            'patient_profile',
            JSON.stringify(currentProfile),
          )
        } catch (error) {
          console.warn('Failed to store default profile:', error)
        }
      }

      // Make API call with correct profile
      const apiResponse = await apiService.getDashboardData(
        currentProfile, // Send the actual profile!
        currentFeedback,
      )

      console.log('🔄 Using API response directly...')

      // Use API response directly without transformation
      setDashboardData(apiResponse)

      // Store patient profile for display (use what we sent to API)
      setPatientProfile(currentProfile)

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
  }, [loadDashboardData])

  // Handle profile updates
  const handleProfileUpdate = async updatedProfile => {
    try {
      console.log('🔄 Updating patient profile...', updatedProfile)

      // Add 'name' field for API compatibility
      const profileWithName = {
        ...updatedProfile,
        name: updatedProfile.first_name || updatedProfile.name,
      }

      // Store in localStorage for persistence
      try {
        localStorage.setItem('patient_profile', JSON.stringify(profileWithName))
        console.log('💾 Profile saved to localStorage')
      } catch (error) {
        console.warn('Failed to save profile to localStorage:', error)
      }

      // Update the patient profile state
      setPatientProfile(profileWithName)

      // Reload dashboard with new profile data
      await loadDashboardData(profileWithName)

      console.log('✅ Profile and dashboard updated successfully')
    } catch (error) {
      console.error('Failed to update profile:', error)
      throw error
    }
  }

  // Handle feedback collection
  const handleFeedback = (type, item, category) => {
    console.log(`📝 Collecting feedback: ${type} for ${category}`)
    feedbackManager.collectFeedback(type, item, category)
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
      <Header
        currentView={currentView}
        onViewChange={handleViewChange}
        onProfileClick={handleProfileClick}
      />

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
                onNavigate={handleNavigate}
                onFeedback={handleFeedback}
                data={dashboardData}
                patientProfile={patientProfile}
                // Pass the local profile name, not from API
                patientName={patientProfile?.first_name || 'Lily'}
              />
            )}
            {currentPage === 'music' && (
              <MusicDetail
                onBack={handleBack}
                musicData={dashboardData?.music}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'photo' && (
              <PhotoDetail
                onBack={handleBack}
                photoData={dashboardData?.photo}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'recipe' && (
              <RecipeDetail
                onBack={handleBack}
                recipeData={dashboardData?.recipe}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'nostalgia' && (
              <NostalgiaDetail
                onBack={handleBack}
                nostalgiaData={dashboardData?.nostalgia}
                onFeedback={handleFeedback}
              />
            )}
            {currentPage === 'profile' && (
              <Profile
                onBack={handleBack}
                patientProfile={patientProfile}
                onProfileUpdate={handleProfileUpdate}
              />
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default App
