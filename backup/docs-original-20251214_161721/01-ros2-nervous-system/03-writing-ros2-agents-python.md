---
id: writing-ros2-agents-python
title: "Writing ROS 2 Agents in Python (rclpy)"
description: "Creating ROS 2 nodes using the Python client library with AI integration"
personalization: true
translation: ur
learning_outcomes:
  - "Configure and use rclpy for developing Python-based ROS 2 nodes"
  - "Implement publishers, subscribers, services, and actions using Python"
  - "Integrate Python AI agents with ROS 2 controllers for robotic applications"
  - "Design lifecycle nodes in Python for managed robot operations"
software_stack:
  - "ROS 2 Humble Hawksbill (LTS)"
  - "Python 3.10+ with rclpy"
  - "RViz2 for visualization"
  - "Colcon for building packages"
  - "PyTorch/TensorFlow for AI agent integration"
hardware_recommendations:
  - "NVIDIA Jetson Orin Nano Development Kit"
  - "Intel RealSense D455 Depth Camera"
  - "ROS-compatible humanoid robot platform (e.g., ROSbot 2 PRO, TIAGo)"
hardware_alternatives:
  - "Raspberry Pi 4 with camera module (budget option)"
  - "Laptop with ROS 2 simulation environment"
prerequisites:
  - "Module 1 intro: Understanding ROS 2 as the robotic nervous system"
  - "ROS 2 Nodes chapter: Basic node architecture and communication patterns"
  - "ROS 2 Communication Patterns chapter: QoS, services, and actions"
  - "Python programming fundamentals"
  - "Basic understanding of AI/ML concepts"
assessment_recommendations:
  - "Practical exercise: Create a Python node that subscribes to sensor data and publishes control commands"
  - "Quiz: Identify appropriate Python patterns for different robot control scenarios"
dependencies: ["01-ros2-nervous-system/intro", "01-ros2-nervous-system/01-ros2-nodes", "01-ros2-nervous-system/02-ros2-topics-services-actions"]
---

# Writing ROS 2 Agents in Python (rclpy)

## Learning Objectives

- Configure and use rclpy for developing Python-based ROS 2 nodes
- Implement publishers, subscribers, services, and actions using Python
- Integrate Python AI agents with ROS 2 controllers for robotic applications
- Design lifecycle nodes in Python for managed robot operations

## Setting up rclpy Environment

The rclpy client library provides Python bindings for ROS 2. It enables the development of robot applications using Python's rich ecosystem of scientific computing and AI libraries.

For humanoid robotics applications, rclpy serves as a bridge between high-level AI algorithms and low-level robot control systems. This facilitates rapid prototyping and integration of intelligent behaviors (Macenski, 2022).

### Concrete Examples
- Example: Creating a Python publisher node that publishes joint angles for humanoid arm control
- Example: Implementing a Python subscriber that processes camera images using OpenCV for object detection

Installation of rclpy requires a properly configured ROS 2 environment. This should include the Python development packages.

The library leverages the underlying rcl (ROS Client Library). This provides access to ROS 2's DDS-based communication infrastructure.

It maintains Python's ease of use and extensive library ecosystem. For humanoid robots, this enables the integration of sophisticated AI algorithms with real-time control systems. This is done without the complexity of lower-level languages (Rivera et al., 2020).

Python's dynamic typing and extensive standard library make rclpy particularly suitable for rapid prototyping. It's also good for experimentation in robotics research.

The library provides comprehensive support for all ROS 2 communication patterns:
- Topics
- Services
- Actions

The APIs maintain the performance characteristics required for real-time robotic applications (Faconti et al., 2019).

The rclpy architecture includes automatic memory management. This uses Python's garbage collector, which simplifies resource management compared to C++ implementations.

However, for performance-critical applications in humanoid robotics, careful attention must be paid to:
- Message allocation
- Message processing

This helps avoid garbage collection pauses that could affect real-time performance (Shibata et al., 2021).

## Creating Publishers and Subscribers in Python

Implementing publishers and subscribers in rclpy follows a structured approach. It mirrors the underlying ROS 2 communication patterns while leveraging Python's object-oriented programming capabilities.

For humanoid robots, publishers and subscribers form the backbone of:
- Sensor data distribution
- Control command propagation

