import React from 'react'

const MusicDetail = ({ data, onBack, onFeedback }) => {
  const musicData = data || {}

  const handleLike = () => {
    if (onFeedback) {
      onFeedback('like', `${musicData.artist} - ${musicData.title}`, 'music')
    }
  }

  const handleDislike = () => {
    if (onFeedback) {
      onFeedback('dislike', `${musicData.artist} - ${musicData.title}`, 'music')
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
              <div
                className='w-8 h-8 rounded-full mr-4'
                style={{ backgroundColor: '#D4A574' }}
              ></div>
              <h2 className='text-4xl font-light' style={{ color: '#4A4A4A' }}>
                Today's Music
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

          <div className='mb-8'>
            <h3 className='text-3xl font-medium text-gray-800 mb-2'>
              {musicData.artist || 'Loading artist...'}
            </h3>
            <p className='text-2xl text-gray-600'>
              {musicData.title || 'Loading piece...'}
            </p>
          </div>

          {/* YouTube Video */}
          <div className='mb-8'>
            {musicData.embedUrl ? (
              <iframe
                width='100%'
                height='400'
                src={musicData.embedUrl}
                title='YouTube video player'
                frameBorder='0'
                allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
                allowFullScreen
                className='rounded-lg border border-gray-200'
              ></iframe>
            ) : (
              <div className='w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center border border-gray-200'>
                <div className='text-center text-gray-500'>
                  <div className='text-6xl mb-4'>🎵</div>
                  <p className='text-lg'>Music loading...</p>
                </div>
              </div>
            )}
          </div>

          {/* Conversation Starters */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              💬 Conversation Starters
            </h4>
            <ul className='space-y-4'>
              {musicData.conversationStarters &&
              musicData.conversationStarters.length > 0 ? (
                musicData.conversationStarters.map((starter, index) => (
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

          {/* Fun Fact */}
          {musicData.funFact && (
            <div
              className='p-6 rounded-lg border-2'
              style={{ backgroundColor: '#F5F3FF', borderColor: '#8B7CB6' }}
            >
              <h4
                className='text-2xl font-medium mb-4'
                style={{ color: '#4A4A4A' }}
              >
                🎼 Fun Fact
              </h4>
              <p className='text-gray-700 text-lg leading-relaxed'>
                {musicData.funFact}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MusicDetail
