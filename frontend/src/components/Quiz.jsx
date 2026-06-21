import React, { useState } from 'react';
import styles from './Quiz.module.css';

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

  const getOptionClassName = (option) => {
    const classes = [styles.quizOption];

    if (!submitted) {
      if (selectedOption === option) {
        classes.push(styles.quizOptionSelected);
      }
    } else {
      if (option === correctAnswer) {
        classes.push(styles.quizOptionCorrect);
      } else if (option === selectedOption && option !== correctAnswer) {
        classes.push(styles.quizOptionIncorrect);
      } else {
        classes.push(styles.quizOptionDisabled);
      }
    }

    return classes.join(' ');
  };

  return (
    <div className={`${styles.quizContainer} quiz-component ${className}`}>
      <h4 className={styles.quizQuestion}>{question}</h4>

      <div className={styles.quizOptionsContainer}>
        {parsedOptions.map((option, index) => (
          <div
            key={index}
            className={getOptionClassName(option)}
            onClick={() => handleSubmit(option)}
          >
            <input
              type="radio"
              name={`quiz-${question}`}
              value={option}
              checked={selectedOption === option}
              onChange={() => {}}
              disabled={submitted}
              className={styles.quizOptionInput}
            />
            {option}
          </div>
        ))}
      </div>

      {submitted && (
        <div className={`${styles.feedbackBox} ${isCorrect ? styles.feedbackBoxCorrect : styles.feedbackBoxIncorrect}`}>
          <p className={styles.feedbackMessage}>
            {isCorrect ? '✅ Correct!' : '❌ Incorrect'}
          </p>
          {explanation && (
            <p className={styles.feedbackExplanation}>
              <strong>Explanation:</strong> {explanation}
            </p>
          )}
        </div>
      )}

      {submitted ? (
        <button
          onClick={handleReset}
          className={`${styles.quizButton} ${styles.quizButtonSecondary}`}
        >
          Try Again
        </button>
      ) : (
        selectedOption && (
          <button
            onClick={() => handleSubmit(selectedOption)}
            className={`${styles.quizButton} ${styles.quizButtonSuccess}`}
          >
            Submit Answer
          </button>
        )
      )}
    </div>
  );
};

export default Quiz;
