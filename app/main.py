from fastapi import FastAPI
from app.api.products import router as product_router

app = FastAPI()

app.include_router(product_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
