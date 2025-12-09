import { loadFromLocalStorage } from './localStorage';

// Personalization utility functions

// Get user profile from localStorage
export const getUserProfile = () => {
  return loadFromLocalStorage('userProfile');
};

// Get content adaptation level based on user experience
export const getContentAdaptation = () => {
  const profile = getUserProfile();
  if (!profile) {
    // Default to intermediate for non-logged-in users
    return {
      skipBasicContent: false,
      showAdvancedExamples: false,
      highlightHardwareRelevance: 'all'
    };
  }

  switch (profile.softwareExperience) {
    case 'Beginner':
      return {
        skipBasicContent: false,
        showAdvancedExamples: false,
        highlightHardwareRelevance: profile.hardwareSetup || 'all'
      };
    case 'Intermediate':
      return {
        skipBasicContent: true,
        showAdvancedExamples: true,
        highlightHardwareRelevance: profile.hardwareSetup || 'all'
      };
    case 'Advanced':
      return {
        skipBasicContent: true,
        showAdvancedExamples: true,
        highlightHardwareRelevance: profile.hardwareSetup || 'all'
      };
    default:
      return {
        skipBasicContent: false,
        showAdvancedExamples: false,
        highlightHardwareRelevance: 'all'
      };
  }
};

// Filter content based on user profile
export const filterContent = (content: any, adaptation: any) => {
  // This function would be used to filter content based on user preferences
  // For now, it returns the original content
  return content;
};

// Get learning style preference
export const getLearningStylePreference = () => {
  const profile = getUserProfile();
  if (!profile) {
    return 'Visual'; // Default learning style
  }
  return profile.learningStyle;
};

// Get hardware setup preference
export const getHardwarePreference = () => {
  const profile = getUserProfile();
  if (!profile) {
    return 'all'; // Show all hardware options to non-logged-in users
  }
  return profile.hardwareSetup;
};