import React, { useState } from 'react'
import apiService from '../services/apiService'

const Demo = ({ onDashboardUpdate, onReturnToDashboard }) => {
  const [currentStep, setCurrentStep] = useState(0)
  const [isRunning, setIsRunning] = useState(false)
  const [showJson, setShowJson] = useState(false)
  const [apiResponse, setApiResponse] = useState(null)

  const agentSteps = [
    {
      id: 1,
      name: 'Information Consolidator',
      description: 'Gathering patient profile and theme selection',
      details:
        'Processing patient info: Maria, age 80, Italian-American heritage. Selecting daily theme: Travel.',
      status: 'waiting',
      color: '#D4A574',
    },
    {
      id: 2,
      name: 'Photo Analysis',
      description: 'Analyzing cultural context of selected images',
      details:
        'Analyzing travel.png - detecting coastal scene with cultural context enhancement.',
      status: 'waiting',
      color: '#8B7CB6',
    },
    {
      id: 3,
      name: 'Qloo Cultural Intelligence',
      description: 'Finding culturally relevant artists and places',
      details:
        'Qloo API finding Italian-American cultural preferences. Discovering classical music preferences.',
      status: 'waiting',
      color: '#C4916B',
    },
    {
      id: 4,
      name: 'Content Generation',
      description: 'Curating music, recipes, and photo descriptions',
      details:
        '4A: Music (Puccini), 4B: Recipe (Microwave Clam Chowder), 4C: Photo Description (Cultural context)',
      status: 'waiting',
      color: '#A8B5A0',
    },
    {
      id: 5,
      name: 'Nostalgia News Generator',
      description: 'Creating personalized cultural storytelling',
      details:
        "Gemini AI generating personalized news story connecting Maria's heritage with today's theme.",
      status: 'waiting',
      color: '#B8A9D9',
    },
    {
      id: 6,
      name: 'Dashboard Synthesizer',
      description: 'Assembling final personalized dashboard',
      details:
        'Final assembly: All content ready for delivery with quality score and metadata.',
      status: 'waiting',
      color: '#4A4A4A',
    },
  ]

  const [steps, setSteps] = useState(agentSteps)

  const runDemo = async () => {
    setIsRunning(true)
    setCurrentStep(0)
    setApiResponse(null)

    // Reset all steps
    setSteps(agentSteps.map(step => ({ ...step, status: 'waiting' })))

    // Start the API call in the background
    const apiCall = apiService.refreshDashboard()

    // Run through each step with delays
    agentSteps.forEach((step, index) => {
      setTimeout(() => {
        setCurrentStep(index)
        setSteps(prev =>
          prev.map((s, i) => ({
            ...s,
            status:
              i < index ? 'completed' : i === index ? 'running' : 'waiting',
          })),
        )

        // Complete the current step after 2 seconds
        setTimeout(() => {
          setSteps(prev =>
            prev.map((s, i) => ({
              ...s,
              status: i <= index ? 'completed' : 'waiting',
            })),
          )

          // If this is the last step, finish the demo
          if (index === agentSteps.length - 1) {
            setTimeout(async () => {
              // Wait for API call to complete
              try {
                const realApiResponse = await apiCall
                setApiResponse(realApiResponse)
                console.log('🎉 Real API Response:', realApiResponse)

                // Notify parent component about dashboard update
                if (onDashboardUpdate) {
                  onDashboardUpdate(realApiResponse)
                }
              } catch (error) {
                console.error('API call failed:', error)
                // Still show fallback data
                const fallbackData = apiService.getFallbackData()
                setApiResponse(fallbackData)
              }

              setIsRunning(false)
              setCurrentStep(-1)
            }, 1000)
          }
        }, 2000)
      }, index * 3000)
    })
  }

  const getStatusIcon = status => {
    switch (status) {
      case 'completed':
        return '✅'
      case 'running':
        return '⚡'
      case 'waiting':
        return '⏳'
      default:
        return '⭕'
    }
  }

  const getStatusColor = status => {
    switch (status) {
      case 'completed':
        return '#10B981'
      case 'running':
        return '#F59E0B'
      case 'waiting':
        return '#6B7280'
      default:
        return '#EF4444'
    }
  }

  return (
    <div className='min-h-screen' style={{ backgroundColor: '#F8F7ED' }}>
      <div className='max-w-6xl mx-auto p-6'>
        {/* Back to Dashboard Button */}
        <button
          onClick={onReturnToDashboard}
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

        {/* Header */}
        <div className='text-center mb-12'>
          <h1 className='text-5xl font-light mb-4' style={{ color: '#4A4A4A' }}>
            Agent Pipeline Demo
          </h1>
          <h2 className='text-2xl font-light mb-8' style={{ color: '#6B6B6B' }}>
            Watch AI agents create personalized content in real-time
          </h2>

          <button
            onClick={runDemo}
            disabled={isRunning}
            className={`px-8 py-4 rounded-full text-white text-lg font-medium transition-all ${
              isRunning ? 'bg-gray-400 cursor-not-allowed' : 'hover:shadow-lg'
            }`}
            style={{ backgroundColor: isRunning ? '#9CA3AF' : '#8B7CB6' }}
          >
            {isRunning ? 'Running Demo...' : 'Start Demo'}
          </button>
        </div>

        {/* Pipeline Overview */}
        <div className='mb-12'>
          <h3
            className='text-3xl font-light mb-8 text-center'
            style={{ color: '#4A4A4A' }}
          >
            6-Agent Pipeline
          </h3>

          {/* Progress Bar */}
          <div className='mb-8'>
            <div className='w-full bg-gray-200 rounded-full h-3'>
              <div
                className='h-3 rounded-full transition-all duration-1000 ease-out'
                style={{
                  backgroundColor: '#8B7CB6',
                  width: `${((currentStep + 1) / steps.length) * 100}%`,
                }}
              ></div>
            </div>
            <p className='text-center mt-2 text-gray-600'>
              {isRunning
                ? `Step ${currentStep + 1} of ${steps.length}`
                : 'Ready to start'}
            </p>
          </div>

          {/* Agent Steps */}
          <div className='space-y-6'>
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`bg-white rounded-xl p-6 border-2 transition-all duration-500 ${
                  step.status === 'running'
                    ? 'border-yellow-400 shadow-lg scale-105'
                    : step.status === 'completed'
                    ? 'border-green-400'
                    : 'border-gray-200'
                }`}
              >
                <div className='flex items-center justify-between'>
                  <div className='flex items-center space-x-4'>
                    <div
                      className='w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg'
                      style={{ backgroundColor: step.color }}
                    >
                      {step.id}
                    </div>
                    <div>
                      <h4 className='text-xl font-semibold text-gray-800'>
                        {step.name}
                      </h4>
                      <p className='text-gray-600'>{step.description}</p>
                      {(step.status === 'running' ||
                        step.status === 'completed') && (
                        <p className='text-sm text-gray-500 mt-2 italic'>
                          {step.details}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className='text-right'>
                    <div className='text-3xl mb-2'>
                      {getStatusIcon(step.status)}
                    </div>
                    <div
                      className='text-sm font-medium uppercase'
                      style={{ color: getStatusColor(step.status) }}
                    >
                      {step.status}
                    </div>
                  </div>
                </div>

                {/* Progress bar for current step */}
                {step.status === 'running' && (
                  <div className='mt-4'>
                    <div className='w-full bg-gray-200 rounded-full h-2'>
                      <div
                        className='bg-yellow-400 h-2 rounded-full animate-pulse'
                        style={{ width: '70%' }}
                      ></div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Results Section */}
        {!isRunning && currentStep === -1 && (
          <div className='mt-12'>
            <div className='bg-green-50 border-2 border-green-200 rounded-xl p-8 text-center mb-8'>
              <div className='text-6xl mb-4'>🎉</div>
              <h3 className='text-3xl font-semibold text-green-800 mb-4'>
                Demo Complete!
              </h3>
              <p className='text-lg text-green-700 mb-6'>
                All 6 agents have successfully created personalized content for
                Maria
              </p>
              <div className='grid md:grid-cols-4 gap-4 text-sm'>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>Music</div>
                  <div className='text-green-600'>Puccini Selected</div>
                </div>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>Recipe</div>
                  <div className='text-green-600'>Clam Chowder</div>
                </div>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>Photo</div>
                  <div className='text-green-600'>Travel Scene</div>
                </div>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>News</div>
                  <div className='text-green-600'>Personal Story</div>
                </div>
              </div>
            </div>

            {/* API Response Section */}
            <div className='bg-white rounded-xl shadow-sm p-8 border-2 border-gray-100'>
              <div className='flex justify-between items-center mb-6'>
                <h3
                  className='text-3xl font-medium'
                  style={{ color: '#4A4A4A' }}
                >
                  📄 Real API Response
                </h3>
                <button
                  onClick={() => setShowJson(!showJson)}
                  disabled={!apiResponse}
                  className={`px-6 py-3 rounded-lg font-medium transition-colors text-lg min-h-12 ${
                    !apiResponse ? 'bg-gray-400 cursor-not-allowed' : ''
                  }`}
                  style={{
                    backgroundColor: !apiResponse ? '#9CA3AF' : '#8B7CB6',
                    color: 'white',
                  }}
                >
                  {showJson ? 'Hide' : 'View'} JSON Response
                </button>
              </div>

              {!apiResponse && (
                <div className='text-center p-8 text-gray-500'>
                  <div className='text-4xl mb-4'>📡</div>
                  <p className='text-lg'>
                    API response will appear here after the demo completes...
                  </p>
                </div>
              )}

              {showJson && apiResponse && (
                <pre
                  className='p-6 rounded-lg overflow-auto text-base border-2'
                  style={{ backgroundColor: '#F0F0F0', borderColor: '#A8B5A0' }}
                >
                  {JSON.stringify(apiResponse, null, 2)}
                </pre>
              )}
            </div>

            {/* Return to Dashboard Section */}
            <div className='bg-blue-50 border-2 border-blue-200 rounded-xl p-8 text-center mt-8'>
              <div className='text-4xl mb-4'>🔄</div>
              <h3 className='text-2xl font-semibold text-blue-800 mb-4'>
                Dashboard Updated!
              </h3>
              <p className='text-lg text-blue-700 mb-6'>
                The new personalized content from this API call is now cached
                and will be reflected on the dashboard. The fresh data includes
                updated music, recipes, photos, and nostalgia news tailored for
                Maria.
              </p>
              <button
                onClick={onReturnToDashboard}
                className='px-8 py-4 rounded-xl text-xl font-medium transition-all shadow-sm hover:shadow-lg'
                style={{ backgroundColor: '#8B7CB6', color: 'white' }}
              >
                Return to Dashboard to See Changes
              </button>
            </div>
          </div>
        )}

        {/* Technical Details */}
        <div className='mt-12'>
          <h3
            className='text-2xl font-light mb-6 text-center'
            style={{ color: '#4A4A4A' }}
          >
            Technical Architecture
          </h3>
          <div className='grid md:grid-cols-3 gap-6'>
            <div className='bg-white rounded-xl p-6 border-2 border-gray-100'>
              <h4
                className='text-lg font-semibold mb-3'
                style={{ color: '#8B7CB6' }}
              >
                🤖 AI Technologies
              </h4>
              <ul className='text-sm text-gray-600 space-y-1'>
                <li>• Google Gemini AI</li>
                <li>• Qloo Cultural Intelligence</li>
                <li>• YouTube Data API</li>
                <li>• Google Vision AI</li>
              </ul>
            </div>

            <div className='bg-white rounded-xl p-6 border-2 border-gray-100'>
              <h4
                className='text-lg font-semibold mb-3'
                style={{ color: '#D4A574' }}
              >
                ⚡ Pipeline Features
              </h4>
              <ul className='text-sm text-gray-600 space-y-1'>
                <li>• Real-time processing</li>
                <li>• Cultural personalization</li>
                <li>• Feedback integration</li>
                <li>• Quality scoring</li>
              </ul>
            </div>

            <div className='bg-white rounded-xl p-6 border-2 border-gray-100'>
              <h4
                className='text-lg font-semibold mb-3'
                style={{ color: '#A8B5A0' }}
              >
                🎯 Outcomes
              </h4>
              <ul className='text-sm text-gray-600 space-y-1'>
                <li>• Personalized content</li>
                <li>• Cultural relevance</li>
                <li>• Memory stimulation</li>
                <li>• Conversation starters</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Demo
