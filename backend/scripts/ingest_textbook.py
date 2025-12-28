#!/usr/bin/env python3
"""
Textbook Content Ingestion Script - REFINED
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

# Load environment variables from the root project folder
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
CHUNK_SIZE_MIN = 400
CHUNK_SIZE_MAX = 800
BATCH_SIZE = 96
VECTOR_DIM = 1024

class TextChunker:
    def __init__(self, min_size: int = CHUNK_SIZE_MIN, max_size: int = CHUNK_SIZE_MAX):
        self.min_size = min_size
        self.max_size = max_size

    def estimate_tokens(self, text: str) -> int:
        return len(text) // 4

    def split_by_headers(self, content: str) -> List[Tuple[str, str]]:
        header_pattern = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)
        sections = []
        last_end = 0
        current_header = ""
        for match in header_pattern.finditer(content):
            if last_end < match.start():
                section_content = content[last_end:match.start()].strip()
                if section_content:
                    sections.append((current_header, section_content))
            current_header = match.group(2).strip()
            last_end = match.end()
        if last_end < len(content):
            remaining = content[last_end:].strip()
            if remaining:
                sections.append((current_header, remaining))
        return sections

    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = []
        sections = self.split_by_headers(text)
        for header, section_content in sections:
            section_content = self._clean_content(section_content)
            if not section_content: continue
            estimated_tokens = self.estimate_tokens(section_content)
            if estimated_tokens <= self.max_size:
                chunks.append({"content": section_content, "metadata": {**metadata, "subsection": header}})
            else:
                paragraphs = section_content.split('\n\n')
                current_chunk = ""
                current_tokens = 0
                for para in paragraphs:
                    para_tokens = self.estimate_tokens(para)
                    if current_tokens + para_tokens > self.max_size:
                        if current_chunk:
                            chunks.append({"content": current_chunk.strip(), "metadata": {**metadata, "subsection": header}})
                        current_chunk = para
                        current_tokens = para_tokens
                    else:
                        current_chunk += "\n\n" + para if current_chunk else para
                        current_tokens += para_tokens
                if current_chunk and self.estimate_tokens(current_chunk) >= self.min_size:
                    chunks.append({"content": current_chunk.strip(), "metadata": {**metadata, "subsection": header}})
        return chunks

    def _clean_content(self, text: str) -> str:
        text = re.sub(r'```[\s\S]*?```', '', text)
        text = re.sub(r'`[^`]+`', '', text)
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

class CohereEmbedder:
    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key: raise ValueError("COHERE_API_KEY environment variable not set")
        self.client = cohere.Client(api_key=api_key, timeout=60)
        self.model = os.getenv("EMBEDDING_MODEL", "embed-multilingual-v3.0")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        all_embeddings = []
        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]
            logger.info(f"Embedding batch {i // BATCH_SIZE + 1} ({len(batch)} texts)")
            response = self.client.embed(texts=batch, model=self.model, input_type="search_document")
            all_embeddings.extend(response.embeddings)
        return all_embeddings

class QdrantIngester:
    def __init__(self, collection_name: str = None):
        url = os.getenv("QDRANT_URL")
        api_key = os.getenv("QDRANT_API_KEY")
        if not url: raise ValueError("QDRANT_URL environment variable not set")
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name or os.getenv("QDRANT_COLLECTION_NAME", "textbook_rag")
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' exists")
        except Exception:
            logger.info(f"Creating collection '{self.collection_name}'")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=VECTOR_DIM, distance=models.Distance.COSINE)
            )
        
        # --- FIX: Create Payload Index for metadata.file_path ---
        # This prevents the 400 Bad Request error during deletion
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="metadata.file_path",
            field_schema=models.PayloadSchemaType.KEYWORD,
        )

    def delete_by_filter(self, filter_key: str, filter_value: str):
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[models.FieldCondition(key=f"metadata.{filter_key}", match=models.MatchValue(value=filter_value))]
                    )
                )
            )
            logger.info(f"Deleted existing chunks for {filter_key}={filter_value}")
        except Exception as e:
            logger.warning(f"Could not delete existing chunks: {e}")

    def upsert_chunks(self, chunks: List[Dict], embeddings: List[List[float]]):
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())
            points.append(models.PointStruct(id=point_id, vector=embedding, payload={"content": chunk["content"], "metadata": chunk["metadata"]}))
        
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.client.upsert(collection_name=self.collection_name, points=batch)
            logger.info(f"Upserted batch {i // batch_size + 1} ({len(batch)} points)")

    def get_collection_info(self) -> Dict:
        # --- FIX: Safe attribute access for different SDK versions ---
        info = self.client.get_collection(self.collection_name)
        return {
            "name": self.collection_name,
            "points_count": getattr(info, 'points_count', 0)
        }

def find_markdown_files(docs_path: Path, module_filter: Optional[str] = None) -> List[Path]:
    files = []
    # Find .md and .mdx recursively
    for ext in ["*.md", "*.mdx"]:
        for f in docs_path.rglob(ext):
            if f.name.startswith("_") or f.name == "index.md": continue
            if module_filter and module_filter.lower() not in str(f).lower(): continue
            files.append(f)
    return sorted(files)

def extract_metadata(file_path: Path, docs_root: Path) -> Dict:
    relative = file_path.relative_to(docs_root)
    parts = relative.parts
    metadata = {"module": parts[0] if len(parts) >= 1 else "root", "chapter": file_path.stem.replace("-", " ").title(), "file_path": str(relative), "page_reference": file_path.stem}
    return metadata

def ingest_file(file_path: Path, docs_root: Path, chunker: TextChunker, embedder: CohereEmbedder, ingester: QdrantIngester, dry_run: bool = False) -> int:
    logger.info(f"Processing: {file_path.relative_to(docs_root)}")
    content = file_path.read_text(encoding="utf-8")
    metadata = extract_metadata(file_path, docs_root)
    chunks = chunker.chunk_text(content, metadata)
    if not chunks: return 0
    if dry_run: return len(chunks)
    ingester.delete_by_filter("file_path", str(file_path.relative_to(docs_root)))
    texts = [chunk["content"] for chunk in chunks]
    embeddings = embedder.embed_documents(texts)
    ingester.upsert_chunks(chunks, embeddings)
    return len(chunks)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--module", type=str)
    parser.add_argument("--docs-path", type=str, default=None)
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent.parent
    docs_path = Path(args.docs_path) if args.docs_path else project_root / "frontend" / "docs"

    if not docs_path.exists():
        logger.error(f"Docs directory not found: {docs_path}")
        sys.exit(1)

    chunker = TextChunker()
    embedder = CohereEmbedder() if not args.dry_run else None
    ingester = QdrantIngester() if not args.dry_run else None

    files = find_markdown_files(docs_path, args.module)
    logger.info(f"Found {len(files)} MDX/markdown files")

    total_chunks = 0
    for file_path in files:
        try:
            total_chunks += ingest_file(file_path, docs_path, chunker, embedder, ingester, args.dry_run)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    logger.info(f"\nIngestion complete!")
    if not args.dry_run and ingester:
        info = ingester.get_collection_info()
        logger.info(f"Collection '{info['name']}' now has {info['points_count']} points")

if __name__ == "__main__":
    main()