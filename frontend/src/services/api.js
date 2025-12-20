// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Helper function to make API requests
const makeRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if available
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// RAG Chat API functions
export const ragService = {
  // Send a query to the RAG system
  query: async (queryData) => {
    try {
      return await makeRequest('/rag/chat', {
        method: 'POST',
        body: JSON.stringify(queryData),
      });
    } catch (error) {
      console.error('Error querying RAG system:', error);
      throw error;
    }
  },

  // Get health status of the RAG system
  getHealth: async () => {
    try {
      return await makeRequest('/health', {
        method: 'GET',
      });
    } catch (error) {
      console.error('Error getting health status:', error);
      throw error;
    }
  }
};

// Embeddings API functions
export const embeddingsService = {
  // Generate embeddings for content
  generate: async (contentData) => {
    try {
      return await makeRequest('/embeddings/generate', {
        method: 'POST',
        body: JSON.stringify(contentData),
      });
    } catch (error) {
      console.error('Error generating embeddings:', error);
      throw error;
    }
  }
};

// User/Personalization API functions
export const userService = {
  // Get user settings
  getSettings: async () => {
    try {
      return await makeRequest('/user/settings', {
        method: 'GET',
      });
    } catch (error) {
      console.error('Error getting user settings:', error);
      throw error;
    }
  },

  // Update user settings
  updateSettings: async (settingsData) => {
    try {
      return await makeRequest('/user/settings', {
        method: 'PUT',
        body: JSON.stringify(settingsData),
      });
    } catch (error) {
      console.error('Error updating user settings:', error);
      throw error;
    }
  }
};

// Translation API functions
export const translationService = {
  // Translate content
  translate: async (translationData) => {
    try {
      return await makeRequest('/translate', {
        method: 'POST',
        body: JSON.stringify(translationData),
      });
    } catch (error) {
      console.error('Error translating content:', error);
      throw error;
    }
  }
};

// Chat API functions
export const chatService = {
  // Send a chat message to the backend
  sendMessage: async (messageData) => {
    try {
      return await makeRequest('/chat', {
        method: 'POST',
        body: JSON.stringify(messageData),
      });
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  },

  // Get chat history
  getHistory: async (sessionId) => {
    try {
      return await makeRequest(`/chat/history/${sessionId}`, {
        method: 'GET',
      });
    } catch (error) {
      console.error('Error getting chat history:', error);
      throw error;
    }
  },

  // Create new chat session
  createSession: async (sessionData) => {
    try {
      return await makeRequest('/chat/session', {
        method: 'POST',
        body: JSON.stringify(sessionData),
      });
    } catch (error) {
      console.error('Error creating chat session:', error);
      throw error;
    }
  }
};