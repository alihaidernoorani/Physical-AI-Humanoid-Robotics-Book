---
id: 7
title: Update plan for Root.tsx ChatLoader implementation
stage: plan
date_iso: 2025-12-25
surface: agent
model: sonnet-4-5-20250929
feature: 001-chatwidget-stabilization
branch: 001-chatwidget-stabilization
user: Claude Sonnet 4.5
command: sp.plan
labels:
  - planning
  - architecture
  - docusaurus
  - Root.tsx
  - SSG
  - ChatLoader
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-chatwidget-stabilization/plan.md
  - specs/001-chatwidget-stabilization/research.md
  - specs/001-chatwidget-stabilization/data-model.md
  - specs/001-chatwidget-stabilization/quickstart.md
  - specs/001-chatwidget-stabilization/contracts/chat-api-contract.md
tests_yaml: |
  - npm run build should complete without SSG errors
  - ChatWidget should load in browser after hydration
  - No circular dependencies during build
outcome: |
  Successfully updated the implementation plan to use Root.tsx with ChatLoader
  component for SSG-safe ChatWidget implementation.
evaluation: |
  The plan now properly addresses SSG build failures and circular dependency issues
  with the recommended architecture approach.
---

# Prompt History Record: Update plan for Root.tsx ChatLoader implementation

## Original Prompt

Update the existing plan in this folder.
1. Technical change: Remove the `@theme/Layout` override.
2. Architecture: Implement a "Theme Wrapper" using `src/theme/Root.tsx`.
3. SSG Safety: Plan for a `ChatLoader` component that uses `useState` and `useEffect` to lazily load the ChatKit code only after the browser has hydrated. This specifically targets the fix for the `RangeError: Maximum call stack size exceeded` seen in the build logs.

## Implementation Response

The implementation plan has been successfully updated with the following key changes:

1. Updated plan.md to reflect Root.tsx theme wrapper architecture
2. Updated research.md to document the SSG-safe loading pattern
3. Maintained existing data-model.md and quickstart.md files
4. Created API contract documentation in contracts/ directory
5. Added detailed technical approach for ChatLoader component pattern

Key architectural decisions documented:
- Use Root.tsx as the theme wrapper instead of Layout.tsx to prevent circular dependencies
- Implement ChatLoader component with useState/useEffect for lazy loading
- Use dynamic imports to prevent SSG evaluation of browser APIs
- Ensure browser-specific code only executes after hydration