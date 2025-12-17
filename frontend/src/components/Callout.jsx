import React from 'react';

const Callout = ({ type = 'note', title, children, className = '' }) => {
  const calloutStyles = {
    note: {
      borderLeft: '4px solid #4285f4',
      backgroundColor: '#f0f4ff',
      color: '#202124',
    },
    tip: {
      borderLeft: '4px solid #34a853',
      backgroundColor: '#f0f9ff',
      color: '#202124',
    },
    warning: {
      borderLeft: '4px solid #fbbc04',
      backgroundColor: '#fef7e0',
      color: '#202124',
    },
    danger: {
      borderLeft: '4px solid #ea4335',
      backgroundColor: '#fce8e6',
      color: '#202124',
    },
  };

  const iconMap = {
    note: 'ℹ️',
    tip: '💡',
    warning: '⚠️',
    danger: '❌',
  };

  const currentStyle = calloutStyles[type] || calloutStyles.note;
  const icon = iconMap[type] || iconMap.note;

  return (
    <div
      className={`callout callout-${type} ${className}`}
      style={{
        border: '1px solid',
        borderRadius: '4px',
        padding: '1rem',
        margin: '1rem 0',
        ...currentStyle,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start' }}>
        <span style={{ fontSize: '1.2rem', marginRight: '0.5rem' }}>{icon}</span>
        <div>
          {title && (
            <h5 style={{
              margin: '0 0 0.5rem 0',
              fontSize: '1rem',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              {title}
            </h5>
          )}
          <div>{children}</div>
        </div>
      </div>
    </div>
  );
};

export default Callout;