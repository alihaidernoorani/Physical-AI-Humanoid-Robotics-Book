import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { RAGModeSelector, CompactRAGModeSelector, ToggleRAGModeSelector } from './RAGModeSelector';

describe('RAGModeSelector Component - Unit Tests', () => {
  describe('RAGModeSelector (Standard)', () => {
    test('renders both mode options correctly', () => {
      render(<RAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      expect(screen.getByRole('button', { name: /full book mode \(selected\)/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /per page mode/i })).toBeInTheDocument();
    });

    test('shows correct active state based on currentMode prop', () => {
      const { rerender } = render(<RAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      // Initially full-book should be active
      let fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
      let perPageButton = screen.getByRole('button', { name: /per page mode/i });
      expect(fullBookButton).toHaveClass('active');
      expect(perPageButton).not.toHaveClass('active');

      // Rerender with per-page mode
      rerender(<RAGModeSelector currentMode="per-page" onModeChange={jest.fn()} />);

      fullBookButton = screen.getByRole('button', { name: /full book mode/i });
      perPageButton = screen.getByRole('button', { name: /per page mode \(selected\)/i });
      expect(perPageButton).toHaveClass('active');
      expect(fullBookButton).not.toHaveClass('active');
    });

    test('calls onModeChange when mode is selected', () => {
      const mockOnModeChange = jest.fn();
      render(<RAGModeSelector currentMode="full-book" onModeChange={mockOnModeChange} />);

      const perPageButton = screen.getByRole('button', { name: /per page mode/i });
      fireEvent.click(perPageButton);

      expect(mockOnModeChange).toHaveBeenCalledWith('per-page');
    });

    test('disables buttons when disabled prop is true', () => {
      render(<RAGModeSelector currentMode="full-book" onModeChange={jest.fn()} disabled={true} />);

      const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
      const perPageButton = screen.getByRole('button', { name: /per page mode/i });

      expect(fullBookButton).toBeDisabled();
      expect(perPageButton).toBeDisabled();
    });

    test('does not call onModeChange when disabled', () => {
      const mockOnModeChange = jest.fn();
      render(<RAGModeSelector currentMode="full-book" onModeChange={mockOnModeChange} disabled={true} />);

      const perPageButton = screen.getByRole('button', { name: /per page mode/i });
      fireEvent.click(perPageButton);

      expect(mockOnModeChange).not.toHaveBeenCalled();
    });

    test('shows active indicator for selected mode', () => {
      render(<RAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
      expect(fullBookButton).toHaveClass('active');
      expect(fullBookButton.querySelector('.active-indicator')).toBeInTheDocument();
    });
  });

  describe('CompactRAGModeSelector', () => {
    test('renders select element with correct options', () => {
      render(<CompactRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      const selectElement = screen.getByRole('combobox');
      expect(selectElement).toBeInTheDocument();

      expect(screen.getByRole('option', { name: /full book/i })).toBeInTheDocument();
      expect(screen.getByRole('option', { name: /per page/i })).toBeInTheDocument();
    });

    test('has correct initial selected value', () => {
      render(<CompactRAGModeSelector currentMode="per-page" onModeChange={jest.fn()} />);

      const selectElement = screen.getByRole('combobox');
      expect(selectElement.value).toBe('per-page');
    });

    test('calls onModeChange when selection changes', () => {
      const mockOnModeChange = jest.fn();
      render(<CompactRAGModeSelector currentMode="full-book" onModeChange={mockOnModeChange} />);

      const selectElement = screen.getByRole('combobox');
      fireEvent.change(selectElement, { target: { value: 'per-page' } });

      expect(mockOnModeChange).toHaveBeenCalledWith('per-page');
    });

    test('disables select when disabled prop is true', () => {
      render(<CompactRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} disabled={true} />);

      const selectElement = screen.getByRole('combobox');
      expect(selectElement).toBeDisabled();
    });
  });

  describe('ToggleRAGModeSelector', () => {
    test('renders toggle switch with labels', () => {
      render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      expect(screen.getByText(/full book/i)).toBeInTheDocument();
      expect(screen.getByText(/per page/i)).toBeInTheDocument();
      expect(screen.getByRole('switch')).toBeInTheDocument();
    });

    test('has correct initial state based on currentMode', () => {
      const { rerender } = render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      // Initially full-book should be active
      let fullBookLabel = screen.getByText(/full book/i);
      let perPageLabel = screen.getByText(/per page/i);
      let toggleSwitch = screen.getByRole('switch');

      expect(fullBookLabel).toHaveClass('active');
      expect(perPageLabel).not.toHaveClass('active');
      expect(toggleSwitch.checked).toBe(false); // unchecked means full-book mode

      // Rerender with per-page mode
      rerender(<ToggleRAGModeSelector currentMode="per-page" onModeChange={jest.fn()} />);

      fullBookLabel = screen.getByText(/full book/i);
      perPageLabel = screen.getByText(/per page/i);
      toggleSwitch = screen.getByRole('switch');

      expect(perPageLabel).toHaveClass('active');
      expect(fullBookLabel).not.toHaveClass('active');
      expect(toggleSwitch.checked).toBe(true); // checked means per-page mode
    });

    test('calls onModeChange when toggle is switched', () => {
      const mockOnModeChange = jest.fn();
      render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={mockOnModeChange} />);

      const toggleSwitch = screen.getByRole('switch');
      fireEvent.click(toggleSwitch);

      expect(mockOnModeChange).toHaveBeenCalledWith('per-page');
    });

    test('toggles back to full-book when clicked again', () => {
      const mockOnModeChange = jest.fn();
      render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={mockOnModeChange} />);

      const toggleSwitch = screen.getByRole('switch');
      fireEvent.click(toggleSwitch); // Switch to per-page
      fireEvent.click(toggleSwitch); // Switch back to full-book

      expect(mockOnModeChange).toHaveBeenNthCalledWith(2, 'full-book');
    });

    test('disables toggle when disabled prop is true', () => {
      render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} disabled={true} />);

      const toggleSwitch = screen.getByRole('switch');
      expect(toggleSwitch).toBeDisabled();
    });

    test('does not call onModeChange when disabled', () => {
      const mockOnModeChange = jest.fn();
      render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={mockOnModeChange} disabled={true} />);

      const toggleSwitch = screen.getByRole('switch');
      fireEvent.click(toggleSwitch);

      expect(mockOnModeChange).not.toHaveBeenCalled();
    });
  });

  describe('Accessibility', () => {
    test('standard selector has proper aria labels', () => {
      render(<RAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
      const perPageButton = screen.getByRole('button', { name: /per page mode/i });

      expect(fullBookButton).toHaveAttribute('aria-pressed', 'true');
      expect(perPageButton).toHaveAttribute('aria-pressed', 'false');
    });

    test('compact selector has proper label', () => {
      render(<CompactRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      const label = screen.getByText(/search mode:/i);
      const selectElement = screen.getByRole('combobox');

      expect(label).toBeInTheDocument();
      expect(selectElement).toHaveAccessibleName(/search mode:/i);
    });

    test('toggle selector has proper accessibility attributes', () => {
      render(<ToggleRAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      const toggleSwitch = screen.getByRole('switch');
      expect(toggleSwitch).toBeInTheDocument();
      expect(toggleSwitch).toHaveAttribute('type', 'checkbox');
    });
  });

  describe('Visual Feedback', () => {
    test('shows visual feedback for active mode', () => {
      render(<RAGModeSelector currentMode="per-page" onModeChange={jest.fn()} />);

      const perPageButton = screen.getByRole('button', { name: /per page mode \(selected\)/i });
      const fullBookButton = screen.getByRole('button', { name: /full book mode/i });

      expect(perPageButton).toHaveClass('active');
      expect(fullBookButton).not.toHaveClass('active');
    });

    test('standard selector shows active indicator', () => {
      render(<RAGModeSelector currentMode="full-book" onModeChange={jest.fn()} />);

      const fullBookButton = screen.getByRole('button', { name: /full book mode \(selected\)/i });
      expect(fullBookButton.querySelector('.active-indicator')).toBeInTheDocument();
    });
  });
});