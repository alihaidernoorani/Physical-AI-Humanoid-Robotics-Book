import React, { useState, useEffect } from 'react';
import { useAuth } from '../components/auth/AuthContext';

const PersonalizationButton = () => {
  const { profile, isAuthenticated, isInitialized } = useAuth();
  const [showModal, setShowModal] = useState(false);

  if (!isInitialized) {
    return null; // Don't render until auth is initialized
  }

  const handleClick = () => {
    if (!isAuthenticated) {
      setShowModal(true);
    } else {
      // For now, just show a simple alert - in the future this could open personalization options
      alert(`Current profile: ${profile.softwareExperience} level, ${profile.learningStyle} learner`);
    }
  };

  if (!isAuthenticated) {
    return (
      <div style={{ marginBottom: '1.5rem' }}>
        <button
          onClick={handleClick}
          style={{
            backgroundColor: '#4285f4',
            color: 'white',
            border: 'none',
            padding: '0.5rem 1rem',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '0.9rem'
          }}
        >
          Personalize This Chapter
        </button>
        {showModal && (
          <div className="modal-overlay" style={{
            position: 'fixed',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: 1000
          }}>
            <div className="modal-content" style={{
              backgroundColor: 'white',
              padding: '2rem',
              borderRadius: '8px',
              maxWidth: '500px',
              width: '90%',
              maxHeight: '90vh',
              overflowY: 'auto'
            }}>
              <h3>Complete Your Profile</h3>
              <p>Please complete your profile to enable personalization features.</p>
              <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                <button
                  onClick={() => setShowModal(false)}
                  style={{
                    padding: '0.5rem 1rem',
                    border: '1px solid #ccc',
                    borderRadius: '4px',
                    backgroundColor: '#f5f5f5',
                    cursor: 'pointer'
                  }}
                >
                  Later
                </button>
                <button
                  onClick={() => {
                    setShowModal(false);
                    // Redirect to profile completion
                    window.location.hash = '#profile-modal';
                  }}
                  style={{
                    padding: '0.5rem 1rem',
                    border: 'none',
                    borderRadius: '4px',
                    backgroundColor: '#007cba',
                    color: 'white',
                    cursor: 'pointer'
                  }}
                >
                  Complete Now
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={{ marginBottom: '1.5rem' }}>
      <button
        onClick={handleClick}
        style={{
          backgroundColor: '#34a853',
          color: 'white',
          border: 'none',
          padding: '0.5rem 1rem',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '0.9rem'
        }}
      >
        Personalization Active: {profile.softwareExperience}
      </button>
    </div>
  );
};

export default PersonalizationButton;