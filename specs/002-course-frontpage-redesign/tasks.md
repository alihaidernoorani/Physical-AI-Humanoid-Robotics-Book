# Task Breakdown: Course Frontpage Redesign & UI/UX Improvements

**Branch**: `002-course-frontpage-redesign`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)
**Status**: Ready for implementation
**Total Tasks**: 35

---

## Overview

This feature decomposes the course frontpage redesign into 8 task groups organized by priority. Each group delivers incremental value and is independently testable.

**User Stories**:
1. **US1 (P1)**: First-time Visitor Orientation - Hero section + module cards visible
2. **US2 (P2)**: Module Navigation via Cards - Cards clickable with animations
3. **US3 (P3)**: Dark/Light Mode Toggle - Theme switching without regressions
4. **US4 (P4)**: Mobile Responsive Experience - Layout adapts to all viewports
5. **US5 (P5)**: Course Progress Visualization - Timeline bars show week ranges

**Implementation Strategy**: Build design tokens → Dark mode fixes → Frontpage components → Enhancements → Polish

---

## GROUP 1: Design Tokens & Theme Foundations

**Goal**: Establish CSS variable system with WCAG AA validated tokens

**Acceptance**: Tokens defined, dark mode renders without white backgrounds, contrast validated

### Tasks

- [x] T001 [P] Define design token CSS variables (surface, color, typography, spacing, radius) in `frontend/src/css/custom.css`
- [x] T002 [P] Define module accent colors (--module-1-accent through --module-4-accent) and verify contrast in light/dark modes
- [x] T003 [P] Import design tokens in `frontend/docusaurus.config.ts` customCSS array
- [x] T004 Validate all color contrast ratios against WCAG AA using WebAIM Contrast Checker
- [x] T005 Test token rendering by toggling theme in browser and verify no white backgrounds in dark mode

**Checkpoint**: Design tokens defined, validated, imported. All contrast ratios ≥4.5:1.

---

## GROUP 2: Dark Mode Component Fixes

**Goal**: Fix quiz, exercise, callout dark mode rendering

**Acceptance**: No pure white backgrounds in dark mode, text readable at WCAG AA contrast

### Tasks

- [x] T006 Create `frontend/src/css/dark-mode-fixes.css` with overrides for quiz, exercise, callout components
- [x] T007 [P] Add dark mode styles for quiz containers ([data-theme='dark'] .quiz-container)
- [x] T008 [P] Add dark mode styles for exercise blocks ([data-theme='dark'] .exercise-block)
- [x] T009 [P] Add dark mode styles for callouts/admonitions ([data-theme='dark'] .admonition)
- [x] T010 [P] Add dark mode styles for interactive components ([data-theme='dark'] .quiz-input, .quiz-button)
- [x] T011 Import `dark-mode-fixes.css` in `frontend/docusaurus.config.ts` customCSS array
- [x] T012 Test 3-5 chapter pages with quizzes/exercises in dark mode and verify visibility

**Checkpoint**: All internal content components render correctly in dark mode.

---

## GROUP 3: Frontpage Cleanup & Branding

**Goal**: Remove default Docusaurus content and apply course branding

**Acceptance**: No default branding visible, frontpage reads as custom landing page

### Tasks

- [x] T013 [P] Remove default Docusaurus frontpage content in `frontend/src/pages/index.tsx`
- [x] T014 [P] Source/create course-specific favicon (robot/AI icon) and replace `frontend/static/img/favicon.ico`
- [x] T015 [P] Update navbar branding in `frontend/docusaurus.config.ts` (course name + icon)
- [x] T016 [P] Update footer links in `frontend/docusaurus.config.ts` (remove defaults, add GitHub/resources)
- [x] T017 Update site metadata (title, description, og:image) in `frontend/docusaurus.config.ts`

**Checkpoint**: Docusaurus branding removed, course-specific assets in place.

---

## GROUP 4: Frontpage Layout & Hero Section (US1)

**Goal**: Implement hero section with course title, tagline, description

**Acceptance**: Hero renders in <3s, displays correctly in light/dark modes, fits above fold

### Tasks

- [x] T018 [P] [US1] Create HeroSection component with TypeScript interface in `frontend/src/components/HeroSection/index.tsx`
- [x] T019 [P] [US1] Create HeroSection styles with gradient background in `frontend/src/components/HeroSection/styles.module.css`
- [x] T020 [US1] Implement hero with semantic HTML (header, h1), responsive typography, gradient using theme tokens
- [x] T021 [US1] Ensure hero fits above fold on 1280px+ viewports, scales typography for mobile
- [x] T022 [US1] Integrate HeroSection into `frontend/src/pages/index.tsx` with course content (title, tagline, description)

