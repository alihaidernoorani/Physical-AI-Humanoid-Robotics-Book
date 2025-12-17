import React, { useState } from 'react';

const Exercise = ({
  title,
  problem,
  solution,
  hints = [],
  initialCode = '',
  className = ''
}) => {
  const [code, setCode] = useState(initialCode);
  const [showSolution, setShowSolution] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);

  const handleRunCode = () => {
    // In a real implementation, this would execute the code
    // For now, we'll just show a message
    setResult({
      success: true,
      message: "Code executed successfully! Check your logic against the solution."
    });
    setSubmitted(true);
  };

  const handleReset = () => {
    setCode(initialCode);
    setShowSolution(false);
    setShowHint(false);
    setSubmitted(false);
    setResult(null);
  };

  return (
    <div className={`exercise-component ${className}`} style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '1rem',
      margin: '1rem 0',
      backgroundColor: '#fff',
    }}>
      <h4 style={{ margin: '0 0 1rem 0' }}>{title}</h4>

      <div style={{ marginBottom: '1rem' }}>
        <h5 style={{ margin: '0.5rem 0', color: '#202124' }}>Problem:</h5>
        <div style={{ padding: '0.5rem', backgroundColor: '#f9f9f9', borderRadius: '4px' }}>
          {problem}
        </div>
      </div>

      {hints.length > 0 && (
        <div style={{ marginBottom: '1rem' }}>
          <button
            onClick={() => setShowHint(!showHint)}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#fbbc04',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              marginBottom: '0.5rem'
            }}
          >
            {showHint ? 'Hide Hint' : 'Show Hint'}
          </button>
          {showHint && (
            <div style={{
              padding: '0.5rem',
              backgroundColor: '#fef7e0',
              borderRadius: '4px',
              border: '1px solid #fbbc04'
            }}>
              <strong>Hint:</strong> {hints[0]}
            </div>
          )}
        </div>
      )}

      <div style={{ marginBottom: '1rem' }}>
        <h5 style={{ margin: '0.5rem 0', color: '#202124' }}>Your Solution:</h5>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          style={{
            width: '100%',
            minHeight: '150px',
            padding: '0.5rem',
            fontFamily: 'monospace',
            border: '1px solid #ddd',
            borderRadius: '4px',
            fontSize: '0.9rem'
          }}
          placeholder="Write your solution here..."
        />
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <button
          onClick={handleRunCode}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#4caf50',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Run Code
        </button>
        <button
          onClick={() => setShowSolution(!showSolution)}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#2196f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          {showSolution ? 'Hide Solution' : 'Show Solution'}
        </button>
        <button
          onClick={handleReset}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#9e9e9e',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Reset
        </button>
      </div>

      {submitted && result && (
        <div style={{
          padding: '0.75rem',
          borderRadius: '4px',
          backgroundColor: result.success ? '#e8f5e9' : '#ffebee',
          border: `1px solid ${result.success ? '#4caf50' : '#f44336'}`,
          marginBottom: '1rem'
        }}>
          <strong>Status:</strong> {result.message}
        </div>
      )}

      {showSolution && (
        <div style={{
          padding: '0.5rem',
          backgroundColor: '#e8f5e9',
          borderRadius: '4px',
          border: '1px solid #4caf50'
        }}>
          <h5 style={{ margin: '0.5rem 0', color: '#202124' }}>Solution:</h5>
          <pre style={{
            padding: '0.5rem',
            backgroundColor: '#f1f8e9',
            borderRadius: '4px',
            overflowX: 'auto',
            whiteSpace: 'pre-wrap'
          }}>
            {solution}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Exercise;