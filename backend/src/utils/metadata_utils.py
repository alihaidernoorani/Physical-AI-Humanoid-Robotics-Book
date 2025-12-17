from typing import Dict, Any, List
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def validate_metadata(metadata: Dict[str, Any]) -> bool:
    """
    Validate that required metadata fields are present and properly formatted
    """
    required_fields = ["module", "chapter", "subsection", "source_type", "source_origin"]

    for field in required_fields:
        if field not in metadata or not metadata[field] or not isinstance(metadata[field], str) or len(metadata[field].strip()) == 0:
            logger.error(f"Missing or invalid required metadata field: {field}")
            return False

    # Additional validation for specific fields
    if len(metadata["module"]) > 200:
        logger.error("Module name is too long (max 200 characters)")
        return False

    if len(metadata["chapter"]) > 200:
        logger.error("Chapter name is too long (max 200 characters)")
        return False

    if len(metadata["subsection"]) > 200:
        logger.error("Subsection name is too long (max 200 characters)")
        return False

    # Validate source_type
    valid_source_types = ["textbook", "diagram", "exercise", "example", "definition", "theorem", "code", "figure"]
    if metadata["source_type"] not in valid_source_types:
        logger.error(f"Invalid source_type: {metadata['source_type']}. Must be one of {valid_source_types}")
        return False

    return True

def sanitize_content(content: str) -> str:
    """
    Sanitize content by removing potentially harmful characters or patterns
    """
    if not content:
        return ""

    # Remove any potential script tags or other harmful content
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

    # Remove control characters except common whitespace
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)

    return sanitized.strip()

def extract_module_info_from_path(file_path: str) -> Dict[str, str]:
    """
    Extract module, chapter, and subsection info from a file path
    Example: docs/module1/chapter1/subsection1.md -> {"module": "Module 1", "chapter": "Chapter 1", "subsection": "Subsection 1"}
    """
    path_parts = file_path.strip('/').split('/')

    # Look for patterns that indicate module/chapter/subsection
    module = ""
    chapter = ""
    subsection = ""

    # Simple heuristic to extract module/chapter/subsection from path
    for i, part in enumerate(path_parts):
        clean_part = part.replace('_', ' ').replace('-', ' ').title()

        if i == 0 and 'docs' in part.lower():
            continue  # Skip 'docs' directory
        elif i == 1:  # Likely module
            module = clean_part
        elif i == 2:  # Likely chapter
            chapter = clean_part
        elif i == 3:  # Likely subsection
            subsection = clean_part
            break  # Stop at subsection level

    return {
        "module": module or "Unknown Module",
        "chapter": chapter or "Unknown Chapter",
        "subsection": subsection or "Unknown Subsection"
    }

def format_citation(chunk_info: Dict[str, Any]) -> str:
    """
    Format a citation string from chunk metadata
    """
    module = chunk_info.get("module", "Unknown Module")
    chapter = chunk_info.get("chapter", "Unknown Chapter")
    subsection = chunk_info.get("subsection", "Unknown Subsection")
    page_reference = chunk_info.get("page_reference", "")

    citation = f"{module} - {chapter}"
    if subsection != "Unknown Subsection":
        citation += f" - {subsection}"

    if page_reference:
        citation += f" (Page/Section: {page_reference})"

    return citation

def calculate_confidence_score(relevance_scores: List[float], threshold: float = 0.3) -> float:
    """
    Calculate a confidence score based on relevance scores from vector search
    """
    if not relevance_scores:
        return 0.0

    # Calculate average relevance score
    avg_score = sum(relevance_scores) / len(relevance_scores)

    # Normalize to 0-1 scale based on threshold
    if avg_score >= threshold:
        # Scale scores above threshold to 0.5-1.0 range
        normalized = 0.5 + (0.5 * (avg_score - threshold) / (1.0 - threshold))
        return min(1.0, normalized)
    else:
        # Scale scores below threshold to 0.0-0.5 range
        normalized = 0.5 * (avg_score / threshold)
        return max(0.0, normalized)

def is_content_sufficient(content: str, min_chars: int = 50) -> bool:
    """
    Check if content is sufficient for RAG processing
    """
    if not content:
        return False

    clean_content = sanitize_content(content)
    return len(clean_content) >= min_chars

def generate_chunk_id(content: str, metadata: Dict[str, Any]) -> str:
    """
    Generate a unique chunk ID based on content hash and metadata
    """
    import hashlib

    # Create a unique identifier from content and metadata
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:16]
    module_hash = hashlib.md5(metadata.get("module", "").encode('utf-8')).hexdigest()[:8]
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    return f"chunk_{module_hash}_{content_hash}_{timestamp}"

def validate_chunk_content(content: str) -> Dict[str, Any]:
    """
    Validate chunk content and return validation results
    """
    results = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "sanitized_content": sanitize_content(content)
    }

    if not content:
        results["is_valid"] = False
        results["errors"].append("Content cannot be empty")
        return results

    if len(content) < 50:
        results["warnings"].append("Content is very short (< 50 characters)")

    if len(content) > 2000:
        results["is_valid"] = False
        results["errors"].append("Content is too long (> 2000 characters)")

    # Check for potential issues
    if content.count('\n') > 20:
        results["warnings"].append("Content has many line breaks")

    return results