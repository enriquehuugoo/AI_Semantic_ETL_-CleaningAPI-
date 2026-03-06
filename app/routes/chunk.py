from fastapi import APIRouter, HTTPException
from app.models.requests import ChunkRequest
from app.models.responses import ChunkResponse
from app.services.chunker import chunk_markdown
import logging

# Initialize the API Router for chunk-related endpoints.
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chunk", response_model=ChunkResponse)
async def chunk_document(request: ChunkRequest):
    """
    Endpoint to chunk a markdown string into smaller, context-aware pieces.
    
    Args:
        request (ChunkRequest): The request body containing the markdown string.
        
    Returns:
        ChunkResponse: A list of text chunks.
        
    Raises:
        HTTPException(500): If chunking fails.
    """
    try:
        # Delegate the logic to the service layer.
        chunks = chunk_markdown(request.markdown)
        return ChunkResponse(chunks=chunks)
    except Exception as e:
        # Log and re-raise as 500.
        logger.error(f"Error chunking markdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))
