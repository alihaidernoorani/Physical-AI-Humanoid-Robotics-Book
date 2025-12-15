# Research: textbook-mdx-compliance

## Overview
This research document captures findings and decisions related to implementing the textbook MDX compliance update. The research focuses on the technical requirements specified in the feature specification.

## Current State Analysis

### Docusaurus Setup
- The project uses Docusaurus v3.9.2 as the documentation framework
- Content is organized in the `docs/` directory with modules and chapters
- The project is configured for deployment to GitHub Pages
- Sidebar navigation is managed through `sidebars.js`

### File Format Analysis
- Currently using `.md` and `.mdx` files
- `.md` files are standard Markdown
- `.mdx` files support React components and interactive elements
- Need to identify which files require interactive components for MDX conversion

### Interactive Components Requirements
- Toggles (Urdu/English)
- Callouts/Admonitions
- Quizzes
- Other interactive elements that require React components

### Module Structure
- Module 1: The Robotic Nervous System (ROS 2)
- Module 2: The Digital Twin (Gazebo & Unity)
- Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- Module 4: Vision-Language-Action (VLA)
- These names must remain unchanged per constitution requirements

## Technical Decisions

### MDX Migration Strategy
**Decision**: Convert .md files to .mdx only when interactive components are required
**Rationale**: Maintains compatibility and performance for static content while enabling interactivity where needed
**Implementation**: Scan files for required interactive elements before conversion

### Toggle Implementation
**Decision**: Implement Urdu/English toggles as MDX/React components
**Rationale**: Provides dynamic language switching without requiring backend processing
**Implementation**: Create reusable toggle component that switches content display

### Link Verification Process
**Decision**: Implement comprehensive link checking process
**Rationale**: Ensures zero broken link warnings in Docusaurus build
**Implementation**: Use Docusaurus build process and manual verification

## Implementation Approach

### Subagent Roles
1. **MDXMigrationAgent**: Handle file format conversions
2. **ContentWriterAgent**: Improve content quality
3. **ToggleAgent**: Add language toggle functionality
4. **LinkCheckerAgent**: Verify all internal links
5. **FrontpageDesignAgent**: Update homepage layout

### Validation Criteria
- Docusaurus build completes with zero broken link warnings
- All interactive components function correctly
- Frontpage provides clear access to all four modules
- Content maintains technical accuracy and academic clarity
- Navigation structure matches file structure