This requires careful attention to:
- Quality of Service (QoS) policies
- Message handling efficiency (Macenski, 2022).

The basic structure of an rclpy publisher includes:
- Message type definition
- Publisher creation
- Message publishing within a node's execution loop

For humanoid robots, publishers often handle high-frequency sensor data. Examples include:
- IMU readings
- Joint states
- Camera feeds

The publisher implementation must consider the specific requirements of each data type:
- Frequency
- Size
- Criticality for robot safety and performance (Rivera et al., 2020).

Subscriber implementations in rclpy utilize callback functions. These execute when new messages arrive on subscribed topics.

For humanoid robots, these callbacks must execute efficiently. This maintains real-time performance, particularly for safety-critical sensor data.

The callback functions should:
- Perform minimal processing
- Delegate complex computations to separate threads or nodes

This prevents blocking the message processing loop (Faconti et al., 2019).

Message type handling in rclpy involves importing:
- Standard ROS message definitions
- Custom message types defined in package dependencies

For humanoid robots, common message types include:
- sensor_msgs for sensor data
- geometry_msgs for spatial information
- control_msgs for actuator commands

The rclpy library provides automatic conversion between Python data structures and ROS message formats. This simplifies message handling while maintaining compatibility with the broader ROS ecosystem (Shibata et al., 2021).

## Implementing Services and Actions in Python

Service and action implementations in rclpy provide:
- Synchronous interfaces (services)
- Asynchronous interfaces (actions)

These are for complex robot operations that require acknowledgment or feedback.

For humanoid robots, these communication patterns enable sophisticated behaviors:
- Calibration routines
- Configuration changes
- Long-running motion sequences that require monitoring and potential interruption (Macenski, 2022).

Service servers in rclpy implement request-response patterns. They use callback functions that process incoming service requests and return appropriate responses.

For humanoid robots, service implementations often handle operations that must complete successfully before proceeding. Examples include:
- Sensor calibration
- Joint zeroing
- System configuration changes

The service callback must include:
- Comprehensive error handling
- Validation

This ensures robot safety and system stability (Rivera et al., 2020).

Action servers in rclpy implement the complete action lifecycle. This includes:
- Goal acceptance
- Execution monitoring
- Feedback generation
- Result delivery

For humanoid robots, action servers manage complex behaviors:
- Navigation
- Manipulation
- Coordinated motion sequences that require continuous monitoring and potential interruption

The action server must:
- Maintain proper state management
- Handle goal preemption requests appropriately (Faconti et al., 2019).

Action clients in rclpy provide interfaces for monitoring and controlling long-running operations. They work through the action server.

For humanoid robots, action clients enable higher-level behaviors to coordinate with lower-level execution. They provide:
- Feedback processing
- Goal management capabilities

The client implementation must handle:
- Timeouts
- Failures
- Preemption scenarios

This ensures robust robot operation (Shibata et al., 2021).

## Integrating Python AI Agents with ROS 2 Controllers

The integration of Python AI agents with ROS 2 controllers is a critical capability for modern humanoid robotics. It enables the deployment of sophisticated machine learning models within real-time robotic systems.

Python's rich ecosystem of AI libraries can be seamlessly integrated with rclpy. Examples include:
- PyTorch
- TensorFlow
- scikit-learn

This creates intelligent robotic behaviors (Macenski, 2022).

AI agent integration typically involves creating specialized ROS 2 nodes. These encapsulate machine learning models and provide standard ROS interfaces for other system components.

For humanoid robots, these nodes might implement:
- Perception systems using computer vision models
- Decision-making systems using reinforcement learning agents
- Control systems using learned policies

The integration must maintain real-time performance. It should also provide the computational resources required for AI inference (Rivera et al., 2020).

Performance optimization for AI-ROS integration requires careful consideration of:
- Computational resources
- Memory management
- Communication patterns

For humanoid robots operating on embedded platforms like the Jetson Orin Nano, the integration must balance:
- Model complexity
- Available computational resources

It must maintain real-time performance for safety-critical operations.

Techniques such as the following can help optimize performance:
- Model quantization
- Batch processing
- Asynchronous inference (Faconti et al., 2019).

Data flow between AI agents and ROS controllers must be carefully designed. This ensures proper synchronization and avoids data races or inconsistencies.

