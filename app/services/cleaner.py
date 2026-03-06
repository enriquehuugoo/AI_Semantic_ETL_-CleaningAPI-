import tempfile
import os
from pathlib import Path
from docling.document_converter import DocumentConverter
import tiktoken
from app.models.responses import CleanResponse, CleanMetadata

# Initialize the Docling converter. This is a heavy object, so we instantiate it once globally.
# It handles the conversion of various document formats (PDF, DOCX, HTML, etc.) to Markdown.
converter = DocumentConverter()

# Initialize the tokenizer for counting tokens. 
# We use 'cl100k_base', which is the encoding used by OpenAI's GPT-4 and GPT-3.5 models.
encoding = tiktoken.get_encoding("cl100k_base")

def clean_file(file_content: bytes, filename: str) -> CleanResponse:
    """
    Process a raw file and convert it to Markdown using Docling.
    
    Args:
        file_content (bytes): The raw binary content of the file.
        filename (str): The original filename, used to determine the extension.
        
    Returns:
        CleanResponse: The structured response containing markdown, metadata, and extracted tables.
    """
    
    # Determine the file extension to tell Docling what kind of file it is processing.
    file_ext = os.path.splitext(filename)[1].lower()
    
    # Docling's current API primarily works with file paths rather than in-memory bytes.
    # We write the content to a temporary file ensuring the correct extension is preserved.
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name
    
    try:
        # Perform the document conversion.
        # This scans the file, performs OCR if necessary (depending on config), and extracts structure.
        result = converter.convert(tmp_path)
        doc = result.document
        
        # Export the main content of the document to Markdown format.
        markdown_text = doc.export_to_markdown()
        
        # Extract tables found in the document.
        # We iterate through the tables identified by Docling and convert them individually to Markdown.
        tables = []
        for table in doc.tables:
            # Check if the table object has an export method (API compatibility check)
            if hasattr(table, "export_to_markdown"):
                tables.append(table.export_to_markdown())
            else:
                # Fallback for older versions or different table objects
                tables.append(str(table))

        # Calculate metadata statistics.
        # Character count is the raw length of the string.
        char_count = len(markdown_text)
        # Token count is estimated using tiktoken to help the user plan context window usage.
        token_count = len(encoding.encode(markdown_text))
        
        metadata = CleanMetadata(
            file_type=file_ext.strip('.').upper(),
            character_count=char_count,
            estimated_tokens=token_count
        )
        
        return CleanResponse(
            markdown=markdown_text,
            metadata=metadata,
            tables=tables
        )
        
    finally:
        # Crucial clean-up step: ensure the temporary file is removed to prevent disk space leaks.
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
