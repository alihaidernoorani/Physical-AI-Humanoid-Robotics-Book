const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

class ChatApi {
  static async chat(query, mode = 'full_text', selectedText = null, sessionId = null) {
    const requestBody = {
      query,
      mode,
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
        throw new Error(`HTTP error! status: ${response.status}`);
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
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error in retrieve context API call:', error);
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