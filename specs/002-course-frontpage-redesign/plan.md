# Implementation Plan: Course Frontpage Redesign & UI/UX Improvements

**Branch**: `002-course-frontpage-redesign` | **Date**: 2025-12-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-course-frontpage-redesign/spec.md`

## Summary

Redesign the Docusaurus-based course frontpage to create a modern, professional landing experience with animated module cards, 13-week timeline visualization, and comprehensive dark mode optimization across all UI components. This includes:

- **Frontpage**: Custom hero section + 4-module card grid with timeline bars
- **Design System**: Dark-mode-first CSS variable system using Infima tokens
- **Branding**: Replace default Docusaurus assets with course-specific identity
- **Dark Mode Fixes**: Visual optimization for quizzes, exercises, callouts (no functional changes)
- **Visual Tone**: Hybrid technical-education aesthetic (modern, professional, balanced)

**Technical Approach**: CSS-first with progressive enhancement; leverage existing Docusaurus theming; use CSS modules for custom components; maintain <3s initial page load.

## Technical Context

**Language/Version**: TypeScript/JavaScript (ES2020+), React 18, CSS3
**Primary Dependencies**: Docusaurus v3.9, React 18, Infima CSS framework
**Storage**: N/A (static site generation)
**Testing**: Manual visual regression, Lighthouse CI, WCAG contrast validation
**Target Platform**: Static site (GitHub Pages), modern browsers (Chrome 90+, Firefox 90+, Safari 14+, Edge 90+)
**Project Type**: Web (frontend-only, existing Docusaurus site)
**Performance Goals**: <3s initial page load on 3G, Lighthouse Performance 90+, Accessibility 90+
**Constraints**: No large JS bundles, maintain existing docs navigation, integrate with Infima theming system
**Scale/Scope**: 1 frontpage, 4 module cards, 5 custom components, ~15-20 CSS files (global + modules)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Scientific Accuracy**: UI/UX design decisions grounded in accessibility standards (WCAG AA) and web performance best practices
- ✅ **Academic Clarity**: Visual design supports learning goals with clear information hierarchy and minimal cognitive load
- ✅ **Reproducibility & Transparency**: All design tokens, spacing scales, and color systems documented in design system
- ✅ **Ethical & Safety Awareness**: Dark mode prevents eye strain; accessibility ensures inclusive access for all learners
- ✅ **Module Structure Compliance**: Frontpage displays all 4 modules with locked names (The Robotic Nervous System, The Digital Twin, The AI-Robot Brain, Vision-Language-Action)
- ✅ **Frontend Architecture**: Builds on existing Docusaurus v3.9 structure; uses React components and CSS modules
- ⚠️ **Backend Architecture**: N/A for this feature (frontend-only)
- ⚠️ **Personalization & Translation**: Out of scope for frontpage redesign (handled by existing backend)
- ✅ **Change Control**: Module names and structure are immutable; frontpage reflects existing 4-module architecture

**Post-Design Re-check**: Will validate that design system adheres to constitution after Phase 1.

## Project Structure

### Documentation (this feature)

```text
specs/002-course-frontpage-redesign/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (design patterns, Infima tokens, accessibility)
├── data-model.md        # Phase 1 output (component props, theme token schema)
├── quickstart.md        # Phase 1 output (local dev setup, component usage)
├── contracts/           # Phase 1 output (component API contracts, CSS variable schema)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── components/
│   │   ├── HomepageFeatures/     # Existing (may be replaced/removed)
│   │   ├── ModuleCard/            # NEW: Module card component
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   ├── TimelineBar/           # NEW: Progress timeline component
│   │   │   ├── index.tsx
│   │   │   └── styles.module.css
│   │   └── HeroSection/           # NEW: Custom hero component
│   │       ├── index.tsx
│   │       └── styles.module.css
│   ├── pages/
│   │   ├── index.tsx              # MODIFY: Frontpage (complete redesign)
│   │   └── index.module.css       # MODIFY: Frontpage styles
│   ├── css/
│   │   ├── custom.css             # MODIFY: Add design system tokens
│   │   ├── readability.css        # EXISTING: Maintain
│   │   ├── diagrams.css           # EXISTING: Maintain
│   │   ├── dark-mode-fixes.css    # NEW: Quiz/exercise dark mode overrides
│   │   └── module-accents.css     # NEW: Per-module color accents
│   └── theme/                     # Docusaurus theme customizations (if needed)
├── static/
│   └── img/
│       ├── favicon.ico            # REPLACE: Course-specific icon
│       └── logo.svg               # REPLACE: Course branding
├── docusaurus.config.ts           # MODIFY: Update metadata, navbar, footer
└── sidebars.ts                    # EXISTING: No changes

