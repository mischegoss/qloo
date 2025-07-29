import React from 'react'
import FeedbackButtons from './FeedbackButtons'
import dashboardDataStore from '../services/dashboardDataStore'

const RecipeDetail = ({ onBack, onFeedback }) => {
  // Get recipe data directly from global store instead of props
  const recipeData = dashboardDataStore.getRecipeData()

  // DEBUG: Log what data the component is actually receiving
  console.log('🍽️ RecipeDetail received data from store:', recipeData)
  console.log(
    '🍽️ RecipeDetail conversation_starters:',
    recipeData.conversation_starters,
  )
  console.log('🍽️ RecipeDetail ingredients:', recipeData.ingredients)

  // Emergency fallback recipe
  const fallbackRecipe = {
    name: 'Surprise Warm Apple Treat',
    description: 'A comforting and easy-to-make warm treat',
    ingredients: [
      '1 apple (any kind you have)',
      '1 tablespoon butter',
      '1 tablespoon brown sugar or honey',
      'A pinch of cinnamon (optional)',
    ],
    instructions: [
      'Wash and cut the apple into small pieces',
      'Put apple pieces in a microwave-safe bowl',
      'Add butter and brown sugar on top',
      'Microwave for 2 minutes',
      'Stir gently and add cinnamon if you like',
      'Let cool for 1 minute before enjoying',
    ],
    conversation_starters: [
      "What's your favorite type of apple?",
      'Do you remember making treats like this before?',
      'How does the warm apple smell?',
      'What other simple treats do you enjoy?',
      'Does this remind you of any family recipes?',
    ],
  }

  // Use fallback if data is missing or incomplete
  const currentRecipe =
    !recipeData.name || !recipeData.ingredients || !recipeData.instructions
      ? fallbackRecipe
      : recipeData

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
            <FeedbackButtons
              onFeedback={onFeedback}
              itemName={currentRecipe.name}
              category='recipe'
              size='default'
            />
          </div>

          <div className='mb-8'>
            <h3 className='text-3xl font-medium text-gray-800 mb-2'>
              {currentRecipe.name}
            </h3>
            <p className='text-xl text-gray-600'>{currentRecipe.description}</p>
          </div>

          {/* Dementia-Friendly Instructions */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              Let's Explore This Recipe Together
            </h4>
            <div
              className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
              style={{ backgroundColor: '#E8F4FD', borderColor: '#8B7CB6' }}
            >
              <p className='mb-4'>
                <strong>
                  Food can bring back strong memories and feelings.
                </strong>{' '}
                Read this recipe together and talk about the smells and tastes
                you remember.
              </p>
              <p className='mb-4'>
                If you'd like, you can make this recipe together. All recipes
                use simple ingredients and only need a microwave - safe and easy
                to prepare.
              </p>
              <p>
                Share any memories this food brings up, or simply enjoy reading
                about it together. All ways of responding are welcome!
              </p>
            </div>
          </div>

          {/* Ingredients - Now Full Width */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              🥘 Ingredients
            </h4>
            <ul className='space-y-3'>
              {currentRecipe.ingredients &&
              currentRecipe.ingredients.length > 0 ? (
                currentRecipe.ingredients.map((ingredient, index) => (
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

          {/* Instructions - Now Full Width */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              👩‍🍳 Instructions
            </h4>
            <ol className='space-y-3'>
              {currentRecipe.instructions &&
              currentRecipe.instructions.length > 0 ? (
                currentRecipe.instructions.map((instruction, index) => (
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

          {/* Conversation Starters */}
          <div>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              💬 Optional Conversation Topics
            </h4>
            <ul className='space-y-4'>
              {currentRecipe.conversation_starters &&
              currentRecipe.conversation_starters.length > 0 ? (
                currentRecipe.conversation_starters.map((question, index) => (
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
