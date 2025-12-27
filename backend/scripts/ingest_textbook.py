#!/usr/bin/env python3
"""
Textbook Content Ingestion Script

Ingests markdown content from the docs/ directory into Qdrant vector database
using Cohere embeddings with proper input_type parameters.

Usage:
    python scripts/ingest_textbook.py [--dry-run] [--module MODULE_NAME]

Features:
    - Chunks markdown files (500-1000 tokens)
    - Generates embeddings with Cohere embed-v3 (input_type="search_document")
    - Stores vectors in Qdrant with metadata
    - Supports incremental updates (deletes old chunks before re-ingesting)
"""
import argparse
import logging
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
CHUNK_SIZE_MIN = 400  # Minimum tokens per chunk
CHUNK_SIZE_MAX = 800  # Maximum tokens per chunk
BATCH_SIZE = 96  # Cohere API batch limit
VECTOR_DIM = 1024  # Cohere embed-v3 dimension


class TextChunker:
    """
    Splits markdown text into semantic chunks of appropriate size.
    """

    def __init__(self, min_size: int = CHUNK_SIZE_MIN, max_size: int = CHUNK_SIZE_MAX):
        self.min_size = min_size
        self.max_size = max_size

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (4 chars per token average)."""
        return len(text) // 4

    def split_by_headers(self, content: str) -> List[Tuple[str, str]]:
        """
        Split content by markdown headers, returning (header, content) tuples.
        """
        # Pattern to match headers (## or ###)
        header_pattern = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)

        sections = []
        last_end = 0
        current_header = ""

        for match in header_pattern.finditer(content):
            # Get content before this header
            if last_end < match.start():
                section_content = content[last_end:match.start()].strip()
                if section_content:
                    sections.append((current_header, section_content))

            current_header = match.group(2).strip()
            last_end = match.end()

        # Get remaining content
        if last_end < len(content):
            remaining = content[last_end:].strip()
            if remaining:
                sections.append((current_header, remaining))

        return sections

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Chunk text into appropriately sized pieces with metadata.
        """
        chunks = []
        sections = self.split_by_headers(text)

        for header, section_content in sections:
            # Clean the content
            section_content = self._clean_content(section_content)

            if not section_content:
                continue

            estimated_tokens = self.estimate_tokens(section_content)

            if estimated_tokens <= self.max_size:
                # Section fits in one chunk
                chunks.append({
                    "content": section_content,
                    "metadata": {
                        **metadata,
                        "subsection": header
                    }
                })
            else:
                # Split large sections by paragraphs
                paragraphs = section_content.split('\n\n')
                current_chunk = ""
                current_tokens = 0

                for para in paragraphs:
                    para_tokens = self.estimate_tokens(para)

                    if current_tokens + para_tokens > self.max_size:
                        if current_chunk:
                            chunks.append({
                                "content": current_chunk.strip(),
                                "metadata": {
                                    **metadata,
                                    "subsection": header
                                }
                            })
                        current_chunk = para
                        current_tokens = para_tokens
                    else:
                        current_chunk += "\n\n" + para if current_chunk else para
                        current_tokens += para_tokens

                # Add remaining chunk
                if current_chunk and self.estimate_tokens(current_chunk) >= self.min_size:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "metadata": {
                            **metadata,
                            "subsection": header
                        }
                    })

        return chunks

    def _clean_content(self, text: str) -> str:
        """Clean markdown content for embedding."""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        # Remove inline code
        text = re.sub(r'`[^`]+`', '', text)
        # Remove images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # Remove links but keep text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Clean up whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()


class CohereEmbedder:
    """
    Generates embeddings using Cohere's embed-v3 model.
    """

    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")

        self.client = cohere.Client(api_key=api_key, timeout=60)
        self.model = os.getenv("EMBEDDING_MODEL", "embed-multilingual-v3.0")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for documents using input_type="search_document".
        """
        all_embeddings = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            logger.info(f"Embedding batch {i // BATCH_SIZE + 1} ({len(batch)} texts)")

            response = self.client.embed(
                texts=batch,
                model=self.model,
                input_type="search_document"  # Critical for embed-v3
            )
            all_embeddings.extend(response.embeddings)

        return all_embeddings


class QdrantIngester:
    """
    Ingests content into Qdrant vector database.
    """

    def __init__(self, collection_name: str = None):
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")

        if not url:
            raise ValueError("QDRANT_URL environment variable not set")

        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION_NAME", "textbook_rag")
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if it doesn't exist."""
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' exists")
        except Exception:
            logger.info(f"Creating collection '{self.collection_name}'")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=VECTOR_DIM,
                    distance=models.Distance.COSINE
                )
            )

    def delete_by_filter(self, filter_key: str, filter_value: str):
        """Delete points matching a filter."""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key=f"metadata.{filter_key}",
                                match=models.MatchValue(value=filter_value)
                            )
                        ]
                    )
                )
            )
            logger.info(f"Deleted existing chunks for {filter_key}={filter_value}")
        except Exception as e:
            logger.warning(f"Could not delete existing chunks: {e}")

    def upsert_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        """Upsert chunks with embeddings into Qdrant."""
        points = []

        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "content": chunk["content"],
                        "metadata": chunk["metadata"]
                    }
                )
            )

        # Batch upsert
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch
            )
            logger.info(f"Upserted batch {i // batch_size + 1} ({len(batch)} points)")

        logger.info(f"Successfully ingested {len(points)} chunks")

    def get_collection_info(self) -> Dict:
        """Get collection statistics."""
        info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "points_count": info.points_count,
            "vectors_count": info.vectors_count
        }


