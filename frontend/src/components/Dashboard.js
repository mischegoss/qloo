// Example of how to update your Dashboard component to use API data
import React from 'react'

const Dashboard = ({
  data,
  onNavigate,
  onFeedback,
  onRefresh,
  onViewChange,
  onProfileClick,
  currentView,
}) => {
  // Use data from API instead of hardcoded realDashboardData
  const dashboardData = data || {}

  // Handle refresh with loading state
  const handleRefresh = async () => {
    console.log('🔄 Refreshing dashboard...')
    if (onRefresh) {
      await onRefresh()
    }
  }

  // Quick feedback handlers
  const handleQuickLike = (category, item) => {
    if (onFeedback) {
      onFeedback('like', item, category)
    }
  }

  const handleQuickDislike = (category, item) => {
    if (onFeedback) {
      onFeedback('dislike', item, category)
    }
  }

  return (
    <div className='min-h-screen' style={{ backgroundColor: '#F8F7ED' }}>
      {/* Header */}
      <header className='text-gray-700 p-4 shadow-sm border-b border-gray-200'>
        <div className='max-w-6xl mx-auto flex justify-between items-center'>
          <div className='flex items-center'>
            {/* Your existing LumiCue logo */}
            <span
              className='text-2xl font-light tracking-wide'
              style={{ color: '#4A4A4A' }}
            >
              LumiCue
            </span>
          </div>
          <div className='flex items-center space-x-6'>
            <nav className='flex space-x-4'>
              <button
                onClick={() => onViewChange && onViewChange('app')}
                className={`px-6 py-3 rounded-lg text-lg font-medium transition-colors min-h-12 ${
                  currentView === 'app'
                    ? 'text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                style={{
                  backgroundColor:
                    currentView === 'app' ? '#8B7CB6' : 'transparent',
                }}
              >
                App
              </button>
              <button
                onClick={() => onViewChange && onViewChange('demo')}
                className={`px-6 py-3 rounded-lg text-lg font-medium transition-colors min-h-12 ${
                  currentView === 'demo'
                    ? 'text-white'
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                style={{
                  backgroundColor:
                    currentView === 'demo' ? '#8B7CB6' : 'transparent',
                }}
              >
                Demo
              </button>
            </nav>
            <button
              onClick={onProfileClick}
              className='p-3 rounded-full hover:bg-gray-100 transition-colors'
              title='View Profile'
            >
              👤
            </button>
          </div>
        </div>
      </header>

      <div className='max-w-6xl mx-auto p-6'>
        {/* Welcome section with dynamic data */}
        <div className='text-center mb-12'>
          <h1 className='text-5xl font-light mb-4' style={{ color: '#4A4A4A' }}>
            Welcome, {dashboardData.patient?.name || 'Friend'}
          </h1>
          <h2 className='text-3xl font-light' style={{ color: '#6B6B6B' }}>
            Today's Theme is {dashboardData.patient?.theme || 'Memory Lane'}
          </h2>
        </div>

        {/* Content grid with dynamic data */}
        <div className='grid md:grid-cols-2 gap-8 mb-12'>
          {/* Music Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-gray-100 cursor-pointer hover:shadow-md transition-shadow'
            onClick={() => onNavigate && onNavigate('music')}
            style={{ backgroundColor: '#FDF5E6' }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-8 h-8 rounded-full mr-4'
                style={{ backgroundColor: '#D4A574' }}
              ></div>
              <h3 className='text-2xl font-medium' style={{ color: '#4A4A4A' }}>
                Music
              </h3>
            </div>
            <h4 className='text-xl font-medium text-gray-800 mb-2'>
              {dashboardData.music?.title || 'Loading...'}
            </h4>
            <p className='text-lg text-gray-600 mb-4'>
              by {dashboardData.music?.artist || 'Artist'}
            </p>
            {/* Quick feedback buttons */}
            <div className='flex space-x-2'>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickLike(
                    'music',
                    `${dashboardData.music?.artist} - ${dashboardData.music?.title}`,
                  )
                }}
                className='px-3 py-1 text-sm bg-green-100 hover:bg-green-200 rounded transition-colors'
              >
                👍
              </button>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickDislike(
                    'music',
                    `${dashboardData.music?.artist} - ${dashboardData.music?.title}`,
                  )
                }}
                className='px-3 py-1 text-sm bg-red-100 hover:bg-red-200 rounded transition-colors'
              >
                👎
              </button>
            </div>
          </div>

          {/* Recipe Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-gray-100 cursor-pointer hover:shadow-md transition-shadow'
            onClick={() => onNavigate && onNavigate('recipe')}
            style={{ backgroundColor: '#F0F0F0' }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-8 h-8 rounded-full mr-4'
                style={{ backgroundColor: '#C4916B' }}
              ></div>
              <h3 className='text-2xl font-medium' style={{ color: '#4A4A4A' }}>
                Recipe
              </h3>
            </div>
            <h4 className='text-xl font-medium text-gray-800 mb-2'>
              {dashboardData.recipe?.name || 'Loading...'}
            </h4>
            <p className='text-lg text-gray-600 mb-4'>A comforting dish</p>
            {/* Quick feedback buttons */}
            <div className='flex space-x-2'>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickLike('recipe', dashboardData.recipe?.name)
                }}
                className='px-3 py-1 text-sm bg-green-100 hover:bg-green-200 rounded transition-colors'
              >
                👍
              </button>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickDislike('recipe', dashboardData.recipe?.name)
                }}
                className='px-3 py-1 text-sm bg-red-100 hover:bg-red-200 rounded transition-colors'
              >
                👎
              </button>
            </div>
          </div>

          {/* Photo Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-gray-100 cursor-pointer hover:shadow-md transition-shadow'
            onClick={() => onNavigate && onNavigate('photo')}
            style={{ backgroundColor: '#F5F3FF' }}
          >
            <div className='flex items-center mb-6'>
              <div
                className='w-8 h-8 rounded-full mr-4'
                style={{ backgroundColor: '#8B7CB6' }}
              ></div>
              <h3 className='text-2xl font-medium' style={{ color: '#4A4A4A' }}>
                Photo of the day
              </h3>
            </div>
            <h4 className='text-xl font-medium text-gray-800 mb-2'>
              {dashboardData.photo?.filename || 'Loading...'}
            </h4>
            <p className='text-lg text-gray-600 mb-4'>A meaningful moment</p>
            {/* Quick feedback buttons */}
            <div className='flex space-x-2'>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickLike('photo', dashboardData.photo?.description)
                }}
                className='px-3 py-1 text-sm bg-green-100 hover:bg-green-200 rounded transition-colors'
              >
                👍
              </button>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickDislike('photo', dashboardData.photo?.description)
                }}
                className='px-3 py-1 text-sm bg-red-100 hover:bg-red-200 rounded transition-colors'
              >
                👎
              </button>
            </div>
          </div>

          {/* Nostalgia News Card */}
          <div
            className='bg-white rounded-xl p-8 shadow-sm border-2 border-gray-100 cursor-pointer hover:shadow-md transition-shadow'
            onClick={() => onNavigate && onNavigate('nostalgia')}
            style={{ backgroundColor: '#FFF7F0' }}
          >
            <div className='flex items-center mb-6'>
              <div className='flex space-x-2 mr-4'>
                <div
                  className='w-3 h-3 rounded-full'
                  style={{ backgroundColor: '#D4A574' }}
                ></div>
                <div
                  className='w-3 h-3 rounded-full'
                  style={{ backgroundColor: '#C4916B' }}
                ></div>
                <div
                  className='w-3 h-3 rounded-full'
                  style={{ backgroundColor: '#8B7CB6' }}
                ></div>
              </div>
              <h3 className='text-2xl font-medium' style={{ color: '#4A4A4A' }}>
                Nostalgia News
              </h3>
            </div>
            <h4 className='text-xl font-medium text-gray-800 mb-2'>
              {dashboardData.nostalgia?.headline || 'Loading...'}
            </h4>
            <p className='text-lg text-gray-600 mb-4'>
              Personal stories and memories
            </p>
            {/* Quick feedback buttons */}
            <div className='flex space-x-2'>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickLike(
                    'nostalgia',
                    dashboardData.nostalgia?.headline,
                  )
                }}
                className='px-3 py-1 text-sm bg-green-100 hover:bg-green-200 rounded transition-colors'
              >
                👍
              </button>
              <button
                onClick={e => {
                  e.stopPropagation()
                  handleQuickDislike(
                    'nostalgia',
                    dashboardData.nostalgia?.headline,
                  )
                }}
                className='px-3 py-1 text-sm bg-red-100 hover:bg-red-200 rounded transition-colors'
              >
                👎
              </button>
            </div>
          </div>
        </div>

        {/* Refresh button */}
        <div className='text-center'>
          <button
            onClick={handleRefresh}
            className='px-8 py-4 rounded-full text-white text-lg font-medium hover:opacity-90 transition-opacity'
            style={{ backgroundColor: '#4A4A4A' }}
          >
            Refresh Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
