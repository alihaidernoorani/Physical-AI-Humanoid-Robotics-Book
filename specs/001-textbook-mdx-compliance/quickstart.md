# Quickstart: textbook-mdx-compliance

## Overview
This quickstart guide provides the essential steps to implement the textbook MDX compliance update. This feature focuses on migrating .md files to .mdx where interactive components are required, improving content quality, fixing broken links, and ensuring proper navigation.

## Prerequisites
- Node.js 18+ installed
- Docusaurus v3.9.2 project setup
- Git repository with existing textbook content
- Basic knowledge of MDX and React components

## Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Verify the current setup:
   ```bash
   npm run build
   ```

## Implementation Steps

### 1. MDX Migration
- Scan all .md files in the `docs/` directory
- Identify files that require interactive components (toggles, callouts, quizzes)
- Convert these files to .mdx while preserving file names, routing, and titles
- Skip conversion for files without interactive components

### 2. Toggle Implementation
- Add Urdu/English toggle buttons to chapters/pages where missing
- Implement toggles as frontend-only MDX/React components
- Ensure English is default; Urdu content may be shown if present, else placeholder

### 3. Content Refinement
- Refine existing chapter content for clarity, depth, and pedagogical quality
- Complete incomplete sections defined in the course outline
- Add missing examples, diagrams, exercises, quizzes, and glossary entries

### 4. Link Verification
- Scan all internal links within chapters and frontpage
- Fix broken or missing links
- Ensure cross-links point only to existing files
- Confirm images, diagrams, and assets resolve correctly

### 5. Frontpage Update
- Review and improve homepage layout
- Ensure all four modules are clearly visible
- Each module card must navigate to its correct module entry page
- Use module names verbatim as locked in the constitution

## Validation
Run the following commands to validate your changes:

1. Build the site:
   ```bash
   npm run build
   ```

2. Verify no broken link warnings:
   ```bash
   # Check build output for any 404 warnings
   ```

3. Run local server to test navigation:
   ```bash
   npm run start
   ```

## Key Files and Directories
- `docs/` - Contains all textbook content files
- `src/components/` - Contains React components including toggle components
- `sidebars.js` - Defines navigation structure
- `docusaurus.config.js` - Main Docusaurus configuration

## Important Notes
- Module names are locked and must not change: "The Robotic Nervous System (ROS 2)", "The Digital Twin (Gazebo & Unity)", "The AI-Robot Brain (NVIDIA Isaac™)", "Vision-Language-Action (VLA)"
- Only convert .md files to .mdx when interactive components are required
- Ensure all internal links point to existing files to avoid 404 errors
- Test all interactive components after implementation