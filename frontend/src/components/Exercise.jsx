import React, { useState } from 'react';
import styles from './Exercise.module.css';

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
    <div className={`${styles.exerciseContainer} exercise-component ${className}`}>
      <h4 className={styles.exerciseTitle}>{title}</h4>

      <div className={styles.exerciseSection}>
        <h5 className={styles.exerciseSectionTitle}>Problem:</h5>
        <div className={styles.exerciseProblemBox}>
          {problem}
        </div>
      </div>

      {hints.length > 0 && (
        <div className={styles.exerciseSection}>
          <button
            onClick={() => setShowHint(!showHint)}
            className={`${styles.exerciseButton} ${styles.exerciseButtonHint}`}
          >
            {showHint ? 'Hide Hint' : 'Show Hint'}
          </button>
          {showHint && (
            <div className={styles.exerciseHintBox}>
              <strong>Hint:</strong> {hints[0]}
            </div>
          )}
        </div>
      )}

      <div className={styles.exerciseSection}>
        <h5 className={styles.exerciseSectionTitle}>Your Solution:</h5>
        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className={styles.exerciseTextarea}
          placeholder="Write your solution here..."
        />
      </div>

      <div className={styles.exerciseButtonGroup}>
        <button
          onClick={handleRunCode}
          className={`${styles.exerciseButton} ${styles.exerciseButtonRun}`}
        >
          Run Code
        </button>
        <button
          onClick={() => setShowSolution(!showSolution)}
          className={`${styles.exerciseButton} ${styles.exerciseButtonShow}`}
        >
          {showSolution ? 'Hide Solution' : 'Show Solution'}
        </button>
        <button
          onClick={handleReset}
          className={`${styles.exerciseButton} ${styles.exerciseButtonReset}`}
        >
          Reset
        </button>
      </div>

      {submitted && result && (
        <div className={`${styles.exerciseResultBox} ${result.success ? styles.exerciseResultSuccess : styles.exerciseResultError}`}>
          <strong>Status:</strong> {result.message}
        </div>
      )}

      {showSolution && (
        <div className={styles.exerciseSolutionBox}>
          <h5 className={styles.exerciseSectionTitle}>Solution:</h5>
          <pre className={styles.exerciseSolutionCode}>
            {solution}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Exercise;
