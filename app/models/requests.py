from pydantic import BaseModel

class ChunkRequest(BaseModel):
    """
    Request schema for the chunking endpoint.
    """
    # The raw markdown string to be split into chunks.
    markdown: str
