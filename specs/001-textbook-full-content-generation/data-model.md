# Data Model: Textbook Content Structure

## Entities

### Textbook Chapter
**Description**: Educational content unit containing learning objectives, conceptual explanations, examples, and key takeaways

**Attributes**:
- `id`: String - Unique identifier matching file name (e.g., "ros2-nodes", "gazebo-simulation")
- `title`: String - Human-readable title displayed in navigation and page
- `module`: String - Parent module identifier (e.g., "ros2-nervous-system", "digital-twin")
- `position`: Integer - Sequential position within module
- `learning_objectives`: Array[String] - 3-5 specific, measurable outcomes for the chapter
- `content`: String - Main educational content with conceptual explanations
- `examples`: Array[String] - Concrete examples of technology usage (ROS 2, Gazebo, Isaac, VLA)
- `key_takeaways`: Array[String] - Summary points of key concepts
- `forward_references`: Array[String] - Links to future modules/chapters
- `frontmatter`: Object - Metadata including `personalization: true`, `translation: ur`

**Validation Rules**:
- `id` must match the corresponding file name in the docs/ directory
- `learning_objectives` must contain exactly 3-5 items
- `content` must not contain code blocks or implementation commands
- `frontmatter.personalization` must equal `true`
- `frontmatter.translation` must equal `ur`

### Module
**Description**: Collection of related chapters forming a cohesive learning unit

**Attributes**:
- `id`: String - Module identifier (e.g., "01-ros2-nervous-system", "02-digital-twin")
- `title`: String - Module title
- `chapters`: Array[Chapter] - Ordered list of chapters in the module
- `intro_chapter`: Chapter - The introductory chapter for the module

**Relationships**:
- One Module contains many Chapters (1 to many)
- Each Chapter belongs to exactly one Module (many to 1)

### Learning Objective
**Description**: Specific, measurable outcome that students should achieve after reading a chapter

**Attributes**:
- `text`: String - The objective statement
- `measurable`: Boolean - Whether the objective can be assessed
- `relevance`: String - Connection to capstone project or later modules

### Frontmatter
**Description**: Metadata at the beginning of each chapter file containing configuration settings

**Attributes**:
- `id`: String - Document ID used by Docusaurus
- `title`: String - Page title
- `description`: String - SEO description
- `personalization`: Boolean - Whether personalization is enabled
- `translation`: String - Translation language code (e.g., "ur" for Urdu)
- `learning_outcomes`: Array[String] - Learning objectives for the chapter
- `software_stack`: Array[String] - Technology stack used in the chapter
- `hardware_recommendations`: Array[String] - Recommended hardware for the chapter
- `prerequisites`: Array[String] - Prerequisites for understanding the chapter

## State Transitions

### Chapter Lifecycle
1. **Empty** - File exists but contains only frontmatter
2. **Draft** - Content is being written with basic structure
3. **Reviewed** - Content has been reviewed for accuracy and consistency
4. **Complete** - Content is final and meets all specification requirements

## Constraints

### Content Constraints
- All content must maintain GitHub Pages-compatible Markdown format
- No code blocks or implementation commands (except when explicitly allowed by constitution)
- All hardware/tool references must use 2024-2025 standards (Jetson Orin Nano, Isaac Sim 2024+, etc.)
- Frontmatter must be preserved and not modified during content generation

### Structural Constraints
- File names and directory structure must remain unchanged
- Each module must have exactly one intro.md file
- Learning objectives must be 3-5 bullet points at the beginning of each chapter
- Key takeaways must be at the end of each chapter
- Forward references to capstone project and later modules must be included