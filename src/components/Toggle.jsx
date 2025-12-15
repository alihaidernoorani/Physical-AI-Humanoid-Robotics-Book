import React, { useState, useEffect } from 'react';
import { useColorMode } from '@docusaurus/theme-common';

const Toggle = ({ children, className = '' }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const { isDarkTheme } = useColorMode();

  // Determine content based on current language
  const getContent = () => {
    if (typeof children === 'object' && children !== null) {
      return children[currentLanguage] || children['en'] || 'Content not available';
    }
    return children;
  };

  // Toggle between languages
  const toggleLanguage = () => {
    setCurrentLanguage(prev => prev === 'en' ? 'ur' : 'en');
  };

  // Set initial language preference from localStorage
  useEffect(() => {
    const savedLanguage = localStorage.getItem('preferred-language');
    if (savedLanguage && (savedLanguage === 'en' || savedLanguage === 'ur')) {
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  // Save language preference to localStorage
  useEffect(() => {
    localStorage.setItem('preferred-language', currentLanguage);
  }, [currentLanguage]);

  const toggleStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '1rem',
    padding: '0.5rem',
    borderRadius: '4px',
    backgroundColor: isDarkTheme ? '#2a2a2a' : '#f5f5f5',
    border: `1px solid ${isDarkTheme ? '#444' : '#ddd'}`,
  };

  const buttonStyle = {
    padding: '0.25rem 0.75rem',
    margin: '0 0.25rem',
    border: 'none',
    borderRadius: '3px',
    cursor: 'pointer',
    backgroundColor: currentLanguage === 'en' ? (isDarkTheme ? '#007acc' : '#007cba') : (isDarkTheme ? '#333' : '#e0e0e0'),
    color: currentLanguage === 'en' ? '#fff' : (isDarkTheme ? '#fff' : '#333'),
    fontWeight: currentLanguage === 'en' ? 'bold' : 'normal',
  };

  const urduButtonStyle = {
    ...buttonStyle,
    backgroundColor: currentLanguage === 'ur' ? (isDarkTheme ? '#007acc' : '#007cba') : (isDarkTheme ? '#333' : '#e0e0e0'),
    color: currentLanguage === 'ur' ? '#fff' : (isDarkTheme ? '#fff' : '#333'),
    fontWeight: currentLanguage === 'ur' ? 'bold' : 'normal',
  };

  return (
    <div className={`language-toggle ${className}`} style={toggleStyle}>
      <button
        onClick={() => setCurrentLanguage('en')}
        style={buttonStyle}
        aria-label="Switch to English"
      >
        English
      </button>
      <span style={{ margin: '0 0.5rem', color: isDarkTheme ? '#aaa' : '#666' }}>|</span>
      <button
        onClick={() => setCurrentLanguage('ur')}
        style={urduButtonStyle}
        aria-label="Switch to Urdu"
      >
        اردو
      </button>
      <div className="content" style={{ width: '100%', marginTop: '0.5rem' }}>
        {getContent()}
      </div>
    </div>
  );
};

export default Toggle;