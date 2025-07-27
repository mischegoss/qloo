import React, { useState, useEffect } from 'react'

const Demo = () => {
  const [currentStep, setCurrentStep] = useState(0)
  const [isRunning, setIsRunning] = useState(false)

  const agentSteps = [
    {
      id: 1,
      name: 'Information Consolidator',
      description: 'Gathering patient profile and theme selection',
      details:
        'Processing patient info: Maria, age 80, Italian-American heritage. Selecting daily theme: Family.',
      status: 'waiting',
      color: '#D4A574',
    },
    {
      id: 2,
      name: 'Photo Analysis',
      description: 'Analyzing cultural context of selected images',
      details:
        'Analyzing family.png - detecting warm family scene with cultural context enhancement.',
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
        '4A: Music (Vivaldi), 4B: Recipe (Microwave Risotto), 4C: Photo Description (Cultural context)',
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

  const runDemo = () => {
    setIsRunning(true)
    setCurrentStep(0)

    // Reset all steps
    setSteps(agentSteps.map(step => ({ ...step, status: 'waiting' })))

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
            setTimeout(() => {
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
              isRunning
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-purple-600 hover:bg-purple-700 hover:shadow-lg'
            }`}
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
                className='bg-purple-600 h-3 rounded-full transition-all duration-1000 ease-out'
                style={{
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
            <div className='bg-green-50 border-2 border-green-200 rounded-xl p-8 text-center'>
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
                  <div className='text-green-600'>Vivaldi Selected</div>
                </div>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>Recipe</div>
                  <div className='text-green-600'>Microwave Risotto</div>
                </div>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>Photo</div>
                  <div className='text-green-600'>Family Scene</div>
                </div>
                <div className='bg-white p-4 rounded-lg border border-green-200'>
                  <div className='font-semibold text-green-800'>News</div>
                  <div className='text-green-600'>Personal Story</div>
                </div>
              </div>
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
              <h4 className='text-lg font-semibold mb-3 text-purple-700'>
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
              <h4 className='text-lg font-semibold mb-3 text-blue-700'>
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
              <h4 className='text-lg font-semibold mb-3 text-green-700'>
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
