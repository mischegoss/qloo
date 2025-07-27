// Feedback collection and local storage
const feedbackManager = {
  // Collect feedback without sending
  collectFeedback(type, item, category) {
    const feedback = this.getFeedback()
    const timestamp = new Date().toISOString()

    const feedbackEntry = {
      type, // 'like' or 'dislike'
      item, // what they liked/disliked
      category, // 'music', 'recipe', 'photo', 'nostalgia'
      timestamp,
    }

    if (type === 'like') {
      feedback.likes.push(feedbackEntry)
    } else {
      feedback.dislikes.push(feedbackEntry)
    }

    // Store locally for now
    try {
      localStorage.setItem('user_feedback', JSON.stringify(feedback))
    } catch (error) {
      console.warn('Could not save feedback to localStorage:', error)
    }

    console.log(`✅ Feedback collected: ${type} for ${category} - ${item}`)
    return feedback
  },

  // Get current feedback
  getFeedback() {
    try {
      const stored = localStorage.getItem('user_feedback')
      return stored ? JSON.parse(stored) : { likes: [], dislikes: [] }
    } catch (error) {
      console.warn('Could not read feedback from localStorage:', error)
      return { likes: [], dislikes: [] }
    }
  },

  // Clear feedback
  clearFeedback() {
    try {
      localStorage.removeItem('user_feedback')
    } catch (error) {
      console.warn('Could not clear feedback from localStorage:', error)
    }
    return { likes: [], dislikes: [] }
  },

  // Format for API (but we send empty string)
  formatForAPI() {
    const feedback = this.getFeedback()
    return {
      likes: feedback.likes.map(f => f.item),
      dislikes: feedback.dislikes.map(f => f.item),
    }
  },

  // Get feedback summary
  getFeedbackSummary() {
    const feedback = this.getFeedback()
    return {
      totalFeedback: feedback.likes.length + feedback.dislikes.length,
      likes: feedback.likes.length,
      dislikes: feedback.dislikes.length,
      categories: this.getCategorySummary(feedback),
    }
  },

  // Get feedback by category
  getCategorySummary(feedback) {
    const categories = {}

    ;[...feedback.likes, ...feedback.dislikes].forEach(item => {
      if (!categories[item.category]) {
        categories[item.category] = { likes: 0, dislikes: 0 }
      }
      categories[item.category][item.type === 'like' ? 'likes' : 'dislikes']++
    })

    return categories
  },

  // Quick feedback helpers
  likeSong(artist, song) {
    return this.collectFeedback('like', `${artist} - ${song}`, 'music')
  },

  dislikeSong(artist, song) {
    return this.collectFeedback('dislike', `${artist} - ${song}`, 'music')
  },

  likeRecipe(recipeName) {
    return this.collectFeedback('like', recipeName, 'recipe')
  },

  dislikeRecipe(recipeName) {
    return this.collectFeedback('dislike', recipeName, 'recipe')
  },

  likePhoto(photoDescription) {
    return this.collectFeedback('like', photoDescription, 'photo')
  },

  dislikePhoto(photoDescription) {
    return this.collectFeedback('dislike', photoDescription, 'photo')
  },

  likeNostalgia(headline) {
    return this.collectFeedback('like', headline, 'nostalgia')
  },

  dislikeNostalgia(headline) {
    return this.collectFeedback('dislike', headline, 'nostalgia')
  },
}

export default feedbackManager
