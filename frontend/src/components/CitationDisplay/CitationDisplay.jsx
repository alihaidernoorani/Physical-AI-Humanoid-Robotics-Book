import React from 'react';
import './CitationDisplay.css';

const CitationDisplay = ({ citations, maxCitations = 5 }) => {
  if (!citations || citations.length === 0) {
    return (
      <div className="citation-display">
        <p className="no-citations">No citations available for this response.</p>
      </div>
    );
  }

  // Limit the number of citations displayed
  const displayedCitations = citations.slice(0, maxCitations);
  const hasMoreCitations = citations.length > maxCitations;

  return (
    <div className="citation-display">
      <h4 className="citations-title">Sources Referenced:</h4>
      <ul className="citations-list">
        {displayedCitations.map((citation, index) => (
          <li key={index} className="citation-item">
            <div className="citation-content">
              <div className="citation-module">
                <strong>{citation.module || 'Unknown Module'}</strong>
              </div>
              <div className="citation-details">
                {citation.chapter && (
                  <span className="citation-chapter">{citation.chapter}</span>
                )}
                {citation.subsection && (
                  <span className="citation-subsection"> • {citation.subsection}</span>
                )}
                {citation.page_reference && (
                  <span className="citation-page"> • Page/Section: {citation.page_reference}</span>
                )}
              </div>
              {citation.chunk_id && (
                <div className="citation-id">
                  ID: {citation.chunk_id.substring(0, 8)}...
                </div>
              )}
            </div>
          </li>
        ))}
      </ul>
      {hasMoreCitations && (
        <div className="more-citations">
          + {citations.length - maxCitations} more source{citations.length - maxCitations > 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
};

// Component to display citations in a compact format (e.g., for inline citations)
const CompactCitationDisplay = ({ citations, maxCitations = 3 }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  const displayedCitations = citations.slice(0, maxCitations);
  const hasMoreCitations = citations.length > maxCitations;

  return (
    <div className="compact-citation-display">
      <span className="citation-label">Sources:</span>
      {displayedCitations.map((citation, index) => (
        <span key={index} className="compact-citation">
          {citation.module}{citation.chapter ? ` - ${citation.chapter}` : ''}
          {index < displayedCitations.length - 1 && ', '}
        </span>
      ))}
      {hasMoreCitations && (
        <span className="more-citations"> and {citations.length - maxCitations} more</span>
      )}
    </div>
  );
};

// Component to display citation statistics
const CitationStats = ({ citations }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  // Group citations by module
  const moduleCounts = {};
  citations.forEach(citation => {
    const module = citation.module || 'Unknown Module';
    moduleCounts[module] = (moduleCounts[module] || 0) + 1;
  });

  const modules = Object.keys(moduleCounts);
  const totalCitations = citations.length;

  return (
    <div className="citation-stats">
      <div className="stat-item">
        <span className="stat-label">Total Sources:</span>
        <span className="stat-value">{totalCitations}</span>
      </div>
      <div className="stat-item">
        <span className="stat-label">Modules Covered:</span>
        <span className="stat-value">{modules.length}</span>
      </div>
      {modules.length > 0 && (
        <div className="stat-item">
          <span className="stat-label">Primary Module:</span>
          <span className="stat-value">{modules[0]}</span>
        </div>
      )}
    </div>
  );
};

export { CitationDisplay, CompactCitationDisplay, CitationStats };
export default CitationDisplay;