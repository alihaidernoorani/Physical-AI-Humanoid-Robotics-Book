// src/components/ChatLoader/ChatLoader.tsx
import React, { useState, useEffect } from 'react';
import ErrorBoundary from './ErrorBoundary';

const ChatLoader = () => {
  const [Component, setComponent] = useState(null);
  const [hasError, setHasError] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Dynamic import is the safest way to prevent SSG leakage
    const loadComponent = async () => {
      try {
        const mod = await import('../ChatKit/ChatKit');
        if (mod && mod.default) {
          setComponent(() => mod.default);
          setHasError(false);
        } else {
          throw new Error('ChatKit module does not have a default export');
        }
      } catch (err) {
        console.error("ChatLoader failed to load ChatKit:", err);
        setHasError(true);
      } finally {
        setIsLoading(false);
      }
    };

    loadComponent();
  }, []);

  // Render nothing if there's an error or component not loaded yet
  // This prevents any UI issues during SSG or if loading fails
  if (hasError) {
    // Display an error state instead of failing silently
    if (typeof window !== 'undefined') {
      // Only render error element in browser environment
      return (
        <div style={{ position: 'fixed', bottom: '20px', right: '20px', color: 'red', fontSize: '12px' }}>
          Chat widget failed to load
        </div>
      );
    }
    return null; // Don't render anything during SSG
  }

  if (isLoading || !Component) {
    // Render nothing while loading to prevent flickering
    return null;
  }

  return (
    <ErrorBoundary>
      <Component />
    </ErrorBoundary>
  );
};

export default ChatLoader;