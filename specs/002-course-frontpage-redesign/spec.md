# Feature Specification: Course Frontpage Redesign

**Feature Branch**: `002-course-frontpage-redesign`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Redesign the frontpage of a 13-week technical AI/robotics course Docusaurus book with hero section, animated module cards grid, progress timelines, dark/light mode, and responsive design."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - First-time Visitor Orientation (Priority: P1)

A prospective student visits the course homepage to understand what the course covers and decide if it's relevant to their learning goals.

**Why this priority**: The frontpage is the first touchpoint for all users. If visitors cannot quickly understand the course structure and value proposition, they will leave before exploring content.

**Independent Test**: Can be fully tested by loading the homepage and verifying all visual elements render correctly with clear navigation paths.

**Acceptance Scenarios**:

1. **Given** a user visits the frontpage, **When** the page loads, **Then** a hero section displays the course title, tagline, and brief description within 3 seconds
2. **Given** the hero section is visible, **When** the user scrolls down, **Then** module cards appear in a visually organized grid layout
3. **Given** module cards are displayed, **When** the user views any card, **Then** they can see the module title, description, duration (weeks), and progress timeline

---

### User Story 2 - Module Navigation via Cards (Priority: P2)

A student wants to quickly navigate to a specific module from the frontpage by clicking on the relevant module card.

**Why this priority**: Primary navigation mechanism for course content; directly impacts learning workflow and user engagement.

**Independent Test**: Can be fully tested by clicking each module card and verifying correct navigation to the module introduction page.

**Acceptance Scenarios**:

1. **Given** a user hovers over a module card, **When** the hover state activates, **Then** the card displays a visual animation (scale/lift effect) within 200ms
2. **Given** a user clicks on a module card, **When** the click event fires, **Then** the user is navigated to the corresponding module introduction page
3. **Given** a module card is in view, **When** the user focuses on it (keyboard/mouse), **Then** the card shows clear visual focus indication for accessibility

---

### User Story 3 - Dark/Light Mode Toggle (Priority: P3)

A user wants to switch between dark and light modes based on their viewing preference or ambient lighting conditions.

**Why this priority**: Essential for accessibility and user comfort during extended reading sessions; prevents eye strain.

**Independent Test**: Can be fully tested by toggling the theme and verifying all frontpage components render correctly in both modes.

**Acceptance Scenarios**:

1. **Given** the page is in light mode, **When** a user toggles to dark mode, **Then** all frontpage elements (hero, cards, progress bars, backgrounds) update to dark theme colors
2. **Given** the page is in dark mode, **When** a user views module cards, **Then** text contrast meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
3. **Given** the page respects system preferences, **When** the user's OS is set to dark mode, **Then** the page loads in dark mode by default

---

### User Story 4 - Mobile Responsive Experience (Priority: P4)

A user accesses the frontpage on a mobile device and needs to view and interact with all content comfortably on a smaller screen.

**Why this priority**: Significant portion of users access educational content on mobile; poor mobile experience leads to abandonment.

**Independent Test**: Can be fully tested by viewing the frontpage on various viewport sizes and verifying layout adjustments.

**Acceptance Scenarios**:

1. **Given** a user views the frontpage on a screen narrower than 768px, **When** the page renders, **Then** module cards display in a single-column stacked layout
2. **Given** a user views the frontpage on desktop (wider than 768px), **When** the page renders, **Then** module cards display in a responsive grid layout (2-3 columns)
3. **Given** a mobile user taps a module card, **When** the tap completes, **Then** the tap target is at least 44x44 pixels for comfortable interaction

---

### User Story 5 - Course Progress Visualization (Priority: P5)

A student wants to see the overall 13-week timeline and understand which weeks correspond to which modules.

**Why this priority**: Provides mental model of course structure and time commitment; helps with learning planning.

**Independent Test**: Can be fully tested by viewing module cards and verifying progress timeline bars display with correct week ranges.

**Acceptance Scenarios**:

1. **Given** a module card displays, **When** the user views the progress timeline, **Then** a visual bar shows the week range for that module (e.g., Weeks 1-3)
2. **Given** progress timelines are visible, **When** the user views all module cards, **Then** the combined timelines represent the full 13-week course duration
3. **Given** the page is in dark mode, **When** progress bars render, **Then** progress bar colors maintain sufficient contrast against the dark background

---

### Edge Cases

- What happens when JavaScript is disabled?
  - Hero section and static content must remain visible
  - Cards must be clickable links (not JS-dependent)