docs/                              # EXISTING: No structural changes (only dark mode CSS fixes)
```

**Structure Decision**: Leverages existing Docusaurus frontend structure. All new components live in `frontend/src/components/`. Design system tokens extend `frontend/src/css/custom.css`. Dark mode fixes isolated in separate CSS file for maintainability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations requiring justification.*

## Phase 0: Research & Discovery

### Research Tasks

1. **Infima CSS Token Exploration**
   - **Goal**: Document all available `--ifm-*` CSS variables for colors, spacing, typography
   - **Method**: Inspect Docusaurus Infima source, test in DevTools
   - **Output**: Token inventory categorized by surface levels, text colors, interactive states

2. **Dark Mode Best Practices**
   - **Goal**: Research WCAG-compliant dark mode color strategies for educational content
   - **Method**: Review Material Design, Apple HIG, Tailwind dark mode patterns
   - **Output**: Contrast requirements, elevation strategies (borders vs shadows), surface hierarchy

3. **Module Timeline Visualization Patterns**
   - **Goal**: Identify accessible, responsive patterns for displaying week ranges
   - **Method**: Survey educational platforms, progress indicators, Gantt chart libraries
   - **Output**: Recommended pattern: inline horizontal bar with week labels + ARIA roles

4. **Animation & Reduced Motion**
   - **Goal**: Define animation strategy respecting `prefers-reduced-motion`
   - **Method**: Review CSS animation best practices, A11y animation guidelines
   - **Output**: Transform-based animations (GPU-accelerated), duration guidelines, reduced-motion fallbacks

5. **Favicon & Branding Assets**
   - **Goal**: Identify tools/resources for creating course-specific icon assets
   - **Method**: Review Figma/SVG icon libraries, favicon generators
   - **Output**: Asset specs (sizes, formats), design direction (minimalistic robot/AI iconography)

### Research Consolidation

**Output**: `research.md` containing:
- Infima token reference table
- Dark mode elevation strategy decision
- Timeline visualization mockup/description
- Animation timing function specifications
- Branding asset requirements checklist

## Phase 1: Design & Component Architecture

### 1. Design System Definition (`data-model.md`)

#### Color System (Dark-Mode-First)

**Surface Hierarchy** (using Infima tokens):
```css
/* Light Mode */
--surface-background: var(--ifm-background-color);        /* #ffffff */
--surface-primary: var(--ifm-background-surface-color);   /* #f5f5f5 */
--surface-elevated: var(--ifm-card-background-color);     /* #ffffff with shadow */

