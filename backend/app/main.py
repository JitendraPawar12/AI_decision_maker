from fastapi import FastAPI
from app.api.compare import router as compare_router
from app.utils.env import load_environment

load_environment()

app = FastAPI(
    title="Buy / Wait Advisor",
    description="A production-ready decision API that recommends BUY or WAIT using SerpAPI shopping data.",
    version="1.0.0",
)

app.include_router(compare_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "buy-wait-advisor"}
