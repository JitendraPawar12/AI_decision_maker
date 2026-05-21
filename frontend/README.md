# Frontend - Buy / Wait Advisor

## Run locally

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open the URL shown by Vite (usually `http://localhost:5173`).

## Behavior

- Enter a product name.
- Click "Get Recommendation." 
- The React app calls the backend and displays a BUY or WAIT recommendation with pricing details.

## Configuration

If your backend is hosted somewhere else, set the `VITE_BACKEND_URL` environment variable in your shell before running Vite:

```bash
export VITE_BACKEND_URL=http://localhost:8000/api
```
