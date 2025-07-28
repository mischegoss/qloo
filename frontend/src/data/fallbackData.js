// frontend/src/data/fallbackData.js
// Complete bulletproof demo fallback with Happy Days theme

export const FALLBACK_API_RESPONSE = {
  patient_info: {
    name: 'Maria',
    cultural_heritage: 'Italian-American',
    age: 80,
    daily_theme: 'Happy Days',
  },
  content: {
    music: {
      artist: 'Giacomo Puccini',
      piece_title: 'La Bohème',
      youtube_url: 'https://www.youtube.com/watch?v=eKh7SnSi8S8',
      youtube_embed: 'https://www.youtube.com/embed/eKh7SnSi8S8',
      conversation_starters: [
        'This beautiful opera reminds me of those wonderful Friday nights at the theater',
        "Puccini's music makes me think of romantic dinners and dancing under the stars",
      ],
      fun_fact:
        'In the 1950s, families would gather around the radio to listen to beautiful opera broadcasts together',
    },
    recipe: {
      name: 'Happy Days Italian Afternoon Snack',
      ingredients: [
        '1 slice good bread',
        '1 tablespoon olive oil',
        '1 teaspoon balsamic vinegar',
        'Pinch of salt',
        '1 teaspoon Parmesan cheese',
      ],
      instructions: [
        'Toast bread lightly in microwave for 30 seconds',
        'Drizzle with olive oil and balsamic vinegar',
        'Sprinkle with salt and Parmesan',
        'Heat for additional 30 seconds to warm',
      ],
      conversation_starters: [
        'Remember those carefree afternoons when life was simple and sweet?',
        'Did your family enjoy these kinds of treats while watching The Ed Sullivan Show?',
        'What were your favorite simple pleasures back in the happy days?',
      ],
    },
    photo: {
      filename: 'school.png',
      description:
        "Here's a delightful photo that captures the joy of the Happy Days era! It shows children with bright smiles and that unmistakable 1950s charm. Everyone looks so neat and cheerful, just like those wonderful times when life felt full of promise and every day brought new adventures.",
      cultural_context:
        'Enhanced for italian-american heritage with Happy Days nostalgia',
      conversation_starters: [
        'Look at those happy faces! Does this remind you of the good old days when everything felt magical?',
        "This photo brings back memories of sock hops and soda fountains, doesn't it? Those were such happy times!",
        "See how everyone's dressed up so nicely? Those were the days when people took pride in looking their best!",
      ],
    },
    nostalgia_news: {
      title: 'Nostalgia News – July 28',
      subtitle: 'Happy Days Edition',
      date: 'July 28, 2025',
      personalized_for: 'Maria',
      sections: {
        memory_spotlight: {
          headline: '✨ Memory Spotlight',
          content:
            'On this day in 1948, Italy adopted a new constitution, symbolizing hope and new beginnings - just like those wonderful Happy Days when the future seemed bright and full of possibilities! It was an era of optimism, much like the feeling of cruising down Main Street with friends on a perfect summer evening.',
          fun_fact:
            'The happiest memories are made during times of hope and togetherness.',
        },
        era_highlights: {
          headline: '🎶 Era Highlights',
          content:
            'The 1950s were truly the Happy Days - drive-in movies, jukeboxes playing the latest hits, and families gathering for Sunday dinners. Remember the excitement of getting dressed up for a night out at the local diner? Those simple pleasures made every day feel special and full of joy.',
          fun_fact:
            "Rock 'n' roll and family values made the 50s an unforgettable time.",
        },
        heritage_traditions: {
          headline: '🏛️ Heritage Traditions',
          content:
            'Italian-American families in the Happy Days era brought such warmth to their communities - Sunday gravy simmering all day, kids playing stickball in the street, and neighbors who were like family. Those traditions of food, music, and togetherness made every day feel like a celebration of la bella vita.',
          fun_fact:
            'Family traditions create the happiest and most lasting memories.',
        },
        conversation_starters: {
          headline: '💬 Conversation Starters',
          questions: [
            'What made you happiest during those wonderful 1950s days?',
            'Do you remember dancing to your favorite songs at the local hop?',
            'What was your favorite family tradition that made those days so special?',
          ],
        },
      },
      themes: ['Happy Days', 'Heritage', 'Memories'],
      metadata: {
        generated_by: 'gemini_newsletter',
        generation_timestamp: '2025-07-28T15:51:22.347808',
        theme_integrated: 'Happy Days',
        heritage_featured: 'italian-american',
        safety_level: 'dementia_friendly',
        structure_verified: true,
        sections_count: 4,
        newsletter_tone: true,
      },
    },
  },
  metadata: {
    quality_score: 'high',
    personalization_level: 'highly_personalized',
    generation_timestamp: '2025-07-28T15:51:22.349328',
    theme: 'Happy Days',
    agent_pipeline: '6_agent_enhanced',
  },
  pipeline_metadata: {
    agents_executed: 8,
    execution_timestamp: '2025-07-28T15:51:22.349785',
    pipeline_version: '6_agent_nostalgia_news',
    star_feature: 'nostalgia_news_generator',
    cultural_intelligence: 'qloo_powered',
    personalization: 'gemini_enhanced',
    agents_summary: {
      agent1: 'Information consolidation with theme selection',
      agent2: 'Simple photo analysis (theme-based)',
      agent3: 'Qloo cultural intelligence (heritage-driven)',
      agent4a: 'Music curation with YouTube integration',
      agent4b: 'Recipe selection (microwave-safe)',
      agent4c: 'Photo description with cultural context',
      agent5: 'Nostalgia News generation (Gemini AI)',
      agent6: 'Dashboard synthesis and final assembly',
    },
  },
}
