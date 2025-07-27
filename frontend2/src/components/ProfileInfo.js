import React from 'react'

const Profile = ({
  patientProfile,
  feedback,
  feedbackSummary,
  onBack,
  onClearFeedback,
}) => {
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
          {/* Patient Profile Section */}
          <div className='mb-8'>
            <h2
              className='text-3xl font-light mb-6'
              style={{ color: '#4A4A4A' }}
            >
              Patient Profile
            </h2>
            <div className='grid md:grid-cols-2 gap-6'>
              <div className='space-y-4'>
                <div>
                  <label className='text-sm font-medium text-gray-600'>
                    Name
                  </label>
                  <p className='text-lg text-gray-800'>
                    {patientProfile?.first_name} {patientProfile?.last_name}
                  </p>
                </div>
                <div>
                  <label className='text-sm font-medium text-gray-600'>
                    Age
                  </label>
                  <p className='text-lg text-gray-800'>
                    {patientProfile?.current_age} years old
                  </p>
                </div>
                <div>
                  <label className='text-sm font-medium text-gray-600'>
                    Cultural Heritage
                  </label>
                  <p className='text-lg text-gray-800'>
                    {patientProfile?.cultural_heritage}
                  </p>
                </div>
              </div>
              <div className='space-y-4'>
                <div>
                  <label className='text-sm font-medium text-gray-600'>
                    Location
                  </label>
                  <p className='text-lg text-gray-800'>
                    {patientProfile?.city}, {patientProfile?.state}
                  </p>
                </div>
                <div>
                  <label className='text-sm font-medium text-gray-600'>
                    Birth Year
                  </label>
                  <p className='text-lg text-gray-800'>
                    {patientProfile?.birth_year}
                  </p>
                </div>
                <div>
                  <label className='text-sm font-medium text-gray-600'>
                    Interests
                  </label>
                  <p className='text-lg text-gray-800'>
                    {patientProfile?.interests?.join(', ')}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Feedback Summary */}
          {feedbackSummary && (
            <div className='mb-8 p-4 bg-gray-50 rounded-lg'>
              <h3 className='text-lg font-medium text-gray-800 mb-2'>
                Feedback Summary
              </h3>
              <div className='grid grid-cols-3 gap-4 text-center'>
                <div>
                  <div className='text-2xl font-bold text-gray-700'>
                    {feedbackSummary.totalFeedback}
                  </div>
                  <div className='text-sm text-gray-600'>Total Feedback</div>
                </div>
                <div>
                  <div className='text-2xl font-bold text-green-600'>
                    {feedbackSummary.likes}
                  </div>
                  <div className='text-sm text-gray-600'>Likes</div>
                </div>
                <div>
                  <div className='text-2xl font-bold text-red-600'>
                    {feedbackSummary.dislikes}
                  </div>
                  <div className='text-sm text-gray-600'>Dislikes</div>
                </div>
              </div>
            </div>
          )}

          {/* Feedback Section */}
          <div>
            <div className='flex justify-between items-center mb-6'>
              <h3 className='text-2xl font-light' style={{ color: '#4A4A4A' }}>
                Collected Feedback
              </h3>
              {feedback &&
                (feedback.likes?.length > 0 ||
                  feedback.dislikes?.length > 0) && (
                  <button
                    onClick={onClearFeedback}
                    className='px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors'
                  >
                    Clear All Feedback
                  </button>
                )}
            </div>

            <div className='grid md:grid-cols-2 gap-6'>
              {/* Likes */}
              <div>
                <h4 className='text-lg font-medium text-green-700 mb-4 flex items-center'>
                  <span className='mr-2'>👍</span>
                  Likes ({feedback?.likes?.length || 0})
                </h4>
                <div className='space-y-2 max-h-60 overflow-y-auto'>
                  {feedback?.likes?.length ? (
                    feedback.likes.map((like, index) => (
                      <div
                        key={index}
                        className='p-3 bg-green-50 border border-green-200 rounded-lg'
                      >
                        <p className='text-sm font-medium text-green-800 capitalize'>
                          {like.category}
                        </p>
                        <p className='text-sm text-green-700'>{like.item}</p>
                        <p className='text-xs text-green-600'>
                          {new Date(like.timestamp).toLocaleString()}
                        </p>
                      </div>
                    ))
                  ) : (
                    <div className='p-4 text-center text-gray-500 italic border-2 border-dashed border-gray-200 rounded-lg'>
                      No likes collected yet
                    </div>
                  )}
                </div>
              </div>

              {/* Dislikes */}
              <div>
                <h4 className='text-lg font-medium text-red-700 mb-4 flex items-center'>
                  <span className='mr-2'>👎</span>
                  Dislikes ({feedback?.dislikes?.length || 0})
                </h4>
                <div className='space-y-2 max-h-60 overflow-y-auto'>
                  {feedback?.dislikes?.length ? (
                    feedback.dislikes.map((dislike, index) => (
                      <div
                        key={index}
                        className='p-3 bg-red-50 border border-red-200 rounded-lg'
                      >
                        <p className='text-sm font-medium text-red-800 capitalize'>
                          {dislike.category}
                        </p>
                        <p className='text-sm text-red-700'>{dislike.item}</p>
                        <p className='text-xs text-red-600'>
                          {new Date(dislike.timestamp).toLocaleString()}
                        </p>
                      </div>
                    ))
                  ) : (
                    <div className='p-4 text-center text-gray-500 italic border-2 border-dashed border-gray-200 rounded-lg'>
                      No dislikes collected yet
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Category Breakdown */}
            {feedbackSummary?.categories &&
              Object.keys(feedbackSummary.categories).length > 0 && (
                <div className='mt-8'>
                  <h4 className='text-lg font-medium text-gray-700 mb-4'>
                    Feedback by Category
                  </h4>
                  <div className='grid grid-cols-2 md:grid-cols-4 gap-4'>
                    {Object.entries(feedbackSummary.categories).map(
                      ([category, counts]) => (
                        <div
                          key={category}
                          className='p-3 bg-gray-50 rounded-lg text-center'
                        >
                          <div className='text-sm font-medium text-gray-800 capitalize mb-1'>
                            {category}
                          </div>
                          <div className='flex justify-center space-x-4 text-xs'>
                            <span className='text-green-600'>
                              👍 {counts.likes}
                            </span>
                            <span className='text-red-600'>
                              👎 {counts.dislikes}
                            </span>
                          </div>
                        </div>
                      ),
                    )}
                  </div>
                </div>
              )}

            {/* No feedback message */}
            {(!feedback ||
              (feedback.likes?.length === 0 &&
                feedback.dislikes?.length === 0)) && (
              <div className='text-center py-8'>
                <div className='text-6xl mb-4'>📝</div>
                <h4 className='text-xl text-gray-600 mb-2'>
                  No feedback collected yet
                </h4>
                <p className='text-gray-500'>
                  Start interacting with the dashboard content to collect
                  feedback automatically.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
