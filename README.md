# Semantic ETL Service & Studio

A robust Semantic ETL service designed to prepare documents for Large Language Models (LLMs). It utilizes [Docling](https://github.com/DS4SD/docling) to clean and convert complex documents (PDF, DOCX, HTML) into structured Markdown and provides context-aware chunking optimized for vector embeddings.

The project consists of two parts:
1.  **FastAPI Backend**: The core engine that processes documents.
2.  **Streamlit Frontend (Studio)**: An interactive web interface to easily use the API.

## Features

-   **Clean Endpoint / UI Tool**: Accurately parses PDF, DOCX, and HTML into clean Markdown. It automatically isolates data tables and calculates token telemetry.
-   **Chunk Endpoint / UI Tool**: Context-aware chunking of Markdown text that strictly respects header boundaries and enforces a max limit of 512 tokens per chunk.
-   **No-Noise Architecture**: The API is fully decoupled and standalone, containing no unnecessary billing, authentication, or rate-limiting bloat.

## Installation

### Prerequisites
- Python 3.9+

### Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/enriquehuugoo/AI_Semantic_ETL_-CleaningAPI-.git
    cd AI_Semantic_ETL_-CleaningAPI-
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    
    # Windows:
    .\venv\Scripts\activate
    
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

### Option 1: The Easy Way (Windows)
We've included a script that automatically boots up both the FastAPI backend and the Streamlit frontend.
```powershell
.\run_local.ps1
```
This will open the Semantic ETL Studio in your default web browser at `http://localhost:8501`.

### Option 2: Manual Start
If you prefer manual control or are on Mac/Linux, run these in two separate terminal windows (ensure your virtual environment is active in both).

**Terminal 1 (Backend API):**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
*The API interactive documentation will be available at http://127.0.0.1:8000/docs*

**Terminal 2 (Frontend Studio):**
```bash
streamlit run streamlit_app.py
```

## API Usage (Direct)

If you wish to bypass the Streamlit UI and use the API natively in your own applications:

### `POST /v1/clean`
Upload a file to convert it to Markdown.
-   **Body**: `file` (multipart/form-data)
-   **Supported Types**: PDF, DOCX, HTML

### `POST /v1/chunk`
Split Markdown text into semantic chunks.
-   **Body**: JSON `{"markdown": "your markdown string here"}`

## License
MIT License
