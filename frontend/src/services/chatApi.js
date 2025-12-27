const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

class ChatApi {
  static async chat(message, mode = 'full_text', selectedText = null, sessionId = null) {
    // Use 'message' field as per API contract, but also include 'query' for backwards compatibility
    const requestBody = {
      message,  // Primary field per API contract
      query: message,  // Backwards compatibility
      mode,
      retrieval_mode: mode === 'full_text' ? 'full-book' : 'per-page',
    };

    if (selectedText) {
      requestBody.selected_text = selectedText;
    }

    if (sessionId) {
      requestBody.session_id = sessionId;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error in chat API call:', error);
      throw error;
    }
  }

  static async retrieveContext(query, topK = 5) {
    const requestBody = {
      query,
      message: query,  // Also send as message for compatibility
      top_k: topK
    };

    try {
      const response = await fetch(`${API_BASE_URL}/chat/retrieve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error in retrieve context API call:', error);
      throw error;
    }
  }

  static async createSession() {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating session:', error);
      throw error;
    }
  }

  static async getHistory(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/history/${sessionId}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching history:', error);
      throw error;
    }
  }

  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error in health check API call:', error);
      throw error;
    }
  }
}

export default ChatApi;
