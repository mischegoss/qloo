import React from 'react'

const LoadingSpinner = () => {
  return (
    <div
      className='min-h-screen flex items-center justify-center relative overflow-hidden'
      style={{ backgroundColor: '#F8F7ED' }}
    >
      {/* Subtle background glow effect */}
      <div className='absolute inset-0 bg-gradient-radial from-yellow-50/30 via-transparent to-transparent'></div>

      <div className='text-center relative z-10 max-w-2xl mx-auto px-6'>
        {/* Animated Logo Container */}
        <div className='mb-12 animate-fade-in'>
          {/* Brand Name - Main Focus */}
          <h1
            className='text-8xl font-light tracking-wide mb-6 animate-fade-in-delay-1'
            style={{
              color: '#7F74A8',
              fontFamily: 'system-ui, -apple-system, sans-serif',
            }}
          >
            LumiCue
          </h1>

          {/* Tagline */}
          <p
            className='text-3xl font-light tracking-wide animate-fade-in-delay-2'
            style={{ color: '#7F74A8', opacity: 0.8 }}
          >
            Sparking Meaningful Conversations
          </p>
        </div>

        {/* Loading indicator */}
        <div className='space-y-8 animate-fade-in-delay-3'>
          {/* Prominent animated progress dots */}
          <div className='flex justify-center space-x-4'>
            <div
              className='w-6 h-6 rounded-full animate-bounce-gentle'
              style={{ backgroundColor: '#B8B0D7', animationDelay: '0ms' }}
            ></div>
            <div
              className='w-6 h-6 rounded-full animate-bounce-gentle'
              style={{ backgroundColor: '#FFDAC0', animationDelay: '150ms' }}
            ></div>
            <div
              className='w-6 h-6 rounded-full animate-bounce-gentle'
              style={{ backgroundColor: '#8B7CB6', animationDelay: '300ms' }}
            ></div>
          </div>

          {/* Loading text */}
          <p
            className='text-xl font-light animate-pulse-text'
            style={{ color: '#7F74A8', opacity: 0.7 }}
          >
            Curating your personalized experience
          </p>
        </div>

        {/* Subtle bottom accent */}
        <div className='mt-16 flex justify-center'>
          <div
            className='w-32 h-2 rounded-full opacity-30'
            style={{
              background:
                'linear-gradient(to right, #B8B0D7, #FFDAC0, #8B7CB6, #FFDAC0, #B8B0D7)',
            }}
          ></div>
        </div>
      </div>

      {/* Custom styles for animations */}
      <style>{`
        @keyframes lumicue-fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes lumicue-bounce-gentle {
          0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-12px); }
          60% { transform: translateY(-6px); }
        }
        
        @keyframes lumicue-pulse-text {
          0%, 100% { opacity: 0.7; }
          50% { opacity: 1; }
        }
        
        .animate-fade-in { animation: lumicue-fade-in 1s ease-out; }
        .animate-fade-in-delay-1 { animation: lumicue-fade-in 1s ease-out 0.3s both; }
        .animate-fade-in-delay-2 { animation: lumicue-fade-in 1s ease-out 0.6s both; }
        .animate-fade-in-delay-3 { animation: lumicue-fade-in 1s ease-out 0.9s both; }
        .animate-bounce-gentle { animation: lumicue-bounce-gentle 1.5s infinite; }
        .animate-pulse-text { animation: lumicue-pulse-text 2s ease-in-out infinite; }
      `}</style>
    </div>
  )
}

export default LoadingSpinner