**Checkpoint (US1 Partial)**: Hero section renders with correct content in both themes.

---

## GROUP 5: Module Cards & Timeline Visualization (US1, US5)

**Goal**: Implement module cards with timeline bars showing week ranges

**Acceptance**: 4 cards display with correct content, timelines show accurate week ranges

### Tasks

- [x] T023 [P] [US1] Create ModuleCard component with TypeScript interface in `frontend/src/components/ModuleCard/index.tsx`
- [x] T024 [P] [US1] Create ModuleCard styles (left border accent, shadow, padding) in `frontend/src/components/ModuleCard/styles.module.css`
- [x] T025 [P] [US5] Create TimelineBar component with TypeScript interface in `frontend/src/components/TimelineBar/index.tsx`
- [x] T026 [P] [US5] Create TimelineBar styles (horizontal bar, colored fill) in `frontend/src/components/TimelineBar/styles.module.css`
- [x] T027 [US1] Implement ModuleCard as anchor tag with module content, description truncation (line-clamp: 3), accent color border
- [x] T028 [US5] Implement TimelineBar with week range calculation, ARIA roles (role="progressbar"), visual label
- [x] T029 [US1] [US5] Add module data array (4 modules with titles, descriptions, week ranges) in `frontend/src/pages/index.tsx`
- [x] T030 [US1] [US5] Render responsive grid of 4 ModuleCard components with TimelineBar in each card
- [x] T031 [US1] [US5] Define grid layout (2x2 desktop, 2x1 tablet, 1x1 mobile) in `frontend/src/pages/index.module.css`

**Checkpoint (US1, US5 Complete)**: Frontpage displays hero + 4 module cards with accurate timelines.

---

## GROUP 6: Module Card Interactions (US2)

**Goal**: Add hover/focus animations and verify navigation

**Acceptance**: Cards animate on hover (<200ms), navigate correctly, keyboard accessible

### Tasks

- [x] T032 [P] [US2] Add hover animation (translateY(-4px), shadow, 200ms) in `frontend/src/components/ModuleCard/styles.module.css`
- [x] T033 [P] [US2] Add focus styles (outline, offset) and prefers-reduced-motion fallback in `styles.module.css`
- [x] T034 [US2] Verify link hrefs point to correct module intros (e.g., /docs/ros2-nervous-system/intro)
- [x] T035 [US2] Test keyboard navigation (Tab, Enter) and verify focus visible on all cards
- [x] T036 [US2] Test screen reader announcements with VoiceOver or NVDA

**Checkpoint (US2 Complete)**: Module cards interactive, navigable, animate smoothly.

---

## GROUP 7: Responsive Behavior (US4)

**Goal**: Ensure layout adapts to mobile viewports with proper touch targets

**Acceptance**: No horizontal scroll on mobile, cards stack correctly, tap targets ≥44px

### Tasks

- [x] T037 [P] [US4] Define responsive breakpoints (mobile <768px, tablet 768-1024px, desktop >1024px) in `frontend/src/pages/index.module.css`
- [x] T038 [P] [US4] Scale hero typography for mobile in `frontend/src/components/HeroSection/styles.module.css`
- [x] T039 [P] [US4] Scale module card typography for mobile in `frontend/src/components/ModuleCard/styles.module.css`
- [x] T040 [US4] Verify minimum touch targets (44x44px) on mobile, adjust min-height if needed
- [x] T041 [US4] Test frontpage at 320px, 768px, 1280px viewports and verify layout correctness

**Checkpoint (US4 Complete)**: Frontpage adapts to all viewports with usable touch targets.

---

## GROUP 8: Accessibility, Performance & Final Validation (US3)

**Goal**: Validate theme switching, accessibility compliance, performance targets

**Acceptance**: Lighthouse Accessibility ≥90, Performance ≥90, CLS <0.1, keyboard navigation works

### Tasks

