import React from 'react'

const RecipeDetail = ({ data, onBack, onFeedback }) => {
  const recipeData = data || {}

  const handleLike = () => {
    if (onFeedback) {
      onFeedback('like', recipeData.name, 'recipe')
    }
  }

  const handleDislike = () => {
    if (onFeedback) {
      onFeedback('dislike', recipeData.name, 'recipe')
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
                style={{ backgroundColor: '#C4916B' }}
              ></div>
              <h2 className='text-4xl font-light' style={{ color: '#4A4A4A' }}>
                Today's Recipe
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
              {recipeData.name || 'Loading recipe...'}
            </h3>
            <p className='text-xl text-gray-600'>
              {recipeData.description || 'A comforting dish'}
            </p>
          </div>

          <div className='grid md:grid-cols-2 gap-8 mb-8'>
            {/* Ingredients */}
            <div>
              <h4
                className='text-2xl font-medium mb-6'
                style={{ color: '#4A4A4A' }}
              >
                🥘 Ingredients
              </h4>
              <ul className='space-y-3'>
                {recipeData.ingredients && recipeData.ingredients.length > 0 ? (
                  recipeData.ingredients.map((ingredient, index) => (
                    <li
                      key={index}
                      className='text-gray-700 text-lg p-3 rounded border'
                      style={{ backgroundColor: '#F0F0F0' }}
                    >
                      {ingredient}
                    </li>
                  ))
                ) : (
                  <li className='text-gray-500 text-lg p-3 rounded border border-dashed border-gray-300'>
                    Ingredients loading...
                  </li>
                )}
              </ul>
            </div>

            {/* Instructions */}
            <div>
              <h4
                className='text-2xl font-medium mb-6'
                style={{ color: '#4A4A4A' }}
              >
                👩‍🍳 Instructions
              </h4>
              <ol className='space-y-3'>
                {recipeData.instructions &&
                recipeData.instructions.length > 0 ? (
                  recipeData.instructions.map((instruction, index) => (
                    <li
                      key={index}
                      className='text-gray-700 text-lg p-3 rounded border'
                      style={{ backgroundColor: '#F0F0F0' }}
                    >
                      <span className='font-medium text-gray-800'>
                        {index + 1}.
                      </span>{' '}
                      {instruction}
                    </li>
                  ))
                ) : (
                  <li className='text-gray-500 text-lg p-3 rounded border border-dashed border-gray-300'>
                    Instructions loading...
                  </li>
                )}
              </ol>
            </div>
          </div>

          {/* Cultural Context */}
          {recipeData.culturalContext && (
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
                {recipeData.culturalContext}
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
              {recipeData.conversationQuestions &&
              recipeData.conversationQuestions.length > 0 ? (
                recipeData.conversationQuestions.map((question, index) => (
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

export default RecipeDetail