- How does the system handle very long module descriptions?
  - Descriptions truncate with ellipsis after 3 lines
  - Full description available on module page

- What happens on extremely narrow viewports (<320px)?
  - Minimum supported viewport is 320px
  - Cards stack vertically with horizontal padding

- How does the page handle slow network connections?
  - Hero content (text) loads first
  - Images/animations load progressively
  - No layout shift when animations initialize

- How are quiz/exercise components styled if custom MDX/JSX is used?
  - If using theme tokens, they adapt automatically
  - If hard-coded colors exist, replace with CSS variables referencing theme tokens

## Requirements *(mandatory)*

### Functional Requirements

#### Hero Section
- **FR-001**: The frontpage MUST display a hero section with the course title "Physical AI & Humanoid Robotics"
- **FR-002**: The hero section MUST display the course tagline "AI Systems in the Physical World: Embodied Intelligence"
- **FR-003**: The hero section MUST display a brief description paragraph (2-3 sentences) explaining the course scope
- **FR-004**: The hero section MUST have a visually distinct gradient background that works in both light and dark modes
- **FR-005**: The hero section MUST be fully visible without scrolling on standard desktop viewports (1280px+)

#### Module Cards Grid
- **FR-006**: The frontpage MUST display module cards for all 4 course modules in a grid layout
- **FR-007**: Each module card MUST display the module number (1-4), title, and subtitle/technology name
- **FR-008**: Each module card MUST display a description of 30-60 words summarizing the module content
- **FR-009**: Each module card MUST display the estimated duration in weeks
- **FR-010**: Each module card MUST display a visual progress timeline showing which weeks of the 13-week course it covers
- **FR-011**: Module cards MUST link directly to the corresponding module introduction page
- **FR-012**: Module cards MUST display a subtle hover/focus animation with a lift effect (2-4px translateY, 200ms transition duration)
- **FR-013**: Each module card MUST have a subtle per-module color accent (e.g., left border) for visual differentiation

#### Design System
- **FR-014**: The design MUST use a modern sans-serif font (Inter, Poppins, or system font stack)
- **FR-015**: The design MUST use Docusaurus CSS theme tokens exclusively (--ifm-color-*, --ifm-background-*) for all colors to ensure automatic dark mode support
- **FR-016**: Progress timeline bars MUST use distinct colors for each module derived from theme color variables
- **FR-017**: All interactive elements MUST have a minimum touch target size of 44x44 pixels
- **FR-018**: Buttons MUST have rounded corners (border-radius of 8px or more)

#### Responsive Design
- **FR-019**: The module grid MUST display as 2 columns on tablets (768px-1024px viewport)
- **FR-020**: The module grid MUST display as a single column on mobile (<768px viewport)
- **FR-021**: The hero section MUST scale text size appropriately for mobile viewports
- **FR-022**: All content MUST be accessible without horizontal scrolling on viewports ≥320px

#### Dark Mode & Accessibility
- **FR-023**: All text MUST maintain WCAG AA contrast ratios (4.5:1 minimum) in both light and dark modes
- **FR-024**: The page MUST respect the user's system color scheme preference (prefers-color-scheme)
- **FR-025**: Interactive elements MUST have visible focus indicators for keyboard navigation
- **FR-026**: Progress bars MUST not rely solely on color to convey information (include week labels)

#### Branding & Cleanup
- **FR-027**: The favicon MUST be replaced with a course-specific icon (robot or AI-themed, minimalistic style)
- **FR-028**: Default Docusaurus logos MUST be removed or replaced with course branding reflecting a hybrid technical-education aesthetic (modern, professional, balanced)
- **FR-029**: Footer links MUST be relevant to the course (GitHub repo, resources) - remove unrelated defaults
- **FR-030**: Navbar MUST display the course name and primary navigation to textbook content

#### Internal Content Dark Mode (Visual Fixes Only)
- **FR-031**: Quiz components MUST use theme background tokens and maintain WCAG AA contrast in dark mode
- **FR-032**: Exercise containers MUST use theme surface colors (--ifm-background-surface-color) instead of hard-coded backgrounds
- **FR-033**: Callout/admonition components MUST be readable in dark mode with appropriate border and background contrast
- **FR-034**: Interactive components (buttons, inputs in quizzes) MUST have visible borders/outlines in dark mode
- **FR-035**: All internal content components MUST inherit typography from theme tokens (no hard-coded light-mode-only colors)

### Key Entities

