// frontend/src/services/dashboardDataStore.js
// Global store for dashboard data with bulletproof fallback support

import { FALLBACK_API_RESPONSE } from '../data/fallbackData'

class DashboardDataStore {
  constructor() {
    this.data = null
    this.listeners = []
  }

  // Set the dashboard data (called after API response)
  setData(dashboardData) {
    this.data = dashboardData
    console.log('📦 Dashboard data stored globally:', dashboardData)

    // Notify any listeners that data has updated
    this.listeners.forEach(listener => listener(this.data))
  }

  // Get the current dashboard data with bulletproof fallback
  getData() {
    if (this.data) {
      return this.data
    }

    console.log('🛡️ Using bulletproof fallback data')
    return FALLBACK_API_RESPONSE
  }

  // Get music data with granular fallback for missing elements
  getMusicData() {
    const apiData = this.data?.content?.music || {}
    const fallbackData = FALLBACK_API_RESPONSE.content.music

    // If no API data at all, use complete fallback
    if (!apiData || Object.keys(apiData).length === 0) {
      console.log('🎵 Using complete fallback music data')
      return fallbackData
    }

    // Merge API data with fallback for missing elements
    const mergedData = {
      artist: apiData.artist || fallbackData.artist,
      piece_title: apiData.piece_title || fallbackData.piece_title,
      youtube_url: apiData.youtube_url || fallbackData.youtube_url,
      youtube_embed: apiData.youtube_embed || fallbackData.youtube_embed,
      conversation_starters:
        apiData.conversation_starters &&
        apiData.conversation_starters.length > 0
          ? apiData.conversation_starters
          : fallbackData.conversation_starters,
      fun_fact: apiData.fun_fact || fallbackData.fun_fact,
    }

    // Log which elements were filled in
    const filledElements = []
    if (!apiData.artist) filledElements.push('artist')
    if (!apiData.piece_title) filledElements.push('piece_title')
    if (!apiData.youtube_url) filledElements.push('youtube_url')
    if (!apiData.youtube_embed) filledElements.push('youtube_embed')
    if (
      !apiData.conversation_starters ||
      apiData.conversation_starters.length === 0
    )
      filledElements.push('conversation_starters')
    if (!apiData.fun_fact) filledElements.push('fun_fact')

    if (filledElements.length > 0) {
      console.log(
        '🎵 Filled missing music elements:',
        filledElements.join(', '),
      )
    }

    return mergedData
  }

  // Get photo data with granular fallback for missing elements
  getPhotoData() {
    const apiData = this.data?.content?.photo || {}
    const fallbackData = FALLBACK_API_RESPONSE.content.photo

    // If no API data at all, use complete fallback
    if (!apiData || Object.keys(apiData).length === 0) {
      console.log('📸 Using complete fallback photo data')
      return fallbackData
    }

    // Merge API data with fallback for missing elements
    const mergedData = {
      filename: apiData.filename || fallbackData.filename,
      description: apiData.description || fallbackData.description,
      cultural_context:
        apiData.cultural_context || fallbackData.cultural_context,
      conversation_starters:
        apiData.conversation_starters &&
        apiData.conversation_starters.length > 0
          ? apiData.conversation_starters
          : fallbackData.conversation_starters,
    }

    // Log which elements were filled in
    const filledElements = []
    if (!apiData.filename) filledElements.push('filename')
    if (!apiData.description) filledElements.push('description')
    if (!apiData.cultural_context) filledElements.push('cultural_context')
    if (
      !apiData.conversation_starters ||
      apiData.conversation_starters.length === 0
    )
      filledElements.push('conversation_starters')

    if (filledElements.length > 0) {
      console.log(
        '📸 Filled missing photo elements:',
        filledElements.join(', '),
      )
    }

    return mergedData
  }

  // Get recipe data with granular fallback for missing elements
  getRecipeData() {
    const apiData = this.data?.content?.recipe || {}
    const fallbackData = FALLBACK_API_RESPONSE.content.recipe

    // If no API data at all, use complete fallback
    if (!apiData || Object.keys(apiData).length === 0) {
      console.log('🍽️ Using complete fallback recipe data')
      return fallbackData
    }

    // Merge API data with fallback for missing elements
    const mergedData = {
      name: apiData.name || fallbackData.name,
      ingredients:
        apiData.ingredients && apiData.ingredients.length > 0
          ? apiData.ingredients
          : fallbackData.ingredients,
      instructions:
        apiData.instructions && apiData.instructions.length > 0
          ? apiData.instructions
          : fallbackData.instructions,
      conversation_starters:
        apiData.conversation_starters &&
        apiData.conversation_starters.length > 0
          ? apiData.conversation_starters
          : fallbackData.conversation_starters,
    }

    // Log which elements were filled in
    const filledElements = []
    if (!apiData.name) filledElements.push('name')
    if (!apiData.ingredients || apiData.ingredients.length === 0)
      filledElements.push('ingredients')
    if (!apiData.instructions || apiData.instructions.length === 0)
      filledElements.push('instructions')
    if (
      !apiData.conversation_starters ||
      apiData.conversation_starters.length === 0
    )
      filledElements.push('conversation_starters')

    if (filledElements.length > 0) {
      console.log(
        '🍽️ Filled missing recipe elements:',
        filledElements.join(', '),
      )
    }

    return mergedData
  }

