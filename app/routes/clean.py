from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.cleaner import clean_file
from app.models.responses import CleanResponse
import logging
import os

# Initialize the API Router for clean-related endpoints.
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/clean", response_model=CleanResponse)
async def clean_document(file: UploadFile = File(...)):
    """
    Endpoint to clean a document file (PDF, DOCX, HTML) and return structured data.
    
    Args:
        file (UploadFile): The binary file uploaded by the user.
        
    Returns:
        CleanResponse: The cleaned markdown, metadata, and tables.
        
    Raises:
        HTTPException(400): If filename is missing.
        HTTPException(415): If the file type is not supported.
        HTTPException(500): If an internal processing error occurs.
    """
    
    # Validation: Ensure a filename is provided.
    if not file.filename:
         raise HTTPException(status_code=400, detail="Filename is missing")
         
    # Validation: Check file extension against allowed types.
    # While Docling supports many formats, we restrict to the ones requested in the requirements.
    allowed_extensions = {".pdf", ".docx", ".html", ".htm"}
    ext = os.path.splitext(file.filename)[1].lower()
    
    if ext not in allowed_extensions:
        raise HTTPException(status_code=415, detail=f"Unsupported Media Type. Allowed: {allowed_extensions}")

    try:
        # Read the file content into memory.
        # Note: For extremely large files, streaming to disk first (which we do in clean_file via tempfile) is better.
        # fastAPI UploadFile.read() reads into memory.
        content = await file.read()
        
        # Call the service layer to process the file.
        return clean_file(content, file.filename)
        
    except Exception as e:
        # Log the error for debugging.
        logger.error(f"Error cleaning file {file.filename}: {e}")
        
        # Error Handling Strategy:
        # If the error message clearly indicates "unsupported" (from docling or our logic), return 415.
        # Otherwise, default to a 500 Internal Server Error but return the detail for transparency.
        if "unsupported" in str(e).lower():
             raise HTTPException(status_code=415, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