- **Module**: Represents a course unit (1-4); attributes include number, title (e.g., "The Robotic Nervous System"), subtitle (e.g., "ROS 2"), description (30-60 words), duration_weeks, week_start, week_end, introduction_link. Titles are final and match existing docs structure.
- **Progress Timeline**: Visual representation of a module's position within the 13-week course; shows week_start to week_end as a colored bar. Does not include assessment milestones or prerequisites (those belong on module pages).
- **Theme**: User preference state (light/dark); persisted in browser storage

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: First-time visitors can identify the course purpose within 5 seconds of page load
- **SC-002**: Users can navigate to any module content in 2 clicks or fewer from the frontpage
- **SC-003**: Page achieves Lighthouse Accessibility score of 90+ in both light and dark modes
- **SC-004**: Module cards display and respond to hover interactions within 200ms
- **SC-005**: Page layout renders correctly on 95% of browsers released in the last 3 years (Chrome, Firefox, Safari, Edge)
- **SC-006**: Mobile users (viewport <768px) can access all module cards without horizontal scrolling
- **SC-007**: All interactive elements are keyboard-accessible with visible focus states
- **SC-008**: Page content remains usable when JavaScript fails to load (progressive enhancement)
- **SC-009**: Hero section and module cards have 0 layout shift after initial render (CLS < 0.1)
- **SC-010**: Dark mode text contrast ratios verified at 4.5:1 minimum for body text

## Clarifications

### Session 2025-12-30 (Course Structure)

- Q: Should we use a new 6-module structure or keep existing 4-module structure? → A: Keep existing 4-module structure with 13-week distribution (aligns with current codebase docs structure)
- Q: Are module titles final or subject to renaming? → A: Titles are final — use as-is (The Robotic Nervous System, The Digital Twin, The AI-Robot Brain, Vision-Language-Action)
- Q: What is Unity's dependency status in Module 2? → A: Introductory only — mentioned but not a core dependency (Gazebo is primary)
- Q: Should module cards display explicit prerequisites? → A: No — sequential numbering implies order; prerequisite details belong on module introduction pages
- Q: Should assessment milestones be indicated on frontpage timeline? → A: No — assessments belong in module content, not frontpage overview

### Session 2025-12-30 (UI/UX Design)

- Q: Should all frontpage components rely exclusively on Docusaurus CSS variables/theme tokens? → A: Yes — exclusively use Docusaurus theme tokens (--ifm-color-*, --ifm-background-*) for automatic dark mode support and consistency
- Q: What visual tone should the frontpage convey? → A: Hybrid technical-education — modern but professional, balanced visuals (not overly academic, futuristic, or commercial)
- Q: Should each module card have distinct color accents? → A: Subtle accents — minimal per-module color (e.g., left border only) for differentiation without overwhelming design
- Q: Should animations be subtle or expressive? → A: Subtle — minimal transforms (2-4px lift, 200ms duration), educational tone (not product-style)
- Q: Does this feature scope include internal content pages (quizzes, exercises, module chapters)? → A: Yes — include dark mode optimization for quizzes, exercises, callouts, and interactive components (visual fixes only, not functional changes)

## Assumptions

1. **Course Structure**: The course consists of 4 modules spanning 13 weeks total:
   - Module 1: The Robotic Nervous System (ROS 2) — Weeks 1-3
   - Module 2: The Digital Twin (Gazebo & Unity) — Weeks 4-6
   - Module 3: The AI-Robot Brain (NVIDIA Isaac) — Weeks 7-10
   - Module 4: Vision-Language-Action (VLA) — Weeks 11-13

2. **Technology Stack**: Implementation will use Docusaurus v3.x with React components and CSS modules (existing stack)

3. **Animation Library**: CSS transitions will be preferred over JavaScript animations for performance; Framer Motion may be used if complex animations are required

4. **Font Hosting**: Fonts will be loaded via system font stack or locally hosted files (no external CDN dependency for privacy)

5. **Browser Support**: Modern browsers only (Chrome 90+, Firefox 90+, Safari 14+, Edge 90+); no IE11 support required

6. **Existing Content**: Module descriptions and week assignments will be derived from existing course content in the `docs/` directory. Unity is mentioned as introductory/optional in Module 2; Gazebo is the primary simulation tool.

## Constraints

- Must integrate with existing Docusaurus theming system (Infima CSS framework)
- Must not break existing navigation to docs content
- Must maintain fast initial page load (<3 seconds on 3G connection)
- Must not add large JavaScript bundles that impact performance
- Internal content dark mode fixes are **visual only** — no changes to quiz logic, exercise functionality, or assessment mechanics
