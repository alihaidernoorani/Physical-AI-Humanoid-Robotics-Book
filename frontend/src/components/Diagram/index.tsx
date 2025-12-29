import React from 'react';

interface DiagramProps {
  title?: string;
  description?: string;
  caption?: string;
  width?: string | number;
  height?: string | number;
}

/**
 * Temporary Diagram stub component
 * TODO: This component should be removed once all Diagram usages
 * are converted to native Mermaid blocks.
 */
export default function Diagram({ title, description, caption }: DiagramProps) {
  return (
    <div style={{
      border: '2px dashed #ccc',
      borderRadius: '8px',
      padding: '2rem',
      margin: '1.5rem 0',
      textAlign: 'center',
      backgroundColor: 'var(--ifm-background-surface-color)'
    }}>
      <p style={{ fontWeight: 'bold', margin: 0 }}>
        {title || 'Diagram Placeholder'}
      </p>
      <p style={{ fontStyle: 'italic', color: '#666', margin: '0.5rem 0 0' }}>
        {description || caption || 'This diagram will be converted to Mermaid'}
      </p>
    </div>
  );
}
