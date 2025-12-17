import re
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TextChunk:
    id: str
    content: str
    module_name: str
    chapter_title: str
    section_path: str
    token_count: int


class TextChunker:
    """
    Utility class for splitting text content into chunks of appropriate size for embedding.
    """

    def __init__(self, max_tokens: int = 400, min_tokens: int = 100, overlap: int = 50):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.overlap = overlap

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate the number of tokens in a text string.
        This is a rough estimation based on word count.
        """
        # Simple token estimation: words + punctuation + special tokens
        words = re.findall(r'\b\w+\b', text)
        return len(words) + len(re.findall(r'[^\w\s]', text)) // 2

    def chunk_text(self, text: str, module_name: str, chapter_title: str, section_path: str) -> List[TextChunk]:
        """
        Split text into chunks of appropriate size.
        """
        if not text.strip():
            return []

        # Split text into sentences
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = []
        current_chunk = []
        current_token_count = 0
        chunk_id = 0

        for sentence in sentences:
            sentence_token_count = self.estimate_tokens(sentence)

            # If a single sentence is too long, split it by paragraphs or fixed length
            if sentence_token_count > self.max_tokens:
                sub_chunks = self._split_long_sentence(sentence, module_name, chapter_title, section_path)
                chunks.extend(sub_chunks)
                continue

            # Check if adding this sentence would exceed the max token count
            if current_token_count + sentence_token_count > self.max_tokens and current_chunk:
                # Finalize current chunk
                chunk_content = ' '.join(current_chunk).strip()
                if self.min_tokens <= self.estimate_tokens(chunk_content) <= self.max_tokens:
                    chunks.append(
                        TextChunk(
                            id=f"{section_path}_chunk_{chunk_id}",
                            content=chunk_content,
                            module_name=module_name,
                            chapter_title=chapter_title,
                            section_path=section_path,
                            token_count=self.estimate_tokens(chunk_content)
                        )
                    )
                    chunk_id += 1

                # Start new chunk with overlap
                overlap_sentences = current_chunk[-max(0, len(current_chunk) - self.overlap // 10):]
                current_chunk = overlap_sentences + [sentence]
                current_token_count = sum(self.estimate_tokens(s) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_token_count += sentence_token_count

        # Add the final chunk if it meets the minimum size requirement
        if current_chunk:
            final_content = ' '.join(current_chunk).strip()
            if self.estimate_tokens(final_content) >= self.min_tokens:
                chunks.append(
                    TextChunk(
                        id=f"{section_path}_chunk_{chunk_id}",
                        content=final_content,
                        module_name=module_name,
                        chapter_title=chapter_title,
                        section_path=section_path,
                        token_count=self.estimate_tokens(final_content)
                    )
                )

        return chunks

    def _split_long_sentence(self, sentence: str, module_name: str, chapter_title: str, section_path: str) -> List[TextChunk]:
        """
        Split a sentence that is too long into smaller chunks.
        """
        chunks = []
        chunk_id = 0

        # Split by paragraphs first
        paragraphs = sentence.split('\n\n')

        current_sub_chunk = []
        current_token_count = 0

        for paragraph in paragraphs:
            para_token_count = self.estimate_tokens(paragraph)

            if current_token_count + para_token_count <= self.max_tokens:
                current_sub_chunk.append(paragraph)
                current_token_count += para_token_count
            else:
                # Finalize current sub-chunk
                if current_sub_chunk:
                    sub_content = '\n\n'.join(current_sub_chunk).strip()
                    chunks.append(
                        TextChunk(
                            id=f"{section_path}_chunk_{len(chunks)}",
                            content=sub_content,
                            module_name=module_name,
                            chapter_title=chapter_title,
                            section_path=section_path,
                            token_count=self.estimate_tokens(sub_content)
                        )
                    )

                # Start new sub-chunk
                current_sub_chunk = [paragraph]
                current_token_count = para_token_count

        # Add final sub-chunk
        if current_sub_chunk:
            sub_content = '\n\n'.join(current_sub_chunk).strip()
            chunks.append(
                TextChunk(
                    id=f"{section_path}_chunk_{len(chunks)}",
                    content=sub_content,
                    module_name=module_name,
                    chapter_title=chapter_title,
                    section_path=section_path,
                    token_count=self.estimate_tokens(sub_content)
                )
            )

        return chunks


# Example usage
if __name__ == "__main__":
    chunker = TextChunker()

    sample_text = """
    The Robot Operating System (ROS) is a flexible framework for writing robot software.
    It is a collection of tools, libraries, and conventions that aim to simplify the task
    of creating complex and robust robot behavior across a wide variety of robotic platforms.

    ROS provides hardware abstraction, device drivers, libraries, visualizers, message-passing,
    package management, and other capabilities. It simplifies the development of distributed
    robotic applications by providing services such as hardware abstraction, low-level device
    control, implementation of commonly used functionality, message passing between processes,
    and package management.
    """

    chunks = chunker.chunk_text(sample_text, "The Robotic Nervous System (ROS 2)", "Introduction to ROS", "module-1/introduction")

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk.token_count} tokens")
        print(f"Content preview: {chunk.content[:100]}...")
        print("---")