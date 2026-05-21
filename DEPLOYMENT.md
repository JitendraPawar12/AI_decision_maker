# Deployment Guide

This project has a React frontend in `frontend/` and a FastAPI backend in `backend/`.

## 1. Deploy the backend

Use a service like Render, Railway, or Fly.io to deploy the backend.

### Render example
1. Create a new Web Service on Render.
2. Connect your GitHub repo: `https://github.com/JitendraPawar12/AI_decision_maker`
3. Set the root directory to `backend`.
4. Build command:
   ```bash
   pip install -r requirements.txt
   ```
5. Start command:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. Add environment variables:
   - `SERP_API_KEY`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (optional)

After deployment, note the public backend URL, for example:

```text
https://ai-decision-maker.onrender.com/api
```

## 2. Deploy the frontend

Use Vercel or Netlify to deploy the `frontend/` app.

### Vercel example
1. Create a new Vercel project and import the GitHub repo.
2. Set the project root to `frontend`.
3. Configure Build Command:
   ```bash
   npm install
   npm run build
   ```
4. Configure Output Directory:
   ```text
   dist
   ```
5. Set an environment variable:
   - `VITE_BACKEND_URL=https://<your-backend-domain>/api`

### Notes
- The frontend reads `VITE_BACKEND_URL` at build time.
- If you do not set it, it defaults to `http://localhost:8000/api`.

## 3. Share the link

After deployment, Vercel will give you a public URL such as:

```text
https://ai-decision-maker.vercel.app
```

Share that URL with anyone, and they can use the app in their browser.

## 4. Monetization ideas

- Add a paid plan or referral/affiliate links for product purchases.
- Add a Stripe checkout flow to unlock premium recommendations.
- Use the public link for marketing, social sharing, and paid traffic.

## 5. Recommended next step

If you want, I can also add a simple Stripe payment flow or a landing page to make this app monetizable.
