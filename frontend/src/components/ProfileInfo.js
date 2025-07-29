import React, { useState, useEffect } from 'react'
import apiService from '../services/apiService'
import feedbackManager from '../utils/feedbackManager'

const Profile = ({ onBack, patientProfile, onProfileUpdate }) => {
  const [isLocked, setIsLocked] = useState(true)
  const [showAdmin, setShowAdmin] = useState(false)
  const [formData, setFormData] = useState({
    first_name: '',
    birth_year: '',
    cultural_heritage: '',
    cultural_heritage_2: '',
    cultural_heritage_3: '',
    city: '',
    state: '',
    interests: '',
    additional_info: '',
  })
  const [feedback, setFeedback] = useState({ likes: [], dislikes: [] })

  // Initialize form data from patientProfile
  useEffect(() => {
    if (patientProfile) {
      setFormData({
        first_name: patientProfile.first_name || '',
        birth_year: patientProfile.birth_year || '',
        cultural_heritage: patientProfile.cultural_heritage || '',
        cultural_heritage_2: patientProfile.cultural_heritage_2 || '',
        cultural_heritage_3: patientProfile.cultural_heritage_3 || '',
        city: patientProfile.city || '',
        state: patientProfile.state || '',
        interests: Array.isArray(patientProfile.interests)
          ? patientProfile.interests.join(', ')
          : patientProfile.interests || '',
        additional_info: '',
      })
    }
  }, [patientProfile])

  // Load feedback data
  useEffect(() => {
    const currentFeedback = feedbackManager.getFeedback()
    setFeedback(currentFeedback)
  }, [])

  const handleUnlock = () => {
    setIsLocked(false)
  }

  const handleAdminToggle = () => {
    setShowAdmin(!showAdmin)
  }

  const handleInputChange = (field, value) => {
    if (!isLocked) {
      setFormData(prev => ({
        ...prev,
        [field]: value,
      }))
    }
  }

  const handleSave = async () => {
    try {
      // Create updated patient profile
      const updatedProfile = {
        first_name: formData.first_name,
        birth_year:
          parseInt(formData.birth_year) || new Date().getFullYear() - 80,
        cultural_heritage: formData.cultural_heritage || 'American', // Defaults to American
        cultural_heritage_2: formData.cultural_heritage_2, // Stored locally only
        cultural_heritage_3: formData.cultural_heritage_3, // Stored locally only
        city: formData.city || '',
        state: formData.state || '',
        interests: formData.interests
          .split(',')
          .map(i => i.trim())
          .filter(i => i), // Properly converted to array
      }

      // Call parent component to update profile
      if (onProfileUpdate) {
        await onProfileUpdate(updatedProfile)
      }

      setIsLocked(true)
      alert('Profile updated successfully!')
    } catch (error) {
      console.error('Failed to save profile:', error)
      alert('Failed to save profile. Please try again.')
    }
  }

  const handleRefresh = async () => {
    if (
      window.confirm(
        'This will refresh the dashboard and current content will be lost. Continue?',
      )
    ) {
      try {
        // Get current feedback
        const currentFeedback = feedbackManager.formatForAPI()

        // Clear cache and refresh dashboard
        await apiService.refreshDashboard(patientProfile, currentFeedback)

        alert('Dashboard refreshed successfully!')

        // Navigate back to dashboard to see changes
        onBack()
      } catch (error) {
        console.error('Failed to refresh dashboard:', error)
        alert('Failed to refresh dashboard. Please try again.')
      }
    }
  }

  // Mock feedback with real data from feedbackManager for Demo purposes
  const mockFeedback =
    feedback.likes.length > 0 || feedback.dislikes.length > 0
      ? feedback
      : {
          likes: [
            {
              category: 'music',
              item: 'Frank Sinatra - The Way You Look Tonight',
              timestamp: new Date(Date.now() - 86400000),
            },
            {
              category: 'recipe',
              item: 'Italian Wedding Soup',
              timestamp: new Date(Date.now() - 172800000),
            },
            {
              category: 'photo',
              item: 'Vintage Italian Market',
              timestamp: new Date(Date.now() - 259200000),
            },
          ],
          dislikes: [
            {
              category: 'recipe',
              item: 'Scrambled Eggs with Tomato and Mozzarella',
              timestamp: new Date(Date.now() - 345600000),
            },
          ],
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
          {/* Profile Header */}
          <div className='flex items-center mb-6'>
            <div
              className='w-8 h-8 rounded-full mr-4'
              style={{ backgroundColor: '#D4A574' }}
            ></div>
            <h2 className='text-3xl font-light' style={{ color: '#4A4A4A' }}>
              Patient Profile
            </h2>
          </div>

          {/* Privacy Notice */}
          <div
            className='mb-8 p-4 rounded-lg border-2 border-blue-200'
            style={{ backgroundColor: '#F0F8FF' }}
          >
            <div className='flex items-start'>
              <svg
                className='w-6 h-6 mr-3 mt-1 text-blue-600'
                fill='currentColor'
                viewBox='0 0 24 24'
              >
                <path d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z' />
              </svg>
              <div>
                <h4 className='font-medium text-blue-800 mb-2'>
                  Privacy-First Technology
                </h4>
                <p className='text-sm text-blue-700'>
                  LumiCue uses Qloo's advanced AI that creates personalized
                  recommendations without collecting or storing personal
                  identifiable information (PII). Personal information stays
                  completely private and safe. Details like names or birth years
                  are only used on the device itself to create a better
                  experience - this information never leaves the device or gets
                  sent to any outside companies. Instead, we transform this into
                  anonymous categories (like "Italian-American heritage" or
                  "senior age group") to find the right music, recipes, and
                  photos. Think of it like telling a librarian you enjoy mystery
                  books without sharing your name - they can still recommend
                  great books! Our technology focuses on cultural connections
                  rather than personal details, keeping your information exactly
                  where it belongs - private and secure on your device.
                </p>
              </div>
            </div>
          </div>

          {/* Profile Form */}
          <div className='mb-8'>
            <h3
              className='text-xl font-medium mb-6'
              style={{ color: '#4A4A4A' }}
            >
              Profile Information
            </h3>

            {/* Required Fields */}
            <div className='mb-6'>
              <h4 className='text-lg font-medium mb-4 text-gray-800'>
                Required Information
              </h4>
              <div className='grid md:grid-cols-2 gap-6'>
                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    First Name or Nickname{' '}
                    <span className='text-red-500'>*</span>
                  </label>
                  <input
                    type='text'
                    value={formData.first_name}
                    onChange={e =>
                      handleInputChange('first_name', e.target.value)
                    }
                    disabled={isLocked}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                </div>

                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    Year of Birth <span className='text-red-500'>*</span>
                  </label>
                  <input
                    type='number'
                    value={formData.birth_year}
                    onChange={e =>
                      handleInputChange('birth_year', e.target.value)
                    }
                    disabled={isLocked}
                    min='1920'
                    max={new Date().getFullYear()}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                </div>
              </div>
            </div>

            {/* Optional Cultural Identity */}
            <div className='mb-6'>
              <h4 className='text-lg font-medium mb-4 text-gray-800'>
                Cultural Identity{' '}
                <span className='text-sm text-gray-500 font-normal'>
                  (Optional but helpful)
                </span>
              </h4>
              <div className='grid md:grid-cols-3 gap-4'>
                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    Primary Identity
                  </label>
                  <input
                    type='text'
                    value={formData.cultural_heritage}
                    onChange={e =>
                      handleInputChange('cultural_heritage', e.target.value)
                    }
                    placeholder='e.g., Italian-American'
                    disabled={isLocked}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                  <p className='text-xs text-gray-500 mt-1'>Primary identity</p>
                </div>

                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    Secondary Identity
                  </label>
                  <input
                    type='text'
                    value={formData.cultural_heritage_2}
                    onChange={e =>
                      handleInputChange('cultural_heritage_2', e.target.value)
                    }
                    placeholder='e.g., Irish'
                    disabled={isLocked}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                  <p className='text-xs text-gray-500 mt-1'>
                    Secondary identity
                  </p>
                </div>

                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    Additional Identity
                  </label>
                  <input
                    type='text'
                    value={formData.cultural_heritage_3}
                    onChange={e =>
                      handleInputChange('cultural_heritage_3', e.target.value)
                    }
                    placeholder='e.g., German'
                    disabled={isLocked}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                  <p className='text-xs text-gray-500 mt-1'>
                    Additional identity
                  </p>
                </div>
              </div>
            </div>

            {/* Optional Location */}
            <div className='mb-6'>
              <h4 className='text-lg font-medium mb-4 text-gray-800'>
                Location{' '}
                <span className='text-sm text-gray-500 font-normal'>
                  (Optional)
                </span>
              </h4>
              <div className='grid md:grid-cols-2 gap-6'>
                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    City
                  </label>
                  <input
                    type='text'
                    value={formData.city}
                    onChange={e => handleInputChange('city', e.target.value)}
                    placeholder='e.g., Brooklyn'
                    disabled={isLocked}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                </div>

                <div>
                  <label className='block text-sm font-medium text-gray-700 mb-2'>
                    State
                  </label>
                  <input
                    type='text'
                    value={formData.state}
                    onChange={e => handleInputChange('state', e.target.value)}
                    placeholder='e.g., New York'
                    disabled={isLocked}
                    className={`w-full p-3 rounded-lg border-2 ${
                      isLocked
                        ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                        : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                    }`}
                  />
                </div>
              </div>
            </div>

            {/* Optional Interests */}
            <div className='mb-6'>
              <h4 className='text-lg font-medium mb-4 text-gray-800'>
                Known Interests{' '}
                <span className='text-sm text-gray-500 font-normal'>
                  (Optional but helpful)
                </span>
              </h4>
              <div>
                <input
                  type='text'
                  value={formData.interests}
                  onChange={e => handleInputChange('interests', e.target.value)}
                  placeholder='cooking, music, family, gardening (comma separated)'
                  disabled={isLocked}
                  className={`w-full p-3 rounded-lg border-2 ${
                    isLocked
                      ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                      : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                  }`}
                />
                <p className='text-xs text-gray-500 mt-1'>
                  Separate multiple interests with commas
                </p>
              </div>
            </div>

            {/* Additional Information */}
            <div className='mb-6'>
              <h4 className='text-lg font-medium mb-4 text-gray-800'>
                Additional Information
              </h4>
              <div>
                <label className='block text-sm font-medium text-gray-700 mb-2'>
                  Anything else you want to share
                </label>
                <textarea
                  rows='3'
                  value={formData.additional_info}
                  onChange={e =>
                    handleInputChange('additional_info', e.target.value)
                  }
                  placeholder='Additional information that might help personalize the experience...'
                  disabled={isLocked}
                  className={`w-full p-3 rounded-lg border-2 ${
                    isLocked
                      ? 'bg-gray-50 text-gray-600 cursor-not-allowed'
                      : 'bg-white border-gray-300 focus:border-blue-500 focus:outline-none'
                  }`}
                />
              </div>
            </div>

            {/* Save Button (only show when unlocked) */}
            {!isLocked && (
              <div className='mt-6'>
                <button
                  onClick={handleSave}
                  className='px-6 py-3 rounded-lg font-medium text-white transition-colors min-h-12'
                  style={{ backgroundColor: '#8B7CB6' }}
                >
                  Save Changes
                </button>
              </div>
            )}
          </div>

          <div className='mb-8'>
            <h3
              className='text-xl font-medium mb-4'
              style={{ color: '#4A4A4A' }}
            >
              Feedback History
            </h3>

            {/* Feedback Guidelines */}
            <div
              className='mb-6 p-4 rounded-lg'
              style={{ backgroundColor: '#F8F7ED' }}
            >
              <h4 className='font-medium text-gray-800 mb-2'>
                How to Use Feedback
              </h4>
              <div className='text-sm text-gray-700 space-y-1'>
                <p>
                  <strong>👍 Like:</strong> Did they respond positively? (smile,
                  seem engaged, said they liked it) Click 'Like' to get more
                  content like this.
                </p>
                <p>
                  <strong>👎 Dislike:</strong> Did they not respond positively
                  or seem disinterested? Click 'Dislike' to see less content
                  like this.
                </p>
                <p className='text-xs text-gray-600 mt-2'>
                  Adding feedback helps personalize the experience and improves
                  future recommendations.
                </p>
              </div>
            </div>

            <div className='grid md:grid-cols-2 gap-6'>
              {/* Likes */}
              <div>
                <h4 className='text-lg font-medium text-green-700 mb-4 flex items-center'>
                  <span className='mr-2'>👍</span>
                  Likes ({mockFeedback.likes.length})
                </h4>
                <div className='space-y-2 max-h-48 overflow-y-auto'>
                  {mockFeedback.likes.map((like, index) => (
                    <div
                      key={index}
                      className='p-3 bg-green-50 border border-green-200 rounded-lg'
                    >
                      <p className='text-sm font-medium text-green-800 capitalize'>
                        {like.category}
                      </p>
                      <p className='text-sm text-green-700'>{like.item}</p>
                      <p className='text-xs text-green-600'>
                        {like.timestamp instanceof Date
                          ? like.timestamp.toLocaleDateString()
                          : new Date(like.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Dislikes */}
              <div>
                <h4 className='text-lg font-medium text-red-700 mb-4 flex items-center'>
                  <span className='mr-2'>👎</span>
                  Dislikes ({mockFeedback.dislikes.length})
                </h4>
                <div className='space-y-2 max-h-48 overflow-y-auto'>
                  {mockFeedback.dislikes.map((dislike, index) => (
                    <div
                      key={index}
                      className='p-3 bg-red-50 border border-red-200 rounded-lg'
                    >
                      <p className='text-sm font-medium text-red-800 capitalize'>
                        {dislike.category}
                      </p>
                      <p className='text-sm text-red-700'>{dislike.item}</p>
                      <p className='text-xs text-red-600'>
                        {dislike.timestamp instanceof Date
                          ? dislike.timestamp.toLocaleDateString()
                          : new Date(dislike.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Admin Section - Real App Style (Hidden by default) */}
          <div className='pt-6 border-t border-gray-200'>
            <div className='flex justify-between items-center mb-4'>
              <h3 className='text-xl font-medium' style={{ color: '#4A4A4A' }}>
                {showAdmin ? 'Advanced Settings' : ''}
              </h3>
              <button
                onClick={handleAdminToggle}
                className='flex items-center text-gray-600 hover:text-gray-800 px-3 py-2 rounded transition-colors'
                title='Advanced Settings'
              >
                <svg
                  className='w-5 h-5 mr-2'
                  fill='currentColor'
                  viewBox='0 0 24 24'
                >
                  <path d='M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z' />
                </svg>
                {showAdmin ? 'Hide' : 'Settings'}
              </button>
            </div>

            {showAdmin && (
              <>
                <div className='space-y-4'>
                  <div className='flex items-center justify-between p-4 bg-gray-50 rounded-lg'>
                    <div>
                      <h4 className='font-medium text-gray-800'>
                        Profile Editing
                      </h4>
                      <p className='text-sm text-gray-600'>
                        Unlock profile information for editing
                      </p>
                    </div>
                    <button
                      onClick={handleUnlock}
                      disabled={!isLocked}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${
                        isLocked
                          ? 'bg-blue-600 text-white hover:bg-blue-700'
                          : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                      }`}
                    >
                      {isLocked ? 'Unlock' : 'Unlocked'}
                    </button>
                  </div>

                  <div className='flex items-center justify-between p-4 bg-gray-50 rounded-lg'>
                    <div>
                      <h4 className='font-medium text-gray-800'>
                        Refresh Content
                      </h4>
                      <p className='text-sm text-gray-600'>
                        Generate new personalized recommendations
                      </p>
                    </div>
                    <button
                      onClick={handleRefresh}
                      className='px-4 py-2 rounded-lg font-medium transition-colors text-sm bg-orange-500 text-white hover:bg-orange-600'
                    >
                      Refresh
                    </button>
                  </div>
                </div>

                {!isLocked && (
                  <div className='mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg'>
                    <p className='text-sm text-blue-800'>
                      ✏️ Profile editing is now enabled. Remember to save
                      changes when finished.
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