  // Get nostalgia news data with granular fallback for missing elements
  getNostalgiaData() {
    const apiData = this.data?.content?.nostalgia_news || {}
    const fallbackData = FALLBACK_API_RESPONSE.content.nostalgia_news

    // If no API data at all, use complete fallback
    if (!apiData || Object.keys(apiData).length === 0) {
      console.log('📰 Using complete fallback nostalgia data')
      return fallbackData
    }

    // Handle sections with granular fallback
    const apiSections = apiData.sections || {}
    const fallbackSections = fallbackData.sections || {}

    const mergedSections = {
      memory_spotlight:
        apiSections.memory_spotlight || fallbackSections.memory_spotlight,
      era_highlights:
        apiSections.era_highlights || fallbackSections.era_highlights,
      heritage_traditions:
        apiSections.heritage_traditions || fallbackSections.heritage_traditions,
      conversation_starters:
        apiSections.conversation_starters ||
        fallbackSections.conversation_starters,
    }

    // Merge main nostalgia data
    const mergedData = {
      title: apiData.title || fallbackData.title,
      subtitle: apiData.subtitle || fallbackData.subtitle,
      date: apiData.date || fallbackData.date,
      personalized_for:
        apiData.personalized_for || fallbackData.personalized_for,
      sections: mergedSections,
      themes:
        apiData.themes && apiData.themes.length > 0
          ? apiData.themes
          : fallbackData.themes,
      metadata: apiData.metadata || fallbackData.metadata,
    }

    // Log which elements were filled in
    const filledElements = []
    if (!apiData.title) filledElements.push('title')
    if (!apiData.subtitle) filledElements.push('subtitle')
    if (!apiData.sections || Object.keys(apiData.sections).length === 0) {
      filledElements.push('all_sections')
    } else {
      if (!apiSections.memory_spotlight) filledElements.push('memory_spotlight')
      if (!apiSections.era_highlights) filledElements.push('era_highlights')
      if (!apiSections.heritage_traditions)
        filledElements.push('heritage_traditions')
      if (!apiSections.conversation_starters)
        filledElements.push('conversation_starters')
    }
    if (!apiData.themes || apiData.themes.length === 0)
      filledElements.push('themes')

    if (filledElements.length > 0) {
      console.log(
        '📰 Filled missing nostalgia elements:',
        filledElements.join(', '),
      )
    }

    return mergedData
  }

  // Get patient info with granular fallback for missing elements
  getPatientInfo() {
    const apiData = this.data?.patient_info || {}
    const fallbackData = FALLBACK_API_RESPONSE.patient_info

    // If no API data at all, use complete fallback
    if (!apiData || Object.keys(apiData).length === 0) {
      console.log('👤 Using complete fallback patient info')
      return fallbackData
    }

    // Merge API data with fallback for missing elements
    const mergedData = {
      name: apiData.name || fallbackData.name,
      cultural_heritage:
        apiData.cultural_heritage || fallbackData.cultural_heritage,
      age: apiData.age || fallbackData.age,
      daily_theme: apiData.daily_theme || fallbackData.daily_theme,
    }

    // Log which elements were filled in
    const filledElements = []
    if (!apiData.name) filledElements.push('name')
    if (!apiData.cultural_heritage) filledElements.push('cultural_heritage')
    if (!apiData.age) filledElements.push('age')
    if (!apiData.daily_theme) filledElements.push('daily_theme')

    if (filledElements.length > 0) {
      console.log(
        '👤 Filled missing patient info elements:',
        filledElements.join(', '),
      )
    }

    return mergedData
  }

  // Subscribe to data changes (for React components)
  subscribe(listener) {
    this.listeners.push(listener)

    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  // Check if data is available (now always returns true due to fallback)
  hasData() {
    return true // Always true because we have bulletproof fallback
  }

  // Check if we're using fallback data
  isUsingFallback() {
    return (
      this.data === null ||
      this.data?.metadata?.agent_pipeline === 'fallback_mode'
    )
  }

  // Clear data (useful for refresh)
  clearData() {
    this.data = null
    console.log('🗑️ Dashboard data store cleared')
    this.listeners.forEach(listener => listener(null))
  }

  // Get bulletproof fallback data directly
  getFallbackData() {
    return FALLBACK_API_RESPONSE
  }

  // Debug helper - log all sections with fallback status
  logAllSections() {
    const usingFallback = this.isUsingFallback()
    const status = usingFallback ? '🛡️ FALLBACK' : '✅ LIVE'

    console.log(`🔍 === DASHBOARD DATA STORE CONTENTS (${status}) ===`)
    console.log('👤 Patient Info:', this.getPatientInfo())
    console.log('🎵 Music Data:', this.getMusicData())
    console.log('📷 Photo Data:', this.getPhotoData())
    console.log('🍽️ Recipe Data:', this.getRecipeData())
    console.log('📰 Nostalgia Data:', this.getNostalgiaData())
    console.log('🔍 === END STORE CONTENTS ===')
  }
}

// Create a singleton instance
const dashboardDataStore = new DashboardDataStore()

export default dashboardDataStore
