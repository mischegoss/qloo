import React from 'react'

const Dashboard = ({
  data,
  onNavigate,
  onFeedback,
  onRefresh,
  onViewChange,
  onProfileClick,
  currentView,
  patientName, // Use this prop instead of API response
  patientProfile, // Also available if needed
}) => {
  // Use data from API instead of hardcoded realDashboardData
  const dashboardData = data || {}

  // Extract data from new API structure
  const patientInfo = dashboardData.patient_info || dashboardData.patient || {}
  const content = dashboardData.content || {}
  const musicData = content.music || {}
  const recipeData = content.recipe || {}
  const photoData = content.photo || {}
  const nostalgiaData = content.nostalgia_news || {}

  // Get theme from correct location in API response
  const currentTheme =
    dashboardData.metadata?.theme ||
    patientInfo.daily_theme ||
    content.theme ||
    'Memory Lane'

  // Get current date using JavaScript Date object (no API call)
  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })

  return (
    <div className='min-h-screen' style={{ backgroundColor: '#F8F7ED' }}>
      <div className='max-w-6xl mx-auto p-6'>
        {/* Welcome Header */}
        <div className='text-center mb-12'>
          <h1 className='text-5xl font-light mb-6' style={{ color: '#4A4A4A' }}>
            Welcome, {patientName || 'Friend'}!
          </h1>
          <div
            className='text-3xl font-light mb-2'
            style={{ color: '#4A4A4A' }}
          >
            Today is {currentDate}
          </div>
          <div className='text-3xl font-light' style={{ color: '#4A4A4A' }}>
            Today's Theme is {currentTheme}
          </div>
        </div>

        {/* Three Card Grid - Desktop: 3 columns, Mobile: 1 column */}
        <div className='grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10'>
          {/* Music Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-transparent hover:border-orange-300 cursor-pointer hover:shadow-md transition-all hover:-translate-y-1'
            onClick={() => onNavigate && onNavigate('music')}
            style={{ borderColor: '#D4A574' }}
            onMouseEnter={e => {
              e.target.style.backgroundColor = '#FDF9F3'
              e.target.style.borderColor = '#B8935F'
            }}
            onMouseLeave={e => {
              e.target.style.backgroundColor = 'white'
              e.target.style.borderColor = '#D4A574'
            }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-10 h-10 rounded-full mr-4 flex items-center justify-center text-white text-xl'
                style={{ backgroundColor: '#D4A574' }}
              >
                🎵
              </div>
              <h3
                className='text-2xl font-semibold'
                style={{ color: '#4A4A4A' }}
              >
                Music
              </h3>
            </div>
            <div
              className='text-base font-medium mb-4'
              style={{ color: '#6B6B6B' }}
            >
              Engage through Sound
            </div>
            <h4 className='text-xl font-semibold text-gray-800 mb-2'>
              {musicData.artist && musicData.piece_title
                ? `${musicData.artist}: ${musicData.piece_title}`
                : musicData.artist ||
                  musicData.piece_title ||
                  'Classical Music'}
            </h4>
          </div>

          {/* Recipe Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-transparent hover:border-orange-400 cursor-pointer hover:shadow-md transition-all hover:-translate-y-1'
            onClick={() => onNavigate && onNavigate('recipe')}
            style={{ borderColor: '#C4916B' }}
            onMouseEnter={e => {
              e.target.style.backgroundColor = '#FBF6F0'
              e.target.style.borderColor = '#A67A56'
            }}
            onMouseLeave={e => {
              e.target.style.backgroundColor = 'white'
              e.target.style.borderColor = '#C4916B'
            }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-10 h-10 rounded-full mr-4 flex items-center justify-center text-white text-xl'
                style={{ backgroundColor: '#C4916B' }}
              >
                🍽️
              </div>
              <h3
                className='text-2xl font-semibold'
                style={{ color: '#4A4A4A' }}
              >
                Recipe
              </h3>
            </div>
            <div
              className='text-base font-medium mb-4'
              style={{ color: '#6B6B6B' }}
            >
              Connect Through Taste and Smell
            </div>
            <h4 className='text-xl font-semibold text-gray-800 mb-2'>
              {recipeData.name || 'Comfort Food Recipe'}
            </h4>
          </div>

          {/* Photo Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-transparent hover:border-purple-400 cursor-pointer hover:shadow-md transition-all hover:-translate-y-1'
            onClick={() => onNavigate && onNavigate('photo')}
            style={{ borderColor: '#8B7CB6' }}
            onMouseEnter={e => {
              e.target.style.backgroundColor = '#F8F6FF'
              e.target.style.borderColor = '#7A6BA4'
            }}
            onMouseLeave={e => {
              e.target.style.backgroundColor = 'white'
              e.target.style.borderColor = '#8B7CB6'
            }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-10 h-10 rounded-full mr-4 flex items-center justify-center text-white text-xl'
                style={{ backgroundColor: '#8B7CB6' }}
              >
                📸
              </div>
              <h3
                className='text-2xl font-semibold'
                style={{ color: '#4A4A4A' }}
              >
                Photo of the Day
              </h3>
            </div>
            <div
              className='text-base font-medium mb-4'
              style={{ color: '#6B6B6B' }}
            >
              Stimulate through Sight
            </div>
            <h4 className='text-xl font-semibold text-gray-800 mb-2'>
              {photoData.filename
                ? `${currentTheme} Photo`
                : `A ${currentTheme}-Related Photo`}
            </h4>
          </div>
        </div>

        {/* Nostalgia News Section - Larger and Centered */}
        <div className='flex justify-center mt-4'>
          <div
            className='bg-white rounded-xl p-12 shadow-lg border-2 cursor-pointer hover:shadow-xl transition-all hover:-translate-y-1 max-w-4xl w-full'
            onClick={() => onNavigate && onNavigate('nostalgia')}
            style={{ borderColor: '#B8A9D9' }}
            onMouseEnter={e => {
              e.target.style.backgroundColor = '#FDFCFF'
              e.target.style.borderColor = '#A695C7'
            }}
            onMouseLeave={e => {
              e.target.style.backgroundColor = 'white'
              e.target.style.borderColor = '#B8A9D9'
            }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-12 h-12 rounded-full mr-4 flex items-center justify-center text-white text-2xl'
                style={{ backgroundColor: '#B8A9D9' }}
              >
                📰
              </div>
              <h3
                className='text-3xl font-semibold'
                style={{ color: '#4A4A4A' }}
              >
                Nostalgia News
              </h3>
            </div>
            <div
              className='text-lg font-medium mb-4'
              style={{ color: '#6B6B6B' }}
            >
              Explore through Stories
            </div>
            <h4 className='text-2xl font-semibold text-gray-800 mb-4'>
              {nostalgiaData.headline ||
                nostalgiaData.title ||
                `Personalized for ${patientName || 'you'}`}
            </h4>
            <p className='text-lg text-gray-600 leading-relaxed'>
              {nostalgiaData.content ||
                `Discover meaningful connections 
                and memories that bring warmth to your day.`}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
