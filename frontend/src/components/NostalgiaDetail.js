import React from 'react'

const NostalgiaDetail = ({ data, onBack, onFeedback }) => {
  const nostalgiaData = data || {}

  const handleLike = () => {
    if (onFeedback) {
      onFeedback('like', nostalgiaData.headline, 'nostalgia')
    }
  }

  const handleDislike = () => {
    if (onFeedback) {
      onFeedback('dislike', nostalgiaData.headline, 'nostalgia')
    }
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
              <div className='flex space-x-2 mr-4'>
                <div
                  className='w-6 h-6 rounded-full'
                  style={{ backgroundColor: '#D4A574' }}
                ></div>
                <div
                  className='w-6 h-6 rounded-full'
                  style={{ backgroundColor: '#C4916B' }}
                ></div>
                <div
                  className='w-6 h-6 rounded-full'
                  style={{ backgroundColor: '#8B7CB6' }}
                ></div>
              </div>
              <h2 className='text-4xl font-light' style={{ color: '#4A4A4A' }}>
                Nostalgia News
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

          {/* Headline */}
          <div className='mb-8'>
            <h3 className='text-3xl font-medium text-gray-800 mb-4'>
              {nostalgiaData.headline || 'Loading nostalgia news...'}
            </h3>
          </div>

          {/* Main Content */}
          {nostalgiaData.content && (
            <div className='mb-8'>
              <div
                className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
                style={{ backgroundColor: '#FFF7F0', borderColor: '#D4A574' }}
              >
                {nostalgiaData.content}
              </div>
            </div>
          )}

          {/* Memory Spotlight Section */}
          {nostalgiaData.memorySpotlight && (
            <div className='mb-8'>
              <h4
                className='text-2xl font-medium mb-4'
                style={{ color: '#4A4A4A' }}
              >
                ✨ {nostalgiaData.memorySpotlight.headline}
              </h4>
              <div
                className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
                style={{ backgroundColor: '#F0F0F0', borderColor: '#A8B5A0' }}
              >
                {nostalgiaData.memorySpotlight.content}
              </div>
            </div>
          )}

          {/* Era Spotlight Section */}
          {nostalgiaData.eraSpotlight && (
            <div className='mb-8'>
              <h4
                className='text-2xl font-medium mb-4'
                style={{ color: '#4A4A4A' }}
              >
                🕰️ {nostalgiaData.eraSpotlight.headline}
              </h4>
              <div
                className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
                style={{ backgroundColor: '#F5F3FF', borderColor: '#8B7CB6' }}
              >
                {nostalgiaData.eraSpotlight.content}
              </div>
            </div>
          )}

          {/* Heritage Traditions Section */}
          {nostalgiaData.heritageTraditions && (
            <div className='mb-8'>
              <h4
                className='text-2xl font-medium mb-4'
                style={{ color: '#4A4A4A' }}
              >
                🏛️ {nostalgiaData.heritageTraditions.headline}
              </h4>
              <div
                className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
                style={{ backgroundColor: '#FDF5E6', borderColor: '#D4A574' }}
              >
                {nostalgiaData.heritageTraditions.content}
              </div>
            </div>
          )}

          {/* Themes Display */}
          {nostalgiaData.themes && nostalgiaData.themes.length > 0 && (
            <div className='mb-8'>
              <h4
                className='text-2xl font-medium mb-4'
                style={{ color: '#4A4A4A' }}
              >
                🏷️ Themes
              </h4>
              <div className='flex flex-wrap gap-3'>
                {nostalgiaData.themes.map((theme, index) => (
                  <span
                    key={index}
                    className='px-4 py-2 rounded-full text-sm font-medium'
                    style={{ backgroundColor: '#F0F0F0', color: '#4A4A4A' }}
                  >
                    {theme}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Conversation Corner */}
          <div>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              💬{' '}
              {nostalgiaData.conversationCorner?.headline ||
                'Conversation Starters'}
            </h4>
            <ul className='space-y-4'>
              {nostalgiaData.conversationStarters &&
              nostalgiaData.conversationStarters.length > 0 ? (
                nostalgiaData.conversationStarters.map((starter, index) => (
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
              ) : nostalgiaData.conversationCorner?.questions &&
                nostalgiaData.conversationCorner.questions.length > 0 ? (
                nostalgiaData.conversationCorner.questions.map(
                  (question, index) => (
                    <li
                      key={index}
                      className='text-gray-700 text-lg p-6 rounded-lg border-2'
                      style={{
                        backgroundColor: '#F0F0F0',
                        borderColor: '#A8B5A0',
                      }}
                    >
                      "{question}"
                    </li>
                  ),
                )
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

export default NostalgiaDetail
