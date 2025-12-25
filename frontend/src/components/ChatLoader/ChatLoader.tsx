// src/components/ChatLoader/ChatLoader.tsx
import React, { useState, useEffect } from 'react';

const ChatLoader = () => {
  const [Component, setComponent] = useState(null);

  useEffect(() => {
    // Dynamic import is the safest way to prevent SSG leakage
    import('../ChatKit/ChatKit')
      .then((mod) => setComponent(() => mod.default))
      .catch((err) => console.error("Loader failed", err));
  }, []);

  return Component ? <Component /> : null;
};

export default ChatLoader;