/* Dark Mode */
--surface-background: var(--ifm-background-color);        /* #18181b */
--surface-primary: var(--ifm-background-surface-color);   /* #27272a */
--surface-elevated: var(--ifm-card-background-color);     /* #3f3f46 */
```

**Module Accent Colors** (derived from `--ifm-color-primary` variants):
```css
--module-1-accent: var(--ifm-color-primary);              /* ROS 2 - Green */
--module-2-accent: var(--ifm-color-info);                 /* Digital Twin - Blue */
--module-3-accent: var(--ifm-color-warning);              /* Isaac - Orange */
--module-4-accent: var(--ifm-color-secondary);            /* VLA - Purple */
```

**Text Colors** (WCAG AA compliant):
```css
--text-primary: var(--ifm-font-color-base);               /* 4.5:1 contrast minimum */
--text-secondary: var(--ifm-color-secondary-darkest);     /* Light mode */
--text-secondary-dark: var(--ifm-color-secondary-lighter); /* Dark mode */
```

#### Typography System

**Font Stack**:
```css
--font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
--font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
```

**Heading Scale** (modular scale 1.25):
```css
--font-size-h1: 2.5rem;    /* 40px - Hero title */
--font-size-h2: 2rem;      /* 32px - Section headers */
--font-size-h3: 1.5rem;    /* 24px - Module card titles */
--font-size-body: 1rem;    /* 16px - Base */
--font-size-small: 0.875rem; /* 14px - Meta text */
```

**Line Heights**:
```css
--line-height-tight: 1.2;   /* Headings */
--line-height-normal: 1.65; /* Body text */
--line-height-loose: 1.8;   /* Long-form content */
```

#### Spacing Scale (8px base unit)

```css
--spacing-xs: 0.5rem;   /* 8px */
--spacing-sm: 1rem;     /* 16px */
--spacing-md: 1.5rem;   /* 24px */
--spacing-lg: 2rem;     /* 32px */
--spacing-xl: 3rem;     /* 48px */
--spacing-2xl: 4rem;    /* 64px */
```

#### Border Radius

```css
--radius-sm: 4px;    /* Buttons, inputs */
--radius-md: 8px;    /* Cards */
--radius-lg: 12px;   /* Hero section */
```

### 2. Component Specifications

#### Component 1: HeroSection

**Purpose**: Display course title, tagline, description with gradient background

**Props Interface**:
```typescript
interface HeroSectionProps {
  title: string;          // "Physical AI & Humanoid Robotics"
  tagline: string;        // "AI Systems in the Physical World..."
  description: string;    // 2-3 sentence course scope
}
```

**Visual Spec**:
- Background: Linear gradient using `--ifm-color-primary` variants
- Text: Centered, white in both modes
- Padding: `--spacing-2xl` vertical, responsive on mobile
- Max-width: 700px for description

**Accessibility**:
- Semantic `<header>` with `role="banner"`
- `<h1>` for title (proper heading hierarchy)
- Sufficient contrast for white text on gradient (verify 4.5:1)

---

#### Component 2: ModuleCard

**Purpose**: Clickable card displaying module info + timeline

**Props Interface**:
```typescript
interface ModuleCardProps {
  moduleNumber: 1 | 2 | 3 | 4;
  title: string;               // e.g., "The Robotic Nervous System"
  subtitle: string;            // e.g., "ROS 2"
  description: string;         // 30-60 words
  weekStart: number;           // 1-13
  weekEnd: number;             // 1-13
  link: string;                // e.g., "/docs/ros2-nervous-system/intro"
  accentColor: string;         // CSS variable name
}
```

**Visual Spec**:
- Layout: Vertical stack (number → title → subtitle → description → timeline)
- Border: Left border (4px) using `accentColor`
- Background: `--surface-elevated` with hover shadow
- Padding: `--spacing-md`
- Border-radius: `--radius-md`
- Description: Clamp to 3 lines with ellipsis (`line-clamp: 3`)

**States**:
- Default: Border + subtle shadow
- Hover: `translateY(-4px)` + increased shadow (200ms ease-out)
- Focus: 2px outline using `--ifm-color-primary` + offset 2px

**Accessibility**:
- Entire card is `<a>` tag (not div with onClick)
- `aria-label`: "{title} - Weeks {weekStart} to {weekEnd}"
- Keyboard focusable with visible focus ring

---

#### Component 3: TimelineBar

**Purpose**: Visual bar showing week range within 13-week course

**Props Interface**:
```typescript
interface TimelineBarProps {
  weekStart: number;       // 1-13
  weekEnd: number;         // 1-13
  totalWeeks: 13;          // Fixed
  accentColor: string;     // CSS variable name
  label?: string;          // Optional, e.g., "Weeks 1-3"
}
```

**Visual Spec**:
- Container: Full-width horizontal bar (height: 8px)
- Background: `--ifm-color-emphasis-200` (neutral gray)
- Fill: Colored segment from `weekStart` to `weekEnd` using `accentColor`
- Label: Small text (`--font-size-small`) above or below bar

**Calculation**:
```typescript
const startPercent = ((weekStart - 1) / totalWeeks) * 100;
const widthPercent = ((weekEnd - weekStart + 1) / totalWeeks) * 100;
```

**Accessibility**:
- `role="progressbar"`
- `aria-valuenow={weekEnd}`
- `aria-valuemin="1"`
- `aria-valuemax="13"`
- `aria-label="Module spans weeks {weekStart} to {weekEnd}"`
- Visual label text for non-screen-reader users

---

### 3. Dark Mode Component Fixes

#### Quiz Containers

**Problem**: Hard-coded white backgrounds in dark mode
**Solution**:
```css
/* dark-mode-fixes.css */
[data-theme='dark'] .quiz-container,
[data-theme='dark'] .exercise-block {
  background-color: var(--ifm-background-surface-color);
  border: 1px solid var(--ifm-color-emphasis-300);
  color: var(--ifm-font-color-base);
}
```

#### Callouts / Admonitions

**Problem**: Low contrast borders/backgrounds
**Solution**:
```css
[data-theme='dark'] .admonition {
  background-color: var(--ifm-background-surface-color);
  border-left: 4px solid var(--ifm-color-primary);
}

