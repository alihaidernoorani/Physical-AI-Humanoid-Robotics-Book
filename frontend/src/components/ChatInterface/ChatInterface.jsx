import React, { useState, useEffect, useRef } from 'react';
import { ragService } from '../../services/api';
import { RAGModeSelector } from '../RAGModeSelector/RAGModeSelector';
import './ChatInterface.css';

const ChatInterface = ({ mode = 'full-book', selectedText = null }) => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentMode, setCurrentMode] = useState(mode);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setError(null);

    try {
      // Prepare query data based on current mode
      const queryData = {
        query_text: inputText,
        retrieval_mode: currentMode,
      };

      // Add selected text if in per-page mode
      if (currentMode === 'per-page' && selectedText) {
        queryData.selected_text = selectedText;
      }

      // Call the RAG service
      const response = await ragService.query(queryData);

      // Add AI response to chat
      const aiMessage = {
        id: Date.now() + 1,
        text: response.response_text,
        sender: 'ai',
        timestamp: new Date(),
        citations: response.citations || [],
        confidence_score: response.confidence_score,
        is_fallback: response.is_fallback
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Error getting RAG response:', err);
      setError('Failed to get response. Please try again.');

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your request. Please try again.',
        sender: 'system',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleModeChange = (newMode) => {
    setCurrentMode(newMode);
    setMessages([]); // Clear chat when mode changes
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>RAG Chatbot</h3>
        <RAGModeSelector
          currentMode={currentMode}
          onModeChange={handleModeChange}
          disabled={isLoading}
        />
        <div className="current-mode-indicator">
          <small>Mode: <strong>{currentMode === 'full-book' ? 'Full Book' : 'Per Page'}</strong></small>
        </div>
        {currentMode === 'per-page' && selectedText && (
          <div className="selected-text-preview">
            <small>Selected: {selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}</small>
          </div>
        )}
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Hello! I'm your RAG assistant for the Physical AI & Humanoid Robotics textbook.</p>
            <p>Ask me questions about the content, and I'll provide answers based on the textbook material.</p>
            <p>Currently in <strong>{currentMode === 'full-book' ? 'Full Book' : 'Per Page'}</strong> mode.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender}-message`}
            >
              <div className="message-content">
                <p>{message.text}</p>

                {message.sender === 'ai' && message.citations && message.citations.length > 0 && (
                  <div className="citations">
                    <h4>Sources:</h4>
                    <ul>
                      {message.citations.slice(0, 3).map((citation, index) => (
                        <li key={index}>
                          <strong>{citation.module}</strong> - {citation.chapter}
                          {citation.subsection && ` - ${citation.subsection}`}
                          {citation.page_reference && ` (Page/Section: ${citation.page_reference})`}
                        </li>
                      ))}
                    </ul>
                    {message.citations.length > 3 && (
                      <p className="more-citations">+ {message.citations.length - 3} more sources</p>
                    )}
                  </div>
                )}

                {message.sender === 'ai' && message.confidence_score !== undefined && (
                  <div className="confidence-score">
                    Confidence: {Math.round(message.confidence_score * 100)}%
                    {message.is_fallback && <span className="fallback-indicator"> (Fallback response)</span>}
                  </div>
                )}
              </div>
              <div className="timestamp">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai-message">
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
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask a question about the textbook content..."
          disabled={isLoading}
          rows={3}
        />
        <button type="submit" disabled={!inputText.trim() || isLoading}>
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  );
};

export default ChatInterface;