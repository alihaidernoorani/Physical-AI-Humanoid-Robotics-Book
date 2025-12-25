import React from 'react';
import { useLocation } from '@docusaurus/router';
import ChatKit from '../components/ChatKit/ChatKit';

interface Props {
  children: React.ReactNode;
}

const Layout = ({ children }: Props): JSX.Element => {
  const location = useLocation();

  // Show ChatKit on all pages except for specific routes where it might interfere
  // For now, we'll show it on all pages since it's a global widget
  const shouldShowChatKit = true; // Show on all pages for global access

  return (
    <>
      {children}
      {shouldShowChatKit && <ChatKit />}
    </>
  );
};

export default Layout;