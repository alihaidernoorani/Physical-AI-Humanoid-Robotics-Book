#!/usr/bin/env python3
"""
Script to index the textbook content into Qdrant vector database using Cohere embeddings.
This script extracts content from the docs directory, chunks it,
generates Cohere embeddings, and stores everything in Qdrant.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.services.textbook_content_extractor import TextbookContentExtractor
from src.services.embedding_service import EmbeddingService
from src.services.retrieval_service import RetrievalService
from src.config.settings import settings


def main():
    print("Starting textbook content indexing with Cohere embeddings...")

    # Initialize services
    extractor = TextbookContentExtractor()
    embedding_service = EmbeddingService()
    retrieval_service = RetrievalService()

    # Extract content from textbook
    print("Extracting content from textbook...")
    chunks = extractor.extract_all_modules()

    if not chunks:
        print("No content found to index. Please check the docs directory.")
        return

    print(f"Extracted {len(chunks)} text chunks from the textbook")

    # Generate Cohere embeddings for all chunks
    print("Generating Cohere embeddings...")
    texts = [chunk.content for chunk in chunks]

    # Process in batches to avoid memory issues
    batch_size = 50  # Reduced batch size for Cohere API limits
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        batch_embeddings = embedding_service.generate_embeddings_batch(batch_texts)
        all_embeddings.extend(batch_embeddings)
        print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} chunks...")

    print(f"Generated {len(all_embeddings)} Cohere embeddings")

    # Store in Qdrant (with 1024-dimensional vectors for Cohere)
    print("Storing embeddings in Qdrant...")
    success = retrieval_service.store_chunks(chunks, all_embeddings)

    if success:
        print(f"Successfully indexed {len(chunks)} chunks into Qdrant collection '{retrieval_service.collection_name}' with Cohere embeddings")
        print("Indexing complete!")
    else:
        print("Failed to store chunks in Qdrant")


if __name__ == "__main__":
    # Load environment variables
    if not os.getenv("COHERE_API_KEY"):
        print("Warning: COHERE_API_KEY environment variable not set. Please set it before running this script.")
        print("Example: export COHERE_API_KEY=your_cohere_api_key_here")

    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable not set. Please set it before running this script.")
        print("Example: export GEMINI_API_KEY=your_gemini_api_key_here")

    if not os.getenv("QDRANT_URL"):
        print("Warning: QDRANT_URL environment variable not set. Using default value.")

    main()