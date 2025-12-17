import React, { useState } from 'react';

const Quiz = ({ question, options, correctAnswer, explanation, className = '' }) => {
  // Handle both array and string formats for options
  const parsedOptions = Array.isArray(options)
    ? options
    : options && typeof options === 'string'
      ? options.split('||')  // Use '||' as separator for string format
      : [];
  const [selectedOption, setSelectedOption] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);

  const handleSubmit = (option) => {
    if (submitted) return;

    setSelectedOption(option);
    const correct = option === correctAnswer;
    setIsCorrect(correct);
    setSubmitted(true);
  };

  const handleReset = () => {
    setSelectedOption(null);
    setSubmitted(false);
    setIsCorrect(false);
  };

  const getOptionStyle = (option) => {
    if (!submitted) {
      return {
        padding: '0.75rem',
        margin: '0.5rem 0',
        cursor: 'pointer',
        border: '1px solid #ddd',
        borderRadius: '4px',
        backgroundColor: selectedOption === option ? '#e3f2fd' : '#fff',
      };
    } else {
      if (option === correctAnswer) {
        return {
          padding: '0.75rem',
          margin: '0.5rem 0',
          border: '1px solid #4caf50',
          borderRadius: '4px',
          backgroundColor: '#e8f5e9',
          fontWeight: 'bold',
        };
      } else if (option === selectedOption && option !== correctAnswer) {
        return {
          padding: '0.75rem',
          margin: '0.5rem 0',
          border: '1px solid #f44336',
          borderRadius: '4px',
          backgroundColor: '#ffebee',
        };
      } else {
        return {
          padding: '0.75rem',
          margin: '0.5rem 0',
          border: '1px solid #ddd',
          borderRadius: '4px',
          backgroundColor: '#f5f5f5',
        };
      }
    }
  };

  return (
    <div className={`quiz-component ${className}`} style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '1rem',
      margin: '1rem 0',
      backgroundColor: '#fff',
    }}>
      <h4 style={{ margin: '0 0 1rem 0' }}>{question}</h4>

      <div>
        {parsedOptions.map((option, index) => (
          <div
            key={index}
            style={getOptionStyle(option)}
            onClick={() => handleSubmit(option)}
          >
            <input
              type="radio"
              name={`quiz-${question}`}
              value={option}
              checked={selectedOption === option}
              onChange={() => {}}
              disabled={submitted}
              style={{ marginRight: '0.5rem' }}
            />
            {option}
          </div>
        ))}
      </div>

      {submitted && (
        <div style={{
          marginTop: '1rem',
          padding: '0.75rem',
          borderRadius: '4px',
          backgroundColor: isCorrect ? '#e8f5e9' : '#ffebee',
          border: `1px solid ${isCorrect ? '#4caf50' : '#f44336'}`,
        }}>
          <p style={{ margin: '0.5rem 0', fontWeight: 'bold' }}>
            {isCorrect ? '✅ Correct!' : '❌ Incorrect'}
          </p>
          {explanation && (
            <p style={{ margin: '0.5rem 0' }}>
              <strong>Explanation:</strong> {explanation}
            </p>
          )}
        </div>
      )}

      {submitted ? (
        <button
          onClick={handleReset}
          style={{
            marginTop: '1rem',
            padding: '0.5rem 1rem',
            backgroundColor: '#2196f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Try Again
        </button>
      ) : (
        selectedOption && (
          <button
            onClick={() => handleSubmit(selectedOption)}
            style={{
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#4caf50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          >
            Submit Answer
          </button>
        )
      )}
    </div>
  );
};

export default Quiz;