// src/components/ChatLoader/ChatLoader.tsx
import React, { useState, useEffect } from 'react';

const ChatLoader = () => {
  const [Component, setComponent] = useState(null);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    // Dynamic import is the safest way to prevent SSG leakage
    import('../ChatKit/ChatKit')
      .then((mod) => {
        setComponent(() => mod.default);
        setHasError(false);
      })
      .catch((err) => {
        console.error("ChatLoader failed to load ChatKit:", err);
        setHasError(true);
      });
  }, []);

  // Render nothing if there's an error or component not loaded yet
  // This prevents any UI issues during SSG or if loading fails
  if (hasError) {
    return null; // Fail gracefully without breaking the page
  }

  return Component ? <Component /> : null;
};

export default ChatLoader;