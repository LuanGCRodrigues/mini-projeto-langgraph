from fastapi import FastAPI
from app.routes.api import router as api_router

app = FastAPI(
    title="Seller System API",
    description="API de análise de compras",
    version="0.1.0"
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(api_router)
