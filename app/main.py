from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import clean, chunk
import uvicorn

# Initialize the FastAPI application with a title.
app = FastAPI(title="Semantic ETL Service")

@app.get("/")
async def root():
    """
    Root endpoint. Public access.
    """
    return {"message": "Welcome to the Semantic ETL Service. Visit /docs for API documentation."}

# Register the API routers (Clean and Chunk endpoints).
# We prefix them with "/v1" for versioning.
app.include_router(clean.router, prefix="/v1", tags=["Clean"])
app.include_router(chunk.router, prefix="/v1", tags=["Chunk"])

@app.exception_handler(415)
async def unsupported_media_type_handler(request: Request, exc: Exception):
    """
    Custom exception handler for 415 Unsupported Media Type.
    Returns a JSON response with the error detail.
    """
    return JSONResponse(
        status_code=415,
        content={"detail": str(exc)},
    )

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to verify the server is running.
    """
    return {"status": "ok"}

# Entry point for running the application directly.
if __name__ == "__main__":
    # Run the Uvicorn server.
    # host="0.0.0.0" makes it accessible externally (if needed).
    # reload=True enables hot-reloading for development.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
