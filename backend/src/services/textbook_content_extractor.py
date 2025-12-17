import os
import re
from typing import List, Dict, Tuple
from pathlib import Path
from src.utils.text_chunker import TextChunk, TextChunker


class TextbookContentExtractor:
    """
    Extract content from the textbook docs directory and prepare it for embedding.
    """

    def __init__(self, docs_path: str = "../../../docs"):
        self.docs_path = Path(docs_path)
        self.chunker = TextChunker()

    def extract_all_modules(self) -> List[TextChunk]:
        """
        Extract content from all modules in the textbook.
        """
        all_chunks = []

        # Find all module directories
        for module_dir in self.docs_path.iterdir():
            if module_dir.is_dir() and "module" in module_dir.name.lower():
                print(f"Processing module: {module_dir.name}")
                module_chunks = self.extract_module_content(module_dir)
                all_chunks.extend(module_chunks)

        return all_chunks

    def extract_module_content(self, module_dir: Path) -> List[TextChunk]:
        """
        Extract content from a single module directory.
        """
        chunks = []

        # Get module name from directory name
        module_name = self._clean_module_name(module_dir.name)

        # Process all markdown files in the module
        for md_file in module_dir.rglob("*.md*"):  # Process both .md and .mdx files
            if md_file.is_file():
                print(f"  Processing file: {md_file.name}")
                file_chunks = self.extract_file_content(md_file, module_name)
                chunks.extend(file_chunks)

        return chunks

    def extract_file_content(self, file_path: Path, module_name: str) -> List[TextChunk]:
        """
        Extract content from a single markdown file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove markdown headers and metadata if present
            content = self._clean_markdown_content(content)

            # Extract chapter and section info from file path
            chapter_title = self._extract_chapter_title(file_path)
            section_path = self._create_section_path(file_path)

            # Chunk the content
            chunks = self.chunker.chunk_text(
                content,
                module_name,
                chapter_title,
                section_path
            )

            return chunks
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return []

    def _clean_module_name(self, dir_name: str) -> str:
        """
        Clean and format the module name.
        """
        # Convert snake_case or kebab-case to readable format
        name = dir_name.replace('_', ' ').replace('-', ' ')
        return name.title()

    def _extract_chapter_title(self, file_path: Path) -> str:
        """
        Extract chapter title from the file path.
        """
        # Use the filename as the chapter title (without extension)
        return file_path.stem.replace('_', ' ').replace('-', ' ').title()

    def _create_section_path(self, file_path: Path) -> str:
        """
        Create a section path from the file path relative to docs directory.
        """
        # Get the relative path from docs directory
        relative_path = file_path.relative_to(self.docs_path)
        # Convert to forward slashes and remove extension
        section_path = str(relative_path).replace('\\', '/').replace('.mdx', '').replace('.md', '')
        return section_path

    def _clean_markdown_content(self, content: str) -> str:
        """
        Remove markdown metadata and headers from content.
        """
        # Remove frontmatter (content between --- delimiters)
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove markdown headers but keep the text
        # This regex removes # headers but keeps the content
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

        # Remove image references and links but keep alt text
        content = re.sub(r'!\[([^\]]*)\]\([^)]*\)', r'\1', content)

        # Remove reference-style links but keep link text
        content = re.sub(r'\[([^\]]+)\]\[[^\]]*\]', r'\1', content)

        # Remove inline links but keep link text
        content = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', content)

        # Remove extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)

        return content.strip()


# Example usage
if __name__ == "__main__":
    extractor = TextbookContentExtractor()
    print("Extracting textbook content...")

    chunks = extractor.extract_all_modules()

    print(f"Extracted {len(chunks)} chunks from the textbook")

    # Print some statistics
    total_tokens = sum(chunk.token_count for chunk in chunks)
    print(f"Total tokens: {total_tokens}")
    print(f"Average chunk size: {total_tokens / len(chunks) if chunks else 0:.2f} tokens")

    # Print first few chunks as examples
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1}:")
        print(f"  ID: {chunk.id}")
        print(f"  Module: {chunk.module_name}")
        print(f"  Chapter: {chunk.chapter_title}")
        print(f"  Section: {chunk.section_path}")
        print(f"  Tokens: {chunk.token_count}")
        print(f"  Content preview: {chunk.content[:100]}...")