[data-theme='dark'] .admonition-heading {
  color: var(--ifm-font-color-base);
}
```

#### Interactive Components (Buttons, Inputs in Quizzes)

**Problem**: Invisible borders in dark mode
**Solution**:
```css
[data-theme='dark'] .quiz-input,
[data-theme='dark'] .quiz-button {
  border: 1px solid var(--ifm-color-emphasis-400);
  background-color: var(--ifm-background-color);
  color: var(--ifm-font-color-base);
}

[data-theme='dark'] .quiz-button:hover {
  background-color: var(--ifm-background-surface-color);
}
```

### 4. API Contracts (`contracts/`)

#### Module Data Contract (`contracts/module-data.json`)

```json
{
  "modules": [
    {
      "id": 1,
      "title": "The Robotic Nervous System",
      "subtitle": "ROS 2",
      "description": "Master the communication infrastructure for humanoid robots with nodes, topics, services, and actions.",
      "weekStart": 1,
      "weekEnd": 3,
      "link": "/docs/ros2-nervous-system/intro",
      "accentColor": "--module-1-accent"
    },
    {
      "id": 2,
      "title": "The Digital Twin",
      "subtitle": "Gazebo & Unity",
      "description": "Build high-fidelity simulation environments for testing robot behaviors before real-world deployment.",
      "weekStart": 4,
      "weekEnd": 6,
      "link": "/docs/digital-twin/intro",
      "accentColor": "--module-2-accent"
    },
    {
      "id": 3,
      "title": "The AI-Robot Brain",
      "subtitle": "NVIDIA Isaac",
      "description": "Implement perception, navigation, and edge inference using NVIDIA Isaac ROS and Jetson platforms.",
      "weekStart": 7,
      "weekEnd": 10,
      "link": "/docs/ai-robot-brain/intro",
      "accentColor": "--module-3-accent"
    },
    {
      "id": 4,
      "title": "Vision-Language-Action",
      "subtitle": "VLA",
      "description": "Integrate voice commands, LLM reasoning, and robotic actions for natural human-robot interaction.",
      "weekStart": 11,
      "weekEnd": 13,
      "link": "/docs/vla/intro",
      "accentColor": "--module-4-accent"
    }
  ]
}
```

#### CSS Variable Schema (`contracts/design-tokens.json`)

```json
{
  "surfaces": {
    "--surface-background": "var(--ifm-background-color)",
    "--surface-primary": "var(--ifm-background-surface-color)",
    "--surface-elevated": "var(--ifm-card-background-color)"
  },
  "moduleAccents": {
    "--module-1-accent": "var(--ifm-color-primary)",
    "--module-2-accent": "var(--ifm-color-info)",
    "--module-3-accent": "var(--ifm-color-warning)",
    "--module-4-accent": "var(--ifm-color-secondary)"
  },
  "typography": {
    "--font-primary": "...",
    "--font-size-h1": "2.5rem",
    "..."
  },
  "spacing": {
    "--spacing-xs": "0.5rem",
    "..."
  }
}
```

### 5. Quickstart Guide (`quickstart.md`)

**Contents**:
1. **Local Development Setup**
   - Clone repo, install dependencies (`npm install`)
   - Run dev server (`npm start`)
   - Navigate to `http://localhost:3000`

