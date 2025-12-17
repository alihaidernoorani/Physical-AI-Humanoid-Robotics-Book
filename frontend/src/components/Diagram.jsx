import React from 'react';

const Diagram = ({
  title,
  description,
  src,
  alt,
  caption,
  className = ''
}) => {
  return (
    <div className={`diagram-component ${className}`} style={{
      textAlign: 'center',
      margin: '1.5rem 0',
      padding: '1rem',
      border: '1px solid #eee',
      borderRadius: '8px',
      backgroundColor: '#fafafa',
    }}>
      {title && (
        <h5 style={{
          margin: '0 0 1rem 0',
          color: '#202124',
          fontSize: '1rem',
          fontWeight: 'bold'
        }}>
          {title}
        </h5>
      )}

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        margin: '0 auto',
        maxWidth: '100%',
      }}>
        {src ? (
          <img
            src={src}
            alt={alt || title || 'Diagram'}
            style={{
              maxWidth: '100%',
              height: 'auto',
              border: '1px solid #ddd',
              borderRadius: '4px',
            }}
          />
        ) : (
          <div style={{
            width: '100%',
            height: '200px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#f5f5f5',
            border: '2px dashed #ccc',
            borderRadius: '4px',
            color: '#666',
          }}>
            Diagram placeholder
          </div>
        )}
      </div>

      {(description || caption) && (
        <div style={{
          marginTop: '0.5rem',
          fontSize: '0.9rem',
          color: '#5f6368',
          textAlign: 'left',
          padding: '0.5rem',
        }}>
          {description && <p style={{ margin: '0.5rem 0' }}>{description}</p>}
          {caption && <p style={{ margin: '0.5rem 0', fontStyle: 'italic' }}><strong>Figure:</strong> {caption}</p>}
        </div>
      )}
    </div>
  );
};

export default Diagram;