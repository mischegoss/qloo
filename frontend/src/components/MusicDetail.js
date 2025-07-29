import React from 'react'
import FeedbackButtons from './FeedbackButtons'
import dashboardDataStore from '../services/dashboardDataStore'

const MusicDetail = ({ onBack, onFeedback }) => {
  // Get music data directly from global store instead of props
  const musicData = dashboardDataStore.getMusicData()

  // DEBUG: Log what data the component is actually receiving
  console.log('🎵 MusicDetail received data from store:', musicData)
  console.log(
    '🎵 MusicDetail conversation_starters:',
    musicData.conversation_starters,
  )
  console.log('🎵 MusicDetail fun_fact:', musicData.fun_fact)

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
            <FeedbackButtons
              onFeedback={onFeedback}
              itemName={`${musicData.artist} - ${musicData.piece_title}`}
              category='music'
              size='default'
            />
          </div>

          <div className='mb-8'>
            <h3 className='text-3xl font-medium text-gray-800 mb-2'>
              {musicData.artist || 'Loading artist...'}
            </h3>
            <p className='text-2xl text-gray-600'>
              {musicData.piece_title || 'Loading piece...'}
            </p>
          </div>

          {/* YouTube Video */}
          <div className='mb-8'>
            {musicData.youtube_embed ? (
              <iframe
                width='100%'
                height='400'
                src={musicData.youtube_embed}
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
            <p className='text-center mt-2 text-gray-500 text-sm'>
              This work is licensed under a Creative Commons license
            </p>
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
              {musicData.conversation_starters &&
              musicData.conversation_starters.length > 0 ? (
                musicData.conversation_starters.map((starter, index) => (
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
          {musicData.fun_fact && (
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
                {musicData.fun_fact}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MusicDetail
