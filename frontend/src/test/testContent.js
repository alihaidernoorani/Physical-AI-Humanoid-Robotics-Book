// Test content for verifying dual retrieval modes
export const testContent = {
  "fullBookContent": [
    {
      "module": "Module 1",
      "chapter": "Chapter 1",
      "subsection": "1.1 Introduction to Physical AI",
      "page_reference": "p.15",
      "text": "Physical AI represents the convergence of artificial intelligence and physical systems. This field explores how AI can be embodied in physical agents that interact with the real world through sensors and actuators. The foundational principles include perception, decision-making, and action in dynamic environments.",
      "confidence_score": 0.95
    },
    {
      "module": "Module 2",
      "chapter": "Chapter 3",
      "subsection": "3.2 Robot Learning Algorithms",
      "page_reference": "p.45",
      "text": "Robot learning algorithms enable machines to acquire skills through experience. These algorithms include reinforcement learning, imitation learning, and self-supervised learning approaches. The key challenge is to develop algorithms that can learn efficiently in real-world environments with safety guarantees.",
      "confidence_score": 0.92
    },
    {
      "module": "Module 3",
      "chapter": "Chapter 5",
      "subsection": "5.1 Humanoid Robotics Fundamentals",
      "page_reference": "p.80",
      "text": "Humanoid robots are designed to mimic human form and behavior. They typically feature a head, torso, two arms, and two legs. The design challenges include achieving stable bipedal locomotion, dexterous manipulation, and natural human-robot interaction.",
      "confidence_score": 0.89
    }
  ],
  "perPageContent": [
    {
      "module": "Module 1",
      "chapter": "Chapter 1",
      "subsection": "1.1 Introduction to Physical AI",
      "page_reference": "p.15",
      "text": "Physical AI represents the convergence of artificial intelligence and physical systems. This field explores how AI can be embodied in physical agents that interact with the real world through sensors and actuators. The foundational principles include perception, decision-making, and action in dynamic environments.",
      "confidence_score": 0.95
    }
  ],
  "queries": {
    "broadQuery": "What are the main topics covered in the textbook?",
    "specificQuery": "What does the introduction section say about Physical AI?",
    "crossModuleQuery": "How do robot learning algorithms relate to humanoid robotics?",
    "selectedTextQuery": "What is Physical AI according to the text?"
  }
};

// Mock responses for different modes
export const mockResponses = {
  "fullBookMode": {
    "response_text": "The textbook covers several main topics including Physical AI fundamentals, robot learning algorithms, and humanoid robotics. Physical AI represents the convergence of artificial intelligence and physical systems. Robot learning algorithms enable machines to acquire skills through experience. Humanoid robots are designed to mimic human form and behavior.",
    "citations": [
      {
        "module": "Module 1",
        "chapter": "Chapter 1",
        "subsection": "1.1 Introduction to Physical AI",
        "page_reference": "p.15",
        "text": "Physical AI represents the convergence of artificial intelligence and physical systems...",
        "confidence_score": 0.95
      },
      {
        "module": "Module 2",
        "chapter": "Chapter 3",
        "subsection": "3.2 Robot Learning Algorithms",
        "page_reference": "p.45",
        "text": "Robot learning algorithms enable machines to acquire skills through experience...",
        "confidence_score": 0.92
      }
    ],
    "confidence_score": 0.88,
    "is_fallback": false
  },
  "perPageMode": {
    "response_text": "According to the text, Physical AI represents the convergence of artificial intelligence and physical systems. This field explores how AI can be embodied in physical agents that interact with the real world through sensors and actuators. The foundational principles include perception, decision-making, and action in dynamic environments.",
    "citations": [
      {
        "module": "Module 1",
        "chapter": "Chapter 1",
        "subsection": "1.1 Introduction to Physical AI",
        "page_reference": "p.15",
        "text": "Physical AI represents the convergence of artificial intelligence and physical systems...",
        "confidence_score": 0.95
      }
    ],
    "confidence_score": 0.92,
    "is_fallback": false
  }
};