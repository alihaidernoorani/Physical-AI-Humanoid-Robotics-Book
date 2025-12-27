import React, { useState, useRef, useEffect, useCallback } from 'react';
import ChatApi from '../../services/chatApi';
import './ChatWindow.css';

// Constants for validation
const MAX_MESSAGE_LENGTH = 2000;

// Generate unique temporary ID to prevent React key collisions
const generateTempId = () => `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chatMode, setChatMode] = useState('full_text');
  const [selectedText, setSelectedText] = useState('');
  const [validationError, setValidationError] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when messages change
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Input validation
  const validateInput = (text) => {
    if (!text || !text.trim()) {
      return 'Please enter a message';
    }
    if (text.length > MAX_MESSAGE_LENGTH) {
      return `Message too long. Maximum ${MAX_MESSAGE_LENGTH} characters allowed.`;
    }
    return null;
  };

  // Handle input change with validation
  const handleInputChange = (e) => {
    const value = e.target.value;
    setInputValue(value);

    // Clear validation error when user starts typing
    if (validationError) {
      setValidationError('');
    }

    // Show warning if approaching limit
    if (value.length > MAX_MESSAGE_LENGTH) {
      setValidationError(`Message too long (${value.length}/${MAX_MESSAGE_LENGTH})`);
    }
  };

  // Retry handler for failed messages
  const handleRetry = async (failedMessage) => {
    // Remove the error message
    setMessages(prev => prev.filter(m => m.id !== failedMessage.id));

    // Re-submit the original message
    setInputValue(failedMessage.originalText || '');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate input
    const error = validateInput(inputValue);
    if (error) {
      setValidationError(error);
      return;
    }

    if (isLoading) return;

    const messageText = inputValue.trim();

    // Generate unique temporary ID for optimistic update
    const tempUserId = generateTempId();

    // OPTIMISTIC UPDATE: Add user message immediately before API call
    const userMessage = {
      id: tempUserId,
      text: messageText,
      sender: 'user',
      timestamp: new Date(),
      status: 'sent'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setValidationError('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await ChatApi.chat(messageText, chatMode, selectedText);

      // Generate unique ID for bot response
      const botId = generateTempId();

      const botMessage = {
        id: botId,
        text: response.response,
        sender: 'bot',
        citations: response.citations || [],
        confidence: response.grounding_confidence,
        timestamp: new Date(),
        status: 'received'
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);

      // Generate unique ID for error message
      const errorId = generateTempId();

      const errorMessage = {
        id: errorId,
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'bot',
        error: true,
        canRetry: true,
        originalText: messageText,
        timestamp: new Date(),
        status: 'error'
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextSelection = () => {
    const selected = window.getSelection().toString().trim();
    if (selected) {
      setSelectedText(selected);
      setChatMode('selected_text');
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>Textbook Assistant</h3>
        <div className="chat-mode-selector">
          <button
            className={chatMode === 'full_text' ? 'active' : ''}
            onClick={() => setChatMode('full_text')}
          >
            Full Textbook
          </button>
          <button
            className={chatMode === 'selected_text' ? 'active' : ''}
            onClick={handleTextSelection}
          >
            Selected Text
          </button>
        </div>
        {chatMode === 'selected_text' && selectedText && (
          <div className="selected-text-preview">
            <small>Selected: {selectedText.substring(0, 60)}{selectedText.length > 60 ? '...' : ''}</small>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your textbook assistant. Ask me questions about the Physical AI & Humanoid Robotics content.</p>
            <p>You can switch between "Full Textbook" mode (searches entire book) and "Selected Text" mode (answers based only on highlighted text).</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}${message.error ? ' error-message' : ''}`}
            >
              <div className="message-content">
                <p>{message.text}</p>
                {message.citations && message.citations.length > 0 && (
                  <div className="citations">
                    <small>Sources: {message.citations.join(', ')}</small>
                  </div>
                )}
                {message.confidence !== undefined && (
                  <div className="confidence">
                    <small>Confidence: {(message.confidence * 100).toFixed(1)}%</small>
                  </div>
                )}
                {message.error && message.canRetry && (
                  <div className="error-actions">
                    <button
                      className="retry-button"
                      onClick={() => handleRetry(message)}
                    >
                      Try Again
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form">
        <div className="input-wrapper">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder={chatMode === 'selected_text' ? "Ask about selected text..." : "Ask a question about the textbook..."}
            disabled={isLoading}
            maxLength={MAX_MESSAGE_LENGTH + 100}
          />
          {validationError && (
            <div className="validation-error">{validationError}</div>
          )}
          <div className="char-count">
            {inputValue.length}/{MAX_MESSAGE_LENGTH}
          </div>
        </div>
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim() || inputValue.length > MAX_MESSAGE_LENGTH}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;
