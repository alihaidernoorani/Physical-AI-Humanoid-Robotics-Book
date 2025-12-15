# API Contracts: textbook-mdx-compliance

## Overview
This document describes the API contracts relevant to the textbook MDX compliance update. Since this is primarily a content and frontend update, the contracts focus on component interfaces and data structures.

## Component Interface Contracts

### Urdu/English Toggle Component
- **Purpose**: Provides language switching functionality for textbook content
- **Type**: React/MDX Component
- **Props**:
  - `defaultLanguage`: string (optional, default: "en") - The default language to display
  - `children`: ReactNode - Content that can be toggled between languages
- **State**:
  - `currentLanguage`: "en" | "ur" - Tracks the currently selected language
- **Events**:
  - `onLanguageChange`: (language: "en" | "ur") => void - Called when language is switched

### Interactive Quiz Component
- **Purpose**: Provides interactive quiz functionality within textbook chapters
- **Type**: React/MDX Component
- **Props**:
  - `questions`: Array of question objects with the following structure:
    - `id`: string - Unique identifier for the question
    - `type`: "multiple-choice" | "true-false" | "short-answer" - Type of question
    - `question`: string - The question text
    - `options?`: Array of option objects for multiple choice questions
    - `correctAnswer`: string - The correct answer
  - `onSubmit?`: (results: QuizResult) => void - Called when quiz is submitted

### Content Card Component
- **Purpose**: Displays module or chapter information in a card format
- **Type**: React Component
- **Props**:
  - `title`: string - The title of the module/chapter
  - `description`: string - Brief description
  - `link`: string - URL to navigate to the content
  - `icon?`: ReactNode - Optional icon to display

## Data Contracts

### Chapter Frontmatter Schema
- **Format**: YAML frontmatter in MD/MDX files
- **Required Fields**:
  - `title`: string - Chapter title
  - `sidebar_label`: string - Label to display in sidebar navigation
- **Optional Fields**:
  - `description`: string - Brief description of the chapter
  - `sidebar_position`: number - Position in sidebar navigation
  - `keywords`: string[] - SEO keywords
  - `requiresInteractiveComponents`: boolean - Indicates if MDX format is required

### Navigation Structure Schema
- **Format**: JavaScript object in sidebars.js
- **Structure**:
  - `type`: "category" | "doc" | "link" - Type of navigation item
  - `label`: string - Display label for the item
  - `items`: Array of child navigation items (for category type)
  - `id`: string - Reference to document (for doc type)
  - `href`: string - External URL (for link type)

## File Format Contracts

### MDX File Requirements
- **Extension**: `.mdx`
- **Structure**:
  - YAML frontmatter (required)
  - Import statements for React components (when needed)
  - Markdown content with optional JSX components
- **Constraints**:
  - Must be parseable by Docusaurus MDX parser
  - React components must be properly imported
  - JSX syntax must be valid

### Link Format Contract
- **Internal Links**: Must use relative paths or Docusaurus doc/link syntax
- **Format**: `[Link Text](./relative-path)` or `[Link Text](/absolute-path)`
- **Validation**: All internal links must point to existing files to prevent 404 errors