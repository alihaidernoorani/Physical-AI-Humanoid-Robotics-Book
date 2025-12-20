# ChatKit Components

ChatKit is a comprehensive chat interface solution for the Physical AI Humanoid Robotics Textbook project. It provides a complete chat experience with message history, real-time communication, and error handling.

## Components

### ChatWindow
The main chat interface component that combines all other components into a cohesive chat experience.

**Props:**
- `sessionId` (optional): Existing session ID to continue a conversation
- `initialMessages` (optional): Array of messages to display initially

### MessageList
Displays the list of chat messages in chronological order.

### Message
Represents a single message with sender, content, timestamp, and citations.

### MessageInput
Provides the input interface for users to type and send messages.

### ErrorDisplay
Handles and displays error messages with optional retry functionality.

## Features

- Real-time chat communication with backend API
- Message history and session management
- Connection status monitoring
- Error handling with retry functionality
- Citation support for referenced content
- Responsive design for different screen sizes
- Loading states for better user experience

## API Integration

The components integrate with the backend through the `chatService` in `frontend/src/services/api.js`, which provides methods for:
- Sending messages
- Retrieving chat history
- Creating new chat sessions

## Usage

```jsx
import { ChatWindow } from './components/ChatKit';

function App() {
  return (
    <div className="app">
      <ChatWindow />
    </div>
  );
}
```