def find_markdown_files(docs_path: Path, module_filter: Optional[str] = None) -> List[Path]:
    """Find all markdown files in docs directory."""
    files = []

    for md_file in docs_path.rglob("*.md"):
        # Skip index files and non-content files
        if md_file.name.startswith("_") or md_file.name == "index.md":
            continue

        # Apply module filter if specified
        if module_filter:
            if module_filter.lower() not in str(md_file).lower():
                continue

        files.append(md_file)

    # Also check for .mdx files
    for mdx_file in docs_path.rglob("*.mdx"):
        if mdx_file.name.startswith("_"):
            continue
        if module_filter and module_filter.lower() not in str(mdx_file).lower():
            continue
        files.append(mdx_file)

    return sorted(files)


def extract_metadata(file_path: Path, docs_root: Path) -> Dict:
    """Extract metadata from file path."""
    relative = file_path.relative_to(docs_root)
    parts = relative.parts

    # Default metadata
    metadata = {
        "module": "",
        "chapter": "",
        "file_path": str(relative),
        "page_reference": file_path.stem
    }

    # Extract module from path (e.g., module-1-foundations)
    if len(parts) >= 1:
        module_part = parts[0]
        if module_part.startswith("module"):
            metadata["module"] = module_part
        else:
            metadata["module"] = module_part

    # Extract chapter name from filename
    if file_path.stem:
        # Convert filename to readable chapter name
        chapter_name = file_path.stem.replace("-", " ").replace("_", " ").title()
        metadata["chapter"] = chapter_name

    return metadata


def ingest_file(
    file_path: Path,
    docs_root: Path,
    chunker: TextChunker,
    embedder: CohereEmbedder,
    ingester: QdrantIngester,
    dry_run: bool = False
) -> int:
    """Ingest a single markdown file."""
    logger.info(f"Processing: {file_path.relative_to(docs_root)}")

    # Read content
    content = file_path.read_text(encoding="utf-8")

    # Extract metadata
    metadata = extract_metadata(file_path, docs_root)

    # Chunk content
    chunks = chunker.chunk_text(content, metadata)

    if not chunks:
        logger.warning(f"No chunks generated for {file_path}")
        return 0

    logger.info(f"  Generated {len(chunks)} chunks")

    if dry_run:
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            logger.info(f"  Chunk {i + 1}: {chunk['content'][:100]}...")
        return len(chunks)

    # Delete existing chunks for this file
    ingester.delete_by_filter("file_path", str(file_path.relative_to(docs_root)))

    # Generate embeddings
    texts = [chunk["content"] for chunk in chunks]
    embeddings = embedder.embed_documents(texts)

    # Upsert to Qdrant
    ingester.upsert_chunks(chunks, embeddings)

    return len(chunks)


def main():
    parser = argparse.ArgumentParser(description="Ingest textbook content into Qdrant")
    parser.add_argument("--dry-run", action="store_true", help="Preview without ingesting")
    parser.add_argument("--module", type=str, help="Only process specific module")
    parser.add_argument("--docs-path", type=str, default=None, help="Path to docs directory")
    args = parser.parse_args()

    # Determine docs path
    if args.docs_path:
        docs_path = Path(args.docs_path)
    else:
        # Default: look for docs/ relative to project root
        project_root = Path(__file__).parent.parent.parent
        docs_path = project_root / "docs"

    if not docs_path.exists():
        logger.error(f"Docs directory not found: {docs_path}")
        sys.exit(1)

    logger.info(f"Docs path: {docs_path}")
    logger.info(f"Dry run: {args.dry_run}")
    if args.module:
        logger.info(f"Module filter: {args.module}")

    # Initialize components
    chunker = TextChunker()

    if not args.dry_run:
        embedder = CohereEmbedder()
        ingester = QdrantIngester()
    else:
        embedder = None
        ingester = None

    # Find markdown files
    files = find_markdown_files(docs_path, args.module)
    logger.info(f"Found {len(files)} markdown files")

    if not files:
        logger.warning("No files to process")
        return

    # Process files
    total_chunks = 0
    for file_path in files:
        try:
            chunks = ingest_file(
                file_path,
                docs_path,
                chunker,
                embedder,
                ingester,
                args.dry_run
            )
            total_chunks += chunks
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    logger.info(f"\nIngestion complete!")
    logger.info(f"Total files processed: {len(files)}")
    logger.info(f"Total chunks {'generated' if args.dry_run else 'ingested'}: {total_chunks}")

    # Show collection info
    if not args.dry_run and ingester:
        info = ingester.get_collection_info()
        logger.info(f"Collection '{info['name']}' now has {info['points_count']} points")


if __name__ == "__main__":
    main()
