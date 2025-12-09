import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const UserProfileModal = ({ isOpen, onClose, onSubmit }) => {
  const { profile, setProfile } = useAuth();
  const [formData, setFormData] = useState({
    softwareExperience: profile?.softwareExperience || 'Beginner',
    hardwareSetup: profile?.hardwareSetup || '',
    learningStyle: profile?.learningStyle || 'Visual'
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newProfile = {
      ...formData,
      id: profile?.id || Date.now().toString(),
      createdAt: profile?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    setProfile(newProfile);
    if (onSubmit) onSubmit(newProfile);
    onClose();
  };

  if (!isOpen) return null;

  return (
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
        <h2 style={{ marginBottom: '1.5rem' }}>Complete Your Profile</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Software Experience
            </label>
            <select
              name="softwareExperience"
              value={formData.softwareExperience}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Hardware Setup
            </label>
            <input
              type="text"
              name="hardwareSetup"
              value={formData.hardwareSetup}
              onChange={handleChange}
              placeholder="e.g., Jetson Orin, RTX GPU, etc."
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
            />
          </div>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
              Learning Style
            </label>
            <select
              name="learningStyle"
              value={formData.learningStyle}
              onChange={handleChange}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ccc',
                borderRadius: '4px'
              }}
            >
              <option value="Visual">Visual</option>
              <option value="Text-based">Text-based</option>
              <option value="Hands-on">Hands-on</option>
            </select>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: '0.5rem 1rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                backgroundColor: '#f5f5f5',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              style={{
                padding: '0.5rem 1rem',
                border: 'none',
                borderRadius: '4px',
                backgroundColor: '#007cba',
                color: 'white',
                cursor: 'pointer'
              }}
            >
              Save Profile
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserProfileModal;