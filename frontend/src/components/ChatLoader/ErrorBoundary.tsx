import React, { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log the error to an error reporting service
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      // Return fallback UI if provided, otherwise render error message
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div style={{ position: 'fixed', bottom: '20px', right: '20px', color: 'red', fontSize: '12px', zIndex: 10000 }}>
          Chat widget encountered an error
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;