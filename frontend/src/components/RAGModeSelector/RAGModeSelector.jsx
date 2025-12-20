import React from 'react';
import './RAGModeSelector.css';

const RAGModeSelector = ({ currentMode, onModeChange, disabled = false }) => {
  const modes = [
    { value: 'full-book', label: 'Full Book', description: 'Search across the entire textbook' },
    { value: 'per-page', label: 'Per Page', description: 'Search only within selected text' }
  ];

  return (
    <div className="rag-mode-selector">
      <div className="mode-options">
        {modes.map((mode) => (
          <button
            key={mode.value}
            className={`mode-option ${currentMode === mode.value ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
            onClick={() => !disabled && onModeChange(mode.value)}
            disabled={disabled}
            aria-pressed={currentMode === mode.value}
            aria-label={`${mode.label} mode ${currentMode === mode.value ? '(selected)' : ''}`}
          >
            <div className="mode-header">
              <span className="mode-label">{mode.label}</span>
              {currentMode === mode.value && <span className="active-indicator">●</span>}
            </div>
            <div className="mode-description">{mode.description}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

// Alternative compact version for smaller spaces
const CompactRAGModeSelector = ({ currentMode, onModeChange, disabled = false }) => {
  return (
    <div className="compact-rag-mode-selector">
      <label htmlFor="rag-mode-select" className="mode-label">Search Mode:</label>
      <select
        id="rag-mode-select"
        value={currentMode}
        onChange={(e) => onModeChange(e.target.value)}
        disabled={disabled}
        className="mode-select"
      >
        <option value="full-book">Full Book</option>
        <option value="per-page">Per Page</option>
      </select>
    </div>
  );
};

// Toggle switch version
const ToggleRAGModeSelector = ({ currentMode, onModeChange, disabled = false }) => {
  return (
    <div className="toggle-rag-mode-selector">
      <span className={`mode-label ${currentMode === 'full-book' ? 'active' : ''}`}>
        Full Book
      </span>

      <label className="switch">
        <input
          type="checkbox"
          checked={currentMode === 'per-page'}
          onChange={(e) => onModeChange(e.target.checked ? 'per-page' : 'full-book')}
          disabled={disabled}
        />
        <span className="slider round"></span>
      </label>

      <span className={`mode-label ${currentMode === 'per-page' ? 'active' : ''}`}>
        Per Page
      </span>
    </div>
  );
};

export { RAGModeSelector, CompactRAGModeSelector, ToggleRAGModeSelector };
export default RAGModeSelector;