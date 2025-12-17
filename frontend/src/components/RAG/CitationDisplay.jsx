import React from 'react';

const CitationDisplay = ({ citations, className = '' }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  return (
    <div className={`citation-display ${className}`}>
      <h4>Source Citations:</h4>
      <ul>
        {citations.map((citation, index) => (
          <li key={index} className="citation-item">
            <span className="citation-path">{citation}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CitationDisplay;