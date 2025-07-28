import React, { useState } from 'react'

const FeedbackButtons = ({
  onFeedback,
  itemName,
  category,
  size = 'default', // 'small' for dashboard, 'default' for detail pages
}) => {
  const [feedbackGiven, setFeedbackGiven] = useState(null)

  const handleLike = () => {
    if (feedbackGiven !== 'like') {
      setFeedbackGiven('like')
      if (onFeedback) {
        onFeedback('like', itemName, category)
      }
    }
  }

  const handleDislike = () => {
    if (feedbackGiven !== 'dislike') {
      setFeedbackGiven('dislike')
      if (onFeedback) {
        onFeedback('dislike', itemName, category)
      }
    }
  }

  // Small size for dashboard tiles
  if (size === 'small') {
    return (
      <div className='flex space-x-3'>
        <button
          onClick={handleLike}
          disabled={feedbackGiven === 'like'}
          className={`min-h-12 min-w-12 flex items-center justify-center rounded-lg transition-all ${
            feedbackGiven === 'like'
              ? 'bg-green-600 text-white cursor-default'
              : feedbackGiven === 'dislike'
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-green-100 hover:bg-green-200 text-green-700 hover:scale-110'
          }`}
        >
          <span className='text-2xl'>
            {feedbackGiven === 'like' ? '✅' : '👍'}
          </span>
        </button>
        <button
          onClick={handleDislike}
          disabled={feedbackGiven === 'dislike'}
          className={`min-h-12 min-w-12 flex items-center justify-center rounded-lg transition-all ${
            feedbackGiven === 'dislike'
              ? 'bg-red-600 text-white cursor-default'
              : feedbackGiven === 'like'
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-red-100 hover:bg-red-200 text-red-700 hover:scale-110'
          }`}
        >
          <span className='text-2xl'>
            {feedbackGiven === 'dislike' ? '❌' : '👎'}
          </span>
        </button>
      </div>
    )
  }

  // Default size for detail pages
  return (
    <div className='flex space-x-3'>
      <button
        onClick={handleLike}
        disabled={feedbackGiven === 'like'}
        className={`px-4 py-2 rounded-lg transition-all flex items-center space-x-2 ${
          feedbackGiven === 'like'
            ? 'bg-green-600 text-white cursor-default'
            : feedbackGiven === 'dislike'
            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
            : 'bg-green-100 hover:bg-green-200 text-green-700'
        }`}
      >
        <span className='text-lg'>
          {feedbackGiven === 'like' ? '✅' : '👍'}
        </span>
        <span className='font-medium'>
          {feedbackGiven === 'like' ? 'Liked' : 'Like'}
        </span>
      </button>
      <button
        onClick={handleDislike}
        disabled={feedbackGiven === 'dislike'}
        className={`px-4 py-2 rounded-lg transition-all flex items-center space-x-2 ${
          feedbackGiven === 'dislike'
            ? 'bg-red-600 text-white cursor-default'
            : feedbackGiven === 'like'
            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
            : 'bg-red-100 hover:bg-red-200 text-red-700'
        }`}
      >
        <span className='text-lg'>
          {feedbackGiven === 'dislike' ? '❌' : '👎'}
        </span>
        <span className='font-medium'>
          {feedbackGiven === 'dislike' ? 'Disliked' : 'Dislike'}
        </span>
      </button>
    </div>
  )
}

export default FeedbackButtons
