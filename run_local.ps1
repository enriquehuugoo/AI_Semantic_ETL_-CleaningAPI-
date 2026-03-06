# PowerShell script to run both API and Streamlit UI simultaneously
Write-Host "Starting AI Cleaning API & Semantic ETL Studio..." -ForegroundColor Cyan

# Check if port 8000 is open (API server)
try {
    $port_check = Test-NetConnection -ComputerName 127.0.0.1 -Port 8000 -InformationLevel Quiet
    if ($port_check) {
        Write-Host "WARNING: A process is already running on port 8000. Assuming API is up." -ForegroundColor Yellow
    } else {
        # Start backend asynchronously
        Write-Host "Starting FastAPI Backend on port 8000..." -ForegroundColor Green
        Start-Process -NoNewWindow -FilePath "powershell.exe" -ArgumentList "-Command `"venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000`""
        Start-Sleep -Seconds 3
    }
} catch {
    Write-Host "Starting FastAPI Backend..." -ForegroundColor Green
    Start-Process -NoNewWindow -FilePath "powershell.exe" -ArgumentList "-Command `"venv\Scripts\Activate.ps1; uvicorn app.main:app --host 0.0.0.0 --port 8000`""
    Start-Sleep -Seconds 3
}

# Start Frontend
Write-Host "Starting Streamlit Frontend on port 8501..." -ForegroundColor Green
venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