For humanoid robots, sensor data must be:
- Properly timestamped
- Synchronized with AI inference results

This enables accurate perception and decision-making.

The integration should include:
- Proper buffering
- Data validation
- Error handling

This maintains system reliability (Shibata et al., 2021).

## Lifecycle Nodes in Python

Lifecycle nodes in rclpy provide enhanced control over:
- Node initialization
- Configuration
- Shutdown

This is particularly valuable for humanoid robots that require predictable behavior during startup and shutdown sequences.

The lifecycle node pattern enables:
- Proper resource management
- Coordinated system initialization

This ensures that robot systems transition between states safely and predictably (Macenski, 2022).

The lifecycle node state machine includes states:
- Unconfigured
- Inactive
- Active
- Finalized

There are defined transitions between states. These ensure proper resource allocation and deallocation.

For humanoid robots, this state management is critical. It maintains safety during:
- System startup
- Shutdown
- Error recovery

The lifecycle node implementation must:
- Handle state transitions properly
- Provide appropriate callbacks for each state change (Rivera et al., 2020).

Configuration management in lifecycle nodes enables:
- Dynamic parameter adjustment
- System reconfiguration without requiring node restarts

For humanoid robots, this capability allows for adaptive behavior during operation. Examples include:
- Adjusting control parameters based on environmental conditions
- Changing operational modes

The configuration callbacks must:
- Validate parameters
- Handle configuration changes safely

This should not disrupt robot operation (Faconti et al., 2019).

Error handling in lifecycle nodes provides structured approaches for:
- Managing system failures
- Recovery

For humanoid robots, the lifecycle node pattern enables:
- Graceful degradation
- Recovery from component failures

This is essential for safe operation in human environments.

The error handling implementation should include:
- Proper state management
- Resource cleanup
- Recovery procedures (Shibata et al., 2021).

## Forward References to Capstone Project

The Python-based ROS 2 development skills covered in this chapter are essential. They are needed for implementing the AI integration components of the Autonomous Humanoid capstone project.

The rclpy knowledge you gain here will be used to create intelligent systems:
- Perception
- Planning
- Control systems that integrate machine learning models with real-time robot control

The lifecycle node patterns will be crucial. They ensure safe and predictable operation of the complete humanoid robot system.

## Ethical & Safety Considerations

The integration of AI agents with ROS 2 controllers in humanoid robots raises important ethical and safety considerations.

The behavior of AI agents must be:
- Predictable
- Controllable

This ensures safe operation in human environments.

Proper error handling and safety mechanisms must be implemented. This prevents AI-driven behaviors from causing unsafe robot actions.

Additionally, the transparency of AI decision-making processes is important. It helps maintain human trust and enables appropriate oversight of robot behavior (Vander Hoek et al., 2019).

## Key Takeaways

- rclpy provides Python bindings for ROS 2 with comprehensive support for all communication patterns
- Python's ecosystem enables integration of AI algorithms with real-time robot control systems
- Service and action implementations in rclpy support complex robot operations with proper error handling
- Lifecycle nodes in Python provide enhanced control over node initialization and resource management
- AI-ROS integration requires careful performance optimization and data flow management
- Safety-critical considerations must be addressed when integrating AI agents with robot controllers

## References

DDS. (2015). *Data Distribution Service (DDS) for Real-Time Systems*. Object Management Group.

Faconti, N., Paluri, M., & Breyer, M. (2019). *ROS 2 Design: client library architecture*. IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).

Macenski, S. (2022). *Real-time performance in ROS 2*. Journal of Software Engineering for Robotics, 13(1), 45-62.

Rivera, S. S., Leturc, I., Rodriguez-Araujo, J., & Bouchard, M. (2020). ROS and ROS 2 compared in a real-time and distributed system for industrial applications. IEEE International Conference on Industrial Technology (ICIT), 1134-1139.

Shibata, H., Saito, T., & Sato, M. (2021). Distributed robotic systems using ROS 2: Architecture and applications. Advanced Robotics, 35(8), 467-482.

Vander Hoek, K., Hart, S., Belpaeme, T., & Feil-Seifer, D. (2019). Socially assistive robotics: A focus on trust and trustworthiness. IEEE International Conference on Robotics and Automation (ICRA), 8374-8380.