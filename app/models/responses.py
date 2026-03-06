from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class CleanMetadata(BaseModel):
    """
    Metadata extracted from the cleaned document.
    """
    # The detected file type (e.g., PDF, DOCX, HTML).
    file_type: str
    # Total character count of the markdown output.
    character_count: int
    # Estimated token count using tiktoken (cl100k_base encoding).
    estimated_tokens: int

class CleanResponse(BaseModel):
    """
    Response schema for the cleaning endpoint.
    """
    # The cleaned text content in Markdown format.
    markdown: str
    # Metadata about the file and content.
    metadata: CleanMetadata
    # A list of tables found in the document, formatted as Markdown strings.
    tables: List[str]

class ChunkResponse(BaseModel):
    """
    Response schema for the chunking endpoint.
    """
    # A list of text chunks, each legally sized within the token limit.
    chunks: List[str]
