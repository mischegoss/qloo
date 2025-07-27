// Complete fallback data - date-agnostic version
export const FALLBACK_API_RESPONSE = {
  patient_info: {
    name: 'Maria',
    cultural_heritage: 'Italian-American',
    age: 80,
    daily_theme: 'Family',
  },
  content: {
    music: {
      artist: 'Johann Sebastian Bach',
      piece_title: 'Brandenburg Concerto No. 3',
      youtube_url: 'https://www.youtube.com/watch?v=x8EqpwVErbo',
      youtube_embed: 'https://www.youtube.com/embed/x8EqpwVErbo',
      conversation_starters: [
        "Bach's music is so mathematical and beautiful",
        'This music has such intricate harmonies',
      ],
      fun_fact: 'Bach had 20 children and taught many of them music',
    },
    recipe: {
      name: 'Microwave Risotto with Parmesan',
      description: '',
      ingredients: [
        '1/2 cup instant rice',
        '1 cup chicken broth (from carton)',
        '2 tablespoons grated Parmesan cheese',
        '1 teaspoon butter',
      ],
      instructions: [
        'Combine rice and broth in microwave-safe bowl',
        'Microwave for 3-4 minutes until rice is tender',
        'Stir in Parmesan cheese and butter',
        'Let sit for 2 minutes before serving',
      ],
      conversation_starters: [
        'Did your family make risotto on special occasions?',
        'Do you remember Italian dishes from your childhood?',
        'What was your favorite Italian restaurant?',
      ],
    },
    photo: {
      filename: 'family.png',
      description:
        "Here's a lovely picture of a family outside. See the little girl with curly hair? She's smiling! A man is sitting nearby, watching her. Everyone looks so happy and peaceful.",
      cultural_context: 'Enhanced for italian-american heritage',
      conversation_starters: [
        "That's a lovely sunny day, isn't it? Reminds me of picnics!",
        'Look at that beautiful family. Happy times, right?',
        "This picture makes me think of good food and laughter. What's your favorite food?",
      ],
    },
    nostalgia_news: {
      headline: "Maria's Memory Lane",
      content:
        "The 1940s were a time of hope and rebuilding, filled with optimism for the future. Maria, you were just a baby during this era of fresh starts and new beginnings. In those days, Memory Lane was often celebrated through family gatherings and listening to beautiful music. Think of the joy of sharing stories while listening to music like today's selection by Johann Sebastian Bach – perhaps it reminds you of some special family moments? It's a beautiful melody. Italian-American families like Maria's often celebrated Memory Lane with delicious home-cooked meals, sharing stories and laughter around the table. Today's microwave risotto with parmesan cheese is a simple yet comforting dish, Maria, perhaps reminding you of similar family meals from your youth.",
      themes: ['memories', 'traditions', 'family'],
      conversation_starters: [
        'Maria, what are some of your favorite childhood memories from your family gatherings?',
        'Maria, can you recall a happy moment from your youth that involved music?',
        'Maria, what are some of the delicious foods you remember enjoying with your family during your younger years?',
      ],
    },
  },
  metadata: {
    quality_score: 'high',
    personalization_level: 'highly_personalized',
    generation_timestamp: null,
    theme: 'Family',
    agent_pipeline: 'fallback_mode',
  },
  pipeline_metadata: {
    agents_executed: 8,
    execution_timestamp: null,
    pipeline_version: 'fallback_demo',
    star_feature: 'nostalgia_news_generator',
    cultural_intelligence: 'demo_powered',
    personalization: 'sample_enhanced',
    agents_summary: {
      agent1: 'Information consolidation with theme selection',
      agent2: 'Simple photo analysis (theme-based)',
      agent3: 'Cultural intelligence (heritage-driven)',
      agent4a: 'Music curation with YouTube integration',
      agent4b: 'Recipe selection (microwave-safe)',
      agent4c: 'Photo description with cultural context',
      agent5: 'Nostalgia News generation',
      agent6: 'Dashboard synthesis and final assembly',
    },
  },
}
