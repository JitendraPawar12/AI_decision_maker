from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.compare import router as compare_router
from app.utils.env import load_environment

load_environment()

app = FastAPI(
    title="Buy / Wait Advisor",
    description="A production-ready decision API that recommends BUY or WAIT using SerpAPI shopping data.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compare_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "buy-wait-advisor"}
