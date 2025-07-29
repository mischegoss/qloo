// frontend/src/data/fallbackData.js
// Complete bulletproof demo fallback matching exact API response structure

export const FALLBACK_API_RESPONSE = {
  patient_info: {
    cultural_heritage: 'Italian-American',
    age_group: 'oldest_senior',
    daily_theme: 'Holidays',
    anonymized: true,
    pii_compliant: true,
  },
  content: {
    music: {
      artist: 'Giacomo Puccini',
      piece_title: 'O Mio Babbino Caro',
      youtube_url: 'https://www.youtube.com/watch?v=ndBVQ1etM24',
      youtube_embed: 'https://www.youtube.com/embed/ndBVQ1etM24',
      conversation_starters: [
        "Puccini's operas tell such beautiful stories",
        'This music feels so dramatic and romantic',
      ],
      fun_fact: 'Puccini wrote some of the most beloved operas in history',
    },
    recipe: {
      name: 'Italian Christmas Panettone Bread Pudding',
      ingredients: [
        '2 cubes day-old bread (or panettone)',
        '1/4 cup milk',
        '1 tablespoon sugar',
        '1/2 teaspoon vanilla',
        '1 tablespoon raisins',
      ],
      instructions: [
        'Place bread cubes in microwave-safe mug',
        'Mix milk, sugar, and vanilla',
        'Pour over bread and let soak 2 minutes',
        'Add raisins and microwave 90 seconds',
      ],
      conversation_starters: [
        'Did you enjoy panettone during Christmas?',
        'Do you remember Italian holiday traditions?',
        'What Italian holiday foods were special to your family?',
      ],
    },
    photo: {
      filename: 'holidays.png',
      description:
        'Look at all the happy people!  There are bright colors everywhere.  Someone is playing music.  It looks like a fun day for everyone.',
      cultural_context: 'Enhanced for Italian-American heritage',
      conversation_starters: [
        'Friend, look at this picture of a parade!  Do you remember how much fun families had at celebrations like this, with music and happy people?',
        'This photo shows a lovely community event.  Many people enjoyed sharing food and laughter together at these gatherings.  What happy memories do you have of getting together with others?',
        "Friend, this picture reminds me of lively festivals.  Families often enjoyed delicious food and beautiful decorations at these events.  Wasn't it wonderful to share those moments?",
      ],
    },
    nostalgia_news: {
      title: 'Nostalgia News – July 29',
      subtitle: 'Holidays Edition',
      date: 'July 29, 2025',
      sections: {
        memory_spotlight: {
          headline: '📚 Memory Spotlight',
          content:
            'Remember the excitement of decorating the Christmas tree?  Back in the 1940s and 50s, families often used handmade ornaments and repurposed materials, making each decoration unique and special. It was a time of simpler pleasures, focusing on family togetherness.',
          fun_fact: 'Historical moments create our most treasured memories.',
        },
        era_highlights: {
          headline: '🎵 Era Highlights',
          content:
            'In those days, holiday celebrations were often centered around family gatherings and delicious food.  Think of the aroma of simmering sauces and the joyful sounds of laughter and conversation filling the home.  Radio shows provided festive music, bringing the spirit of the holidays into every living room.',
          fun_fact: "Music has always been central to life's celebrations.",
        },
        heritage_traditions: {
          headline: '🏛️ Heritage Traditions',
          content:
            'Italian-American families often celebrated with traditional feasts featuring dishes like lasagna, ravioli, and of course, panettone!  These gatherings were a time to honor family heritage and share cherished recipes passed down through generations, creating a warm and welcoming atmosphere.',
          fun_fact: 'Cultural traditions connect us to our roots.',
        },
        conversation_starters: {
          headline: '💬 Conversation Starters',
          questions: [
            'Friend, what are some of your favorite holiday memories from your childhood?',
            'Friend, what kind of special treats did families enjoy during the holidays in the past?',
            'Friend, what are some of the sounds and smells that remind you of happy holidays?',
          ],
        },
      },
      themes: ['Holidays', 'Heritage', 'Memories'],
      metadata: {
        generated_by: 'gemini_newsletter',
        generation_timestamp: '2025-07-29T00:51:58.169750',
        theme_integrated: 'Holidays',
        heritage_featured: 'italian-american',
        age_group: 'oldest_senior',
        safety_level: 'dementia_friendly',
        structure_verified: true,
        sections_count: 4,
        newsletter_tone: true,
        pii_compliant: true,
        anonymized: true,
      },
    },
  },
  metadata: {
    quality_score: 'high',
    personalization_level: 'highly_personalized',
    generation_timestamp: '2025-07-29T00:51:58.171921',
    theme: 'Holidays',
    agent_pipeline: '6_agent_enhanced_pii_compliant',
    pii_compliant: true,
    anonymized_profile: true,
    cultural_heritage_used: 'Italian-American',
    age_group_used: 'oldest_senior',
  },
  pipeline_metadata: {
    agents_executed: 8,
    execution_timestamp: '2025-07-29T00:51:58.172479',
    pipeline_version: '6_agent_nostalgia_news_pii_compliant',
    star_feature: 'nostalgia_news_generator',
    cultural_intelligence: 'qloo_powered',
    personalization: 'gemini_enhanced',
    pii_compliant: true,
    anonymized_profile: true,
    agents_summary: {
      agent1: 'Information consolidation with theme selection (anonymized)',
      agent2: 'Simple photo analysis (theme-based)',
      agent3: 'Qloo cultural intelligence (heritage-driven, PII-compliant)',
      agent4a: 'Music curation with YouTube integration',
      agent4b: 'Recipe selection (microwave-safe)',
      agent4c: 'Photo description with cultural context',
      agent5: 'Nostalgia News generation (Gemini AI, PII-compliant)',
      agent6: 'Dashboard synthesis and final assembly',
    },
  },
}
