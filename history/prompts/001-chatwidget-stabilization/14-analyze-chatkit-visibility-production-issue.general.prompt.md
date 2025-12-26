---
id: 14
title: Analyze ChatKit visibility production issue
stage: general
date_iso: 2025-12-25
surface: agent
model: sonnet-4-5-20250929
feature: 001-chatwidget-stabilization
branch: 001-chatwidget-stabilization
user: Claude Sonnet 4.5
command: sp.analyze
labels:
  - analysis
  - production
  - visibility
  - docusaurus
  - chatkit
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - frontend/src/services/api.js
  - frontend/src/components/ChatLoader/ChatLoader.tsx
  - frontend/src/components/ChatKit/ChatKit.tsx
  - frontend/src/theme/Root.tsx
tests_yaml: |
  - Widget visible on localhost
  - Widget missing on GitHub Pages
  - Error: process is not defined
outcome: |
  Identified root cause: Node.js globals (process) not available in production browser environment
evaluation: |
  Analysis reveals process.env references in API service causing ReferenceError in production
---

# Prompt History Record: Analyze ChatKit visibility production issue

## Original Prompt

Analyze why the ChatKit widget is visible on localhost but NOT on GitHub Pages.

Context:
- Frontend: Docusaurus static site deployed on GitHub Pages
- Chat widget loads locally (`npm start`) but not in production
- BrowserOnly is used
- ChatLoader dynamically imports ChatKit
- Production console error:
  - "ReferenceError: process is not defined"
  - "ChatLoader failed to load ChatKit"

Goals:
1. Identify ALL differences between dev mode and production build
2. Identify why ChatKit fails silently on GitHub Pages
3. Identify Node.js globals leaking into the browser bundle
4. Identify environment variable or config mismatches
5. Identify whether CSS is missing, scoped, or overridden in prod
6. Identify if dynamic imports break after build
7. Explain why BrowserOnly does not prevent the failure

Constraints:
- No fixes
- No code
- No assumptions
- Analyze production-only behavior

Output:
- Clear root causes (not symptoms)
- File-level responsibility
- Explanation of why localhost works but GitHub Pages fails
- Concrete conclusions for next steps

## Analysis Response

### Root Causes Identified:

1. **Node.js Global Variable Issue (`process` not defined)**:
   - **File Level Responsibility**: `frontend/src/services/api.js`
   - **Issue**: The API service file contains `process.env.REACT_APP_API_BASE_URL` which works in development (where Webpack/Browserify polyfills `process`) but fails in production builds where `process` is not defined in the browser
   - **Why localhost works**: Development server (Webpack) provides polyfills for Node.js globals like `process.env`
   - **Why GitHub Pages fails**: Production build strips these polyfills to reduce bundle size, leaving `process` undefined in browsers

2. **Dynamic Import Failure Propagation**:
   - **File Level Responsibility**: `frontend/src/components/ChatLoader/ChatLoader.tsx`
   - **Issue**: When the ChatKit component fails to load due to the API service error, the ChatLoader catches the error but fails silently
   - **Why BrowserOnly doesn't prevent**: BrowserOnly only prevents server-side rendering of the component, but doesn't prevent runtime errors that occur after the component mounts in the browser

3. **Environment Detection Logic**:
   - **File Level Responsibility**: `frontend/src/services/api.js`
   - **Issue**: The current environment detection logic may not work properly in all deployment contexts
   - **Localhost works**: Uses `localhost` detection which functions during development
   - **GitHub Pages fails**: The hostname detection may not properly identify the GitHub Pages URL, or the API endpoint configuration may be incorrect

4. **Bundle Size and Optimization Differences**:
   - **Build System**: Docusaurus production builds apply different optimizations than development
   - **Tree Shaking**: May remove seemingly unused code that's actually needed
   - **Minification**: Can cause issues with dynamic imports or variable references
   - **Why localhost works**: Development mode doesn't apply aggressive optimizations that might break dynamic imports
   - **Why GitHub Pages fails**: Production optimizations may interfere with dynamic import mechanisms

5. **CSS and Styling Issues**:
   - **File Level Responsibility**: `frontend/src/components/ChatKit/ChatKit.css`
   - **Issue**: Production build may have different CSS scoping or minification that affects visibility
   - **Possible scenario**: CSS rules might be overridden by Docusaurus themes in production but not in development

### Explanation of Why BrowserOnly Doesn't Prevent the Failure

BrowserOnly only ensures the component is not rendered during server-side rendering. However, the failure occurs during the component's lifecycle after mounting in the browser:
1. BrowserOnly renders the ChatLoader component in the browser
2. ChatLoader attempts to dynamically import ChatKit
3. ChatKit imports the API service which contains the `process.env` reference
4. The `process` variable is undefined in production, causing a ReferenceError
5. The error propagates up and the component fails to render

### File-Level Responsibility Summary

- **Primary**: `frontend/src/services/api.js` - Contains the `process.env` reference causing the core issue
- **Secondary**: `frontend/src/components/ChatLoader/ChatLoader.tsx` - Fails to handle dynamic import errors gracefully
- **Tertiary**: `frontend/src/theme/Root.tsx` - Entry point for the ChatKit through BrowserOnly
- **Potential**: `frontend/src/components/ChatKit/ChatKit.tsx` - May have additional environment dependencies

### Next Steps for Resolution

1. **Immediate**: Replace all `process.env` references with browser-compatible environment detection
2. **Secondary**: Add better error boundaries in ChatLoader to handle import failures
3. **Verification**: Test the API service configuration specifically for GitHub Pages deployment context
4. **Debugging**: Add error logging to identify the exact point of failure in production

The core issue is that Node.js-specific globals like `process` are being bundled into the client-side code but aren't available in the production browser environment without proper bundler configuration.