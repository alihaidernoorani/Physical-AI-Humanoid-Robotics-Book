# Textbook Content Contract

## Purpose
This contract defines the interface and structure for textbook content generation, ensuring consistency and compliance with project requirements across all chapters.

## Content Structure Contract

### Required Chapter Elements
Each textbook chapter MUST include the following elements in the specified order:

```
1. Frontmatter (preserved from existing files)
2. Learning Objectives (3-5 bullet points)
3. Main Content (conceptual explanations with examples)
4. Key Takeaways (summary with forward references)
5. References (APA 7th edition citations)
```

### Frontmatter Requirements
The following fields MUST be present and preserved in every chapter:

```yaml
---
id: string
title: string
description: string
personalization: true
translation: ur
learning_outcomes: array of strings (3-5 items)
software_stack: array of strings
hardware_recommendations: array of strings
prerequisites: array of strings
---
```

### Content Requirements
Each chapter MUST satisfy these requirements:

#### Learning Objectives
- **Type**: Array of strings
- **Cardinality**: Exactly 3-5 items
- **Content**: Specific, measurable outcomes using action verbs
- **Format**: "- [Action verb] [object] to [purpose]"

#### Main Content
- **Type**: Markdown text
- **Depth**: Graduate-level technical depth with conceptual focus
- **Restrictions**: No code blocks or implementation commands
- **Requirements**: Include concrete examples of ROS 2, Gazebo, Isaac, or VLA usage

#### Key Takeaways
- **Type**: Array of strings (as a bulleted list in Markdown)
- **Cardinality**: At least 3 summary points
- **Requirements**: Include connection to capstone project and forward references to later modules

## Compliance Validation

### Content Validation Rules
1. **Frontmatter Preservation**: All existing frontmatter fields must remain unchanged
2. **No Code Blocks**: Content must not contain any fenced code blocks or inline code examples
3. **Technology Standards**: All hardware/tool references must use 2024-2025 standards
4. **Educational Focus**: Content must focus on conceptual understanding rather than implementation

### Cross-Chapter Consistency
Each chapter MUST:
- Maintain consistent terminology with other chapters in the same module
- Build on concepts introduced in prerequisite chapters
- Provide forward references to concepts in later modules
- Satisfy the capstone project scaffolding requirement

## Quality Assurance Criteria

### Scientific Accuracy
- All technical claims must be verifiable against official documentation
- No hallucinated references or fabricated information
- Citations must follow APA 7th edition format

### Academic Clarity
- Writing level appropriate for undergraduate+ audience
- Advanced terminology defined before use
- Flesch–Kincaid Grade 10–12 reading level

### Reproducibility
- All methods and conceptual frameworks presented with sufficient detail
- Each chapter clearly states assumptions and dependencies
- Mathematical formulations include symbolic definitions

## Module-Specific Requirements

### Module 1: ROS 2 Nervous System
- Focus on real-time control, node architecture, and humanoid URDF
- Emphasize ROS 2 Humble Hawksbill features
- Include examples of node communication patterns

### Module 2: Digital Twin
- Focus on physics simulation, sensor modeling, Gazebo/Unity interoperability
- Emphasize simulation accuracy and sensor fidelity
- Include examples of simulation-to-reality transfer

### Module 3: AI-Robot Brain
- Focus on Isaac Sim synthetic data, hardware-accelerated perception, Nav2 for bipeds
- Emphasize perception and navigation for humanoid robots
- Include examples of AI/ML integration in robotics

### Module 4: VLA
- Focus on voice-to-action, LLM-based task planning, capstone integration
- Emphasize multimodal interaction and task decomposition
- Include examples of LLM integration with ROS 2 systems

## Success Criteria
A chapter is considered complete when:
- [ ] All required elements are present and properly formatted
- [ ] Content meets educational depth requirements
- [ ] All compliance validation checks pass
- [ ] Cross-chapter consistency is maintained
- [ ] Quality assurance criteria are satisfied
- [ ] Capstone project scaffolding is established