2. **Component Development Workflow**
   - Create component in `frontend/src/components/`
   - Import into `index.tsx`
   - Use CSS modules for scoped styles
   - Test in both light and dark modes

3. **Design Token Usage**
   - Reference `custom.css` for available tokens
   - Use `var(--token-name)` in styles
   - Never hard-code colors (always use theme tokens)

4. **Dark Mode Testing**
   - Toggle theme in browser
   - Verify contrast with DevTools Color Picker
   - Test with screen reader (VoiceOver, NVDA)

## Phase 2: Implementation Roadmap

### Step 1: Design System Foundation (Priority: P0)

**Goal**: Establish CSS variable system and typography

**Tasks**:
1. Extend `frontend/src/css/custom.css` with design tokens
2. Define module accent colors
3. Test tokens in light/dark modes
4. Document token usage in comments

**Validation**:
- All tokens render correctly in both themes
- No hard-coded colors remain in base styles

---

### Step 2: Frontpage Components (Priority: P1)

**Goal**: Build HeroSection, ModuleCard, TimelineBar components

**Tasks**:
1. Create `HeroSection` component
2. Create `ModuleCard` component with props interface
3. Create `TimelineBar` component with accessible markup
4. Implement hover/focus animations (200ms, 2-4px translateY)
5. Add `prefers-reduced-motion` media query for animation fallbacks

**Validation**:
- Components render with correct props
- Animations work smoothly (no jank)
- Keyboard navigation functions correctly
- Screen reader announces module info accurately

---

### Step 3: Frontpage Integration (Priority: P1)

**Goal**: Replace default index.tsx with custom frontpage

**Tasks**:
1. Remove existing `HomepageFeatures` component references
2. Import module data from `contracts/module-data.json` (or inline)
3. Render `HeroSection` + grid of 4 `ModuleCard` components
4. Implement responsive grid (2x2 desktop, 1-col mobile)
5. Add module accent left borders

**Validation**:
- Frontpage loads in <3s on 3G
- All 4 modules display correctly
- Grid adapts to mobile viewport
- Links navigate to correct module intro pages

---

### Step 4: Dark Mode Fixes (Priority: P2)

**Goal**: Fix quiz/exercise/callout dark mode rendering

**Tasks**:
1. Create `frontend/src/css/dark-mode-fixes.css`
2. Add CSS overrides for `.quiz-container`, `.exercise-block`, `.admonition`
3. Import in `docusaurus.config.ts` custom CSS array
4. Test all interactive components in dark mode

**Validation**:
- No white backgrounds in dark mode
- All text meets WCAG AA contrast (4.5:1)
- Borders/outlines visible on inputs/buttons
- Callouts readable with sufficient background contrast

---

### Step 5: Branding Updates (Priority: P2)

**Goal**: Replace Docusaurus default branding with course identity

**Tasks**:
1. Design/source favicon (robot/AI icon, minimalistic)
2. Replace `frontend/static/img/favicon.ico`
3. Replace logo in navbar (update `docusaurus.config.ts`)
4. Update footer links (remove Docusaurus defaults)
5. Update metadata (title, description, OpenGraph tags)

**Validation**:
- Favicon displays in browser tab
- Navbar shows course name/logo
- Footer contains only relevant links (GitHub, resources)
- Metadata appears correctly in link previews

---

### Step 6: Responsive & Accessibility Audit (Priority: P3)

**Goal**: Ensure mobile experience and accessibility compliance

**Tasks**:
1. Test on mobile devices (iOS Safari, Chrome Android)
2. Verify 320px minimum viewport support
3. Run Lighthouse audit (target: 90+ Accessibility, 90+ Performance)
4. Run axe DevTools for WCAG violations
5. Test keyboard-only navigation
6. Verify color contrast in dark mode (WebAIM Contrast Checker)

