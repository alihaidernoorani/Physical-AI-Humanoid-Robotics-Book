import React, { useState, useEffect } from 'react';
import { ChatWindow } from './index';
import { chatService } from '../../services/api';
import './ChatKit.css';

interface ChatMessage {
  id: string | number;
  text: string;
  sender: 'user' | 'bot' | 'system';
  timestamp: string;
  citations?: string[];
}

interface ChatKitProps {
  initialMessages?: ChatMessage[];
  sessionId?: string;
  showChat?: boolean;
}

const ChatKit: React.FC<ChatKitProps> = ({
  initialMessages = [],
  sessionId = null,
  showChat = true
}) => {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(() => {
    // Check if we already have a session ID in localStorage
    if (sessionId) return sessionId;
    return localStorage.getItem('chat_session_id') || null;
  });
  const [isVisible, setIsVisible] = useState(() => {
    // Check if visibility state is stored in localStorage
    const savedVisibility = localStorage.getItem('chatkit_visibility');
    if (savedVisibility !== null) {
      return savedVisibility === 'true';
    }
    return showChat;
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize session if not provided
  useEffect(() => {
    const initializeSession = async () => {
      if (!currentSessionId) {
        try {
          const sessionData = await chatService.createSession({
            timestamp: new Date().toISOString(),
            metadata: { type: 'global-chat' }
          });
          const newSessionId = sessionData.session_id;
          setCurrentSessionId(newSessionId);
          localStorage.setItem('chat_session_id', newSessionId);
        } catch (err) {
          console.error('Error creating session:', err);
          setError('Failed to initialize chat session');
        }
      }
    };

    initializeSession();

    // Cleanup function to handle component unmount
    return () => {
      // Optionally save current messages to localStorage for persistence
      if (messages.length > 0) {
        localStorage.setItem('chat_messages', JSON.stringify(messages));
      }
    };
  }, []);

  // Toggle chat visibility
  const toggleChat = () => {
    const newState = !isVisible;
    setIsVisible(newState);
    localStorage.setItem('chatkit_visibility', newState.toString());
  };

  // Handle sending a message to the backend
  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading || !currentSessionId) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message immediately
      const userMessage: ChatMessage = {
        id: Date.now(),
        text: message,
        sender: 'user',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, userMessage]);

      // Send to backend API
      const response = await chatService.sendMessage({
        query: message,
        session_id: currentSessionId
      });

      // Add bot response
      const botMessage: ChatMessage = {
        id: Date.now() + 1,
        text: response.response || response.answer || 'No response received',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        citations: response.citations || []
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (err) {
      console.error('Error sending message:', err);

      if (err.message === 'Request timeout') {
        setError('Request timed out. Please try again.');
      } else {
        setError('Failed to send message. Please try again.');
      }

      // Add error message to chat
      const errorMessage: ChatMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'system',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`chatkit-container ${isVisible ? 'chatkit-visible' : 'chatkit-hidden'}`}>
      {isVisible ? (
        <div className="chatkit-wrapper">
          <div className="chatkit-header">
            <h3>AI Chat Assistant</h3>
            <button
              className="chatkit-toggle-btn"
              onClick={toggleChat}
              aria-label="Minimize chat"
            >
              −
            </button>
          </div>
          <ChatWindow
            sessionId={currentSessionId}
            initialMessages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isLoading}
            error={error}
          />
        </div>
      ) : (
        <button
          className="chatkit-open-btn"
          onClick={toggleChat}
          aria-label="Open chat"
        >
          💬 Chat
        </button>
      )}
    </div>
  );
};

export default ChatKit;