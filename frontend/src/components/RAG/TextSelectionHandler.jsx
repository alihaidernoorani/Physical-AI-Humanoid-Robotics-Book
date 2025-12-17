import React, { useEffect } from 'react';

const TextSelectionHandler = ({ onTextSelected }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();

      if (selectedText && selectedText.length > 10) { // Only trigger for meaningful selections
        // Call the parent handler with the selected text
        onTextSelected(selectedText);
      }
    };

    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Cleanup event listeners on unmount
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [onTextSelected]);

  return null; // This component doesn't render anything
};

export default TextSelectionHandler;