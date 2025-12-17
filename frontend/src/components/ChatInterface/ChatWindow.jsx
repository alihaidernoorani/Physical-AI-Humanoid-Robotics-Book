import React, { useState, useRef, useEffect } from 'react';
import ChatApi from '../../services/chatApi';
import './ChatWindow.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [chatMode, setChatMode] = useState('full_text'); // 'full_text' or 'selected_text'
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await ChatApi.chat(inputValue, chatMode, selectedText);

      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        citations: response.citations || [],
        confidence: response.grounding_confidence,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'bot',
        error: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
      setChatMode('selected_text');
      // Optionally show a notification that text has been captured
      console.log('Selected text captured:', selectedText);
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
              className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
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
                {message.error && (
                  <div className="error">
                    <small>Error occurred - please try again</small>
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
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={chatMode === 'selected_text' ? "Ask about selected text..." : "Ask a question about the textbook..."}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !inputValue.trim()}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatWindow;