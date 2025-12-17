import google.generativeai as genai
from typing import List, Dict, Any, Optional
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        # Initialize Gemini client with API key from settings
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        genai.configure(api_key=settings.gemini_api_key)

        # Use the Gemini 2.5-flash model as specified
        self.model_name = "gemini-2.5-flash"
        self.model = genai.GenerativeModel(self.model_name)

    def generate_response(self,
                         prompt: str,
                         context_chunks: Optional[List[Dict[str, Any]]] = None,
                         max_tokens: int = 1000,
                         temperature: float = 0.7) -> str:
        """
        Generate a response using Gemini based on the prompt and context
        """
        try:
            # Build the full prompt with context if provided
            full_prompt = prompt

            if context_chunks:
                context_text = "\n\nContext from textbook:\n"
                for chunk in context_chunks:
                    context_text += f"- Module: {chunk.get('module', 'N/A')}\n"
                    context_text += f"  Chapter: {chunk.get('chapter', 'N/A')}\n"
                    context_text += f"  Content: {chunk.get('content', '')}\n\n"

                full_prompt = f"{context_text}\n\nQuestion: {prompt}\n\nPlease provide a comprehensive answer based on the context above, citing the relevant sources. If the context doesn't contain enough information to answer the question, please state that clearly."

            # Generate content
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature
                )
            )

            # Extract text from response
            if response.text:
                logger.info(f"Generated response using {self.model_name}")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty response")
                return "I couldn't generate a response based on the provided information."

        except Exception as e:
            logger.error(f"Error generating response with Gemini: {str(e)}")
            raise

    def chat_with_context(self,
                         query: str,
                         context_chunks: List[Dict[str, Any]],
                         history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Perform a chat interaction with context and optional history
        """
        try:
            # Create a chat session
            chat = self.model.start_chat()

            # Add conversation history if provided
            if history:
                for message in history:
                    role = "user" if message.get("role") == "user" else "model"
                    chat.history.append(
                        genai.types.ContentDict(
                            parts=[genai.types.PartDict(text=message.get("content", ""))],
                            role=role
                        )
                    )

            # Build context-aware prompt
            context_text = "\n\nReference material from textbook:\n"
            for i, chunk in enumerate(context_chunks):
                context_text += f"{i+1}. Module: {chunk.get('module', 'N/A')}\n"
                context_text += f"   Chapter: {chunk.get('chapter', 'N/A')}\n"
                context_text += f"   Section: {chunk.get('subsection', 'N/A')}\n"
                context_text += f"   Content: {chunk.get('content', '')[:500]}...\n\n"  # Truncate long content

            full_prompt = f"{context_text}\n\nUser Question: {query}\n\nBased on the reference material above, please answer the user's question comprehensively. Cite the relevant modules, chapters, and sections where you found the information. If the reference material doesn't contain enough information to answer the question, please acknowledge that limitation."

            # Get response
            response = chat.send_message(full_prompt)

            if response.text:
                result = {
                    "response_text": response.text.strip(),
                    "model_used": self.model_name,
                    "usage": {
                        "prompt_tokens": len(full_prompt.split()),
                        "response_tokens": len(response.text.split())
                    }
                }
                logger.info(f"Chat response generated using {self.model_name}")
                return result
            else:
                logger.warning("Gemini chat returned empty response")
                return {
                    "response_text": "I couldn't generate a response based on the provided information.",
                    "model_used": self.model_name,
                    "usage": {"prompt_tokens": len(full_prompt.split()), "response_tokens": 0}
                }

        except Exception as e:
            logger.error(f"Error in Gemini chat: {str(e)}")
            raise

    def health_check(self) -> bool:
        """
        Check if Gemini service is accessible by generating a test response
        """
        try:
            test_prompt = "Hello, this is a health check. Please respond with a simple confirmation."
            response = self.generate_response(test_prompt, max_tokens=50, temperature=0.1)
            return bool(response and len(response) > 0)
        except Exception as e:
            logger.error(f"Gemini health check failed: {str(e)}")
            return False

# Create a singleton instance
gemini_service = GeminiService()