**Validation**:
- All interactive elements have 44x44px touch targets
- No horizontal scrolling on mobile
- Lighthouse scores meet targets
- No axe violations
- Keyboard navigation complete without mouse
- All text passes WCAG AA contrast

---

### Step 7: Progressive Enhancement (Priority: P3)

**Goal**: Ensure site works without JavaScript

**Tasks**:
1. Verify `<a>` tags work without JS (no onClick handlers)
2. Test frontpage with JS disabled
3. Ensure static content (hero, cards) renders
4. Add `<noscript>` fallback message if needed

**Validation**:
- Hero and module cards visible with JS off
- Links navigate correctly without JS
- No broken functionality for core navigation

---

## Implementation Strategy

### Style Organization

```text
frontend/src/css/
├── custom.css              # Design tokens + global overrides
├── readability.css         # Existing (no changes)
├── diagrams.css            # Existing (no changes)
├── dark-mode-fixes.css     # NEW: Quiz/exercise dark mode
└── module-accents.css      # NEW: Per-module color accents
```

**Import Order** (in `docusaurus.config.ts`):
1. `custom.css` (tokens first)
2. `readability.css`
3. `diagrams.css`
4. `dark-mode-fixes.css` (overrides last)

### Component Ownership

| Component | Owner | Type |
|-----------|-------|------|
| HeroSection | Frontpage | Custom React component |
| ModuleCard | Frontpage | Reusable component |
| TimelineBar | Frontpage | Reusable component |
| Quiz containers | Content | CSS-only fixes |
| Exercise blocks | Content | CSS-only fixes |
| Callouts | Content | CSS-only fixes |

### Progressive Enhancement Strategy

**Core Functionality (No JS)**:
- Hero section (static HTML)
- Module cards (anchor links)
- Navigation links

**Enhanced Functionality (With JS)**:
- Hover animations (CSS only, JS not required)
- Theme toggle (Docusaurus built-in)
- Smooth scrolling (CSS `scroll-behavior: smooth`)

**Graceful Degradation**:
- Animations disabled with `prefers-reduced-motion`
- Cards remain functional clickable links even if React fails

### Rollout Order (Minimize Regressions)

1. ✅ **Design tokens** → Non-breaking (extends existing CSS)
2. ✅ **New components** → Non-breaking (isolated in `/components/`)
3. ✅ **Frontpage update** → Localized (only affects `/`)
4. ✅ **Dark mode fixes** → Risk: May affect existing pages
   - Mitigation: Test thoroughly, use specific selectors, isolate in separate CSS file
5. ✅ **Branding updates** → Low risk (asset replacement)

### Testing & Validation Gates

**Per-Step Gates**:
- Visual regression (manual screenshot comparison)
- Lighthouse audit (Performance 90+, Accessibility 90+)
- Contrast validation (WebAIM tool)
- Keyboard navigation test
- Screen reader test (VoiceOver or NVDA)

**Final Acceptance**:
- All 35 functional requirements pass (FR-001 to FR-035)
- All 10 success criteria met (SC-001 to SC-010)
- No WCAG AA violations
- Lighthouse scores ≥90
- No console errors
- No layout shift (CLS < 0.1)

---

## Dependencies & Risks

### External Dependencies

| Dependency | Version | Purpose | Risk |
|------------|---------|---------|------|
| Docusaurus | 3.9.x | Static site framework | Low (stable API) |
| React | 18.x | Component library | Low (peer dep of Docusaurus) |
| Infima | 1.x | CSS framework | Low (bundled with Docusaurus) |

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Dark mode CSS conflicts with existing styles | Medium | Medium | Isolate fixes in separate CSS file; use specific selectors |
| Module accent colors fail WCAG in dark mode | High | Low | Pre-validate all accent colors with contrast checker |
| Animations cause performance issues on mobile | Medium | Low | Use GPU-accelerated transforms; respect `prefers-reduced-motion` |
| JS bundle size increases | Low | Low | CSS-first approach; no heavy animation libraries |
| Existing quiz/exercise components break | High | Low | Test exhaustively; visual-only fixes (no DOM changes) |

### Mitigation Strategies

