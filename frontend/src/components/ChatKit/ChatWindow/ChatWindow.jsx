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
  // Use messages from props as source of truth, not local state
  const [messages, setMessages] = useState(initialMessages);
  const [error, setError] = useState(errorProp || null);
  const [connectionStatus, setConnectionStatus] = useState('connected'); // connected, connecting, disconnected

  // Sync messages with parent when they change
  useEffect(() => {
    setMessages(initialMessages);
  }, [initialMessages]);

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
    if (!message.trim() || loadingProp) return;

    // Always delegate to parent handler
    if (onSendMessageProp) {
      onSendMessageProp(message);
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

      {(error || errorProp) && (
        <ErrorDisplay
          error={{ message: error || errorProp }}
          onRetry={handleRetry}
        />
      )}

      <MessageList messages={messages} />
      <MessageInput
        onSendMessage={handleSendMessage}
        isLoading={loadingProp}
      />
    </div>
  );
};

export default ChatWindow;