"""
Text processing utilities for KETA.
"""

import logging
from typing import Iterator

logger = logging.getLogger(__name__)


def chunk_text(text: str, max_chunk_size: int = 10000, overlap: int = 500) -> list[str]:
    """
    Split text into chunks with optional overlap.

    Args:
        text: Text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Number of overlapping characters between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        # Calculate end position
        end = min(start + max_chunk_size, text_length)

        # Try to find a good breaking point (sentence or paragraph end)
        if end < text_length:
            # Look for sentence endings within the last 20% of the chunk
            search_start = max(start + int(max_chunk_size * 0.8), start)
            chunk_portion = text[search_start:end]

            # Try to find sentence breaks
            for delimiter in ["\n\n", "\n", ". ", "! ", "? "]:
                last_break = chunk_portion.rfind(delimiter)
                if last_break != -1:
                    end = search_start + last_break + len(delimiter)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move to next chunk with overlap
        start = end - overlap if end < text_length else text_length

    logger.info(f"Split text into {len(chunks)} chunks (max_size={max_chunk_size})")
    return chunks


def chunk_text_iterator(
    text: str, max_chunk_size: int = 10000, overlap: int = 500
) -> Iterator[tuple[int, str]]:
    """
    Iterator version of chunk_text that yields (index, chunk) tuples.

    Args:
        text: Text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Number of overlapping characters between chunks

    Yields:
        Tuple of (chunk_index, chunk_text)
    """
    chunks = chunk_text(text, max_chunk_size, overlap)
    for index, chunk in enumerate(chunks):
        yield index, chunk


def extract_text_snippet(text: str, max_length: int = 500) -> str:
    """
    Extract a snippet from the beginning of text.

    Args:
        text: Full text
        max_length: Maximum snippet length

    Returns:
        Text snippet
    """
    if len(text) <= max_length:
        return text

    snippet = text[:max_length].strip()

    # Try to end at a sentence boundary
    for delimiter in [". ", "! ", "? ", "\n"]:
        last_break = snippet.rfind(delimiter)
        if last_break > max_length * 0.8:  # Only use if break is near the end
            return snippet[: last_break + len(delimiter)].strip() + "..."

    return snippet + "..."


def count_tokens_estimate(text: str) -> int:
    """
    Rough estimate of token count for text.

    Uses approximation of ~4 characters per token.

    Args:
        text: Text to estimate

    Returns:
        Estimated token count
    """
    return len(text) // 4
