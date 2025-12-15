# Data Model: textbook-mdx-compliance

## Overview
This document describes the data structures and entities relevant to the textbook MDX compliance update. Since this is primarily a content and presentation layer update, the "data model" focuses on content organization and structure.

## Content Entities

### Textbook Chapter
- **Name**: Individual chapter document
- **Type**: `.md` or `.mdx` file
- **Fields**:
  - title: string (chapter title)
  - slug: string (URL-friendly identifier)
  - content: string (chapter content in Markdown/MDX format)
  - frontmatter: object (metadata like description, tags, etc.)
  - module: reference to parent Module
  - requiresInteractiveComponents: boolean (indicates need for .mdx format)

### Module
- **Name**: Course module grouping
- **Type**: Directory with _category_.json
- **Fields**:
  - title: string (module name as per constitution)
  - slug: string (URL-friendly identifier)
  - chapters: array of Chapter references
  - description: string (module description)

### Interactive Component
- **Name**: Reusable interactive elements
- **Type**: React/MDX components
- **Fields**:
  - type: string (toggle, callout, quiz, etc.)
  - props: object (component-specific properties)
  - content: string or JSX (component content)

### Navigation Structure
- **Name**: Sidebar and page navigation
- **Type**: Configuration object
- **Fields**:
  - label: string (display name)
  - type: string (doc, link, category)
  - id: string (reference to document)
  - items: array of child navigation items

## Content Relationships

```
Module (1) -- (Many) Chapter
Chapter (1) -- (0..1) Interactive Component
Navigation Structure (1) -- (Many) Navigation Item
```

## Frontmatter Schema

Each chapter document includes frontmatter with:

```yaml
title: "Chapter Title"
description: "Brief description"
sidebar_label: "Sidebar text"
sidebar_position: number
keywords: [list, of, keywords]
```

## Validation Rules

1. All module names must match exactly: "The Robotic Nervous System (ROS 2)", "The Digital Twin (Gazebo & Unity)", "The AI-Robot Brain (NVIDIA Isaac™)", "Vision-Language-Action (VLA)"
2. Chapter slugs must maintain existing URL structure during MDX conversion
3. Interactive components must be properly encapsulated in MDX format
4. Navigation structure must match file structure in docs/ directory