- [x] T042 [P] [US3] Audit all frontpage components in dark mode and verify theme token usage (no hard-coded colors)
- [x] T043 [P] [US3] Validate all text contrast in dark mode using WebAIM Contrast Checker (≥4.5:1 for body text)
- [x] T044 [US3] Test theme toggle 10+ times and verify no flicker, layout shift, or content flash
- [x] T045 [US3] Test with OS dark mode preference and verify page loads in dark theme by default
- [x] T046 Add visible keyboard focus styles for all interactive elements (if not already present)
- [x] T047 Test keyboard-only navigation through entire frontpage (Tab, Shift+Tab, Enter)
- [x] T048 Run Lighthouse Accessibility audit and verify score ≥90
- [x] T049 Run Lighthouse Performance audit and verify score ≥90
- [x] T050 Measure Cumulative Layout Shift (CLS) and verify <0.1
- [x] T051 Test progressive enhancement (disable JS, verify hero + cards render, links work)
- [x] T052 Run axe DevTools extension and fix any WCAG AA violations
- [x] T053 Test frontpage on Chrome, Firefox, Safari, Edge and verify consistent rendering
- [x] T054 Test frontpage on mobile devices (iOS Safari, Chrome Android) and verify no regressions
- [x] T055 Verify no console errors on any page load (frontpage + 3-5 chapter pages)

**Checkpoint (US3, Final Complete)**: All user stories passing, accessibility/performance validated, no regressions.

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**Target**: User Story 1 (P1) complete
- Hero section rendering
- 4 module cards displaying
- Timeline bars showing week ranges
- Basic navigation working

**Tasks**: T001-T005, T006-T012, T013-T017, T018-T022, T023-T031 (29 tasks)
**Timeline**: ~3-4 days

### Incremental Delivery

| Week | Groups | Deliverable |
|------|--------|-------------|
| 1 | Groups 1-5 | Frontpage with hero + cards, dark mode fixes |
| 1-2 | Groups 6-7 | Interactive cards, responsive layouts |
| 2 | Group 8 | Accessibility validated, production-ready |

### Parallel Execution Opportunities

- **Group 1** (5 tasks): T001-T003 parallel (token categories), T004-T005 sequential
- **Group 2** (7 tasks): T007-T010 parallel (different components), T012 sequential
- **Group 3** (5 tasks): T013-T016 parallel (independent files)
- **Group 4** (5 tasks): T018-T019 parallel (component files), T020-T022 sequential
- **Group 5** (9 tasks): T023-T026 parallel (component files), T027-T031 sequential
- **Group 6** (5 tasks): T032-T033 parallel, T034-T036 sequential
- **Group 7** (5 tasks): T037-T039 parallel, T040-T041 sequential
- **Group 8** (13 tasks): T042-T043, T046 parallel, rest sequential

**Total Parallel Tasks**: 19 of 55 (35%)

### Task Dependencies

```
Group 1 (Tokens) → Group 2 (Dark Mode)
Group 2 → Group 3 (Branding)
Group 3 → Group 4 (Hero) & Group 5 (Cards)
Groups 4 & 5 → Group 6 (Interactions)
Group 6 → Group 7 (Responsive)
Group 7 → Group 8 (Validation)
```

**Critical Path**: Group 1 → Group 2 → Groups 4-5 → Group 8

---

## Task Summary

| Group | Tasks | Parallel | Sequential | User Story |
|-------|-------|----------|------------|------------|
| Group 1: Tokens | T001-T005 (5) | 3 | 2 | Foundational |
| Group 2: Dark Mode | T006-T012 (7) | 4 | 3 | Foundational |
| Group 3: Branding | T013-T017 (5) | 4 | 1 | Foundational |
| Group 4: Hero | T018-T022 (5) | 2 | 3 | US1 (P1) |
| Group 5: Cards | T023-T031 (9) | 4 | 5 | US1 (P1), US5 (P5) |
| Group 6: Interactions | T032-T036 (5) | 2 | 3 | US2 (P2) |
| Group 7: Responsive | T037-T041 (5) | 3 | 2 | US4 (P4) |
| Group 8: Validation | T042-T055 (14) | 3 | 11 | US3 (P3), Final |
| **TOTAL** | **55 tasks** | **25** | **30** | 5 user stories |

---

## Success Criteria

All tasks complete when:
- ✅ All 35 functional requirements (FR-001 to FR-035) met
- ✅ All 10 success criteria (SC-001 to SC-010) verified
- ✅ Lighthouse Performance ≥90, Accessibility ≥90
- ✅ WCAG AA contrast validated (≥4.5:1 for body text)
- ✅ No console errors, CLS <0.1
- ✅ All 5 user stories independently testable and passing
