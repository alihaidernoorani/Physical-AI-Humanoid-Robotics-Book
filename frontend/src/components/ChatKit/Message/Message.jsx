import React from 'react';
import './Message.css';

const Message = ({ message }) => {
  const { text, sender, timestamp, citations } = message;

  const formatTime = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={`message message--${sender}`}>
      <div className="message__content">
        <div className="message__text">{text}</div>

        {citations && citations.length > 0 && (
          <div className="message__citations">
            <details>
              <summary>Citations</summary>
              <ul>
                {citations.map((citation, index) => (
                  <li key={index}>{citation}</li>
                ))}
              </ul>
            </details>
          </div>
        )}
      </div>

      <div className="message__meta">
        <span className="message__time">{formatTime(timestamp)}</span>
      </div>
    </div>
  );
};

export { Message };