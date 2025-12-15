import React, { useState } from 'react';

const Glossary = ({ terms = [], className = '' }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedTerm, setExpandedTerm] = useState(null);

  const filteredTerms = terms.filter(term =>
    term.term.toLowerCase().includes(searchTerm.toLowerCase()) ||
    term.definition.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleTerm = (termKey) => {
    setExpandedTerm(expandedTerm === termKey ? null : termKey);
  };

  return (
    <div className={`glossary-component ${className}`} style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '1rem',
      margin: '1rem 0',
      backgroundColor: '#fff',
    }}>
      <h3 style={{ margin: '0 0 1rem 0', color: '#202124' }}>Glossary</h3>

      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search terms..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '0.5rem',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '1rem'
          }}
        />
      </div>

      <div>
        {filteredTerms.length > 0 ? (
          filteredTerms.map((termObj, index) => (
            <div key={index} style={{ marginBottom: '0.5rem' }}>
              <div
                style={{
                  padding: '0.75rem',
                  backgroundColor: '#f8f9fa',
                  border: '1px solid #eee',
                  borderRadius: '4px',
                  cursor: 'pointer',
                }}
                onClick={() => toggleTerm(`${termObj.term}-${index}`)}
              >
                <strong style={{ color: '#1a73e8' }}>{termObj.term}</strong>
                {expandedTerm === `${termObj.term}-${index}` ? (
                  <div style={{ marginTop: '0.5rem', paddingLeft: '0.5rem' }}>
                    <p style={{ margin: '0.5rem 0 0 0' }}>{termObj.definition}</p>
                    {termObj.example && (
                      <p style={{ margin: '0.5rem 0', fontStyle: 'italic', color: '#5f6368' }}>
                        <strong>Example:</strong> {termObj.example}
                      </p>
                    )}
                  </div>
                ) : (
                  <span style={{ marginLeft: '0.5rem', color: '#5f6368', fontSize: '0.9rem' }}>
                    - {termObj.definition.substring(0, 60)}...
                  </span>
                )}
              </div>
            </div>
          ))
        ) : (
          <p style={{ textAlign: 'center', color: '#666', fontStyle: 'italic' }}>
            No terms match your search.
          </p>
        )}
      </div>

      {terms.length === 0 && (
        <p style={{ textAlign: 'center', color: '#666', fontStyle: 'italic' }}>
          No glossary terms defined yet.
        </p>
      )}
    </div>
  );
};

export default Glossary;