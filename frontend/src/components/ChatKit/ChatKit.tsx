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
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [isVisible, setIsVisible] = useState<boolean>(true); // Always default to visible
  const [initialLoadComplete, setInitialLoadComplete] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load initial state from localStorage after component mounts
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Load session ID from localStorage
      if (!sessionId) {
        const savedSessionId = localStorage.getItem('chat_session_id');
        if (savedSessionId) {
          setCurrentSessionId(savedSessionId);
        }
      } else {
        setCurrentSessionId(sessionId);
      }

      // Load visibility state from localStorage
      // Only apply saved visibility if it exists, otherwise keep default (true)
      const savedVisibility = localStorage.getItem('chatkit_visibility');
      if (savedVisibility !== null) {
        setIsVisible(savedVisibility === 'true');
      } else {
        // If no saved visibility state exists, ensure it stays visible
        setIsVisible(true);
      }

      setInitialLoadComplete(true);
    }
  }, [sessionId]);

  // Initialize session if not provided
  useEffect(() => {
    const initializeSession = async () => {
      if (!currentSessionId && initialLoadComplete) {
        try {
          const sessionData = await chatService.createSession({
            timestamp: new Date().toISOString(),
            metadata: { type: 'global-chat' }
          });
          const newSessionId = sessionData.session_id;
          setCurrentSessionId(newSessionId);
          localStorage.setItem('chat_session_id', newSessionId);
          setError(null); // Clear any previous errors on successful session creation
        } catch (err) {
          console.error('Error creating session:', err);
          // Don't set an error here as we want the UI to remain functional
          // even if session creation fails - use a fallback session ID
          setCurrentSessionId(`fallback-session-${Date.now()}`);
        }
      }
    };

    if (initialLoadComplete) {
      initializeSession();
    }

    // Cleanup function to handle component unmount
    return () => {
      // Optionally save current messages to localStorage for persistence
      if (messages.length > 0) {
        localStorage.setItem('chat_messages', JSON.stringify(messages));
      }
    };
  }, [currentSessionId, initialLoadComplete]);

  // Toggle chat visibility
  const toggleChat = () => {
    const newState = !isVisible;
    setIsVisible(newState);
    if (typeof window !== 'undefined') {
      localStorage.setItem('chatkit_visibility', newState.toString());
    }
  };

  // Handle sending a message to the backend
  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

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

      // Only send to backend if we have a valid session ID (not fallback)
      if (currentSessionId && !currentSessionId.startsWith('fallback-session-')) {
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
      } else {
        // If using fallback session, simulate a response
        const botMessage: ChatMessage = {
          id: Date.now() + 1,
          text: 'I\'m currently unable to connect to the backend service. This is a fallback mode where responses are simulated locally.',
          sender: 'system',
          timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, botMessage]);
      }

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
          💬
        </button>
      )}
    </div>
  );
};

export default ChatKit;