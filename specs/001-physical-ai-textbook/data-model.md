# Data Model: Physical AI & Humanoid Robotics Textbook Blueprint

## Entity: Module
- **id**: string (unique identifier, e.g., "ros2-nervous-system")
- **title**: string (display title, e.g., "The Robotic Nervous System (ROS 2)")
- **description**: string (brief overview of module focus)
- **learning_outcomes**: array of strings (3-5 measurable outcomes)
- **software_stack**: array of strings (recommended tools and versions)
- **hardware_recommendations**: array of strings (primary hardware components)
- **hardware_alternatives**: array of strings (budget-conscious alternatives)
- **prerequisites**: array of strings (specific knowledge requirements)
- **assessment_recommendations**: array of strings (optional evaluation methods)
- **dependencies**: array of strings (modules that should be completed first)
- **chapters**: array of Chapter entities
- **order**: integer (1-4 for sequence in course)

## Entity: Chapter
- **id**: string (unique identifier within module, e.g., "ros2-nodes")
- **title**: string (display title, e.g., "ROS 2 Nodes, Topics, Services, and Actions")
- **description**: string (brief overview of chapter content)
- **subtopics**: array of strings (2-5 specific subtopics as H2/H3 headings)
- **estimated_duration**: string (e.g., "1 week", "2-3 hours")
- **module_id**: string (foreign key to Module)

## Entity: Subtopic
- **id**: string (unique identifier within chapter)
- **title**: string (H2/H3 heading text)
- **depth_level**: integer (2 for H2, 3 for H3)
- **content_type**: string (e.g., "concept", "procedure", "example", "reference")
- **chapter_id**: string (foreign key to Chapter)

## Entity: Course
- **id**: string (unique identifier for entire course)
- **title**: string ("Physical AI & Humanoid Robotics")
- **subtitle**: string ("AI Systems in the Physical World: Embodied Intelligence")
- **total_weeks**: integer (13 weeks)
- **modules**: array of Module entities
- **target_audience**: string ("Advanced undergraduate or graduate students in AI/robotics")
- **prerequisites_overview**: string ("Python, Linux, basic ML experience")

## Validation Rules
- Module.order must be between 1-4 and unique across all modules
- Module.learning_outcomes must contain 3-5 items
- Module.software_stack must not be empty
- Chapter.subtopics must contain 2-5 items
- Module.hardware_recommendations must include alternatives as specified
- All entities must have non-empty titles
- Module.assessment_recommendations are optional per FR-014
- Module.prerequisites must be specified per FR-015

## Relationships
- Course (1) → (0..4) Module
- Module (1) → (3..6) Chapter
- Chapter (1) → (2..5) Subtopic