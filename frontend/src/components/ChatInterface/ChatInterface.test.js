import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import ChatInterface from '../src/components/ChatInterface/ChatInterface';

// Mock the API service
const server = setupServer(
  rest.post('http://localhost:8000/api/rag/query', (req, res, ctx) => {
    const body = req.body;
    if (body && typeof body === 'object') {
      const retrieval_mode = body.retrieval_mode;
      const query_text = body.query_text;

      // Mock response based on mode
      const mockResponse = {
        response_text: `This is a mock response in ${retrieval_mode} mode for query: ${query_text}`,
        citations: [
          {
            module: "Module 1",
            chapter: "Chapter 1",
            subsection: "1.1 Introduction",
            page_reference: "p.15",
            text: "Sample text from the textbook",
            confidence_score: 0.95
          }
        ],
        confidence_score: 0.95,
        is_fallback: false
      };

      return res(ctx.json(mockResponse));
    }

    return res(ctx.status(400));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('ChatInterface Dual Retrieval Modes', () => {
  test('should initialize in full-book mode by default', () => {
    render(<ChatInterface />);

    // Check that the full-book mode option is active
    const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
    expect(fullBookButton).toBeInTheDocument();
    expect(fullBookButton).toHaveClass('active');

    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    expect(perPageButton).toBeInTheDocument();
    expect(perPageButton).not.toHaveClass('active');
  });

  test('should switch to per-page mode when selected', () => {
    render(<ChatInterface />);

    // Switch to per-page mode
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    fireEvent.click(perPageButton);

    // Check that per-page mode is now active
    expect(perPageButton).toHaveClass('active');

    const fullBookButton = screen.getByRole('button', { name: /full book mode/i });
    expect(fullBookButton).not.toHaveClass('active');
  });

  test('should send correct mode in API request when in full-book mode', async () => {
    render(<ChatInterface />);

    // Find and fill the input
    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Test question in full-book mode' } });

    // Submit the form
    const submitButton = screen.getByText(/send/i);
    fireEvent.click(submitButton);

    // Wait for the API call to complete
    await waitFor(() => {
      expect(screen.getByText(/this is a mock response in full-book mode for query: test question in full-book mode/i)).toBeInTheDocument();
    });
  });

  test('should send correct mode in API request when in per-page mode', async () => {
    render(<ChatInterface />);

    // Switch to per-page mode
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    fireEvent.click(perPageButton);

    // Find and fill the input
    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Test question in per-page mode' } });

    // Submit the form
    const submitButton = screen.getByText(/send/i);
    fireEvent.click(submitButton);

    // Wait for the API call to complete
    await waitFor(() => {
      expect(screen.getByText(/this is a mock response in per-page mode for query: test question in per-page mode/i)).toBeInTheDocument();
    });
  });

  test('should clear chat when mode is changed', async () => {
    render(<ChatInterface />);

    // Add a message first
    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'First question' } });

    const submitButton = screen.getByText(/send/i);
    fireEvent.click(submitButton);

    // Wait for the response
    await waitFor(() => {
      expect(screen.getByText(/this is a mock response in full-book mode for query: first question/i)).toBeInTheDocument();
    });

    // Verify message exists
    expect(screen.getByText(/first question/i)).toBeInTheDocument();

    // Switch mode - this should clear the chat
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    fireEvent.click(perPageButton);

    // The welcome message should be shown again
    expect(screen.getByText(/hello! i'm your rag assistant/i)).toBeInTheDocument();
    expect(screen.queryByText(/first question/i)).not.toBeInTheDocument();
  });

  test('should pass selected text to API in per-page mode', async () => {
    render(<ChatInterface selectedText="This is the selected text for testing" />);

    // Switch to per-page mode
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    fireEvent.click(perPageButton);

    // Verify selected text preview is shown
    expect(screen.getByText(/selected: this is the selected text for testing/i)).toBeInTheDocument();

    // Add a question
    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Question about selected text' } });

    const submitButton = screen.getByText(/send/i);
    fireEvent.click(submitButton);

    // Wait for the response
    await waitFor(() => {
      expect(screen.getByText(/this is a mock response in per-page mode for query: question about selected text/i)).toBeInTheDocument();
    });
  });
});