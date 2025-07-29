import React from 'react'
import FeedbackButtons from './FeedbackButtons'
import dashboardDataStore from '../services/dashboardDataStore'

// Import all images for safety
import birthdayImage from '../static/images/birthday.png'
import clothingImage from '../static/images/clothing.png'
import familyImage from '../static/images/family.png'
import foodImage from '../static/images/food.png'
import holidaysImage from '../static/images/holidays.png'
import musicImage from '../static/images/music.png'
import petsImage from '../static/images/pets.png'
import schoolImage from '../static/images/school.png'
import seasonsImage from '../static/images/seasons.png'
import travelImage from '../static/images/travel.png'
import weatherImage from '../static/images/weather.png'

const PhotoDetail = ({ onBack, onFeedback }) => {
  // Get photo data directly from global store instead of props
  const photoData = dashboardDataStore.getPhotoData()

  // More comprehensive image mapping with better fallback logic
  const imageMap = {
    // With .png extension
    'birthday.png': birthdayImage,
    'clothing.png': clothingImage,
    'family.png': familyImage,
    'food.png': foodImage,
    'holidays.png': holidaysImage,
    'music.png': musicImage,
    'pets.png': petsImage,
    'school.png': schoolImage,
    'seasons.png': seasonsImage,
    'travel.png': travelImage,
    'weather.png': weatherImage,
    // Without .png extension
    birthday: birthdayImage,
    clothing: clothingImage,
    family: familyImage,
    food: foodImage,
    holidays: holidaysImage,
    music: musicImage,
    pets: petsImage,
    school: schoolImage,
    seasons: seasonsImage,
    travel: travelImage,
    weather: weatherImage,
    // Common variations
    Family: familyImage,
    Food: foodImage,
    Travel: travelImage,
    Birthday: birthdayImage,
    Holidays: holidaysImage,
    Music: musicImage,
    Pets: petsImage,
    School: schoolImage,
    Seasons: seasonsImage,
    Clothing: clothingImage,
    Weather: weatherImage,
  }

  // Improved getImage function with better matching logic
  const getImage = filename => {
    if (!filename) {
      return {
        src: weatherImage,
        name: 'Surprise Photo',
        description:
          'A beautiful surprise scene with lovely colors and interesting details to explore together.',
      }
    }

    // Try multiple variations of the filename
    const variations = [
      filename, // exact match: "family.png"
      filename.toLowerCase(), // lowercase: "family.png"
      filename.toLowerCase().replace('.png', ''), // no extension: "family"
      filename.replace('.png', ''), // no extension, original case: "Family"
      filename.charAt(0).toUpperCase() + filename.slice(1).toLowerCase(), // Title case: "Family"
    ]

    // Try each variation
    for (const variation of variations) {
      if (imageMap[variation]) {
        return {
          src: imageMap[variation],
          name:
            filename.replace('.png', '').charAt(0).toUpperCase() +
            filename.replace('.png', '').slice(1),
          description:
            photoData.description ||
            'A meaningful photo chosen especially for today.',
        }
      }
    }

    // Complete fallback
    return {
      src: weatherImage,
      name: 'Surprise Photo',
      description:
        'A beautiful surprise scene with lovely colors and interesting details to explore together.',
    }
  }

  const currentImage = getImage(photoData.filename)

  // Generate fallback conversation starters if none provided
  const getFallbackConversationStarters = () => [
    'What colors do you see in this picture?',
    'Does anything in this photo look familiar to you?',
    'What part of the picture draws your attention?',
    'How does this picture make you feel?',
    "Does this remind you of any places you've been?",
  ]

  // Use the correct field from the response object
  const conversationStarters =
    photoData.conversation_starters &&
    photoData.conversation_starters.length > 0
      ? photoData.conversation_starters
      : photoData.conversationStarters &&
        photoData.conversationStarters.length > 0
      ? photoData.conversationStarters
      : getFallbackConversationStarters()

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
            <FeedbackButtons
              onFeedback={onFeedback}
              itemName={photoData.filename || 'Photo of the Day'}
              category='photo'
              size='default'
            />
          </div>

          {/* Photo Display */}
          <div className='mb-8'>
            <div className='w-full h-96 rounded-lg overflow-hidden border-2 border-gray-200 bg-gray-100'>
              <img
                src={currentImage.src}
                alt={currentImage.name}
                className='w-full h-full object-cover'
                onError={e => {
                  // Fallback to weather image if the image fails to load
                  e.target.src = weatherImage
                }}
              />
            </div>
            <p className='text-center mt-4 text-gray-600 text-lg font-medium'>
              {currentImage.name}
            </p>
            {/* Creative Commons License Attribution */}
            <p className='text-center mt-2 text-gray-500 text-sm'>
              This work is licensed under a Creative Commons license
            </p>
          </div>

          {/* Dementia-Friendly Instructions */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              Let's Look at This Photo Together
            </h4>
            <div
              className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
              style={{ backgroundColor: '#E8F4FD', borderColor: '#8B7CB6' }}
            >
              <p className='mb-4'>
                <strong>Take your time looking at this picture.</strong> You can
                look at it quietly, point to things that interest you, or share
                any thoughts you'd like.
              </p>
              <p className='mb-4'>
                Notice the colors, shapes, and details. Sometimes pictures can
                bring back memories or feelings - that's perfectly normal.
              </p>
              <p>
                There's no need to answer questions or explain anything. Just
                enjoy looking and experiencing whatever comes to mind.
              </p>
            </div>
          </div>

          {/* Photo Description Display */}
          <div className='mb-8'>
            <h4
              className='text-2xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              Photo Description
            </h4>
            <div
              className='text-gray-700 text-lg leading-relaxed p-6 rounded-lg border-2'
              style={{ backgroundColor: '#F8F6FF', borderColor: '#A8B5A0' }}
            >
              {/* Clean up the description by removing unwanted text */}
              {photoData.description
                ? photoData.description
                    .replace(
                      /Here's a description a caregiver could read to a senior with dementia[,:]?\s*/gi,
                      '',
                    )
                    .replace(/^["']|["']$/g, '')
                    .replace(/\\"/g, '"')
                    .trim()
                : currentImage.description}
            </div>
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
              {conversationStarters.map((starter, index) => (
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
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PhotoDetail
