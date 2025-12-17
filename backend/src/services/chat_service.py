from typing import List, Dict, Optional
from datetime import datetime
import uuid
import openai
from src.config.settings import settings
from src.services.embedding_service import EmbeddingService
from src.services.retrieval_service import RetrievalService
from src.models.chat_session import ChatMode, UserQuery, GeneratedResponse, RetrievedContext
from src.utils.text_chunker import TextChunk


class ChatService:
    """
    Main service for handling chat interactions with RAG capabilities.
    """

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.retrieval_service = RetrievalService()
        # Use the Google API key (which is the Gemini API key) with the OpenAI client
        self.client = openai.OpenAI(api_key=settings.google_api_key)

    def process_query(self, query_text: str, session_id: str, mode: ChatMode, selected_text: Optional[str] = None) -> GeneratedResponse:
        """
        Process a user query and generate a response based on retrieved context.
        """
        query_id = str(uuid.uuid4())
        timestamp = datetime.now()

        # Create user query object
        user_query = UserQuery(
            id=query_id,
            session_id=session_id,
            query_text=query_text,
            selected_text=selected_text,
            query_mode=mode,
            timestamp=timestamp
        )

        # Retrieve relevant context based on mode
        retrieved_contexts = []
        if mode == ChatMode.full_text:
            # Retrieve from full textbook content
            retrieved_contexts = self.retrieval_service.search_by_text(query_text, self.embedding_service, top_k=5)
        elif mode == ChatMode.selected_text and selected_text:
            # Use only the selected text as context
            retrieved_contexts = [{
                "id": f"selected_text_{query_id}",
                "content": selected_text,
                "module_name": "Selected Text",
                "chapter_title": "User Selection",
                "section_path": "user/selection",
                "token_count": self._estimate_tokens(selected_text),
                "similarity_score": 1.0
            }]

        # Generate response using OpenAI
        response_text = self._generate_response(query_text, retrieved_contexts)

        # Create citations from retrieved contexts
        citations = [ctx["section_path"] for ctx in retrieved_contexts if "section_path" in ctx]

        # Estimate grounding confidence based on context relevance
        grounding_confidence = self._calculate_confidence(retrieved_contexts)

        # Create and return the response
        return GeneratedResponse(
            id=str(uuid.uuid4()),
            session_id=session_id,
            query_id=query_id,
            response_text=response_text,
            citations=citations,
            grounding_confidence=grounding_confidence,
            generated_at=timestamp,
            response_metadata={
                "context_count": len(retrieved_contexts),
                "mode": mode
            }
        )

    def _generate_response(self, query: str, contexts: List[Dict]) -> str:
        """
        Generate a response using OpenAI-compatible interface with Gemini based on the query and retrieved contexts.
        """
        if not contexts:
            return "I couldn't find any relevant information in the textbook to answer your question. Please try rephrasing your question or check if the topic is covered in the textbook."

        # Format the context for the LLM
        context_text = "\n\n".join([f"Source: {ctx.get('section_path', 'Unknown')} - {ctx['content']}" for ctx in contexts])

        # Create the prompt for the model
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Answer the user's question based only on the provided context from the textbook. Do not make up information or hallucinate. If the context doesn't contain enough information to answer the question, say so explicitly.

        Context:
        {context_text}

        Question: {query}

        Answer (be concise, accurate, and cite sources when possible):
        """

        try:
            response = self.client.chat.completions.create(
                model="gemini-2.5-flash",  # Using Gemini model through OpenAI-compatible interface
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error while processing your request. Please try again."

    def _calculate_confidence(self, contexts: List[Dict]) -> float:
        """
        Calculate grounding confidence based on context relevance scores.
        """
        if not contexts:
            return 0.0

        # Average the similarity scores as a basic confidence measure
        scores = [ctx.get("similarity_score", 0.0) for ctx in contexts]
        avg_score = sum(scores) / len(scores) if scores else 0.0

        # Ensure confidence is between 0 and 1
        return min(1.0, max(0.0, avg_score))

    def _estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in a text string.
        """
        # Simple token estimation based on word count
        import re
        words = re.findall(r'\b\w+\b', text)
        return len(words) + len(re.findall(r'[^\w\s]', text)) // 2


# Example usage
if __name__ == "__main__":
    import os
    # Set the OpenAI API key (in a real app, this would come from settings)
    os.environ["OPENAI_API_KEY"] = settings.openai_api_key

    chat_service = ChatService()

    # Test full-text mode
    response = chat_service.process_query(
        query_text="What is ROS?",
        session_id="test_session_1",
        mode=ChatMode.full_text
    )

    print(f"Response: {response.response_text}")
    print(f"Citations: {response.citations}")
    print(f"Confidence: {response.grounding_confidence}")