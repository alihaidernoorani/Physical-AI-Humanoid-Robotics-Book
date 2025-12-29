# Feature Specification: Textbook MDX Compliance

**Feature Branch**: `001-textbook-mdx-compliance`
**Created**: 2025-12-15
**Updated**: 2025-12-29
**Status**: Draft
**Input**: User description: "Translate the UI/UX problems of the Docusaurus textbook into clear, testable requirements. Include requirements for mobile responsiveness, dark mode typography and contrast, diagram rendering using Mermaid, removal of conversion artifacts, proper placement of diagrams with captions, consistent visual rhythm for long chapters, and presence/content of introduction/landing page."

## Objective

Refactor and recreate the existing textbook content to:
- Improve clarity, structure, and reading flow
- Maintain technical accuracy
- Ensure **100% MDX compatibility**
- Remove all MDX/JSX syntax errors that break builds
- Meet mobile-first responsive design standards
- Optimize for dark mode reading experience
- Render all diagrams using native Mermaid with proper captions
- Eliminate all conversion artifacts and placeholder text
- Establish consistent visual rhythm for educational content
- Provide a proper introductory landing page

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mobile-First Content Consumption (Priority: P1)

As a student reading the textbook on a mobile device, I want all content to be readable and navigable without horizontal scrolling or text overflow so that I can study effectively on any screen size.

**Why this priority**: Mobile access is critical for modern learners. Content that overflows or is unreadable on mobile excludes a significant portion of users.

**Independent Test**: Can be fully tested by loading any chapter on a mobile viewport (320px width) and verifying all content is visible without horizontal scrolling.

**Acceptance Scenarios**:

1. **Given** I am viewing any chapter on a mobile device (320px viewport), **When** I scroll vertically, **Then** no content extends beyond the viewport width requiring horizontal scrolling
2. **Given** I am reading body text on mobile, **When** I view the typography, **Then** the font size is at least 16px equivalent with line-height between 1.5-1.7
3. **Given** I am viewing a diagram on mobile, **When** I look at the diagram, **Then** it fits within the viewport width without overflow or is scrollable within its container
4. **Given** I am interacting with navigation or buttons on mobile, **When** I tap interactive elements, **Then** touch targets are at least 44x44px for comfortable interaction

---

### User Story 2 - Dark Mode Reading Experience (Priority: P2)

As a reader studying at night or in low-light conditions, I want the textbook to provide a comfortable dark mode experience with proper contrast so that I can read for extended periods without eye strain.

**Why this priority**: Dark mode is essential for extended reading sessions and accessibility. Poor contrast in dark mode causes eye strain and reduces readability.

**Independent Test**: Can be fully tested by switching to dark mode and verifying all text, diagrams, and UI elements maintain proper contrast ratios.

**Acceptance Scenarios**:

