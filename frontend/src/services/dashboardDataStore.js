// dashboardDataStore.js - Global store for dashboard data

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

  // Get the current dashboard data
  getData() {
    return this.data
  }

  // Get music data specifically
  getMusicData() {
    return this.data?.content?.music || {}
  }

  // Get photo data specifically
  getPhotoData() {
    return this.data?.content?.photo || {}
  }

  // Get recipe data specifically
  getRecipeData() {
    return this.data?.content?.recipe || {}
  }

  // Get nostalgia news data specifically
  getNostalgiaData() {
    return this.data?.content?.nostalgia_news || {}
  }

  // Get patient info
  getPatientInfo() {
    return this.data?.patient_info || {}
  }

  // Subscribe to data changes (for React components)
  subscribe(listener) {
    this.listeners.push(listener)

    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  // Check if data is available
  hasData() {
    return this.data !== null
  }

  // Clear data (useful for refresh)
  clearData() {
    this.data = null
    console.log('🗑️ Dashboard data store cleared')
    this.listeners.forEach(listener => listener(null))
  }

  // Debug helper - log all sections
  logAllSections() {
    if (!this.data) {
      console.log('❌ No data in store')
      return
    }

    console.log('🔍 === DASHBOARD DATA STORE CONTENTS ===')
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
