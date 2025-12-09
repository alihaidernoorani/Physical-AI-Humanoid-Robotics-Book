import React from 'react';
import { useAuth } from './AuthContext';

interface PersonalizeButtonProps {
  onPersonalizeClick?: () => void;
}

const PersonalizeButton: React.FC<PersonalizeButtonProps> = ({ onPersonalizeClick }) => {
  const { user, isAuthenticated } = useAuth();

  const handleClick = () => {
    if (!isAuthenticated) {
      alert('Please log in or create an account to personalize your learning experience.');
      return;
    }
    if (onPersonalizeClick) {
      onPersonalizeClick();
    } else {
      // Default behavior could be to show profile manager or personalization options
      alert('Personalization options would appear here based on your profile.');
    }
  };

  return (
    <button
      onClick={handleClick}
      style={{
        padding: '0.5rem 1rem',
        backgroundColor: '#4285f4',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        marginBottom: '1rem',
        display: 'inline-block'
      }}
    >
      {isAuthenticated ? 'Personalize This Chapter' : 'Login to Personalize'}
    </button>
  );
};

export default PersonalizeButton;