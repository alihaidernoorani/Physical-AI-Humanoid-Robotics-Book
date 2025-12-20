import React from 'react';
import './MessageList.css';
import { Message } from '../Message/Message';

const MessageList = ({ messages = [] }) => {
  return (
    <div className="message-list">
      {messages.length === 0 ? (
        <div className="empty-state">
          <p>Start a conversation by sending a message below!</p>
        </div>
      ) : (
        messages.map((message) => (
          <Message
            key={message.id || message.timestamp}
            message={message}
          />
        ))
      )}
    </div>
  );
};

export { MessageList };