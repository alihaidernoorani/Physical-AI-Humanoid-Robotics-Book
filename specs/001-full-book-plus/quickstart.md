# Quickstart Guide: Interactive Physical AI & Humanoid Robotics Textbook

## Overview
This guide provides a quick introduction to implementing the interactive features for the Physical AI & Humanoid Robotics textbook, including authentication, personalization, Urdu translation, and UI enhancements.

## Prerequisites
- Node.js 18+ installed
- Docusaurus v3.9.2 project already set up
- Basic knowledge of React and JavaScript
- Understanding of Claude Code Subagent/Skill patterns

## Setup Steps

### 1. Install Dependencies
```bash
npm install better-auth
# Other dependencies will be installed as needed during implementation
```

### 2. Create Directory Structure
Create the following directory structure in your project root:

```
src/
├── components/
│   ├── auth/
│   ├── personalization/
│   ├── translation/
│   └── ui/
├── utils/
└── theme/
.claude/
├── subagents/
│   └── urdu_translator/
└── skills/
    └── urdu-translation-skill/
```

### 3. Initialize Claude Code Subagent & Skill
Create the Claude Code framework files:

**.claude/subagents/urdu_translator/agent.md**:
```markdown
# UrduTranslator Subagent

This subagent handles Urdu translation requests by loading the urdu-translation-skill when needed.

## Capabilities
- Load translation skill on demand
- Process chapter content for translation
- Manage translation state and caching
```

**.claude/skills/urdu-translation-skill/skill.yaml**:
```yaml
name: urdu-translation-skill
version: 1.0.0
description: Translates English text to Urdu using LibreTranslate API
interface:
  input: Text content to translate
  output: Urdu translated content
  method: translate(text)
```

### 4. Implementation Order
Follow this sequence for implementation:

1. **Authentication Layer**:
   - Create SignupModal component
   - Implement localStorage profile persistence
   - Set up ProfileContext for global state

2. **UI Enhancement Layer**:
   - Add custom CSS for typography improvements
   - Create callout components for "Key Takeaways" and "Ethical Notes"
   - Update MDX components to include new styling

3. **Personalization Engine**:
   - Create PersonalizationButton component
   - Implement ContentAdapter for dynamic content adjustment
   - Connect to user profile data

4. **Translation System**:
   - Create UrduTranslationButton component
   - Implement UrduTranslatorSubagent
   - Connect to LibreTranslate API
   - Handle RTL layout switching

## Testing
- Verify all 21 chapters display new buttons
- Test localStorage profile persistence
- Confirm Urdu translation renders with RTL layout
- Validate bundle size stays under 500KB
- Run Lighthouse audit (target >85 score)

## Deployment
- Build the Docusaurus site: `npm run build`
- Verify GitHub Pages compatibility
- Test all features on deployed site