// Transform API response to your current UI data structure
export const mapApiToUIData = apiResponse => {
  if (!apiResponse?.content) {
    console.warn('Invalid API response, using minimal fallback')
    return getFallbackUIData()
  }

  return {
    // Patient information
    patient: {
      name: apiResponse.patient_info?.name || 'Guest',
      theme: apiResponse.patient_info?.daily_theme || 'Memories',
      heritage: apiResponse.patient_info?.cultural_heritage || '',
      age: apiResponse.patient_info?.age || 0,
    },

    // Music content
    music: {
      artist: apiResponse.content.music?.artist || '',
      title: apiResponse.content.music?.piece_title || '',
      embedUrl: apiResponse.content.music?.youtube_embed || '',
      youtubeUrl: apiResponse.content.music?.youtube_url || '',
      conversationStarters:
        apiResponse.content.music?.conversation_starters || [],
      funFact: apiResponse.content.music?.fun_fact || '',
    },

    // Recipe content
    recipe: {
      name: apiResponse.content.recipe?.name || '',
      description: apiResponse.content.recipe?.description || '',
      ingredients: apiResponse.content.recipe?.ingredients || [],
      instructions: apiResponse.content.recipe?.instructions || [],
      conversationQuestions:
        apiResponse.content.recipe?.conversation_starters || [],
      culturalContext: 'A comforting dish that brings families together', // Default context
    },

    // Photo content
    photo: {
      filename: apiResponse.content.photo?.filename || '',
      description: apiResponse.content.photo?.description || '',
      culturalContext: apiResponse.content.photo?.cultural_context || '',
      conversationStarters:
        apiResponse.content.photo?.conversation_starters || [],
    },

    // Nostalgia news content
    nostalgia: {
      headline: apiResponse.content.nostalgia_news?.headline || '',
      content: apiResponse.content.nostalgia_news?.content || '',
      themes: apiResponse.content.nostalgia_news?.themes || [],
      conversationStarters:
        apiResponse.content.nostalgia_news?.conversation_starters || [],
      // Break down into sections for your current UI structure
      memorySpotlight: {
        headline: 'Memory Spotlight',
        content: extractFirstParagraph(
          apiResponse.content.nostalgia_news?.content,
        ),
      },
      eraSpotlight: {
        headline: 'Your Era Spotlight',
        content: extractSecondParagraph(
          apiResponse.content.nostalgia_news?.content,
        ),
      },
      heritageTraditions: {
        headline: 'Heritage Traditions',
        content: extractThirdParagraph(
          apiResponse.content.nostalgia_news?.content,
        ),
      },
      conversationCorner: {
        headline: 'Conversation Corner',
        questions:
          apiResponse.content.nostalgia_news?.conversation_starters || [],
      },
    },

    // Metadata
    metadata: {
      qualityScore: apiResponse.metadata?.quality_score || 'unknown',
      personalizationLevel:
        apiResponse.metadata?.personalization_level || 'basic',
      timestamp:
        apiResponse.metadata?.generation_timestamp || new Date().toISOString(),
      theme: apiResponse.metadata?.theme || 'General',
      agentPipeline: apiResponse.metadata?.agent_pipeline || 'unknown',
      isUsingFallback: apiResponse.metadata?.agent_pipeline === 'fallback_mode',
    },
  }
}

// Helper functions to break down nostalgia content
function extractFirstParagraph(content) {
  if (!content) return 'Reflecting on wonderful memories from the past.'
  const sentences = content.split('.').filter(s => s.trim().length > 0)
  return sentences.slice(0, 2).join('.') + '.'
}

function extractSecondParagraph(content) {
  if (!content) return 'Every era has its own special charm and character.'
  const sentences = content.split('.').filter(s => s.trim().length > 0)
  return sentences.slice(2, 4).join('.') + '.'
}

function extractThirdParagraph(content) {
  if (!content)
    return 'Family traditions create lasting bonds and cherished memories.'
  const sentences = content.split('.').filter(s => s.trim().length > 0)
  return sentences.slice(4).join('.') + '.'
}

// Minimal fallback UI data
function getFallbackUIData() {
  return {
    patient: { name: 'Guest', theme: 'Memories' },
    music: {
      artist: 'Unknown',
      title: 'Beautiful Music',
      conversationStarters: [],
    },
    recipe: {
      name: 'Simple Recipe',
      ingredients: [],
      instructions: [],
      conversationQuestions: [],
    },
    photo: {
      filename: 'photo.png',
      description: 'A lovely picture',
      conversationStarters: [],
    },
    nostalgia: {
      headline: 'Memory Lane',
      content: 'Reflecting on wonderful memories.',
      conversationStarters: [],
      memorySpotlight: {
        headline: 'Memory Spotlight',
        content: 'Beautiful memories from the past.',
      },
      eraSpotlight: {
        headline: 'Your Era Spotlight',
        content: 'Every era has its special moments.',
      },
      heritageTraditions: {
        headline: 'Heritage Traditions',
        content: 'Family traditions matter.',
      },
      conversationCorner: { headline: 'Conversation Corner', questions: [] },
    },
    metadata: { qualityScore: 'fallback', isUsingFallback: true },
  }
}

// Extract all conversation starters for easy access
export const getAllConversationStarters = uiData => {
  return [
    ...uiData.music.conversationStarters,
    ...uiData.recipe.conversationQuestions,
    ...uiData.photo.conversationStarters,
    ...uiData.nostalgia.conversationStarters,
  ]
}

// Default export for the main mapper function
export default mapApiToUIData
