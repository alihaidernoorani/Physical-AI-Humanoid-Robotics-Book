import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Define the user profile type
interface UserProfile {
  id: string;
  email: string;
  name: string;
  softwareExperience: 'Beginner' | 'Intermediate' | 'Advanced';
  hardwareSetup: string;
  learningStyle: 'Visual' | 'Hands-on' | 'Theoretical';
  createdAt: string;
}

// Define the auth context type
interface AuthContextType {
  user: UserProfile | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string, profile: Omit<UserProfile, 'id' | 'createdAt'>) => Promise<void>;
  logout: () => void;
  updateUserProfile: (profile: Partial<UserProfile>) => void;
  isAuthenticated: boolean;
}

// Create the context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth provider component
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on initial load
  useEffect(() => {
    const storedUser = localStorage.getItem('userProfile');
    if (storedUser) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
      } catch (error) {
        console.error('Error parsing user profile from localStorage:', error);
      }
    }
    setLoading(false);
  }, []);

  // Save user to localStorage whenever it changes
  useEffect(() => {
    if (user) {
      localStorage.setItem('userProfile', JSON.stringify(user));
    } else {
      localStorage.removeItem('userProfile');
    }
  }, [user]);

  const login = async (email: string, password: string) => {
    // Simulate login - in a real app, this would call an API
    setLoading(true);

    // For demo purposes, we'll create a mock user
    const mockUser: UserProfile = {
      id: `user_${Date.now()}`,
      email,
      name: email.split('@')[0],
      softwareExperience: 'Intermediate',
      hardwareSetup: 'Jetson Orin',
      learningStyle: 'Hands-on',
      createdAt: new Date().toISOString(),
    };

    setUser(mockUser);
    setLoading(false);
  };

  const signup = async (email: string, password: string, name: string, profile: Omit<UserProfile, 'id' | 'createdAt'>) => {
    // Simulate signup - in a real app, this would call an API
    setLoading(true);

    const newUser: UserProfile = {
      id: `user_${Date.now()}`,
      email,
      name,
      softwareExperience: profile.softwareExperience,
      hardwareSetup: profile.hardwareSetup,
      learningStyle: profile.learningStyle,
      createdAt: new Date().toISOString(),
    };

    setUser(newUser);
    setLoading(false);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('userProfile');
  };

  const updateUserProfile = (profile: Partial<UserProfile>) => {
    if (user) {
      const updatedUser = { ...user, ...profile };
      setUser(updatedUser);
    }
  };

  const value = {
    user,
    loading,
    login,
    signup,
    logout,
    updateUserProfile,
    isAuthenticated: !!user,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};