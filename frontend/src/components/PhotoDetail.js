import React from 'react'

const PhotoDetail = ({ data, onBack, onFeedback }) => {
  const photoData = data || {}

  const handleLike = () => {
    if (onFeedback) {
      onFeedback('like', photoData.description || photoData.filename, 'photo')
    }
  }

  const handleDislike = () => {
    if (onFeedback) {
      onFeedback(
        'dislike',
        photoData.description || photoData.filename,
        'photo',
      )
    }
  }

  // Get photo icon based on filename
  const getPhotoIcon = filename => {
    if (!filename) return '🖼️'
    if (filename.includes('family')) return '👨‍👩‍👧‍👦'
    if (filename.includes('music')) return '🎹'
    if (filename.includes('birthday')) return '🎂'
    if (filename.includes('beach') || filename.includes('ocean')) return '🏖️'
    return '📸'
  }

  return (
    <div className='min-h-screen' style={{ backgroundColor: '#F8F7ED' }}>
      <div className='max-w-4xl mx-auto p-6'>
        <button
          onClick={onBack}
          className='mb-8 flex items-center hover:text-gray-800 font-medium text-lg min-h-12'
          style={{ color: '#4A4A4A' }}
        >
          <svg
            className='w-6 h-6 mr-3'
            fill='none'
            stroke='currentColor'
            viewBox='0 0 24 24'
          >
            <path
              strokeLinecap='round'
              strokeLinejoin='round'
              strokeWidth={2}
              d='M10 19l-7-7m0 0l7-7m-7 7h18'
            />
          </svg>
          Back to Dashboard
        </button>

        <div className='bg-white rounded-xl shadow-sm p-8 border-2 border-gray-100'>
          <div className='flex items-center justify-between mb-8'>
            <div className='flex items-center'>
              <div
                className='w-8 h-8 rounded-full mr-4'
                style={{ backgroundColor: '#8B7CB6' }}
              ></div>
              <h2 className='text-4xl font-light' style={{ color: '#4A4A4A' }}>
                Photo of the Day
              </h2>
            </div>

            {/* Feedback buttons */}
            <div className='flex space-x-3'>
              <button
                onClick={handleLike}
                className='px-4 py-2 bg-green-100 hover:bg-green-200 text-green-700 rounded-lg transition-colors flex items-center space-x-2'
              >
                <span>👍</span>
                <span>Like</span>
              </button>
              <button
                onClick={handleDislike}
                className='px-4 py-2 bg-red-100 hover:bg-red-200 text-red-700 rounded-lg transition-colors flex items-center space-x-2'
              >
                <span>👎</span>
                <span>Dislike</span>
              </button>
            </div>
          </div>

          {/* Photo Display */}
          <div className='mb-8'>
            <div className='w-full h-80 bg-gradient-to-br from-blue-200 to-blue-300 rounded-lg flex items-center justify-center text-gray-700 border-2 border-gray-200'>
              <div className='text-center'>
                <div className='text-6xl mb-4'>
                  {getPhotoIcon(photoData.filename)}
                </div>
                <div className='font-medium text-xl'>
                  {photoData.filename || 'Loading photo...'}
                </div>
              </div>
            </div>
          </div>

          {/* Description */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              📖 Description
            </h4>
            <p
              className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
              style={{ backgroundColor: '#F0F0F0', borderColor: '#A8B5A0' }}
            >
              {photoData.description || 'Photo description loading...'}
            </p>
          </div>

          {/* Cultural Context */}
          {photoData.culturalContext && (
            <div className='mb-8'>
              <h4
                className='text-2xl font-medium mb-6'
                style={{ color: '#4A4A4A' }}
              >
                🏛️ Cultural Context
              </h4>
              <p
                className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
                style={{ backgroundColor: '#F5F3FF', borderColor: '#8B7CB6' }}
              >
                {photoData.culturalContext}
              </p>
            </div>
          )}

          {/* Conversation Starters */}
          <div>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              💬 Conversation Starters
            </h4>
            <ul className='space-y-4'>
              {photoData.conversationStarters &&
              photoData.conversationStarters.length > 0 ? (
                photoData.conversationStarters.map((starter, index) => (
                  <li
                    key={index}
                    className='text-gray-700 text-lg p-6 rounded-lg border-2'
                    style={{
                      backgroundColor: '#F0F0F0',
                      borderColor: '#A8B5A0',
                    }}
                  >
                    "{starter}"
                  </li>
                ))
              ) : (
                <li className='text-gray-500 text-lg p-6 rounded-lg border-2 border-dashed border-gray-300'>
                  Conversation starters loading...
                </li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PhotoDetail
