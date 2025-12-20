import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatWindow from './ChatWindow';

// Mock the chat service
jest.mock('../../../services/api', () => ({
  chatService: {
    sendMessage: jest.fn(),
    getHistory: jest.fn(),
    createSession: jest.fn()
  }
}));

describe('ChatWindow', () => {
  const mockSendMessage = require('../../../services/api').chatService.sendMessage;
  const mockGetHistory = require('../../../services/api').chatService.getHistory;
  const mockCreateSession = require('../../../services/api').chatService.createSession;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock successful API calls
    mockCreateSession.mockResolvedValue({ session_id: 'test-session-123' });
    mockSendMessage.mockResolvedValue({
      response: 'Test response',
      citations: ['Test citation']
    });
    mockGetHistory.mockResolvedValue([]);
  });

  test('renders ChatWindow component', () => {
    render(<ChatWindow />);

    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Type your message here...')).toBeInTheDocument();
  });

  test('allows user to type and send a message', async () => {
    render(<ChatWindow />);

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hello, world!' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(mockSendMessage).toHaveBeenCalledWith({
        query: 'Hello, world!',
        session_id: 'test-session-123'
      });
    });
  });

  test('shows loading state when sending message', async () => {
    // Make the API call take some time to simulate loading
    mockSendMessage.mockImplementation(() => new Promise(resolve =>
      setTimeout(() => resolve({ response: 'Test response' }), 100)
    ));

    render(<ChatWindow />);

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hello, world!' } });
    fireEvent.click(sendButton);

    expect(sendButton).toHaveTextContent('Sending...');
  });

  test('handles error when sending message', async () => {
    mockSendMessage.mockRejectedValue(new Error('API Error'));

    render(<ChatWindow />);

    const input = screen.getByPlaceholderText('Type your message here...');
    const sendButton = screen.getByText('Send');

    fireEvent.change(input, { target: { value: 'Hello, world!' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Failed to send message. Please try again.')).toBeInTheDocument();
    });
  });

  test('prevents sending empty messages', () => {
    render(<ChatWindow />);

    const sendButton = screen.getByText('Send');

    // Initially disabled for empty message
    expect(sendButton).toBeDisabled();

    const input = screen.getByPlaceholderText('Type your message here...');
    fireEvent.change(input, { target: { value: ' ' } });

    // Still disabled for whitespace-only message
    expect(sendButton).toBeDisabled();
  });
});