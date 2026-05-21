# Buy / Wait Advisor

A complete end-to-end product recommendation system:
- Backend: FastAPI + Python
- Frontend: React + Vite
- Integrations: SerpAPI for shopping listings and OpenAI for explanation text only

## Project structure

- `backend/` - API server and business logic
- `frontend/` - React web app

## Local setup

1. Create a Python virtual environment and activate it in the workspace root:
   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install backend dependencies:
   ```powershell
   pip install -r backend/requirements.txt
   ```

3. Create a `.env` file in the root using `.env.example` and provide:
   ```text
   SERP_API_KEY=your_serpapi_key
   OPENAI_API_KEY=your_openai_key
   BACKEND_URL=http://localhost:8000/api
   ```

4. Start the backend from the `backend/` folder:
   ```powershell
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Start the frontend:
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

## API Usage

POST `/api/compare`

Request body:
```json
{ "product": "iPhone 15" }
```

Successful response:
```json
{
  "product": "iPhone 15",
  "decision": "BUY",
  "confidence": 0.82,
  "reason": "Current best price is significantly below the median market price.",
  "market_maturity": { ... },
  "price_analysis": { ... },
  "explanation": "..."
}
```

## Testing scenarios

- Popular product: `iPhone`
- Fake product: `NonexistentGizmo314159`
- Low data product: `rare collector item`

## GitHub setup

```bash
git init
git add .
git commit -m "Initial Buy / Wait Advisor scaffold"
# create repo on GitHub and add remote
git remote add origin https://github.com/<your-org>/<your-repo>.git
git branch -M main
git push -u origin main
```

## Notes

- OpenAI is used only for explanation text, not decision logic.
- SerpAPI powers product search and shopping listing extraction.
- The architecture is modular and ready for future features like caching, price history, notifications, and personalization.
