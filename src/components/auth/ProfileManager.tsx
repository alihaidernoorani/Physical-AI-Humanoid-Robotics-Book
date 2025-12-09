import React, { useState } from 'react';
import { useAuth } from './AuthContext';

const ProfileManager: React.FC = () => {
  const { user, updateUserProfile, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editProfile, setEditProfile] = useState({
    softwareExperience: user?.softwareExperience || 'Beginner',
    hardwareSetup: user?.hardwareSetup || 'Jetson Orin',
    learningStyle: user?.learningStyle || 'Visual',
  });

  if (!user) {
    return null; // Don't show profile manager if not logged in
  }

  const handleSave = () => {
    updateUserProfile(editProfile);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditProfile({
      softwareExperience: user.softwareExperience,
      hardwareSetup: user.hardwareSetup,
      learningStyle: user.learningStyle,
    });
    setIsEditing(false);
  };

  return (
    <div style={{
      padding: '1rem',
      border: '1px solid #ddd',
      borderRadius: '8px',
      backgroundColor: '#f9f9f9',
      marginBottom: '1rem'
    }}>
      <h3 style={{ marginBottom: '1rem' }}>Your Profile</h3>

      <div style={{ marginBottom: '0.5rem' }}>
        <strong>Name:</strong> {user.name}
      </div>
      <div style={{ marginBottom: '0.5rem' }}>
        <strong>Email:</strong> {user.email}
      </div>

      {isEditing ? (
        <div style={{ marginTop: '1rem' }}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              <strong>Software Experience:</strong>
            </label>
            <select
              value={editProfile.softwareExperience}
              onChange={(e) => setEditProfile({...editProfile, softwareExperience: e.target.value})}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
            >
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              <strong>Hardware Setup:</strong>
            </label>
            <select
              value={editProfile.hardwareSetup}
              onChange={(e) => setEditProfile({...editProfile, hardwareSetup: e.target.value})}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
            >
              <option value="Jetson Orin">NVIDIA Jetson Orin</option>
              <option value="RTX GPU">NVIDIA RTX GPU</option>
              <option value="Laptop">Laptop with discrete GPU</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              <strong>Learning Style:</strong>
            </label>
            <select
              value={editProfile.learningStyle}
              onChange={(e) => setEditProfile({...editProfile, learningStyle: e.target.value})}
              style={{
                width: '100%',
                padding: '0.5rem',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
            >
              <option value="Visual">Visual Learner</option>
              <option value="Hands-on">Hands-on Learner</option>
              <option value="Theoretical">Theoretical Learner</option>
            </select>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              onClick={handleSave}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: '#4285f4',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              style={{
                padding: '0.5rem 1rem',
                backgroundColor: '#f0f0f0',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '0.5rem' }}>
            <strong>Software Experience:</strong> {user.softwareExperience}
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <strong>Hardware Setup:</strong> {user.hardwareSetup}
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <strong>Learning Style:</strong> {user.learningStyle}
          </div>

          <button
            onClick={() => setIsEditing(true)}
            style={{
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              backgroundColor: '#4285f4',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Edit Profile
          </button>
        </div>
      )}

      <button
        onClick={logout}
        style={{
          marginTop: '1rem',
          padding: '0.5rem 1rem',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Logout
      </button>
    </div>
  );
};

export default ProfileManager;