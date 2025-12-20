import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import ChatInterface from './ChatInterface';

// Mock the API service
const server = setupServer(
  rest.post('http://localhost:8000/api/rag/chat', (req, res, ctx) => {
    const body = req.body;
    if (body && typeof body === 'object') {
      const retrieval_mode = body.retrieval_mode;
      const query_text = body.query_text;

      // Mock response based on mode
      const mockResponse = {
        response_id: 'test-response-id',
        response_text: `This is a mock response in ${retrieval_mode} mode for query: ${query_text}`,
        citations: [
          {
            chunk_id: 'chunk-1',
            module: "Module 1",
            chapter: "Chapter 1",
            subsection: "1.1 Introduction",
            page_reference: "p.15"
          }
        ],
        confidence_score: 0.95,
        grounded_chunks: ['chunk-1'],
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

describe('ChatInterface Component - Unit Tests', () => {
  test('renders without crashing', () => {
    render(<ChatInterface />);

    expect(screen.getByRole('heading', { name: /rag chatbot/i })).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/ask a question about the textbook content/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
  });

  test('initializes with default mode (full-book)', () => {
    render(<ChatInterface />);

    const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
    expect(fullBookButton).toBeInTheDocument();
    expect(fullBookButton).toHaveClass('active');

    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    expect(perPageButton).toBeInTheDocument();
    expect(perPageButton).not.toHaveClass('active');
  });

  test('accepts custom initial mode prop', () => {
    render(<ChatInterface mode="per-page" />);

    const perPageButton = screen.getByRole('button', { name: /per page mode \(selected\)/i });
    expect(perPageButton).toBeInTheDocument();
    expect(perPageButton).toHaveClass('active');

    const fullBookButton = screen.getByRole('button', { name: /full book mode/i });
    expect(fullBookButton).toBeInTheDocument();
    expect(fullBookButton).not.toHaveClass('active');
  });

  test('updates mode when RAGModeSelector changes', () => {
    render(<ChatInterface />);

    // Initially full-book mode should be active
    const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
    expect(fullBookButton).toHaveClass('active');

    // Switch to per-page mode
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    fireEvent.click(perPageButton);

    // Now per-page mode should be active
    expect(perPageButton).toHaveClass('active');
    expect(fullBookButton).not.toHaveClass('active');
  });

  test('clears chat when mode changes', async () => {
    render(<ChatInterface />);

    // Add a message first
    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Initial question' } });

    const submitButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(submitButton);

    // Wait for the response to be displayed
    await waitFor(() => {
      expect(screen.getByText(/initial question/i)).toBeInTheDocument();
    });

    // Verify message exists
    expect(screen.getByText(/initial question/i)).toBeInTheDocument();

    // Switch mode - this should clear the chat
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });
    fireEvent.click(perPageButton);

    // The welcome message should be shown again
    expect(screen.getByText(/hello! i'm your rag assistant/i)).toBeInTheDocument();
    expect(screen.queryByText(/initial question/i)).not.toBeInTheDocument();
  });

  test('submits query and displays response', async () => {
    render(<ChatInterface />);

    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Test question' } });

    const submitButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(submitButton);

    // Wait for the API call to complete and response to be displayed
    await waitFor(() => {
      expect(screen.getByText(/this is a mock response in full-book mode for query: test question/i)).toBeInTheDocument();
    });

    // Check that the user message is also displayed
    expect(screen.getByText(/test question/i)).toBeInTheDocument();

    // Check that citations are displayed
    expect(screen.getByText(/sources:/i)).toBeInTheDocument();
    expect(screen.getByText(/module 1/i)).toBeInTheDocument();
  });

  test('disables submit button when input is empty', () => {
    render(<ChatInterface />);

    const submitButton = screen.getByRole('button', { name: /send/i });
    expect(submitButton).toBeDisabled();

    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Non-empty text' } });

    expect(submitButton).not.toBeDisabled();
  });

  test('shows loading state during API call', async () => {
    render(<ChatInterface />);

    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Loading test' } });

    const submitButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(submitButton);

    // Check that loading indicator appears
    expect(screen.getByText(/sending\.\.\./i)).toBeInTheDocument();
    expect(submitButton).toBeDisabled();

    // Wait for the response to complete
    await waitFor(() => {
      expect(screen.queryByText(/sending\.\.\./i)).not.toBeInTheDocument();
      expect(submitButton).not.toBeDisabled();
    });
  });

  test('displays error message when API call fails', async () => {
    // Mock a failing API call
    server.use(
      rest.post('http://localhost:8000/api/rag/chat', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Internal server error' }));
      })
    );

    render(<ChatInterface />);

    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Error test' } });

    const submitButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(submitButton);

    // Wait for the error to be displayed
    await waitFor(() => {
      expect(screen.getByText(/failed to get response\. please try again\./i)).toBeInTheDocument();
    });
  });

  test('handles selected text prop correctly in per-page mode', () => {
    const selectedText = "This is the selected text for testing per-page functionality.";
    render(<ChatInterface mode="per-page" selectedText={selectedText} />);

    // Check that selected text preview is displayed
    const previewElement = screen.getByText(/selected: this is the selected text for testing per-page functionality\.\.\./i);
    expect(previewElement).toBeInTheDocument();
  });

  test('disables mode selector during loading', async () => {
    render(<ChatInterface />);

    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Loading test' } });

    const submitButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(submitButton);

    // Mode selector buttons should be disabled during loading
    const fullBookButton = screen.getByRole('button', { name: /full book mode/i });
    const perPageButton = screen.getByRole('button', { name: /per page mode/i });

    expect(fullBookButton).toBeDisabled();
    expect(perPageButton).toBeDisabled();

    // Wait for the response to complete
    await waitFor(() => {
      expect(fullBookButton).not.toBeDisabled();
      expect(perPageButton).not.toBeDisabled();
    });
  });

  test('maintains proper state transitions', () => {
    const { rerender } = render(<ChatInterface />);

    // Initial state check
    let fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
    let perPageButton = screen.getByRole('button', { name: /per page mode/i });
    expect(fullBookButton).toHaveClass('active');
    expect(perPageButton).not.toHaveClass('active');

    // Switch to per-page
    fireEvent.click(perPageButton);
    expect(perPageButton).toHaveClass('active');
    expect(fullBookButton).not.toHaveClass('active');

    // Switch back to full-book
    fireEvent.click(fullBookButton);
    expect(fullBookButton).toHaveClass('active');
    expect(perPageButton).not.toHaveClass('active');
  });

  test('displays confidence score correctly', async () => {
    render(<ChatInterface />);

    const input = screen.getByPlaceholderText(/ask a question about the textbook content/i);
    fireEvent.change(input, { target: { value: 'Confidence test' } });

    const submitButton = screen.getByRole('button', { name: /send/i });
    fireEvent.click(submitButton);

    // Wait for response with confidence score
    await waitFor(() => {
      expect(screen.getByText(/confidence: 95%/i)).toBeInTheDocument();
    });
  });
});