1. **Dark Mode Conflicts**: Use `[data-theme='dark']` attribute selector + specific class names to avoid cascading issues
2. **Contrast Validation**: Run WebAIM Contrast Checker on all accent colors before implementation
3. **Performance**: Lighthouse CI in GitHub Actions to catch regressions
4. **Bundle Size**: Audit with `npm run build` + analyze output; reject PRs that exceed size budget
5. **Component Breakage**: Manual QA of all quiz/exercise pages; screenshot comparison

---

## Success Metrics

### Functional Completeness (35/35 FRs)

- FR-001 to FR-030: Frontpage, branding, design system
- FR-031 to FR-035: Dark mode fixes for internal content

### Performance Targets

- **Initial Load**: <3s on 3G (target: 2.5s)
- **Lighthouse Performance**: ≥90 (target: 95)
- **Lighthouse Accessibility**: ≥90 (target: 100)
- **CLS**: <0.1 (Cumulative Layout Shift)

### Accessibility Compliance

- **WCAG Level**: AA minimum (4.5:1 contrast for body text)
- **Keyboard Navigation**: All interactive elements focusable
- **Screen Reader**: All components properly announced
- **Focus Visibility**: 2px outlines with offset

### User Experience

- **First Visit**: Course purpose identified in <5 seconds (SC-001)
- **Navigation**: Any module reachable in ≤2 clicks (SC-002)
- **Mobile**: No horizontal scroll on ≥320px viewports (SC-006)
- **Dark Mode**: All components legible with sufficient contrast (SC-010)

---

## Next Steps

**After `/sp.plan` completion**:
1. Review `research.md`, `data-model.md`, `quickstart.md`, `contracts/`
2. Run `/sp.tasks` to decompose Phase 2 roadmap into atomic tasks
3. Implement tasks in priority order (P0 → P1 → P2 → P3)
4. Create PR with frontpage redesign + dark mode fixes
5. Run Lighthouse CI and accessibility audits
6. Merge after passing all validation gates

**Estimated Timeline**: ~5-7 days (assuming 1 developer)
- Phase 0 Research: 0.5 day
- Phase 1 Design: 1 day
- Phase 2 Implementation: 3-5 days (includes testing)

---

## Appendix: Design System Visual Reference

### Color Palette (Light Mode)

```
Background:  #ffffff  (--ifm-background-color)
Surface:     #f5f5f5  (--ifm-background-surface-color)
Primary:     #2e8555  (--ifm-color-primary) [Green]
Info:        #0288d1  (--ifm-color-info) [Blue]
Warning:     #ff9800  (--ifm-color-warning) [Orange]
Secondary:   #6c757d  (--ifm-color-secondary) [Gray]
Text:        #1c1e21  (--ifm-font-color-base)
```

### Color Palette (Dark Mode)

```
Background:  #18181b  (--ifm-background-color)
Surface:     #27272a  (--ifm-background-surface-color)
Primary:     #25c2a0  (--ifm-color-primary) [Teal]
Info:        #64b5f6  (--ifm-color-info) [Light Blue]
Warning:     #ffb74d  (--ifm-color-warning) [Light Orange]
Secondary:   #adb5bd  (--ifm-color-secondary) [Light Gray]
Text:        #e4e4e7  (--ifm-font-color-base)
```

### Typography Scale

```
H1 (Hero):   40px / 2.5rem  (line-height: 1.2)
H2 (Section): 32px / 2rem   (line-height: 1.2)
H3 (Card):   24px / 1.5rem  (line-height: 1.2)
Body:        16px / 1rem    (line-height: 1.65)
Small:       14px / 0.875rem (line-height: 1.65)
```

### Spacing Scale

```
XS:  8px  / 0.5rem
SM:  16px / 1rem
MD:  24px / 1.5rem
LG:  32px / 2rem
XL:  48px / 3rem
2XL: 64px / 4rem
```

---

## References

- [Docusaurus v3 Documentation](https://docusaurus.io/docs)
- [Infima CSS Framework](https://infima.dev/)
- [WCAG 2.1 Level AA](https://www.w3.org/WAI/WCAG21/quickref/?versions=2.1&levels=aa)
- [Material Design Dark Theme](https://m3.material.io/styles/color/dark-mode/overview)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
