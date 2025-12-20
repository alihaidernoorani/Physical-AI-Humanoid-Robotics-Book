import React, { useState, useEffect } from 'react';
import './ChatWindow.css';
import { MessageList } from '../MessageList/MessageList';
import { MessageInput } from '../MessageInput/MessageInput';
import { ErrorDisplay } from '../ErrorDisplay/ErrorDisplay';
import { chatService } from '../../../services/api';

const ChatWindow = ({
  sessionId = null,
  initialMessages = [],
  onSendMessage: onSendMessageProp,
  isLoading: loadingProp,
  error: errorProp
}) => {
  const [messages, setMessages] = useState(initialMessages);
  const [isLoading, setIsLoading] = useState(loadingProp || false);
  const [error, setError] = useState(errorProp || null);
  const [connectionStatus, setConnectionStatus] = useState('connected'); // connected, connecting, disconnected

  // Create or use session
  const [currentSessionId, setCurrentSessionId] = useState(sessionId);

  useEffect(() => {
    if (!currentSessionId) {
      createNewSession();
    }

    // Check connection status periodically
    checkConnection();
    const interval = setInterval(checkConnection, 30000); // every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const checkConnection = async () => {
    try {
      setConnectionStatus('connecting');
      await chatService.getHistory('test');
      setConnectionStatus('connected');
    } catch (err) {
      setConnectionStatus('disconnected');
      console.error('Connection check failed:', err);
    }
  };

  const createNewSession = async () => {
    try {
      const sessionData = await chatService.createSession({
        timestamp: new Date().toISOString(),
        metadata: { type: 'chat' }
      });
      setCurrentSessionId(sessionData.session_id);
    } catch (err) {
      console.error('Error creating session:', err);
      setError('Failed to create chat session');
    }
  };

  const handleSendMessage = async (message) => {
    if (!message.trim() || isLoading) return;

    // If a parent handler is provided, use it instead
    if (onSendMessageProp) {
      onSendMessageProp(message);
      return;
    }

    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      text: message,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Set timeout for API call
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Request timeout')), 30000)
      );

      // Send to backend
      const responsePromise = chatService.sendMessage({
        query: message,
        session_id: currentSessionId
      });

      const response = await Promise.race([responsePromise, timeoutPromise]);

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        text: response.response || response.answer || 'No response',
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
      const errorMessage = {
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

  const handleRetry = () => {
    setError(null);
    checkConnection();
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>AI Chat Assistant</h3>
        <div className={`connection-status connection-status--${connectionStatus}`}>
          {connectionStatus === 'connected' ? '● Connected' :
           connectionStatus === 'connecting' ? '○ Connecting...' : '○ Disconnected'}
        </div>
      </div>

      {error && (
        <ErrorDisplay
          error={{ message: error }}
          onRetry={handleRetry}
        />
      )}

      <MessageList messages={messages} />
      <MessageInput
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
};

export default ChatWindow;