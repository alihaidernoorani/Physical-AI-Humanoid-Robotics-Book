import React from 'react';
import './ErrorDisplay.css';

const ErrorDisplay = ({ error, onRetry = null, showRetry = true }) => {
  if (!error) return null;

  return (
    <div className="error-display">
      <div className="error-display__content">
        <div className="error-display__icon">⚠️</div>
        <div className="error-display__message">
          <h4>Error</h4>
          <p>{error.message || error || 'An unknown error occurred'}</p>
        </div>
        {onRetry && showRetry && (
          <button className="error-display__retry-button" onClick={onRetry}>
            Retry
          </button>
        )}
      </div>
    </div>
  );
};

export { ErrorDisplay };