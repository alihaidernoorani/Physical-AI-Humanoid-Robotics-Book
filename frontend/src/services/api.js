import axios from 'axios';

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth headers if needed
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens or headers here if needed
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response || error.message);
    return Promise.reject(error);
  }
);

// RAG Chat API functions
export const ragService = {
  // Send a query to the RAG system
  query: async (queryData) => {
    try {
      const response = await api.post('/rag/chat', queryData);
      return response.data;
    } catch (error) {
      console.error('Error querying RAG system:', error);
      throw error;
    }
  },

  // Get health status of the RAG system
  getHealth: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
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
      const response = await api.post('/embeddings/generate', contentData);
      return response.data;
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
      const response = await api.get('/user/settings');
      return response.data;
    } catch (error) {
      console.error('Error getting user settings:', error);
      throw error;
    }
  },

  // Update user settings
  updateSettings: async (settingsData) => {
    try {
      const response = await api.put('/user/settings', settingsData);
      return response.data;
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
      const response = await api.post('/translate', translationData);
      return response.data;
    } catch (error) {
      console.error('Error translating content:', error);
      throw error;
    }
  }
};

export default api;