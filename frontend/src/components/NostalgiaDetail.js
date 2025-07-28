import React from 'react'
import FeedbackButtons from './FeedbackButtons'
import dashboardDataStore from '../services/dashboardDataStore'

const NostalgiaDetail = ({ onBack, onFeedback }) => {
  // Get nostalgia data directly from global store instead of props
  const nostalgiaData = dashboardDataStore.getNostalgiaData()
  const patientInfo = dashboardDataStore.getPatientInfo()

  // DEBUG: Log what data the component is actually receiving
  console.log('📰 NostalgiaDetail received data from store:', nostalgiaData)

  // Extract sections from the complex nostalgia structure
  const sections = nostalgiaData.sections || {}

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
                  style={{ backgroundColor: '#8B7CB6' }}
                ></div>
              </div>
              <h2 className='text-4xl font-light' style={{ color: '#4A4A4A' }}>
                Today's Nostalgia News
              </h2>
            </div>

            {/* Feedback buttons */}
            <FeedbackButtons
              onFeedback={onFeedback}
              itemName={nostalgiaData.title || 'Nostalgia News'}
              category='nostalgia'
              size='default'
            />
          </div>

          <div className='mb-8'>
            <h3 className='text-3xl font-medium text-gray-800 mb-2'>
              {nostalgiaData.title || "Today's Special News"}
            </h3>
            <p className='text-xl text-gray-600 mb-6'>
              {nostalgiaData.subtitle ||
                `Personalized for ${patientInfo.name || 'you'}`}
            </p>
          </div>

          <div className='space-y-8'>
            {/* Memory Spotlight Section */}
            {sections.memory_spotlight && (
              <div
                className='p-6 rounded-lg border-2'
                style={{ backgroundColor: '#F0F0F0', borderColor: '#A8B5A0' }}
              >
                <h4
                  className='text-2xl font-medium mb-4'
                  style={{ color: '#4A4A4A' }}
                >
                  {sections.memory_spotlight.headline || '📚 Memory Spotlight'}
                </h4>
                <p className='text-gray-700 text-lg leading-relaxed mb-4'>
                  {sections.memory_spotlight.content}
                </p>
                {sections.memory_spotlight.fun_fact && (
                  <p className='text-sm text-gray-600 italic'>
                    💡 {sections.memory_spotlight.fun_fact}
                  </p>
                )}
              </div>
            )}

            {/* Era Highlights Section */}
            {sections.era_highlights && (
              <div
                className='p-6 rounded-lg border-2'
                style={{ backgroundColor: '#F5F3FF', borderColor: '#8B7CB6' }}
              >
                <h4
                  className='text-2xl font-medium mb-4'
                  style={{ color: '#4A4A4A' }}
                >
                  {sections.era_highlights.headline || '🎵 Era Highlights'}
                </h4>
                <p className='text-gray-700 text-lg leading-relaxed mb-4'>
                  {sections.era_highlights.content}
                </p>
                {sections.era_highlights.fun_fact && (
                  <p className='text-sm text-gray-600 italic'>
                    💡 {sections.era_highlights.fun_fact}
                  </p>
                )}
              </div>
            )}

            {/* Heritage Traditions Section */}
            {sections.heritage_traditions && (
              <div
                className='p-6 rounded-lg border-2'
                style={{ backgroundColor: '#FFF8E7', borderColor: '#D4A574' }}
              >
                <h4
                  className='text-2xl font-medium mb-4'
                  style={{ color: '#4A4A4A' }}
                >
                  {sections.heritage_traditions.headline ||
                    '🏛️ Heritage Traditions'}
                </h4>
                <p className='text-gray-700 text-lg leading-relaxed mb-4'>
                  {sections.heritage_traditions.content}
                </p>
                {sections.heritage_traditions.fun_fact && (
                  <p className='text-sm text-gray-600 italic'>
                    💡 {sections.heritage_traditions.fun_fact}
                  </p>
                )}
              </div>
            )}

            {/* Conversation Starters Section */}
            {sections.conversation_starters &&
              sections.conversation_starters.questions && (
                <div>
                  <h4
                    className='text-2xl font-medium mb-6'
                    style={{ color: '#4A4A4A' }}
                  >
                    {sections.conversation_starters.headline ||
                      '💭 Conversation Corner'}
                  </h4>
                  <ul className='space-y-4'>
                    {sections.conversation_starters.questions.map(
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
                    )}
                  </ul>
                </div>
              )}

            {/* Fallback if no sections available */}
            {Object.keys(sections).length === 0 && (
              <div
                className='p-6 rounded-lg border-2'
                style={{ backgroundColor: '#F5F3FF', borderColor: '#8B7CB6' }}
              >
                <h4
                  className='text-2xl font-medium mb-4'
                  style={{ color: '#4A4A4A' }}
                >
                  ✨ Today's Special Story
                </h4>
                <p className='text-gray-700 text-lg leading-relaxed'>
                  {nostalgiaData.content ||
                    `Today is a wonderful day filled with beautiful memories and meaningful moments, ${
                      patientInfo.name || 'friend'
                    }!`}
                </p>
              </div>
            )}

            {/* Themes Section */}
            {nostalgiaData.themes && nostalgiaData.themes.length > 0 && (
              <div
                className='p-4 rounded-lg'
                style={{ backgroundColor: '#F8F6FF' }}
              >
                <h5
                  className='text-lg font-medium mb-2'
                  style={{ color: '#4A4A4A' }}
                >
                  Today's Themes:
                </h5>
                <div className='flex flex-wrap gap-2'>
                  {nostalgiaData.themes.map((theme, index) => (
                    <span
                      key={index}
                      className='px-3 py-1 rounded-full text-sm font-medium'
                      style={{ backgroundColor: '#8B7CB6', color: 'white' }}
                    >
                      {theme}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default NostalgiaDetail
