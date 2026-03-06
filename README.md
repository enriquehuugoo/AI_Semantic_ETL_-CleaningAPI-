# Semantic ETL Service

A production-grade FastAPI application that serves as a Semantic ETL service for LLMs. It cleans documents (PDF, DOCX, HTML) into Markdown using [Docling](https://github.com/DS4SD/docling) and chunks text for LLM context windows.

## Features

-   **Clean Endpoint**: Converts PDF, DOCX, and HTML to Markdown with metadata and table extraction.
-   **Chunk Endpoint**: Context-aware chunking of Markdown text (max 512 tokens).
-   **Authentication**: API Key protection via `X-API-Key` header.
-   **Rate Limiting**: Throttling to prevent abuse (e.g., 5 requests/minute for heavy ops).
-   **Usage Logging**: Tracks usage per API key for billing/monitoring.
-   **Docker Ready**: Includes Dockerfile for easy deployment.

## Installation

### Local Development

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd AI_cleaningAPI
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # Linux/Mac
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory:
    ```env
    VALID_API_KEYS=my-secret-key,another-key
    ```
    *Note: If no keys are set, all requests will be rejected.*

5.  **Run the server**:
    ```bash
    uvicorn app.main:app --reload
    ```

## Usage

### Authentication
All API requests must include the `X-API-Key` header.

### Endpoints

#### `POST /v1/clean`
Upload a file to convert it to Markdown.
-   **Headers**: `X-API-Key: <your-key>`
-   **Body**: `file` (multipart/form-data)
-   **Limits**: Max file size 10MB. Rate limit: 5/minute.

#### `POST /v1/chunk`
Split Markdown text into chunks.
-   **Headers**: `X-API-Key: <your-key>`
-   **Body**: JSON `{"markdown": "string"}`
-   **Limits**: Rate limit: 20/minute.

## Deployment with Docker

1.  **Build the image**:
    ```bash
    docker build -t ai-cleaning-api .
    ```

2.  **Run the container**:
    ```bash
    docker run -d -p 8000:8000 -e VALID_API_KEYS="production-secret-key" ai-cleaning-api
    ```

## License
[Your License Here]
