// src/theme/Root.tsx
import React from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import ChatLoader from '../components/ChatLoader/ChatLoader';

export default function Root({children}) {
  return (
    <>
      {children}
      <BrowserOnly fallback={null}>
        {() => <ChatLoader />}
      </BrowserOnly>
    </>
  );
}