1. **Given** I am reading the textbook in dark mode, **When** I view body text, **Then** the contrast ratio meets WCAG AA standards (minimum 4.5:1 for normal text)
2. **Given** I am viewing a Mermaid diagram in dark mode, **When** I examine the diagram, **Then** all elements (lines, labels, shapes) are clearly visible with sufficient contrast
3. **Given** I am reading in dark mode for an extended period, **When** I view text against backgrounds, **Then** the colors avoid pure white (#FFFFFF) on pure black (#000000) to reduce eye strain
4. **Given** I am viewing code blocks in dark mode, **When** I read the code, **Then** syntax highlighting maintains legibility with appropriate contrast

---

### User Story 3 - Diagram Clarity and Rendering (Priority: P3)

As a visual learner studying complex robotics concepts, I want all diagrams to render correctly as visual elements with descriptive captions so that I can understand system architectures and data flows visually.

**Why this priority**: Diagrams are essential for understanding complex technical concepts. Missing or broken diagrams severely impact comprehension.

**Independent Test**: Can be fully tested by navigating to any chapter containing diagrams and verifying each diagram renders as a visible graphic with an accompanying caption.

**Acceptance Scenarios**:

1. **Given** I am viewing any chapter with diagrams, **When** I look at diagram locations, **Then** each diagram renders as a visible Mermaid graphic (not placeholder text)
2. **Given** I am viewing any diagram, **When** I look below it, **Then** there is a caption describing what the diagram represents
3. **Given** I am searching for diagrams mentioned in text, **When** I navigate to the referenced location, **Then** a corresponding visual diagram exists (no orphan references)
4. **Given** I am viewing diagram source code, **When** I inspect the MDX, **Then** the diagram uses native Mermaid syntax (no custom Diagram components)

---

### User Story 4 - Clean Content Without Artifacts (Priority: P4)

As a reader consuming textbook content, I want the content to be free of conversion artifacts and placeholder text so that my reading experience is professional and uninterrupted.

**Why this priority**: Conversion artifacts disrupt the reading flow and make the textbook appear incomplete or unprofessional.

**Independent Test**: Can be fully tested by searching all chapters for known artifact patterns and verifying zero matches.

**Acceptance Scenarios**:

1. **Given** I am reading any chapter, **When** I search for "Diagram Description:", **Then** zero matches are found
2. **Given** I am reading any chapter, **When** I search for "Figure shows:" or similar placeholder patterns, **Then** zero matches are found
3. **Given** I am viewing any section that should contain a diagram, **When** I look at that location, **Then** there is a rendered visual diagram (not descriptive text replacing the diagram)
4. **Given** I am reading any chapter, **When** I encounter diagram references, **Then** the actual diagrams exist at those locations

---

### User Story 5 - Consistent Visual Hierarchy (Priority: P5)

As a student reading long chapters, I want consistent visual rhythm with clear section breaks and hierarchy so that I can easily navigate and understand the content structure.

**Why this priority**: Consistent visual hierarchy aids comprehension and navigation in long-form educational content.

**Independent Test**: Can be fully tested by reading through any chapter and verifying headings follow a consistent size/weight progression and sections have consistent spacing.

**Acceptance Scenarios**:

1. **Given** I am reading any chapter, **When** I observe heading levels, **Then** h1 > h2 > h3 maintain clear visual distinction (size/weight)
2. **Given** I am reading long-form content, **When** I scroll through sections, **Then** there is consistent whitespace between major sections
3. **Given** I am looking for key definitions or callouts, **When** I scan the page, **Then** these elements are visually distinct from body text
4. **Given** I am navigating the textbook, **When** I view chapter titles, **Then** they are prominent and easily scannable

---

### User Story 6 - Introductory Landing Page (Priority: P6)

As a new visitor to the textbook, I want an introductory landing page that clearly presents the book's purpose and navigation so that I can understand what the textbook covers and how to access content.

**Why this priority**: The landing page creates the first impression and serves as the navigation hub for the entire textbook.

**Independent Test**: Can be fully tested by loading the root URL and verifying all required elements are present and functional.

**Acceptance Scenarios**:

1. **Given** I navigate to the textbook root URL, **When** the page loads, **Then** I see a clear book title and subtitle
2. **Given** I am on the landing page, **When** I look for module navigation, **Then** I see cards or links to all four modules (The Robotic Nervous System, The Digital Twin, The AI-Robot Brain, Vision-Language-Action)
3. **Given** I click on any module card, **When** the navigation occurs, **Then** I am taken to that module's content
4. **Given** I view the landing page on any device, **When** I observe the layout, **Then** it is responsive and properly formatted for that viewport size

---

### Edge Cases

- What happens when a Mermaid diagram is too complex to fit on mobile viewports?
- How does the system handle content that legitimately needs horizontal scrolling (e.g., wide code blocks)?
- What occurs when dark mode preference changes mid-session?
- How are images/diagrams handled that cannot be converted to Mermaid format?
- What happens when a chapter has no diagrams but references are present?

## Requirements *(mandatory)*

### Mobile Responsiveness Requirements

- **FR-MR-001**: All text content MUST be readable at 320px viewport width without horizontal scrolling
- **FR-MR-002**: Body text MUST have a minimum font size equivalent to 16px
- **FR-MR-003**: Line height MUST be between 1.5 and 1.7 for body text
- **FR-MR-004**: No content element MUST cause horizontal overflow at mobile viewports
- **FR-MR-005**: Interactive elements MUST have touch targets of at least 44x44px
- **FR-MR-006**: Diagrams MUST either fit within mobile viewport or be contained in a scrollable container
- **FR-MR-007**: Navigation MUST be accessible and usable on mobile devices

### Dark Mode Requirements

- **FR-DM-001**: All text MUST maintain WCAG AA contrast ratio (4.5:1 minimum) in dark mode
- **FR-DM-002**: Dark mode MUST avoid pure white (#FFFFFF) text on pure black (#000000) backgrounds
- **FR-DM-003**: Code blocks MUST be legible with appropriate syntax highlighting in dark mode
- **FR-DM-004**: Mermaid diagrams MUST be clearly visible in dark mode with sufficient contrast
- **FR-DM-005**: All UI elements (buttons, links, navigation) MUST maintain visibility in dark mode
- **FR-DM-006**: Dark mode theming for diagrams MUST use Docusaurus Mermaid plugin's automatic theme switching (no manual per-diagram theming)

### Diagram Requirements

- **FR-DG-001**: All diagrams MUST be rendered using native Mermaid syntax
- **FR-DG-002**: Custom diagram rendering components MUST NOT be used unless explicitly justified
- **FR-DG-003**: Every diagram MUST have a visible rendered representation (no placeholder text)
- **FR-DG-004**: Every diagram MUST have an accompanying caption describing its purpose
- **FR-DG-005**: Diagrams MUST be responsive and not overflow on mobile viewports
- **FR-DG-006**: All diagram references in text MUST correspond to actual rendered diagrams
- **FR-DG-007**: Diagrams MUST render correctly in both light and dark modes
- **FR-DG-008**: Diagram descriptions that are too abstract for visual representation MUST be converted to explanatory prose instead of forced Mermaid diagrams
- **FR-DG-009**: Mermaid diagrams MUST target simple, readable complexity: 5-10 nodes maximum, clear labels, basic styling for emphasis
- **FR-DG-010**: Diagrams MUST render at build time (SSG); no client-side JavaScript required for diagram viewing

### Conversion Artifact Removal Requirements

- **FR-CA-001**: No content MUST contain "Diagram Description:" or similar placeholder patterns
- **FR-CA-002**: No content MUST contain descriptive text that replaces actual visual diagrams
- **FR-CA-003**: No content MUST contain empty or commented-out diagram blocks
- **FR-CA-004**: No content MUST contain references to diagrams that do not exist
- **FR-CA-005**: No content MUST contain "Figure shows:", "The diagram below shows:", or equivalent placeholder text

### Visual Hierarchy Requirements

- **FR-VH-001**: Heading levels MUST maintain clear visual distinction (h1 > h2 > h3)
- **FR-VH-002**: Major sections MUST have consistent whitespace separation
- **FR-VH-003**: Key definitions and callouts MUST be visually distinct from body text
- **FR-VH-004**: Chapter titles MUST be prominent and easily scannable
- **FR-VH-005**: Content MUST follow textbook-style visual hierarchy (not API documentation style)
- **FR-VH-006**: Pull quotes and key concepts MUST be styled distinctly

### Landing Page Requirements

- **FR-LP-001**: Landing page MUST display a clear book title and subtitle
- **FR-LP-002**: Landing page MUST include navigation cards for all four modules
- **FR-LP-003**: Module cards MUST link correctly to their respective content
- **FR-LP-004**: Landing page MUST be responsive across all viewport sizes
- **FR-LP-005**: Landing page visual hierarchy MUST emphasize textbook identity (not API docs)

### Regression Prevention Requirements

- **FR-RP-001**: Build process MUST include automated validation that fails on conversion artifact patterns (e.g., "Diagram Description:", "Figure shows:")
- **FR-RP-002**: Build process MUST validate all Mermaid diagrams render successfully at build time
- **FR-RP-003**: Build process MUST fail if any diagram reference in text lacks a corresponding rendered diagram
- **FR-RP-004**: New content imports MUST pass all build-time validation checks before merging

### SSG Constraints

- **FR-SSG-001**: All content MUST be fully renderable at build time without client-side JavaScript
- **FR-SSG-002**: Core content viewing (text, diagrams, navigation) MUST NOT require JavaScript execution
- **FR-SSG-003**: Theme switching (light/dark) MAY use client-side JavaScript as it is a progressive enhancement
- **FR-SSG-004**: All Mermaid diagrams MUST be pre-rendered to SVG during static site generation

### Existing MDX Compliance Requirements (Preserved)

- **FR-MDX-001**: All textbook content MUST be 100% MDX-safe and compatible with Docusaurus builds
- **FR-MDX-002**: Square brackets MUST NOT be placed inside JSX or attribute positions
- **FR-MDX-003**: Invalid JSX attributes (commas, colons, unquoted values) MUST NOT exist
- **FR-MDX-004**: Pure Markdown MUST be used unless JSX is absolutely necessary
- **FR-MDX-005**: Code examples MUST be wrapped in fenced code blocks
- **FR-MDX-006**: Raw HTML MUST NOT be mixed with Markdown unless MDX-safe

### Key Entities

- **Chapter Content**: Individual MDX files containing textbook content with text, diagrams, and interactive elements
- **Mermaid Diagram**: Visual representation using Mermaid syntax with accompanying caption
- **Landing Page**: Entry point for the textbook with module navigation and book overview
- **Visual Theme**: Light/dark mode presentation layer affecting typography and contrast
- **Viewport**: Device screen dimensions affecting responsive layout behavior

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of chapters are readable on 320px viewport without horizontal scrolling
- **SC-002**: 100% of text elements meet WCAG AA contrast ratio in both light and dark modes
- **SC-003**: 100% of diagrams render as visible Mermaid graphics (zero placeholder text instances)
- **SC-004**: 100% of diagrams have accompanying captions
- **SC-005**: Zero instances of "Diagram Description:" or similar conversion artifacts across all content
- **SC-006**: Landing page exists with all four module cards linking correctly
- **SC-007**: Docusaurus build completes with zero MDX/JSX syntax errors
- **SC-008**: Body text font size is 16px minimum across all chapters
- **SC-009**: Line height is between 1.5-1.7 for all body text
- **SC-010**: All interactive elements have touch targets of at least 44x44px
- **SC-011**: All heading levels maintain clear visual distinction when viewed
- **SC-012**: Chapter reading flow is uninterrupted by formatting issues or artifacts
- **SC-013**: All Mermaid diagrams have 10 or fewer nodes for readability
- **SC-014**: Build-time validation catches 100% of known artifact patterns before deployment
- **SC-015**: All content renders completely without client-side JavaScript (SSG compliance)
- **SC-016**: Diagrams automatically adapt to dark/light mode without manual intervention

## Assumptions

- Docusaurus built-in Mermaid plugin is available and configured
- Dark mode is implemented via Docusaurus theme switching (user preference respected)
- Mobile testing uses standard viewport widths (320px, 375px, 414px as breakpoints)
- WCAG AA compliance is the minimum accessibility target
- Existing module structure (4 modules) remains unchanged per constitution
- No custom React components are needed for diagram rendering
- Mermaid diagrams are pre-rendered to SVG at build time (SSG)
- Build process can be extended with custom validation scripts
- Abstract concepts that cannot be visualized will be converted to explanatory prose
- Docusaurus Mermaid plugin supports automatic dark/light theme detection

## Clarifications

### Session 2025-12-15

- Q: What is the maximum extent of content changes allowed during rewrites that still preserves original technical meaning? → A: Substantial reorganization and rewriting is allowed as long as technical accuracy is preserved
- Q: What specific criteria should be used to determine if a reference is non-essential and can be removed? → A: All reader-facing references, but all claims must be source-verified internally
- Q: How should technical accuracy be verified when content undergoes substantial reorganization and rewriting? → A: Through subject matter expert review and comparison with original source material
- Q: What level of content structure (sections, subsections, headings) must be preserved during the rewrite process? → A: Only top-level module structure and main chapter divisions must be preserved

### Session 2025-12-29

- Mobile viewport testing baseline: 320px as minimum, 375px and 414px as additional breakpoints
- Dark mode contrast: WCAG AA (4.5:1 for normal text, 3:1 for large text) as minimum standard
- Diagram technology: Native Mermaid via Docusaurus plugin; custom components prohibited
- Landing page scope: Module navigation cards, book title/subtitle, responsive design

### Session 2025-12-29 (Clarification Round 2)

- Q: Should all diagram descriptions become Mermaid diagrams, or should some be converted to prose? → A: Mermaid-first with prose fallback: Convert to Mermaid where possible; rewrite as explanatory prose if concept is too abstract for visual representation
- Q: What complexity level should Mermaid diagrams target? → A: Simple and readable: 5-10 nodes, clear labels, basic styling for emphasis, optimized for mobile viewing
- Q: How should Mermaid diagrams adapt to dark mode? → A: Automatic theme switching via Docusaurus Mermaid plugin's built-in dark/light theme detection (no manual theming)
- Q: How should future content imports be handled to prevent regression? → A: Build-time validation: Add automated checks during Docusaurus build that fail on artifact patterns
- Q: What SSG-specific constraints should be enforced? → A: Strict static-only: All diagrams must render at build time; no client-side JavaScript required for core content viewing
