# Backend - Buy / Wait Advisor

## Run locally

1. Create and activate a Python virtual environment:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and populate API keys.

4. Start the service:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API docs

Open `http://localhost:8000/docs` after startup.

## Endpoint

- POST `/api/compare`

Request body:
```json
{ "product": "iPhone 15" }
```

Response includes structured decision output and an AI-generated explanation.
